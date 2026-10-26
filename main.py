
import json
from ai_assistant import ask_ai

FILE_NAME = "attendance.json"


def load_data():
    with open(FILE_NAME, "r") as file:
        return json.load(file)


def save_data(data):
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)


def mark_attendance(roll_no, date, status):
    data = load_data()

    for student in data["students"]:
        if student["roll_no"] == roll_no:
            if date in student["attendance"]:
                print("Attendance already exists for this date!")
                return

            if status not in ["Present", "Absent"]:
                print("Invalid status! Use Present or Absent.")
                return

            student["attendance"][date] = status
            student["total_days"] = len(student["attendance"])
            save_data(data)
            print("Attendance marked successfully!")
            return

    print("Student not found!")


def remove_attendance(roll_no, date):
    data = load_data()

    for student in data["students"]:
        if student["roll_no"] == roll_no:
            if date not in student["attendance"]:
                print("No attendance record exists for this date!")
                return

            del student["attendance"][date]
            student["total_days"] = len(student["attendance"])
            save_data(data)
            print("Attendance removed successfully!")
            return

    print("Student not found!")


def calculate_attendance(roll_no):
    data = load_data()

    for student in data["students"]:
        if student["roll_no"] == roll_no:
            records = student["attendance"]
            total_days = len(records)
            present_days = sum(
                1 for status in records.values()
                if status == "Present"
            )
            percentage = (
                present_days / total_days * 100
                if total_days else 0
            )

            print("Student:", student["name"])
            print("Total Days:", total_days)
            print("Present Days:", present_days)
            print("Attendance:", round(percentage, 2), "%")
            return

    print("Student not found!")


def main():
    while True:
        print("\n===== AI Attendance Management System =====")
        print("1. Mark Attendance")
        print("2. Remove Attendance")
        print("3. Calculate Attendance")
        print("4. Ask AI Assistant")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        try:
            if choice == "1":
                roll_no = input("Enter student roll number: ")
                date = input("Enter date (YYYY-MM-DD): ")
                status = input("Enter status (Present/Absent): ")
                mark_attendance(roll_no, date, status)

            elif choice == "2":
                roll_no = input("Enter student roll number: ")
                date = input("Enter date (YYYY-MM-DD): ")
                remove_attendance(roll_no, date)

            elif choice == "3":
                roll_no = input("Enter student roll number: ")
                calculate_attendance(roll_no)

            elif choice == "4":
                question = input("Ask your attendance question: ")
                print("AI:", ask_ai(question))

            elif choice == "5":
                print("Goodbye!")
                break

            else:
                print("Invalid choice. Please select 1-5.")

        except FileNotFoundError:
            print("Error: attendance.json was not found.")
        except json.JSONDecodeError:
            print("Error: attendance.json contains invalid JSON.")
        except Exception as error:
            print("Something went wrong:", error)


if __name__ == "__main__":
    main()
