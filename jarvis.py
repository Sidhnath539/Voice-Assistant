
from __future__ import annotations
import argparse
import json
import random
import re
import sys
import webbrowser
import subprocess
import os
import tempfile
from datetime import datetime
from pathlib import Path

# Sounddevice imports (instead of PyAudio)
try:
    import sounddevice as sd
    from scipy.io.wavfile import write
except ImportError:
    sd = None

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

try:
    import speech_recognition as sr
except ImportError:
    sr = None

try:
    import wikipedia
    wikipedia.set_lang("en")
except ImportError:
    wikipedia = None

try:
    import pywhatkit as kit
except ImportError:
    kit = None

try:
    import pyjokes
except ImportError:
    pyjokes = None

DATA_FILE = Path.home() / ".jarvis_data.json"


def load_data():
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def save_data(data):
    try:
        DATA_FILE.write_text(
            json.dumps(data, indent=2),
            encoding="utf-8"
        )
    except Exception:
        pass


engine = None
if pyttsx3:
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 180)
    except Exception:
        pass


def say(text, speak=True):
    print(f"Jarvis: {text}")

    if not speak or engine is None:
        return

    try:
        engine.say(text)
        engine.runAndWait()
    except Exception:
        pass


def get_english_joke():
    if pyjokes:
        try:
            return pyjokes.get_joke()
        except Exception:
            pass

    return (
        "Why do programmers prefer dark mode? Because light attracts bugs."
    )


def get_hindi_joke():
    jokes = [
        "कंप्यूटर की शादी में सिर्फ एक ही बात की कमी थी — वह भी एकदम सही नहीं था!",
        "मुझे फोन का डर लगता है, क्योंकि हर बार उसकी आवाज़ में कोई न कोई 'कनेक्ट' होता है!",
        "मैंने अपने दोस्त से पूछा, तुम इतने खुश क्यों हो? उसने कहा, क्योंकि मैं अपने दिमाग को इंटरनेट से अलग रखता हूँ!",
        "डॉक्टर ने कहा, आप बहुत ज़्यादा काम करते हैं। मैंने कहा, हाँ, मैं सिर्फ अपने काम की 'बैकअप' नहीं लेता!"
    ]
    return random.choice(jokes)


# --------- Voice Input Using Sounddevice ---------
def hear_once(timeout=5, phrase_time_limit=6):
    if sr is None:
        return None, "SpeechRecognition not installed"

    if sd is None:
        return None, "sounddevice not installed"

    try:
        recognizer = sr.Recognizer()

        fs = 16000
        duration = phrase_time_limit

        print("Listening...")

        recording = sd.rec(
            int(duration * fs),
            samplerate=fs,
            channels=1,
            dtype="int16"
        )

        sd.wait()

        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        ) as temp_audio:
            temp_filename = temp_audio.name

        write(temp_filename, fs, recording)

        with sr.AudioFile(temp_filename) as source:
            audio = recognizer.record(source)

        print("Recognizing...")

        text = recognizer.recognize_google(
            audio,
            language="en-US"
        ).lower()

        os.remove(temp_filename)

        return text, None

    except sr.UnknownValueError:
        return None, "Could not understand audio"

    except sr.RequestError as e:
        return None, str(e)

    except Exception as e:
        return None, str(e)


def handle_command(cmd, speak, data):
    c = cmd.strip().lower()

    if not c:
        say("I didn't catch that. Please try again.", speak)
        return True

    # Exit
    if any(word in c for word in
           ["exit", "quit", "stop", "goodbye"]):
        say("Goodbye!", speak)
        return False

    # Greeting
    if re.search(r"^(hi|hello|hey)\b", c):
        name = data.get("name")
        say(
            f"Hello {name if name else 'there'}! "
            "How can I help you?",
            speak
        )
        return True

    # Save name
    m = re.search(r"my name is (\w+)", c)
    if m:
        name = m.group(1).capitalize()
        data["name"] = name
        save_data(data)
        say(f"Nice to meet you, {name}!", speak)
        return True

    # Text to speech
    m = re.search(r"^(say|speak|read)\s+(.+)", c)
    if m:
        text_to_speak = m.group(2).strip()
        if text_to_speak:
            say(text_to_speak, speak)
        else:
            say("Please provide something for me to speak.", speak)
        return True

    # Recall name
    if "what is my name" in c or "what's my name" in c:
        name = data.get("name")
        if name:
            say(f"Your name is {name}.", speak)
        else:
            say("I don't know your name yet.", speak)
        return True

    # Time
    if "time" in c:
        now = datetime.now().strftime("%I:%M %p")
        say(f"The current time is {now}.", speak)
        return True

    # Date
    if "date" in c:
        today = datetime.now().strftime("%A, %B %d, %Y")
        say(f"Today is {today}.", speak)
        return True

    # Websites
    if "open youtube" in c:
        webbrowser.open("https://www.youtube.com")
        say("Opening YouTube.", speak)
        return True

    if "open google" in c:
        webbrowser.open("https://www.google.com")
        say("Opening Google.", speak)
        return True

    if "open github" in c:
        webbrowser.open("https://github.com")
        say("Opening GitHub.", speak)
        return True

    if "open stackoverflow" in c:
        webbrowser.open("https://stackoverflow.com")
        say("Opening Stack Overflow.", speak)
        return True

    # Open Notepad
    if "open notepad" in c:
        try:
            if sys.platform.startswith("win"):
                subprocess.Popen(["notepad.exe"])
            else:
                subprocess.Popen(["gedit"])

            say("Opening Notepad.", speak)
        except Exception:
            say("Unable to open Notepad.", speak)

        return True

    # Open Calculator
    if "open calculator" in c:
        try:
            if sys.platform.startswith("win"):
                subprocess.Popen(["calc.exe"])
            elif sys.platform == "darwin":
                subprocess.Popen(["open", "-a", "Calculator"])
            else:
                subprocess.Popen(["gnome-calculator"])

            say("Opening Calculator.", speak)
        except Exception:
            say("Unable to open Calculator.", speak)

        return True

    # Play song
    m = re.search(r"play (.+)", c)
    if m and kit:
        song = m.group(1).strip()

        try:
            kit.playonyt(song)
        except Exception:
            webbrowser.open(
                f"https://www.youtube.com/results?"
                f"search_query={song}"
            )

        say(f"Playing {song}.", speak)
        return True

    # Google Search
    m = re.search(r"search for (.+)", c)
    if m:
        query = m.group(1).strip()

        webbrowser.open(
            f"https://www.google.com/search?"
            f"q={query.replace(' ', '+')}"
        )

        say(f"Searching for {query}.", speak)
        return True

    # Wikipedia
    if wikipedia:
        m = re.search(
            r"(who is|what is|wikipedia) (.+)",
            c
        )

        if m:
            topic = m.group(2)

            try:
                summary = wikipedia.summary(
                    topic,
                    sentences=2
                )

                say(summary, speak)

            except wikipedia.exceptions.DisambiguationError as e:
                say(
                    f"Too many results. "
                    f"Try {e.options[:5]}",
                    speak
                )

            except Exception:
                say(
                    f"Sorry, I couldn't find "
                    f"information on {topic}.",
                    speak
                )

            return True

    # Joke
    if "joke" in c or "jokes" in c:
        if "hindi" in c or "hindhi" in c:
            joke = get_hindi_joke()
            say(
                f"Sure, here is a joke in Hindi: {joke}",
                speak
            )
        else:
            joke = get_english_joke()
            say(
                f"Sure, here is a joke: {joke}",
                speak
            )
        return True

    say(
        "Sorry, I don't understand that command.",
        speak
    )

    return True


def run(text_mode=False, speak=True):
    data = load_data()

    if text_mode:
        say(
            "Jarvis is now online in text mode.",
            speak
        )

        while True:
            try:
                cmd = input("You: ")

            except (EOFError, KeyboardInterrupt):
                say("Goodbye!", speak)
                break

            if not handle_command(
                    cmd,
                    speak,
                    data):
                break

    else:
        say(
            "Jarvis is now online. "
            "Say quit to exit.",
            speak
        )

        while True:
            cmd, error = hear_once()

            if error or not cmd:
                say(
                    "Sorry, I didn't catch that.",
                    speak
                )
                continue

            print(f"You: {cmd}")

            if not handle_command(
                    cmd,
                    speak,
                    data):
                break


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--text",
        action="store_true",
        help="Run in text mode"
    )

    parser.add_argument(
        "--no-speak",
        action="store_true",
        help="Disable speech"
    )

    args = parser.parse_args()

    run(
        text_mode=args.text,
        speak=not args.no_speak
    )


if __name__ == "__main__":
    main()

