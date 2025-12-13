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
            with open(csvFilePath, encoding='utf-8') as csvf:
                csvReader = csv.DictReader(csvf)
                
                # Convert each row into a dictionary 
                # and add it to data
                for rows in csvReader:

                    numbers = [i for i in range(1,10)]
                    
                    data['course_code'] = rows['course_code']
                    data['course_name'] = rows['name']
                    data['units'] = int(rows['units']) if rows['units'].isnumeric() else rows['units']
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
   
         
# csvFilePath1 = r'/Users/chezzie/Documents/Professional/ucsd-major-course-info/courses/edited/CSE.csv'
# csvFilePath2 = r'/Users/chezzie/Documents/Professional/ucsd-major-course-info/courses/edited/MATH.csv'
# csvFilePath3 = r'/Users/chezzie/Documents/Professional/ucsd-major-course-info/courses/edited/ECE.csv'
# csvFilePath4 = r'/Users/chezzie/Documents/Professional/ucsd-major-course-info/courses/edited/DSC.csv'
# jsonFilePath = r'/Users/chezzie/Documents/Professional/ucsd-major-course-info/scripts/courses/CSE.json'
 
# # Call the make_json function
# make_json([csvFilePath1, csvFilePath2, csvFilePath3, csvFilePath4], jsonFilePath)