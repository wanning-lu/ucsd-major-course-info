import csv
import json
import re
import glob

def make_json(csvFilePaths, jsonFilePath):
     
    # create a dictionary
    data = {}
     
    # Open a csv reader called DictReader
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        for csvFilePath in csvFilePaths:
            with open(csvFilePath, encoding='utf-8') as csvf:
                jsonf.write('[')
                csvReader = csv.reader(csvf)
                
                # Convert each row into a dictionary 
                # and add it to data
                for row in csvReader:
                    if row[1] != "CS26" and row[1] != "CS25":
                        continue

                    data['core_classes'] = []
                    for col, i in zip(row, range(len(row))):
                        print(col)
                        
                        # if we've reached the end of the major requirements
                        if col == "" and i != 2:
                            break

                        if col == "" and i == 2:
                            continue
                    
                        if i == 0:
                            data['name'] = col
                            continue
                        elif i == 1:
                            data['code'] = col
                            continue
                        
                        # our indicator for electives
                        if col[0] == "!":
                            elective_name = ""
                            count_num = 0

                            if col.find("(") == -1:
                                # we're setting the key to the name of the elective
                                elective_name = col[1:col.find(":")]
                                count_num = 1
                            else:
                                elective_name = col[1:col.find("(")]
                                count_num = int(col[col.find("(")+1])

                            data[elective_name] = []
                            data[elective_name].append(count_num)
                            electives = col[col.find(":")+1:].replace(' or ', ',').split(',')
    
                            # strip any leading or trailing whitespace from each element
                            electives = [elective.strip() for elective in electives]
                            data[elective_name].extend(electives)
                        
                        else:
                            data['core_classes'].append(col)
                        
                    print(data)

                    # Use the json.dumps() function to dump data
                    jsonf.write(json.dumps(data, indent=4))
                    jsonf.write(',\n')

                    data = {}
                
                jsonf.write(']')
    
        
         
csvFilePath1 = r'/Users/wanninglu/Documents/Professional/ucsd-major-course-info/majors/majors.csv'
jsonFilePath = r'/Users/wanninglu/Documents/Professional/ucsd-major-course-info/scripts/majors/majors.json'
 
# Call the make_json function
make_json([csvFilePath1], jsonFilePath)