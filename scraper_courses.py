from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time
import csv

driver = webdriver.Firefox()

with open('courses.csv', 'w') as csvfile:

    csvwriter = csv.DictWriter(csvfile, fieldnames=["course_code", "name", "units", "desc", "prereq1", "prereq2", "prereq3", "prereq4", "prereq5", "prereq6", "prereq7", "prereq8", "prereq9", "misc_prereq"])
    csvwriter.writeheader()
    
    row_to_insert = {}

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

        # for j in range(len(names)):
        #     descriptions.append(driver.find_element(By.XPATH, f'//p[@class="course-name"]/following-siblings::p[1]'))
        # descriptions = driver.find_elements(By.XPATH, '//p[@class="course-descriptions"]')
        # print(len(names))
        # print(len(descriptions))

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

                prereq_index = 1
                while prerequisites[0:2].isupper():
                    if prerequisites.find("and") == -1:
                        if prerequisites.find(";") != -1:
                            row_to_insert[f'prereq{prereq_index}'] = prerequisites[0:prerequisites.find(";")]
                            prerequisites = prerequisites[prerequisites.find(";") + 1:]
                        elif prerequisites.find(".") != -1:
                            row_to_insert[f'prereq{prereq_index}'] = prerequisites[0:prerequisites.find(".")]
                            prerequisites = prerequisites[prerequisites.find(".") + 1:]
                        else:
                            row_to_insert[f'prereq{prereq_index}'] = prerequisites
                            prerequisites = ""
                    else:
                        row_to_insert[f'prereq{prereq_index}'] = prerequisites[0:prerequisites.find("and") - 1]
                        prerequisites = prerequisites[prerequisites.find("and")+4:]
                        prereq_index += 1

                if "none" not in prerequisites:
                    row_to_insert["misc_prereq"] = prerequisites


            row_to_insert["course_code"] = course_code
            row_to_insert["name"] = name
            row_to_insert["units"] = units
            row_to_insert["desc"] = description

            csvwriter.writerow(row_to_insert)






