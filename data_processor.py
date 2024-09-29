import json
import re
import os


def is_title_or_number(line):
    # Check if the line contains only capital letters and punctuation
    return bool(re.match(r'^[A-Z\s\W]+$', line.strip()))

def is_roman_numeral( line):
    # Check if the line contains only a Roman numeral
    return bool(re.match(r'^[IVXLCDM]+\.?$', line.strip()))

def open_file(raw_file):
    with open(raw_file, 'r', encoding='utf-8') as f:
        return f.read()


class PoemCleaner:
    def __init__(self, raw_file):
        self.loaded_file = open_file(raw_file)

    def clean_text(self):
        # Split the raw text into lines
        lines = self.loaded_file.splitlines()

        cleaned_poems = []
        current_poem = []
        current_title = "NO TITLE"
        empty_line_count = 0

        for line in lines:
            # Check if the line is a Roman numeral, skip it
            if is_roman_numeral(line):
                continue

            # Check if the line is a title (uppercase letters and punctuation)
            if is_title_or_number(line):
                # If a title is found, set current_title
                current_title = line.strip()
                continue

            # Check for empty lines
            if not line.strip():
                empty_line_count += 1

                # If there are more than one empty line, treat it as end of poem
                # I am not completely sure how I made this work but it works. Don't touch it Because this should only
                # be triggered when the poem is finished, but I see the \m\m after every paragraph, but nowhere else
                # I add the \n\n to the poem_text except for in this loop.

                if empty_line_count > 1 and current_poem:
                    # Add the current poem to cleaned_poems
                    poem_text = "<START> " + "\n\n".join(current_poem) + " <END>" # Can't add \ to an f-string
                    cleaned_poems.append({
                        "title": current_title,
                        "text": poem_text
                    })
                    current_poem = []
                    current_title = "NO TITLE"  # Reset title for the next poem
                continue
            else:
                # Non-empty line resets the empty_line_count
                empty_line_count = 0

            # Add the line to the current poem
            current_poem.append(line.strip())

        # # Append the last poem if there is no trailing empty line
        # if current_poem:
        #     print("i am here")
        #     cleaned_poems.append({
        #         "title": current_title,
        #         "text": "\n\n\n".join(current_poem)
        #     })

        return cleaned_poems

    def to_json(self, output_directory, file_name):
        cleaned_poems = self.clean_text()

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Save to .json format
        with open(os.path.join(output_directory, file_name), 'w', encoding='utf-8') as f:
            json.dump(cleaned_poems, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    raw_dataset = 'Dataset/Raw/Emily_dickinson_raw_data'
    output_filename = 'cleaned_poems.json'
    output_dir = 'Dataset/Cleaned'

    cleaner = PoemCleaner(raw_dataset)
    cleaned_text = cleaner.clean_text()

    cleaner.to_json(output_dir ,output_filename)
