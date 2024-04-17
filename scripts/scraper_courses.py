from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time
import csv
import re

# code for finding "and" as a standalone word and its first occurrence
def find_and_index(text):
    # regex for "and" as a standalone word
    pattern = r'\band\b'

    # use re.search() to find the first occurrence of the pattern in the text
    match = re.search(pattern, text)

    # if a match is found, return the index of the start of the match
    if match:
        return match.start()
    return -1

driver = webdriver.Firefox()

# hardcoding this again; since each time, the list is ordered by how soon it appears on screen
# just means there are 86 valid course pages
for i in range(86):
    # go back to the main list of departments
    driver.get("https://catalog.ucsd.edu/front/courses.html")

    # go to the current selected department's courses
    driver.find_elements(By.XPATH, "//a[contains(text(), 'courses')]")[i].click()

    names = driver.find_elements(By.XPATH, '//p[@class="course-name"]')
    # since not all of the <p> elements have the class course-descriptions...why? i dont know
    descriptions = driver.find_elements(By.XPATH, f'//p[@class="course-name"]/following-sibling::p[1]')

    department = driver.find_element(By.XPATH, '//h1').text
    # write each department into its own csv file
    with open(f"courses/{department}.csv", 'w') as csvfile:

        csvwriter = csv.DictWriter(csvfile, fieldnames=["course_code", "name", "units", "desc", "prereq1", "prereq2", "prereq3", "prereq4", "prereq5", "prereq6", "prereq7", "prereq8", "prereq9", "misc_prereq"])
        csvwriter.writeheader()

        # iterate through all of the courses (which is equal to the number of course names)
        for j in range(len(names)):

            row_to_insert = {}

            course_code = names[j].text[0:names[j].text.find(".")]
            name = names[j].text[names[j].text.find(".")+2:]
            units = name[name.find("(") + 1:name.find(")")]
            name = name[:name.find("(") - 1]

            # some courses don't have prereqs
            if descriptions[j].text.find("Prerequisites: ") == -1:
                description = descriptions[j].text
            else:
                description = descriptions[j].text[0:descriptions[j].text.find("Prerequisites: ")]
                prerequisites = descriptions[j].text[descriptions[j].text.find("Prerequisites: ") + 15:]

                # MOST prerequisites have a split between their actual prereqs and the misc, delineated with a ; or .
                # here I'm making the split prematurely
                if prerequisites[0:2].isupper():
                    if prerequisites.find(";") != -1:
                        row_to_insert["misc_prereq"] = prerequisites[prerequisites.find(";") + 2:prerequisites.find(";") + 3].upper() + prerequisites[prerequisites.find(";") + 3:]
                        prerequisites = prerequisites[0:prerequisites.find(";")]
                    elif prerequisites.find(".") != -1:
                        row_to_insert["misc_prereq"] = prerequisites[prerequisites.find(".") + 2:prerequisites.find(".") + 3].upper() + prerequisites[prerequisites.find(".") + 3:]
                        prerequisites = prerequisites[0:prerequisites.find(".")]
                else:
                    if "none" not in prerequisites:
                        row_to_insert["misc_prereq"] = prerequisites[:1].upper() + prerequisites[1:]
                    prerequisites = ""

                prereq_index = 1
                # iterate over the prereqs while the string isn't empty
                while prerequisites:
                    if find_and_index(prerequisites) == -1:
                        row_to_insert[f'prereq{prereq_index}'] = prerequisites
                        prerequisites = ""
                    else:
                        row_to_insert[f'prereq{prereq_index}'] = prerequisites[0:find_and_index(prerequisites) - 1]
                        prerequisites = prerequisites[find_and_index(prerequisites)+4:]
                        prereq_index += 1

            row_to_insert["course_code"] = course_code
            row_to_insert["name"] = name
            row_to_insert["units"] = units
            row_to_insert["desc"] = description

            csvwriter.writerow(row_to_insert)






