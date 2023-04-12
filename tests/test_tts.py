import pytest

from reddit_to_video.video.tts import get_tts_engine, GoogleTTS, SystemTTS, CoquiTTS


tts_engines = [("google", GoogleTTS), ("system",
                                       SystemTTS)]


@pytest.mark.parametrize("tts_engine_str, tts_engine", tts_engines)
def test_tts_get_engine(tts_engine_str, tts_engine):
    assert isinstance(get_tts_engine(tts_engine_str), tts_engine)


def test_tts_get_engine_invalid():
    with pytest.raises(ValueError):
        get_tts_engine("Invalid")


def test_system_tts_get_voices():
    tts = SystemTTS()
    assert isinstance(tts.get_voices(), list)


def test_system_tts_select_voice():
    tts = SystemTTS()
    voices = tts.get_voices()
    tts.select_voice(voices[0])


def test_system_tts_run():
    tts = SystemTTS()
    tts.run()


def test_system_tts_selected_engine():
    tts = SystemTTS()
    assert tts.selected_engine == "systemTTS"


def test_google_tts_selected_engine():
    tts = GoogleTTS()
    assert tts.selected_engine == "googleTTS"
