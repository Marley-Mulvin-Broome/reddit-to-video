from selenium import webdriver
from selenium.webdriver.common.by import By
from os.path import join as path_join
from utility import download_img


def concat_comment_id(comment_id: str) -> str:
    return f"t1_{comment_id}"


class Post:
    def __init__(self, url: str, post_id: int, has_image: bool = False):
        self.url = url
        self.post_id = post_id
        self._has_image = has_image
        self.driver = webdriver.Firefox()
        self.driver.get(url)

    @property
    def has_image(self) -> bool:
        return self._has_image

    def download_image(self, output_dir: str) -> str:
        if not self.has_image:
            raise Exception("download_image() Post has no image")

        post_content = self.driver.find_element(By.XPATH,
                                                "//div[@data-test-id='post-content']")

        if post_content is None:
            raise Exception(
                "download_image() Post has no content (div[@data-test-id='post-content']). Has reddit changed?")

        images = post_content.find_elements(By.TAG_NAME, "img")

        # the post image is always second

        if len(images) < 2:
            raise Exception(
                "download_image() Post has no image (img). Is it self post?")

        image = images[1]

        destination = path_join(
            output_dir, f"post - {self.post_id}.png")

        try:
            download_img(image.get_attribute("src"), destination)
        except Exception as e:
            print(
                "download_image() Error downloading image, trying screenshot instead:", e)
            # try screenshot
            image.screenshot(destination)

        return destination

    def screenshot_comment(self, comment_id: str, output_dir: str) -> str:
        comment = self.driver.find_element(
            By.ID, concat_comment_id(comment_id))

        destination = path_join(
            output_dir, f"comment - {comment_id}.png")

        comment.screenshot(destination)

        return destination

    def screenshot_comments(self, comment_ids: list[str], output_dir: str) -> list:
        return [self.screenshot_comment(comment_id, path_join(
            output_dir, f"comment - {comment_id}.png")) for comment_id in comment_ids]

    def screenshot_title(self, output_dir: str) -> str:
        title = self.driver.find_element(
            By.XPATH, "//div[@data-testid='post-container']")

        destination = path_join(
            output_dir, f"post title - {self.post_id}.png")

        title.screenshot(destination)

        return destination

    def close(self):
        self.driver.close()
