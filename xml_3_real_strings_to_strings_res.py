#!/usr/bin/env python3
import os
import re
from settings import ROOT_PATH

RES_PATH = '/app/src/main/res'
LAYOUT_PATH = '/layout'
STRINGS_PATH = '/values/strings.xml'

full_layout_path = ROOT_PATH + RES_PATH + LAYOUT_PATH
full_strings_path = ROOT_PATH + RES_PATH + STRINGS_PATH

def snakecase_to_camelcase(snake_str):
    components = snake_str.split('_')
    return "".join(x.title() for x in components)

def camelcase_to_snakecase(camel_str):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_str)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

# Change all data from strings.xml to a dictionary data
result = {}
with open(full_strings_path, 'r') as f:
    write_to_dict = False
    key_category = ""
    for line in f.readlines():
        if "start-->" in line:
            key_category = re.findall('<!--(.*) start-->', line)[0]
            key_category = camelcase_to_snakecase(key_category)
            result[key_category] = {}
            write_to_dict = True

        if "string" in line and write_to_dict:
            key = re.findall('name="(.*)"', line)[0]
            if "formatted" in key:
                key = re.findall('(.*)" ', key)[0]
            # print(key)
            
            value = re.findall('">(.*)</string>', line)[0]
            value = value.replace("\\", "")
            
            result[key_category][key] = value

        if "end-->" in line:
            write_to_dict = False
            

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


for root, dirs, files in os.walk(full_layout_path):
    for single_file in sorted(files):
        fullpath = os.path.join(root, single_file)
        # print(fullpath)
        file_name = single_file.replace('.xml', '')

        tag = file_name.split('_', 1)[0]
        filtered_file_name = file_name.split('_', 1)[1]
        filename_result = filtered_file_name + '_' + tag
        # filename_result = snakecase_to_camelcase(filename_result)

        try:
            if result[filename_result]:
                # print result[filename_result]
                temp_file = []
                with open(fullpath, 'r') as f:
                    for line in f.readlines():                        
                        filter_result = re.findall('text="(.*)"', line)

                        if filter_result:
                            # print filter_result
                            # filter_result = filter_result.replace('', '')
                            # if filter_result in result[file_name]:
                                # print True
                            filter_result = filter_result[0]

                            for key, value in result[filename_result].iteritems():
                                # print key
                                # print value
                                if value==filter_result:
                                    
                                    string_before = '"' + value + '"'
                                    string_after = '"@string/' + key + '"'
                                    line = line.replace(string_before, string_after)
                                    print line
                        
                        temp_file.append(line)
                
                with open(fullpath, 'w+') as f:
                    for line in temp_file:
                        f.writelines(line)        
            else:
                print False

        except KeyError, e:
            print e

        # if result[file_name]:
        #     temp_file = []
        #     with open(fullpath, 'r') as f:
        #         for line in f.readlines():
        #             if '"' in line:
        #                 filter_result = re.findall('"(.*)"', line)[0]
        #                 # filter_result = filter_result.replace('', '')
        #                 # if filter_result in result[file_name]:
        #                     # print True

        #                 for key, value in result[file_name].iteritems():
        #                     # print key
        #                     # print value
        #                     if value in line:
        #                         string_before = '"' + value + '"'
        #                         string_after = 'AndroidUtilities.getString(R.string.' + key + ')'
        #                         line = line.replace(string_before, string_after)

        #                 print line

        #             temp_file.append(line)

        #     # with open(fullpath, 'w+') as f:
        #     #     for line in temp_file:
        #     #         f.writelines(line)

        # else:          
        #     print False