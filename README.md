# Android Strings Mover
This repo contains some script to move strings from java and xml files to strings res in an Android project.
Written in python 2.7

## XML Part
### 1. xml_1_strings_to_real_strings
Move '@string/any_string' to be real strings

### 2. xml_2_list_text_to_strings_res
Get all strings from layout and write them to a file with some specific format

## Java Part
### 1. java_1_strings_to_real_strings
Move 'R.string.[any_string]' to be real strings

### 2. java_2_list_text_to_strings_res
Get all strings from layout and write them to a file with some specific format

### 3. java_3_real_strings_to_strings_res
Change all necessary strings in java to be using coresponding strings from strings res