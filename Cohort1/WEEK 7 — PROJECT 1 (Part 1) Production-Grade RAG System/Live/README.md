# Multi-Document-Assist
The system shall enable users to upload documents and retrieve precise, context-aware answers in response to their queries based on the content of the uploaded documents.



## Architecture

![Unable to load Architecture](data/supporting_documents/multi-document-assist.drawio.png)

---



## 🖥 Local Installation

1 . Create Environment

```
py -3.12 -m venv .venv
source .venv/bin/activate     # Mac/Linux
.venv\Scripts\activate        # Windows
```

2. Install dependencies
```
pip install -r requirements.txt
```

## ▶ Running Locally (Without Docker)

3. Run FASTAPI 

```
uvicorn src.backend.main:app --host 0.0.0.0  --port 8000
```

4. Run Streamlit

```
python -m streamlit run src/frontend/app.py
```

## ▶ Running with Docker

1. Build Image

```
docker build -t multi-document-assist .
```

2. Run Container

```
docker run -p 8000:8000 -p 10000:10000 multi-document-assist
```


Backend 👉 http://localhost:8000/docs

Frontend 👉 http://localhost:10000

---


## 🖥 Render Deployment Link

```
https://multi-document-assist.onrender.com
```