import os

import get_users as get_users
import get_active_members as get_active_members
import getpass

trainer_file = './group_members/trainer.txt'
active_file = './portal_members/active_members.txt'
output_file = './portal_members/to_deactivate.txt'

def is_trainer(username, usernames):
    return username in usernames

def get_to_deactivate(active_members, trainer_members):
    to_deactivate = []
    for username in active_members:
        if not is_trainer(username, trainer_members):
            print(username)
            to_deactivate.append(username)
    
    return to_deactivate

def main():

    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    # Update the list of active members on the Portal
    get_active_members.get_active(username,password)

    # Update the list of members within the Trainer group
    get_users.get_members()

    # Get them as lists within the script
    with open(trainer_file, 'r') as file:
        trainer_members = file.read().splitlines()
    trainer_members = [member.lower() for member in trainer_members]

    with open(active_file, 'r') as file:
        active_members = file.read().splitlines()
    active_members = [member.lower() for member in active_members]

    # Get the list of all active members on Portal who aren't within the Trainer group
    to_deactivate = get_to_deactivate(active_members,trainer_members)

    # Delete the file that will contain the users to deactivate if it already exists
    if os.path.exists(output_file):
        os.remove(output_file)

    # Save the list of users to deactivate as a new file
    with open(output_file, 'w') as output_f:
        for deac in to_deactivate:
            output_f.write(deac + "\n")
    print(output_file)

if __name__ == "__main__":
    main()


