"""
main.py — AI Email Generator (Command-Line Interface)
======================================================
AI Engineer Ready | Cohort 1 | Assignment 1 | Option 3

This script is the command-line version of your email generator.

INSTRUCTIONS FOR STUDENTS:
---------------------------
Step 1: Complete the notebook (AI_Email_Generator.ipynb) first.
Step 2: Copy your working `generate_email()` implementation from the
        notebook into this file (replace the TODO placeholder below).
Step 3: Add the required imports at the top of this file.
Step 4: Test from terminal using the examples at the bottom of this file.

Usage:
    python main.py --context "Your email context here" --tone formal
    python main.py --context "Your email context here" --tone informal
    python main.py --context "Your email context here" --tone neutral

Example:
    python main.py --context "Schedule a meeting about Q3 results" --tone formal
"""

import argparse
import os

# TODO: Add your LangChain imports here after completing the notebook
# from langchain.prompts import PromptTemplate
# from langchain_openai import ChatOpenAI


# ==============================================================
# CORE FUNCTION — implement this after completing the notebook
# ==============================================================

def generate_email(context: str, tone: str = "neutral") -> str:
    """
    Generates a complete, AI-written email using LangChain + OpenAI.

    Args:
        context (str): A short description of what the email should be about.
                       Example: "Schedule a project kickoff meeting for next Monday"
        tone    (str): The writing style for the email.
                       Must be one of: 'formal', 'informal', 'neutral'
                       - 'formal'   → Professional language, structured, suitable for business
                       - 'informal' → Casual, friendly, conversational
                       - 'neutral'  → Balanced, clear, neither stiff nor too casual

    Returns:
        str: A complete email string containing:
             - Subject line
             - Greeting
             - Body (2–3 paragraphs)
             - Sign-off

    Raises:
        ValueError: If OPENAI_API_KEY is not set in the environment.

    Example:
        >>> email = generate_email("Schedule a team lunch", "informal")
        >>> print(email)
        Subject: Let's Do Team Lunch! ...
    """
    # TODO: Replace this placeholder with your implementation from the notebook.
    #
    # Your implementation should:
    #   1. Create a PromptTemplate with input_variables=["context", "tone"]
    #   2. Initialise ChatOpenAI (model="gpt-3.5-turbo", temperature=0.7)
    #   3. Build a chain: chain = prompt | llm
    #   4. Invoke: result = chain.invoke({"context": context, "tone": tone})
    #   5. Return: result.content
    #
    # Refer to Step 4 in AI_Email_Generator.ipynb for the full skeleton.

    return (
        f"[{tone.title()} Email — PLACEHOLDER]\n"
        f"Subject: {context}\n\n"
        f"Dear Recipient,\n\n"
        f"(This is a placeholder. Implement generate_email() using LangChain.)\n\n"
        f"Best regards,\n"
        f"[Your Name]"
    )


# ==============================================================
# CLI ENTRY POINT — do not modify this section
# ==============================================================

def main():
    parser = argparse.ArgumentParser(
        description="AI Email Generator — generates emails using LangChain + OpenAI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --context "Invite team to Friday standup" --tone formal
  python main.py --context "Ask a friend for a favour" --tone informal
  python main.py --context "Notify team of deadline change" --tone neutral
        """
    )
    parser.add_argument(
        "--context",
        required=True,
        help="What the email should be about (e.g. 'Schedule a project kickoff')"
    )
    parser.add_argument(
        "--tone",
        default="neutral",
        choices=["formal", "informal", "neutral"],
        help="Writing tone: formal | informal | neutral (default: neutral)"
    )
    args = parser.parse_args()

    # Check API key is available before calling the LLM
    if not os.environ.get("OPENAI_API_KEY"):
        print(
            "\n❌ Error: OPENAI_API_KEY environment variable is not set.\n"
            "\nSet it first:\n"
            "  Mac/Linux:  export OPENAI_API_KEY='sk-your-key-here'\n"
            "  Windows:    set OPENAI_API_KEY=sk-your-key-here\n"
        )
        raise SystemExit(1)

    print(f"\n⏳ Generating a {args.tone} email...\n")
    print("=" * 60)

    email = generate_email(args.context, args.tone)
    print(email)

    print("=" * 60)
    print("\n✅ Done!")


if __name__ == "__main__":
    main()
