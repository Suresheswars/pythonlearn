"""Student version of the Week 1 terminal demo.

Run this file from the terminal with:
    python python_terminal_demo_student.py

Suggested exercise:
- Replace the placeholder values with your own data.
- Read the printed output and predict what will happen before running it.
"""


def greet(name: str) -> str:
    """Return a friendly greeting.

    Student task: change the message to sound more like you.
    """
    return f"Hello, {name}! Welcome to Week 1 Session"


def grade(score: int) -> str:
    """Convert a score into a letter grade.

    Student task: adjust the grade boundaries if your course uses a different scale.
    """
    if score >= 90:
        return "A"
    if score >= 75:
        return "B"
    if score >= 60:
        return "C"
    if score >= 40:
        return "D"
    return "F"


def main() -> None:
    print("=== Python Terminal Demo: Student Version ===")

    # TODO: Replace these placeholder values with your own details.
    name = "Your Name Here"
    age = 21
    skills = ["Python", "Git", "GitHub"]

    # Print basic information.
    print(greet(name))
    print(f"Age: {age}")
    print(f"Skills: {skills}")

    # List indexing example.
    # TODO: Change the index and observe what happens.
    print(f"First skill: {skills[0]}")
    print(f"Total skills: {len(skills)}")

    # Loop example.
    print("\nLoop demo:")
    for index, skill in enumerate(skills, start=1):
        print(f"{index}. {skill}")

    # Function example.
    print("\nFunction demo:")
    sample_scores = [95, 82, 67, 45, 20]
    for score in sample_scores:
        print(f"Score {score} -> Grade {grade(score)}")

    # Student practice section.
    print("\nStudent practice:")
    print("1. Change name, age, and skills.")
    print("2. Add one more skill to the list.")
    print("3. Update sample_scores and re-run the script.")
    print("4. Try changing the greeting text inside greet().")

    print("\nDone running python_terminal_demo_student.py")


if __name__ == "__main__":
    main()
