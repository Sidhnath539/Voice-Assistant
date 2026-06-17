# Jarvis Voice Assistant using Python

## Project Overview

Jarvis is a Python-based voice assistant that can perform various tasks through voice commands or text commands. The assistant uses speech recognition, text-to-speech technology, and web automation to provide an interactive user experience.

Unlike traditional implementations that depend on PyAudio, this project uses **Sounddevice** for recording audio, making it compatible with newer Python versions such as Python 3.14.

---

# Features

### Voice Recognition

* Listen to user commands using a microphone.
* Convert speech into text using Google Speech Recognition.
* Support for text mode if the microphone is unavailable.

### Text-to-Speech

* Speak responses using `pyttsx3`.
* Read jokes, Wikipedia summaries, and user-provided text.

### Personal Information

* Remember the user's name.
* Recall the user's name later.

### Date and Time

* Tell the current time.
* Tell the current date.

### Web Automation

* Open YouTube.
* Open Google.
* Open GitHub.
* Open Stack Overflow.

### Application Automation

* Open Notepad.
* Open Calculator.

### Search and Information

* Search Google.
* Search Wikipedia.

### Entertainment

* Play songs on YouTube.
* Tell English jokes.
* Tell Hindi jokes.

### Text Reading

* Read any text spoken by the user.

---

# Technologies Used

* Python 3.14
* Sounddevice
* SpeechRecognition
* Pyttsx3
* Wikipedia
* PyWhatKit
* PyJokes
* Scipy
* JSON

---

# Project Structure

```text
Jarvis/
│
├── jarvis.py
├── README.md
├── requirements.txt
└── .jarvis_data.json
```

---

# Installation

## Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/jarvis-assistant.git
cd jarvis-assistant
```

---

## Step 2: Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Step 3: Install Required Packages

```bash
pip install sounddevice
pip install scipy
pip install SpeechRecognition
pip install pyttsx3
pip install wikipedia
pip install pywhatkit
pip install pyjokes
```

Or:

```bash
pip install -r requirements.txt
```

---

# requirements.txt

```text
sounddevice
scipy
SpeechRecognition
pyttsx3
wikipedia
pywhatkit
pyjokes
numpy
```

---

# Running the Project

## Voice Mode

```bash
python jarvis.py
```

## Text Mode

```bash
python jarvis.py --text
```

## Disable Speech Output

```bash
python jarvis.py --no-speak
```

---

# Supported Commands

## Greeting Commands

```text
hello
hi
hey
```

---

## User Information

```text
my name is Siddhnath
what is my name
```

---

## Date and Time

```text
what is the time
tell me the date
```

---

## Open Websites

```text
open youtube
open google
open github
open stackoverflow
```

---

## Open Applications

```text
open notepad
open calculator
```

---

## Search Commands

```text
search for python programming
```

---

## Wikipedia

```text
who is Narendra Modi
what is artificial intelligence
wikipedia python
```

---

## Music

```text
play shape of you
play beliver song
```

---

## Jokes

```text
tell me a joke
say a joke
hindi joke
another joke
```

---

## Read Text

```text
say hello everyone
speak welcome to my project
read this sentence
```

---

## Exit

```text
exit
quit
stop
goodbye
```

---

# How It Works

## Voice Input

1. The microphone records audio using Sounddevice.
2. Audio is temporarily stored in WAV format.
3. SpeechRecognition converts the audio into text.

## Command Processing

1. User input is converted to lowercase.
2. Regular expressions identify commands.
3. Corresponding actions are executed.

## Text-to-Speech

The assistant responds using pyttsx3.

---

# Modules Description

## load_data()

Loads saved user information.

## save_data()

Stores user information in JSON format.

## say()

Prints and speaks text.

## hear_once()

Records and recognizes voice commands.

## handle_command()

Processes all user commands.

## run()

Runs the assistant in text mode or voice mode.

## main()

Parses command-line arguments and starts Jarvis.

---

# Future Enhancements

* Weather Forecast API
* Email Sending
* WhatsApp Messaging
* Face Recognition
* Object Detection
* ChatGPT Integration
* System Control Commands
* Reminder System
* Alarm Clock
* GUI Interface
* Database Integration

---

# Advantages

* Easy to use.
* Works on Python 3.14.
* Does not require PyAudio.
* Supports voice and text mode.
* Cross-platform compatibility.

---

# Limitations

* Requires internet for Google Speech Recognition.
* Limited command set.
* Fixed recording duration.
* No wake-word detection.

---

# Author

**Siddhnath Prajapati**

Python Developer | Student

---

# License

This project is developed for educational and learning purposes.
