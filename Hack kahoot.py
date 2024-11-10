from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys
import time

# Path to your WebDriver executable
webdriver_path = 'path_to_your_webdriver'

# Initialize the WebDriver (using Chrome as an example)
driver = webdriver.Chrome()

# Open the Kahoot URL
url = "https://kahoot.it/?pin=464422&refer_method=link"
driver.get(url)

# Wait for the page to load
time.sleep(2)

# Find the 'nickname' input field by its ID and enter 'Not A Bot'
nickname_field = driver.find_element(By.ID, 'nickname')
nickname_field.send_keys('Not A Bot')

# Find the submit button by its class name and click it
submit_button = driver.find_element(By.CSS_SELECTOR, 'button.button__Button-sc-vzgdbz-0.fyUZin.nickname-form__SubmitButton-sc-1mjq176-1.dPDKgw')
submit_button.click()

# Wait until elements with the specified class are visible
wait = WebDriverWait(driver, 30)  # Wait up to 30 seconds
question_elements = wait.until(EC.visibility_of_all_elements_located(
    (By.CSS_SELECTOR, '.question-choice-content__QuestionChoiceText-sc-29yyv9-0.cpgwlw')
))

# Retrieve the inner text of each element and store it in a list
question_texts = [element.text for element in question_elements]

# Print the list of question texts
print(question_texts)

# Keep the browser open for a few seconds to observe the results
time.sleep(10)

# Close the browser
driver.quit()