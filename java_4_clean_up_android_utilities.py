#!/usr/bin/env python3
import os
import re
from settings import ROOT_PATH, JAVA_PROJECT_PATH

JAVA_UI_PATH = '/ui'
RES_PATH = '/app/src/main/res'
STRINGS_PATH = '/values/strings.xml'

full_java_ui_path = ROOT_PATH + JAVA_PROJECT_PATH + JAVA_UI_PATH
full_strings_path = ROOT_PATH + RES_PATH + STRINGS_PATH


for root, dirs, files in os.walk(full_java_ui_path):
    for single_file in sorted(files):
        fullpath = os.path.join(root, single_file)

        temp_file = []
        with open(fullpath, 'r') as f:
            for line in f.readlines():
                if 'AndroidUtilities."' in line:
                    line = line.replace('AndroidUtilities."', '"')
                    print line
                temp_file.append(line)

        with open(fullpath, 'w+') as f:
            for line in temp_file:
                f.writelines(line)
