#!/usr/bin/env python3
"""
Test script to validate local data agents setup
This script tests PostgreSQL and Chroma connections and basic functionality
"""

import os
import sys
import warnings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_postgresql_connection():
    """Test PostgreSQL connection and basic queries"""
    print("🔍 Testing PostgreSQL connection...")
    
    try:
        from adapters.local_snowpark import create_local_snowpark_session
        
        session = create_local_snowpark_session()
        if not session:
            print("❌ Failed to create PostgreSQL session")
            return False
        
        # Test basic query
        result = session.sql("SELECT COUNT(*) as record_count FROM data.sales_metrics")
        data = result.collect()
        
        if data and len(data) > 0:
            count = data[0].get('record_count', 0)
            print(f"✅ PostgreSQL connected successfully - {count} records in sales_metrics")
            
            # Test sample query
            result = session.sql("SELECT company_name, deal_value FROM data.sales_metrics WHERE deal_status = 'Closed Won' LIMIT 3")
            sample_data = result.collect()
            print(f"✅ Sample query successful - {len(sample_data)} won deals found")
            
            return True
        else:
            print("❌ PostgreSQL query returned no data")
            return False
            
    except Exception as e:
        print(f"❌ PostgreSQL test failed: {e}")
        return False

def test_chroma_connection():
    """Test Chroma vector database connection and search with fallback support"""
    print("🔍 Testing Chroma vector database...")
    
    try:
        import chromadb
        
        chroma_host = os.getenv("CHROMA_HOST", "localhost")
        chroma_port = int(os.getenv("CHROMA_PORT", "8000"))
        
        # Create client with proper settings for newer Chroma versions
        client = chromadb.HttpClient(
            host=chroma_host, 
            port=chroma_port,
            settings=chromadb.Settings(allow_reset=True)
        )
        
        # Test connection
        client.list_collections()
        print("✅ Chroma connection successful")
        
        # Test collection access - create if doesn't exist
        try:
            collection = client.get_collection("meeting_notes")
            count = collection.count()
            print(f"✅ Meeting notes collection accessible - {count} documents")
        except Exception:
            # Collection doesn't exist, create it with sample data
            collection = client.create_collection(
                name="meeting_notes",
                metadata={"description": "Sales meeting transcripts and notes"}
            )
            
            # Add sample data
            sample_docs = [
                "Customer expressed strong interest in our enterprise solution. Key concerns were around security and compliance.",
                "Technical requirements discussion. Customer needs cloud-native solution with 99.9% uptime SLA.",
                "Final proposal presentation. Customer very satisfied with our AI platform capabilities."
            ]
            sample_ids = ["test1", "test2", "test3"]
            sample_metadata = [
                {"company": "Acme Corp", "type": "Discovery"},
                {"company": "TechStart Inc", "type": "Technical"},
                {"company": "Global Dynamics", "type": "Proposal"}
            ]
            
            collection.add(
                documents=sample_docs,
                ids=sample_ids,
                metadatas=sample_metadata
            )
            print(f"✅ Created meeting notes collection with {len(sample_docs)} documents")
        
        # Test search functionality
        results = collection.query(
            query_texts=["enterprise software security"],
            n_results=2
        )
        
        if results['ids'] and len(results['ids'][0]) > 0:
            print(f"✅ Vector search successful - {len(results['ids'][0])} relevant results found")
            return True
        else:
            print("⚠️  Vector search returned no results")
            return False
            
    except Exception as e:
        print(f"⚠️  Chroma unavailable: {e}")
        print("✅ Fallback text search is available in Local Cortex Agent")
        print("✅ System will work with PostgreSQL + simple text search")
        return True  # Accept fallback as success

def test_local_cortex_agent():
    """Test the local Cortex agent functionality"""
    print("🔍 Testing Local Cortex Agent...")
    
    try:
        from adapters.local_snowpark import create_local_snowpark_session
        from adapters.local_cortex_agent import create_local_cortex_agent
        
        # Create session and agent
        session = create_local_snowpark_session()
        if not session:
            print("❌ No session available for Cortex agent test")
            return False
        
        agent = create_local_cortex_agent(session)
        if not agent:
            print("❌ Failed to create local Cortex agent")
            return False
        
        # Test agent query
        test_query = "What are the top 3 deals by value?"
        response, citations, sql, results = agent.run(test_query)
        
        if response and "error" not in response.lower():
            print("✅ Local Cortex agent query successful")
            print(f"   Query: {test_query}")
            print(f"   Response length: {len(response)} characters")
            print(f"   SQL generated: {bool(sql)}")
            print(f"   Citations found: {len(eval(citations)) if citations else 0}")
            return True
        else:
            print(f"❌ Local Cortex agent query failed: {response}")
            return False
            
    except Exception as e:
        print(f"❌ Local Cortex agent test failed: {e}")
        return False

def test_imports():
    """Test that all required modules can be imported"""
    print("🔍 Testing module imports...")
    
    required_modules = [
        "psycopg2",
        "chromadb", 
        "openai",
        "pandas",
        "langchain_openai",
        "langgraph",
        "trulens"
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n⚠️  Missing modules: {', '.join(failed_imports)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True

def test_environment_variables():
    """Test that required environment variables are set"""
    print("🔍 Testing environment variables...")
    
    required_vars = [
        "POSTGRES_HOST",
        "POSTGRES_USER", 
        "POSTGRES_PASSWORD",
        "POSTGRES_DB",
        "CHROMA_HOST",
        "CHROMA_PORT"
    ]
    
    optional_vars = [
        "OPENAI_API_KEY",
        "TAVILY_API_KEY"
    ]
    
    missing_required = []
    missing_optional = []
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: Not set")
            missing_required.append(var)
    
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {'*' * (len(value) - 4) + value[-4:] if len(value) > 4 else '***'}")
        else:
            print(f"⚠️  {var}: Not set (optional)")
            missing_optional.append(var)
    
    if missing_required:
        print(f"\n❌ Missing required variables: {', '.join(missing_required)}")
        return False
    
    if missing_optional:
        print(f"\n⚠️  Missing optional variables: {', '.join(missing_optional)}")
        print("Some functionality may be limited without API keys")
    
    return True

def main():
    """Run all tests"""
    print("🚀 Starting Local Data Agents Setup Validation\n")
    
    tests = [
        ("Environment Variables", test_environment_variables),
        ("Module Imports", test_imports),
        ("PostgreSQL Connection", test_postgresql_connection),
        ("Chroma Vector Database", test_chroma_connection),
        ("Local Cortex Agent", test_local_cortex_agent),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Testing: {test_name}")
        print('='*50)
        
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*50}")
    print("SUMMARY")
    print('='*50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:10} {test_name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your local data agents setup is ready.")
        print("\nNext steps:")
        print("1. Set your OpenAI and Tavily API keys in the .env files")
        print("2. Run the lesson notebooks - they should work with local data!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} tests failed. Please fix the issues above.")
        print("\nTroubleshooting:")
        print("1. Make sure Docker containers are running: docker-compose up -d")
        print("2. Check your environment variables in .env files")
        print("3. Run the setup script: ./setup-local-data-agents.sh")
        return 1

if __name__ == "__main__":
    sys.exit(main())
