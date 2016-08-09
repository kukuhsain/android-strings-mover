#!/usr/bin/env python3
import os
import re
from settings import ROOT_PATH, JAVA_PROJECT_PATH

JAVA_UI_PATH = '/ui'
RES_PATH = '/app/src/main/res'
STRINGS_PATH = '/values/strings.xml'

full_java_ui_path = ROOT_PATH + JAVA_PROJECT_PATH + JAVA_UI_PATH
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
            
# for key in result:
    # print result[key]

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


for root, dirs, files in os.walk(full_java_ui_path):
    for single_file in sorted(files):
        fullpath = os.path.join(root, single_file)
        # print(fullpath)
        # file_name = single_file.replace('.xml', '')
        # print("<!--"+file_name+" start-->")

        temp_file = []
        with open(fullpath, 'r') as f:
            for line in f.readlines():
                if 'R.string' in line:
                    filter_results = re.findall('R.string.(.*?)\)', line)
                    # filter_result = filter_result.replace(')', '')
                    for filter_result in filter_results:
                        print(filter_result)
                        print(fullpath)

                        key = filter_result
                        filter_result_added = 'R.string.' + filter_result
                        try:
                            after_converted = '"' + result[key] + '"'
                            
                            if "getString" in line:
                                filter_result_added = "getString(" + filter_result_added + ")"
                                line = line.replace(filter_result_added, after_converted)
                            else:
                                line = line.replace(filter_result_added, after_converted)

                            # print(after_converted)
                            # print(line)
                        except KeyError:
                            # print('Key not found')
                            pass
                temp_file.append(line)
        
        with open(fullpath, 'w+') as f:
            for line in temp_file:
                f.writelines(line)


        # print("<!--"+file_name+" end-->")
        # print("")