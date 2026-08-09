# Week 3 (Live) — LangChain Basics: Prompts, LLMs, Chains

This is the **live-session** workbook for Week 3. It is written for students who are
touching LangChain for the very first time — no prior framework experience assumed.

**Notebook:** [Week3_LangChain_Basics_Student_Workbook _student.ipynb](Week3_LangChain_Basics_Student_Workbook%20_student.ipynb)

**Cheatsheets:** see [Cheatsheets/](Cheatsheets/) for five printable quick-reference sheets
that pair with this notebook.

---

## What You'll Learn Today

By the end of this session you should be able to:

1. Explain what LangChain does and why it's useful.
2. Tell the difference between an **LLM** and a **chat model**.
3. Write a reusable prompt with `PromptTemplate`-style placeholders (`{var}` + `.format()`).
4. Call a chat model with `.invoke()`.
5. Understand when to use `.batch()` vs `.stream()` instead of `.invoke()`.
6. Ask a model for JSON and safely parse it with `json.loads()`.
7. Build a tiny two-step **chain** (Translate → Summarize).
8. Debug the most common beginner mistakes (missing API key, typo'd model name, bad JSON).

---

## Before the Session: Setup

You need three things ready **before** class starts:

### 1. Python environment
Any recent Python 3.10+ environment (venv, conda, or the one from Week 1) works.

### 2. Packages
The notebook installs these for you in the first code cell, but you can pre-install to save time:

```bash
pip install -U langchain langchain-openai python-dotenv
```

### 3. `.env` file with your API key
Create a file named `.env` in this same folder (`Live/`) with:

```
OPENAI_API_KEY=sk-your-key-here
```

> ⚠️ Never commit `.env` to Git or share it in chat/Slack. Add it to `.gitignore`.

Run the "Setup: Load API Key" cell — it should print `OPENAI_API_KEY found: True`.
If it prints `False`, see [Troubleshooting](#troubleshooting) below.

---

## How the Notebook Is Organized

| Section | What happens |
|---|---|
| 1. What is LangChain? | Concept only — the "toolbox" mental model. |
| 1b. LLM vs Chat Model | Concept only — why we use chat models in this course. |
| 2. Must-Know Glossary | Reference block — keep this open while coding. |
| Setup | Install packages, load `.env`, verify the API key. |
| Concept Checks | Small ungraded warm-ups: `invoke`/`batch`/`stream`, prompt templates, roles, JSON. |
| First Real Chat Model Call | The first live API call — `init_chat_model` + `invoke`. |
| Tokens / Context Window / Temperature | Reference block. |
| Prompt Templates with the Chat Model | Reusable templates fed into the model. |
| Few-Shot Prompting + JSON Output | Ask the model to return structured JSON, then parse it. |
| Chains & Orchestration | Build `translate()` and `summarize()` and chain them. |
| Debugging Basics | The 4-step process + a pre-flight checklist. |
| In-Class Exercises 1–5 | Hands-on, ~5–10 min each (see below). |
| Extension Task | Take-home: a 3-step Translate → Summarize → Extract Key Points pipeline. |

---

## In-Class Exercises (do these live)

| # | Exercise | Time | Goal |
|---|---|---|---|
| 1 | `invoke` with different prompts | 5 min | See how prompt wording changes output |
| 2 | `batch` with 3–5 prompts | 5 min | Compare batch vs repeated invoke |
| 3 | `stream` a response | 5 min | See tokens arrive incrementally |
| 4 | Structured JSON output | 5 min | Ask for JSON, parse with `json.loads`, handle failures |
| 5 | Add a `tone` parameter to the chain | 10 min | Extend an existing function without breaking it |

Every exercise cell starts with a `# TODO: Write your code here` comment — that's where your code goes.

## Extension Task (take-home if not finished in class)

Build `process_content(text)` that:
1. Translates input text to English (if needed)
2. Summarizes it in one paragraph
3. Extracts key points as a JSON list of strings

Requirements: system + user messages, prompt templates for each step, `try/except` around
API calls and JSON parsing, tested on **at least 2 different texts**.

Bonus: add `tone`, add `max_points`, cache repeated calls, try `batch()` for multiple texts.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `OPENAI_API_KEY found: False` | `.env` missing, misnamed, or not in this folder | Create `.env` next to the notebook, no quotes around the key, then re-run the cell |
| `ModuleNotFoundError` | Packages not installed in the active kernel | Re-run the `pip install` cell, then **restart the kernel** |
| `AuthenticationError` | Bad/expired key, or billing not set up | Check the key on platform.openai.com, confirm billing is active |
| Model call hangs or times out | Network/proxy issue | Retry; check you're not behind a blocking firewall |
| `json.loads()` fails on the model's response | Model added extra text around the JSON, or it's not valid JSON | Print the raw response first (never parse blindly); tighten the prompt ("Output ONLY valid JSON") |
| Chain output looks wrong | An earlier step silently failed | Print the intermediate value after every step before moving to the next |
| `NameError: chat is not defined` | Ran a later cell before the "First Real Chat Model Call" cell | Run cells top-to-bottom in order |

**The 4-step debugging process (from the notebook):**
1. Identify where it breaks (API key? model call? JSON parsing?)
2. Print intermediate values
3. Check assumptions (key loaded? model name spelled right — `gpt-4o-mini`, not `gpt4o`?)
4. Google the exact error message

---

## Quick Glossary (also in the notebook)

- **Prompt** — the instruction you send to the model
- **PromptTemplate** — a reusable prompt with `{placeholders}`
- **LLM** — a model that generates raw text completions
- **Chat model** — a model that works with role-based messages (system/user/assistant)
- **System message** — hidden instruction that sets the model's behavior
- **User message** — the actual user input
- **Chain** — one step's output feeding into the next step's input
- **Token** — a chunk of text (~4 characters) the model reads/writes
- **Context window** — max tokens the model can process at once (`gpt-4o-mini` ≈ 128k)

---

## What to Submit

1. Your completed workbook notebook, all TODO cells attempted and run top-to-bottom.
2. In a markdown cell at the bottom (or on the LMS), answer:
   - One concept you understood well
   - One concept that was challenging
   - One question you still have

## Success Checklist

- [ ] `.env` loads and prints `True`
- [ ] First chat model call (`chat.invoke(...)`) runs and prints a response
- [ ] All 5 in-class exercises attempted
- [ ] Translate → Summarize chain runs end-to-end on a sample sentence
- [ ] At least one JSON response parsed successfully (with error handling in place)
- [ ] Reflection questions answered
