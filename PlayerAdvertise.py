from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# Read credentials from the file
with open('credentials.txt', 'r') as f:
    user = f.readline().strip()
    password = f.readline().strip()

# Start browser
browser = webdriver.Chrome()
browser.maximize_window()
browser.get('https://www.gokickoff.com/main.php')

try:
    # Login
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, 'user_login'))).send_keys(user)
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, 'pwd_login'))).send_keys(password)
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.NAME, 'Submit'))).click()

    # Wait for main page to load
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'country_id')))

    # Loop through country chat tabs
    for country_id in range(0, 209):  # 0 to 208 inclusive
        # Select country
        sleep(3)
        select_element = Select(browser.find_element(By.ID, 'country_id'))
        select_element.select_by_value(str(country_id))

        sleep(11)  # Let the chatbox reload for that country

        # Find chat input box and send message
        try:
            chat_input = WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((By.ID, 'news_input'))
            )
            chat_input.clear()
            chat_input.send_keys(f" MSG ") #Msg here

            # Click the "Share" button
            share_button = browser.find_element(By.XPATH, '//input[@value="Share"]')
            share_button.click()
            print(f"Sent message in country {country_id}")
        except:
            print(f"Skipped country {country_id}: Chatbox not found")

        sleep(2)  # Wait between messages to be safe

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    sleep(5)
    browser.quit()
