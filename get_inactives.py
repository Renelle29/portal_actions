import os
import json
from urllib.request import urlopen, HTTPError
from datetime import datetime, timezone, timedelta
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import getpass
from selenium.webdriver.firefox.options import Options
from tqdm import tqdm

import portal_actions.get_users as get_users

security_file = './group_members/security.txt'
output_file = './inactive_members/inactive.txt'

base_url = 'https://www.habbo.com/api/public/users?name='

def get_inactive(usernames):
    
    print("-------- Start get_inactive -----------")
    inactives = []
    n = len(usernames)

    # Get the current datestamp to compare with the last access time
    time1 = datetime.now(timezone.utc)

    # Main Loop on each username to find those who haven't come online for 15+ Days
    for username in tqdm(usernames):

        # Get the last access time from the server with the correct format
        url = base_url + username
        
        try:
            response = urlopen(url)
            datas = json.loads(response.read())
            if 'lastAccessTime' in datas:
                if datas['lastAccessTime'] != None:
                    time2 = datetime.strptime(datas['lastAccessTime'], "%Y-%m-%dT%H:%M:%S.%f%z")

                    # Main comparison
                    if (time1 - time2 > timedelta(days=15)):
                        inactives.append(username)
                
                else: # OT hidden
                    inactives.append(username)
                    print("OT hidden: ", username)

            else: # Profile closed
                inactives.append(username)
                print("Profile closed: ", username)
        
        except HTTPError as e:
            inactives.append(username)
            print("Error: ", e.code, " Username: ", username)
        
    print("-------- End get_inactive -----------")
    return inactives

def not_on_loa(usernames,username,password):

    print("-------- Start not_on_loa -----------")

    options = Options() 
    options.add_argument("-headless") 

    driver = webdriver.Firefox(options=options)
    url = "https://www.habbohia.net"
    driver.get(url)
    time.sleep(5)

    login_username = driver.find_element("id", "login-username")
    login_password = driver.find_element("id", "login-password")
    login_button = driver.find_element("id", "login-btn")

    login_username.send_keys(username)
    login_password.send_keys(password)
    login_button.send_keys(Keys.ENTER)
    time.sleep(7)

    xpath = "/html/body/div[1]/aside/section/nav/ul/li[24]"
    loa_hub = driver.find_element("xpath", xpath)
    loa_hub.click()
    time.sleep(5)

    css_selector = "#search_to"
    search_to = driver.find_element("css selector", css_selector)

    table_xpath = "/html/body/div[1]/div[1]/section[2]/div[2]/div/div/div[2]/div[2]/table/tbody/tr[1]"

    inactives = []

    # Main Loop on each username to find those that aren't on LOA
    for username in tqdm(usernames):
        search_to.send_keys(username)
        search_to.send_keys(Keys.ENTER)
        time.sleep(5)
        table = driver.find_elements("xpath", table_xpath)
        if len(table) > 0:
            text = table[0].text
            if ("Ending Soon" not in text) and ("In Progress" not in text) and (("LOA Expired" not in text)):
                inactives.append(username)
        else:
            inactives.append(username)
        search_to.clear()
    
    driver.quit()

    print("-------- End not_on_loa -----------")

    return inactives

def main():

    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    # Update the list of members within the Security group
    get_users.get_members()

    # Get it as a list within the script
    with open(security_file, 'r') as file:
        security_members = file.read().splitlines()

    # Get the list of inactive members
    inactive_members = get_inactive(security_members)

    # Remove those that are on LOA
    inactive_members = not_on_loa(inactive_members,username,password)

    # Delete the file that will contain the users to deactivate if it already exists
    if os.path.exists(output_file):
        os.remove(output_file)

    # Save the list of users to deactivate as a new file
    with open(output_file, 'w') as output_f:
        for inactive in inactive_members:
            output_f.write(inactive + "\n")
    print(output_file)

if __name__ == "__main__":
    main()
