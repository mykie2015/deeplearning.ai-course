#!/usr/bin/env python3
"""
Script to populate Neo4j database with Knowledge Graphs for RAG course structure
"""

from neo4j import GraphDatabase

class Neo4jPopulator:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self.driver.close()
    
    def clear_database(self):
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            print("Database cleared.")
    
    def create_course_structure(self):
        with self.driver.session() as session:
            # Create main course node
            session.run("""
                CREATE (course:Course {
                    name: 'Knowledge Graphs for RAG Course',
                    description: 'A comprehensive course on building Knowledge Graphs for Retrieval-Augmented Generation',
                    technology: 'Neo4j',
                    framework: 'LangChain',
                    data_source: 'SEC Form 10-K documents'
                })
            """)
            
            # Create technology nodes
            session.run("""
                CREATE (neo4j:Technology {
                    name: 'Neo4j Graph Database',
                    type: 'Graph Database',
                    query_language: 'Cypher',
                    capabilities: ['vector indexing', 'graph relationships', 'ACID compliance']
                })
            """)
            
            session.run("""
                CREATE (langchain:Framework {
                    name: 'LangChain Integration',
                    type: 'AI Framework',
                    classes: ['Neo4jGraph', 'Neo4jVector', 'RetrievalQAWithSourcesChain', 'GraphCypherQAChain'],
                    purpose: 'AI workflow integration'
                })
            """)
            
            session.run("""
                CREATE (openai:APIService {
                    name: 'OpenAI Integration',
                    type: 'AI API',
                    services: ['OpenAIEmbeddings', 'ChatOpenAI'],
                    purpose: 'Text vectorization and language model interactions'
                })
            """)
            
            # Create lesson nodes
            lessons = [
                {
                    'id': 'L2',
                    'name': 'Query with Cypher',
                    'file': '23001/L2-query_with_cypher.ipynb',
                    'focus': 'Introduction to querying Knowledge Graphs using Cypher',
                    'topics': ['Neo4j connection', 'Cypher syntax', 'basic graph operations']
                },
                {
                    'id': 'L3',
                    'name': 'Prep Text for RAG',
                    'file': '23002/L3-prep_text_for_RAG.ipynb',
                    'focus': 'Text preprocessing and chunking strategies',
                    'topics': ['text preprocessing', 'OpenAI embeddings', 'RAG foundation']
                },
                {
                    'id': 'L4',
                    'name': 'Construct KG from Text',
                    'file': '23003/L4-construct_kg_from_text.ipynb',
                    'focus': 'Core lesson on building knowledge graphs from text documents',
                    'topics': ['RecursiveCharacterTextSplitter', 'vector indexing', 'form_10k_chunks']
                },
                {
                    'id': 'L5',
                    'name': 'Add Relationships to KG',
                    'file': '23004/L5-add_relationships_to_kg.ipynb',
                    'focus': 'Relationship extraction and enhancement',
                    'topics': ['relationship discovery', 'graph connectivity', 'semantic richness']
                },
                {
                    'id': 'L6',
                    'name': 'Expand the KG',
                    'file': '23005/L6-expand_the_kg.ipynb',
                    'focus': 'Graph expansion with additional data sources',
                    'topics': ['form13.csv integration', 'graph expansion techniques', 'data enrichment']
                },
                {
                    'id': 'L7',
                    'name': 'Chat with KG',
                    'file': '23006/L7-chat_with_kg.ipynb',
                    'focus': 'Conversational interface implementation',
                    'topics': ['GraphCypherQAChain', 'natural language querying', 'end-to-end RAG']
                }
            ]
            
            for lesson in lessons:
                session.run("""
                    CREATE (lesson:Lesson {
                        id: $id,
                        name: $name,
                        file: $file,
                        focus: $focus,
                        topics: $topics
                    })
                """, lesson)
            
            # Create data source nodes
            session.run("""
                CREATE (form10k:DataSource {
                    name: 'SEC Form 10-K Data',
                    type: 'Primary Data Source',
                    format: 'JSON',
                    file: '0000950170-23-027948.json',
                    content: 'Financial and business information',
                    size: '470KB'
                })
            """)
            
            session.run("""
                CREATE (form13:DataSource {
                    name: 'Form 13 CSV Data',
                    type: 'Secondary Data Source',
                    format: 'CSV',
                    file: 'form13.csv',
                    content: 'Institutional holdings data',
                    size: '118KB'
                })
            """)
            
            print("All nodes created successfully!")
    
    def create_relationships(self):
        with self.driver.session() as session:
            # Course uses technologies
            session.run("""
                MATCH (course:Course {name: 'Knowledge Graphs for RAG Course'})
                MATCH (neo4j:Technology {name: 'Neo4j Graph Database'})
                CREATE (course)-[:USES]->(neo4j)
            """)
            
            session.run("""
                MATCH (course:Course {name: 'Knowledge Graphs for RAG Course'})
                MATCH (langchain:Framework {name: 'LangChain Integration'})
                CREATE (course)-[:LEVERAGES]->(langchain)
            """)
            
            session.run("""
                MATCH (course:Course {name: 'Knowledge Graphs for RAG Course'})
                MATCH (openai:APIService {name: 'OpenAI Integration'})
                CREATE (course)-[:INTEGRATES_WITH]->(openai)
            """)
            
            # Lessons belong to course
            lesson_ids = ['L2', 'L3', 'L4', 'L5', 'L6', 'L7']
            for lesson_id in lesson_ids:
                session.run("""
                    MATCH (course:Course {name: 'Knowledge Graphs for RAG Course'})
                    MATCH (lesson:Lesson {id: $lesson_id})
                    CREATE (lesson)-[:BELONGS_TO]->(course)
                """, lesson_id=lesson_id)
            
            # Sequential lesson relationships
            lesson_pairs = [('L2', 'L3'), ('L3', 'L4'), ('L4', 'L5'), ('L5', 'L6'), ('L6', 'L7')]
            for prev, next_lesson in lesson_pairs:
                session.run("""
                    MATCH (prev:Lesson {id: $prev})
                    MATCH (next:Lesson {id: $next})
                    CREATE (prev)-[:PRECEDES]->(next)
                """, prev=prev, next=next_lesson)
            
            # Technology integration relationships
            session.run("""
                MATCH (neo4j:Technology {name: 'Neo4j Graph Database'})
                MATCH (langchain:Framework {name: 'LangChain Integration'})
                CREATE (neo4j)-[:INTEGRATES_WITH]->(langchain)
            """)
            
            session.run("""
                MATCH (langchain:Framework {name: 'LangChain Integration'})
                MATCH (openai:APIService {name: 'OpenAI Integration'})
                CREATE (langchain)-[:CONNECTS_TO]->(openai)
            """)
            
            print("All relationships created successfully!")
    
    def verify_population(self):
        with self.driver.session() as session:
            # Count nodes by type
            result = session.run("""
                MATCH (n)
                RETURN labels(n) as node_type, count(n) as count
                ORDER BY count DESC
            """)
            
            print("\n=== Node Summary ===")
            for record in result:
                print(f"{record['node_type']}: {record['count']}")
            
            # Count relationships by type
            result = session.run("""
                MATCH ()-[r]->()
                RETURN type(r) as relationship_type, count(r) as count
                ORDER BY count DESC
            """)
            
            print("\n=== Relationship Summary ===")
            for record in result:
                print(f"{record['relationship_type']}: {record['count']}")
            
            # Total counts
            result = session.run("MATCH (n) RETURN count(n) as total_nodes")
            total_nodes = result.single()['total_nodes']
            
            result = session.run("MATCH ()-[r]->() RETURN count(r) as total_relationships")
            total_relationships = result.single()['total_relationships']
            
            print(f"\n=== Total Summary ===")
            print(f"Total Nodes: {total_nodes}")
            print(f"Total Relationships: {total_relationships}")

def main():
    # Neo4j connection details
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "password"
    
    populator = Neo4jPopulator(uri, user, password)
    
    try:
        print("Clearing existing database...")
        populator.clear_database()
        
        print("Creating course structure...")
        populator.create_course_structure()
        
        print("Creating relationships...")
        populator.create_relationships()
        
        print("Verifying population...")
        populator.verify_population()
        
        print("\n✅ Knowledge Graphs for RAG course structure successfully populated in Neo4j!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        populator.close()

if __name__ == "__main__":
    main()
