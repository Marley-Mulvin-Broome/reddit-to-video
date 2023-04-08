from moviepy.video.io.VideoFileClip import VideoFileClip


def remove_links_from_text(text: str) -> str:
    import re

    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'www\S+', '', text)
    return text


def download_img(url, destination) -> None:
    from requests import get

    img_data = get(url).content

    with open(destination, 'wb') as handler:
        handler.write(img_data)


def get_audio_duration(audio_path: str) -> float:
    from mutagen.mp3 import MP3

    audio = MP3(audio_path)
    return audio.info.length


def get_video_duration(video_path: str) -> float:
    video = VideoFileClip(video_path)
    return video.duration
