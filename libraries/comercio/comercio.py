from libraries.common import log_message, capture_page_screenshot, act_on_element, files, file_system, check_file_download_complete, pdf
from config import OUTPUT_FOLDER
import random, os
from selenium.webdriver.common.keys import Keys

class Comercio():

    def __init__(self, rpa_selenium_instance, credentials:dict):
        self.browser = rpa_selenium_instance
        self.comercio_url = credentials["url"]
        self.results_data = []

    def access_comercio(self):
        """
        Access elcomercio.pe from the browser
        """
        log_message("Start - Access El Comercio")
        self.browser.go_to(self.comercio_url)
        log_message("End - Access El Comercio")

    def search_keyword(self):
        """
        Using the environmental variable as keyword, search that term
        """
        log_message("Start - Search Keyword Term")
        
        term = os.environ.get("Keyword", "tecnologia")

        act_on_element('//div[@class="nav-d__search-c"]', "click_element") 
        search_bar = act_on_element('//input[@class="nav-d__search-i active"]', "find_element")
        self.browser.input_text_when_element_is_visible('//input[@class="nav-d__search-i active"]', term)
        search_bar.send_keys(Keys.ENTER) 

        log_message("End - Search Keyword Term")

    def find_articles(self):
        """
        Saves the  elements from the search results
        """
        log_message("Start - Find Articles")
        page_number = 1
        articles = True
        while articles:
            date_elements = []
            hour_elements = []
            image_elements = []
            date_results = act_on_element('//span[@class="story-item__date-time"]', "find_elements")
            title_results = act_on_element('//a[@class="story-item__title block overflow-hidden primary-font line-h-xs mt-10"]', "find_elements")
            sinopsis_results = act_on_element('//p[@class="story-item__subtitle overflow-hidden hidden mt-10 mb-10 text-md text-gray-200 line-h-xs"]', "find_elements")
            image_results = act_on_element('//img[contains(@class,"lazy story-item__img object-cover object-center")]', "find_elements")
            for index, date_result in enumerate(date_results):
                if index%2 == 1:
                    hour_elements.append(date_result.text)
                    image_elements.append(image_results[index//2].get_attribute("data-src"))
                else:
                    date_elements.append(date_result.text)
  
            for date, hour, title, sinopsis, image in zip(date_elements, hour_elements,title_results, sinopsis_results, image_elements):
                self.results_data.append({"Date": date, "Hour": hour, "Title": title.text, "Sinopsis": sinopsis.text, "Image": image})
            page_number +=1
            if page_number <=3:
                try:
                    url =self.browser.get_location()
                    split_url= url[:-1].split('/')
                    new_url=""
                    for word in split_url[:-1]:
                        new_url = new_url+"{}/".format(word)
                    new_url = new_url+str(page_number)
                    self.browser.go_to(new_url)
                    act_on_element('//span[@class="story-item__date-time"]', "find_element")
                    
                except Exception as e:
                    articles = False
            else:
                articles = False

        log_message("End - Find Articles")

    def create_excel(self):
        """
        Create the Excel file with the information
        """
        log_message("Start - Create Excel")
        files.create_workbook(path = "{}/News.xlsx".format(OUTPUT_FOLDER))
        files.create_worksheet(name = "Results", content= None, exist_ok = True, header = False)
        files.append_rows_to_worksheet(self.results_data, name = "Results", header = True, start= None)
        files.remove_worksheet(name = "Sheet")
        files.save_workbook(path = None)
        files.close_workbook()
        log_message("End - Create Excel")

