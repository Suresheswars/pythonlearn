# chatbot_homework.py
"""
TerminalTranslator — standalone chatbot (dotenv + init_chat_model) with guardrail + memory.

Run:
  pip install -U python-dotenv langchain langchain-openai
  # .env: OPENAI_API_KEY=...
  python chatbot_homework.py
"""

from __future__ import annotations

import os
import re
from datetime import datetime
from typing import List

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import PromptTemplate


EXIT_WORDS = {"quit", "exit", "bye"}
MAX_TURNS_TO_KEEP = 16
SAVE_TRANSCRIPT = True


SYSTEM_PROMPT_TMPL = PromptTemplate.from_template(
    """You are "{bot_name}", a focused {role}.

Job scope (STRICT):
- You ONLY translate text the user provides into a target language.
- If the user asks anything else (questions, advice, general chat), you must refuse and redirect.

When translating:
- Output ONLY the translated text (no extra commentary) unless the user asks otherwise.
- If the target language is missing, ask: "Which language should I translate it to?"

Refusal style:
- 1-2 sentences, polite, redirect to "paste text to translate".
"""
)


def build_system_message(bot_name: str, role: str) -> SystemMessage:
    return SystemMessage(content=SYSTEM_PROMPT_TMPL.format(bot_name=bot_name, role=role))


def is_exit(text: str) -> bool:
    return text.strip().lower() in EXIT_WORDS


def safe_input(prompt: str) -> str:
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        return "quit"


def trim_history(messages: List, max_turns_to_keep: int) -> List:
    if not messages:
        return messages
    system = messages[0] if isinstance(messages[0], SystemMessage) else None
    rest = messages[1:] if system else messages[:]
    max_msgs = max_turns_to_keep * 2
    if len(rest) <= max_msgs:
        return messages
    trimmed_rest = rest[-max_msgs:]
    return ([system] + trimmed_rest) if system else trimmed_rest


def save_transcript(messages: List, filename: str) -> None:
    lines = []
    for m in messages:
        if isinstance(m, SystemMessage):
            lines.append(f"SYSTEM: {m.content}")
        elif isinstance(m, HumanMessage):
            lines.append(f"USER: {m.content}")
        elif isinstance(m, AIMessage):
            lines.append(f"ASSISTANT: {m.content}")
        else:
            lines.append(f"MSG: {getattr(m, 'content', str(m))}")
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n\n".join(lines).strip() + "\n")


_TRANSLATE_VERBS = re.compile(r"\btranslate|translation|convert\b", re.IGNORECASE)


def looks_like_translation_task(text: str) -> bool:
    t = text.strip()
    if len(t) < 2:
        return False

    # Explicit translate request is in-scope
    if _TRANSLATE_VERBS.search(t):
        return True

    # Questions are treated as off-topic (translator only)
    if t.endswith("?"):
        return False

    # Short meta-instructions about the bot are not translation tasks
    lowered = t.lower()
    meta_markers = [
        "you are", "you're", "act as", "please", "can you", "could you",
        "i'm a translator", "be a translator", "tasks only", "only"
    ]
    if any(m in lowered for m in meta_markers) and len(t.split()) <= 12:
        return False

    # Otherwise assume they pasted text to translate
    return True


def main() -> int:
    load_dotenv()

    bot_name = "TerminalTranslator"

    # REQUIRED: welcome message describing what the bot does
    print(f"Welcome to {bot_name}!")
    print("I translate text you paste in. I will refuse non-translation requests.")
    print("Type 'quit', 'exit', or 'bye' anytime to end the chat.\n")

    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.2"))

    try:
        llm = init_chat_model(
            model=model_name,
            model_provider="openai",
            temperature=temperature,
        )
    except Exception as e:
        print("Failed to initialize the chat model.")
        print(f"Error: {e}")
        return 1

    messages: List = [build_system_message(bot_name=bot_name, role="translator")]

    while True:
        text = safe_input("Please enter the text you want to translate:\n> ").strip()
        if not text:
            print("Please type some text to translate.\n")
            continue
        if is_exit(text):
            print("\nGoodbye!")
            break

        # Guardrail: refuse off-topic inputs and DO NOT ask for target language
        if not looks_like_translation_task(text):
            messages.append(HumanMessage(content=text))
            messages = trim_history(messages, MAX_TURNS_TO_KEEP)
            try:
                resp = llm.invoke(messages)
                messages.append(AIMessage(content=resp.content))
                print("\n--- Translator ---")
                print(resp.content.strip())
                print()
            except Exception as e:
                print("\n--- Error ---")
                print("Sorry — I couldn't reach the model/API right now. Please try again.")
                print(f"(Details: {e})\n")
            continue

        target_lang = safe_input("\nWhich language do you want to translate it to?\n> ").strip()
        if not target_lang:
            print("Please provide a target language.\n")
            continue
        if is_exit(target_lang):
            print("\nGoodbye!")
            break

        user_request = (
            f"Translate the following text into {target_lang}. "
            f"Return ONLY the translated text.\n\n{text}"
        )

        messages.append(HumanMessage(content=user_request))
        messages = trim_history(messages, MAX_TURNS_TO_KEEP)

        try:
            resp = llm.invoke(messages)
            messages.append(AIMessage(content=resp.content))
            print("\n--- Translated text ---")
            print(resp.content.strip())
            print()
        except Exception as e:
            print("\n--- Error ---")
            print("Sorry — I couldn't reach the model/API right now. Please try again.")
            print(f"(Details: {e})\n")

    if SAVE_TRANSCRIPT:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chat_transcript_{ts}.txt"
        try:
            save_transcript(messages, filename)
            print(f"(Saved conversation to {filename})")
        except Exception as e:
            print(f"(Could not save transcript: {e})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())