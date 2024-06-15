from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import os
import time
import getpass
from tqdm import tqdm

output_file = './portal_members/active_members.txt'

def get_active_depr(username, password):

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

    admin_tools_xpath = "/html/body/div[1]/aside/section/nav/ul/li[4]"
    admin_tools = driver.find_element("xpath", admin_tools_xpath)
    admin_tools.click()
    time.sleep(3)

    manage_users_xpath = "/html/body/div[1]/aside/section/nav/ul/li[4]/ul/li"
    manage_users = driver.find_element("xpath", manage_users_xpath)
    manage_users.click()
    time.sleep(5)

    active_users = []

    while True:
        table_xpath = "/html/body/div[1]/div[1]/section[2]/div[2]/div/div/div[2]/div[2]/table"
        table = driver.find_element("xpath", table_xpath)

        usernames_column = table.find_elements("xpath", './/tbody/tr/td[1]')
        activity_column = colonne2 = table.find_elements("xpath", './/tbody/tr/td[2]')

        usernames = [usernames_column[i].text for i in range(len(usernames_column)) if '<i class="fas fa-times" style="color:red;"></i>' not in activity_column[i].get_attribute("innerHTML")]
        active_users = active_users + usernames

        if ("SirCaptain-t" in active_users):
            break

        pagination_button = driver.find_element("css selector", 'a.page-link[aria-label="Next"]')
        pagination_button.click()
        time.sleep(1)
    
    driver.quit()

    # Delete the file that will contain the active users if it already exists
    if os.path.exists(output_file):
        os.remove(output_file)

    # Save the list of active users as a new file
    with open(output_file, 'w') as output_f:
        for active in active_users:
            output_f.write(active + "\n")
    print(output_file)

def get_active(username, password):

    print("-------- Start get_active -----------")

    options = Options() 
    options.add_argument("-headless") 

    driver = webdriver.Firefox(options=options)

    url = "https://www.habbohia.net"
    driver.get(url)
    time.sleep(3)

    login_username = driver.find_element("id", "login-username")
    login_password = driver.find_element("id", "login-password")
    login_button = driver.find_element("id", "login-btn")

    login_username.send_keys(username)
    login_password.send_keys(password)
    login_button.send_keys(Keys.ENTER)
    time.sleep(5)

    division_tracker_xpath = '/html/body/div[1]/aside/section/nav/ul/li[13]'
    division_tracker = driver.find_element("xpath", division_tracker_xpath)
    division_tracker.click()
    time.sleep(3)

    division_xpath = '/html/body/div[1]/div[1]/section[2]/div[1]/div/div/div[2]/form/div/div[1]/select'
    division = driver.find_element("xpath", division_xpath)
    division = Select(division)

    search_xpath = '/html/body/div[1]/div[1]/section[2]/div[1]/div/div/div[2]/form/div/div[4]/button'
    search = driver.find_element("xpath", search_xpath)

    options = [str(i) for i in range(2,16)]
    actives = []

    for option in tqdm(options):

        time.sleep(1)
        division.select_by_value(option)
        search.click()
        time.sleep(1)

        table_xpath = '/html/body/div[1]/div[1]/section[2]/div[2]/div/div/div/div[2]/table'
        table = driver.find_element("xpath", table_xpath)

        lignes = table.text.splitlines()[1:]
        usernames = [ligne.split(' ')[0] for ligne in lignes]

        actives = actives + usernames
    
    tools_xpath = '/html/body/div[1]/aside/section/nav/ul/li[7]'
    tools = driver.find_element("xpath",tools_xpath)
    tools.click()
    time.sleep(3)

    division_lookup_xpath = '/html/body/div[1]/aside/section/nav/ul/li[7]/ul/li[4]'
    division_lookup = driver.find_element("xpath", division_lookup_xpath)
    division_lookup.click()
    time.sleep(3)

    division_xpath = "/html/body/div[1]/div[1]/section[2]/div[1]/div/div/div[2]/form/span/span[1]/span"
    division = driver.find_element("xpath", division_xpath)

    options = ["Assistant Leadership", "Leadership", "Founders Cabinet", "Executive Committee", "Ownership", "Chief of Staff", "Special Ranks", "Directorate", "Foundation"]

    for option in tqdm(options):

        time.sleep(1)
        division.click()
        time.sleep(1)
        field_xpath = '/html/body/span/span/span[1]/input'
        field = driver.find_element("xpath", field_xpath)
        field.send_keys(option)
        if option == "Leadership":
            field.send_keys(Keys.ARROW_DOWN)
        field.send_keys(Keys.ENTER)
        time.sleep(3)

        table_xpath = '/html/body/div[1]/div[1]/section[2]/div[2]/div/div/div/div[2]/table'
        table = driver.find_element("xpath", table_xpath)

        lignes = table.text.splitlines()[1:]
        usernames = [ligne.split(' ')[0] for ligne in lignes]

        actives = actives + usernames

    driver.quit()

    # Delete the file that will contain the active users if it already exists
    if os.path.exists(output_file):
        os.remove(output_file)

    # Save the list of active users as a new file
    with open(output_file, 'w') as output_f:
        for active in actives:
            output_f.write(active + "\n")
    print(output_file)

    print("-------- End get_active -----------")
