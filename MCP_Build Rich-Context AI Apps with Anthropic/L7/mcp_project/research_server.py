import arxiv
import json
import os
from typing import List
from mcp.server.fastmcp import FastMCP

PAPER_DIR = "papers"

# Initialize FastMCP server
mcp = FastMCP("research")

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
    
    # Use arxiv to find the papers 
    client = arxiv.Client()

    # Search for the most relevant articles matching the queried topic
    search = arxiv.Search(
        query = topic,
        max_results = max_results,
        sort_by = arxiv.SortCriterion.Relevance
    )

    papers = client.results(search)
    
    # Create directory for this topic
    path = os.path.join(PAPER_DIR, topic.lower().replace(" ", "_"))
    os.makedirs(path, exist_ok=True)
    
    file_path = os.path.join(path, "papers_info.json")

    # Try to load existing papers info
    try:
        with open(file_path, "r") as json_file:
            papers_info = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        papers_info = {}

    # Process each paper and add to papers_info  
    paper_ids = []
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
    
    # Save updated papers_info to json file
    with open(file_path, "w") as json_file:
        json.dump(papers_info, json_file, indent=2)
    
    print(f"Results are saved in: {file_path}")
    
    return paper_ids

@mcp.tool()
def extract_info(paper_id: str) -> str:
    """
    Search for information about a specific paper across all topic directories.
    
    Args:
        paper_id: The ID of the paper to look for
        
    Returns:
        JSON string with paper information if found, error message if not found
    """
 
    for item in os.listdir(PAPER_DIR):
        item_path = os.path.join(PAPER_DIR, item)
        if os.path.isdir(item_path):
            file_path = os.path.join(item_path, "papers_info.json")
            if os.path.isfile(file_path):
                try:
                    with open(file_path, "r") as json_file:
                        papers_info = json.load(json_file)
                        if paper_id in papers_info:
                            return json.dumps(papers_info[paper_id], indent=2)
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    print(f"Error reading {file_path}: {str(e)}")
                    continue
    
    return f"There's no saved information related to paper {paper_id}."

@mcp.resource("papers://folders")
def get_available_folders() -> str:
    """
    List all available topic folders in the papers directory.
    
    This resource provides a simple list of all available topic folders.
    """
    folders = []
    
    # Get all topic directories
    if os.path.exists(PAPER_DIR):
        for topic_dir in os.listdir(PAPER_DIR):
            topic_path = os.path.join(PAPER_DIR, topic_dir)
            if os.path.isdir(topic_path):
                papers_file = os.path.join(topic_path, "papers_info.json")
                if os.path.exists(papers_file):
                    folders.append(topic_dir)
    
    # Create a simple markdown list
    content = "# Available Topics\n\n"
    if folders:
        for folder in folders:
            content += f"- {folder}\n"
        content += f"\nUse @{folder} to access papers in that topic.\n"
    else:
        content += "No topics found.\n"
    
    return content

@mcp.resource("papers://{topic}")
def get_topic_papers(topic: str) -> str:
    """
    Get detailed information about papers on a specific topic.
    
    Args:
        topic: The research topic to retrieve papers for
    """
    topic_dir = topic.lower().replace(" ", "_")
    papers_file = os.path.join(PAPER_DIR, topic_dir, "papers_info.json")
    
    if not os.path.exists(papers_file):
        return f"# No papers found for topic: {topic}\n\nTry searching for papers on this topic first."
    
    try:
        with open(papers_file, 'r') as f:
            papers_data = json.load(f)
        
        # Create markdown content with paper details
        content = f"# Papers on {topic.replace('_', ' ').title()}\n\n"
        content += f"Total papers: {len(papers_data)}\n\n"
        
        for paper_id, paper_info in papers_data.items():
            content += f"## {paper_info['title']}\n"
            content += f"- **Paper ID**: {paper_id}\n"
            content += f"- **Authors**: {', '.join(paper_info['authors'])}\n"
            content += f"- **Published**: {paper_info['published']}\n"
            content += f"- **PDF URL**: [{paper_info['pdf_url']}]({paper_info['pdf_url']})\n\n"
            content += f"### Summary\n{paper_info['summary'][:500]}...\n\n"
            content += "---\n\n"
        
        return content
    except json.JSONDecodeError:
        return f"# Error reading papers data for {topic}\n\nThe papers data file is corrupted."

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
    if ".." in filename or "/" in filename or "\\" in filename:
        return "Error: Invalid filename. Cannot contain path separators."
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully saved content to {filename}"
    except Exception as e:
        return f"Error saving file: {e}"

@mcp.prompt()
def generate_search_prompt(topic: str, num_papers: int = 5) -> str:
    """Generate a prompt for the AI assistant to find and discuss academic papers on a specific topic."""
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
    return f"""First, get the detailed information for {num_papers} papers on the topic '{topic}'. To do this, you must first call the `search_papers` tool, and then for each paper ID returned, you must call the `extract_info` tool.

Once you have the detailed information for all papers, create a comprehensive report in markdown format. The report should have two sections:
1.  A high-level synthesis of the research, including common themes, trends, and key findings.
2.  A detailed breakdown of each individual paper, including its title, authors, publication date, and a summary of its contributions.

Finally, take the complete markdown report and save it to a file by calling the `save_to_markdown` tool with the specified `filename` ('{filename}') and the markdown content you generated."""

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')