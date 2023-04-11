"""Post module used for opening a reddit post and screenshotting / downloading images

Classes:
    Post: Represents a reddit post

Functions:
    concat_comment_id: Concatenates a comment id with the prefix "t1_"

Example:
    >>> from reddit_to_video.post import Post
    >>> post = Post("https://www.reddit.com/r/...", 1)
    >>> post.has_image
    False
    >>> post.url
    'https://www.reddit.com/r/...'
    >>> post.download_image("output")
    'output/post - 1.png'
    >>> post.screenshot_comment("g4q7xu", "output")
    'output/comment - 1.png'

Todo:
    * Refactor this class to be more readable, detect images automatically
"""

from os.path import join as path_join

from selenium import webdriver
from selenium.webdriver.common.by import By

from reddit_to_video.utility import download_img
from reddit_to_video.exceptions import NoImageError, ScrapingError


def concat_comment_id(comment_id: str) -> str:
    """Concatenates a comment id with the prefix "t1_"""
    return f"t1_{comment_id}"

# TODO: Refactor this class to be more readable, detect images automatically


class Post:
    """Represents a reddit post and opens it in selenium"""

    def __init__(self, url: str, post_id: int, has_image: bool = False):
        self.post_id = post_id
        self._has_image = has_image
        self.driver = webdriver.Firefox()
        self.url = url

    @property
    def has_image(self) -> bool:
        """Returns True if the post has an image, False otherwise"""
        return self._has_image

    @property
    def url(self) -> str:
        """Returns the url of the post"""
        return self._url

    @url.setter
    def url(self, url: str):
        """Sets the url of the post and opens it in selenium"""
        self._url = url
        self.driver.get(url)

    def reload(self):
        """Reloads the post in selenium"""
        self.driver.get(self.url)

    def download_image(self, output_dir: str) -> str:
        """Downloads the image of the post to the output directory"""
        if not self.has_image:
            raise NoImageError("download_image() Post has no image")

        post_content = self.driver.find_element(By.XPATH,
                                                "//div[@data-test-id='post-content']")

        if post_content is None:
            raise ScrapingError(
                ("download_image() Post has no content"
                 " (div[@data-test-id='post-content']). Has reddit changed?")
            )

        images = post_content.find_elements(By.TAG_NAME, "img")

        # the post image is always second

        if len(images) < 2:
            raise ScrapingError(
                "download_image() Post has no image (img). Is it self post?")

        image = images[1]

        destination = path_join(
            output_dir, f"post - {self.post_id}.png")

        try:
            download_img(image.get_attribute("src"), destination)
        except Exception as exception:
            print(
                "download_image() Error downloading image, trying screenshot instead:" + exception)
            # try screenshot
            image.screenshot(destination)

        return destination

    def screenshot_comment(self, comment_id: str, output_dir: str) -> str:
        """Screenshots a comment to the output directory"""
        comment = self.driver.find_element(
            By.ID, concat_comment_id(comment_id))

        destination = path_join(
            output_dir, f"comment - {comment_id}.png")

        comment.screenshot(destination)

        return destination

    def screenshot_comments(self, comment_ids: list[str], output_dir: str) -> list:
        """Screenshots a list of comments to the output directory"""
        return [self.screenshot_comment(comment_id, path_join(
            output_dir, f"comment - {comment_id}.png")) for comment_id in comment_ids]

    def screenshot_title(self, output_path: str):
        """Screenshots the title of the post"""
        title = self.driver.find_element(
            By.XPATH, "//div[@data-testid='post-container']")

        title.screenshot(output_path)

    def close(self):
        """Closes the selenium driver"""
        self.driver.close()
