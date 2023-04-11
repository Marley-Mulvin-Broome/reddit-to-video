"""Text to speech module for reddit_to_video

Classes:
    ttsEngine: Base class for TTS engines
    coquiTTS: Coqui TTS engine
    googleTTS: Google TTS engine
    pyttsx3TTS: pyttsx3 TTS engine
    TTSAccents: Enum for Google TTS accents

Functions:
    get_tts_engine: Get a TTS engine

"""

from enum import Enum
import gtts
import pyttsx3

from reddit_to_video.utility import remove_links_from_text, remove_non_words

class TTSAccents(Enum):
    """List of accents for the Google Translate TTS engines"""
    AUSTRALIA = 'com.au'
    UK = 'co.uk'
    US = 'us'
    CANADA = 'ca'
    INDIA = 'co.in'
    IRELAND = 'ie'
    SOUTH_AFRICA = 'co.za'

    # from https://stackoverflow.com/questions/29795488/how-to-test-if-an-enum-member-with-a-certain-name-exists
    @classmethod
    def has_key(cls, name):
        """Check if an enum has a key"""
        return name in cls.__members__

    @classmethod
    def get_keys(cls):
        """Get all the keys in an enum"""
        return cls.__members__.keys()


class ttsEngine:
    def save_audio(self, text: str, filename: str) -> None:
        """Save the audio to a file"""
        raise NotImplementedError("save_audio() is not implemented")

    def get_voices(self) -> list:
        """Get a list of voices"""
        raise NotImplementedError("get_voices() is not implemented")

    def select_voice(self, voice_id: str) -> None:
        """Select a voice"""
        raise NotImplementedError("select_voice() is not implemented")

    def run(self) -> None:
        """Run the TTS engine"""
        raise NotImplementedError("run() is not implemented")

    @property
    def selected_engine(self) -> str:
        """Get the selected engine"""
        raise NotImplementedError("selected_engine() is not implemented")


class coquiTTS(ttsEngine):
    """Coqui TTS engine"""
    def __init__(self, model: str = "tts_models/multilingual/multi-dataset/your_tts", speaker_file: str = None, **kwargs):
        """Coqui TTS engine"""
        # importing this here because it takes a while to load
        from TTS.api import TTS as coqui

        self.model = model
        self.tts = coqui(model, progress_bar=False)

        self.speaker_file = speaker_file

        self.kwargs = kwargs

        if self.kwargs is None:
            self.kwargs = {}

        if self.speaker_file is not None:
            self.kwargs['speaker_wav'] = self.speaker_file

    def save_audio(self, text: str, filename: str) -> None:
        """Save the audio to a file"""
        text = remove_links_from_text(text)
        self.tts.tts_to_file(text, file_path=filename, **self.kwargs)

    def get_voices(self) -> list:
        """Get a list of voices"""
        return self.tts.list_models()

    def __repr__(self) -> str:
        return "coquiTTS"


class googleTTS(ttsEngine):
    """Google Translate TTS engine"""
    def __init__(self, lang: str = 'en', accent: str = 'com.au'):
        """Google Translate TTS engine"""
        self.lang = lang
        self.accent = accent

    def save_audio(self, text: str, filename: str) -> None:
        """Save the audio to a file"""
        text = remove_links_from_text(text)
        text = remove_non_words(text)
        # print("Writing text" + text)
        tts = gtts.gTTS(text, lang=self.lang, tld=self.accent)
        tts.save(filename)

    def __repr__(self) -> str:
        return "googleTTS"


class systemTTS(ttsEngine):
    """System TTS engine"""
    def __init__(self, rate: int = 150):
        """System TTS engine"""
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', rate)

    def save_audio(self, text: str, filename: str) -> None:
        """Save the audio to a file"""
        text = remove_links_from_text(text)
        self.engine.save_to_file(text, filename)

    def get_voices(self) -> list:
        """Get a list of voices"""
        return self.engine.getProperty('voices')

    def select_voice(self, voice_id: str) -> None:
        """Select a voice"""
        self.engine.setProperty('voice', voice_id)

    def run(self) -> None:
        """Run the TTS engine"""
        self.engine.runAndWait()

    def __repr__(self) -> str:
        return "systemTTS"


google_names = ["g", "google"]
system_names = ["s", "system"]
coqui_names = ["c", "coqui"]

all_tts_names = google_names + system_names + coqui_names


def get_tts_engine(engine: str, **kwargs) -> ttsEngine:
    """Get a TTS engine based on a string"""
    if engine in google_names:
        return googleTTS(**kwargs)
    elif engine in system_names:
        return systemTTS(**kwargs)
    elif engine in coqui_names:
        return coquiTTS(**kwargs)

    raise ValueError("Unknown engine: " + engine)
