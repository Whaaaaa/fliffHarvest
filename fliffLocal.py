import re
import sys  # Import sys to detect the platform
import getpass  # Import getpass to hide password input

import schedule
import time
import configparser
import subprocess

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


# Load the config file
config = configparser.ConfigParser()
config.read('config.ini')



# URL to navigate to
url = "https://sports.getfliff.com/shop"
def get_chrome_version():
    try:
        # Determine the platform and get the Chrome version accordingly
        command = ""
        if sys.platform == "win32":
            command = r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version'
        elif sys.platform == "darwin":
            command = r"/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version"
        else:
            command = r"google-chrome --version"

        version_output = subprocess.check_output(command, shell=True).decode('utf-8')
        version_number = re.search(r"(\d+)\.", version_output).group(1)
        return int(version_number)
    except Exception as e:
        print(f"Error while getting Chrome version: {e}")
        return 130  # Default to version 130 if unable to determine
def convert_time_to_minutes(cleaned_time_string):
    time_pattern = r"(\d{2}) : (\d{2}) : (\d{2})"
    match = re.match(time_pattern, cleaned_time_string)
    if match:
        hours = int(match.group(1))
        minutes = int(match.group(2))
        total_minutes = hours * 60 + minutes + 1  # Add an additional minute as requested
        return total_minutes
    return 1  # Default to 1 minute if the pattern doesn't match

def click_claim_buttons(driver):
    try:
        fliff_coin_icon = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//i[contains(@class, 'icon-fliff-coin tab-item__icon tab-item__icon--large')]"))
        )
        fliff_coin_icon.click()

        # Locate and click the first "Claim Now" span button
        claim_now_span = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[contains(@class, 'fliff-button__label') and contains(text(), 'Claim Now')]"))
        )
        claim_now_span.click()
        print("First 'Claim Now' span button clicked.")
        time.sleep(5)

        # Locate and click the "Claim Now" button inside the specific modal container
        claim_now_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "//div[contains(@class, 'bottom-modal__content free-coins-modal')]//button[contains(@class, 'fliff-button fliff-button-icon')]//span[contains(text(), 'Claim Now')]"))
        )
        claim_now_button.click()
        print("'Claim Now' button inside modal clicked.")
        driver.quit()
        schedule.clear()
        schedule.every(121).minutes.do(claim_coins)  # Update the schedule with new wait time
        return
    except Exception as e:
        try:
            # If the first "Claim Now" button is not found, locate the countdown element
            countdown_container = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'free-coins-countdown__container')]"))
            )
            countdown_time = countdown_container.text
            cleaned_time_string = ' '.join(countdown_time.split())

            print(f"Cash not available yet, try again in: {cleaned_time_string}")
            minutes_to_wait = convert_time_to_minutes(cleaned_time_string)
            schedule.clear()
            # Schedule the job to run after `minutes_to_wait` minutes
            schedule.every(minutes_to_wait).minutes.do(lambda: schedule_next_claim()).tag('next_claim')


        except Exception as countdown_exception:
            print(f"Error occurred while locating countdown element: {countdown_exception}")

        # Close the driver to end this attempt and continue with scheduling
        driver.quit()
        return  # End the function execution, but keep the schedule

def claim_coins():
    options = uc.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--user-agent=Mozilla/5.0 (Linux; Android 10; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36")

    version_main = get_chrome_version()

    driver = uc.Chrome(options=options, version_main=version_main)  # Specify the Chrome version dynamically
    #chrome_options = Options()
    #chrome_options.add_argument(f"user-data-dir={chrome_user_data_dir}")  # Correct profile path
    #chrome_options.add_argument("--profile-directory=Default")  # Specify the profile directory if needed
    #chrome_options.add_argument("--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1")

    # Set up the Chrome driver with the specified options
    #driver = webdriver.Chrome(options=chrome_options)

    # Launch the URL in Chrome with mobile emulation
    driver.get(url)

    try:
        # Try to locate and click the "Sign In" button
        try:
            sign_in_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'sign-in-buttons-button-container')]//span[contains(text(), 'Sign Up')]"))
            )
            sign_in_button.click()
        except Exception as e:
            # If the "Sign In" button is not found, click the icon instead
            print("Sign In button not found. Attempting to click the icon.")
            fliff_coin_icon = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//i[contains(@class, 'icon-fliff-coin tab-item__icon tab-item__icon--large')]"))
            )
            fliff_coin_icon.click()
            click_claim_buttons(driver)
            driver.quit()
            return  # End function if claim buttons are clicked successfully

        # Wait until the "Sign In with Google" button is clickable and click it
        google_sign_in_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'social-button-container')]//span[contains(text(), 'Sign In with Google')]"))
        )
        google_sign_in_button.click()

        # Switch to the Google login popup
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
        driver.switch_to.window(driver.window_handles[1])
        try:
            email_selection = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@data-identifier='benezra.noah@gmail.com']"))
            )
            email_selection.click()
            print('Email Account Selected')
            WebDriverWait(driver, 5000).until(EC.number_of_windows_to_be(1))
            driver.switch_to.window(driver.window_handles[0])
            WebDriverWait(driver, 500).until(EC.url_contains('https://sports.getfliff.com/channels?channelId=-333'))
            time.sleep(5)

            fliff_coin_icon = WebDriverWait(driver, 100).until(
                EC.element_to_be_clickable((By.XPATH, "//i[contains(@class, 'icon-fliff-coin tab-item__icon tab-item__icon--large')]"))
            )
            fliff_coin_icon.click()
            click_claim_buttons(driver)

        except Exception as noGoogleAccount:
            print(f"Error occurred while locating Google Account element: {noGoogleAccount}")
            # Wait for the email input field to be present and enter the email address
            email_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "identifierId"))
            )
            email_input.send_keys(email)
            email_input.send_keys(Keys.RETURN)

            # Wait for the password input field to be present and enter the password
            password_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "Passwd"))
            )
            password_input.send_keys(password)
            password_input.send_keys(Keys.RETURN)
            WebDriverWait(driver, 5000).until(EC.number_of_windows_to_be(1))
            driver.switch_to.window(driver.window_handles[0])
            WebDriverWait(driver, 500).until(EC.url_contains('https://sports.getfliff.com/channels?channelId=-333'))
            time.sleep(5)

            fliff_coin_icon = WebDriverWait(driver, 100).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//i[contains(@class, 'icon-fliff-coin tab-item__icon tab-item__icon--large')]"))
            )
            fliff_coin_icon.click()
            click_claim_buttons(driver)

    except Exception as e:
        print(f"Error occurred while processing claim: {e}")

    # Close the driver to end this attempt
    driver.quit()


def schedule_next_claim():
    # Run the claim_coins function
    claim_coins()
    # Clear all jobs and schedule the next recurring task every 121 minutes
    schedule.clear('next_claim')
    schedule.every(121).minutes.do(claim_coins).tag('recurring_claim')

def print_schedule():
    for job in schedule.get_jobs():
        print(job)


if __name__ == '__main__':
    # Load the config file
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Extract values from the config file
    email = config.get('Credentials', 'email')
    print(f"Email {email} loaded successfully.")

    if config.has_option('Credentials', 'password'):
        password = config.get('Credentials', 'password')
        print("Password loaded from config.")
    else:
        password = getpass.getpass(f'Please enter your password to {email}: ')

    # Schedule the task to run every 1 minute initially
    claim_coins()

    while True:
        schedule.run_pending()
        print_schedule()
        time.sleep(1)
