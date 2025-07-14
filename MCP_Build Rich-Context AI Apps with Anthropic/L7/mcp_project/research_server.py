import arxiv
import json
import os
import logging
import secrets
from datetime import datetime
from typing import List
from mcp.server.fastmcp import FastMCP

PAPER_DIR = "papers"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs.txt'),
        logging.StreamHandler()  # Also log to console
    ]
)

logger = logging.getLogger('research_server')

def log_proxy_info():
    """
    Log proxy address and session token information to logs.txt
    """
    try:
        # Get proxy address from environment or use default
        dlai_url = os.environ.get('DLAI_LOCAL_URL', 'http://localhost:{port}/')
        proxy_address = dlai_url.format(port=6277)
        
        # Remove trailing slash if present
        if proxy_address.endswith('/'):
            proxy_address = proxy_address[:-1]
        
        # Generate or get session token
        session_token = os.environ.get('MCP_SESSION_TOKEN')
        if not session_token:
            session_token = secrets.token_hex(16)
            logger.info("Generated new session token")
        else:
            logger.info("Using existing session token from environment")
        
        # Log the proxy information
        logger.info("=== MCP PROXY CONFIGURATION ===")
        logger.info(f"Inspector Proxy Address: {proxy_address}")
        logger.info(f"Session Token: {session_token}")
        logger.info("================================")
        
        # Also log additional environment info
        logger.info("Environment Variables Check:")
        for key in ['DLAI_LOCAL_URL', 'MCP_SESSION_TOKEN', 'ANTHROPIC_API_KEY']:
            value = os.environ.get(key)
            if value:
                if 'TOKEN' in key or 'KEY' in key:
                    logger.info(f"{key}: {'*' * 8}...{value[-4:] if len(value) > 4 else '***'}")
                else:
                    logger.info(f"{key}: {value}")
            else:
                logger.info(f"{key}: Not set")
        
        return proxy_address, session_token
        
    except Exception as e:
        logger.error(f"Error logging proxy information: {str(e)}")
        return None, None

# Initialize FastMCP server
mcp = FastMCP("research")
logger.info("FastMCP research server initialized")

# Log proxy configuration at startup
proxy_addr, session_token = log_proxy_info()

@mcp.tool()
def get_proxy_info() -> str:
    """
    Get current proxy address and session token information.
    
    Returns:
        JSON string with proxy configuration details
    """
    logger.info("Getting proxy information via tool call")
    
    try:
        dlai_url = os.environ.get('DLAI_LOCAL_URL', 'http://localhost:{port}/')
        proxy_address = dlai_url.format(port=6277)
        
        if proxy_address.endswith('/'):
            proxy_address = proxy_address[:-1]
        
        session_token = os.environ.get('MCP_SESSION_TOKEN', 'Not set - use generated token')
        
        proxy_info = {
            "proxy_address": proxy_address,
            "session_token": session_token if session_token != 'Not set - use generated token' else f"Generated: {secrets.token_hex(16)}",
            "timestamp": datetime.now().isoformat(),
            "environment_variables": {
                "DLAI_LOCAL_URL": os.environ.get('DLAI_LOCAL_URL', 'Not set'),
                "MCP_SESSION_TOKEN": "Set" if os.environ.get('MCP_SESSION_TOKEN') else "Not set"
            }
        }
        
        logger.info(f"Proxy info requested: {proxy_address}")
        return json.dumps(proxy_info, indent=2)
        
    except Exception as e:
        logger.error(f"Error getting proxy info: {str(e)}")
        return json.dumps({"error": str(e)}, indent=2)

@mcp.tool()
def search_papers(topic: str, max_results: int = 5) -> List[str]:
    """
    Search for papers on arXiv based on a topic and store their information.
    
    Args:
        topic: The topic to search for
        max_results: Maximum number of results to retrieve (default: 5)
        
    Returns:
        List of paper IDs found in the search
    """
    logger.info(f"Starting paper search for topic: '{topic}' with max_results: {max_results}")
    
    try:
        # Use arxiv to find the papers 
        client = arxiv.Client()
        logger.debug("Created arXiv client")

        # Search for the most relevant articles matching the queried topic
        search = arxiv.Search(
            query = topic,
            max_results = max_results,
            sort_by = arxiv.SortCriterion.Relevance
        )
        logger.debug(f"Created search query for topic: {topic}")

        papers = client.results(search)
        logger.info(f"Retrieved papers from arXiv for topic: {topic}")
        
        # Create directory for this topic
        path = os.path.join(PAPER_DIR, topic.lower().replace(" ", "_"))
        os.makedirs(path, exist_ok=True)
        logger.debug(f"Created/verified directory: {path}")
        
        file_path = os.path.join(path, "papers_info.json")

        # Try to load existing papers info
        try:
            with open(file_path, "r") as json_file:
                papers_info = json.load(json_file)
            logger.debug(f"Loaded existing papers info from: {file_path}")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            papers_info = {}
            logger.debug(f"No existing papers info found or file corrupted: {e}")

        # Process each paper and add to papers_info  
        paper_ids = []
        processed_count = 0
        for paper in papers:
            paper_ids.append(paper.get_short_id())
            paper_info = {
                'title': paper.title,
                'authors': [author.name for author in paper.authors],
                'summary': paper.summary,
                'pdf_url': paper.pdf_url,
                'published': str(paper.published.date())
            }
            papers_info[paper.get_short_id()] = paper_info
            processed_count += 1
            logger.debug(f"Processed paper {processed_count}: {paper.get_short_id()} - {paper.title[:50]}...")
        
        # Save updated papers_info to json file
        with open(file_path, "w") as json_file:
            json.dump(papers_info, json_file, indent=2)
        
        logger.info(f"Successfully saved {processed_count} papers to: {file_path}")
        print(f"Results are saved in: {file_path}")
        
        logger.info(f"Paper search completed successfully. Found {len(paper_ids)} papers for topic: '{topic}'")
        return paper_ids
        
    except Exception as e:
        logger.error(f"Error in search_papers for topic '{topic}': {str(e)}")
        raise

@mcp.tool()
def extract_info(paper_id: str) -> str:
    """
    Search for information about a specific paper across all topic directories.
    
    Args:
        paper_id: The ID of the paper to look for
        
    Returns:
        JSON string with paper information if found, error message if not found
    """
    logger.info(f"Extracting information for paper ID: {paper_id}")
    
    try:
        if not os.path.exists(PAPER_DIR):
            logger.warning(f"Papers directory does not exist: {PAPER_DIR}")
            return f"There's no saved information related to paper {paper_id}."
        
        directories_searched = 0
        for item in os.listdir(PAPER_DIR):
            item_path = os.path.join(PAPER_DIR, item)
            if os.path.isdir(item_path):
                directories_searched += 1
                file_path = os.path.join(item_path, "papers_info.json")
                logger.debug(f"Searching in directory: {item_path}")
                
                if os.path.isfile(file_path):
                    try:
                        with open(file_path, "r") as json_file:
                            papers_info = json.load(json_file)
                            if paper_id in papers_info:
                                logger.info(f"Found paper {paper_id} in {file_path}")
                                return json.dumps(papers_info[paper_id], indent=2)
                    except (FileNotFoundError, json.JSONDecodeError) as e:
                        logger.error(f"Error reading {file_path}: {str(e)}")
                        print(f"Error reading {file_path}: {str(e)}")
                        continue
        
        logger.warning(f"Paper {paper_id} not found after searching {directories_searched} directories")
        return f"There's no saved information related to paper {paper_id}."
        
    except Exception as e:
        logger.error(f"Error in extract_info for paper_id '{paper_id}': {str(e)}")
        return f"Error occurred while searching for paper {paper_id}: {str(e)}"

@mcp.resource("papers://folders")
def get_available_folders() -> str:
    """
    List all available topic folders in the papers directory.
    
    This resource provides a simple list of all available topic folders.
    """
    logger.info("Getting available topic folders")
    
    try:
        folders = []
        
        # Get all topic directories
        if os.path.exists(PAPER_DIR):
            for topic_dir in os.listdir(PAPER_DIR):
                topic_path = os.path.join(PAPER_DIR, topic_dir)
                if os.path.isdir(topic_path):
                    papers_file = os.path.join(topic_path, "papers_info.json")
                    if os.path.exists(papers_file):
                        folders.append(topic_dir)
                        logger.debug(f"Found valid topic folder: {topic_dir}")
        else:
            logger.warning(f"Papers directory does not exist: {PAPER_DIR}")
        
        # Create a simple markdown list
        content = "# Available Topics\n\n"
        if folders:
            for folder in folders:
                content += f"- {folder}\n"
            content += f"\nUse @{folder} to access papers in that topic.\n"
            logger.info(f"Found {len(folders)} available topic folders")
        else:
            content += "No topics found.\n"
            logger.info("No topic folders found")
        
        return content
        
    except Exception as e:
        logger.error(f"Error in get_available_folders: {str(e)}")
        return f"# Error\n\nFailed to retrieve topic folders: {str(e)}"

@mcp.resource("papers://{topic}")
def get_topic_papers(topic: str) -> str:
    """
    Get detailed information about papers on a specific topic.
    
    Args:
        topic: The research topic to retrieve papers for
    """
    logger.info(f"Getting papers for topic: {topic}")
    
    try:
        topic_dir = topic.lower().replace(" ", "_")
        papers_file = os.path.join(PAPER_DIR, topic_dir, "papers_info.json")
        logger.debug(f"Looking for papers file: {papers_file}")
        
        if not os.path.exists(papers_file):
            logger.warning(f"No papers file found for topic: {topic} at {papers_file}")
            return f"# No papers found for topic: {topic}\n\nTry searching for papers on this topic first."
        
        try:
            with open(papers_file, 'r') as f:
                papers_data = json.load(f)
            logger.debug(f"Loaded {len(papers_data)} papers for topic: {topic}")
            
            # Create markdown content with paper details
            content = f"# Papers on {topic.replace('_', ' ').title()}\n\n"
            content += f"Total papers: {len(papers_data)}\n\n"
            
            paper_count = 0
            for paper_id, paper_info in papers_data.items():
                content += f"## {paper_info['title']}\n"
                content += f"- **Paper ID**: {paper_id}\n"
                content += f"- **Authors**: {', '.join(paper_info['authors'])}\n"
                content += f"- **Published**: {paper_info['published']}\n"
                content += f"- **PDF URL**: [{paper_info['pdf_url']}]({paper_info['pdf_url']})\n\n"
                content += f"### Summary\n{paper_info['summary'][:500]}...\n\n"
                content += "---\n\n"
                paper_count += 1
            
            logger.info(f"Successfully generated content for {paper_count} papers on topic: {topic}")
            return content
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error for topic {topic}: {str(e)}")
            return f"# Error reading papers data for {topic}\n\nThe papers data file is corrupted."
            
    except Exception as e:
        logger.error(f"Error in get_topic_papers for topic '{topic}': {str(e)}")
        return f"# Error\n\nFailed to retrieve papers for topic {topic}: {str(e)}"

@mcp.tool()
def save_to_markdown(filename: str, content: str) -> str:
    """
    Saves the given content to a markdown file.
    
    Args:
        filename: The name of the file to save (e.g., 'report.md').
        content: The text content to write to the file.
        
    Returns:
        A confirmation message.
    """
    logger.info(f"Attempting to save content to file: {filename}")
    
    if ".." in filename or "/" in filename or "\\" in filename:
        logger.warning(f"Invalid filename attempted: {filename}")
        return "Error: Invalid filename. Cannot contain path separators."
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        file_size = len(content.encode('utf-8'))
        logger.info(f"Successfully saved {file_size} bytes to {filename}")
        return f"Successfully saved content to {filename}"
        
    except Exception as e:
        logger.error(f"Error saving file {filename}: {str(e)}")
        return f"Error saving file: {e}"

@mcp.prompt()
def generate_search_prompt(topic: str, num_papers: int = 5) -> str:
    """Generate a prompt for the AI assistant to find and discuss academic papers on a specific topic."""
    logger.info(f"Generating search prompt for topic: '{topic}' with {num_papers} papers")
    
    return f"""Search for {num_papers} academic papers about '{topic}'.

Follow these instructions:
1. First, call the `search_papers` tool with `topic='{topic}'` and `max_results={num_papers}`.
2. The `search_papers` tool will return a list of paper IDs. For each paper ID in the list, you MUST call the `extract_info` tool to get the details of that paper.
3. After you have gathered the information for all the papers, provide a comprehensive summary that synthesizes the information. Your summary should include:
   - An overview of the current state of research in '{topic}'.
   - Common themes and trends across the papers.
   - Key research gaps or areas for future investigation.
4. Finally, present the detailed information for each paper individually. Organize your findings in a clear, structured format with headings and bullet points. For each paper, include:
   - Paper title
   - Authors
   - Publication date
   - A brief summary of the key findings.

Please execute this multi-step process. First call all necessary tools, then provide the synthesis and detailed breakdown."""

@mcp.prompt()
def research_and_save_report(topic: str, num_papers: int = 3, filename: str = "research_report.md") -> str:
    """
    Researches a topic, synthesizes the findings, and saves the result to a markdown file.
    
    Args:
        topic: The research topic.
        num_papers: The number of papers to include in the research.
        filename: The name of the markdown file for the final report.
    """
    logger.info(f"Generating research and save prompt for topic: '{topic}' with {num_papers} papers, saving to: {filename}")
    
    return f"""First, get the detailed information for {num_papers} papers on the topic '{topic}'. To do this, you must first call the `search_papers` tool, and then for each paper ID returned, you must call the `extract_info` tool.

Once you have the detailed information for all papers, create a comprehensive report in markdown format. The report should have two sections:
1.  A high-level synthesis of the research, including common themes, trends, and key findings.
2.  A detailed breakdown of each individual paper, including its title, authors, publication date, and a summary of its contributions.

Finally, take the complete markdown report and save it to a file by calling the `save_to_markdown` tool with the specified `filename` ('{filename}') and the markdown content you generated."""

if __name__ == "__main__":
    logger.info("Starting MCP research server with stdio transport")
    try:
        # Initialize and run the server
        mcp.run(transport='stdio')
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        raise
    finally:
        logger.info("MCP research server shutting down")