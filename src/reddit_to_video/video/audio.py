import pyloudnorm as pyln
import soundfile as sf
from os.path import isfile as is_file



def normalise_audio_clip(audio_path: str, target_loudness: float):
    """Normalises an audio clip to a target loudness. The audio clip must be a .mp3 or .wav file"""
    if not is_file(audio_path):
        raise FileNotFoundError(
            f"normalise_audio_clip() Audio file {audio_path} does not exist")

    if not audio_path.endswith(".mp3") and not audio_path.endswith(".wav"):
        raise ValueError(
            f"normalise_audio_clip() Audio file {audio_path} is not a .mp3 or .wav file")

    data = normalise_audio_bytes(audio_path, target_loudness)

    sf.write(audio_path, data, 44100)


def normalise_audio_bytes(audio_bytes: bytes, target_loudness: float):
    """Normalises an audio clip to a target loudness. The audio bytes must be in a readable format"""
    data, rate = sf.read(audio_bytes)

    loudness = pyln.Meter(rate).integrated_loudness(data)

    data = pyln.normalize.loudness(data, loudness, target_loudness)

    return data
