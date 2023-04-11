import pytest

from reddit_to_video.post import Post


class TestPost:

    def test_has_image(self):
        post = Post(
            "https://www.reddit.com/r/meirl/comments/vqghhh/me_irl/?utm_source=share&utm_medium=web2x&context=3", 1)
        assert post.has_image == True

    def test_doesnt_have_image(self):
        post = Post(
            "https://www.reddit.com/r/AskReddit/comments/12gzsyz/what_are_dealbreaker_fetishes_and_why/")
        assert post.has_image == False


# TODO: Add tests for the following:
# screenshot_title
# screenshot_comment
# screenshot_comments
# init to incorrect url
