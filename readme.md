
# Reddit To Video

![Ruff Linting](https://github.com/Marley-Mulvin-Broome/reddit-to-video/actions/workflows/ruff.yml/badge.svg)
![Pytest](https://github.com/Marley-Mulvin-Broome/reddit-to-video/actions/workflows/pytest.yml/badge.svg)
![Python Version](badges/python_version.svg)

Reddit to video is a tool that scrapes reddit for posts, comments, and other general media, compiling it into highly customisable videos.

## Table of Contents

1. [User Guide](#user-guide)
2. [Text To Speech](#text-to-speech)
    1. [TTS Settings](#tts-settings)
        1. [System Voices](#system-voices)
        2. [Google Translate TTS](#google-translate-tts)
        3. [Coqui TTS](#coqui-tts)
3. [FAQ](#faq)
    1. [Can I speed up the export?](#can-i-speed-up-the-export)
4. [Known Issues](#known-issues)

# User Guide

As the project is currently in its alpha version, there is no current user guide. However, running *main.py* and viewing the .json files in `user_configs/` should be able to give you an idea on how to use it.

# Text To Speech

The current options for text to speech at the moment are: your systems, google translates, and coqui tts apis. There may be more support addded, but this is not being focused at the current moment. If you are looking to create your own AI model to use, [Coqui TTS](https://tts.readthedocs.io/en/latest/tutorial_for_nervous_beginners.html) has a great guide on that.

## TTS Settings

---

### **System Voices**

Run `main.py -sv`  to see a list of your available system voices. To use one of these voices, you must set the `voice` key in your TTS settings.
For example:

    "tts": {
        "engine": "system",
        "kwargs": {
            "voice": "your voice here",
            "rate": 150
        }
    }

### **Google Translate TTS**

Google translate TTS supports both language and accents. To see a list of supported languages and accents check the [gtts docs](https://gtts.readthedocs.io/en/latest/index.html).

An example of implementing an English speaker with an australia accent would look like this:

    "tts": {
        "engine": "google",
        "kwargs": {
            "accent": "AUSTRALIA"
        }
    }

### **Coqui TTS**

Coqui TTS offers a [large variety of different models](https://tts.readthedocs.io/en/latest/#implemented-models). To view all the pre installed models on your machine type on the command line `tts --list-models`. Custom trained models are supported and are selected by setting the key `model_path` to the path of the model on your machine.

The `kwargs` tag in the configuration passed all of the kwargs to coqui itself directly, meaning you can put any argument you would as if you were directly calling the Coqui constructor. 

    "tts": {
        "engine": "coqui",
        "kwargs": {
            "model_name": "tts_models/multilingual/multi-dataset/your_tts",
            "speaker_wav": "E:\speaker.wav"
        }
    }

# FAQ

## Can I speed up the export?

There are a couple of things you can do to speed up exporting at the current moment:

- Decreasing the **bitrate** in export_settings
- Increasing the number of **threads** in export_settings
- Exporting shorter videos and combining them manually

Otherwise, it is simply an issue with the implementation and *[Moviepy](https://pypi.org/project/moviepy/)*.

# Known Issues

- Google Speech TTS sometimes has random long breaks while reading out long sentences
