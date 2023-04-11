
# Reddit To Video

[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)

Reddit to video is a script that scrapes reddit for posts and / or comments, compiling them into those horrible videos you see on YouTube and TikTok!

## Why?

I thought it would be interesting...

## How to use

Stay tuned!

## Can I speed up the export?

At the moment, besides increasing the threads or lowering the bitrate / fps in the config, not really.

# Text To Speech

The current options for text to speech at the moment are: your systems, google translates, and coqui tts apis. These may be expanded upon in the future, however and the current moment, these will be primarily focused going forward.

## How do I change my system voice?

Run main.py with the flag -sv to see a list of your available system voices. From there, copy the ID and set it to the voice value in the TTS json key

## AI generated text

Currently, coqui is the only real AI based speech synthesis api supported.
