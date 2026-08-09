# 🤖 Assignment 1 — Option 2: Chatbot with Conversational Memory

> **Cohort:** AI Engineer Ready — Cohort 1
> **Difficulty:** ⭐⭐⭐ Intermediate
---

## 📌 Problem Statement

Most chatbots have no memory. Ask *"What sport did I say I love?"* and a forgetful bot will have no idea — it treats every message as brand new.

**Your task:** Complete the memory-enabled chatbot pipeline in this repository. The scaffolding is already in place — your job is to replace the placeholder implementation with real LLM-powered logic using `PromptTemplate` and LangChain.

The finished chatbot should:

- **Remember** everything discussed in the current conversation
- **Generate context-aware replies** that reference what you said earlier
- **Persist memory to disk** (`memory.json`) so the conversation survives across multiple script runs

---

## 📁 Repository Structure

```
Option2_Chatbot_With_Memory/
│
├── chatbot.py                  # Main script — your primary file to edit
├── Chatbot_With_Memory.ipynb   # Guided notebook — start here
├── requirements.txt            # Python dependencies
├── memory.json                 # Auto-created at runtime to persist chat history
└── README.md                   # This file
```

| File | Purpose |
|---|---|
| `chatbot.py` | Runs the chat loop, loads/saves memory, and calls `generate_response()` — **the function you implement** |
| `Chatbot_With_Memory.ipynb` | Step-by-step guided notebook — build and test your implementation section by section |
| `requirements.txt` | Lists required packages — install before starting |
| `memory.json` | Auto-generated at runtime — stores conversation history between runs |

---

## 🛠️ Setup

### Step 1 — Clone the repository and navigate to this folder

```bash
git clone <repo-url>
cd "AI Engineer Ready - Cohort1/Assignment 1/Option2_Chatbot_With_Memory"
```

### Step 2 — Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Set your API key

Create a `.env` file in this folder:

```
OPENAI_API_KEY=your_key_here
```

Then load it at the top of your script:

```python
from dotenv import load_dotenv
load_dotenv()
```

> **No OpenAI key?** You can use [Groq](https://console.groq.com) (free tier) or [Google Gemini](https://aistudio.google.com) instead. Just swap the LLM in your LangChain setup — the `PromptTemplate` and LCEL structure stays the same.

---

## 📓 How to Use the Notebook

**Start with `Chatbot_With_Memory.ipynb`** — it walks you through the entire implementation one section at a time.

### Notebook Sections

| Section | What You Do |
|---|---|
| **1 — Environment Setup** | Install packages, load `.env`, verify LLM connection |
| **2 — Memory Format** | Understand the `{"role", "text"}` structure; implement `format_memory()` |
| **3 — Load & Save JSON** | Study and test `load_memory()` / `save_memory()` |
| **4 — PromptTemplate** | Build the prompt with `{history}` and `{user_input}` placeholders |
| **5 — LCEL Chain** | Connect prompt → LLM using the `\|` pipe operator |
| **6 — generate_response()** | ⭐ Assemble everything into the core function |
| **7 — Full Chat Loop** | Simulate a 3-turn conversation and verify memory persists |
| **8 — Code Quality** | Self-assessment checklist before submitting |
| **9 — Final Checklist** | Submission checklist and grading breakdown |

Each section follows the same pattern:

```
📖 Explanation  →  🧱 Scaffold code  →  ✏️ TODO cell  →  ✅ Verification cell
```

**Recommended workflow:**
1. Work through the notebook top to bottom — don't skip sections
2. Run every `✅ Verification` cell and make sure it passes before moving on
3. Once `generate_response()` works in the notebook, copy it into `chatbot.py`
4. Run `chatbot.py` end-to-end to confirm everything works

---

## 🧱 What You Need to Implement

### The Memory Format

The `memory` variable is a Python list of dictionaries — one dict per message:

```python
[
  {"role": "user",      "text": "Hi! My name is Priya."},
  {"role": "assistant", "text": "Hello Priya! How can I help you today?"},
  {"role": "user",      "text": "I want to learn about neural networks."}
]
```

You will write a `format_memory()` function that converts this list into a readable string like:

```
User: Hi! My name is Priya.
Assistant: Hello Priya! How can I help you today?
User: I want to learn about neural networks.
```

---

### Function: `generate_response(user_input, memory)`

This is the core function — located in `chatbot.py` with a `# TODO` comment. Your job is to replace the placeholder with real logic.

**Current placeholder:**

```python
def generate_response(user_input: str, memory: list) -> str:
    # TODO: Use PromptTemplate + LLM to generate a context-aware response
    return "This is a placeholder response. Replace with LLM call."
```

**Your implementation must:**

1. Call `format_memory(memory)` to convert the history list into a string
2. Build a prompt using LangChain's `PromptTemplate` with `{history}` and `{user_input}` placeholders — include a system instruction like *"You are a helpful assistant. Remember context from the conversation."*
3. Create a `ChatOpenAI` LLM and connect it to the prompt using LCEL (`prompt | llm`)
4. Call `.invoke()` on the chain and return the model's reply as a plain string (`result.content`)

**Tips:**

- Use `msg["role"].capitalize()` to get `"User"` or `"Assistant"` when formatting history
- Use **LangChain LCEL** (the `|` pipe syntax) — it's the modern approach, preferred over the older `LLMChain`
- Set `temperature=0.7` for natural, conversational responses
- Return `result.content` — not `result` itself (that's an `AIMessage` object, not a string)

---

## ▶️ Running the Chatbot

Once your implementation is in `chatbot.py`:

```bash
python chatbot.py
```

Type `exit` or `quit` to end the session. The conversation is automatically saved to `memory.json`.

### Verifying Memory Works — Test Conversation

Run through this exact exchange to confirm memory is working:

```
You: My name is Arjun and I love cricket.
Bot: [greets Arjun and acknowledges cricket]

You: What sport did I say I love?
Bot: [should say cricket — without you repeating yourself]

You: Suggest a Python project related to what I enjoy.
Bot: [should suggest something cricket-related]
```

If the bot answers correctly without you repeating yourself — **your memory implementation works.** ✅

---

## ✅ Evaluation Criteria

| Criteria | Weight |
|---|---|
| `generate_response()` correctly uses PromptTemplate + LLM (not a hardcoded response) | 30% |
| Conversation history is passed into the prompt and influences the bot's replies | 30% |
| `memory.json` is correctly saved and loaded between runs | 15% |
| Code is clean, readable, and well-commented | 15% |
| Runs end-to-end via `chatbot.py` without errors | 10% |

---

## ❓ FAQ

**Q: Can I use a different LLM — Gemini, Groq, Mistral?**
Yes. Replace `ChatOpenAI` with the appropriate LangChain wrapper. The `PromptTemplate` and LCEL structure stays exactly the same.

**Q: Do I have to use LangChain?**
The core requirement is `PromptTemplate + LLM`. Using the OpenAI SDK directly with a manually crafted prompt is acceptable — just document your approach clearly in the notebook.

**Q: My bot forgets things even though `memory.json` exists. Why?**
Two things to check: (1) make sure you are reading the file at the start of `main()` and passing the `memory` list into `generate_response()`, and (2) make sure you are appending new messages to the list *before* calling `save_memory()`.

**Q: I'm getting an `OPENAI_API_KEY` not found error.**
Create a `.env` file in the assignment folder (same level as `chatbot.py`) containing `OPENAI_API_KEY=sk-...` and make sure `load_dotenv()` is called at the top of your script.

**Q: Can I change the structure of `memory.json`?**
The `{"role": ..., "text": ...}` format should be preserved since `chatbot.py` depends on it. You may add extra fields if needed.

**Q: My bot returns an `AIMessage` object instead of a string.**
You are returning `result` instead of `result.content`. The LLM chain returns an `AIMessage` object — always extract the text with `.content`.

---

## 💬 Need Help?

Post questions in the cohort Discord / WhatsApp group under `#assignment-1-help`.

Check the notebook hints before asking — most common issues are covered in the `✅ Verification` cells and the FAQ above.

---

> 🧠 **Pro Tip:** The quality of your chatbot depends almost entirely on how well you construct the `PromptTemplate`. Spend real time on it — inject the history cleanly, write a clear system instruction, and iterate. That's the core skill being assessed here.

*Happy building! The scaffolding is ready — your job is to bring it to life. 🚀*