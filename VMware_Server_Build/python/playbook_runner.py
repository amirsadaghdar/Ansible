# Import the module
# Define allowed values.
# fucntion to check user input.
# function to collect user input.
# function to ask for input confirmation.
# while loop until user input is confirmed.
# Create folder for thenew server.
# Copy the server build files.
# Replace the values in the variable files.
# Run the playbook.

# How to run the script:
# This script can be run fom anywhere on the Ansible Contrl node.
# sudo python3 playbook_runner<##>.py
# <##> is the last version of the script.

"""
Capture server build details and run the Ansible playbook.

Usage:
    sudo python3 playbok_runner<##>.py
    <##> is the latest version of the code.
"""

import subprocess
import os
import shutil
import shlex
import sys
from colorama import Fore, Style
from playbook_values import *


def input_validate(true_list, list_name):
    """
    Capture the user input and check it against a pre-defined list.
    Args:
        A list of pre-defined values for th vriables.

    Returns:
        A variable which is populated and checked for its correctness.
    """
    try:
        is_valid = False
        while not is_valid:
            input_name = list_name
            input_question = (f"\nPlease input the value for the {input_name} " + f"\nAvailable options {true_list}: ")
            user_input = input(input_question)
            if user_input in true_list:
                is_valid = True
                return user_input
            else:
                is_valid = False

    except TypeError:
        print(Fore.RED + "\nCouldn't find the correct list.")
        print(Style.RESET_ALL)


def get_server_details():
    """
    Capture the server name and create the Ansible inventory file path.
    Use input_validate function to capture all user input.
    Args:
        None

    Returens:
        All the variables which are required for the server build.
    """
    global SERVER_NAME, DIRECTORY_PATH2, FILE_PATH1, FILE_PATH2, IP_ADDRESS, DC_NAME, CLUSTER_NAME, RESOURCEPOOL_NAME, \
        TEMPLATES_NAME, DATASTORE_NAME, VCS_NAME, DNS_SERVER01, DNS_SERVER02, DVPG_NAME, SUBNET_MASK, \
            DEFAULT_GATEWAY, WEEK_NAME, WEEK01, WEEK02, WEEK03

    print(Fore.GREEN + "\n### Capture the server details ###")
    print(Style.RESET_ALL)

    SERVER_NAME_INPUT = input("\nPlease input in the server name: ")
    SERVER_NAME = SERVER_NAME_INPUT.upper()
    DIRECTORY_PATH1 = "/etc/ansible/prod/serverbuild/"
    DIRECTORY_PATH2 = f"{DIRECTORY_PATH1}{SERVER_NAME}"
    FILE_PATH1 = f"{DIRECTORY_PATH2}/host.yml"
    FILE_PATH2 = f"{DIRECTORY_PATH2}/hostvars.yml"

    IP_ADDRESS = input("\ntype in the server IP: ")

    DC_NAME = input_validate(DC_NAMES, "datacenter name")
    CLUSTER_NAME = input_validate(CLUSTER_NAMES, "cluster name")
    RESOURCEPOOL_NAME = input_validate(RESOURCEPOOL_NAMES, "resource pool name")
    TEMPLATES_NAME = input_validate(TEMPLATES_NAMES, "template name")

    if DC_NAME == "LD4_DC":
        DATASTORE_NAME = "UKLD4UNITY01_POOL1_CLUSTER_01"
        VCS_NAME = "lwpld4vcs03.corp.com"
        DNS_SERVER01 = "10.64.64.71"
        DNS_SERVER02 = "10.76.101.21"
    elif DC_NAME == "155_DC":
        DATASTORE_NAME = "UKINXUNITY01_POOL1_CLUSTER_01"
        VCS_NAME = "lwp155vcs03.corp.com"
        DNS_SERVER01 = "10.76.101.21"
        DNS_SERVER02 = "10.64.64.71"
    DVPG_NAME = input_validate(DVPG_NAMES, "vlan name")
    SUBNET_MASK = input("\ntype in the server subnet mask: ")
    DEFAULT_GATEWAY = input("\ntype in the server default gateway: ")

    WEEK_NAME = input_validate(WEEK_NAMES, "week name")
    if WEEK_NAME == "week1":
        WEEK01 = "true"
        WEEK02 = "false"
        WEEK03 = "false"
    elif WEEK_NAME == "week2":
        WEEK01 = "false"
        WEEK02 = "true"
        WEEK03 = "false"
    elif WEEK_NAME == "week3":
        WEEK01 = "false"
        WEEK02 = "false"
        WEEK03 = "true"


def confirm_input():
    """
    Prints the user input and asks for the confirmation.
    It uses a bool to check if the user is happy with the input.
    Args:
        None

    Returns:
        The confirmed list of variables.
    """
    global CONFIRM_INPUTS

    print(Fore.GREEN + "\n### Server Details ###")
    print(Style.RESET_ALL)

    MESSAGE_DICT = {
        '"Server Name"' : SERVER_NAME,
        '"Server IP Address"' : IP_ADDRESS,
        '"VMware Datacenter Name"' : DC_NAME,
        '"VMware Cluster Name"' : CLUSTER_NAME,
        '"VMware Resource Pool"' : RESOURCEPOOL_NAME,
        '"VMware Template"' : TEMPLATES_NAME,
        '"VMware Datastore"' : DATASTORE_NAME,
        '"VMware VLAN"' : DVPG_NAME,
        '"Server Subnetmask"' : SUBNET_MASK,
        '"Server Default Gateway"' : DEFAULT_GATEWAY,
        '"Server Patching Week"' : WEEK_NAME
        }

    for entry in MESSAGE_DICT:
        print(entry, MESSAGE_DICT[entry])
        print("")

    CONFIRM_CONFIG = input(Fore.GREEN + "\nAre you happy with the deails above - (Y)es / (N)o: ").lower()
    print(Style.RESET_ALL)
    CONFIRM_VALUE = ["yes", "y"]
    DENY_VALUE = ["no", "n"]

    if CONFIRM_CONFIG in CONFIRM_VALUE:
        CONFIRM_INPUTS = True
        print("true")
    elif CONFIRM_CONFIG in DENY_VALUE:
        CONFIRM_INPUTS = False
        print("false")
    else:
        print(Fore.RED + "Your answer were inccorect. Please run the program again to restart the process.")
        print(Style.RESET_ALL)
        sys.exit(42)


def create_dir(directory_path):
    """
    Create a new directory to hold server build variables and playbook.
    Args:
        Path to the new directory.

    Returns:
        A new direcotry under server build directory.
    """
    try:
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        else:
            print("The direcotry already exists.")
    except TypeError:
        print(Fore.RED + "Couldn't create the folder.")
        print(Style.RESET_ALL)


def copy_files(src_path, dst_path):
    """
    Copy the tmplate files for the server build to the new directory.
    Args:
        Source and destination folders.

    Returns:
        The confirmed list of variables.
    """
    try:
        src_files = os.listdir(src_path)
        for file_name in src_files:
            full_file_name = os.path.join(src_path, file_name)
            if os.path.isfile(full_file_name):
                shutil.copy(full_file_name, dst_path)
    except TypeError:
        print(Fore.RED + "Couldn't copy the file.")
        print(Style.RESET_ALL)


def replace_text(file_path, old_text, new_text):
    """
    Replace the variable files with the user input.
    Args:
        File pthe to target.
        Place holder values.
        User input.

    Returns:
        Updated variable file with user input.
    """
    try:
        fin = open(file_path, "rt")
        data = fin.read()
        data = data.replace(old_text, new_text)
        fin.close()
        fin = open(file_path, "wt")
        fin.write(data)
        fin.close()
    except TypeError:
        print(Fore.RED + "\nCouldn't replace the text.")
        print(Style.RESET_ALL)


def shlex_convert_str_2list(comm_str):
    """
    Convert a linux command into list format with shlex.
    Args:
        A command.

    Returns:
        A list made of command arguments.
    """

    split_comm = shlex.split(comm_str)

    # remove all instances of empty string
    split_comm_clean = list(filter(lambda a: a != "", split_comm))

    return split_comm_clean

def run_cmd_with_output(comm_str):
    """
    Run a subprocess command and print error message on failure.
    Args:
        A list

    Returns:
        Executes the subprcess.
    """

    split_comm_clean = shlex_convert_str_2list(comm_str=comm_str)

    try:
        sp_resp = subprocess.run(split_comm_clean, check=True)
        return sp_resp
    except Exception as err:
        print(Fore.RED + f"\n{err}")
        print(Style.RESET_ALL)
        return None

def main():
    """
    Run the main code.
    Args:
        None

    Returns:
        Run the playbook
    """
    global CONFIRM_INPUTS
    CONFIRM_INPUTS = False

    # Get the user input and check if the final input is correct.
    while CONFIRM_INPUTS == False:
        get_server_details()
        confirm_input()

    # Create the directory for the new server.
    create_dir(DIRECTORY_PATH2)

    # Copy template folder to the new folder.
    print(Fore.GREEN + "\n### Copy the files from the template folder ###")
    print(Style.RESET_ALL)

    # Set th source and destination folder paths.
    SRC_PATH1 = "/etc/ansible/prod/serverbuild/buildtemplate/"
    DST_PATH1 = f"/etc/ansible/prod/serverbuild/{SERVER_NAME}"

    # Copy the files to the new directry.
    copy_files(SRC_PATH1, DST_PATH1)

    # Replace the config files with the input variables.
    print(Fore.GREEN + "\n### Replace the config files with the correct values ###")
    print(Style.RESET_ALL)

    REPLACE_DICT1 = {
        'server_name' : SERVER_NAME,
        'week01' : WEEK01,
        'week02' : WEEK02,
        'week03' : WEEK03
        }

    REPLACE_DICT2 = {
        'vcs_name' : VCS_NAME,
        'ip_address' : IP_ADDRESS,
        'dc_name' : DC_NAME,
        'cluster_name' : CLUSTER_NAME,
        'resourcepool_name' : RESOURCEPOOL_NAME,
        'template_name' : TEMPLATES_NAME,
        'server_name' : SERVER_NAME,
        'datastore_name' : DATASTORE_NAME,
        'dvpg_name' : DVPG_NAME,
        'subnet_mask' : SUBNET_MASK,
        'default_gateway' : DEFAULT_GATEWAY,
        'dns_server01' : DNS_SERVER01,
        'dns_server02' : DNS_SERVER02
        }

    for rep1 in REPLACE_DICT1:
        replace_text(FILE_PATH1, rep1, REPLACE_DICT1[rep1])

    for rep2 in REPLACE_DICT2:
        replace_text(FILE_PATH2, rep2, REPLACE_DICT2[rep2])

    # Execute the Playbook
    print(Fore.GREEN + "\n### Running the Playbook... ###")
    print(Style.RESET_ALL)

    # Change the working directory to the new server directory.
    PATH = f"/etc/ansible/prod/serverbuild/{SERVER_NAME}"
    os.chdir(PATH)

    # Run the Playbook.
    COMMAND = "sudo ansible-playbook --vault-id server_build@vault_password_file -i host.yml playbook.yml -vvv"
    run_cmd_with_output(COMMAND)

if __name__ == "__main__":
    main()
