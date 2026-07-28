# 📧 Option 3 — AI Email Generator
### AI Engineer Ready | Cohort 1 | Assignment 1

---

## 🧠 What Is This Assignment?

You will build an **AI-powered email generator** using Python and LangChain.

Given a short **context** (what the email is about) and a **tone** (formal / informal / neutral), your program will call a real LLM (GPT) and return a complete, well-written email — subject line, greeting, body, and sign-off included.

This assignment teaches you how to:
- Use **LangChain's `PromptTemplate`** to write reusable, structured prompts
- Connect a prompt to an **LLM** (ChatGPT) using LangChain's chain syntax
- Build both a **Jupyter notebook** workflow and a **command-line** tool

---

## 🗂️ Project Structure

```
Option3_AI_Email_Generator/
│
├── AI_Email_Generator.ipynb   ← Your main workspace (work here first)
├── main.py                    ← Command-line version (update after notebook)
├── requirements.txt           ← Python dependencies
└── README.md                  ← This file
```

---

## ✅ Assignment Steps at a Glance

| Step | What You'll Do | File |
|------|----------------|------|
| 1 | Install dependencies | Notebook |
| 2 | Set up your OpenAI API key securely | Notebook |
| 3 | Learn how `PromptTemplate` works (demo) | Notebook |
| 4 ⭐ | Implement `generate_email(context, tone)` | Notebook |
| 5 | Test with formal, informal, and neutral tones | Notebook |
| 6 | Port your implementation to `main.py` | `main.py` |


> ⭐ Step 4 is the core task. Everything else supports it.

---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.11 or higher
- An OpenAI account with API access → [platform.openai.com](https://platform.openai.com)
- Jupyter Notebook or VS Code with the Jupyter extension

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Or run the first cell in the notebook — it handles this for you.

### 3. Get your OpenAI API key

1. Go to [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Click **Create new secret key**
3. Copy it — it looks like `sk-...`
4. When the notebook prompts you, paste it in. **Never hardcode it in your files.**

### 4. Open the notebook

```bash
jupyter notebook AI_Email_Generator.ipynb
```

Run the cells **top to bottom**, reading every markdown cell as you go.

### 5. Run from command line (after completing the notebook)

```bash
# Set your API key first
export OPENAI_API_KEY="sk-your-key-here"   # Mac/Linux
set OPENAI_API_KEY=sk-your-key-here        # Windows CMD

# Run the generator
python main.py --context "Schedule a meeting about Q3 results" --tone formal
python main.py --context "Remind a friend about hiking this weekend" --tone informal
python main.py --context "Notify team of a deadline change" --tone neutral
```

---

## 🎯 What Your `generate_email()` Function Must Do

Your implementation in Step 4 must:

1. **Define a `PromptTemplate`** with `input_variables=["context", "tone"]`
   - The template must instruct the LLM to write a complete email
   - It must specify the tone clearly and ask for: subject, greeting, body (2–3 paragraphs), sign-off

2. **Initialise `ChatOpenAI`** from `langchain_openai`
   - Recommended: `model="gpt-3.5-turbo"`, `temperature=0.7`

3. **Build a chain** using `prompt | llm`

4. **Invoke the chain** with `.invoke({"context": context, "tone": tone})`

5. **Return** `result.content` as a string

---

## 📊 Grading Breakdown

| Criteria | Marks |
|----------|-------|
| `PromptTemplate` used with correct `input_variables` | 20% |
| Prompt is detailed (subject + body + sign-off instructions) | 20% |
| `ChatOpenAI` correctly initialised | 20% |
| Chain built with `prompt \| llm` and `.invoke()` used | 20% |
| All 3 test tones produce real, complete emails | 20% |
| **Bonus:** Multi-language support (Step 7) | +30% |

---

## 📤 What to Submit

1. `AI_Email_Generator.ipynb` — with **all cells run** (outputs visible)
2. `main.py` — updated with your working implementation
3. A terminal screenshot showing `main.py` producing a real email

---

## ⚠️ Common Mistakes to Avoid

| Mistake | Why it's a problem |
|---------|-------------------|
| Using an f-string instead of `PromptTemplate` | Misses the point of the assignment |
| Hardcoding your API key in the file | Security risk — never commit keys to git |
| Returning `result` instead of `result.content` | Returns an object, not a string |
| A vague prompt like "write an email about {context}" | LLM output will be inconsistent and incomplete |
| Not running all cells before submitting | Evaluators need to see the output |

---

## 🔗 Useful Resources

- [LangChain PromptTemplate Docs](https://python.langchain.com/docs/concepts/prompt_templates/)
- [LangChain ChatOpenAI Docs](https://python.langchain.com/docs/integrations/chat/openai/)
- [OpenAI API Pricing](https://openai.com/pricing) — gpt-3.5-turbo is cheapest
- [LangChain Expression Language (LCEL) — the `|` pipe syntax](https://python.langchain.com/docs/concepts/lcel/)

---

## 💬 Need Help?

- Re-read the README cells in the notebook — they have step-by-step hints
- Ask in the cohort Slack/Discord channel
- Helping each other is encouraged — but don't share your full solution before the deadline!

---

*AI Engineer Ready — Cohort 1 | Assignment 1 | Option 3*
