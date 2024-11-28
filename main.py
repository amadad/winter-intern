import ollama
import json
import numpy as np
from typing import List, Dict
import sys

def get_embeddings(text: str) -> List[float]:
    """Get embeddings using nomic-embed-text"""
    response = ollama.embeddings(
        model='nomic-embed-text',
        prompt=text
    )
    return response['embedding']

def cosine_similarity(a: List[float], b: List[float]) -> float:
    """Calculate cosine similarity between two vectors"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def find_relevant_context(query: str, document_chunks: Dict[str, List[str]], embeddings_cache: Dict[str, List[float]]) -> str:
    """Find most relevant document chunks using semantic search"""
    query_embedding = get_embeddings(query)
    
    # Calculate similarities
    chunk_scores = []
    for doc_name, chunks in document_chunks.items():
        for i, chunk in enumerate(chunks):
            cache_key = f"{doc_name}_{i}"
            if cache_key not in embeddings_cache:
                embeddings_cache[cache_key] = get_embeddings(chunk)
            
            similarity = cosine_similarity(query_embedding, embeddings_cache[cache_key])
            chunk_scores.append((similarity, doc_name, chunk))
    
    # Get top 3 most relevant chunks
    chunk_scores.sort(reverse=True)
    relevant_chunks = chunk_scores[:3]
    
    # Format context
    context = ""
    for _, doc_name, chunk in relevant_chunks:
        context += f"\n{doc_name}:\n{chunk}\n"
    
    return context

def chunk_document(text: str, chunk_size: int = 2000, overlap: int = 200) -> List[str]:
    """Split document into overlapping chunks"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    return chunks

def analyze_documents_stream(query: str, context: str):
    """Analyze documents using Ollama qwq model with streaming"""
    prompt = f"""You are an AI assistant helping SCTY analyze legal documents and generate responses.
Focus on protecting SCTY's interests while maintaining a professional and collaborative relationship.
RESPOND IN ENGLISH ONLY.

Context: {context}

Question: {query}

Please provide a detailed analysis and suggested response that:
1. Identifies key issues and concerns
2. Suggests specific changes or compromises
3. Maintains a constructive tone
4. Protects SCTY's interests
5. Considers the relationship between SCTY, TalentOpinion, and Barbarian Group

Format your response in clear sections:
- Key Issues
- Proposed Changes
- Recommendations"""

    stream = ollama.chat(
        model='qwq',
        messages=[{'role': 'user', 'content': prompt}],
        stream=True
    )

    for chunk in stream:
        content = chunk['message']['content']
        print(content, end='', flush=True)
    print()  # New line after response

# Read document contents
def read_file_content(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()

# Load documents
docs = {
    'MSA': read_file_content('doc/msa.md'),
    'SOW': read_file_content('doc/sow.md'),
    'BAR': read_file_content('doc/bar.md'),
    'RESPONSE': read_file_content('doc/response.md')
}

# Main analysis queries
queries = [
    "Analyze the key differences between SCTY's requirements and TalentOpinion's proposed terms in the MSA and SOW",
    "How should we structure the payment terms to align with both Barbarian's Net 30 requirement and maintain healthy cash flow?",
    "What specific changes are needed in the IP rights section to protect SCTY's obligations to Barbarian?",
    "Draft a concise response to TalentOpinion that addresses their MSA vs SOW distinction while protecting SCTY's interests"
]

# Generate analysis and responses
print("Document Analysis and Response Generation\n")
print("=" * 80)

for query in queries:
    print(f"\nQuery: {query}")
    print("-" * 80)
    
    # Provide full context for analysis
    context = f"""MSA: {docs['MSA'][:2000]}
    
SOW: {docs['SOW'][:2000]}

BAR: {docs['BAR'][:2000]}

RESPONSE: {docs['RESPONSE'][:2000]}"""
    
    print("\nAnalysis & Response:")
    analyze_documents_stream(query, context)
    print("\n" + "=" * 80)