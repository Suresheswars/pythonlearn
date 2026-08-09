# 📄 Assignment 1 — Option 1: AI-Powered Resume Analyzer

> **Cohort:** AI Engineer Ready — Cohort 1
> **Difficulty Level:** ⭐⭐⭐ (Intermediate)

---

## 🎯 Problem Statement

Recruiters spend an average of **6–7 seconds** scanning a resume before deciding whether a candidate moves forward. Most candidates have no idea whether their resume is aligned to a specific role — they apply blindly and wonder why they don't hear back.

**Your task:** Complete the Resume Analyzer pipeline in this repository. The scaffolding is already in place — your job is to **replace the placeholder implementations** with real LLM-powered logic using `PromptTemplate` and LangChain.

The finished tool should:
- **Extract skills** from any resume text using an LLM
- **Identify missing skills** by comparing extracted skills against a target role's requirements
- **Suggest improvements** — specific, actionable advice for each missing skill

---

## 📁 Repository Structure

```
Option1_Resume_Analyzer/
│
├── main.py                  # CLI entry point — run your analyzer here
├── Resume_Analyzer.ipynb    # Guided notebook — start here if you're new
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

### What each file does

| File | Purpose |
|---|---|
| `main.py` | Parses a resume from `--file` or `--text`, calls the three pipeline functions, and prints JSON output |
| `Resume_Analyzer.ipynb` | Step-by-step guided notebook with hints for each function |
| `requirements.txt` | Lists `openai`, `langchain`, `requests` — install before starting |

---

## 🛠️ Setup

### 1. Clone the repository and navigate to this folder

```bash
git clone <repo-url>
cd "AI Engineer Ready - Cohort1/Assignment 1/Option1_Resume_Analyzer"
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your API key

Create a `.env` file in this folder:

```
OPENAI_API_KEY=your_key_here
```

Then load it at the top of your script:

```python
from dotenv import load_dotenv
load_dotenv()
```

> **No OpenAI key?** You can use [Groq](https://console.groq.com) (free tier) or [Google Gemini](https://aistudio.google.com) instead. Just swap the LLM in your LangChain setup.

---

## 🧱 What You Need to Implement

Open `main.py`. You'll find three functions with `# TODO` comments. Your job is to replace each placeholder with real LLM logic.

---

### Function 1: `extract_skills(text: str) → list`

**What it should do:** Take raw resume text and return a Python list of skills mentioned in it.

**Current placeholder:**
```python
def extract_skills(text: str):
    # TODO: replace this placeholder with LLM + PromptTemplate logic
    return ["Python", "Data Analysis"]
```


**Tips:**
- Normalize skill names to lowercase for reliable comparison later

---

### Function 2: `identify_missing_skills(skills: list) → list`

**What it should do:** Compare the extracted skills against a target skill set for the role, and return what's missing.

**Current placeholder:**
```python
def identify_missing_skills(skills: list):
    # TODO: define target skills for the job/role and compare
    target = ["Python", "Data Analysis", "Machine Learning", "SQL"]
    return [s for s in target if s not in skills]
```

**Challenge (Optional):** Make the `target` skill list **dynamic** — accept a job description as input and use an LLM to extract the required skills from it, rather than hardcoding the list.

---

### Function 3: `suggest_improvements(missing: list) → list`

**What it should do:** For each missing skill, return a specific, actionable suggestion (not just "Learn X").

**Current placeholder:**
```python
def suggest_improvements(missing: list):
    # TODO: use LLM to craft human-friendly suggestions
    return [f"Learn {m}" for m in missing]
```


**Tips:**
- Keep `temperature` above 0 here — you want varied, natural suggestions
- Consider batching all missing skills into a single LLM call for efficiency

---

## ▶️ How to Run

### Using a text file

```bash
python main.py --file path/to/resume.txt
```


### Expected output format

```json
{
  "skills": ["Python", "SQL", "Data Analysis"],
  "missing_skills": ["Machine Learning", "Statistics"],
  "suggestions": [
    "Take Andrew Ng's Machine Learning Specialization on Coursera and build a regression project.",
    "Work through Khan Academy's Statistics course and apply it to a real dataset on Kaggle."
  ]
}
```

---

## 📓 Using the Notebook

If you prefer to build and test iteratively, start with `Resume_Analyzer.ipynb`. It walks you through each function one cell at a time with hints.

**Recommended workflow:**
1. Build and test each function in the notebook first
2. Once all three work, copy the implementations into `main.py`
3. Run `main.py` end-to-end to verify the pipeline

The notebook also has an **Integration Exercise** at the end — create a single `analyze_resume(text, target_skills)` function, test it on 3 example resumes, and save the outputs in a `results/` folder.

---

## ✅ Evaluation Criteria

| Criteria | Weightage |
|---|---|
| `extract_skills` correctly uses PromptTemplate + LLM (not hardcoded) | 25% |
| `identify_missing_skills` uses normalized, dynamic comparison | 20% |
| `suggest_improvements` returns specific, LLM-generated advice (not "Learn X") | 25% |
| Code is clean, readable, and well-commented | 15% |
| Successfully runs end-to-end via `main.py` | 15% |


---


## ❓ FAQ

**Q: Can I use a different LLM — Gemini, Groq, Mistral?**
Yes. Just replace the `OpenAI` LLM in LangChain with the appropriate wrapper. The `PromptTemplate` and `LLMChain` structure stays the same.

**Q: The target skills in `identify_missing_skills` are hardcoded — is that OK?**
For the base submission, yes. 

**Q: Do I need to support PDFs?**
Plain text (`.txt`) input is the minimum requirement. PDF support is a Stretch Goal.

**Q: Can I change the output format of `main.py`?**
The JSON structure (`skills`, `missing_skills`, `suggestions`) should be preserved. You may add extra fields.

---

## 💬 Need Help?

- Post questions in the cohort Discord/WhatsApp group under `#assignment-1-help` as instructed.
- Check the notebook hints before asking — most common issues are covered there

> 🧠 **Pro Tip:** The quality of your output depends almost entirely on the quality of your prompts. Spend real time crafting and iterating on your `PromptTemplate` — that's the core skill being assessed here.

---

*Happy building! The scaffolding is ready — your job is to bring it to life.* 🚀
