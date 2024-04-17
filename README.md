# UCSD Course and Major Information

Information on UCSD courses and majors scraped from publicly available data on UCSD websites. The data in `majors.csv` was also curated to be more detailed (and therefore, useful).

Here's a list of categories that each course or major object has.

## Courses

| Category    | Description | Example |
| -------- | ------- | ------- | 
| `course_code`  | The course code corresponding to each unique course.   | CSE 100 |
| `name` | The course name corresponding to the course code.     | "Advanced Data Structures"
| `units`    | The number of units a course fulfills.    | 4 |
| `desc` | The description corresponding to the course, as provided on the course catalog | "High-performance data structures and supporting algorithms. Use and implementation of data structures..." (truncated for brevity) |
| `prereqs` | An array of the different prerequisites needed to enroll in the course. Each item in the array corresponds to a list of different courses that can be used to fulfill one prerequisite. | [ [CSE 21, MATH 154, MATH 158, MATH 184, MATH 188], [CSE 12], [CSE 15L], [CSE 30, ECE 15] ] |
| `misc_info` | Other important information pertaining to the course. | "Restricted to undergraduates. Students may not receive credit for both CSE 100R and CSE 100." |

## Majors

| Category    | Description | Example |
| -------- | ------- | ------- | 
| `major` | The name of the major. | Mathematics-Computer Science |
| `major_code` | The alphanumeric code corresponding to the major. | MA30 |
| `requirements` | An array of the major requirements. May have arrays as elements for elective possibilities. | [[CSE 11, CSE 8A/B], CSE 12, CSE 15L, ...]