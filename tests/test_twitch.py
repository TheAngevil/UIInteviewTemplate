from pages.twitch import HomePage
import pytest


class TestTwitch:

    @pytest.mark.twitch
    def test_open_home_page(self, driver):
        twitch_home_page = HomePage(driver)
        twitch_home_page.open("https://twitch.tv/")
        pass
