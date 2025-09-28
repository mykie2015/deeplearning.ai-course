#!/usr/bin/env python3
"""
Test script to verify the course environment is properly set up
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_imports():
    """Test that all key packages can be imported"""
    try:
        print("Testing imports...")
        
        # Core langchain imports
        from langchain_openai import ChatOpenAI
        from langchain_community import __version__ as lc_community_version
        from langchain_experimental import __version__ as lc_experimental_version
        print(f"✅ LangChain Community: {lc_community_version}")
        print(f"✅ LangChain Experimental: {lc_experimental_version}")
        
        # LangGraph
        from langgraph.graph import StateGraph
        try:
            from langgraph import __version__ as lg_version
            print(f"✅ LangGraph: {lg_version}")
        except ImportError:
            print("✅ LangGraph: (version import not available, but core functionality works)")
        
        # Tavily (will work if API key is provided)
        from langchain_tavily import TavilySearch
        print("✅ Tavily Search")
        
        # Snowflake
        from snowflake.core import Root
        print("✅ Snowflake Core")
        
        # TruLens
        from trulens.core import Feedback
        from trulens.providers.openai import OpenAI
        print("✅ TruLens")
        
        # Matplotlib
        import matplotlib
        print(f"✅ Matplotlib: {matplotlib.__version__}")
        
        print("\n🎉 All imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_openai_config():
    """Test OpenAI configuration"""
    print("\nTesting OpenAI configuration...")
    
    api_key = os.getenv('OPENAI_API_KEY')
    base_url = os.getenv('OPENAI_BASE_URL')
    
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment")
        return False
    
    if not base_url:
        print("⚠️  OPENAI_BASE_URL not set (using default)")
    else:
        print(f"✅ OPENAI_BASE_URL: {base_url}")
    
    print(f"✅ OPENAI_API_KEY: {api_key[:10]}...{api_key[-4:] if len(api_key) > 14 else '[short]'}")
    
    try:
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(
            api_key=api_key,
            base_url=base_url,
            model="gpt-3.5-turbo",
            temperature=0
        )
        print("✅ OpenAI client created successfully")
        return True
    except Exception as e:
        print(f"❌ Error creating OpenAI client: {e}")
        return False

def test_course_files():
    """Test that course files are accessible"""
    print("\nTesting course files...")
    
    files_to_check = [
        "helper.py",
        "prompts.py", 
        "requirements.txt",
        ".env"
    ]
    
    all_good = True
    for file in files_to_check:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} not found")
            all_good = False
    
    # Check lesson directories
    lesson_dirs = ["L2", "L3", "L4", "L5", "L6"]
    for lesson in lesson_dirs:
        if os.path.exists(lesson):
            print(f"✅ {lesson}/")
        else:
            print(f"❌ {lesson}/ not found")
            all_good = False
    
    return all_good

def main():
    print("🧪 Building and Evaluating Data Agents - Environment Test")
    print("=" * 60)
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    print("=" * 60)
    
    tests = [
        ("Package Imports", test_imports),
        ("OpenAI Configuration", test_openai_config), 
        ("Course Files", test_course_files)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 40)
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All tests passed! Your environment is ready for the course.")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
    
    print(f"\nTo get started:")
    print(f"1. Activate the virtual environment: source /Users/mykielee/GitHub/deeplearning.ai-course/.venv/bin/activate")
    print(f"2. Add your Tavily API key to .env files (for web search functionality)")  
    print(f"3. Add Snowflake credentials to .env files (for enterprise data features in L3+)")
    print(f"4. Start with lesson 2: cd L2 && jupyter lab L2.ipynb")

if __name__ == "__main__":
    main()