import pytest

from reddit_to_video.utility import remove_links_from_text, get_audio_duration

links = [
    ("www.twitter.com/deeznuts?lol=1",
     "Yo www.twitter.com/deeznuts?lol=1 twitter moment"),
    ("https://www.youtube.com/watch?v=dQw4w9WgXcQ",
     "Yo https://www.youtube.com/watch?v=dQw4w9WgXcQ youtube moment"),
    ("https://www.youtube.com/watch?v=dQw4w9WgXcQ&feature=youtu.be",
     "Yo https://www.youtube.com/watch?v=dQw4w9WgXcQ&feature=youtu.be youtube moment"),
    ("https://www.youtube.com/watch?v=dQw4w9WgXcQ&feature=youtu.be&t=1",
     "Yo https://www.youtube.com/watch?v=dQw4w9WgXcQ&feature=youtu.be&t=1 youtube moment"),
    ("https://www.youtube.com/watch?v=dQw4w9WgXcQ&feature=youtu.be&t=1",
     "Yo This has a link in brackets (https://www.youtube.com/watch?v=dQw4w9WgXcQ&feature=youtu.be&t=1) youtube moment"),
]

no_links = [
    ("Yo what this is based"),
    ("!!!!waht the twitter moment"),
    ("Email me at cat@gmail.com")
]


@pytest.mark.parametrize("link, text", links)
def test_remove_links_from_text(link, text):
    assert link not in remove_links_from_text(text)


@pytest.mark.parametrize("text", no_links)
def test_remove_links_from_text_no_links(text):
    assert remove_links_from_text(text) == text


def test_invalid_file_path():
    with pytest.raises(FileNotFoundError):
        get_audio_duration("invalid_file_path.mp3")


def test_invalid_file_type():
    with pytest.raises(ValueError):
        get_audio_duration("tests/test_utility.py")
