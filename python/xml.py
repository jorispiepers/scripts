import xml.etree.ElementTree as ET

def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Iterate through each book element
    for book in root.findall("book"):
        book_id = book.get("id")
        title = book.find("title")
        author = book.find("author")
        year = book.find("year")

        print(f"Book ID: {book_id}")
        print("Title: {}".format(title.text))
        print("Author: {}".format(author.text))
        print("Year: {}".format(year))
        print("-" * 20)

if __name__ == "__main__":
    parse_xml(".\example.xml")