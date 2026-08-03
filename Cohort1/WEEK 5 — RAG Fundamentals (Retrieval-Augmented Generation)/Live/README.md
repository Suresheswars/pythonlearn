# Week 5 Live Session: RAG Fundamentals

This folder contains the live classroom material for Week 5 of the RAG Fundamentals module. Use these notebooks in order to follow the progression from setup to chunking, embeddings, and retrieval.

## Contents

1. `WEEK5_RAG_Live_Session_student.ipynb`
2. `WEEK5_Chunking_Strategies_student.ipynb`
3. `WEEK5_Embeddings_Types_and_Dimensions_student.ipynb`
4. `WEEK5_Retrieval_student.ipynb`

Supporting documents are included for experimentation with document loading and retrieval:

1. `HDFC-Life-Group-Term-Life-Policy.pdf`
2. `HDFC-Life-Sampoorna-Jeevan-101N158V04-Policy-Document (1).pdf`
3. `HDFC-Life-Sanchay-Plus-Life-Long-Income-Option-101N134V19-Policy-Document.pdf`

## Recommended Flow

1. Start with `WEEK5_RAG_Live_Session_student.ipynb` for the core concepts.
2. Move to `WEEK5_Chunking_Strategies_student.ipynb` to compare chunk sizes and overlap.
3. Continue with `WEEK5_Embeddings_Types_and_Dimensions_student.ipynb` to understand embedding behavior.
4. Finish with `WEEK5_Retrieval_student.ipynb` to combine retrieval with grounded generation.

## What You Should Practice

1. Load PDFs and text documents into a simple RAG pipeline.
2. Compare different chunking strategies and note retrieval quality.
3. Observe how embedding choice affects semantic search.
4. Inspect retrieved context before generating a final answer.

## Setup Notes

If you run the notebooks locally, make sure the environment includes the dependencies used in the course notebooks, such as:

1. `langchain`
2. `langchain-openai`
3. `langchain-community`
4. `faiss-cpu`
5. `chromadb`
6. `pypdf`
7. `python-dotenv`

## Suggested Submission

If this folder is used for student work, keep the completed notebooks alongside a short note covering:

1. What retrieval setup worked best.
2. What changed when chunking was adjusted.
3. One improvement you would make in the next version of the pipeline.

## Required Work

- **Complete all class exercises and the homework** listed in [WEEK5_RAG_Live_Session_student.ipynb](WEEK5_RAG_Live_Session_student.ipynb): finish the "Class Exercises" sections and the newly-added "Homework Questions" cell.
- **Fill non-code cells** (answers, observations, short writeups) in the other notebooks listed above — these are required parts of the submission (not code-only cells).
- When you submit, include the completed notebooks and any additional artifacts requested in the homework (e.g., short demo video, cost analysis, or evaluation reports).