# imports
import pandas as pd
import pobapi

MAX_LEN = 48
all_gems = pd.read_json('gems.json')

# functions
def gemSort(all_gems):
    red1, red2, green1, green2, blue1, blue2 = [], [], [], [], [], []
    for index, row in all_gems.iterrows():
        name = str.lower(row['name'])
        color = row['colors'][0]
        isSupport = False
        if "vaal " in name: 
            continue
        elif "awakened " in name: 
            continue
        if 'Support' in row['tags']:
            isSupport = True
        if not isSupport: 
            if color == 'Red':
                red1.append(name)
            elif color == 'Blue': 
                blue1.append(name)
            elif color == 'Green': 
                green1.append(name)
        else: 
            split_name = str.split(name, " support")[0]
            if color == 'Red':
                red2.append(split_name)
            elif color == 'Blue': 
                blue2.append(split_name)
            elif color == 'Green': 
                green2.append(split_name)
    sorted_gems = [red1, red2, green1, green2, blue1, blue2]
    return sorted_gems

def allSubstrings(string):
    test_str = str(string)
    substrings = [test_str[i: j] for i in range(len(test_str)) for j in range(i + 1, len(test_str) + 1)]
    sorted_substrings = sorted(substrings, key = len)
    return sorted_substrings

def createSubstringList(gem_tab):
    substring_list = []
    for gem_name in gem_tab: 
        gem_substring = allSubstrings(gem_name)
        substring_list.append(gem_substring)
    return substring_list

def findUniqueSubstring(gem_tab, substring_list):
    unique_substring_dict = {}
    for i in range(len(substring_list)):
        gem_name = gem_tab[i]
        for substring in substring_list[i]:
            has_match = False
            for j in range(len(substring_list)):
                if i == j:
                    continue
                if substring in substring_list[j]:
                    has_match = True
                    break
            if has_match == False: 
                unique_substring_dict[gem_name] = substring
                break
    return unique_substring_dict

def getSkillGems(pob_url):
    build = pobapi.from_url(pob_url)
    skills = build.skill_gems
    skill_names = [skill.name for skill in skills]
    return skill_names

def getGemSubstrings(skill_gems):
    gem_strings = [[], [], [], [], [], []]
    for raw_gem in skill_gems:
        gem = str.lower(raw_gem)
        if gem in red1_substring: 
            gem_strings[0].append(red1_substring[gem])
        elif gem in red2_substring: 
            gem_strings[1].append(red2_substring[gem])
        elif gem in green1_substring: 
            gem_strings[2].append(green1_substring[gem])
        elif gem in green2_substring: 
            gem_strings[3].append(green2_substring[gem])
        elif gem in blue1_substring: 
            gem_strings[4].append(blue1_substring[gem])
        elif gem in blue2_substring: 
            gem_strings[5].append(blue2_substring[gem])
    return gem_strings 

def listToCopy(gem_string):
    string = '"'
    for i in range(len(gem_string)): 
        if len(string) + len(gem_string[i]) >= MAX_LEN-1:
            string += '"'
            print(string)
            string = '"'
        string += gem_string[i]
        if i < len(gem_string) - 1: 
            string += '|'
    string += '"'
    print(string)
    return

def substringToCopy(gem_strings):
    print("Active Red Gems: ")
    listToCopy(gem_strings[0])
    print("Support Red Gems: ")
    listToCopy(gem_strings[1])
    print("Active Green Gems: ")
    listToCopy(gem_strings[2])
    print("Support Green Gems: ")
    listToCopy(gem_strings[3])
    print("Active Blue Gems: ")
    listToCopy(gem_strings[4])
    print("Support Blue Gems: ")
    listToCopy(gem_strings[5])

# initialize gem tabs with substrings
sorted_gems = gemSort(all_gems)
findUniqueSubstring(sorted_gems[0], createSubstringList(sorted_gems[0]))

red1_substring = findUniqueSubstring(sorted_gems[0], createSubstringList(sorted_gems[0]))
red2_substring = findUniqueSubstring(sorted_gems[1], createSubstringList(sorted_gems[1]))
green1_substring = findUniqueSubstring(sorted_gems[2], createSubstringList(sorted_gems[2]))
green2_substring = findUniqueSubstring(sorted_gems[3], createSubstringList(sorted_gems[3]))
blue1_substring = findUniqueSubstring(sorted_gems[4], createSubstringList(sorted_gems[4]))
blue2_substring = findUniqueSubstring(sorted_gems[5], createSubstringList(sorted_gems[5]))

url = input("Enter PoB pastebin:")
substringToCopy(getGemSubstrings(getSkillGems(url)))