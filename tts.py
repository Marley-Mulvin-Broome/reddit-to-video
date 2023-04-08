import pyttsx3
import gtts
from utility import remove_links_from_text
from enum import Enum


class TTSAccents(Enum):
    AUSTRALIA = 'com.au'
    UK = 'co.uk'
    US = 'us'
    CANADA = 'ca'
    INDIA = 'co.in'
    IRELAND = 'ie'
    SOUTH_AFRICA = 'co.za'


class googleTTS:
    def __init__(self, lang: str = 'en', accent: str = 'com.au'):
        self.lang = lang
        self.accent = accent

    def save_audio(self, text: str, filename: str) -> None:
        text = remove_links_from_text(text)
        tts = gtts.gTTS(text, lang=self.lang, tld=self.accent)
        tts.save(filename)


class systemTTS:
    def __init__(self, rate: int = 150):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', rate)

    def save_audio(self, text: str, filename: str) -> None:
        text = remove_links_from_text(text)
        self.engine.save_to_file(text, filename)

    def get_voices(self) -> list:
        return self.engine.getProperty('voices')

    def select_voice(self, voice) -> None:
        self.engine.setProperty('voice', voice.id)

    def run(self) -> None:
        self.engine.runAndWait()


class TTS:
    def __init__(self, engine: str = 'g', **kwargs):
        if engine == 'g':
            self.engine = googleTTS(**kwargs)
        elif engine == 's':
            self.engine = systemTTS(**kwargs)

    def save_audio(self, text: str, filename: str) -> None:
        self.engine.save_audio(text, filename)

    def get_voices(self) -> list:
        if not isinstance(self.engine, systemTTS):
            raise TypeError("get_voices() Engine is not systemTTS")

        return self.engine.get_voices()

    def select_voice(self, voice) -> None:
        if not isinstance(self.engine, systemTTS):
            raise TypeError("select_voice() Engine is not systemTTS")

        self.engine.select_voice(voice)

    def run(self) -> None:
        if not isinstance(self.engine, systemTTS):
            raise TypeError("run() Engine is not systemTTS")

        self.engine.run()

    @property
    def selected_engine(self) -> str:
        return self.engine.__class__.__name__
