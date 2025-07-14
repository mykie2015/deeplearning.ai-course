#!/usr/bin/env python3
"""
Script to restore Neo4j database dumps for the Knowledge Graphs for RAG course
This helps restore the database data from dump files
"""

import os
import subprocess
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv('../.env', override=True)
NEO4J_URI = os.getenv('NEO4J_URI')
NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')
NEO4J_DATABASE = os.getenv('NEO4J_DATABASE') or 'neo4j'

def restore_neo4j_dump(dump_file_path):
    """
    Restore Neo4j database from dump file using neo4j-admin load command
    """
    if not os.path.exists(dump_file_path):
        print(f"❌ Dump file not found: {dump_file_path}")
        return False
    
    print(f"Restoring Neo4j dump from: {dump_file_path}")
    
    try:
        # Stop neo4j service
        print("Stopping Neo4j service...")
        subprocess.run([
            "docker", "exec", "graphiti-mcp-setup-neo4j-1", 
            "neo4j", "stop"
        ], check=True, capture_output=True)
        
        # Copy dump file to container
        print("Copying dump file to container...")
        subprocess.run([
            "docker", "cp", 
            dump_file_path,
            f"graphiti-mcp-setup-neo4j-1:/var/lib/neo4j/dumps/{NEO4J_DATABASE}.dump"
        ], check=True)
        
        # Drop existing database
        print("Dropping existing database...")
        subprocess.run([
            "docker", "exec", "graphiti-mcp-setup-neo4j-1",
            "neo4j-admin", "database", "drop", 
            "--database", NEO4J_DATABASE
        ], check=True, capture_output=True)
        
        # Load dump
        print("Loading dump...")
        subprocess.run([
            "docker", "exec", "graphiti-mcp-setup-neo4j-1",
            "neo4j-admin", "database", "load", 
            "--database", NEO4J_DATABASE,
            "--from-path", "/var/lib/neo4j/dumps/"
        ], check=True, capture_output=True)
        
        # Start neo4j service
        print("Starting Neo4j service...")
        subprocess.run([
            "docker", "exec", "graphiti-mcp-setup-neo4j-1", 
            "neo4j", "start"
        ], check=True, capture_output=True)
        
        # Wait for service to be ready
        print("Waiting for Neo4j to be ready...")
        import time
        time.sleep(10)
        
        print(f"✅ Neo4j dump restored successfully from: {dump_file_path}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error restoring dump: {e}")
        print(f"Output: {e.stdout if e.stdout else 'No output'}")
        print(f"Error: {e.stderr if e.stderr else 'No error details'}")
        
        # Try to restart neo4j if it failed
        try:
            subprocess.run([
                "docker", "exec", "graphiti-mcp-setup-neo4j-1", 
                "neo4j", "start"
            ], check=True, capture_output=True)
        except:
            pass
        
        return False

def restore_cypher_export(export_file_path):
    """
    Alternative method: Restore data from Cypher export file
    """
    try:
        from langchain_community.graphs import Neo4jGraph
        
        if not os.path.exists(export_file_path):
            print(f"❌ Export file not found: {export_file_path}")
            return False
        
        print(f"Restoring from Cypher export: {export_file_path}")
        
        # Connect to Neo4j
        kg = Neo4jGraph(
            url=NEO4J_URI, 
            username=NEO4J_USERNAME, 
            password=NEO4J_PASSWORD, 
            database=NEO4J_DATABASE
        )
        
        # Clear existing data
        print("Clearing existing data...")
        kg.query("MATCH (n) DETACH DELETE n")
        
        # Read and execute Cypher commands
        with open(export_file_path, 'r') as f:
            lines = f.readlines()
        
        cypher_commands = []
        current_command = ""
        
        for line in lines:
            line = line.strip()
            if line.startswith("//") or not line:
                continue
            
            current_command += line + " "
            if line.endswith(";"):
                cypher_commands.append(current_command.strip())
                current_command = ""
        
        print(f"Executing {len(cypher_commands)} Cypher commands...")
        for i, command in enumerate(cypher_commands):
            try:
                kg.query(command)
                if (i + 1) % 10 == 0:
                    print(f"Executed {i + 1}/{len(cypher_commands)} commands")
            except Exception as e:
                print(f"Warning: Failed to execute command {i+1}: {e}")
        
        print(f"✅ Cypher export restored successfully from: {export_file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error restoring Cypher export: {e}")
        return False

def clear_database():
    """
    Clear all data from the Neo4j database
    """
    try:
        from langchain_community.graphs import Neo4jGraph
        
        print("Clearing all data from Neo4j database...")
        
        kg = Neo4jGraph(
            url=NEO4J_URI, 
            username=NEO4J_USERNAME, 
            password=NEO4J_PASSWORD, 
            database=NEO4J_DATABASE
        )
        
        # Clear all nodes and relationships
        kg.query("MATCH (n) DETACH DELETE n")
        
        # Clear all indexes
        indexes = kg.query("SHOW INDEXES")
        for index in indexes:
            index_name = index.get('name')
            if index_name:
                try:
                    kg.query(f"DROP INDEX {index_name}")
                except:
                    pass
        
        print("✅ Database cleared successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error clearing database: {e}")
        return False

def main():
    """
    Main function to restore Neo4j dumps
    """
    print("Neo4j Database Restore Tool")
    print("=" * 40)
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python restore_neo4j_dump.py <dump_file_path>")
        print("  python restore_neo4j_dump.py clear")
        print("  python restore_neo4j_dump.py 23001  # Restore from lesson folder")
        print()
        print("Examples:")
        print("  python restore_neo4j_dump.py neo4j.dump")
        print("  python restore_neo4j_dump.py 23001/neo4j.dump")
        print("  python restore_neo4j_dump.py 23001")
        print("  python restore_neo4j_dump.py clear")
        sys.exit(1)
    
    target = sys.argv[1]
    
    if target == "clear":
        success = clear_database()
    elif os.path.isdir(target):
        # Restore from lesson folder
        dump_file = os.path.join(target, "neo4j.dump")
        if os.path.exists(dump_file):
            success = restore_neo4j_dump(dump_file)
        else:
            export_file = os.path.join(target, "neo4j_export.cypher")
            if os.path.exists(export_file):
                success = restore_cypher_export(export_file)
            else:
                print(f"❌ No dump or export file found in {target}")
                sys.exit(1)
    else:
        # Restore from specific file
        if target.endswith('.dump'):
            success = restore_neo4j_dump(target)
        elif target.endswith('.cypher'):
            success = restore_cypher_export(target)
        else:
            print(f"❌ Unknown file type: {target}")
            sys.exit(1)
    
    if success:
        print("\n✅ Database restore completed successfully!")
    else:
        print("\n❌ Failed to restore database")
        sys.exit(1)

if __name__ == "__main__":
    main() 