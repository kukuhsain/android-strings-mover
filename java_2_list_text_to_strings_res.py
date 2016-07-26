import os
import re
from string import punctuation
from settings import ROOT_PATH, JAVA_PROJECT_PATH

JAVA_UI_PATH = '/ui'

PATH = ROOT_PATH + JAVA_PROJECT_PATH + JAVA_UI_PATH

# Convert CamelCase to snake_case
def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def strip_punctuation(s):
    return ''.join(c for c in s if c not in punctuation)

temp_file = []
for root, dirs, files in os.walk(PATH):
    for single_file in sorted(files):
        fullpath = os.path.join(root, single_file)
        print root
        print fullpath
        
        # file_name = re.findall('consultant/(.*).java', fullpath)
        # file_name = file_name[0].replace('/', '.')

        file_name = single_file.replace('.java', '')
        
        starting_mark = "<!--"+file_name+" start-->\n"
        temp_file.append(starting_mark)

        with open(fullpath, 'r') as f:
            for line in f.readlines():
                if '"' in line:
                    # if "@string" in line:
                        # break
                    # whitespaces_removed = line.replace("  ", "")
                    # prefixes_removed = whitespaces_removed.replace('android:text="', "")
                    # suffixes_removed = prefixes_removed.replace('"\n', "")

                    filter_result = re.findall('"(.*)"', line)[0]
                    # file_name_in_xml = file_name.rsplit('.', 1)[1]
                    # file_name_in_xml = convert(file_name_in_xml)

                    file_name_in_xml = convert(file_name)

                    prefix = '<string name="' + file_name_in_xml + '_' + strip_punctuation(filter_result.lower()).replace(' ', '_') + '">'
                    suffix = '</string>\n'
                    
                    final_result = prefix + filter_result + suffix
                    temp_file.append(final_result)
        ending_mark = "<!--"+file_name+" end-->\n"
        temp_file.append(ending_mark)

        new_line = "\n"
        temp_file.append(new_line)

print(temp_file)

with open('result-strings-java.xml', 'w+') as f:
    for line in temp_file:
        f.writelines(line)