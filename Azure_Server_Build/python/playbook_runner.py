#0. take the host name as an inpurt.
#1. create a folder for the server name.
#2. copy the files from the template folder to the new server folder.
#3. gther all the inputs in differnet variables.
#4. replace the variables files.
#5. run the playbook.

import subprocess
import os
import shutil
import shlex
import sys
import time
import pprint as pp
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
            input_question = (f"\nPlease input the value for the {input_name} " + f"\nAvailable options {pp.pformat(true_list)}: ")
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
    global DIRECTORY_PATH2, FILE_PATH1, FILE_PATH2, SERVER_NAME, NIC, RESOURCE_GROUP, SUBNET, VM_SIZE, \
        LOCATION, SKU, VIRTUAL_NETWORK, VIRTUAL_NETWORK_RESOURCE_GROUP, SECURITY_GROUP, \
            BOOT_DIAGNOSTICS_RESOURCE_GROUP, BOOT_DIAGNOSTICS_STORAGE_ACCOUNT, TAG_NAME, \
                TAG_APPLICATION, TAG_OWNER, TAG_COSTCENTER, WEEK_NAME, WEEK01, WEEK02, WEEK03

    print(Fore.GREEN + "\n### Capture the server details ###")
    print(Style.RESET_ALL)

    SERVER_NAME = input("\ntype in the server name: ")
    DIRECTORY_PATH1 = "/etc/ansible/prod/serverbuild/"
    DIRECTORY_PATH2 = f"{DIRECTORY_PATH1}{SERVER_NAME}"
    FILE_PATH1 = f"{DIRECTORY_PATH2}/host.yml"
    FILE_PATH2 = f"{DIRECTORY_PATH2}/hostvars.yml"

    NIC = SERVER_NAME + "_nic01"
    RESOURCE_GROUP = input_validate(RESOURCE_GROUPS, "resource group")
    SUBNET = input_validate(SUBNETS, "subnet")
    VM_SIZE = input_validate(VM_SIZES, "vm_size_name")
    LOCATION = input_validate(LOCATIONS, "location_name")
    SKU = input_validate(SKUS, "sku_name")

    if SUBNET == "asaze-sn-p-01":
        VIRTUAL_NETWORK = "asaze-vn-p-01"
        VIRTUAL_NETWORK_RESOURCE_GROUP = "asaze-rg-p-network-01"
        SECURITY_GROUP = "asaze-nsg-p-open-01"
        BOOT_DIAGNOSTICS_RESOURCE_GROUP = "asaze-rg-p-infra-01"
        BOOT_DIAGNOSTICS_STORAGE_ACCOUNT = "asazeposdiag01"

    elif SUBNET == "asazs-sn-p-01":
        VIRTUAL_NETWORK = "asazs-vn-p-01"
        VIRTUAL_NETWORK_RESOURCE_GROUP = "asazs-rg-p-network-01"
        SECURITY_GROUP = "asazs-nsg-p-open-01"
        BOOT_DIAGNOSTICS_RESOURCE_GROUP = "asazs-rg-p-infra-01"
        BOOT_DIAGNOSTICS_STORAGE_ACCOUNT = "asazsrgpinfra01diag"

    elif SUBNET == "uks-sn-p-01" or SUBNET == "uks-sn-p-02" or SUBNET == "uks-sn-p-database-01":
        VIRTUAL_NETWORK = "uks-vn-p-01"
        VIRTUAL_NETWORK_RESOURCE_GROUP = "uks-rg-p-network-01"
        SECURITY_GROUP = "uks-nsg-p-open-01"
        BOOT_DIAGNOSTICS_RESOURCE_GROUP = "uks-rg-p-infra-01"
        BOOT_DIAGNOSTICS_STORAGE_ACCOUNT = "uksposdiag01" 

    elif SUBNET == "ukw-sn-p-16" or SUBNET == "ukw-sn-p-database-01":
        VIRTUAL_NETWORK = "ukw-vn-p-01"
        VIRTUAL_NETWORK_RESOURCE_GROUP = "ukw-rg-p-network-01"
        SECURITY_GROUP = "ukw-nsg-p-open-01"
        BOOT_DIAGNOSTICS_RESOURCE_GROUP = "ukw-rg-p-infra-01"
        BOOT_DIAGNOSTICS_STORAGE_ACCOUNT = "ukwposdiag01"

    elif SUBNET == "usaze-sn-p-01":
        VIRTUAL_NETWORK = "usaze-vn-p-01"
        VIRTUAL_NETWORK_RESOURCE_GROUP = "usaze-rg-p-network-01"
        SECURITY_GROUP = "usaze-nsg-p-open-01"
        BOOT_DIAGNOSTICS_RESOURCE_GROUP = "usaze-rg-p-infra-01"
        BOOT_DIAGNOSTICS_STORAGE_ACCOUNT = "usazsrgpinfra01diag"

    elif SUBNET == "uks-sn-d-01" or SUBNET == "uks-sn-d-02" or SUBNET == "uks-sn-d-database-01":
        VIRTUAL_NETWORK = "uks-vn-d-01"
        VIRTUAL_NETWORK_RESOURCE_GROUP = "uks-rg-d-network-01"
        SECURITY_GROUP = "uks-nsg-d-02"
        BOOT_DIAGNOSTICS_RESOURCE_GROUP = "uks-rg-d-infra-01"
        BOOT_DIAGNOSTICS_STORAGE_ACCOUNT = "uksdosdiag01"

    TAG_NAME = input("\nPlease type in the tag name: ")
    TAG_APPLICATION = input("\nPlease type in the tag application: ")
    TAG_OWNER = input("\nPlease type in the tag owner: ")
    TAG_COSTCENTER = str(input("\nPlease type in the tag cost center: "))

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
        '"Server Name: "' : SERVER_NAME,
        '"Server Resource Group: "' : RESOURCE_GROUP,
        '"Server Subnet: "' : SUBNET,
        '"Server VM Size: "' : VM_SIZE,
        '"Server Location: "' : LOCATION,
        '"Server SKU: "' : SKU,
        '"Tag Name: "' : TAG_NAME,
        '"Tag Application: "' : TAG_APPLICATION,
        '"Tag Owner: "' : TAG_OWNER,
        '"Tag Cost Center: "' : TAG_COSTCENTER,
        '"Server Patching Week: "' : WEEK_NAME
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
    elif CONFIRM_CONFIG in DENY_VALUE:
        CONFIRM_INPUTS = False
    else:
        print(Fore.RED + "Your answer was inccorect. Please run the program again to restart the process.")
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
    """

    split_comm = shlex.split(comm_str)

    # remove all instances of empty string
    split_comm_clean = list(filter(lambda a: a != "", split_comm))

    return split_comm_clean

def run_cmd_with_output(comm_str):
    """
    Run a subprocess command and print error message on failure.
    Also returns output on success and
    False on failure so that it can be handled downstream.
    """

    split_comm_clean = shlex_convert_str_2list(comm_str=comm_str)

    try:
        sp_resp = subprocess.run(split_comm_clean, check=True)
        return sp_resp
    except Exception as err:
        print(f"\n{err}")
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
    while not CONFIRM_INPUTS:
        get_server_details()
        confirm_input()

    # Create the directory for the new server.
    create_dir(DIRECTORY_PATH2)

    # Copy template folder to the new folder.
    print(Fore.GREEN + "\n### Copy the files from the template folder ###")
    print(Style.RESET_ALL)
    
    # Set th source and destination folder paths.
    SRC_PATH1 = "/etc/ansible/prod/serverbuild/buildtemplate/"
    DST_PATH1 = "/etc/ansible/prod/serverbuild/" + SERVER_NAME

    # Copy the files to the new directry.
    copy_files(SRC_PATH1, DST_PATH1)

    FILE_PATH1 = DIRECTORY_PATH2 + "/host.yml"
    FILE_PATH2 = DIRECTORY_PATH2 + "/hostvars.yml"

    REPLACE_DICT1 = {
        'week01' : WEEK01,
        'week02' : WEEK02,
        'week03' : WEEK03
        }
    
    REPLACE_DICT2 = {
        'nic_name' : NIC,
        'resource_group_name' : RESOURCE_GROUP,
        'virtual_network_name' : VIRTUAL_NETWORK,
        'virtual_network_rg_name' : VIRTUAL_NETWORK_RESOURCE_GROUP,
        'subnet_name' : SUBNET,
        'security_group_name' : SECURITY_GROUP,
        'vm_size_name' : VM_SIZE,
        'server_name' : SERVER_NAME,
        'location_name' : LOCATION,
        'sku_name' : SKU,
        'boot_diagnostics_rg_name' : BOOT_DIAGNOSTICS_RESOURCE_GROUP,
        'boot_diagnostics_storage_account_name' : BOOT_DIAGNOSTICS_STORAGE_ACCOUNT,
        'tag_name_name' : TAG_NAME,
        'tag_application_name' : TAG_APPLICATION,
        'tag_owner_name' : TAG_OWNER,
        'tag_costcenter_name' : TAG_COSTCENTER
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
    COMMAND1 = "ansible-playbook playbook1.yml -vvv"
    run_cmd_with_output(COMMAND1)

    time.sleep(30)

    COMMAND2 = "ansible-playbook -i host.yml playbook2.yml -vvv"
    run_cmd_with_output(COMMAND2)


if __name__ == "__main__":
    main()
