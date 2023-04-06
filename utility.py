import re
from requests import get


def remove_links_from_text(text: str) -> str:
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'www\S+', '', text)
    return text


def download_img(url, destination) -> None:
    img_data = get(url).content

    with open(destination, 'wb') as handler:
        handler.write(img_data)
