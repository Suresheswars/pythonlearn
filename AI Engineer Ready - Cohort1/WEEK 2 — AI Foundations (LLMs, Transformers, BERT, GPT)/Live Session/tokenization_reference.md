# Tokenization Reference Guide - Quick Lookup

## Token Counts by Model (Approximate)

### OpenAI Models

| Model | Input $/1K tokens | Output $/1K tokens | Context Window |
|-------|-------------------|--------------------|-----------------|
| **gpt-3.5-turbo** | $0.0005 | $0.0015 | 4K tokens |
| **gpt-4** | $0.03 | $0.06 | 8K tokens |
| **gpt-4-turbo** | $0.01 | $0.03 | 128K tokens |
| **text-embedding-3-small** | $0.02 | - | - |
| **text-embedding-3-large** | $0.13 | - | - |

---

## Quick Token Estimates

### English Text (Rule of Thumb)

```
1 word ≈ 1.3 tokens
100 words ≈ 130 tokens
1000 words ≈ 1300 tokens
1 page (250 words) ≈ 325 tokens
```

### Common Patterns

| Content Type | Example | Token Count |
|--------------|---------|------------|
| Single word | "hello" | 1 |
| Short sentence | "Hello, world!" | 4 |
| Average paragraph | 100 words | ~130 |
| Short email | 150 words | ~195 |
| Medium article | 500 words | ~650 |
| Long document | 2000 words | ~2600 |
| Book chapter | 5000 words | ~6500 |

---

## Token Costs for Common Tasks

### Chat API Usage

```
Prompt:  500 tokens × $0.0005 = $0.00025
Response: 300 tokens × $0.0015 = $0.00045
─────────────────────────────────
Total:    800 tokens           = $0.0007 (≈ $0.001)
```

### Embeddings

```
Document (300 tokens) × $0.02 ÷ 1000 = $0.000006
(Much cheaper than Chat API!)
```

---

## How to Calculate Tokens in Python

### Using tiktoken

```python
import tiktoken

# Load tokenizer
encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

# Count tokens
text = "Hello, world!"
tokens = encoding.encode(text)
print(len(tokens))  # 4

# Decode tokens back
decoded = encoding.decode(tokens)
print(decoded)  # "Hello, world!"
```

### Using OpenAI API Response

```python
from openai import OpenAI

client = OpenAI()
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response.usage.prompt_tokens)      # Input tokens
print(response.usage.completion_tokens)  # Output tokens
print(response.usage.total_tokens)       # Total used
```

---

## Cost Optimization Tips

### 1. Use Cheaper Models When Possible
- **Fast & cheap**: gpt-3.5-turbo (0.0005 + 0.0015 per 1K tokens)
- **Accurate but pricey**: gpt-4 (0.03 + 0.06 per 1K tokens)
- **Choose based on task**: Simple Q&A → 3.5, complex reasoning → GPT-4

### 2. Reduce Prompt Size
- **Before**: "You are an AI assistant. Your job is to help. Be helpful and harmless and honest. Now answer this question: What is AI?"
- **After**: "Answer briefly: What is AI?"

Savings: ~50% token reduction

### 3. Use Streaming
- Get responses token-by-token
- Show results faster (UX improvement)
- Token count remains the same

### 4. Compress Context
- **Summarize** long documents before sending
- **Extract** key points instead of full text
- **Use embeddings** + semantic search instead of full RAG

### 5. Batch Requests
- Process multiple items together when possible
- Reduces API call overhead

### 6. Cache Common Prompts
- Save recurring system prompts
- Use prompt template libraries

---

## Tokenization Edge Cases

### Multi-Character Tokens

Some sequences tokenize as a single token:

| Text | Tokens | Count |
|------|--------|-------|
| "Hello" | [Hello] | 1 |
| "world" | [world] | 1 |
| "🚀" | [🚀] | 1 |
| "..." | [...] | 1 |
| " and " | [and] | 1 |

### Multi-Token Words

Some words use multiple tokens:

| Word | Token Count | Reason |
|------|------------|--------|
| "running" | 1 | Common |
| "unfortunately" | 2 | Less common |
| "internationalization" | 4 | Rare |
| "pneumonoultramicroscopicsilicovolcanoconiosis" | 17 | Extremely rare |

### Special Characters

| Character | Token Count |
|-----------|------------|
| Space " " | Varies (usually 0-1) |
| Newline "\n" | 1 |
| Tab "\t" | 1 |
| Special char "@" | 1 |
| Emoji "😀" | 1 |

---

## Context Window Management

### What is a Context Window?

Maximum number of tokens you can send in one request.

### Limits by Model

```
GPT-3.5-turbo: 4K tokens (≈ 3000 words)
GPT-4-8K: 8K tokens (≈ 6000 words)  
GPT-4-Turbo: 128K tokens (≈ 96,000 words)
```

### Example: Staying Within Budget

```python
# Your document is 5000 tokens
doc_tokens = 5000

# But GPT-3.5 max is 4000
max_tokens = 4000

# Problem!
if doc_tokens > max_tokens:
    # Solution 1: Use GPT-4-Turbo (128K limit)
    # Solution 2: Split document into chunks
    # Solution 3: Summarize document first
    pass
```

---

## Monitoring and Debugging

### Check Token Usage After API Calls

```python
response = client.chat.completions.create(...)

print(f"Prompt tokens: {response.usage.prompt_tokens}")
print(f"Completion tokens: {response.usage.completion_tokens}")
print(f"Total tokens: {response.usage.total_tokens}")

# Calculate cost
cost = (response.usage.total_tokens / 1000) * 0.0005
print(f"Cost: ${cost:.6f}")
```

### Real-Time Token Counter

```python
def estimate_cost(tokens, model="gpt-3.5-turbo"):
    rates = {
        "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
        "gpt-4": {"input": 0.03, "output": 0.06},
    }
    input_cost = (tokens / 1000) * rates[model]["input"]
    output_cost = (tokens / 1000) * rates[model]["output"]
    return input_cost + output_cost

tokens = 1500
print(f"${estimate_cost(tokens):.4f}")
```

---

## Common Questions

### Q: Does whitespace count as tokens?

**A**: Usually not—leading/trailing spaces are often stripped. But spaces between words might count as part of a token.

### Q: Why does my code have different token count than the tokenizer?

**A**: API responses include system tokens and formatting. The tokenizer shows raw text tokens.

### Q: How do I reduce token count for cost savings?

**A**: Summarize input, use embeddings for search, batch requests, or upgrade to a longer-context model.

### Q: What's the difference between input and output tokens?

**A**: Input = your prompt. Output = model's response. Output often costs more because generation is more compute-intensive.

---

## Resources

- **Official Tokenizer**: https://platform.openai.com/tokenizer
- **tiktoken GitHub**: https://github.com/openai/tiktoken
- **OpenAI Pricing**: https://openai.com/pricing
- **Context Window Docs**: https://platform.openai.com/docs/guides/tokens
