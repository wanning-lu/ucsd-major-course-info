from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()
driver.get("https://catalog.ucsd.edu/curric/BDAAS.html")

courses = driver.find_elements(By.XPATH, '//li[@class="course-list-overview"]')

for course in courses:
    print(course.text[0:course.text.find(".")], "or")