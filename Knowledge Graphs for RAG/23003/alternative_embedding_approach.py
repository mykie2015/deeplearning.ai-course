#!/usr/bin/env python3
"""
Alternative approach to handle embeddings without Neo4j GenAI plugin
This replaces the genai.vector.encode() function calls with LangChain OpenAI embeddings
"""

import os
from dotenv import load_dotenv
from langchain_community.graphs import Neo4jGraph
from langchain_openai import OpenAIEmbeddings
from typing import List

# Load environment variables
load_dotenv('../.env', override=True)
NEO4J_URI = os.getenv('NEO4J_URI')
NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')
NEO4J_DATABASE = os.getenv('NEO4J_DATABASE') or 'neo4j'
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_BASE_URL = os.getenv('OPENAI_API_BASE') or os.getenv('OPENAI_BASE_URL')

# Initialize connections
kg = Neo4jGraph(
    url=NEO4J_URI, 
    username=NEO4J_USERNAME, 
    password=NEO4J_PASSWORD, 
    database=NEO4J_DATABASE
)

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",  # or "text-embedding-ada-002"
    base_url=OPENAI_BASE_URL
)

def compute_and_store_chunk_embeddings():
    """
    Alternative to the genai.vector.encode() approach
    This function computes embeddings using LangChain and stores them in Neo4j
    """
    print("Computing embeddings for chunks without textEmbedding...")
    
    # Get all chunks without embeddings
    chunks_query = """
        MATCH (chunk:Chunk) 
        WHERE chunk.textEmbedding IS NULL 
        RETURN chunk.text as text, elementId(chunk) as id
    """
    
    chunks = kg.query(chunks_query)
    
    if not chunks:
        print("No chunks found without embeddings!")
        return
    
    print(f"Found {len(chunks)} chunks to process")
    
    # Process chunks in batches to avoid API rate limits
    batch_size = 10
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        
        # Extract texts for batch processing
        texts = [chunk['text'] for chunk in batch]
        
        # Compute embeddings for the batch
        try:
            batch_embeddings = embeddings.embed_documents(texts)
            
            # Store each embedding back to Neo4j
            for j, embedding in enumerate(batch_embeddings):
                chunk_id = batch[j]['id']
                
                # Update the chunk with its embedding
                update_query = """
                    MATCH (chunk:Chunk) 
                    WHERE elementId(chunk) = $chunk_id
                    CALL db.create.setNodeVectorProperty(chunk, "textEmbedding", $embedding)
                """
                
                kg.query(update_query, {
                    'chunk_id': chunk_id,
                    'embedding': embedding
                })
            
            print(f"Processed batch {i//batch_size + 1}/{(len(chunks) + batch_size - 1)//batch_size}")
            
        except Exception as e:
            print(f"Error processing batch {i//batch_size + 1}: {e}")
            continue
    
    print("Embedding computation completed!")

def similarity_search_alternative(question: str, top_k: int = 10):
    """
    Alternative similarity search function that uses LangChain embeddings
    instead of genai.vector.encode()
    """
    # Compute embedding for the question
    question_embedding = embeddings.embed_query(question)
    
    # Perform similarity search using the vector index
    search_query = """
        CALL db.index.vector.queryNodes('form_10k_chunks', $top_k, $question_embedding) 
        YIELD node, score
        RETURN score, node.text AS text
    """
    
    results = kg.query(search_query, {
        'question_embedding': question_embedding,
        'top_k': top_k
    })
    
    return results

def create_vector_index():
    """Create the vector index for similarity search"""
    kg.query("""
        CREATE VECTOR INDEX `form_10k_chunks` IF NOT EXISTS
        FOR (c:Chunk) ON (c.textEmbedding) 
        OPTIONS { indexConfig: {
            `vector.dimensions`: 1536,
            `vector.similarity_function`: 'cosine'    
        }}
    """)
    print("Vector index created/verified!")

if __name__ == "__main__":
    print("Starting alternative embedding approach...")
    
    # Create vector index
    create_vector_index()
    
    # Compute embeddings for chunks
    compute_and_store_chunk_embeddings()
    
    # Test similarity search
    print("\nTesting similarity search...")
    results = similarity_search_alternative("Tell me about NetApp's business")
    
    if results:
        print(f"Found {len(results)} similar chunks:")
        for i, result in enumerate(results[:3]):  # Show top 3
            print(f"{i+1}. Score: {result['score']:.4f}")
            print(f"   Text: {result['text'][:200]}...")
            print()
    else:
        print("No results found") 