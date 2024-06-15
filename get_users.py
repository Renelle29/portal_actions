import pandas as pd
import numpy as np
import json
from urllib.request import urlopen
import os
from tqdm import tqdm

start_url = 'https://www.habbo.com/api/public/groups/'
end_url = '/members'

output_folder = './group_members/'
output_type = '.txt'

def get_members():
    print("-------- Start get_members -----------")

    # Get the IDs of all badges
    data = pd.read_csv("groups_id.csv")
    names = np.array(data["name"])
    ids = np.array(data["id"])

    for i in tqdm(range(len(names))): #Main loop (iterate on each badge)

        name = names[i]
        id = ids[i]
        
        # API URL
        url = start_url + id + end_url
        usernames = []

        # Get the data from the server
        response = urlopen(url)
        datas = json.loads(response.read())

        # Build the names list
        for dict in datas:
            usernames.append(dict['name'])

        # Output file name
        output_file = output_folder + name + output_type

        # Delete the file if it already exists
        if os.path.exists(output_file):
            os.remove(output_file)
        
        # Save the members of the badge in a new file
        with open(output_file, 'w') as output_f:
            for username in usernames:
                output_f.write(username + "\n")
        print(output_file)
    
    print("-------- End get_active -----------")


