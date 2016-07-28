import os
import re
from string import punctuation
from settings import ROOT_PATH

RES_PATH = '/app/src/main/res'
# LAYOUT_PATH = '/layout'
LAYOUT_PATH = ''
STRINGS_PATH = '/values/strings'

print ROOT_PATH
PATH = ROOT_PATH + RES_PATH + LAYOUT_PATH

def strip_punctuation(s):
    return ''.join(c for c in s if c not in punctuation)

def list_realstrings_to_file(line, filter_result, filename_result):
    if "@string" not in line:
        string_name_in_xml = strip_punctuation(filter_result.lower()).replace(' ', '_')
        
        prefix = '<string name="' + filename_result + '_' + string_name_in_xml + '">'
        suffix = '</string>\n'
        
        final_result = prefix + filter_result + suffix
        return final_result
    else:
        return False

temp_file = []
for root, dirs, files in os.walk(PATH):
    for single_file in sorted(files):
        fullpath = os.path.join(root, single_file)
        # print fullpath
        file_name = single_file.replace('.xml', '')

        if "layout" in root or "menu" in root:
            print file_name
            tag = file_name.split('_', 1)[0]
            filtered_file_name = file_name.split('_', 1)[1]
            filename_result = filtered_file_name + '_' + tag
            
            starting_mark = "<!--"+filename_result+" start-->\n"
            temp_file.append(starting_mark)

            with open(fullpath, 'r') as f:
                for line in f.readlines():
                    if "android:text=" in line:
                        filter_result = re.findall('text="(.*)"', line)[0]
                        final_result = list_realstrings_to_file(line, filter_result, filename_result)
                        if final_result:
                            temp_file.append(final_result)

                    elif "android:hint" in line:
                        filter_result = re.findall('hint="(.*)"', line)[0]
                        final_result = list_realstrings_to_file(line, filter_result, filename_result)
                        if final_result:
                            temp_file.append(final_result)
                    
                    elif "android:digits" in line:
                        filter_result = re.findall('digits="(.*)"', line)[0]
                        final_result = list_realstrings_to_file(line, filter_result, filename_result)
                        if final_result:
                            temp_file.append(final_result)

                    elif "android:title" in line:
                        filter_result = re.findall('title="(.*)"', line)[0]
                        final_result = list_realstrings_to_file(line, filter_result, filename_result)
                        if final_result:
                            temp_file.append(final_result)

            ending_mark = "<!--"+filename_result+" end-->\n"
            temp_file.append(ending_mark)

            new_line = "\n"
            temp_file.append(new_line)

print(temp_file)

with open('result-strings-xml.xml', 'w+') as f:
    for line in temp_file:
        f.writelines(line)