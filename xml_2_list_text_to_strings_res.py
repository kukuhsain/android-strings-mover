import os
from string import punctuation
from settings import ROOT_PATH

RES_PATH = '/app/src/main/res'
LAYOUT_PATH = '/layout'
STRINGS_PATH = '/values/strings'

print ROOT_PATH
PATH = ROOT_PATH + RES_PATH + LAYOUT_PATH

def strip_punctuation(s):
    return ''.join(c for c in s if c not in punctuation)

temp_file = []
for root, dirs, files in os.walk(PATH):
    for single_file in sorted(files):
        fullpath = os.path.join(PATH, single_file)
        # print fullpath
        file_name = single_file.replace('.xml', '')
        
        starting_mark = "<!--"+file_name+" start-->\n"
        temp_file.append(starting_mark)

        with open(fullpath, 'r') as f:
            for line in f.readlines():
                if "android:text=" in line:
                    if "@string" in line:
                        break
                    whitespaces_removed = line.replace("  ", "")
                    prefixes_removed = whitespaces_removed.replace('android:text="', "")
                    suffixes_removed = prefixes_removed.replace('"\n', "")
                    final_text = suffixes_removed

                    string_name_in_xml = strip_punctuation(final_text.lower()).replace(' ', '_')

                    tag = file_name.split('_', 1)[0]
                    filtered_file_name = file_name.split('_', 1)[1]
                    filename_result = filtered_file_name + '_' + tag
                    
                    prefix = '<string name="' + filename_result + '_' + string_name_in_xml + '">'
                    suffix = '</string>\n'
                    
                    final_result = prefix + final_text + suffix
                    temp_file.append(final_result)
        ending_mark = "<!--"+file_name+" end-->\n"
        temp_file.append(ending_mark)

        new_line = "\n"
        temp_file.append(new_line)

print(temp_file)

with open('result-strings-xml.xml', 'w+') as f:
    for line in temp_file:
        f.writelines(line)