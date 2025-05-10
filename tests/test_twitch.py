import time

from pages.twitch import HomePage, BrowsePage, ShareElements
from utils.actions import Actions
import pytest


class TestTwitch:

    @pytest.mark.twitch
    def test_open_home_page(self, driver, case_name):
        """
        1 go to Twitch
        2 click in the search icon
        3 input StarCraft II
        4* Select StartCraft as search result
        4 scroll down 2 times (a Whole page as once? now applied roughly a whole content view height as once)
        5* There is no streamer after scroll twice, back to top
        5 Select one streamer
        6 on the streamer page wait until all is load and take a screenshot
        """

        twitch_home_page = HomePage(driver)
        twitch_browse_page = BrowsePage(driver)
        action = Actions()

        # 1 go to Twitch
        twitch_home_page.get("https://twitch.tv/")

        # 2 click in the search icon
        twitch_home_page.search_button.wait_clickable(timeout=5)
        twitch_home_page.search_button.click()

        # 3 input StarCraft II
        twitch_browse_page.search_text_input.send_keys("StarCraft II")

        #4* Select StartCraft as search result
        twitch_browse_page.search_result_select(keyword="StarCraft II").wait_clickable(timeout=5).click()

        # scroll down 2 times
        action.scroll_down_by_view(driver, 2, pixel_adjust=-106)

        # 5* There is no streamer after scroll twice, back to top
        driver.execute_script(f"window.scrollTo(0, 0);")

        # 5 Select one streamer
        # Select the first
        twitch_browse_page.streamer_home_page().wait_clickable(timeout=5).click()


        while driver.execute_script("return document.readyState") != "complete":
            print("It is not done")
            time.sleep(0.2)

        twitch_browse_page.search_streamer_page_load_indicator.wait_visible(timeout=10)

        action.take_screen_shot(driver, case_name)

        """
        4 scroll down 2 times
        5 Select one streamer
        6 on the streamer page wait until all is load and take a screenshot
        """
        pass
