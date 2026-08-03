"""
exercise_tokenization.py - Tokenization Deep Dive Exercises
Week 2 Live Session - Classroom Exercises

This file contains hands-on exercises to deepen your understanding of tokenization.
Work through each challenge to practice using the tiktoken library.
"""

import tiktoken
import os
from dotenv import load_dotenv

# ============================================================================
# Setup
# ============================================================================

load_dotenv()

# Load tokenizer for GPT-3.5-turbo
encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

print("=" * 70)
print("TOKENIZATION EXERCISE SUITE - Week 2 Live Session")
print("=" * 70)


# ============================================================================
# CHALLENGE 1: Token Detective - Analyze Word Tokenization
# ============================================================================

def challenge_1_token_detective():
    """
    Challenge 1: Analyze how different words tokenize
    
    Some words tokenize into 1 token, others into multiple.
    Your task: Find the patterns!
    """
    print("\n" + "=" * 70)
    print("CHALLENGE 1: Token Detective")
    print("=" * 70)
    
    words = [
        "Hello",
        "running",
        "unfortunately",
        "internationalization",
        "AI",
        "ChatGPT",
        "🚀",
        "café",
        "naïve",
        "pneumonoultramicroscopicsilicovolcanoconiosis",  # Longest word in English!
    ]
    
    print("\nAnalyzing word tokenization:\n")
    print(f"{'Word':<50} {'Tokens':<10} {'Count':<10}")
    print("-" * 70)
    
    for word in words:
        tokens = encoding.encode(word)
        print(f\"{word:<50} {str(tokens):<10} {len(tokens):<10}\")
    
    # Challenge questions
    print("\n📊 REFLECTION QUESTIONS:")
    print("1. Which words tokenize into 1 token? (easier for LLM)")
    print("2. Which words use many tokens? (why?)")
    print("3. What patterns do you notice about multi-token words?")
    print("4. Why might tokenization affect model performance?")


# ============================================================================
# CHALLENGE 2: Budget Calculator - Token Counting for APIs
# ============================================================================

def challenge_2_budget_calculator():
    """
    Challenge 2: Calculate token costs for real-world scenarios
    
    You need to process multiple documents via API.
    How much will it cost?
    """
    print("\n" + "=" * 70)
    print("CHALLENGE 2: API Budget Calculator")
    print("=" * 70)
    
    # Sample documents
    documents = {
        "Short Email": "Hi, how are you? Looking forward to meeting next week.",
        "Medium Article": """
        Artificial Intelligence has revolutionized many industries.
        From healthcare to finance, AI systems are making critical decisions.
        Machine learning models require large datasets and significant computational resources.
        The future of AI promises even more advanced capabilities.
        """,
        "Long Document": """
        Natural Language Processing (NLP) is a subfield of artificial intelligence
        that focuses on the interaction between computers and human language.
        It's used in machine translation, sentiment analysis, question answering systems,
        and many other applications. The transformer architecture, introduced in the
        "Attention is All You Need" paper, has become the foundation for modern LLMs.
        GPT and BERT are two prominent examples. These models are trained on massive
        datasets using self-supervised learning techniques. Tokenization is a crucial
        preprocessing step in NLP pipelines. Understanding how text is broken into tokens
        is essential for optimizing API costs and managing context windows effectively.
        """ * 3,  # Repeat for more realistic size
    }
    
    # Pricing
    pricing = {
        "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},  # per 1K tokens
        "gpt-4": {"input": 0.03, "output": 0.06},
    }
    
    print("\n📋 Documents to process:\n")
    
    total_tokens = 0
    for doc_name, text in documents.items():
        tokens = encoding.encode(text)
        total_tokens += len(tokens)
        print(f"{doc_name:<20} {len(tokens):>6} tokens")
    
    print(f"\n{'TOTAL':<20} {total_tokens:>6} tokens")
    
    # Calculate costs
    print("\n💰 COST ESTIMATES (assuming 1x input + 1x output):\n")
    
    for model, rates in pricing.items():
        input_cost = (total_tokens / 1000) * rates["input"]
        output_cost = (total_tokens / 1000) * rates["output"]
        total_cost = input_cost + output_cost
        
        print(f"{model}:")
        print(f"  Input:  ${input_cost:.6f}")
        print(f"  Output: ${output_cost:.6f}")
        print(f"  Total:  ${total_cost:.6f}\n")
    
    # Challenge questions
    print("📊 CHALLENGE QUESTIONS:")
    print("1. If you process 100,000 documents this size, what's the total cost?")
    print("2. How would you reduce costs? (Hint: compression, summarization, etc.)")
    print("3. What's your token budget for a month?")


# ============================================================================
# CHALLENGE 3: Token Boundary Explorer - Find Edge Cases
# ============================================================================

def challenge_3_token_boundaries():
    """
    Challenge 3: Explore tokenization edge cases
    
    Discover how special characters, numbers, and whitespace tokenize.
    """
    print("\n" + "=" * 70)
    print("CHALLENGE 3: Token Boundary Explorer")
    print("=" * 70)
    
    test_cases = {
        "Numbers": "123 456 7890",
        "Punctuation": "Hello!!! What??? Really...",
        "Mixed": "Hello123world_test@example.com",
        "Whitespace": "Hello     world",  # Multiple spaces
        "Newlines": "Hello\\nworld\\nfrom\\nPython",
        "Special chars": "@#$%^&*()[]{}",
        "URLs": "https://www.example.com/api/v1/users",
        "Code": "def hello(): return 42",
        "Emoji": "👋 Hello! 🚀 Let's code! 💻",
    }
    
    print("\nEdge case analysis:\n")
    print(f\"{'Test Case':<25} {'Tokens':<15} {'Count':<10}\")
    print("-" * 50)
    
    for case_name, text in test_cases.items():
        tokens = encoding.encode(text)
        print(f\"{case_name:<25} {len(tokens):<15} tokens={len(tokens):<10}\")
    
    # Detailed breakdown
    print("\n\\n📊 DETAILED BREAKDOWN (Token IDs and decoded):\\n\")
    
    for case_name in ["URLs", "Code", "Emoji"]:
        text = test_cases[case_name]
        tokens = encoding.encode(text)
        print(f\"\\n{case_name}: '{text}'\")\n        print(f\"  Token count: {len(tokens)}\")\n        print(f\"  Token IDs: {tokens}\")\n        \n        # Decode each token\n        token_strings = [encoding.decode([t]) for t in tokens]\n        print(f\"  Decoded: {token_strings}\")\n        \n    # Challenge questions\n    print(\"\\n📊 REFLECTION QUESTIONS:\")\n    print(\"1. Why do URLs tokenize into many small tokens?\")\n    print(\"2. How does emoji tokenization compare to regular text?\")\n    print(\"3. What happens with very long URLs or code blocks?\")\n    print(\"4. How might this affect model understanding?\")\n\n\n# ============================================================================\n# CHALLENGE 4: The Tokenization Game - Predict Token Counts\n# ============================================================================\n\ndef challenge_4_prediction_game():\n    \"\"\"  \n    Challenge 4: Predict token counts before tokenizing\n    \n    Without running the tokenizer, try to PREDICT how many tokens\n    each sentence will use. Then check your accuracy!\n    \"\"\"\n    print(\"\\n\" + \"=\" * 70)\n    print(\"CHALLENGE 4: The Tokenization Prediction Game\")\n    print(\"=\" * 70)\n    \n    test_sentences = [\n        \"The quick brown fox jumps over the lazy dog.\",\n        \"Artificial intelligence is transforming the world.\",\n        \"Python programming is fun and productive!\",\n        \"Machine learning models require lots of data for training.\",\n        \"The fast and efficient tokenizer works in microseconds.\",\n        \"PNEUMONOULTRAMICROSCOPICSILICOVOLCANOCONIOSIS is the longest word.\",\n    ]\n    \n    print(\"\\n📝 INSTRUCTIONS:\")\n    print(\"1. For each sentence below, PREDICT how many tokens it will have\")\n    print(\"2. Write your prediction\")\n    print(\"3. Then we'll check the actual count\\n\")\n    \n    actual_counts = []\n    for i, sentence in enumerate(test_sentences, 1):\n        tokens = encoding.encode(sentence)\n        actual_counts.append(len(tokens))\n        \n        print(f\"\\nSentence {i}: '{sentence}'\")\n        print(f\"Your prediction: _____ tokens\")\n        print(f\"Actual count:    {len(tokens)} tokens\")\n        print(f\"Tokens: {tokens}\")\n        \n        # Show decoded tokens\n        token_strings = [encoding.decode([t]) for t in tokens]\n        print(f\"Breakdown: {token_strings}\")\n    \n    print(\"\\n\" + \"=\" * 50)\n    print(\"📊 How did you do? Compare your predictions to actual counts!\")\n    print(\"Typical ratio: English word ≈ 1.3 tokens\")\n    \n\n# ============================================================================\n# CHALLENGE 5: Real-World Scenario - Document Tokenization\n# ============================================================================\n\ndef challenge_5_real_world_scenario():\n    \"\"\"    \n    Challenge 5: Tokenize a realistic customer support ticket\n    \n    You're building an AI chatbot for customer support.\n    How many tokens does a typical support ticket use?\n    \"\"\"\n    print(\"\\n\" + \"=\" * 70)\n    print(\"CHALLENGE 5: Real-World Scenario - Customer Support Chatbot\")\n    print(\"=\" * 70)\n    \n    # Real-like customer support ticket\n    support_ticket = \"\"\"\n    Subject: Issue with payment processing\n    \n    Hello Support Team,\n    \n    I'm experiencing an issue with my payment not going through.\n    I tried multiple times today but keep getting an error message\n    saying \"Transaction declined\". My account has sufficient funds\n    and this is a new issue - it worked fine yesterday.\n    \n    Here are the details:\n    - Error Code: 40123\n    - Card: Visa ending in 4242\n    - Amount: $99.99\n    - Time: 2024-05-15 14:30 UTC\n    - Browser: Chrome 125.0 on Windows 11\n    \n    Please help me resolve this as soon as possible. I need to\n    complete this purchase today for an important project.\n    \n    Thank you for your assistance!\n    Best regards,\n    John Doe\n    \"\"\"\n    \n    tokens = encoding.encode(support_ticket)\n    \n    print(f\"\\n📋 CUSTOMER SUPPORT TICKET:\")\n    print(\"-\" * 70)\n    print(support_ticket)\n    print(\"-\" * 70)\n    \n    print(f\"\\n📊 TOKENIZATION ANALYSIS:\")\n    print(f\"  Text length: {len(support_ticket)} characters\")\n    print(f\"  Word count (approx): {len(support_ticket.split())} words\")\n    print(f\"  Token count: {len(tokens)} tokens\")\n    print(f\"  Ratio: {len(tokens) / len(support_ticket.split()):.2f} tokens/word\")\n    \n    # Cost calculation\n    cost_per_k = 0.0005  # GPT-3.5 input cost\n    cost = (len(tokens) / 1000) * cost_per_k\n    \n    print(f\"\\n💰 COST ANALYSIS:\")\n    print(f\"  Cost per 1K tokens: ${cost_per_k}\")\n    print(f\"  This ticket costs: ${cost:.6f}\")\n    print(f\"  For 1000 tickets: ${cost * 1000:.4f}\")\n    print(f\"  For 10,000 tickets: ${cost * 10000:.2f}\")\n    \n    print(f\"\\n❓ CHALLENGE QUESTIONS:\")\n    print(\"  1. Is this ticket size typical for your use case?\")\n    print(\"  2. How would you optimize this for lower costs?\")\n    print(\"  3. Could you compress this ticket while keeping context?\")\n    print(\"  4. What's your monthly budget for processing tickets?\")\n\n\n# ============================================================================\n# RUN ALL CHALLENGES\n# ============================================================================\n\nif __name__ == \"__main__\":\n    try:\n        challenge_1_token_detective()\n        challenge_2_budget_calculator()\n        challenge_3_token_boundaries()\n        challenge_4_prediction_game()\n        challenge_5_real_world_scenario()\n        \n        print(\"\\n\" + \"=\" * 70)\n        print(\"✅ ALL EXERCISES COMPLETED!\")\n        print(\"=\" * 70)\n        print(\"\"\"\n        Key Takeaways:\n        1. Tokenization is unpredictable without running the tokenizer\n        2. Costs add up quickly with large volumes\n        3. Edge cases (URLs, code, emoji) tokenize unexpectedly\n        4. Understanding tokenization helps optimize API usage\n        \n        Next: Practice these with different texts and models!\n        \"\"\")\n        \n    except Exception as e:\n        print(f\"\\n❌ Error running exercises: {e}\")\n        print(\"Make sure tiktoken is installed: pip install tiktoken\")\n