Overview: 
With 29% of Canadians aged 65+ living alone, and rising concerns around chronic illness and mental health, there is a growing need for personalized, accessible solutions that support both seniors and their caregivers.
The goal of this project was to build a voice-activated smart medication reminder system designed to assist elderly individuals in managing their medication, while also supporting caregivers with real-time alerts and emotional insights.

Key Features:
✅ Personalized Voice Reminders to prompt users to take medications
🗣️ Voice Input Capture + Transcription to confirm user response
🤖 AI-based Medication Confirmation using speech input
📲 WhatsApp Alerts to caregivers if a dose is missed (includes timestamp)
📉 Sentiment Analysis to detect stress or emotional changes in the user's voice

Technical Breakdown: 

Core Language: Python

AI/ML Tools
ElevenLabs – Lifelike speech synthesis
Vosk – Offline speech recognition (English)
VADER (NLTK) – Sentiment analysis of user input

Supporting Tools & APIs
Firebase – Real-time database for user data and medication logs
Twilio API – WhatsApp messaging integration
Sounddevice – Captures voice input from the user
Custom Control Logic – Verifies inputs and updates medication status

How to Run:
Prerequisites:
Python 3.9+
Firebase project + credentials
Twilio account with WhatsApp setup
ElevenLabs API key

Future Improvements
UI dashboard for caregivers to monitor medication history
Multilingual support for diverse user groups
Improved sentiment model using large language models

<img width="441" height="275" alt="Hackathon" src="https://github.com/user-attachments/assets/564d9a59-ce53-447b-81d6-f141e3fe1117" />

