# coding=utf-8

__author__ = 'Alexandre Plateau'
"""
Licence MIT
Voir le GUIDELINES avant de modifier quoi que ce soit
User et abuser de # todo : note
"""

from . import sr
from . import colors


class SpeechRecognition:
    def __init__(self, engine, language="en-US", names=[""]):
        self.engine = engine
        self.language = language
        self.recognizer = sr.Recognizer(language)
        self.recognizer.pause_threshold = 1
        self.recognizer.energy_threshold = 2500
        self.names = names

    def listen(self):
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source)
        try:
            work = self.recognizer.recognize(audio)
            return work
        except LookupError:
            return -1

    def you_talk_to_me(self):
        o = self.listen()
        if not isinstance(o, int):
            if o.lower().strip() in [c.lower().strip() for c in self.names]:
                return self.recognize()
        return None

    def speak(self, texte):
        self.engine.say(texte)
        self.engine.runAndWait()

    def recognize(self):
        self.speak("Yes Sir ?")
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source, timeout=5)
        try:
            work = self.recognizer.recognize(audio)
            return work
        except LookupError:
            return -1