import json
import os
from datetime import datetime

def add_book(library, filename):
    title = input("Enter book title: ").strip()
    author = input("Enter author name: ").strip()
    year = input("Enter publication year: ").strip()
    genre = input("Enter genre: ").strip()
    read_status = input("Have you read this book? (yes/no): ").strip().lower() == 'yes'

    if not title or not author:
        print("Title and author are required!")
        return library

    if not year.isdigit() or int(year) > datetime.now().year:
        print("Invalid publication year!")
        return library

    book = {
        "title": title,
        "author": author,
        "year": int(year),
        "genre": genre,
        "read": read_status
    }
    library.append(book)
    save_library(library, filename)
    print(f"Book '{title}' added successfully!")
    return library

def remove_book(library, filename):
    title = input("Enter book title to remove: ").strip()
    initial_len = len(library)
    library[:] = [book for book in library if book["title"].lower() != title.lower()]
    if len(library) < initial_len:
        save_library(library, filename)
        print(f"Book '{title}' removed successfully!")
    else:
        print(f"Book '{title}' not found!")
    return library

def search_books(library):
    query = input("Enter search term (title or author): ").strip().lower()
    results = [
        book for book in library
        if query in book["title"].lower() or query in book["author"].lower()
    ]
    if results:
        print("\nSearch Results:")
        for book in results:
            display_book(book)
    else:
        print("No books found!")

def display_book(book):
    print(f"Title: {book['title']}")
    print(f"Author: {book['author']}")
    print(f"Year: {book['year']}")
    print(f"Genre: {book['genre']}")
    print(f"Read: {'Yes' if book['read'] else 'No'}")
    print("-" * 30)

def list_all_books(library):
    if not library:
        print("Library is empty!")
        return
    print("\nAll Books:")
    for book in library:
        display_book(book)

def show_statistics(library):
    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
    genres = {}
    for book in library:
        genres[book["genre"]] = genres.get(book["genre"], 0) + 1

    print("\nLibrary Statistics:")
    print(f"Total Books: {total_books}")
    print(f"Books Read: {read_books}")
    print(f"Books Unread: {total_books - read_books}")
    if genres:
        print("\nBooks by Genre:")
        for genre, count in genres.items():
            print(f"{genre}: {count}")

def save_library(library, filename):
    try:
        with open(filename, 'w') as f:
            json.dump(library, f, indent=4)
        print("Library saved successfully!")
    except Exception as e:
        print(f"Error saving library: {e}")

def load_library(filename):
    library = []
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                library = json.load(f)
            print("Library loaded successfully!")
        except Exception as e:
            print(f"Error loading library: {e}")
    return library

def main():
    filename = "library.json"
    library = load_library(filename)
    while True:
        print("\n=== Personal Library Manager ===")
        print("1. Add a book")
        print("2. Remove a book")
        print("3. Search books")
        print("4. List all books")
        print("5. Show statistics")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            library = add_book(library, filename)
        elif choice == "2":
            library = remove_book(library, filename)
        elif choice == "3":
            search_books(library)
        elif choice == "4":
            list_all_books(library)
        elif choice == "5":
            show_statistics(library)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()