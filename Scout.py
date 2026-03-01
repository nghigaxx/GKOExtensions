from turtle import position
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import re

class GoKickOffScanner:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.market_players = []
        self.top_players = {}  # {player_id: {'la': X, 'country': Y, 'name': Z}}
        
        # Country ID to name mapping
        self.country_names = {
            1: "Afghanistan", 2: "Albania", 3: "Algeria", 4: "American Samoa", 5: "Andorra",
            6: "Angola", 7: "Anguilla", 8: "Antigua and Barbuda", 9: "Argentina", 10: "Armenia",
            11: "Aruba", 12: "Australia", 13: "Austria", 14: "Azerbaijan", 15: "Bahamas",
            16: "Bahrain", 17: "Bangladesh", 18: "Barbados", 19: "Belarus", 20: "Belgium",
            21: "Belize", 22: "Benin", 23: "Bermuda", 24: "Bhutan", 25: "Bolivia",
            26: "Bosnia and Herzegovina", 27: "Botswana", 28: "Brazil", 29: "British Virgin Islands",
            30: "Brunei", 31: "Bulgaria", 32: "Burkina Faso", 33: "Burundi", 34: "Cambodia",
            35: "Cameroon", 36: "Canada", 37: "Cape Verde", 38: "Cayman Islands",
            39: "Central African Republic", 40: "Chad", 41: "Chile", 42: "China", 43: "Taipei",
            44: "Colombia", 45: "Comoros", 46: "Congo", 47: "Congo DR", 48: "Cook Islands",
            49: "Costa Rica", 50: "Ivory Coast", 51: "Croatia", 52: "Cuba", 53: "Cyprus",
            54: "Czech Republic", 55: "Denmark", 56: "Djibouti", 57: "Dominica",
            58: "Dominican Republic", 59: "Ecuador", 60: "Egypt", 61: "El Salvador",
            62: "England", 63: "Equatorial Guinea", 64: "Eritrea", 65: "Estonia", 66: "Ethiopia",
            67: "Faroe Islands", 68: "Fiji", 69: "Finland", 70: "France", 71: "Gabon",
            72: "Gambia", 73: "Georgia", 74: "Germany", 75: "Ghana", 76: "Greece", 77: "Grenada",
            78: "Guam", 79: "Guatemala", 80: "Guinea", 81: "Guinea-Bissau", 82: "Guyana",
            83: "Haiti", 84: "Honduras", 85: "Hong Kong", 86: "Hungary", 87: "Iceland",
            88: "India", 89: "Indonesia", 90: "Iran", 91: "Iraq", 92: "Israel", 93: "Italy",
            94: "Jamaica", 95: "Japan", 96: "Jordan", 97: "Kazakhstan", 98: "Kenya",
            99: "Korea DPR", 100: "Korea Republic", 101: "Kuwait", 102: "Kyrgyzstan", 103: "Laos",
            104: "Latvia", 105: "Lebanon", 106: "Lesotho", 107: "Liberia", 108: "Libya",
            109: "Liechtenstein", 110: "Lithuania", 111: "Luxembourg", 112: "Macau",
            113: "Macedonia", 114: "Madagascar", 115: "Malawi", 116: "Malaysia", 117: "Maldives",
            118: "Mali", 119: "Malta", 120: "Mauritania", 121: "Mauritius", 122: "Mexico",
            123: "Moldova", 124: "Mongolia", 125: "Montenegro", 126: "Montserrat", 127: "Morocco",
            128: "Mozambique", 129: "Myanmar", 130: "Namibia", 131: "Nepal", 132: "Netherlands",
            133: "Netherlands Antilles", 134: "New Caledonia", 135: "New Zealand", 136: "Nicaragua",
            137: "Niger", 138: "Nigeria", 139: "Northern Ireland", 140: "Norway", 141: "Oman",
            142: "Pakistan", 143: "Palestine", 144: "Panama", 145: "Papua New Guinea",
            146: "Paraguay", 147: "Peru", 148: "Philippines", 149: "Poland", 150: "Portugal",
            151: "Puerto Rico", 152: "Qatar", 153: "Republic of Ireland", 154: "Romania",
            155: "Russia", 156: "Rwanda", 157: "Saint Kitts and Nevis", 158: "Saint Lucia",
            159: "Saint Vincent and the Grenadines", 160: "Samoa", 161: "San Marino",
            162: "Sao Tome and Principe", 163: "Saudi Arabia", 164: "Scotland", 165: "Senegal",
            166: "Serbia", 167: "Seychelles", 168: "Sierra Leone", 169: "Singapore",
            170: "Slovakia", 171: "Slovenia", 172: "Solomon Islands", 173: "Somalia",
            174: "South Africa", 175: "Spain", 176: "Sri Lanka", 177: "Sudan", 178: "Suriname",
            179: "Swaziland", 180: "Sweden", 181: "Switzerland", 182: "Syria", 183: "Tahiti",
            184: "Tajikistan", 185: "Tanzania", 186: "Thailand", 187: "East Timor", 188: "Togo",
            189: "Tonga", 190: "Trinidad and Tobago", 191: "Tunisia", 192: "Turkey",
            193: "Turkmenistan", 194: "Turks and Caicos Islands", 195: "Uganda", 196: "Ukraine",
            197: "United Arab Emirates", 198: "United States", 199: "Uruguay",
            200: "U.S. Virgin Islands", 201: "Uzbekistan", 202: "Vanuatu", 203: "Venezuela",
            204: "Vietnam", 205: "Wales", 206: "Yemen", 207: "Zambia", 208: "Zimbabwe"
        }
        
    def login(self, target_url):
        """Log into GoKickOff account by navigating to target page first"""
        print("Navigating to target page...")
        self.driver.get(target_url)
        
        try:
            # Will be redirected to login page - wait for login form
            print("Waiting for login form...")
            self.wait.until(EC.presence_of_element_located((By.NAME, 'user_login'))).send_keys(self.username)
            self.wait.until(EC.presence_of_element_located((By.NAME, 'pwd_login'))).send_keys(self.password)
            self.wait.until(EC.element_to_be_clickable((By.NAME, 'Submit'))).click()
            
            # After login, should redirect back to the target page
            sleep(3)
            print("Login successful! Redirected to target page.")
        except Exception as e:
            print(f"Login failed: {e}")
            raise
    
    def scrape_all_market_pages(self):
        """Scrape ALL players from transfer market (age 13-21)"""
        print("\n" + "="*60)
        print("SCRAPING TRANSFER MARKET")
        print("="*60)
        
        # Base URL with all parameters - just change page number
        base_url = "https://gokickoff.com/transfer_market_search.php?page={page}&txt_position=0&txt_side=0&txt_st_age=13&txt_end_age=20&txt_st_sale_price=&txt_end_sale_price=&txt_nationality=0&txt_club_base=0&txt_injured=0&txt_st_crossing=0&txt_end_crossing=20&txt_st_dribbing=0&txt_end_dribbing=20&txt_st_finishing=0&txt_end_finishing=20&txt_st_longShots=0&txt_end_longShots=20&txt_st_marking=0&txt_end_marking=20&txt_st_tacking=0&txt_end_tacking=20&txt_st_heading=0&txt_end_heading=20&txt_st_technique=0&txt_end_technique=20&txt_st_handing=0&txt_end_handing=20&txt_st_reflexes=0&txt_end_reflexes=20&txt_st_setpiece=0&txt_end_setpiece=20&txt_st_aggression=0&txt_end_aggression=20&txt_st_creativity=0&txt_end_creativity=20&txt_st_decisions=0&txt_end_decisions=20&txt_st_determination=0&txt_end_determination=20&txt_st_influence=0&txt_end_influence=20&txt_st_positioning=0&txt_end_positioning=20&txt_st_offtheball=0&txt_end_offtheball=20&txt_st_teamwork=0&txt_end_teamwork=20&txt_st_acceleration=0&txt_end_acceleration=20&txt_st_aglilty=0&txt_end_aglilty=20&txt_st_balance=0&txt_end_balance=20&txt_st_jumping=0&txt_end_jumping=20&txt_st_pace=0&txt_end_pace=20&txt_st_stamina=0&txt_end_stamina=20&txt_st_strength=0&txt_end_strength=20&txt_st_passing=0&txt_end_passing=20&txt_st_kicking=0&txt_end_kicking=20&txt_st_oneonones=0&txt_end_oneonones=20&txt_st_rushingout=0&txt_end_rushingout=20&txt_st_aerial=0&txt_end_aerial=20&txt_st_estvalue=&txt_end_estvalue=&txt_exp=0&txt_limit=2&txt_transfer_type=1&txt_prone_inj=0&or_player=1"
        
        page = 1
        first_page = True
        
        while True:
            url = base_url.format(page=page)
            
            # For first page, we're already there after login
            if not first_page:
                print(f"Scraping market page {page}...")
                self.driver.get(url)
                sleep(2)
            else:
                print(f"Scraping market page {page} (already loaded after login)...")
                first_page = False
            
            try:
                # Find all player rows in the market table
                player_rows = self.driver.find_elements(By.CSS_SELECTOR, 'tr[id][role="row"]')
                
                if not player_rows:
                    print(f"No players found on page {page}. Market scraping complete.")
                    break
                
                for row in player_rows:
                    try:
                        # Extract player ID
                        player_id_cell = row.find_element(By.CSS_SELECTOR, 'td[aria-describedby="player-table_id"]')
                        player_id = player_id_cell.get_attribute('title') or player_id_cell.text.strip()
                        
                        # Extract player name
                        player_name_cell = row.find_element(By.CSS_SELECTOR, 'td[aria-describedby="player-table_name"]')
                        player_name = player_name_cell.text.strip()
                        
                        # Extract player level
                        try:
                            level_cell = row.find_element(By.CSS_SELECTOR, 'td[aria-describedby="player-table_bid_level"]')
                            level = level_cell.get_attribute('title') or level_cell.text.strip()
                        except:
                            level = "N/A"
                        
                        # Extract list price (minimum bid)
                        try:
                            list_price_cell = row.find_element(By.CSS_SELECTOR, 'td[aria-describedby="player-table_bid_min"]')
                            list_price = list_price_cell.get_attribute('title') or list_price_cell.text.strip()
                        except:
                            list_price = "N/A"
                        
                        self.market_players.append({
                            'id': player_id,
                            'name': player_name,
                            'level': level,
                            'list_price': list_price
                        })
                        
                    except Exception as e:
                        print(f"Error extracting player from row: {e}")
                        continue
                
                print(f"Page {page}: Found {len(player_rows)} players")
                page += 1
                sleep(2)  # Be respectful to the server
                
            except Exception as e:
                print(f"Error on page {page}: {e}")
                break
        
        print(f"\nTotal market players scraped: {len(self.market_players)}")
        return self.market_players
    
    def scrape_all_databases(self):
        """Scrape top 100 U21 players from ALL country databases (1-208), including GKs"""
        print("\n" + "="*60)
        print("SCRAPING ALL COUNTRY DATABASES")
        print("="*60)
    
        for nat_id in range(1, 209):
            print(f"Scraping database for country {nat_id}/208...")
        
            for pos_filter in ['', '2']:  # '' = outfield, '2' = GKs
                url = f"https://gokickoff.com/prem_game_stat.php?txt_nat={nat_id}&txt_type=2&txt_age=1&txt_pos={pos_filter}"
                self.driver.get(url)
                sleep(1.5)
            
                try:  # <-- this try must be INSIDE the for pos_filter loop
                    player_rows = self.driver.find_elements(By.CSS_SELECTOR, 'table tr')[1:]
                
                    for row in player_rows[:100]:
                        try:
                            tds = row.find_elements(By.TAG_NAME, 'td')
                        
                            if len(tds) < 8:
                                continue
                        
                            position = tds[1].text.strip()
                        
                            if not position:
                                continue
                        
                            links = tds[2].find_elements(By.TAG_NAME, 'a')
                            if not links:
                                continue
                            name_link = links[0]
                            href = name_link.get_attribute('href')
                            match = re.search(r'player_id=(\d+)', href)
                        
                            if not match:
                                continue
                        
                            player_id = match.group(1)
                            player_name = name_link.text.strip()
                            age = tds[3].text.strip()
                            la_value = tds[6].text.strip()
                            pr_value = tds[7].text.strip()

                            if not la_value.isdigit() or not pr_value.isdigit():
                                continue
                        
                            self.top_players[player_id] = {
                                'name': player_name,
                                'position': position,
                                'age': age,
                               'la': la_value,
                               'pr': pr_value,
                              'country': int(nat_id)
                            }
                        
                        except Exception as e:
                            print(f"Error processing player {player_id}: {e}")
                            continue
                        
                except Exception as e:
                    print(f"Error scraping country {nat_id} (pos={pos_filter or 'outfield'}): {e}")
                    continue
        
            if nat_id % 20 == 0:
                print(f"Progress: {nat_id}/208 countries completed...")
    
        print(f"\nTotal database players scraped: {len(self.top_players)}")
        return self.top_players
    
    def calculate_base_price(self, la, pr, position=None): #Base price depends on LA and PR
        """Calculate base price based on LA and PR"""
        la = int(la)
        pr = int(pr)
        is_gk = (position == 'GK')
    
        if la > 11:
            return 10000000 
        
        if la == 11:
            return 7000000
        
        if la == 10:
            if is_gk:
                return 4000000
            if pr >= 5:
                return 3700000
            elif pr == 4:
                return 3000000
            elif pr == 3:
                return 2500000
        
        if la == 9:
            if is_gk:
                if pr >= 5:
                    return round(1650000 * 1.6)   # 2,640,000
                elif pr == 4:
                    return round(1150000 * 1.6)   # 1,840,000
                elif pr == 3:
                    return round(750000 * 1.6)    # 1,200,000
                elif pr == 2:
                    return round(150000 * 1.6)    # 240,000
            else:
                if pr >= 5:
                    return 1650000
                elif pr == 4:
                    return 1150000
                elif pr == 3:
                    return 750000
                elif pr == 2:
                    return 150000
        
        if la == 8:
            if is_gk:
                if pr >= 5:
                    return 1000000
                elif pr == 4:
                    return 600000
                elif pr == 3:
                    return 400000
            else:
                if pr >= 5:
                    return 200000
                elif pr == 4:
                    return 120000
                elif pr == 3:
                    return 90000
            
        if la == 7:
            return 20000
        
        # Default for anything worse
        return None
    
    def compare_and_find_matches(self, min_la=8):
        """Compare market players against database"""
        print("\n" + "="*60)
        print(f"COMPARING MARKET TO DATABASE (Min LA: {min_la})")
        print("="*60)
        
        matches = []
        
        for market_player in self.market_players:
            player_id = market_player['id']
            
            if player_id in self.top_players:
                db_info = self.top_players[player_id]
                
                # Filter by LA value
                try:
                    la_value = int(db_info['la'])
                    if la_value < min_la:
                        continue  # Skip players with LA < min_la
                except ValueError:
                    # Skip if LA can't be converted to int
                    continue
                
                # Calculate base price and percentage
                base_price = self.calculate_base_price(db_info['la'], db_info['pr'], db_info.get('position'))
                
                # Parse list price (remove commas and 'G')
                try:
                    list_price_str = market_player['list_price'].replace(',', '').replace(' G', '').strip()
                    list_price_num = int(list_price_str)
                except:
                    list_price_num = 0
                
                # Calculate percentage of base price
                if base_price is None or base_price == 0:
                    price_percentage = 6000  #Too low PR to care
                else:
                    price_percentage = (list_price_num / base_price) * 100
                
                match = {
                        'id': player_id,
                        'name': market_player['name'],
                        'level': market_player['level'],
                        'position': db_info['position'],
                        'age': db_info['age'],
                        'list_price': market_player['list_price'],
                        'list_price_num': list_price_num,
                        'base_price': base_price if base_price else 0,
                        'price_percentage': price_percentage,
                        'la': db_info['la'],
                        'pr': db_info['pr'],
                        'country': self.country_names.get(db_info['country'], f"Unknown ({db_info['country']})")
                        }
                
                matches.append(match)
        
        # Sort by price percentage (lowest = best bargain)
        matches.sort(key=lambda x: x['price_percentage'])
        
        # Print sorted matches
        for match in matches:
            print(f"{match['name']} (Lvl {match['level']}, {match['position']}, {match['age']}y) | LA: {match['la']} | PR: {match['pr']} | Price: {match['list_price']} ({match['price_percentage']:.1f}% of base) | Country: {match['country']}")
        
        return matches
    
    def run_full_scan(self):
        """Execute complete scan: login -> market -> databases -> compare"""
        try:
            # Login by going directly to the transfer market page
            market_url = "https://gokickoff.com/transfer_market_search.php?page=1&txt_position=0&txt_side=0&txt_st_age=13&txt_end_age=20&txt_st_sale_price=&txt_end_sale_price=&txt_nationality=0&txt_club_base=0&txt_injured=0&txt_st_crossing=0&txt_end_crossing=20&txt_st_dribbing=0&txt_end_dribbing=20&txt_st_finishing=0&txt_end_finishing=20&txt_st_longShots=0&txt_end_longShots=20&txt_st_marking=0&txt_end_marking=20&txt_st_tacking=0&txt_end_tacking=20&txt_st_heading=0&txt_end_heading=20&txt_st_technique=0&txt_end_technique=20&txt_st_handing=0&txt_end_handing=20&txt_st_reflexes=0&txt_end_reflexes=20&txt_st_setpiece=0&txt_end_setpiece=20&txt_st_aggression=0&txt_end_aggression=20&txt_st_creativity=0&txt_end_creativity=20&txt_st_decisions=0&txt_end_decisions=20&txt_st_determination=0&txt_end_determination=20&txt_st_influence=0&txt_end_influence=20&txt_st_positioning=0&txt_end_positioning=20&txt_st_offtheball=0&txt_end_offtheball=20&txt_st_teamwork=0&txt_end_teamwork=20&txt_st_acceleration=0&txt_end_acceleration=20&txt_st_aglilty=0&txt_end_aglilty=20&txt_st_balance=0&txt_end_balance=20&txt_st_jumping=0&txt_end_jumping=20&txt_st_pace=0&txt_end_pace=20&txt_st_stamina=0&txt_end_stamina=20&txt_st_strength=0&txt_end_strength=20&txt_st_passing=0&txt_end_passing=20&txt_st_kicking=0&txt_end_kicking=20&txt_st_oneonones=0&txt_end_oneonones=20&txt_st_rushingout=0&txt_end_rushingout=20&txt_st_aerial=0&txt_end_aerial=20&txt_st_estvalue=&txt_end_estvalue=&txt_exp=0&txt_limit=2&txt_transfer_type=1&txt_prone_inj=0&or_player=1"
            self.login(market_url)
            
            self.scrape_all_market_pages()
            self.scrape_all_databases()
            matches = self.compare_and_find_matches()
            
            print("\n" + "="*60)
            print(f"SCAN COMPLETE - {len(matches)} MATCHES FOUND")
            print("="*60)
            
            return matches
            
        except Exception as e:
            print(f"Error during scan: {e}")
            raise
        finally:
            sleep(3)
            self.driver.quit()


# Example usage
if __name__ == "__main__":
    # Read credentials from file
    with open('credentials.txt', 'r') as f:
        user = f.readline().strip()
        password = f.readline().strip()
    
    # Initialize and run scanner
    scanner = GoKickOffScanner(user, password)
    matches = scanner.run_full_scan()
    
    # Optional: Save results to file
    if matches:
        with open('matches.txt', 'w', encoding='utf-8') as f:
            for match in matches:
                f.write(f"{match['name']} (Lvl {match['level']}, {match['position']}, {match['age']}y) | LA: {match['la']} | PR: {match['pr']} | "
                       f"Price: {match['list_price']} ({match['price_percentage']:.1f}% of base) | Country: {match['country']}\n")

        print("\nResults saved to matches.txt")
