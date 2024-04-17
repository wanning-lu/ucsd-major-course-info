from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time
import csv

driver = webdriver.Firefox()

driver.get("https://plans.ucsd.edu")

# Selecting a dummy college
college_dropdown = driver.find_element(By.XPATH, '//select[@name="college"]')
college_select = Select(college_dropdown)
college_options = college_select.options

# Using Marshall as the dummy college
college_select.select_by_visible_text(college_options[3].text)
driver.find_element(By.XPATH, '//button').click()

# Give it some time to load
time.sleep(1)

# Selecting the most recent year
year_dropdown = driver.find_element(By.XPATH, '//select[@name="year"]')
year_select = Select(year_dropdown)
year_options = year_select.options
year_select.select_by_visible_text(year_options[1].text)

with open('major-scraper/courses.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile)

    # we're hard coding the indices here since the department options become stale
    for i in range(49):
        department_dropdown = driver.find_element(By.XPATH, '//select[@name="department"]')
        department_select = Select(department_dropdown)
        department_options = department_select.options
        dep_option = department_options[i]

        if (dep_option.text == '--'):
            continue

        # select the current department
        department_select.select_by_visible_text(dep_option.text)

        # just in case the majors take some time to load
        time.sleep(1)

        # now iterate through the majors
        major_dropdown = driver.find_element(By.XPATH, '//select[@name="major"]')
        major_select = Select(major_dropdown)
        major_options = major_select.options
        for major_option in major_options:
            if (major_option.text == '--'):
                continue
            print(major_option.text)

            # select the current major
            major_select.select_by_visible_text(major_option.text)

            # wait for courses to load
            time.sleep(2)

            # select the containers that contain the course info
            courses = driver.find_elements(By.XPATH, '//span[@data-bind="text: name"]')
            course_row = []

            # now iterate through the courses
            for course in courses:
                course_text = course.text

                # text is invalid because it's a header, or it's a non-major/college elective
                if course_text == "Fall" or course_text == "Winter" or course_text == "Spring" or course_text == "ELECTIVE":
                    continue

                # rule out marshall GEs and writing courses
                if course_text == "DOC 1/DEI" or course_text == "DOC 1" or course_text == "DOC 2" or course_text == "DOC 3" or course_text == "GE" or course_text == "UD GE":
                    continue

                course_row.append(course_text)

            # write it to the spreadsheet
            course_row.sort()
            course_row.insert(0, major_option.text)
            csvwriter.writerow(course_row)

