from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.webdriver.chrome.options import Options 

# Read credentials from the file
with open('credentials.txt', 'r') as f:
    user = f.readline().strip()
    password = f.readline().strip()

chrome_options = Options()
chrome_options.add_argument('--headless=new')  # Run in background
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=800,600')

browser = webdriver.Chrome(options=chrome_options)
browser.set_window_position(700, 200)
browser.set_window_size(800, 600)
browser.get('https://www.gokickoff.com/team_tactics.php')

# Players to exclude from efficiency check (add player IDs here)
EXCLUDED_PLAYER_IDS = ['']  # Replace with actual player IDs

try:
    # Wait for the username field and enter the username
    userInput = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.NAME, 'user_login'))
    )
    userInput.send_keys(user)

    # Wait for the password field and enter the password
    passInput = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.NAME, 'pwd_login'))
    )
    passInput.send_keys(password)

    # Wait for the login button and click it
    buttonInput = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.NAME, 'Submit'))
    )
    buttonInput.click()

    # Wait for the player table to load
    sleep(5)
    rows = browser.find_elements(By.XPATH, '//table[@id="player-table"]/tbody/tr')

    min_efficiency = float('inf')
    min_efficiency_player = None

    # Loop through the player rows to get player data
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')
        player_id = cells[0].get_attribute('title')
        player_pos = cells[3].text
        player_name = cells[4].find_element(By.TAG_NAME, 'a').text
        player_efficiency = float(cells[5].get_attribute('title').replace('%', ''))
        player_rate = cells[6].get_attribute('title')

        # Skip excluded players
        if player_id in EXCLUDED_PLAYER_IDS:
            print(f"Skipping excluded player: {player_name} (ID: {player_id})")
            continue

        # Update the player with the lowest efficiency (excluding the excluded players)
        if player_efficiency < min_efficiency:
            min_efficiency = player_efficiency
            min_efficiency_player = {
                'id': player_id,
                'pos': player_pos,
                'name': player_name,
                'efficiency': player_efficiency,
                'rate': player_rate,
            }

    # If all non-excluded players have efficiency above 85%, proceed with merch
    if min_efficiency > 85:
        print("All non-excluded players have an efficiency above 85%. Proceeding with souvenir")
        sleep(5)
        browser.get('https://www.gokickoff.com/activity_souvenirs.php?type=1')
        print("Souvenirs successfully sold!")
        sleep(5)
    else:
        # Print the player with the lowest efficiency
        print("Player with the lowest efficiency:")
        print(min_efficiency_player)
        sleep(5)
        # Navigate to the player's fitness update page
        browser.get(f'https://www.gokickoff.com/activity_player_detail.php?type=4&option=2&player_id={min_efficiency_player["id"]}')
        print("Player's physical condition updated!")
        sleep(5)

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    browser.quit()
