"""
Option 4 — AI Content Generator
AI Engineer Ready · Cohort 1 · Assignment 1

Problem Statement:
    Build a 3-stage LLM pipeline that takes a topic and produces:
      1. A structured blog outline   (generate_outline)
      2. Full blog content           (generate_content)
      3. A concise summary           (summarize)

    Each stage must use LangChain's PromptTemplate and make a real LLM call.

Usage:
    python main.py --topic "Getting started with LangChain"

Submission Checklist:
    [ ] All 3 functions use PromptTemplate + LLM (no hardcoded returns)
    [ ] generate_outline() returns a list
    [ ] generate_content() returns a markdown-formatted string
    [ ] summarize() returns a 3-5 sentence string
    [ ] Script runs end-to-end without errors
"""

import os
import argparse

# TODO: Import LangChain components
# from langchain.prompts import PromptTemplate
# from langchain_openai import ChatOpenAI


# ── Initialise LLM ────────────────────────────────────────────────────────────
# TODO: Create a shared LLM instance here (used by all 3 functions below)
#
#   llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)
#
# Make sure OPENAI_API_KEY is set in your environment before running:
#   Windows:  set OPENAI_API_KEY=sk-...
#   Mac/Linux: export OPENAI_API_KEY=sk-...

llm = None  # TODO: replace with ChatOpenAI(...)


# ── Stage 1: Generate Outline ─────────────────────────────────────────────────
def generate_outline(topic: str) -> list:
    """
    Generates a structured blog post outline for the given topic.

    Args:
        topic (str): The subject of the blog post (e.g. "Getting started with LangChain").

    Returns:
        list: A list of 4-6 section heading strings.

    TODO:
        1. Define a PromptTemplate with input_variable "topic"
           - Instruct the LLM to return ONLY a numbered list of 5 headings, one per line
        2. Format the prompt:   formatted = prompt.format(topic=topic)
        3. Call the LLM:        response = llm.invoke(formatted)
        4. Parse the response:  split by "\\n", strip whitespace, drop blank lines
        5. Return the list
    """
    # TODO: implement this function
    # Remove the placeholder return below once implemented
    return [f"Introduction to {topic}", "Key Concepts", "Conclusion"]


# ── Stage 2: Generate Full Content ────────────────────────────────────────────
def generate_content(outline: list) -> str:
    """
    Expands an outline into a full markdown-formatted blog post.

    Args:
        outline (list): Section headings from generate_outline().

    Returns:
        str: A complete blog post with ## headings and 2-3 paragraphs per section.

    TODO:
        1. Join the outline into a single string:  outline_str = "\\n".join(outline)
        2. Define a PromptTemplate with input_variable "outline"
           - Instruct the LLM to write 2-3 paragraphs per section using ## headings
        3. Format the prompt:   formatted = prompt.format(outline=outline_str)
        4. Call the LLM:        response = llm.invoke(formatted)
        5. Return response.content
    """
    # TODO: implement this function
    # Remove the placeholder return below once implemented
    return "\n\n".join([f"## {h}\nContent for {h}." for h in outline])


# ── Stage 3: Summarize ────────────────────────────────────────────────────────
def summarize(content: str) -> str:
    """
    Produces a concise 3-5 sentence summary of the full blog post.

    Args:
        content (str): The full blog post text from generate_content().

    Returns:
        str: A short summary paragraph (3-5 sentences).

    TODO:
        1. Truncate content to avoid token limits:  content = content[:3000]
        2. Define a PromptTemplate with input_variable "content"
           - Instruct the LLM to summarize in exactly 3-5 sentences
        3. Format the prompt:   formatted = prompt.format(content=content)
        4. Call the LLM:        response = llm.invoke(formatted)
        5. Return response.content
    """
    # TODO: implement this function
    # Remove the placeholder return below once implemented
    return content[:200] + "..."


# ── Main (CLI entry point) ────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="AI Content Generator — generates a blog outline, content, and summary."
    )
    parser.add_argument(
        "--topic",
        required=True,
        help='Topic for the blog post. Example: "Getting started with LangChain"'
    )
    args = parser.parse_args()

    print(f"\n🔄 Running Content Generator Pipeline")
    print(f"   Topic: {args.topic}")
    print("=" * 60)

    print("\n📝 STEP 1 — Generating Outline...")
    outline = generate_outline(args.topic)
    print("OUTLINE:")
    for i, point in enumerate(outline, 1):
        print(f"  {i}. {point}")

    print("\n📄 STEP 2 — Generating Full Content...")
    content = generate_content(outline)
    print("\nCONTENT (first 500 chars):")
    print(content[:500], "...")

    print("\n🔍 STEP 3 — Summarizing...")
    summary = summarize(content)
    print("\nSUMMARY:")
    print(summary)

    print("\n" + "=" * 60)
    print("✅ Done!")


if __name__ == "__main__":
    main()
