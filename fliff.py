from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# URL to navigate to
url = "https://sports.getfliff.com/shop"

# Set up Chrome options to enable mobile emulation
mobile_emulation = {
    "deviceName": "Pixel 2"
}

chrome_options = Options()
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

# Set up the Chrome driver with the specified options
driver = webdriver.Chrome(options=chrome_options)

try:
    # Launch the URL in Chrome with mobile emulation
    driver.get(url)

    # Wait for the "Sign In" button to be clickable and click it
    sign_in_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "sign-in-buttons-button-container"))
    )
    sign_in_button.click()

    # Wait for the "Sign In with Email" button to be clickable and click it
    email_sign_in_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Sign In with Email']]")
    ))
    email_sign_in_button.click()

    # Wait for the email input field, find it, and send the email address
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='email']"))
    )
    email_input.send_keys("TestMcTesterX@gmail.com")

    # Find the password input field and send the password
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
    )
    password_input.send_keys("pa$$w0rD123")

    # Find and click the "Sign In" button
    sign_in_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Sign In']]")
    ))
    sign_in_button.click()

    # Pause for a few seconds to observe the result
    time.sleep(5)

finally:
    # Close the browser
    driver.quit()