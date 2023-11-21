from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service
import pyautogui
import time

"""
Acest script are urmatoarele functionalitati:
- Navigare catre website si maximizare fereastra
- Gasire elemente user si parola si completarea lor + logare
- Deschiderea cursului dorit in functie de ID
- Iterare prin DOM-ul paginii web pentru a descarca local si redenumi fiecare capitol si subcapitol al cursului
"""

webdriver_service = service.Service("operadriver.exe")
webdriver_service.start()
options = webdriver.ChromeOptions()
options.binary_location = "opera.exe"
options.add_experimental_option('w3c', True)
driver = webdriver.Remote(webdriver_service.service_url, options=options)

url = "https://www.example.com/portal/saml_login"
driver.get(url)
driver.maximize_window()
time.sleep(3)

user = driver.find_element(By.ID, "idp-discovery-username")
user.send_keys("example@gmail.com")

next = driver.find_element(By.ID, "idp-discovery-submit")
next.click()
time.sleep(3)

parola = driver.find_element(By.ID, "okta-signin-password")
parola.send_keys("example")

sign_in = driver.find_element(By.ID, "okta-signin-submit")
sign_in.click()
time.sleep(3)

launch_course = driver.find_element(By.XPATH, "//a[@href = 'https://example.com/course/view.php?id=242321']")
launch_course.click()
time.sleep(3)

# accept_cookies = driver.find_element(By.ID, "onetrust-accept-btn-handler")
# accept_cookies.click()
# time.sleep(3)

driver.execute_script("window.scrollBy(0,400)")

launch_content = driver.find_element(By.XPATH, "//a[@href = 'https://example.com/mod/lti/view.php?id=2345789']")
launch_content.click()
time.sleep(4)

driver.switch_to.window(driver.window_handles[3])

pyautogui.moveTo(250, 300)
pyautogui.click()
pyautogui.moveTo(250, 350)
pyautogui.click()

chapters = driver.find_elements(By.XPATH, "//ul[@class='main-sidebar__nav']/li")
for i in range(len(chapters)):
    chapter = chapters[i]
    chapter.click()
    time.sleep(1)
    subchapters = driver.find_elements(By.XPATH, f"//ul[@class='main-sidebar__nav']/li[{i+1}]/ul/li")
    for j in range(len(subchapters)):
        time.sleep(1)
        subchapter = subchapters[j]
        subchapter.click()
        section = driver.find_element(By.XPATH, f"//ul[@class='main-sidebar__nav']/li[{i+1}]/ul/li[{j+1}]/ul/li")
        section.click()
        time.sleep(1)
        pyautogui.moveTo(2150, 720)
        pyautogui.rightClick()
        pyautogui.moveTo(2250, 1040)
        pyautogui.click()
        time.sleep(1)
        pyautogui.press("left")
        pyautogui.press("delete", presses=24)
        pyautogui.write(f"{i+1}.{j} - ")
        pyautogui.press("enter")
        time.sleep(1)

driver.close()
