#!/usr/bin/env python3
"""
Corrected notebook code that works with your environment setup
Copy and paste these code blocks into your notebook cells
"""

# =============================================================================
# CELL 1: Import packages and setup (replaces the failing cell)
# =============================================================================

from dotenv import load_dotenv
import os

from langchain_community.graphs import Neo4jGraph
from langchain_community.vectorstores import Neo4jVector
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQAWithSourcesChain
from langchain_openai import ChatOpenAI

# Warning control
import warnings
warnings.filterwarnings("ignore")

# =============================================================================
# CELL 2: Load environment variables (corrects the endpoint issue)
# =============================================================================

load_dotenv('../.env', override=True)
NEO4J_URI = os.getenv('NEO4J_URI')
NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')
NEO4J_DATABASE = os.getenv('NEO4J_DATABASE') or 'neo4j'
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Handle both environment variable names
OPENAI_BASE_URL = os.getenv('OPENAI_API_BASE') or os.getenv('OPENAI_BASE_URL')
OPENAI_ENDPOINT = OPENAI_BASE_URL + '/embeddings' if OPENAI_BASE_URL else None

print(f"Neo4j URI: {NEO4J_URI}")
print(f"OpenAI Endpoint: {OPENAI_ENDPOINT}")

# =============================================================================
# CELL 3: Initialize connections
# =============================================================================

# Initialize Neo4j connection
kg = Neo4jGraph(
    url=NEO4J_URI, 
    username=NEO4J_USERNAME, 
    password=NEO4J_PASSWORD, 
    database=NEO4J_DATABASE
)

# Initialize OpenAI embeddings with custom endpoint
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    base_url=OPENAI_BASE_URL
)

print("✅ Connections initialized successfully!")

# =============================================================================
# CELL 4: Alternative embedding computation (replaces genai.vector.encode)
# =============================================================================

def compute_embeddings_alternative():
    """
    Alternative method to compute embeddings using LangChain instead of GenAI plugin
    """
    print("Computing embeddings using LangChain...")
    
    # Create vector index if it doesn't exist
    try:
        kg.query("""
            CREATE VECTOR INDEX form_10k_chunks IF NOT EXISTS
            FOR (c:Chunk) ON (c.textEmbedding)
            OPTIONS {
                indexConfig: {
                    `vector.dimensions`: 1536,
                    `vector.similarity_function`: 'cosine'
                }
            }
        """)
        print("✅ Vector index created/verified!")
    except Exception as e:
        print(f"Index creation info: {e}")
    
    # Get chunks without embeddings
    chunks_query = """
        MATCH (chunk:Chunk) 
        WHERE chunk.textEmbedding IS NULL
        RETURN chunk.chunkId as chunkId, chunk.text as text
        LIMIT 50
    """
    
    chunks = kg.query(chunks_query)
    print(f"Found {len(chunks)} chunks to process")
    
    if not chunks:
        print("No chunks found without embeddings")
        return
    
    # Process in batches to avoid API limits
    batch_size = 10
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i+batch_size]
        texts = [chunk['text'] for chunk in batch]
        
        # Compute embeddings for batch
        try:
            batch_embeddings = embeddings.embed_documents(texts)
            
            # Update each chunk with its embedding
            for j, chunk in enumerate(batch):
                chunk_id = chunk['chunkId']
                embedding = batch_embeddings[j]
                
                # Update chunk with embedding
                kg.query("""
                    MATCH (chunk:Chunk {chunkId: $chunkId})
                    CALL db.create.setNodeVectorProperty(chunk, "textEmbedding", $embedding)
                """, params={"chunkId": chunk_id, "embedding": embedding})
            
            print(f"Processed batch {i//batch_size + 1}/{(len(chunks) + batch_size - 1)//batch_size}")
            
        except Exception as e:
            print(f"Error processing batch: {e}")
    
    print("✅ Embedding computation completed!")

# Run the alternative embedding computation
compute_embeddings_alternative()

# =============================================================================
# CELL 5: Similarity search function (replaces genai.vector.encode queries)
# =============================================================================

def similarity_search_alternative(question, top_k=5):
    """
    Alternative similarity search using LangChain embeddings
    """
    # Compute question embedding
    question_embedding = embeddings.embed_query(question)
    
    # Search for similar chunks
    results = kg.query("""
        CALL db.index.vector.queryNodes(
            'form_10k_chunks', 
            $top_k, 
            $question_embedding
        ) YIELD node AS chunk, score
        RETURN chunk.text as text, score
        ORDER BY score DESC
    """, params={
        "question_embedding": question_embedding,
        "top_k": top_k
    })
    
    return results

# Test similarity search
question = "What is NetApp's business model?"
results = similarity_search_alternative(question)
print(f"\nSimilarity search results for: '{question}'")
for i, result in enumerate(results, 1):
    print(f"{i}. Score: {result['score']:.4f}")
    print(f"   Text: {result['text'][:200]}...")
    print()

# =============================================================================
# CELL 6: Create Neo4j dump function
# =============================================================================

def create_database_dump(lesson_folder=None):
    """
    Create a dump of the current Neo4j database
    """
    import subprocess
    from datetime import datetime
    
    if lesson_folder:
        output_path = os.path.join(lesson_folder, "neo4j.dump")
        if not os.path.exists(lesson_folder):
            os.makedirs(lesson_folder)
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"neo4j_dump_{timestamp}.dump"
    
    try:
        # Stop Neo4j service
        subprocess.run([
            "docker", "exec", "graphiti-mcp-setup-neo4j-1", 
            "neo4j", "stop"
        ], check=True, capture_output=True)
        
        # Create dump
        subprocess.run([
            "docker", "exec", "graphiti-mcp-setup-neo4j-1",
            "neo4j-admin", "database", "dump", 
            "--database", NEO4J_DATABASE,
            "--to-path", "/var/lib/neo4j/dumps/"
        ], check=True, capture_output=True)
        
        # Copy dump to host
        subprocess.run([
            "docker", "cp", 
            f"graphiti-mcp-setup-neo4j-1:/var/lib/neo4j/dumps/{NEO4J_DATABASE}.dump",
            output_path
        ], check=True)
        
        # Restart Neo4j
        subprocess.run([
            "docker", "exec", "graphiti-mcp-setup-neo4j-1", 
            "neo4j", "start"
        ], check=True, capture_output=True)
        
        print(f"✅ Database dump created: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating dump: {e}")
        return False

# Create dump for current lesson
# create_database_dump("23001")  # Uncomment to create dump

# =============================================================================
# CELL 7: Vector store setup (alternative to manual embedding)
# =============================================================================

def setup_vector_store():
    """
    Alternative approach using Neo4jVector for automatic embedding handling
    """
    try:
        # Create vector store
        vector_store = Neo4jVector.from_existing_graph(
            embedding=embeddings,
            url=NEO4J_URI,
            username=NEO4J_USERNAME,
            password=NEO4J_PASSWORD,
            database=NEO4J_DATABASE,
            index_name="form_10k_chunks",
            node_label="Chunk",
            text_node_properties=["text"],
            embedding_node_property="textEmbedding"
        )
        
        print("✅ Vector store setup completed!")
        return vector_store
    
    except Exception as e:
        print(f"Vector store setup info: {e}")
        return None

# Setup vector store
vector_store = setup_vector_store()

# Test vector store search
if vector_store:
    docs = vector_store.similarity_search("What is NetApp's business model?", k=3)
    print("\nVector store search results:")
    for i, doc in enumerate(docs, 1):
        print(f"{i}. {doc.page_content[:200]}...")

# =============================================================================
# USAGE INSTRUCTIONS
# =============================================================================

print("""
=== USAGE INSTRUCTIONS ===

1. Use compute_embeddings_alternative() instead of genai.vector.encode()
2. Use similarity_search_alternative() for similarity searches
3. Use create_database_dump() to create dumps
4. Use setup_vector_store() for automatic embedding handling

Example notebook replacements:
- Replace genai.vector.encode() calls with compute_embeddings_alternative()
- Replace similarity queries with similarity_search_alternative()
- Create dumps with create_database_dump("lesson_folder")
""") 