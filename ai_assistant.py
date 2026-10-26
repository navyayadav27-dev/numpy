
import json
import ollama

MODEL_NAME = "qwen2.5:3b"
ATTENDANCE_FILE = "attendance.json"


def load_attendance():
    with open(ATTENDANCE_FILE, "r") as file:
        return json.load(file)


def get_attendance_percentage(student):
    records = student["attendance"]
    total_days = len(records)

    if total_days == 0:
        return 0.0

    present_days = sum(
        1 for status in records.values()
        if status == "Present"
    )

    return round(present_days / total_days * 100, 2)


def ask_ai(message):
    data = load_attendance()
    question = message.lower()

    # Calculate attendance percentages reliably in Python.
    if "percentage" in question or "how much attendance" in question:
        for student in data["students"]:
            if student["name"].lower() in question:
                percentage = get_attendance_percentage(student)
                return (
                    f"{student['name']}'s attendance is "
                    f"{percentage}%."
                )

    attendance_text = json.dumps(data, indent=2)

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an attendance assistant. Answer "
                    "questions using only the supplied attendance "
                    "records. Never invent records or claim that "
                    "attendance was changed. Do not guess missing "
                    "information.\n\n"
                    f"Attendance records:\n{attendance_text}"
                ),
            },
            {"role": "user", "content": message},
        ],
    )

    return response["message"]["content"]


if __name__ == "__main__":
    print("===== AI Attendance Assistant =====")
    question = input("Ask a question about attendance: ")

    try:
        print("\nAI:", ask_ai(question))
    except FileNotFoundError:
        print("Error: attendance.json was not found.")
    except json.JSONDecodeError:
        print("Error: attendance.json contains invalid JSON.")
    except Exception as error:
        print("Something went wrong:", error)
