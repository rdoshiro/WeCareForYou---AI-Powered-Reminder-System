#libraries
import requests
import pygame
import time
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import json
import firebase_admin
from firebase_admin import credentials, firestore
from twilio.rest import Client
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialization

ELEVEN_API_KEY = "xxx"
VOICE_ID = "xxxx"

FIREBASE_KEY_PATH = "serviceaccountkey.json"

TWILIO_SID = "ACxxxxxx"
TWILIO_AUTH = "8cxxxx"
TWILIO_WHATSAPP_FROM = "whatsapp:+14155200000"
TWILIO_WHATSAPP_TO = "whatsapp:+1647000000"

GRANDCHILD_NAME = "Emma"
SENIOR_NAME = "Grandpa"
CAREGIVER_NAME = "Rohan"

MED_NAME = "Heart Pill"

VOSK_MODEL_PATH = "vosk-model-small-en-us-0.15"



# Firebase
cred = credentials.Certificate(FIREBASE_KEY_PATH)
try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app(cred)
db = firestore.client()

# Vosk
model = Model(VOSK_MODEL_PATH)

# Twilio
twilio_client = Client(TWILIO_SID, TWILIO_AUTH)

# VADER sentiment analyzer
vader_analyzer = SentimentIntensityAnalyzer()


def play_voice(text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {"xi-api-key": ELEVEN_API_KEY, "Content-Type": "application/json"}
    payload = {"text": text, "voice_settings": {"stability": 0.75, "similarity_boost": 0.85}}

    r = requests.post(url, headers=headers, json=payload)
    if r.status_code == 200:
        with open("alert.mp3", "wb") as f:
            f.write(r.content)
        pygame.mixer.init()
        pygame.mixer.music.load("alert.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
    else:
        print("TTS Error:", r.text)

def record_and_transcribe(duration=3, fs=16000):
    print(f"Recording for {duration} seconds... Speak now!")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    rec = KaldiRecognizer(model, fs)
    if rec.AcceptWaveform(audio.tobytes()):
        result = json.loads(rec.Result())
        return result['text'].lower()
    else:
        partial = json.loads(rec.PartialResult())
        return partial['partial']

def update_firestore(med_name, status):
    docs = db.collection("medications").where("medicine", "==", med_name).stream()
    for doc in docs:
        doc_ref = db.collection("medications").document(doc.id)
        doc_ref.update({"status": status})
    print(f"Firestore updated: {med_name} -> {status}")

def send_whatsapp_alert(caregiver_name, senior_name, message):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    message_text = f"Hi {caregiver_name}, {senior_name}: {message} at {now}."
    twilio_client.messages.create(
        body=message_text,
        from_=TWILIO_WHATSAPP_FROM,
        to=TWILIO_WHATSAPP_TO
    )
    print("WhatsApp alert sent.")

def analyze_sentiment(text):
    score = vader_analyzer.polarity_scores(text)['compound']
    if score >= 0.05:
        return "POSITIVE", score
    elif score <= -0.05:
        return "NEGATIVE", score
    else:
        return "NEUTRAL", score



def main():
    tts_message = f"{SENIOR_NAME}, this is {GRANDCHILD_NAME}. It's time for your {MED_NAME}. Please say 'Taken' when done."
    play_voice(tts_message)

    transcription = record_and_transcribe(duration=5)
    print("DEBUG transcription:", transcription)

    # --- Sentiment / stress detection ---
    sentiment_label, sentiment_score = analyze_sentiment(transcription)
    print(f"DEBUG sentiment: {sentiment_label} ({sentiment_score:.2f})")

    # --- Check medication confirmation ---
    confirmation_words = ["taken", "yes", "yes taken", "done"]
    if any(word in transcription for word in confirmation_words):
        print("✅ Medication confirmed!")
        update_firestore(MED_NAME, "taken")

    else:
        print("⚠️ No confirmation detected.")
        update_firestore(MED_NAME, "missed")
        send_whatsapp_alert(CAREGIVER_NAME, SENIOR_NAME, f"{MED_NAME} missed")



    if sentiment_label == "NEGATIVE" and sentiment_score < -0.4:  # threshold for stress/unusual behavior
        send_whatsapp_alert(CAREGIVER_NAME, SENIOR_NAME, f"Unusual emotion detected in speech: {sentiment_label}")

# Run app
if __name__ == "__main__":
    main()
