# Example config file
# {
#     "configs": [{
#         "name": "Askreddit comments top all time",
#         "description": "Makes a video from Reddit comments on a post",
#         "settings": {
#             "type": "comment",
#             "subreddit": "askreddit",
#             "sort": "top",
#             "time": "all",
#             "limit": 100,
#             "max_length": 200,
#             "min_length": 30,
#             "background_footage": "backgrounds/footage.mp4",
#             "tts": {
#                 "engine": "google",
#                 "accent": "Australia"
#             },
#             "export_settings": {
#                 "codec": "libx264",
#                 "bitrate": "5000k",
#                 "fps": 30,
#                 "threads": 4,
#                 "compression": "UltraFast"
#             }
#         }
#     }]
# }

from os.path import isfile as is_file
from os.path import isdir as is_dir
from json import load as json_load
from tts import TTSAccents, all_tts_names, google_names, system_names, coqui_names
from .exportSettings import ExportSettings

reddit_sorts = ["relevance", "hot", "top", "new", "comments"]
reddit_time_filters = ["all", "year", "month", "week", "day", "hour"]

# from https://stackoverflow.com/questions/2352181/how-to-use-a-dot-to-access-members-of-dictionary


class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def validate_json_val(json, key, val_type, in_list=None, check_file=False, check_dir=False):
    if check_file and check_dir:
        raise Exception(
            "Config: is_file and is_dir cannot both be True when validating json value (key: {key}))")

    if key not in json:
        raise Exception(f"Config: Missing key {key}")
    if not isinstance(json[key], val_type):
        raise Exception(f"Config: Invalid type for {key}")

    if in_list is not None:
        if json[key] not in in_list:
            raise Exception(f"Config: Invalid value for {key} ({json[key]})")

    if check_file:
        if not is_file(json[key]):
            raise Exception(f"Config: File {json[key]} does not exist")

    elif check_dir:
        if not is_dir(json[key]):
            raise Exception(f"Config: Directory {json[key]} does not exist")


class VideoConfig:
    def __init__(self, json_object):
        self.json = json_object

        self.validate_config()

        self.export_settings = ExportSettings(
            **self._settings["export_settings"])

    def validate_config(self):
        validate_json_val(self.json, "name", str)
        self.name = self.json["name"]
        validate_json_val(self.json, "description", str)
        self.description = self.json["description"]
        validate_json_val(self.json, "settings", dict)
        self._settings = self.json["settings"]

        self.validate_settings()

    def validate_settings(self):
        self.settings = dotdict(self._settings)
        validate_json_val(self._settings, "type", str, ["comment", "post"])
        validate_json_val(self._settings, "subreddit", str)
        validate_json_val(self._settings, "sort", str, reddit_sorts)
        validate_json_val(self._settings, "time", str, reddit_time_filters)
        validate_json_val(self._settings, "limit", int)
        validate_json_val(self._settings, "max_length", int)
        validate_json_val(self._settings, "min_length", int)
        validate_json_val(self._settings, "background_footage",
                          str, check_file=True)

        self.validate_tts()
        self.tts = dotdict(self._settings["tts"])
        self.validate_export_settings()

    def validate_tts(self):
        tts = self._settings["tts"]
        validate_json_val(tts, "engine", str, all_tts_names)
        validate_json_val(tts, "kwargs", dict)

        self.tts_kwargs = tts["kwargs"]

        if tts["engine"] in google_names:
            validate_json_val(self.tts_kwargs, "accent", str,
                              in_list=TTSAccents.get_keys())
            self.tts_kwargs["accent"] = TTSAccents[self.tts_kwargs["accent"]].value

        elif tts["engine"] in system_names:
            validate_json_val(self.tts_kwargs, "rate", int)
            validate_json_val(self.tts_kwargs, "voice", str)

        elif tts["engine"] in coqui_names:
            validate_json_val(self.tts_kwargs, "model", str)

        else:
            raise Exception(f"Config: Invalid TTS engine {tts['engine']}")

    def validate_export_settings(self):
        export_settings = self._settings["export_settings"]

        validate_json_val(export_settings, "codec", str)
        validate_json_val(export_settings, "bitrate", str)
        validate_json_val(export_settings, "fps", int)
        validate_json_val(export_settings, "threads", int)
        validate_json_val(export_settings, "compression", str)

        self.export_settings = ExportSettings(**export_settings)

        self.export_settings.compression = self.export_settings.compression.lower()

    @staticmethod
    def load_configs(file_path) -> list:
        if not is_file(file_path):
            raise Exception(f"Config: File {file_path} does not exist")

        with open(file_path, "r") as f:
            json = json_load(f)

        return [VideoConfig(config) for config in json["configs"]]

    def __repr__(self) -> str:
        return self.name
