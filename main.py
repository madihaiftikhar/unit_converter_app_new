import json
import streamlit as st
import uuid

class BookCollection:
    def __init__(self):
        self.book_list = []
        self.storage_file = "book_data.json"
        self.read_from_file()

    def read_from_file(self):
        try:
            with open(self.storage_file, "r") as file:
                self.book_list = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.book_list = []

    def save_to_file(self):
        with open(self.storage_file, "w") as file:
            json.dump(self.book_list, file, indent=4)

    def create_new_book(self):
        book_title = st.text_input("Enter book title")
        book_author = st.text_input("Enter author:")
        publication_year = st.text_input("Enter publication year:")
        book_genre = st.text_input("Enter genre:")
        is_book_read = st.checkbox("Have you read this book?")
        if st.button("Add Book"):
            if not book_title or not book_author or not publication_year:
                st.warning("Please fill in all required fields.")
                return

            new_book = {
                "title": book_title,
                "author": book_author,
                "year": publication_year,
                "genre": book_genre,
                "read": is_book_read,
            }

            self.book_list.append(new_book)
            self.save_to_file()
            st.success("Book added successfully!")

    def delete_book(self):
        book_title = st.text_input("Enter the title of the book to remove:")
        if st.button("Remove Book"):
            for book in self.book_list:
                if book["title"].lower() == book_title.lower():
                    self.book_list.remove(book)
                    self.save_to_file()
                    st.success("Book removed successfully!")
                    return
            st.error("Book not found!")

    def find_book(self):
        search_type = st.radio("Search by:", ["Title", "Author"])
        search_text = st.text_input("Enter search term:").lower()
        if search_text:
            found_books = [
                book for book in self.book_list
                if search_text in book["title"].lower() or search_text in book["author"].lower()
            ]
            if found_books:
                st.subheader("Matching Books:")
                for index, book in enumerate(found_books, 1):
                    status = "Read" if book["read"] else "Unread"
                    st.write(f"{index}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")
            else:
                st.warning("No matching books found.")

    def update_book(self):
        if not self.book_list:
            st.warning("No books available to update.")
            return

        book_title = st.selectbox("Select a book to edit:", [book["title"] for book in self.book_list])
        for book in self.book_list:
            if book["title"].lower() == book_title.lower():
                st.write("Leave blank to keep existing values.")
                book["title"] = st.text_input("New title:", value=book["title"]) or book["title"]
                book["author"] = st.text_input("New author:", value=book["author"]) or book["author"]
                book["year"] = st.text_input("New year:", value=book["year"]) or book["year"]
                book["genre"] = st.text_input("New genre:", value=book["genre"]) or book["genre"]
                read_input = st.radio("Have you read this book?", ["Yes", "No"])
                book["read"] = (read_input == "Yes")
                if st.button("Save Changes"):
                    self.save_to_file()
                    st.success("Book updated successfully!")
                return

    def show_all_books(self):
        if not self.book_list:
            st.info("Your collection is empty.")
            return
        st.subheader("Your Book Collection:")
        for index, book in enumerate(self.book_list, 1):
            status = "Read" if book["read"] else "Unread"
            st.write(f"{index}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")

    def show_reading_progress(self):
        total_books = len(self.book_list)
        read_books = sum(1 for book in self.book_list if book["read"])
        completion = (read_books / total_books) * 100 if total_books else 0
        st.metric("Total books", total_books)
        st.metric("Reading progress", f"{completion:.2f}%")

    def start_application(self):
        if "run_id" not in st.session_state:
            st.session_state["run_id"] = str(uuid.uuid4())

        st.title("📚 Welcome to Your Book Collection Manager!")
        option = st.sidebar.selectbox("Choose an option:", [
            "Add a new book",
            "Remove a book",
            "Search for books",
            "Update book details",
            "View all books",
            "View reading progress"
        ])

        if option == "Add a new book":
            self.create_new_book()
        elif option == "Remove a book":
            self.delete_book()
        elif option == "Search for books":
            self.find_book()
        elif option == "Update book details":
            self.update_book()
        elif option == "View all books":
            self.show_all_books()
        elif option == "View reading progress":
            self.show_reading_progress()


if __name__ == "__main__":
    book_manager = BookCollection()
    book_manager.start_application()
