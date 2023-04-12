import pytest
from reddit_to_video.scraping.validator import get_clip_service_from_url, is_valid_url, ClipService


clip_urls = {
    "https://clips.twitch.tv/AbstemiousSincereSalamanderPeteZaroll": ClipService.TWITCH,
    "https://clips.twitch.tv/AbstemiousSincereSalamanderPeteZaroll?t=00h00m00s": ClipService.TWITCH,
    "https://youtube.com/watch?v=1234567890": ClipService.YOUTUBE,
    "https://youtu.be/1234567890": ClipService.YOUTUBE,
    "https://streamable.com/1234567890": ClipService.STREAMABLE,
    "https://kick.com/1234567890?clip=1234567890": ClipService.KICK,
    "https://twitch.tv/1234567890/clip/1234567890": ClipService.TWITCH,
    "https://www.twitch.tv/plumy_/clip/MoldyTamePandaBCWarrior-DIsGTx_CrhxaC437": ClipService.TWITCH,
    "https://www.reddit.com/r/fightporn/comments/ei6pek/ochappy_new_year_rfightporn/": ClipService.REDDIT,
    "https://github.com/Marley-Mulvin-Broome/reddit-to-video": ClipService.NONE,
    "https://blog.twitch.tv/en/2021/05/21/lets-talk-about-hot-tub-streams/?utm_referrer=https://help.twitch.tv/": ClipService.NONE,
    "https://v.redd.it/yw6nan929np31": ClipService.REDDIT
}

valid_urls = [
    "https://clips.twitch.tv/AbstemiousSincereSalamanderPeteZaroll",
    "https://clips.twitch.tv/AbstemiousSincereSalamanderPeteZaroll?t=00h00m00s",
    "www.youtube.com"
]

urls_from_text = [
    ("This is a test https://clips.twitch.tv/AbstemiousSincereSalamanderPeteZaroll",
     "https://clips.twitch.tv/AbstemiousSincereSalamanderPeteZaroll"),
    ("This is a test https://clips.twitch.tv/AbstemiousSincereSalamanderPeteZaroll?t=00h00m00s",
     "https://clips.twitch.tv/AbstemiousSincereSalamanderPeteZaroll?t=00h00m00s"),
    ("Lets add brackets (https://clips.twitch.tv/AbstemiousSincereSalamanderPeteZaroll)",
     "https://clips.twitch.tv/AbstemiousSincereSalamanderPeteZaroll"),
    ("without https www.youtube.com", "www.youtube.com"),
    ("www.youtube.com", "www.youtube.com"),
]


@pytest.mark.filterwarnings("ignore:.*is deprecated.*")
@pytest.mark.parametrize("url, service", list(clip_urls.items()))
def test_get_clip_service_from_url(url, service):
    assert get_clip_service_from_url(url).value == service.value


@pytest.mark.filterwarnings("ignore:.*is deprecated.*")
@pytest.mark.parametrize("url", valid_urls)
def test_is_valid_url(url):
    assert is_valid_url(url) is True
