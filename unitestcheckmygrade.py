import unittest
import time
from checkmygrade import Student, Course, Professor, load_csv, write_csv


class TestStudentManagement(unittest.TestCase):

    def setUp(self):
        """test data with 1000 student records"""
        self.students = [
            Student(str(i), f"Student{i}", f"Test{i}", f"student{i}@yahoo.com", "DATA200", "A", str(90 + (i % 10)))
            for i in range(1000)
        ]
        write_csv("students.csv", [s.__dict__ for s in self.students], 
                  ["student_id", "first_name", "last_name", "email", "course_id", "grade", "marks"])

    def test_add_student(self):
        """Test adding a new student"""
        student = Student("1001", "New", "Student", "newstudent@yahoo.com", "DATA300", "B", "85")
        student.add_new_student()
        students = load_csv("students.csv")
        self.assertTrue(any(s['email'] == "newstudent@yahoo.com" for s in students))

    def test_delete_student(self):
        """Test deleting a student"""
        student = Student("7", "", "", "student7@yahoo.com", "", "", "")
        student.delete_new_student()
        students = load_csv("students.csv")
        self.assertFalse(any(s['email'] == "student7@yahoo.com" for s in students))

    def test_update_student_record(self):
        """Test modifying a student's grade"""
        student = Student("10", "", "", "", "", "", "")
        student.update_student_record(new_grade="C")
        students = load_csv("students.csv")
        updated_student = next(s for s in students if s['student_id'] == "10")
        self.assertEqual(updated_student['grade'], "C")

class TestStudentSearch(unittest.TestCase):

    def test_search_student(self):
        """Test searching for a student and measure search time"""
        students = load_csv("students.csv") 
        email_to_search = "student500@yahoo.com"

        start_time = time.time()
        student = next((s for s in students if s['email'] == email_to_search), None)
        end_time = time.time()

        self.assertIsNotNone(student, "Student not found!")
        print(f"Search for {email_to_search} took {end_time - start_time:.6f} seconds")

class TestStudentSorting(unittest.TestCase):

    def test_sort_students_by_marks(self):
        start_time = time.time()
        Student.display_sorted(by="marks")
        end_time = time.time()
        print(f"Sorting by marks has taken: {end_time - start_time:.6f} seconds")

    def test_sort_students_by_email(self):
        start_time = time.time()
        Student.display_sorted(by="email")
        end_time = time.time()

        print(f"Sorting by email has taken: {end_time - start_time:.6f} seconds")


class TestCourseManagement(unittest.TestCase):

    def test_add_course(self):
        course = Course("DATA228", "Big Data", "4", "Big Data Technologies")
        course.add_new_course()
        courses = load_csv("courses.csv")
        self.assertTrue(any(c['course_id'] == "DATA400" for c in courses))

    def test_delete_course(self):
        course = Course("DATA200", "", "", "")
        course.delete_new_course()
        courses = load_csv("courses.csv")
        self.assertFalse(any(c['course_id'] == "DATA200" for c in courses))

    def test_modify_course(self):
        courses = load_csv("courses.csv")
        for course in courses:
            if course["course_id"] == "DATA300":
                course["description"] = "Advanced Python"
        write_csv("courses.csv", courses, ["course_id", "course_name", "credits", "description"])

        updated_courses = load_csv("courses.csv")
        modified_course = next(c for c in updated_courses if c["course_id"] == "DATA300")
        self.assertEqual(modified_course["description"], "Advanced Python")

class TestProfessorManagement(unittest.TestCase):

    def test_add_professor(self):
        """Test adding a new professor"""
        professor = Professor("P100", "Dr. Chan", "chan@edu.com", "Senior", "DATA500")
        professor.add_new_professor()
        professors = load_csv("professors.csv")
        self.assertTrue(any(p['email'] == "chan@edu.com" for p in professors))

    def test_delete_professor(self):
        """Test deleting a professor"""
        professor = Professor("P200", "", "professor200@edu.com", "", "")
        professor.delete_professor()
        professors = load_csv("professors.csv")
        self.assertFalse(any(p['email'] == "professor200@edu.com" for p in professors))

    def test_modify_professor_details(self):
        """Test modifying a professor's rank"""
        professor = Professor("P100", "", "", "", "")
        professor.modify_professor_details(new_rank="Professor Chan")

        professors = load_csv("professors.csv")
        modified_professor = next(p for p in professors if p["professor_id"] == "P100")
        self.assertEqual(modified_professor["rank"], "Professor Chan")

if __name__ == "__main__":
    unittest.main()