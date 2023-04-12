import pytest

import os
from os.path import join as path_join

from reddit_to_video.video.scriptelement import ScriptElement
from reddit_to_video.video.script import VideoScript
from reddit_to_video.exceptions import ScriptElementTooLongError, NotInCollectionError


def get_current_dir() -> str:
    """Returns the current directory"""
    return os.path.dirname(os.path.realpath(__file__))


image_file = path_join(get_current_dir(), "image.png")
video_file = path_join(get_current_dir(), "video.mp4")
audio_file = path_join(get_current_dir(), "audio.mp3")

image_audio_element = ScriptElement("", image_file, audio_file)
video_element = ScriptElement("", video_file, None)
text_element = ScriptElement("Hello World!", video_file, None)

valid_init_params = [
    (0, 0, None, None),
    (0, 0, [image_audio_element], None),
    (0, 0, [image_audio_element, video_element], None),
    (0, 0, None, [image_audio_element, video_element]),
    (0, 0, [image_audio_element], [image_audio_element, video_element]),
    (100000, 0, [image_audio_element], [image_audio_element, video_element]),
    (0, 5, [image_audio_element], [image_audio_element, video_element]),
]


@pytest.mark.parametrize("max_length, min_length, script_elements, footer_elements", valid_init_params)
def test_valid_init(max_length, min_length, script_elements, footer_elements):
    try:
        VideoScript(max_length, min_length, script_elements,
                    footer_elements)
    except Exception as e:
        pytest.fail(f"VideoScript() raised {e} unexpectedly!")


invalid_init_params = [
    (-490, 0, None, None),
    (0, -10892824, None, None),
]


@pytest.mark.parametrize("max_length, min_length, script_elements, footer_elements", invalid_init_params)
def test_invalid_init(max_length, min_length, script_elements, footer_elements):
    with pytest.raises((ValueError, ScriptElementTooLongError)):
        VideoScript(max_length, min_length, script_elements,
                    footer_elements)


def test_finished_true():
    video_script = VideoScript(0, 5, [image_audio_element], None)
    assert video_script.finished is True


def test_finished_false():
    video_script = VideoScript(0, 5000, [image_audio_element], None)
    assert video_script.finished is False


def test_finished_no_min():
    video_script = VideoScript(0, 0, [image_audio_element], None)
    assert video_script.finished is True


def test_script():
    video_script = VideoScript(
        0, 0, [image_audio_element, video_element], None)
    assert video_script.script == "\n".join(
        [image_audio_element.text, video_element.text])


def test_duration():
    video_script = VideoScript(
        0, 0, [image_audio_element, video_element], None)
    assert video_script.duration == image_audio_element.duration + video_element.duration


def test_all():
    video_script = VideoScript(
        0, 0, [image_audio_element, video_element], [text_element])
    assert video_script.all == [
        image_audio_element, video_element, text_element]


def test_all_no_footer():
    video_script = VideoScript(
        0, 0, [image_audio_element, video_element], None)
    assert video_script.all == [image_audio_element, video_element]


def test_all_empty():
    video_script = VideoScript(0, 0, None, None)
    assert video_script.all == []


def test_can_add_true():
    video_script = VideoScript(0, 0, None, None)
    assert video_script.can_add_script_element(image_audio_element) is True


def test_can_add_false():
    video_script = VideoScript(
        image_audio_element.duration + 1, 0, [image_audio_element], None)
    assert video_script.can_add_script_element(image_audio_element) is False


def test_can_add_false_footer():
    video_script = VideoScript(
        image_audio_element.duration + 1, 0, None, [image_audio_element])
    assert video_script.can_add_script_element(image_audio_element) is False


def test_add_script_element():
    video_script = VideoScript(0, 0, None, None)
    video_script.add_script_element(image_audio_element)
    assert video_script.script_elements == [image_audio_element]


def test_add_script_element_false():
    video_script = VideoScript(
        image_audio_element.audio_duration + 1, 0, None, None)
    with pytest.raises(ScriptElementTooLongError):
        video_script.add_script_element(image_audio_element)
        video_script.add_script_element(image_audio_element)


def test_add_script_element_footer():
    video_script = VideoScript(0, 0, None, None)
    video_script.add_script_element(image_audio_element, footer=True)
    assert video_script.footer_elements == [image_audio_element]


def test_add_script_element_footer_false():
    video_script = VideoScript(
        image_audio_element.audio_duration + 1, 0, None, None)
    with pytest.raises(ScriptElementTooLongError):
        video_script.add_script_element(image_audio_element, footer=True)
        video_script.add_script_element(image_audio_element, footer=True)


def test_add_script_element_pair():
    video_script = VideoScript(0, 0, None, None)
    video_script.add_script_element_pair(image_audio_element, text_element)
    assert video_script.script_elements == [image_audio_element, text_element]


def test_add_script_element_pair_false():
    video_script = VideoScript(
        image_audio_element.duration + 1, 0, None, None)
    with pytest.raises(ScriptElementTooLongError):
        video_script.add_script_element_pair(
            image_audio_element, image_audio_element)


def test_add_script_element_pair_footer():
    video_script = VideoScript(0, 0, None, None)
    video_script.add_script_element_pair(
        image_audio_element, text_element, footer=True)
    assert video_script.footer_elements == [image_audio_element, text_element]


def test_add_script_element_pair_footer_false():
    video_script = VideoScript(
        image_audio_element.duration + 1, 0, None, None)
    with pytest.raises(ScriptElementTooLongError):
        video_script.add_script_element_pair(
            image_audio_element, text_element, footer=True)


def test_add_script_elements():
    video_script = VideoScript(0, 0, None, None)
    video_script.add_script_elements([image_audio_element, video_element])
    assert video_script.script_elements == [image_audio_element, video_element]


def test_add_script_elements_one():
    video_script = VideoScript(
        image_audio_element.duration + 1, 0, None, None)
    assert video_script.add_script_elements(
        [image_audio_element, video_element]) == 1


def test_add_script_elements_empty():
    video_script = VideoScript(0, 0, None, None)
    assert video_script.add_script_elements([]) == 0


def test_add_script_elements_footer():
    video_script = VideoScript(0, 0, None, None)
    video_script.add_script_elements(
        [image_audio_element, video_element], footer=True)
    assert video_script.footer_elements == [image_audio_element, video_element]


def test_add_script_elements_footer_one():
    video_script = VideoScript(
        image_audio_element.duration + 1, 0, None, None)
    assert video_script.add_script_elements(
        [image_audio_element, video_element], footer=True) == 1


def test_add_script_elements_footer_empty():
    video_script = VideoScript(0, 0, None, None)
    assert video_script.add_script_elements([], footer=True) == 0


def test_add_script_element_pairs():
    video_script = VideoScript(0, 0, None, None)
    video_script.add_script_element_pairs(
        [(image_audio_element, text_element), (video_element, text_element)])
    assert video_script.script_elements == [
        image_audio_element, text_element, video_element, text_element]


def test_add_script_element_pairs_one():
    video_script = VideoScript(
        image_audio_element.duration + text_element.duration + 1, 0, None, None)
    assert video_script.add_script_element_pairs(
        [(image_audio_element, text_element), (video_element, text_element)]) == 1
    assert video_script.script_elements == [image_audio_element, text_element]


def test_add_script_element_pairs_empty():
    video_script = VideoScript(0, 0, None, None)
    assert video_script.add_script_element_pairs([]) == 0


def test_add_script_element_pairs_footer():
    video_script = VideoScript(0, 0, None, None)
    video_script.add_script_element_pairs(
        [(image_audio_element, text_element), (video_element, text_element)], footer=True)
    assert video_script.footer_elements == [
        image_audio_element, text_element, video_element, text_element]


def test_add_script_element_pairs_footer_one():
    video_script = VideoScript(
        image_audio_element.duration + text_element.duration + 1, 0, None, None)
    assert video_script.add_script_element_pairs(
        [(image_audio_element, text_element), (video_element, text_element)], footer=True) == 1
    assert video_script.footer_elements == [image_audio_element, text_element]


def test_add_script_element_pairs_footer_empty():
    video_script = VideoScript(0, 0, None, None)
    assert video_script.add_script_element_pairs([], footer=True) == 0


def test_get_script_element():
    video_script = VideoScript(0, 0, None, None)
    video_script.add_script_elements([image_audio_element, video_element])
    assert video_script.get_script_element(
        image_audio_element.id) == (image_audio_element, False)
    assert video_script.get_script_element(
        video_element.id) == (video_element, False)


def test_get_script_element_none():
    video_script = VideoScript(0, 0, None, None)
    with pytest.raises(NotInCollectionError):
        video_script.get_script_element(image_audio_element.id)


def test_get_script_element_footer():
    video_script = VideoScript(0, 0, None, None)
    video_script.add_script_elements(
        [image_audio_element, video_element], footer=True)
    assert video_script.get_script_element(
        image_audio_element.id) == (image_audio_element, True)
    assert video_script.get_script_element(
        video_element.id) == (video_element, True)


def test_has_script_element():
    video_script = VideoScript(0, 0, None, None)
    video_script.add_script_elements([image_audio_element, video_element])
    assert video_script.has_script_element(image_audio_element.id)
    assert video_script.has_script_element(video_element.id)


def test_has_script_elemnet_none():
    video_script = VideoScript(0, 0, None, None)
    assert not video_script.has_script_element(image_audio_element.id)


def test_has_script_element_footer():
    video_script = VideoScript(0, 0, None, None)
    video_script.add_script_elements(
        [image_audio_element, video_element], footer=True)
    assert video_script.has_script_element(image_audio_element.id)
    assert video_script.has_script_element(video_element.id)


def test_remove_script_element():
    video_script = VideoScript(0, 0, None, None)
    video_script.add_script_elements([image_audio_element, video_element])
    video_script.remove_script_element(image_audio_element.id)
    assert video_script.script_elements == [video_element]


def test_remove_script_element_none():
    video_script = VideoScript(0, 0, None, None)
    with pytest.raises(NotInCollectionError):
        video_script.remove_script_element(image_audio_element.id)


def test_remove_script_element_footer():
    video_script = VideoScript(0, 0, None, None)
    video_script.add_script_elements(
        [image_audio_element, video_element], footer=True)
    video_script.remove_script_element(image_audio_element.id)
    assert video_script.footer_elements == [video_element]


def test_remove_script_element_footer_none():
    video_script = VideoScript(0, 0, None, None)
    with pytest.raises(NotInCollectionError):
        video_script.remove_script_element(image_audio_element.id)


def test_len():
    video_script = VideoScript(0, 0, None, None)
    video_script.add_script_elements([image_audio_element, video_element])
    assert len(video_script) == 2


def test_len_footer():
    video_script = VideoScript(0, 0, None, None)
    video_script.add_script_elements(
        [image_audio_element, video_element], footer=True)
    assert len(video_script) == 2


def test_len_none():
    video_script = VideoScript(0, 0, None, None)
    assert len(video_script) == 0
