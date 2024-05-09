from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

import time
import random

def init_driver():
    # Create Chromeoptions instance 
    options = webdriver.ChromeOptions() 
    
    # Adding argument to disable the AutomationControlled flag 
    options.add_argument("--disable-blink-features=AutomationControlled") 
    
    # Exclude the collection of enable-automation switches 
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    
    # Turn-off userAutomationExtension 
    options.add_experimental_option("useAutomationExtension", False) 
    
    # Setting the driver path and requesting a page 
    driver = webdriver.Chrome(options=options) 
    
    # Changing the property of the navigator value for webdriver to undefined 
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 
    
    driver.maximize_window()
    driver.get("https://www.booking.com/index.html")
    time.sleep(4)
    return driver


def scroll_to_bottom(times=1):
        for i in range(times):
            time.sleep(3)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

def close_popup():
    try:
        # Locate the element to hover over
        element_to_hover = driver.find_element_by_xpath('//div[@class="abcc616ec7 cc1b961f14 c180176d40 f11eccb5e8 ff74db973c"]')

        # Create ActionChains object
        actions = ActionChains(driver)

        # Move to element (hover)
        actions.move_to_element(element_to_hover).perform()
        # Click the element
        actions.click(element_to_hover).perform()

    except:
        pass


def click_on_show_more():
    global page 
    while True:
                try:
                    close_popup()
                    # wait = WebDriverWait(driver, 10)  # Adjust wait time as needed
                    element = driver.find_element_by_xpath('//button[@class="a83ed08757 c21c56c305 bf0537ecb5 f671049264 deab83296e af7297d90d"]')
                    # Now you can interact with the element (e.g., click)
                    element.click()
                    page += 1
                    print(f"Element found and clicked! Now in page {page}")
                except NoSuchElementException:
                    print("Element not found.")
                    break
                
                finally:
                     scroll_to_bottom()


def extract_hotel_info():
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    urls= soup.find_all("a" , attrs={"data-testid":"title-link"})
    with open("hotels.txt", "a") as file:
        for url in urls:
            file.write(f"{url.get('href')}\n")


def input_city_and_submit(city):
    input_city = driver.find_element_by_xpath('//input[@aria-label="Where are you going?"]')
    close_popup()
    for i in city:
        close_popup()
        input_city.send_keys(i)
        time.sleep(random.uniform(0.1, 0.3))
    else:
        time.sleep(2)
        
    driver.find_element_by_xpath('//button[@class="a83ed08757 c21c56c305 a4c1805887 f671049264 d2529514af c082d89982 cceeb8986b"]').click()




if __name__ == "__main__":
    page=0
    driver = init_driver()
    input_city_and_submit("tabuk")
    scroll_to_bottom(6)
    click_on_show_more()
    extract_hotel_info()
    time.sleep(30)
    driver.quit()