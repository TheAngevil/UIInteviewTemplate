from pages.twitch import HomePage
import pytest


class TestTwitch:

    def test_open_home_page(self, driver):
        twitch_home_page = HomePage(driver)
        twitch_home_page.open("https://m.twitch.tv/")
        pass

    def test_open_home_page_2(self, driver):
        twitch_home_page = HomePage(driver)
        twitch_home_page.open("https://m.twitch.tv/")
        pass