import pytest

from copy import deepcopy
from json import dumps as dumps_json

from reddit_to_video.video.config import VideoConfig, validate_json_val
from reddit_to_video.exceptions import ConfigKeyError

# All posts require a name, description, and settings
# all settings requires a type
# All settings requires a subreddit, sort, time, limit, max_length, min_length, export settings
# Settings can have a target_resolution
#       target_resolution requires a width and height
# Comment posts
#   require a background_footage, tts
#   tts requires an engine and kwargs
#   google engine kwargs requires an accent
#   system engine kwargs requires a voice and rate
#   tts kwargs can't have a key that isn't in the engine's kwargs (Not testing right now)
#   coqui engine kwargs requires a model_name or model_path
# All settings requires an export settings
#   export settings requires a name, fps, threads, bitrate, and compression
#
# Video posts
#  require a end_card_footage, video_break_footage, max_video_length, noramlise_audio (negative float)

validate_json_types = [
    ({"number": 1}, "number", int, False),
    ({"number": 1.0}, "number", float, False),
    ({"number": 1.0}, "number", (int, float), False),
    ({"number": 1}, "number", (int, float), False),
    ({"number": "string"}, "number", int, True),
    ({"number": "string"}, "number", (int, float), True),
    ({"number": []}, "number", str, True),
    ({"number": []}, "number", list, False),
]


@pytest.mark.parametrize("json, key, type, should_raise", validate_json_types)
def test_validate_json_types(json, key, type, should_raise):
    if should_raise:
        with pytest.raises(TypeError):
            validate_json_val(json, key, type)
    else:
        validate_json_val(json, key, type)


validate_json_optional = [
    ({"number": 1}, "number", int, False),
    ({"cat ": 42}, "number", int, True),
]


# test that it doesn't throw
@pytest.mark.parametrize("json, key, type, optional", validate_json_optional)
def test_validate_json_optional(json, key, type, optional):
    assert validate_json_val(json, key, type, optional) is None


validate_json_in_list = [
    ({"number": 1}, "number", [1, 2, 3], False),
    ({"number": 1}, "number", [2, 3, 4], True),
]


@pytest.mark.parametrize("json, key, in_list, should_raise", validate_json_in_list)
def test_validate_json_in_list(json, key, in_list, should_raise):
    if should_raise:
        with pytest.raises(ValueError):
            validate_json_val(json, key, int, in_list=in_list)
    else:
        validate_json_val(json, key, int, in_list=in_list)


valid_video_json = {
    "name": "YouTube haiku",
    "description": "Downloads top videos from r/youtubehaiku this month",
    "settings": {
        "type": "video",
        "subreddit": "youtubehaiku",
        "sort": "top",
        "time": "all",
        "limit": 150,
        "max_length": 600,
        "min_length": 300,
        "min_upvotes": 100,
        "max_video_length": 30,
        "end_card_footage": "E:\\YT\\EndCard.mp4",
        "video_break_footage": "E:\\YT\\transitions\\TV Static.mp4",
        "target_resolution": {
            "width": 1920,
            "height": 1080
        },
        "export_settings": {
            "codec": "mpeg4",
            "bitrate": "16000k",
            "fps": 30,
            "threads": 10,
            "compression": "UltraFast"
        }
    }
}

valid_comment_json = {
    "name": "Askreddit comments top all time",
    "description": "Makes a video from Reddit comments on a post",
    "settings": {
            "type": "comment",
            "subreddit": "askreddit",
            "sort": "top",
            "time": "all",
            "limit": 10,
            "max_length": 60,
            "min_length": 30,
            "background_footage": "E:/YT/bgfootage/satisfying mc prk.mp4",
            "tts": {
                "engine": "google",
                "kwargs": {
                    "accent": "AUSTRALIA"
                }
            },
        "export_settings": {
                "codec": "mpeg4",
                "bitrate": "16000k",
                "fps": 60,
                "threads": 6,
                "compression": "UltraFast"
            }
    }
}

valid_comment_json_system_tts = {
    "name": "Askreddit comments top all time",
    "description": "Makes a video from Reddit comments on a post",
    "settings": {
            "type": "comment",
            "subreddit": "askreddit",
            "sort": "top",
            "time": "all",
            "limit": 10,
            "max_length": 60,
            "min_length": 30,
            "background_footage": "E:/YT/bgfootage/satisfying mc prk.mp4",
            "tts": {
                "engine": "system",
                "kwargs": {
                    "voice": "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_DAVID_11.0",
                    "rate": 180,
                }
            },
        "export_settings": {
                "codec": "mpeg4",
                "bitrate": "16000k",
                "fps": 60,
                "threads": 6,
                "compression": "UltraFast"
            }
    }
}

valid_comment_json_coqui_tts = {
    "name": "Askreddit comments top all time",
    "description": "Makes a video from Reddit comments on a post",
    "settings": {
            "type": "comment",
            "subreddit": "askreddit",
            "sort": "top",
            "time": "all",
            "limit": 10,
            "max_length": 60,
            "min_length": 30,
            "background_footage": "E:/YT/bgfootage/satisfying mc prk.mp4",
            "tts": {
                "engine": "coqui",
                "kwargs": {
                    "model": "coqui-tts-models/en/ljspeech/taco_pretrained"
                }
            },
        "export_settings": {
                "codec": "mpeg4",
                "bitrate": "16000k",
                "fps": 60,
                "threads": 6,
                "compression": "UltraFast"
            }
    }
}

general_missing_keys = [
    "name",
    "description",
    "settings"
]

general_missing_settings_keys = [
    "type",
    "subreddit",
    "sort",
    "time",
    "limit",
    "max_length",
    "min_length",
    "export_settings"
]

general_missing_export_settings_keys = [
    "codec",
    "bitrate",
    "fps",
    "threads",
    "compression"
]

general_missing_target_resolution_keys = [
    "width",
    "height"
]

video_missing_keys = [
    "max_video_length"
]

comment_missing_keys = [
    "background_footage",
    "tts"
]

tts_missing_keys = [
    "engine",
    "kwargs"
]

google_tts_missing_keys = [
    "accent"
]

system_tts_missing_keys = [
    "voice",
    "rate"
]

coqui_tts_missing_keys = [
    "model"
]


@pytest.mark.parametrize("key", general_missing_keys)
def test_general_missing_key(key):
    json = deepcopy(valid_video_json)
    del json[key]
    with pytest.raises(ConfigKeyError):
        VideoConfig(json)


@pytest.mark.parametrize("key", general_missing_settings_keys)
def test_general_missing_settings_key(key):
    json = deepcopy(valid_video_json)
    del json["settings"][key]
    with pytest.raises(ConfigKeyError):
        VideoConfig(json)


@pytest.mark.parametrize("key", general_missing_export_settings_keys)
def test_general_missing_export_settings_key(key):
    json = deepcopy(valid_video_json)
    del json["settings"]["export_settings"][key]
    with pytest.raises(ConfigKeyError):
        VideoConfig(json)


@pytest.mark.parametrize("key", general_missing_target_resolution_keys)
def test_general_missing_target_resolution_key(key):
    json = deepcopy(valid_video_json)
    del json["settings"]["target_resolution"][key]
    with pytest.raises(ConfigKeyError):
        VideoConfig(json)


def test_incorrect_type():
    json = deepcopy(valid_video_json)
    json["settings"]["type"] = "deez nuts"
    with pytest.raises(ValueError):
        VideoConfig(json)


def test_incorrect_reddit_sort():
    json = deepcopy(valid_video_json)
    json["settings"]["sort"] = "lumfao"
    with pytest.raises(ValueError):
        VideoConfig(json)


def test_incorrect_reddit_time():
    json = deepcopy(valid_video_json)
    json["settings"]["time"] = "lumfao"
    with pytest.raises(ValueError):
        VideoConfig(json)


@pytest.mark.parametrize("key", video_missing_keys)
def test_video_missing_key(key):
    json = deepcopy(valid_video_json)
    del json["settings"][key]
    with pytest.raises(ConfigKeyError):
        VideoConfig(json)


@pytest.mark.parametrize("key", comment_missing_keys)
def test_comment_missing_key(key):
    json = deepcopy(valid_comment_json)
    del json["settings"][key]
    with pytest.raises(ConfigKeyError):
        VideoConfig(json)


@pytest.mark.parametrize("key", tts_missing_keys)
def test_tts_missing_key(key):
    json = deepcopy(valid_comment_json)
    del json["settings"]["tts"][key]
    with pytest.raises(ConfigKeyError):
        VideoConfig(json)


@pytest.mark.parametrize("key", google_tts_missing_keys)
def test_google_tts_missing_key(key):
    json = deepcopy(valid_comment_json)
    del json["settings"]["tts"]["kwargs"][key]
    with pytest.raises(ConfigKeyError):
        VideoConfig(json)


@pytest.mark.parametrize("key", system_tts_missing_keys)
def test_system_tts_missing_key(key):
    json = deepcopy(valid_comment_json_system_tts)
    json["settings"]["tts"]["engine"] = "system"
    del json["settings"]["tts"]["kwargs"][key]
    with pytest.raises(ConfigKeyError):
        VideoConfig(json)


@pytest.mark.parametrize("key", coqui_tts_missing_keys)
def test_coqui_tts_missing_key(key):
    json = deepcopy(valid_comment_json_coqui_tts)
    del json["settings"]["tts"]["kwargs"][key]
    with pytest.raises(ConfigKeyError):
        VideoConfig(json)


def test_incorrect_tts_engine():
    json = deepcopy(valid_comment_json)
    json["settings"]["tts"]["engine"] = "deez nuts"
    with pytest.raises(ValueError):
        VideoConfig(json)


def test_has_setting():
    json = valid_video_json
    config = VideoConfig(json)

    assert config.has_setting("type")


def test_load_configs_invalid_file():
    with pytest.raises(FileNotFoundError):
        VideoConfig.load_configs("deez_nuts.json")


def test_load_configs_valid_file(tmp_path):
    file_path = tmp_path / "test.json"

    configs_object = {
        "configs": [valid_video_json]
    }

    file_path.write_text(dumps_json(configs_object))

    configs = VideoConfig.load_configs(file_path)
    assert len(configs) == 1


def test_load_configs_valid_file_multiple(tmp_path):
    file_path = tmp_path / "test.json"

    configs_object = {
        "configs": [valid_video_json, valid_comment_json]
    }

    file_path.write_text(dumps_json(configs_object))

    configs = VideoConfig.load_configs(file_path)
    assert len(configs) == 2


def test_load_configs_valid_file_no_configs(tmp_path):
    file_path = tmp_path / "test.json"

    configs_object = {
        "configs": []
    }

    file_path.write_text(dumps_json(configs_object))

    configs = VideoConfig.load_configs(file_path)
    assert len(configs) == 0


def test_load_configs_valid_file_no_configs_object(tmp_path):
    file_path = tmp_path / "test.json"

    configs_object = {
        "deez": "nuts"
    }

    file_path.write_text(dumps_json(configs_object))

    with pytest.raises(ConfigKeyError):
        VideoConfig.load_configs(file_path)


def test_repr():
    config = VideoConfig(valid_comment_json)

    assert repr(config) == config.name
