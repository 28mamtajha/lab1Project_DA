import csv
import hashlib
import time
import statistics

def encrypt_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def decrypt_password(encrypted, original):
    return encrypt_password(original) == encrypted

def load_csv(file_name):
    """Loads CSV file data into a list of dictionaries"""
    try:
        with open(file_name, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            return [{k.strip().lower(): v for k, v in row.items()} for row in reader]
    except FileNotFoundError:
        return []

def write_csv(file_name, data, fieldnames):
    """Writes data into CSV file """
    normalized_data = [{k.strip().lower(): v for k, v in row.items()} for row in data]

    with open(file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=[f.lower() for f in fieldnames])
        writer.writeheader()
        writer.writerows(normalized_data)

# =================== Student Class ===================

class Student:
    def __init__(self, student_id, first_name, last_name, email, course_id, grade, marks):
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.course_id = course_id
        self.grade = grade
        self.marks = marks

    def add_new_student(self):
        """Add a new student to the system"""
        students = load_csv('students.csv')

        for s in students:
            if s['student_id'] == self.student_id:
                print("Student ID already exists!")
                return

        students.append(self.__dict__)
        write_csv('students.csv', students, ['student_id', 'first_name', 'last_name', 'email', 'course_id', 'grade', 'marks'])
        print("Student Added Successfully!")

    def delete_new_student(self):
        """Delete a student by email"""
        students = load_csv('students.csv')
        students = [s for s in students if s['email'] != self.email]
        write_csv('students.csv', students, ['student_id', 'first_name', 'last_name', 'email', 'course_id', 'grade', 'marks'])
        print(f"Student {self.email} deleted successfully!")

    def update_student_record(self, new_first_name=None, new_last_name=None, new_course_id=None, new_grade=None, new_marks=None):
        """Modify an existing student record"""
        students = load_csv('students.csv')
        student_found = False

        for s in students:
            if s['student_id'] == self.student_id:
                if new_first_name:
                    s['first_name'] = new_first_name
                if new_last_name:
                    s['last_name'] = new_last_name
                if new_course_id:
                    s['course_id'] = new_course_id
                if new_grade:
                    s['grade'] = new_grade
                if new_marks:
                    s['marks'] = new_marks
                student_found = True
                break

        if student_found:
            write_csv('students.csv', students, ['student_id', 'first_name', 'last_name', 'email', 'course_id', 'grade', 'marks'])
            print("Student record updated successfully!")
        else:
            print("Student not found!")

    def check_my_grades(self):
        """Retrieve student's grade"""
        print(f"Student {self.first_name} {self.last_name} has a grade of {self.grade}.")

    def check_my_marks(self):
        """Retrieve student's marks"""
        print(f"Student {self.first_name} {self.last_name} has {self.marks} marks.")

    @classmethod
    def display_records(cls):
        """Display all student records"""
        students = load_csv('students.csv')
        if not students:
            print("No students found!")
        else:
            print("\n===== Student Records =====")
            for s in students:
                print(f"ID: {s['student_id']} | Name: {s['first_name']} {s['last_name']} | Email: {s['email']} | Course: {s['course_id']} | Grade: {s['grade']} | Marks: {s['marks']}")

    @classmethod
    def search(cls, email):
        """Search for a student by email"""
        students = load_csv('students.csv')
        for s in students:
            if s['email'] == email:
                return Student(s['student_id'], s['first_name'], s['last_name'], s['email'], s['course_id'], s['grade'], s['marks'])
        return None

    @classmethod
    def display_sorted(cls, by="marks"):
        """Display students sorted by marks or email"""
        students = load_csv('students.csv')

        if by not in ["marks", "email"]:
            print("Invalid sorting key! Choose 'marks' or 'email'.")
            return

        students = sorted(students, key=lambda x: x[by])

        print("\n===== Sorted Student Records =====")
        for s in students:
            print(f"ID: {s['student_id']} | Name: {s['first_name']} {s['last_name']} | Email: {s['email']} | Marks: {s['marks']} | Grade: {s['grade']}")

   
# =================== Course Class ===================

class Course:
    def __init__(self, course_id, course_name, credits, description):
        self.course_id = course_id
        self.course_name = course_name
        self.credits = credits
        self.description = description

    def add_new_course(self):
        """Add a new course to the system"""
        courses = load_csv('courses.csv')

        for c in courses:
            if c['course_id'] == self.course_id:
                print("Course ID already exists!")
                return

        courses.append(self.__dict__)
        write_csv('courses.csv', courses, ['course_id', 'course_name', 'credits', 'description'])
        print("Course Added Successfully!")

    def delete_new_course(self):
        """Delete a course by course ID"""
        courses = load_csv('courses.csv')
        courses = [c for c in courses if c['course_id'] != self.course_id]
        write_csv('courses.csv', courses, ['course_id', 'course_name', 'credits', 'description'])
        print(f"Course {self.course_id} deleted successfully!")
    
    def get_students(self):
        """Retrieve all students in this course"""
        students = load_csv('students.csv')
        return [s for s in students if s['course_id'] == self.course_id]
    
    def get_median_score(self):
        """Calculate and return the median marks of students in this course"""
        students = self.get_students()
        if not students:
            print("No students enrolled in this course.")
            return 0

        all_marks = [float(s['marks']) for s in students if s['marks'].isdigit()]
        return statistics.median(all_marks) if all_marks else 0
    
    @classmethod
    def display_courses(cls):
        """Display all available courses"""
        courses = load_csv('courses.csv')
        if not courses:
            print("No courses found!")
        else:
            print("\n===== Course List =====")
            for c in courses:
                print(f"Course ID: {c.get('course_id', 'N/A')} | Name: {c.get('course_name', 'N/A')} | Credits: {c.get('credits', 'N/A')} | Description: {c.get('description', 'N/A')}")
# =================== Professor Class ===================

class Professor:
    def __init__(self, professor_id, name, email, rank, course_id):
        self.professor_id = professor_id
        self.name = name
        self.email = email.lower()
        self.rank = rank
        self.course_id = course_id.upper()

    def add_new_professor(self):
        """Add a new professor to the system"""
        professors = load_csv('professors.csv')

        # Ensure professor ID is unique
        for prof in professors:
            if prof['professor_id'] == self.professor_id:
                print("Professor ID already exists!")
                return

        professors.append(self.__dict__)
        write_csv('professors.csv', professors, ['professor_id', 'name', 'email', 'rank', 'course_id'])
        print("Professor Added Successfully!")

    def delete_professor(self):
        """Delete a professor by email"""
        professors = load_csv('professors.csv')
        professors = [p for p in professors if p['email'] != self.email]
        write_csv('professors.csv', professors, ['professor_id', 'name', 'email', 'rank', 'course_id'])
        print(f"Professor {self.email} deleted successfully!")

    def modify_professor_details(self, new_name=None, new_rank=None, new_course_id=None):
        """Modify an existing professor's details"""
        professors = load_csv('professors.csv')
        professor_found = False

        for prof in professors:
            if prof['professor_id'] == self.professor_id:
                if new_name:
                    prof['name'] = new_name
                if new_rank:
                    prof['rank'] = new_rank
                if new_course_id:
                    prof['course_id'] = new_course_id
                professor_found = True
                break

        if professor_found:
            write_csv('professors.csv', professors, ['professor_id', 'name', 'email', 'rank', 'course_id'])
            print("Professor details updated successfully!")
        else:
            print("Professor not found!")

    @classmethod
    def professors_details(cls):
        """Display all professors' details"""
        professors = load_csv('professors.csv')
        if not professors:
            print("No professors found!")
        else:
            print("\n===== Professors Details =====")
            for prof in professors:
                print(f"ID: {prof['professor_id']} | Name: {prof['name']} | Email: {prof['email']} | Rank: {prof['rank']} | Course: {prof['course_id']}")

    @classmethod
    def show_course_details_by_professor(cls, email):
        """Show course details for a given professor"""
        professors = load_csv('professors.csv')
        courses = load_csv('courses.csv')

        professor = next((p for p in professors if p['email'] == email.lower()), None)
        if not professor:
            print("Professor not found!")
            return

        course = next((c for c in courses if c['course_id'] == professor['course_id']), None)
        if course:
            print(f"\nProfessor {professor['name']} teaches:\nCourse ID: {course['course_id']}, Course Name: {course['course_name']}, Description: {course['description']}")
        else:
            print("Course details not found!")

# =================== Grade Class ===================
class Grade:
    def __init__(self, grade_id, grade, marks_range):
        self.grade_id = grade_id
        self.grade = grade
        self.marks_range = marks_range

    def add_grade(self):
        """Add a grade to the CSV file"""
        grades = load_csv('grades.csv')
        grades.append(self.__dict__)
        write_csv('grades.csv', grades, ['grade_id', 'grade', 'marks_range'])

    def delete_grade(self):
        """Delete a grade based on grade_id"""
        grades = load_csv('grades.csv')
        grades = [g for g in grades if g['grade_id'] != self.grade_id]
        write_csv('grades.csv', grades, ['grade_id', 'grade', 'marks_range'])

    def modify_grade(self, new_grade, new_marks_range):
        """Modify an existing grade"""
        grades = load_csv('grades.csv')
        for g in grades:
            if g['grade_id'] == self.grade_id:
                g['grade'] = new_grade
                g['marks_range'] = new_marks_range
                break
        write_csv('grades.csv', grades, ['grade_id', 'grade', 'marks_range'])

    @classmethod
    def display_grade_report(cls):
        """Display all grades in the system"""
        grades = load_csv('grades.csv')
        if not grades:
            print("No grades found!")
        else:
            print("\n===== Grade Report =====")
            for g in grades:
                print(f"Grade ID: {g['grade_id']} | Grade: {g['grade']} | Marks Range: {g['marks_range']}")


# =================== Login Class ===================

class LoginUser:
    def __init__(self, email, password, role):
        self.email = email.lower()
        self.password = encrypt_password(password)  # Store encrypted password
        self.role = role

    def register_user(self):
        """Registers a new user and stores encrypted password in CSV"""
        users = load_csv('login.csv')

        for user in users:
            if user['email'] == self.email:
                print("User already exists!")
                return

        users.append({'email': self.email, 'password': self.password, 'role': self.role})
        write_csv('login.csv', users, ['email', 'password', 'role'])
        print("User Registered Successfully!")

    def login(self):
        """Authenticate user by checking email and password"""
        users = load_csv('login.csv')
        for user in users:
            if user['email'] == self.email and decrypt_password(user['password'], self.password):
                print(f"Login Successful! Welcome, {self.email}")
                return True
        print("Invalid email or password!")
        return False

    def logout(self):
        """Simulate user logout"""
        print(f"{self.email} has logged out.")

    def change_password(self, new_password):
        """Change the password for an existing user"""
        users = load_csv('login.csv')
        user_found = False

        for user in users:
            if user['email'] == self.email:
                user['password'] = encrypt_password(new_password)
                user_found = True
                break

        if user_found:
            write_csv('login.csv', users, ['email', 'password', 'role'])
            print("Password changed successfully!")
        else:
            print("User not found!")

    @staticmethod
    def encrypt_password(password):
        """Encrypt password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def decrypt_password(encrypted_password, original_password):
        """Simulated password decryption (checking hash match)"""
        return encrypt_password(original_password) == encrypted_password

# =================== Main Function ===================

def main():
    logged_in_user = None

    while True:
        print("\n===== CheckMyGrade Application =====")
        print("1. Student Management")
        print("2. Course Management")
        print("3. Professor Management")
        print("4. Grade Management")
        print("5. User Login Management")
        print("6. Exit")
        choice = input("Enter choice: ")

        if choice == '1':  # Student Management
            print("\n--- Student Management ---")
            print("1. Add New Student")
            print("2. Delete Student")
            print("3. Update Student Record")
            print("4. Display All Students")
            print("5. Search Student by Email")
            print("6. Sort Students by Marks or Email")
            print("7. Check Student Grades")
            print("8. Check Student Marks")
            student_choice = input("Enter choice: ")
            
            #add new student
            if student_choice == '1':
                student = Student(
                    input("Student ID: "),
                    input("First Name: "),
                    input("Last Name: "),
                    input("Email: "),
                    input("Course ID: "),
                    input("Grade: "),
                    input("Marks: ")
                )
                student.add_new_student()

            elif student_choice == '2':  #delete student
                email = input("Enter Student Email to delete: ")
                student = Student("", "", "", email, "", "", "")
                student.delete_new_student()

            elif student_choice == '3':  #modify student details
                student_id = input("Enter Student ID to modify: ")
                new_first_name = input("Enter new first name (leave blank if no change): ")
                new_last_name = input("Enter new last name (leave blank if no change): ")
                new_course_id = input("Enter new course ID (leave blank if no change): ")
                new_grade = input("Enter new grade (leave blank if no change): ")
                new_marks = input("Enter new marks (leave blank if no change): ")
                student = Student(student_id, "", "", "", "", "", "")
                student.update_student_record(
                    new_first_name if new_first_name else None,
                    new_last_name if new_last_name else None,
                    new_course_id if new_course_id else None,
                    new_grade if new_grade else None,
                    new_marks if new_marks else None
                )

            elif student_choice == '4':  #display all students
                Student.display_records()

            elif student_choice == '5':  # Search for a student by email
                email = input("Enter Student Email to search: ")
                student = Student.search(email)
                if student:
                    print("\n===== Student Found =====")
                    print(f"ID: {student.student_id} | Name: {student.first_name} {student.last_name} | Course: {student.course_id} | Grade: {student.grade} | Marks: {student.marks}")
                else:
                    print("Student not found!")

            elif student_choice == '6':  #Sort Students by Marks or Email
                sort_by = input("Sort by (marks/email): ").strip().lower()
                if sort_by in ["marks", "email"]:
                    Student.display_sorted(by=sort_by)
                else:
                    print("Invalid sorting option! Choose 'marks' or 'email'.")

            elif student_choice == '7':  #Check Student Grades
                email = input("Enter Student Email: ")
                students = load_csv('students.csv')
                student = next((s for s in students if s['email'] == email), None)
                if student:
                    print(f"Student {student['first_name']} {student['last_name']} has a grade of {student['grade']}.")
                else:
                    print("Student not found!")

            elif student_choice == '8':  #Check Student Marks
                email = input("Enter Student Email: ")
                students = load_csv('students.csv')
                student = next((s for s in students if s['email'] == email), None)
                if student:
                    print(f"Student {student['first_name']} {student['last_name']} has {student['marks']} marks.")
                else:
                    print("Student not found!")

        elif choice == '2':  # Course Management
            print("\n--- Course Management ---")
            print("1. Add New Course")
            print("2. Delete Course")
            print("3. Display All Courses")
            print("4. Median Score for a Course")
            course_choice = input("Enter choice: ")

            if course_choice == '1':  # Add new course
                course = Course(
                    input("Course ID: "),
                    input("Course Name: "),
                    input("Credits: "),
                    input("Description: ")
                )
                course.add_new_course()

            elif course_choice == '2':  # Delete course
                course_id = input("Enter Course ID to delete: ")
                course = Course(course_id, "", "", "")
                course.delete_new_course()

            elif course_choice == '3':  # Display all courses
                Course.display_courses()

            elif course_choice == '4': 
                 course_id = input("Enter Course ID: ")
                 course = Course(course_id, "", "", "")
                 median_score = course.get_median_score()
                 print(f"Median Score for Course {course_id}: {median_score:.2f}")

            else:
               print("Invalid choice! Please enter a valid option.")

        elif choice == '3':  # Professor Management
            print("\n--- Professor Management ---")
            print("1. Add New Professor")
            print("2. Delete Professor")
            print("3. Modify Professor Details")
            print("4. View All Professors")
            print("5. Show Courses Taught by a Professor")
            prof_choice = input("Enter choice: ")

            if prof_choice == '1':  # Add new professor
                professor = Professor(
                    input("Professor ID: "),
                    input("Name: "),
                    input("Email: "),
                    input("Rank: "),
                    input("Course ID: ")
                )
                professor.add_new_professor()

            elif prof_choice == '2':  # Delete professor
                email = input("Enter Professor Email to delete: ")
                professor = Professor("", "", email, "", "")
                professor.delete_professor()

            elif prof_choice == '3':  # Modify professor details
                professor_id = input("Enter Professor ID to modify: ")
                new_name = input("Enter new name (leave blank if no change): ")
                new_rank = input("Enter new rank (leave blank if no change): ")
                new_course_id = input("Enter new course ID (leave blank if no change): ")
                professor = Professor(professor_id, "", "", "", "")
                professor.modify_professor_details(
                    new_name if new_name else None,
                    new_rank if new_rank else None,
                    new_course_id if new_course_id else None
                )

            elif prof_choice == '4':  # View all professors
                Professor.professors_details()

            elif prof_choice == '5':  # Show courses taught by a professor
                email = input("Enter Professor Email: ")
                Professor.show_course_details_by_professor(email)

            else:
                print("Invalid Choice! Please Try Again.")


        elif choice == '4':  # Grade Management
            print("\n--- Grade Management ---")
            print("1. Add Grade")
            print("2. Delete Grade")
            print("3. Modify Grade")
            print("4. Display Grade Report")
            grade_choice = input("Enter choice: ")

            if grade_choice == '1':
                grade = Grade(
                    input("Grade ID: "),
                    input("Grade: "),
                    input("Marks Range: ")
                )
                grade.add_grade()
                print("Grade Added Successfully!")

            elif grade_choice == '2':
                grade_id = input("Enter Grade ID to delete: ")
                grade = Grade(grade_id, "", "")
                grade.delete_grade()
                print("Grade Deleted!")

            elif grade_choice == '3':
                grade_id = input("Enter Grade ID to modify: ")
                new_grade = input("Enter new Grade: ")
                new_marks_range = input("Enter new Marks Range: ")
                grade = Grade(grade_id, "", "")
                grade.modify_grade(new_grade, new_marks_range)
                print("Grade is modified successfully!")

            elif grade_choice == '4':
                Grade.display_grade_report()

        elif choice == '5':  # User Login Management
            print("\n--- User Login Management ---")
            print("1. Register New User")
            print("2. Login")
            print("3. Change Password")
            print("4. Logout")
            login_choice = input("Enter choice: ")

            if login_choice == '1':  # Register New User
                user = LoginUser(
                    input("Enter Email: "),
                    input("Enter Password: "),
                    input("Enter your Role (student/professor/admin): ")
                )
                user.register_user()

            elif login_choice == '2':  # User Login
                email = input("Enter Email: ")
                password = input("Enter Password: ")
                user = LoginUser(email, password, "")
                if user.login():
                    logged_in_user = user

            elif login_choice == '3':  # Change Password
                if logged_in_user:
                    new_password = input("Enter New Password: ")
                    logged_in_user.change_password(new_password)
                else:
                    print("login in to change your password!")

            elif login_choice == '4':  # Logout
                if logged_in_user:
                    logged_in_user.logout()
                    logged_in_user = None
                else:
                    print("No user is logged in!")

        elif choice == '6':  # Exit
            print("Exiting")
            break

        else:
            print("Invalid Choice, Try Again.")

if __name__ == "__main__":
    main()
