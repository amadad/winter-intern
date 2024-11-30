import ollama
import sys
import os
import json
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple

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

def find_relevant_context(query: str, document_chunks: Dict[str, List[str]], embeddings_cache: Dict[str, List[float]], top_k: int = 3) -> str:
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
    
    # Get top k most relevant chunks
    chunk_scores.sort(reverse=True)
    relevant_chunks = chunk_scores[:top_k]
    
    # Format context
    context = ""
    for _, doc_name, chunk in relevant_chunks:
        context += f"\n{doc_name}:\n{chunk}\n"
    
    return context

def get_user_input() -> Tuple[List[str], str, List[str]]:
    """Get user input about the document analysis task"""
    print("\n=== Document Analysis Configuration ===\n")
    
    # Get entities involved
    print("Enter the entities involved (one per line, empty line to finish):")
    entities = []
    while True:
        entity = input("> ").strip()
        if not entity:
            break
        entities.append(entity)
    
    # Get objective
    print("\nWhat is the core objective of this analysis? (e.g., 'Review contract terms', 'Analyze partnership agreement')")
    objective = input("> ").strip()
    
    # Get document paths
    print("\nEnter the paths to your documents relative to doc/ (one per line, empty line to finish):")
    print("Example: contract.md")
    documents = []
    while True:
        doc = input("> ").strip()
        if not doc:
            break
        if os.path.exists(f"doc/{doc}"):
            documents.append(doc)
        else:
            print(f"Warning: doc/{doc} not found, skipping...")
    
    return entities, objective, documents

def analyze_documents_stream(query: str, context: str, entities: list, objective: str) -> str:
    """Analyze documents using Ollama qwq model with streaming"""
    entities_str = ", ".join(entities)
    prompt = f"""You are an AI assistant analyzing documents involving these entities: {entities_str}.
Core objective: {objective}

Focus on maintaining professional relationships while protecting all parties' interests.
RESPOND IN ENGLISH ONLY.

Context: {context}

Question: {query}

Please provide a detailed analysis and suggested response that:
1. Identifies key issues and concerns
2. Suggests specific changes or compromises
3. Maintains a constructive tone
4. Protects all parties' interests
5. Considers relationships between {entities_str}

Format your response in clear sections:
- Key Issues
- Proposed Changes
- Recommendations"""

    stream = ollama.chat(
        model='qwq',
        messages=[{'role': 'user', 'content': prompt}],
        stream=True
    )

    response_parts = []
    for chunk in stream:
        content = chunk['message']['content']
        response_parts.append(content)
        print(content, end='', flush=True)
    print()  # New line after response
    
    return "".join(response_parts)

def read_file_content(filename: str) -> str:
    """Read content from a file"""
    with open(filename, 'r') as f:
        return f.read()

def save_analysis(query: str, response: str, timestamp: str) -> Path:
    """Save analysis to markdown file"""
    out_dir = Path("out")
    out_dir.mkdir(exist_ok=True)
    
    filename = f"analysis_{timestamp}.md"
    filepath = out_dir / filename
    
    with open(filepath, "a") as f:
        f.write(f"\n## Query: {query}\n\n")
        f.write(response)
        f.write("\n\n---\n")
    
    return filepath

def main():
    # Get user input
    entities, objective, documents = get_user_input()
    
    if not documents:
        print("Error: No valid documents provided.")
        return
    
    # Load and chunk documents
    docs = {}
    document_chunks = {}
    for doc in documents:
        name = os.path.splitext(doc)[0].upper()
        content = read_file_content(f"doc/{doc}")
        docs[name] = content
        document_chunks[name] = chunk_document(content)
    
    # Initialize embeddings cache
    embeddings_cache = {}
    
    # Generate default queries based on objective
    default_queries = [
        f"Analyze the key differences between requirements and proposed terms in the documents",
        f"How should payment terms be structured to maintain healthy cash flow for all parties?",
        f"What specific changes are needed to protect intellectual property rights?",
        f"Draft a response addressing document structure and relationships"
    ]
    
    print("\nDefault queries will be used. Would you like to add custom queries? (y/N)")
    if input("> ").lower().strip() == 'y':
        print("\nEnter custom queries (one per line, empty line to finish):")
        while True:
            query = input("> ").strip()
            if not query:
                break
            default_queries.append(query)
    
    # Generate analysis and responses
    print("\nDocument Analysis and Response Generation\n")
    print("=" * 80)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    for query in default_queries:
        print(f"\nQuery: {query}")
        print("-" * 80)
        
        # Find relevant context using semantic search
        context = find_relevant_context(query, document_chunks, embeddings_cache)
        
        print("\nAnalysis & Response:")
        response = analyze_documents_stream(query, context, entities, objective)
        
        # Save to file
        filepath = save_analysis(query, response, timestamp)
        
        print("\n" + "=" * 80)
    
    print(f"\nAnalysis saved to: {filepath}")

if __name__ == "__main__":
    main() 