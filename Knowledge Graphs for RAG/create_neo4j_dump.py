#!/usr/bin/env python3
"""
Script to create Neo4j database dumps for the Knowledge Graphs for RAG course
This helps export the database data so it can be restored later
"""

import os
import subprocess
import sys
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv('../.env', override=True)
NEO4J_URI = os.getenv('NEO4J_URI')
NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')
NEO4J_DATABASE = os.getenv('NEO4J_DATABASE') or 'neo4j'

def create_neo4j_dump(output_file=None, lesson_folder=None):
    """
    Create a Neo4j database dump using neo4j-admin dump command
    """
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"neo4j_dump_{timestamp}.dump"
    
    if lesson_folder:
        output_path = os.path.join(lesson_folder, "neo4j.dump")
    else:
        output_path = output_file
    
    print(f"Creating Neo4j dump: {output_path}")
    
    # Method 1: Using docker exec with neo4j-admin dump
    try:
        # Stop neo4j service temporarily for dump
        print("Stopping Neo4j service...")
        subprocess.run([
            "docker", "exec", "graphiti-mcp-setup-neo4j-1", 
            "neo4j", "stop"
        ], check=True, capture_output=True)
        
        # Create dump
        print("Creating dump...")
        result = subprocess.run([
            "docker", "exec", "graphiti-mcp-setup-neo4j-1",
            "neo4j-admin", "database", "dump", 
            "--database", NEO4J_DATABASE,
            "--to-path", "/var/lib/neo4j/dumps/"
        ], check=True, capture_output=True, text=True)
        
        # Copy dump file from container to host
        print("Copying dump file...")
        subprocess.run([
            "docker", "cp", 
            f"graphiti-mcp-setup-neo4j-1:/var/lib/neo4j/dumps/{NEO4J_DATABASE}.dump",
            output_path
        ], check=True)
        
        # Restart neo4j service
        print("Restarting Neo4j service...")
        subprocess.run([
            "docker", "exec", "graphiti-mcp-setup-neo4j-1", 
            "neo4j", "start"
        ], check=True, capture_output=True)
        
        print(f"✅ Neo4j dump created successfully: {output_path}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating dump: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        
        # Try to restart neo4j if it failed
        try:
            subprocess.run([
                "docker", "exec", "graphiti-mcp-setup-neo4j-1", 
                "neo4j", "start"
            ], check=True, capture_output=True)
        except:
            pass
        
        return False

def create_cypher_export(output_file=None, lesson_folder=None):
    """
    Alternative method: Export data using Cypher queries
    """
    try:
        from langchain_community.graphs import Neo4jGraph
        
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"neo4j_export_{timestamp}.cypher"
        
        if lesson_folder:
            output_path = os.path.join(lesson_folder, "neo4j_export.cypher")
        else:
            output_path = output_file
        
        print(f"Creating Cypher export: {output_path}")
        
        # Connect to Neo4j
        kg = Neo4jGraph(
            url=NEO4J_URI, 
            username=NEO4J_USERNAME, 
            password=NEO4J_PASSWORD, 
            database=NEO4J_DATABASE
        )
        
        # Get all nodes and relationships
        nodes_query = """
        MATCH (n)
        RETURN n, labels(n) as labels, properties(n) as props
        """
        
        relationships_query = """
        MATCH (a)-[r]->(b)
        RETURN a, r, b, type(r) as rel_type, properties(r) as rel_props
        """
        
        with open(output_path, 'w') as f:
            f.write("// Neo4j Database Export\n")
            f.write(f"// Generated: {datetime.now().isoformat()}\n\n")
            
            # Export nodes
            f.write("// === NODES ===\n")
            nodes = kg.query(nodes_query)
            for node in nodes:
                labels = ':'.join(node['labels'])
                props = node['props']
                props_str = ', '.join([f"{k}: {repr(v)}" for k, v in props.items()])
                f.write(f"CREATE (:{labels} {{{props_str}}});\n")
            
            f.write("\n// === RELATIONSHIPS ===\n")
            rels = kg.query(relationships_query)
            for rel in rels:
                # This is a simplified export - full export would need node matching
                rel_type = rel['rel_type']
                rel_props = rel['rel_props']
                props_str = ', '.join([f"{k}: {repr(v)}" for k, v in rel_props.items()]) if rel_props else ""
                f.write(f"// Relationship: {rel_type} {{{props_str}}}\n")
        
        print(f"✅ Cypher export created successfully: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating Cypher export: {e}")
        return False

def main():
    """
    Main function to create Neo4j dumps
    """
    print("Neo4j Database Dump Creator")
    print("=" * 40)
    
    # Parse command line arguments
    lesson_folder = None
    if len(sys.argv) > 1:
        lesson_folder = sys.argv[1]
        print(f"Target lesson folder: {lesson_folder}")
        
        # Create lesson folder if it doesn't exist
        if not os.path.exists(lesson_folder):
            os.makedirs(lesson_folder)
    
    # Try to create dump using neo4j-admin
    success = create_neo4j_dump(lesson_folder=lesson_folder)
    
    if not success:
        print("\nFalling back to Cypher export method...")
        success = create_cypher_export(lesson_folder=lesson_folder)
    
    if success:
        print("\n✅ Database export completed successfully!")
    else:
        print("\n❌ Failed to create database export")
        sys.exit(1)

if __name__ == "__main__":
    main() 