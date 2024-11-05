import pandas as pd
import os
import re

# Function to remove HTML-like tags from content
def remove_tags(text):
    # Regular expression to remove specified HTML tags
    tag_re = re.compile(r'<.*?>')
    return re.sub(tag_re, '', text)

# Clean the CSV by removing tags and handling errors
def clean_csv(file_path):
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Clean the columns by removing HTML tags
        df = df.applymap(lambda x: remove_tags(str(x)) if isinstance(x, str) else x)
        print(f"Successfully read and cleaned {file_path}")
        return df
    except pd.errors.ParserError as e:
        print(f"ParserError processing {file_path}: {e}")
        return None
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

# Add missing quotes to fix formatting issues
def add_missing_quotes(file_path):
    cleaned_lines = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line_number, line in enumerate(file, start=1):
            # Check if line contains a comma and fix quoting
            if ',' in line and not (line.startswith('"') and line.endswith('"\n')):
                line = line.strip().replace(',', '","')
                line = f'"{line}"\n'
            cleaned_lines.append(line)
    return cleaned_lines

# Write the cleaned data to a new CSV file
def write_cleaned_csv(file_path, cleaned_lines):
    new_file_path = f"cleaned_{os.path.basename(file_path)}"
    with open(new_file_path, 'w', encoding='utf-8') as file:
        file.writelines(cleaned_lines)
    print(f"Cleaned data saved to {new_file_path}")

# Main function to process files in a directory
def main(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)

            # Step 1: Clean using Pandas and remove tags
            df = clean_csv(file_path)
            if df is not None:
                # If read successfully, write back to cleaned file
                write_cleaned_csv(file_path, df.to_csv(index=False).splitlines())
            else:
                # Step 2: Attempt to manually clean if reading failed
                cleaned_lines = add_missing_quotes(file_path)
                write_cleaned_csv(file_path, cleaned_lines)

if __name__ == "__main__":
    directory = "C:/Users/Jhouvann/OneDrive/Desktop/College/2ND YEAR/PROG LANGUAGE/Chatbot/CSVS"  # Update with your directory
    main(directory)
