"""
exercise_embeddings.py - Embeddings & Semantic Search Exercises
Week 2 Live Session - Classroom Exercises

Build practical embeddings projects with real data.
Explore semantic similarity, search, and clustering.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI
import numpy as np

# ============================================================================
# Setup
# ============================================================================

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("=" * 70)
print("EMBEDDINGS EXERCISE SUITE - Week 2 Live Session")
print("=" * 70)


# ============================================================================
# UTILITY: Cosine Similarity
# ============================================================================

def cosine_similarity(a, b):
    """Compute cosine similarity between two vectors (0 to 1)"""
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return dot_product / (norm_a * norm_b)


def create_embedding(text, model="text-embedding-3-small"):
    """Create an embedding for text using OpenAI API"""
    response = client.embeddings.create(
        model=model,
        input=text
    )
    return response.data[0].embedding


# ============================================================================
# CHALLENGE 1: Understand Embeddings Basics
# ============================================================================

def challenge_1_embedding_basics():
    """
    Challenge 1: Explore embedding properties
    
    Create embeddings for simple sentences and analyze their properties.
    """
    print("\n" + "=" * 70)
    print("CHALLENGE 1: Embedding Basics")
    print("=" * 70)
    
    texts = [
        "The cat is sleeping.",
        "A cat is resting.",
        "The dog is playing.",
        "Machine learning is powerful.",
    ]
    
    print("\nCreating embeddings for sample texts...")
    embeddings = []
    
    for text in texts:
        emb = create_embedding(text)
        embeddings.append(emb)
        print(f"✅ Embedded: {text[:40]}")
    
    # Analyze properties
    print(f"\n📊 EMBEDDING PROPERTIES:")
    print(f"  Dimension: {len(embeddings[0])} numbers")
    print(f"  First 5 values: {embeddings[0][:5]}")
    print(f"  Min value: {min(embeddings[0]):.6f}")
    print(f"  Max value: {max(embeddings[0]):.6f}")
    print(f"  Mean value: {np.mean(embeddings[0]):.6f}")
    
    # Calculate similarities
    print(f"\n🔍 SIMILARITY ANALYSIS:")
    print(f\"{'Text 1':<30} {'Text 2':<30} {'Similarity':<12}\")\n    print(\"-\" * 72)\n    \n    for i in range(len(texts)):\n        for j in range(i + 1, len(texts)):\n            sim = cosine_similarity(embeddings[i], embeddings[j])\n            text1 = texts[i][:25]\n            text2 = texts[j][:25]\n            print(f\"{text1:<30} {text2:<30} {sim:.4f}\")\n    \n    print(\"\"\"\n    📊 OBSERVATIONS:\n    - Similar texts (cat sentences) should have similarity > 0.8\n    - Different topics (cats vs ML) should have similarity < 0.5\n    - Cosine similarity ranges from -1 (opposite) to +1 (identical)\n    \"\"\")\n\n\n# ============================================================================\n# CHALLENGE 2: Semantic Search Engine\n# ============================================================================\n\ndef challenge_2_semantic_search():\n    \"\"\"\n    Challenge 2: Build a mini semantic search engine\n    \n    Given a query, find the most similar documents from a corpus.\n    \"\"\"\n    print(\"\\n\" + \"=\" * 70)\n    print(\"CHALLENGE 2: Semantic Search Engine\")\n    print(\"=\" * 70)\n    \n    # Document corpus\n    documents = [\n        \"Python is a popular programming language for data science.\",\n        \"Machine learning uses algorithms to learn from data.\",\n        \"Artificial intelligence is transforming many industries.\",\n        \"Deep learning requires large amounts of computational power.\",\n        \"Natural language processing enables computers to understand text.\",\n        \"Data visualization helps communicate insights from data.\",\n        \"Neural networks are inspired by biological brain structures.\",\n        \"Python libraries like pandas and numpy are essential for data work.\",\n        \"Cloud computing provides scalable infrastructure for AI projects.\",\n        \"Transfer learning allows reusing pre-trained models.\",\n    ]\n    \n    # Create embeddings\n    print(\"\\nEmbedding documents...\")\n    doc_embeddings = []\n    for doc in documents:\n        emb = create_embedding(doc)\n        doc_embeddings.append(emb)\n    print(f\"✅ {len(documents)} documents embedded\")\n    \n    # Search queries\n    queries = [\n        \"How do machines learn from data?\",\n        \"What is Python used for?\",\n        \"Tell me about neural networks.\",\n    ]\n    \n    print(\"\\n🔍 SEMANTIC SEARCH RESULTS:\\n\")\n    \n    for query in queries:\n        print(f\"\\nQuery: '{query}'\")\n        print(\"-\" * 70)\n        \n        # Embed query\n        query_embedding = create_embedding(query)\n        \n        # Calculate similarities\n        similarities = [\n            cosine_similarity(query_embedding, doc_emb)\n            for doc_emb in doc_embeddings\n        ]\n        \n        # Sort by similarity\n        ranked = sorted(\n            zip(documents, similarities),\n            key=lambda x: x[1],\n            reverse=True\n        )\n        \n        # Show top 3 results\n        print(\"\\nTop 3 results:\")\n        for i, (doc, sim) in enumerate(ranked[:3], 1):\n            print(f\"{i}. [{sim:.4f}] {doc}\")\n    \n    print(\"\"\"\n    \\n📊 HOW IT WORKS:\n    1. Convert query to embedding vector\n    2. Calculate similarity between query and each document\n    3. Sort documents by similarity score\n    4. Return top-N most similar documents\n    \n    This is the core of RAG (Retrieval-Augmented Generation)!\n    \"\"\")\n\n\n# ============================================================================\n# CHALLENGE 3: Find Similar Items from CSV\n# ============================================================================\n\ndef challenge_3_similarity_clustering():\n    \"\"\"\n    Challenge 3: Group similar documents using embeddings\n    \n    Identify which documents are \"neighbors\" in embedding space.\n    \"\"\"\n    print(\"\\n\" + \"=\" * 70)\n    print(\"CHALLENGE 3: Document Clustering & Neighborhoods\")\n    print(\"=\" * 70)\n    \n    # Sample documents\n    documents = {\n        \"doc1\": \"Python tutorial for beginners\",\n        \"doc2\": \"Getting started with Python\",\n        \"doc3\": \"Advanced Java programming\",\n        \"doc4\": \"Introduction to C++ for developers\",\n        \"doc5\": \"Python best practices and design patterns\",\n        \"doc6\": \"Database design and optimization\",\n    }\n    \n    print(\"\\nEmbedding documents...\")\n    doc_embeddings = {}\n    for doc_id, text in documents.items():\n        emb = create_embedding(text)\n        doc_embeddings[doc_id] = emb\n    print(f\"✅ {len(documents)} documents embedded\")\n    \n    # Find neighbors for each document\n    print(\"\\n🔗 DOCUMENT NEIGHBORS (Most Similar Documents):\\n\")\n    \n    for doc_id, doc_text in documents.items():\n        print(f\"\\nDocument: {doc_id} - '{doc_text}'\")\n        print(\"-\" * 60)\n        \n        # Calculate similarities to all other documents\n        similarities = {}\n        for other_id, other_emb in doc_embeddings.items():\n            if other_id != doc_id:\n                sim = cosine_similarity(\n                    doc_embeddings[doc_id],\n                    other_emb\n                )\n                similarities[other_id] = sim\n        \n        # Sort by similarity\n        ranked = sorted(\n            similarities.items(),\n            key=lambda x: x[1],\n            reverse=True\n        )\n        \n        # Show neighbors\n        print(\"Most similar documents:\")\n        for other_id, sim in ranked[:2]:\n            print(f\"  {other_id} ({sim:.4f}): {documents[other_id]}\")\n    \n    print(\"\"\"\n    \\n📊 CLUSTERING INSIGHT:\n    - Python docs (1,2,5) cluster together\n    - Other languages (3,4) form separate cluster\n    - Database (6) is isolated\n    \n    This grouping happens automatically in embedding space!\n    \"\"\")\n\n\n# ============================================================================\n# CHALLENGE 4: Duplicate Detection\n# ============================================================================\n\ndef challenge_4_duplicate_detection():\n    \"\"\"\n    Challenge 4: Find duplicate or near-duplicate content\n    \n    High similarity = likely duplicates or paraphrases.\n    \"\"\"\n    print(\"\\n\" + \"=\" * 70)\n    print(\"CHALLENGE 4: Duplicate Content Detection\")\n    print(\"=\" * 70)\n    \n    texts = [\n        \"Machine learning is a subset of artificial intelligence.\",\n        \"ML is a branch of AI that focuses on learning from data.\",  # paraphrase\n        \"Neural networks are inspired by the human brain.\",\n        \"Biological brains inspire the design of neural networks.\",  # paraphrase\n        \"Python is a programming language.\",\n        \"Data science uses statistics and programming.\",\n        \"Statistical analysis combined with coding is data science.\",  # paraphrase\n    ]\n    \n    print(\"\\nEmbedding texts...\")\n    embeddings = [create_embedding(text) for text in texts]\n    print(f\"✅ {len(texts)} texts embedded\")\n    \n    # Find potential duplicates (similarity > 0.85)\n    print(\"\\n🔎 POTENTIAL DUPLICATES (Similarity > 0.85):\\n\")\n    \n    duplicates_found = False\n    for i in range(len(texts)):\n        for j in range(i + 1, len(texts)):\n            sim = cosine_similarity(embeddings[i], embeddings[j])\n            \n            if sim > 0.85:\n                duplicates_found = True\n                print(f\"\\n⚠️ Possible duplicate:\")\n                print(f\"  Text 1: '{texts[i]}'\")\n                print(f\"  Text 2: '{texts[j]}'\")\n                print(f\"  Similarity: {sim:.4f}\")\n    \n    if not duplicates_found:\n        print(\"No near-duplicates found (good content diversity!)\")\n    \n    print(\"\"\"\n    \\n💡 USE CASES:\n    - Plagiarism detection\n    - Content deduplication\n    - Finding similar support tickets\n    - Detecting duplicate questions in Q&A forums\n    \n    Threshold (0.85) can be adjusted based on your use case.\n    \"\"\")\n\n\n# ============================================================================\n# CHALLENGE 5: Recommendation System\n# ============================================================================\n\ndef challenge_5_recommendation_system():\n    \"\"\"\n    Challenge 5: Build a simple recommendation engine\n    \n    \"If you liked this, you might also like...\"\n    \"\"\"\n    print(\"\\n\" + \"=\" * 70)\n    print(\"CHALLENGE 5: Content Recommendation System\")\n    print(\"=\" * 70)\n    \n    # Sample content items\n    content = {\n        \"article1\": \"How to Learn Python for Data Science\",\n        \"article2\": \"Advanced NumPy Techniques\",\n        \"article3\": \"Pandas DataFrame Guide\",\n        \"article4\": \"Machine Learning with Scikit-Learn\",\n        \"article5\": \"Web Development with Django\",\n        \"article6\": \"Flask REST API Tutorial\",\n        \"article7\": \"Deep Learning Basics\",\n    }\n    \n    print(\"\\nEmbedding content...\")\n    embeddings = {}\n    for item_id, title in content.items():\n        emb = create_embedding(title)\n        embeddings[item_id] = emb\n    print(f\"✅ {len(content)} content items embedded\")\n    \n    # Recommend content\n    print(\"\\n🎯 RECOMMENDATIONS:\\n\")\n    \n    liked_articles = [\"article1\", \"article4\"]  # User liked these\n    \n    for liked_id in liked_articles:\n        print(f\"\\nUser liked: '{content[liked_id]}'\")\n        print(\"-\" * 60)\n        \n        # Find similar articles\n        similarities = {}\n        for other_id, other_emb in embeddings.items():\n            if other_id not in liked_articles:\n                sim = cosine_similarity(\n                    embeddings[liked_id],\n                    other_emb\n                )\n                similarities[other_id] = sim\n        \n        # Get top recommendations\n        recommendations = sorted(\n            similarities.items(),\n            key=lambda x: x[1],\n            reverse=True\n        )[:2]\n        \n        print(\"\\nRecommended content:\")\n        for rec_id, sim in recommendations:\n            print(f\"  • {content[rec_id]} (similarity: {sim:.4f})\")\n    \n    print(\"\"\"\n    \\n📊 RECOMMENDATION ALGORITHM:\n    1. Get embedding of liked content\n    2. Compare to all other content embeddings\n    3. Rank by similarity\n    4. Recommend top-N similar items\n    \n    Real systems combine multiple signals:\n    - Content similarity (embeddings)\n    - User ratings\n    - Collaborative filtering\n    - Popularity\n    \"\"\")\n\n\n# ============================================================================\n# CHALLENGE 6: Cost Analysis\n# ============================================================================\n\ndef challenge_6_embeddings_cost_analysis():\n    \"\"\"\n    Challenge 6: Understand embedding API costs\n    \n    Embeddings are much cheaper than Chat API!\n    \"\"\"\n    print(\"\\n\" + \"=\" * 70)\n    print(\"CHALLENGE 6: Embeddings Cost Analysis\")\n    print(\"=\" * 70)\n    \n    sample_doc = \"\"\"  \n    Machine learning is a subset of artificial intelligence that enables\n    computer systems to learn and improve from experience without explicit\n    programming. It focuses on developing algorithms and statistical models\n    that allow computers to identify patterns in data and make predictions\n    or decisions based on those patterns.\n    \"\"\"\n    \n    # Count tokens (approximate)\n    token_count = len(sample_doc.split()) * 1.3  # rough estimate\n    \n    print(f\"\\n📝 SAMPLE DOCUMENT:\")\n    print(f\"  Characters: {len(sample_doc)}\")\n    print(f\"  Words (approx): {len(sample_doc.split())}\")\n    print(f\"  Tokens (approx): {int(token_count)}\")\n    \n    # Pricing comparison\n    print(f\"\\n💰 PRICING COMPARISON (per 1 document):\\n\")\n    \n    models = {\n        \"text-embedding-3-small\": 0.02 / 1000,\n        \"text-embedding-3-large\": 0.13 / 1000,\n        \"Chat API (gpt-3.5-turbo)\": (0.0005 + 0.0015) / 1000,  # Input + output\n    }\n    \n    for model, rate_per_token in models.items():\n        cost = token_count * rate_per_token\n        print(f\"{model:<40} ${cost:.6f}\")\n    \n    # Volume calculations\n    print(f\"\\n📊 SCALE TO LARGE VOLUMES:\\n\")\n    volumes = [1000, 10000, 100000, 1000000]\n    \n    for volume in volumes:\n        cost_embeddings = (token_count * volume) * (0.02 / 1000)\n        cost_chat = (token_count * volume) * (0.002 / 1000)  # simplified\n        \n        print(f\"{volume:>10} documents:\")\n        print(f\"  Embeddings: ${cost_embeddings:>8.2f}\")\n        print(f\"  Chat API:   ${cost_chat:>8.2f} (approx)\")\n        print()\n    \n    print(\"\"\"\n    \\n✅ KEY INSIGHT:\n    Embeddings are 10-100x CHEAPER than Chat API!\n    \n    This makes embeddings ideal for:\n    - Semantic search\n    - Clustering\n    - Recommendations  \n    - Duplicate detection\n    \n    Combined with Chat API in RAG:\n    1. Use embeddings for search (cheap)\n    2. Use Chat API only on relevant docs (expensive but fast)\n    = Lower total cost!\n    \"\"\")\n\n\n# ============================================================================\n# RUN ALL CHALLENGES\n# ============================================================================\n\nif __name__ == \"__main__\":\n    try:\n        challenge_1_embedding_basics()\n        challenge_2_semantic_search()\n        challenge_3_similarity_clustering()\n        challenge_4_duplicate_detection()\n        challenge_5_recommendation_system()\n        challenge_6_embeddings_cost_analysis()\n        \n        print(\"\\n\" + \"=\" * 70)\n        print(\"✅ ALL EMBEDDING EXERCISES COMPLETED!\")\n        print(\"=\" * 70)\n        print(\"\"\"\n        You've learned:\n        1. How embeddings represent meaning as vectors\n        2. How to find similar documents\n        3. How to build semantic search and recommendations\n        4. How to detect duplicates\n        5. Why embeddings are cost-effective\n        \n        Next: Integrate embeddings into RAG systems!\n        \"\"\")\n        \n    except Exception as e:\n        print(f\"\\n❌ Error: {e}\")\n        print(\"\\nTroubleshooting:\")\n        print(\"1. Check API key in .env file\")\n        print(\"2. Verify OpenAI Python library is installed\")\n        print(\"3. Check internet connection\")\n