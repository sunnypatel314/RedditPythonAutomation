from selenium import webdriver
from selenium.webdriver.common.by import By

def getTitleScreenShots(browser, url, id, output_path):
    browser.get(url)
    try:    
        div_element_title = browser.find_element(By.ID, f"post-title-t3_{id}")
        div_element_title.screenshot(output_path)
    except Exception as e:
        print("ERROR --> ", e)

