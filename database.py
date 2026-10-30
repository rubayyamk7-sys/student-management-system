import sqlite3

def create_table():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            roll_no INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            course TEXT,
            marks REAL
        )
    """)

    conn.commit()
    conn.close()


def add_student():
    try:
        roll_no = int(input("Enter roll number: "))
        name = input("Enter student name: ")
        age = int(input("Enter age: "))

        if age <= 0:
            print("Age must be greater than 0")
            return

        course = input("Enter course: ")
        marks = float(input("Enter marks: "))

        if marks < 0 or marks > 100:
            print("Marks must be between 0 and 100")
            return

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO students (roll_no, name, age, course, marks)
            VALUES (?, ?, ?, ?, ?)
        """, (roll_no, name, age, course, marks))

        conn.commit()
        print("Student added successfully")

    except ValueError:
        print("Please enter valid numbers for roll number, age and marks")

    except sqlite3.IntegrityError:
        print("This roll number already exists")

    finally:
        if 'conn' in locals():
            conn.close()

def view_student():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()

    if len(students) == 0:
        print("No student found")
    else:
        for student in students:
            print(student)

def search_student():
    roll_no = int(input("Enter roll number to search: "))

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE roll_no = ?",
        (roll_no,)
    )

    student = cursor.fetchone()

    conn.close()

    if student:
        print("Student found:")
        print(student)
    else:
        print("Student not found")



def update_student():
    roll_no = int(input("Enter student roll number: "))

    print("What do you want to update?")
    print("1. Name")
    print("2. Age")
    print("3. Course")
    print("4. Marks")

    choice = input("Enter your choice: ")

    if choice == "1":
        column = "name"
        value = input("Enter new name: ")

    elif choice == "2":
        column = "age"
        value = int(input("Enter new age: "))

    elif choice == "3":
        column = "course"
        value = input("Enter new course: ")

    elif choice == "4":
        column = "marks"
        value = float(input("Enter new marks: "))

    else:
        print("Invalid choice")
        return

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        f"UPDATE students SET {column} = ? WHERE roll_no = ?",
        (value, roll_no)
    )

    conn.commit()

    if cursor.rowcount > 0:
        print("Student details updated successfully")
    else:
        print("Student not found")

    conn.close()


def delete_student():
    roll_no = int(input("Enter roll number to delete: "))

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE roll_no = ?",
        (roll_no,)
    )

    conn.commit()

    if cursor.rowcount > 0:
        print("Student deleted successfully")
    else:
        print("Student not found")

    conn.close()
