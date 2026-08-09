# Week 3 (Live) Cheatsheets

Five printable, one-page PDF quick-reference sheets that pair with the
[Week 3 Live workbook](../Week3_LangChain_Basics_Student_Workbook%20_student.ipynb),
styled to match the Week 1/Week 2 cheatsheet series.

| # | Cheatsheet | Covers |
|---|---|---|
| 1 | [LangChain Core Concepts Cheatsheet](01_LangChain_Core_Concepts_Cheatsheet.pdf) | What LangChain is, LLM vs chat model, roles (system/user/assistant), full glossary. |
| 2 | [Prompt Templates Cheatsheet](02_Prompt_Templates_Cheatsheet.pdf) | `.format()` placeholders, multi-variable templates, few-shot prompting patterns, common mistakes. |
| 3 | [Chat Model API Cheatsheet — invoke / batch / stream](03_Chat_Model_Invoke_Batch_Stream_Cheatsheet.pdf) | `init_chat_model`, `SystemMessage`/`HumanMessage`, when to use invoke vs batch vs stream, syntax for each. |
| 4 | [JSON Output & Parsing Cheatsheet](04_JSON_Output_Parsing_Cheatsheet.pdf) | Asking a model for JSON, `json.loads()`, handling malformed output, defensive parsing pattern. |
| 5 | [Chains & Debugging Cheatsheet](05_Chains_Debugging_Cheatsheet.pdf) | The Translate → Summarize chain pattern, the 4-step debugging process, pre-flight checklist, common errors table. |

## When to reach for which one

- Explaining the big picture to a teammate? → **01**
- Writing/fixing a prompt template? → **02**
- Not sure whether to call `invoke`, `batch`, or `stream`? → **03**
- Model response won't parse as JSON? → **04**
- A multi-step chain is producing wrong output, or you don't know where it broke? → **05**
