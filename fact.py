from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options



def Fact():

    chrome_options = Options()
    chrome_options.add_argument("--headless")

    browser = webdriver.Chrome(executable_path='./chromedriver/chromedriver', options=chrome_options)
    wait = WebDriverWait(browser, 30)

    browser.get("https://www.mentalfloss.com/amazingfactgenerator")

    fact_container = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'af-details')))        
        
    browser.quit()

    return fact_container.get_attribute('data-description')
