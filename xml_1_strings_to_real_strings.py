#!/usr/bin/env python3
import os
import re
from settings import ROOT_PATH

RES_PATH = '/app/src/main/res'
# LAYOUT_PATH = '/layout'
LAYOUT_PATH = ''
STRINGS_PATH = '/values/strings.xml'

full_layout_path = ROOT_PATH + RES_PATH + LAYOUT_PATH
full_strings_path = ROOT_PATH + RES_PATH + STRINGS_PATH


# Change all data from strings.xml to a dictionary data
result = {}
with open(full_strings_path, 'r') as f:
    for line in f.readlines():
        if "string" in line and "<!--" not in line:
            key = re.findall('name="(.*)"', line)[0]
            if "formatted" in key:
                key = re.findall('(.*)" ', key)[0]
            # print(key)
            
            value = re.findall('">(.*)</string>', line)[0]
            value = value.replace("\\", "")
            
            result[key] = value
            
print(result)

# temp_file = []
# with open('activity_chat.xml', 'r') as f:
#     for line in f.readlines():
#         if "android:text=" in line:
#             filter_result = re.findall('text="(.*)"', line)[0]
#             print(filter_result)

#             if "@string/" in filter_result:
#                 key = filter_result.replace("@string/", "")
#                 try:
#                     after_converted = result[key]
#                     print(after_converted)
#                     line = line.replace(filter_result, after_converted)
#                 except KeyError:
#                     print('Key not found')
#         temp_file.append(line)

# with open('activity_chat.xml', 'w+') as f:
#     for line in temp_file:
#         f.writelines(line)


def stringres_to_realstring(line, filter_result):
    if "@string/" in filter_result:
        key = filter_result.replace("@string/", "")
        # print key
        if key in result:
            after_converted = result[key]
            line = line.replace(filter_result, after_converted)
            # print(line)
            return line
        else:
            return line
    else:
        return line


for root, dirs, files in os.walk(full_layout_path):
    for single_file in sorted(files):
        fullpath = os.path.join(root, single_file)
        # print(fullpath)
        file_name = single_file.replace('.xml', '')
        # print("<!--"+file_name+" start-->")

        temp_file = []
        if "layout" in root or "menu" in root:
            with open(fullpath, 'r') as f:
                for line in f.readlines():
                    # print line
                    if "android:text=" in line:
                        filter_result = re.findall('text="(.*)"', line)[0]
                        line = stringres_to_realstring(line, filter_result)
                        # print line

                    elif "android:hint=" in line:
                        filter_result = re.findall('hint="(.*)"', line)[0]
                        line = stringres_to_realstring(line, filter_result)
                        # print line

                    elif "android:digits=" in line:
                        filter_result = re.findall('digits="(.*)"', line)[0]
                        line = stringres_to_realstring(line, filter_result)
                        # print line

                    elif "android:title=" in line:
                        filter_result = re.findall('title="(.*)"', line)[0]
                        line = stringres_to_realstring(line, filter_result)
                        # print line

                    print line
                    temp_file.append(line)
                    # print temp_file
        
            with open(fullpath, 'w+') as f:
                for line in temp_file:
                    f.writelines(line)


        # print("<!--"+file_name+" end-->")
        # print("")