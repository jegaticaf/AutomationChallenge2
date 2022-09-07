from libraries.common import log_message, capture_page_screenshot, browser
from config import OUTPUT_FOLDER, tabs_dict
from libraries.comercio.comercio import Comercio

class Process():
    
    def __init__(self, credentials: dict):
        log_message("Initialization")

        prefs = {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_setting_popups": 0,
            "directory_upgrade": True,
            "download.default_directory": OUTPUT_FOLDER,
            "plugins.always_open_pdf_externally": True,
            "download.prompt_for_download": False
        }

        browser.open_available_browser(preferences = prefs)
        browser.set_window_size(1920, 1080)
        browser.maximize_browser_window()

        comercio = Comercio(browser, {"url": "https://elcomercio.pe/"})
        comercio.access_comercio()
        self.comercio = comercio

    def start(self):
        """
        main
        """

        self.comercio.search_keyword()
        self.comercio.find_articles()
        self.comercio.create_excel()
        pass
    
    def finish(self):
        log_message("DW Process Finished")
        browser.close_browser()