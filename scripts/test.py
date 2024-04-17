import re

def find_and_index(text):
    # Define a regular expression pattern to match "and" as a standalone word
    pattern = r'\band\b'

    # Use re.search() to find the first occurrence of the pattern in the text
    match = re.search(pattern, text)

    # If a match is found, return the index of the start of the match
    if match:
        return match.start()

    # If no match is found, return None
    return None

# Example usage:
text = "This is a sampleand text and it contains the word 'and' as well."
index = find_and_index(text)
print("Index of 'and' as a standalone word:", text[index:])