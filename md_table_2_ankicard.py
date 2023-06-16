import csv
import genanki
import re

def create_anki_decks(markdown_file):
    # Read the Markdown file
    with open(markdown_file, 'r') as file:
        markdown_data = file.read()

    # Split the Markdown data into sections based on "##" headers
    sections = re.split(r'##', markdown_data)

    # Iterate over each section
    for section in sections:
        # Extract the section name (deck name)
        section_lines = section.strip().splitlines()
        if not section_lines:
            continue
        
        deck_name = section_lines[0].strip()

        # Extract the table data within the section
        table_data = re.search(r'\|.*\|.*\|\n([\s\S]*?)\n\n', section)

        if not table_data:
            continue

        # Convert the table to CSV format
        csv_data = list(csv.reader(table_data.group(1).strip().split('\n')))

        # Create an empty list to hold all the notes
        all_notes = []

        # Iterate over each line of the CSV data
        for row in csv_data:
            # Skip the header row
            if row[0] == "Accro":
                continue

            # Extract the fields from the CSV row
            accro = row[0].strip()
            description = row[1].strip() if len(row) > 1 else ""

            # Create an Anki Model
            model_id = hash(accro)
            model_name = f"Model_{deck_name}"
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

# Call the function with the Markdown file path
create_anki_decks("your_markdown_file.md")