from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

if __name__ == '__main__':  # MAIN! PREPARAZIONE AL PRELIEVO DEI FILE PDF

    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option('prefs', {
        "download.default_directory": "C:\\Users\\Donat\\OneDrive\\Desktop\\PDF_File",
        # Change default directory for downloads
        "download.prompt_for_download": False,  # To auto download the file
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True  # It will not show PDF directly in chrome
    })
    # Optional argument, if not specified will search path.
    service = ChromeService(executable_path="C:\Program Files (x86)\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://scholar.google.com//")
    form_textfield = driver.find_element(By.NAME, 'q')
    form_textfield.send_keys("Massimiliano Di Penta" + Keys.ENTER)
    driver.find_element(By.PARTIAL_LINK_TEXT, "Massimiliano Di Penta").click()
    driver.find_element(By.PARTIAL_LINK_TEXT, "Massimiliano Di Penta").click()
    driver.find_element(By.PARTIAL_LINK_TEXT, "ANNO").click()