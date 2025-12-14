import csv
import json
import re
import sys, os
import glob

def make_json(csvFilePaths, jsonFilePath):
     
    # create a dictionary
    data = {}
     
    # Open a csv reader called DictReader
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        for csvFilePath in csvFilePaths:
            if csvFilePath == "/Users/wanninglu/Documents/Professional/ucsd-major-course-info/courses/edited/.DS_Store":
                continue
            with open(csvFilePath, encoding='utf-8') as csvf:
                csvReader = csv.DictReader(csvf)
                print(csvFilePath)
                
                # Convert each row into a dictionary 
                # and add it to data
                for rows in csvReader:

                    numbers = [i for i in range(1,10)]
                    
                    # slash means that the course is cross listed
                    # two cases for the slash: course code before slash or after
                    if "/" in rows['course_code']:
                        # SPECIAL CASE FOR HISTORY (HILD)
                        if rows['course_code'][rows['course_code'].find("/") + 1] == "2":
                            course_abrv = rows['course_code'][:rows['course_code'].find(" ")]
                            codes = rows['course_code'][rows['course_code'].find(" ") + 1:].split("/")
                            for i, code in enumerate(codes):
                                if not code.isdigit():
                                    continue
                                data['course_code'] = course_abrv + " " + code
                                data['course_name'] = rows['name']
                                data['units'] = int(rows['units']) if rows['units'].isdigit() else rows['units']
                                data['desc'] = rows['desc']
                                data['misc_prequisites'] = rows['misc_prereq']
                                data['prerequisites'] = []
                                jsonf.write(json.dumps(data, indent=4))
                                jsonf.write(',\n')
                                data = {}
                            continue
                        elif ' ' in rows['course_code'][:6]:
                            data['course_code'] = rows['course_code'][:rows['course_code'].find("/")]
                        else:
                            data['course_code'] = rows['course_code'][:rows['course_code'].find("/")] + " " + rows['course_code'][rows['course_code'].find(" ") + 1:]
                    # comma also means cross listed
                    elif "," in rows['course_code']:
                        data['course_code'] = rows['course_code'][:rows['course_code'].find(",")]
                    # this means it's a course chain!
                    elif "-" in rows['course_code']:
                        codes = rows['course_code'][rows['course_code'].rfind("A"):]
                        course_abrv = rows['course_code'][:rows['course_code'].rfind("A")]
                        print(course_abrv)
                        codes = codes.split("-")
                        units = rows['units'].split('-')
                        for i, code in enumerate(codes):
                            data['course_code'] = course_abrv + code
                            data['course_name'] = rows['name'] + f' {i+1}'
                            if i >= len(units):
                                data['units'] = int(units[len(units) - 1]) if units[len(units) - 1].isdigit() else units[len(units) - 1]
                            else:
                                data['units'] = int(units[i]) if units[i].isdigit() else units[i]
                            data['desc'] = rows['desc']
                            data['misc_prequisites'] = rows['misc_prereq']
                            if i == 0:
                                data['prerequisites'] = []
                            else: 
                                data['prerequisites'] = [course_abrv + codes[i-1]]
                            jsonf.write(json.dumps(data, indent=4))
                            jsonf.write(',\n')
                            data = {}
                        continue
                    # SPECIAL CASE FOR POLISCI
                    elif " or " in rows['course_code']:
                        course_abrv = rows['course_code'][:rows['course_code'].find(" ")]
                        codes = re.findall(r'\d+[A-Za-z]?', rows['course_code'])
                        for i, code in enumerate(codes):
                            if i == 0:
                                data['course_name'] = rows['name']
                            else:
                                data['course_name'] = rows['name'] + " with discussion"

                            data['course_code'] = course_abrv + " " + code
                            data['units'] = int(rows['units']) if rows['units'].isdigit() else rows['units']
                            data['desc'] = rows['desc']
                            data['misc_prequisites'] = rows['misc_prereq']
                            data['prerequisites'] = []
                            jsonf.write(json.dumps(data, indent=4))
                            jsonf.write(',\n')
                            data = {}
                        continue
                    else:
                        if rows['course_code'][rows['course_code'].find(" ") + 1:].isdigit():
                            data['course_code'] = rows['course_code'][:rows['course_code'].find(" ") + 1] + str(int(rows['course_code'][rows['course_code'].find(" ") + 1:]))
                        else:
                            data['course_code'] = rows['course_code']

                    data['course_name'] = rows['name']
                    data['units'] = int(rows['units']) if rows['units'].isdigit() else rows['units']
                    data['desc'] = rows['desc']
                    data['misc_prequisites'] = rows['misc_prereq']
                    data['prerequisites'] = []

                    for i in numbers:
                        if rows[f'prereq{i}'] == '':
                            break

                        # Split the string into an array using case-insensitive regex
                        prereq = re.split(r'\s+or\s+', rows[f'prereq{i}'], flags=re.IGNORECASE)
                        for i in range(len(prereq)):
                            if rows['course_code'][:rows['course_code'].find(' ')] not in prereq[i] and not prereq[i][0].isalpha():
                                prereq[i] = rows['course_code'][:rows['course_code'].find(' ')] + " " + prereq[i]
                        data['prerequisites'].append(prereq)
        
                    # Use the json.dumps() function to dump data
                    jsonf.write(json.dumps(data, indent=4))
                    jsonf.write(',\n')

                    data = {}

filePath = '/Users/wanninglu/Documents/Professional/ucsd-major-course-info/courses/edited/' # change this to your file path!
jsonFilePath = '/Users/wanninglu/Documents/Professional/ucsd-major-course-info/scripts/courses/courses.json' # change this too



# create one massive json file with all course data
if len(sys.argv) == 1:
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write('[')
        make_json([filePath + course_code for course_code in os.listdir(filePath)], jsonFilePath)
        jsonf.write(']')
    
# choose a specific file(s)
else:
    for course_code in sys.argv[1:]:
        if course_code.upper() + '.csv' not in os.listdir(filePath):
            print("erm...that course code doesn't exist!")
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write('[')
        for course_csv in sys.argv[1:]:
            make_json([filePath + course_csv], jsonFilePath)
        jsonf.write(']')