#!/usr/bin/env python3
# Import modules for communication
import requests
import json
import os
import time
import shutil
import re

# default url for all robots
url = "http://192.168.89.71/api/v2.0.0"

# Unlock code for admin level
admin = {
    'Authorization': 'Basic YWRtaW46OGM2OTc2ZTViNTQxMDQxNWJkZTkwOGJkNGRlZTE1ZGZiMTY3YTljODczZmM0YmI4YTgxZjZmMm'
                     'FiNDQ4YTkxOA==',
    'Content-Type': 'application/json'
}

# data for PUT & POST functions # GET functions leave blank
payload = ""

# Specific Function Initialization
# *************************************************************************************************
missions = "/missions"
actions = "/actions"
actions_guid = ""
m_list_all = []
m_list_final = []
m_actions_list = []
time_object = time.localtime()  # local time
local_time = time.strftime("%Y%m%d", time_object)
i = 0
sub = "mirconst"
# API Commands
# *************************************************************************************************
# Get Mission List
get_robot_missions = requests.request("GET", url + missions, headers=admin, data=payload)

# Format Information
# *************************************************************************************************
# print(get_robot_missions)
read_missions = json.loads(get_robot_missions.text)
# print(*read_missions, sep="\n")

for m_info in read_missions:
    # m_list_all.append([m_info['guid'], m_info['name']])
    if sub in m_info['guid']:
        pass
    else:
        m_list_final.append([m_info['guid'], m_info['name']])

# print(*m_list_all, sep="\n")
# print(*m_list_final, sep="\n")

# Write to file
# *************************************************************************************************
# Create copy of list template and rename for date of creation
# using shutil
shutil.copyfile('mission_list_template.txt', 'Komatsu Mission List'+local_time+'.txt')  # src,dst
# Write to copied file
with open('Komatsu Mission List'+local_time+'.txt', 'w') as file:
    file.write("['GUID', 'Mission Name']\n")
    for item in m_list_final:
        file.write("%s\n" % item)
    # print("Summary Mission List Write Successful")

# Create copies from templates and rename them to the Mission Names
# using shutil
for i in range(len(m_list_final)):
    # print(str(m_list_final[i][1]) + " " + local_time + ".txt")  # Prints element of list within list
    shutil.copyfile('mission_template.txt', m_list_final[i][1] + " " + local_time + ".txt")

# Write to copied files
# *************************************************************************************************
for item in range(len(m_list_final)):
    mission_guid = str(m_list_final[item][0])
    # print(mission_guid)
    mission_actions = missions + "/" + mission_guid + actions
    # print(mission_actions)
    with open(m_list_final[item][1] + " " + local_time + ".txt", 'w') as file:
        get_robot_mission_actions = requests.request("GET", url + mission_actions, headers=admin, data=payload)

        mission_act = json.loads(get_robot_mission_actions.text)
        # print(type(mission_act))
        # print(*mission_act, sep="\n")
        for action in range(len(mission_act)):
            for key, value in mission_act[action].items():
                if key == "priority":
                    continue
                elif key == "parameters":
                    file.write("%s\n" % key)
                    value1 = str(value).replace('[', '')
                    value2 = value1.replace('{', '')
                    value3 = value2.replace(',', '\n')
                    value4 = value3.replace('}', '')
                    value5 = value4.replace(']', '')
                    value6 = re.sub(r"([' guid'']i).{41}", r"\1", value5)
                    value7 = value6.replace("'gui'", '')
                    file.write("%s" % value7)
                    file.write("\n")
                elif key == "mission_id":
                    continue
                elif key == "url":
                    continue
                elif key == "guid":
                    file.write("\n\n")
                    continue
                    # file.write("%s" % key)
                    # file.write(' : ')
                    # file.write("%s\n\n" % value)
                else:
                    file.write("%s" % key)
                    file.write(' : ')
                    file.write("%s\n" % value)
        # print("Write Successful")
