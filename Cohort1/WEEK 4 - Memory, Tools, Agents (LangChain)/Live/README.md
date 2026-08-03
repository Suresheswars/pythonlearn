# Week 4 Live Sessions: Memory, Tools, and Agents with LangChain

This folder contains the live classroom material for Week 4. The goal of this week is to help students understand how LangChain-based chatbots become more useful when they can remember context, call tools, and decide when to act.

Students should use this README as a note-taking guide while working through the notebooks. The code cells are intentionally designed for live coding, so the most important learning happens when students write down the concept, the pattern, and the reason behind each step.

## What Students Should Learn

By the end of this week, students should be able to:
- explain why LLMs are stateless by default
- compare buffer, summary, and window memory
- build simple LangChain tools with clear names and docstrings
- understand how an agent chooses which tool to use
- describe ReAct as reason first, then act
- combine memory, tools, and decision-making into a small chatbot-style app

## Files In This Folder

Use the student notebooks during class. Use the solution notebooks only when you need to unblock yourself or compare your work.

- `1. Week4_Student_Memory_Tools_ReAct.ipynb`: main notebook for memory, tools, ReAct, mini-app thinking, and classroom practice
- `1. Week4_Student_Memory_Tools_ReAct_Solution.ipynb`: completed reference version of the first notebook
- `2. Student_Agents_and_Tools.ipynb`: focused notebook for building tools and creating an agent
- `2. Student_Agents_and_Tools_Solution.ipynb`: completed reference version of the second notebook
- `3. Student_Live_Coding_Chatbot.ipynb`: chatbot notebook focused on adding memory and running an interactive loop

## How To Use These Notebooks

1. Start with the student notebook and try to answer the prompts before looking at the solution.
2. Write short notes after each section: what the feature does, when to use it, and what problem it solves.
3. If a cell is a hint cell, treat it like a checklist. Fill in the missing code yourself.
4. If you get stuck, compare with the solution notebook and then return to the student notebook to continue.

## Detailed Session Guide

### 1. Memory, Tools, and ReAct

Notebook: `1. Week4_Student_Memory_Tools_ReAct.ipynb`

This is the most important notebook in the folder. It introduces three core ideas in one flow: memory, tools, and ReAct.

What students should note:
- LLMs do not remember previous messages unless memory is added explicitly
- buffer memory stores everything, summary memory stores a shorter recap, and window memory stores only the latest messages
- `RunnableWithMessageHistory` is the pattern that connects a chain to chat history
- tools are just Python functions that the model is allowed to call
- ReAct means the model reasons about the task, chooses an action, and then returns the final answer

Classroom checkpoints in this notebook:
- compare different memory types
- reuse the same `session_id` and observe what changes
- create simple tools such as a calculator and a Celsius-to-Fahrenheit converter
- identify when a task needs a tool and when it does not
- build a tiny mini-app idea that combines memory and tool use

Student note-taking prompts:
- What is the difference between buffer, summary, and window memory?
- Why does `session_id` matter?
- What makes a good tool name and docstring?
- When should an assistant use ReAct?
- What is one simple app idea you could build from these parts?

### 2. Building Agents and Choosing Tools

Notebook: `2. Student_Agents_and_Tools.ipynb`

This notebook focuses on tool creation and agent behavior. Students can see how an agent uses an LLM as the decision-maker and an executor to actually run the tools.

What students should note:
- a tool is a Python function with a clear purpose
- the `@tool` decorator tells LangChain that the function is available for agent use
- an agent decides what to do, while the executor runs the actions
- good tool descriptions help the agent choose correctly
- agents can use more than one tool when a question has multiple steps

Scenario practice in this notebook:
- math questions
- weather questions
- multi-step questions that need more than one tool

Exercises and homework in this notebook:
- create a word counter tool
- see how the agent handles unknown locations like `Paris`
- design a time tool
- design a string reverser tool

Student note-taking prompts:
- Why does the agent need a description for each tool?
- What is the difference between the agent and the executor?
- Which type of question should use a tool, and which should not?
- What happens when the tool does not know the answer?

### 3. Building a Chatbot with Memory

Notebook: `3. Student_Live_Coding_Chatbot.ipynb`

This notebook shows the full memory workflow in a chatbot setting. It first demonstrates the problem with a stateless model, then fixes it with message history, and finally turns the pattern into an interactive chat loop.

What students should note:
- each `invoke()` call is independent unless memory is added
- `RunnableWithMessageHistory` stores and reuses previous messages
- the same `session_id` keeps one conversation together
- a `while` loop can keep the chatbot running until the user types `stop` or `quit`

Final exercise in this notebook:
- build a travel agent chatbot with memory
- make the system prompt ask clarifying questions
- keep the same session active during the conversation

Student note-taking prompts:
- Why does the bot forget its earlier answer without memory?
- What role does the history placeholder play in the prompt?
- Why is a persistent session useful in real applications?
- How would you change the chatbot personality for a different use case?

## Suggested Note Template For Students

Copy this pattern into your notebook notes or personal study notes:

- Topic:
- What it does:
- Why it matters:
- One example:
- One question I still have:

## Setup Instructions

1. Create a `.env` file in this folder with the API keys needed by the notebooks.
2. Install the dependencies used across the live sessions.

Suggested packages:

```bash
pip install langchain langchain-core langchain-openai langchain-google-genai python-dotenv
```

Depending on the exact tools or models used in class, you may also need extra packages such as a search or browser integration library.

## Classroom Reminder

Students should treat these notebooks as working notes, not just runnable code. Encourage them to write down:
- the purpose of each pattern
- the meaning of each key object or class
- what changed after each code cell ran
- one real-world use case for the idea they just learned
