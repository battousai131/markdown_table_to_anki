import pandas as pd
from tabulate import tabulate
import csv
import genanki

# Read the Markdown file
with open('test.md', 'r') as file:
    markdown_data = file.read()

#print(markdown_data)

# Find the tables in the Markdown data
tables = markdown_data.split('##')[1:]

#print(tables)
csv_files = []

# Process each table
for i, table in enumerate(tables):
    # Extract the table data
    rows = [row.split('|')[1:-1] for row in table.strip().split('\n')[2:]]

    # Create a pandas DataFrame from the table data
    df = pd.DataFrame(rows, columns=['Accro', 'Description'])
    df = df.iloc[2:]
    # Save the DataFrame as a CSV file
    filename = f'table_{i+1}.csv'
    df.to_csv(filename, index=False)
    csv_files.append(filename)

print(csv_files)

def create_anki_deck(csv_file, deck_name):
    # Read the CSV file
    with open(csv_file, 'r') as file:
        csv_data = list(csv.reader(file))

    # Create an empty list to hold all the notes
    all_notes = []

    # Iterate over each line of the CSV data
    for i, row in enumerate(csv_data):
        # Skip the header row
        if i == 0:
            continue

        # Extract the fields from the CSV row
        accro, description = row

        # Create an Anki Model
        model_id = hash(accro)
        model_name = f"Model_{i}"
        model_fields = [
            {"name": "Accro"},
            {"name": "Description"}
        ]
        model_templates = [
            {
                "name": "Card 1",
                "qfmt": "{{Accro}}",
                "afmt": "{{FrontSide}}<hr id='answer'>{{Description}}"
            }
        ]
        model = genanki.Model(model_id, model_name, fields=model_fields, templates=model_templates)

        # Create an Anki Note
        note = genanki.Note(
            model=model,
            fields=[accro, description]
        )

        # Add the note to the list of all notes
        all_notes.append(note)

    # Create an Anki Deck and add all the notes
    deck_id = hash(deck_name)
    deck = genanki.Deck(deck_id, deck_name)
    for note in all_notes:
        deck.add_note(note)

    # Generate the Anki Package
    package = genanki.Package(deck)

    # Save the Anki Package to a file
    filename = f"{deck_name}.apkg"
    package.write_to_file(filename)

# Call the function for each CSV file

for file in csv_files:
    deck_name = file.split('.')[0]
    create_anki_deck(file, deck_name)