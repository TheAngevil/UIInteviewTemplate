import time
from PIL import Image
from pathlib import Path
from datetime import datetime

class Actions:

    def convert_png_to_jpg_and_delete(png_path: str):
        png_file = Path(png_path)

        if png_file.suffix.lower() != ".png":
            raise ValueError("The input file must be a .png image.")

        # Define the new jpg file path
        jpg_file = png_file.with_suffix(".jpg")

        # Open and convert the image
        with Image.open(png_file) as img:
            rgb_image = img.convert("RGB")  # JPEG doesn't support transparency
            rgb_image.save(jpg_file, format="JPEG")

    @staticmethod
    def scroll_down_by_view(driver, scroll_times:int=1, pixel_adjust:int=0) -> None:
        """
        Scroll down based on the height of scrollable element
        The scroll behaviour will be executed one times regardless scroll_times number.
        This won't scroll a "visable page" instead it will scroll the whole loaded bar
        :param driver:
        :param scroll_times:
        :return:
        """
        scroll_pause_time = 0.5
        inner_windows_height = driver.execute_script('return window.innerHeight;')
        # last_height = driver.execute_script("return document.body.scrollHeight")

        scroll_counter = 0

        while True:
            driver.execute_script(f"window.scrollTo(0, {inner_windows_height+pixel_adjust});")
            time.sleep(scroll_pause_time)
            scroll_counter +=1
            inner_windows_height *=2
            if scroll_counter == scroll_times:
                break

    @staticmethod
    def take_screen_shot(driver, request) -> None:
        """
        Use WebDriver to take a .jpg screenshot
        :param driver: The current instanced driver
        :param request: Passed from root confitest to construct screenshot name
        :return: None
        """
        project_path = Path.cwd()
        screenshot_dir = project_path / "screenshot"
        screenshot_dir.mkdir(exist_ok=True)

        now = datetime.now()
        timestamp = now.strftime("%H:%M:%S %m-%d")
        file_name = f"{request} {timestamp}"

        file_path = screenshot_dir / file_name

        png_file_name = f"{file_path}.png"
        jpg_file_name = f"{file_path}.jpg"

        driver.save_screenshot(png_file_name)

        with Image.open(png_file_name) as img:
            rgb_image = img.convert("RGB")  # JPEG doesn't support transparency
            rgb_image.save(jpg_file_name, format="JPEG")

        Path(png_file_name).unlink()