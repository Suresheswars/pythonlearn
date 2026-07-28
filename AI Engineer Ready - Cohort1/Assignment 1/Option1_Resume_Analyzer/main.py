import argparse
import json
import sys


def extract_skills(text: str):
    # TODO: replace this placeholder with LLM + PromptTemplate logic
    return ["Python", "Data Analysis"]


def identify_missing_skills(skills: list):
    # TODO: define target skills for the job/role and compare
    target = ["Python", "Data Analysis", "Machine Learning", "SQL"]
    return [s for s in target if s not in skills]


def suggest_improvements(missing: list):
    # TODO: use LLM to craft human-friendly suggestions
    return [f"Learn {m}" for m in missing]


def build_output(skills, missing, suggestions):
    return {
        "skills": skills,
        "missing_skills": missing,
        "suggestions": suggestions,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Path to resume text file")
    parser.add_argument("--text", help="Resume text string")
    args = parser.parse_args()

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    elif args.text:
        text = args.text
    else:
        print("Provide --file or --text", file=sys.stderr)
        sys.exit(1)

    skills = extract_skills(text)
    missing = identify_missing_skills(skills)
    suggestions = suggest_improvements(missing)

    print(json.dumps(build_output(skills, missing, suggestions), indent=2))


if __name__ == "__main__":
    main()
