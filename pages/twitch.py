from huskium.selenium import Page, Element, By
from huskium import dynamic

class ShareElements(Page):
    main_content_view = Element(By.XPATH, "//main[@id='page-main-content-wrapper']/div", remark="main_content_view")


class HomePage(Page):

    search_button = Element(By.XPATH, "//*[text()='Browse']", remark='search_button')

class BrowsePage(Page):

    search_text_input = Element(By.XPATH, value="//input[@type='search']", remark='search_text_input')

    @dynamic
    def search_result_select(self, keyword: str|None="") -> Element:
        """
        To select the desired search result if the keyword is given, select the first one if not given.
        :param keyword: Desire keyword
        :return: Element
        """
        return Element(By.XPATH, f"//a[contains(@href, 'direct')]//p[@title = '{keyword}']", remark=f'search_result_select')

    @dynamic
    def streamer_home_page(self, keyword:str|None="") -> Element:
        """
        Based on the streamer's name to return the clickable element to enter streamer's page,
        If not specified, will find the first playing palying channel

        :param keyword: default None. The name of the streamer or streamer's channel
        :return: Element that could be clicked to enter streamer's page
        """
        keyword = (keyword+"/").lower()
        return Element(By.XPATH, value=f'//div[@role="list"]//*[contains(@href, "{keyword}home")]', remark='streamer_home_page')

    search_streamer_page_load_indicator = Element(By.XPATH, value='//button[@role="link"]//img', remark="search_streamer_page_load_indicator")