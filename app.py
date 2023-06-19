import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database Setup
engine = create_engine("sqlite:///library.db")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


# Student Model
class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    index_no = Column(String)
    name = Column(String)


# Book Model
class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    serial_number = Column(String)


# BorrowedBook Model
class BorrowedBook(Base):
    __tablename__ = "borrowed_books"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer)
    book_id = Column(Integer)
    borrow_date = Column(Date)
    return_date = Column(Date)


Base.metadata.create_all(engine)


# Student Management
def add_student(name, index_no):
    student = Student(name=name, index_no=index_no)
    session.add(student)
    session.commit()


def update_student(student_id, name):
    student = session.query(Student).get(student_id)
    student.name = name
    session.commit()


def get_all_students():
    return session.query(Student).all()


# Book Management
def add_book(name, serial_number):
    book = Book(name=name, serial_number=serial_number)
    session.add(book)
    session.commit()


def update_book(book_id, name, serial_number):
    book = session.query(Book).get(book_id)
    book.name = name
    book.serial_number = serial_number
    session.commit()


def get_all_books():
    return session.query(Book).all()


# Borrowing Management
def borrow_book(student_id, book_id, borrow_date, return_date):
    borrowed_book = BorrowedBook(
        student_id=student_id,
        book_id=book_id,
        borrow_date=borrow_date,
        return_date=return_date,
    )
    session.add(borrowed_book)
    session.commit()


def get_all_borrowed_books():
    return session.query(BorrowedBook).all()


# Return Management
def return_book(borrowed_book_id, return_date):
    borrowed_book = session.query(BorrowedBook).get(borrowed_book_id)
    borrowed_book.return_date = return_date
    session.commit()


# Streamlit App
def main():
    st.title("NJA Library Management App")

    # Sidebar navigation
    selected_page = st.sidebar.radio(
        "Navigation",
        ("Add Student", "Add Book", "Borrow Book", 
         "Return Book", "View Borrowed Books", 
        'Available Books', 'All Students'),
    )

    if selected_page == "Add Student":
        st.header("Add Student")
        student_name = st.text_input("Student Name")
        student_index = st.text_input('Student Index Number')
        if st.button("Add Student"):
            add_student(student_name, student_index)
            st.success("Student added successfully!")

    elif selected_page == "Add Book":
        st.header("Add Book")
        book_name = st.text_input("Book Name")
        book_serial_number = st.text_input("Book Serial Number")
        if st.button("Add Book"):
            add_book(book_name, book_serial_number)
            st.success("Book added successfully!")

    elif selected_page == "Borrow Book":
        st.header("Borrow Book")
        students = get_all_students()
        student_names = [student.name for student in students]
        student_name = st.selectbox("Select Student", student_names)

        books = get_all_books()
        book_names = [book.name for book in books]
        book_name = st.selectbox("Select Book", book_names)

        borrow_date = st.date_input("Borrow Date")
        return_date = st.date_input("Expected Return Date")
        if st.button("Borrow Book"):
            student_id = students[student_names.index(student_name)].id
            book_id = books[book_names.index(book_name)].id
            borrow_book(student_id, book_id, borrow_date, return_date)
            st.success("Book borrowed successfully!")

    elif selected_page == "Return Book":
        st.header("Return Book")
        borrowed_books = get_all_borrowed_books()
        borrowed_book_ids = [borrowed_book.student_id for borrowed_book in borrowed_books]
        borrowed_book_id = st.selectbox("Select Borrowed Book", borrowed_book_ids)
        return_date = st.date_input("Return Date")
        if st.button("Return Book"):
            return_book(borrowed_book_id, return_date)
            st.success("Book returned successfully!")

    elif selected_page == "View Borrowed Books":
        st.header("Borrowed Books")
        borrowed_books = get_all_borrowed_books()
        col1, col2, col3, col4= st.columns(4)
        with col1:

            st.markdown("#### Student Name")
        with col2:
            st.markdown("#### Book Name")
        with col3:
            st.markdown("#### Borrow Date")
        with col4:
            st.markdown("#### Return Date")
        
        for borrowed_book in borrowed_books:
            student = session.query(Student).get(borrowed_book.student_id)
            book = session.query(Book).get(borrowed_book.book_id)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.write(student.name)
            with col2:
                st.write(book.name)
            with col3:
                st.write(borrowed_book.borrow_date)
            with col4:
                st.write(borrowed_book.return_date)
            
            st.write("---")
            
            
    elif selected_page == 'All Students':
        # Display all students
        st.subheader("Registered Students")
        all_students = get_all_students()
        for student in all_students:
            col1, col2 = st.columns(2)
            with col1:
                st.write("Student ID:", student.id)
            with col2:
                st.write("Student Name:", student.name)
            st.write("---")

        # Display all books
    elif selected_page == 'Available Books':
        st.subheader("Available Books")
        all_books = get_all_books()
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Book's Name")
        with col2:
            st.markdown("#### Book's Number")
        for book in all_books:
            col1, col2 = st.columns(2)
            with col1:
                st.write(book.name)
            with col2:
                st.write(book.serial_number)
            st.write("---")


if __name__ == "__main__":
    main()
