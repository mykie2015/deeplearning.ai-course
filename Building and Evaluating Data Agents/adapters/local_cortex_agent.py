"""
Local Cortex Agent Adapter
This module provides a drop-in replacement for Snowflake Cortex Agent
using PostgreSQL + Chroma for structured and unstructured data.
"""

import os
import json
import warnings
from typing import Dict, Any, List, Optional, Tuple
from pydantic import BaseModel, PrivateAttr
import chromadb
from openai import OpenAI
import pandas as pd
from adapters.local_snowpark import LocalSnowparkSession


class LocalCortexAgentArgs(BaseModel):
    query: str


class LocalCortexAgentTool:
    """
    Drop-in replacement for Snowflake CortexAgentTool
    Combines PostgreSQL (structured data) + Chroma (unstructured data)
    """
    
    name: str = "LocalCortexAgent"
    description: str = "answers questions using sales conversations and metrics from local data"
    args_schema = LocalCortexAgentArgs
    
    _session: Optional[LocalSnowparkSession] = PrivateAttr()
    _chroma_client: Optional[chromadb.HttpClient] = PrivateAttr()
    _chroma_collection: Optional[chromadb.Collection] = PrivateAttr()
    _openai_client: Optional[OpenAI] = PrivateAttr()
    
    def __init__(self, session: Optional[LocalSnowparkSession] = None):
        """Initialize with local session and setup Chroma client"""
        self._session = session
        self._setup_chroma()
        self._setup_openai()
    
    def _setup_chroma(self):
        """Setup Chroma client and collection with fallback to simple search"""
        try:
            chroma_host = os.getenv("CHROMA_HOST", "localhost")
            chroma_port = int(os.getenv("CHROMA_PORT", "8000"))
            
            # Try Chroma first
            self._chroma_client = chromadb.HttpClient(
                host=chroma_host, 
                port=chroma_port,
                settings=chromadb.Settings(allow_reset=True)
            )
            
            # Test connection
            self._chroma_client.list_collections()
            
            # Try to get existing collection, create if doesn't exist
            try:
                self._chroma_collection = self._chroma_client.get_collection("meeting_notes")
            except Exception:
                # Collection doesn't exist, create it
                self._chroma_collection = self._chroma_client.create_collection(
                    name="meeting_notes",
                    metadata={"description": "Sales meeting transcripts and notes"}
                )
                # Initialize with sample data
                self._initialize_sample_data()
            
            print("✅ Chroma vector database connected successfully")
                
        except Exception as e:
            warnings.warn(f"Chroma unavailable, using simple text search fallback: {e}")
            self._chroma_client = None
            self._chroma_collection = None
            # Initialize simple fallback data
            self._simple_meeting_notes = self._get_simple_meeting_notes()
    
    def _setup_openai(self):
        """Setup OpenAI client for text processing"""
        try:
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                self._openai_client = OpenAI(api_key=api_key)
            else:
                self._openai_client = None
                warnings.warn("OpenAI API key not found")
        except Exception as e:
            warnings.warn(f"Failed to setup OpenAI client: {e}")
            self._openai_client = None
    
    def _initialize_sample_data(self):
        """Initialize Chroma collection with sample meeting notes from PostgreSQL"""
        if not self._chroma_collection:
            return
        
        # Try to get meeting transcripts from PostgreSQL first
        try:
            if hasattr(self._session, 'sql'):
                # Get meeting transcripts from the database
                rows = self._session.sql("""
                    SELECT conversation_id, company_name, meeting_date, meeting_type, 
                           participants, transcript_text, deal_id
                    FROM data.sales_conversations
                    ORDER BY conversation_id
                """).collect()
                
                if rows:
                    sample_notes = []
                    for row in rows:
                        # Create a summary of the transcript for better searchability
                        transcript = row.get('transcript_text', '')
                        # Take first 500 characters as a summary
                        summary = transcript[:500] + "..." if len(transcript) > 500 else transcript
                        
                        sample_notes.append({
                            "id": f"CONV{row.get('conversation_id', 0):03d}",
                            "document": summary,
                            "metadata": {
                                "conversation_id": str(row.get('conversation_id', '')),
                                "company_name": row.get('company_name', ''),
                                "meeting_date": str(row.get('meeting_date', '')),
                                "participants": row.get('participants', ''),
                                "meeting_type": row.get('meeting_type', ''),
                                "deal_id": str(row.get('deal_id', ''))
                            }
                        })
                    
                    print(f"ℹ️  Loading {len(sample_notes)} meeting transcripts from PostgreSQL")
                else:
                    # Fallback to hardcoded data if no database records
                    sample_notes = self._get_fallback_meeting_notes()
            else:
                # Fallback to hardcoded data if no database session
                sample_notes = self._get_fallback_meeting_notes()
                
        except Exception as e:
            print(f"ℹ️  Could not load from database, using fallback data: {e}")
            sample_notes = self._get_fallback_meeting_notes()
        
        # Add the sample notes to Chroma
        try:
            # Add documents to collection
            documents = [note["document"] for note in sample_notes]
            ids = [note["id"] for note in sample_notes]
            metadatas = [note["metadata"] for note in sample_notes]
            
            self._chroma_collection.add(
                documents=documents,
                ids=ids,
                metadatas=metadatas
            )
            print(f"✅ Initialized Chroma collection with {len(sample_notes)} meeting notes")
        except Exception as e:
            warnings.warn(f"Failed to initialize sample data: {e}")
    
    def _get_fallback_meeting_notes(self):
        """Get fallback meeting notes when database is not available"""
        return [
            {
                "id": "MTG001",
                "document": "Customer expressed strong interest in our enterprise solution. Key concerns were around security and compliance. They need integration with their existing CRM system. Budget approved for Q2 implementation.",
                "metadata": {
                    "meeting_id": "MTG001",
                    "company_name": "Acme Corporation",
                    "meeting_date": "2024-03-10",
                    "participants": "John Smith, Customer CTO",
                    "meeting_type": "Discovery",
                    "deal_id": "1"
                }
            },
            {
                "id": "MTG002",
                "document": "Technical requirements discussion. Customer needs cloud-native solution with 99.9% uptime SLA. Discussed scalability requirements for 10,000+ users. Integration with Salesforce is critical.",
                "metadata": {
                    "meeting_id": "MTG002",
                    "company_name": "TechStart Inc",
                    "meeting_date": "2024-03-18",
                    "participants": "Jane Doe, Customer CTO",
                    "meeting_type": "Technical",
                    "deal_id": "2"
                }
            },
            {
                "id": "MTG003",
                "document": "Final proposal presentation. Customer very satisfied with our AI platform capabilities. Discussed implementation timeline - 6 months phased rollout. Decision expected by month end.",
                "metadata": {
                    "meeting_id": "MTG003",
                    "company_name": "Global Dynamics",
                    "meeting_date": "2024-02-25",
                    "participants": "Mike Johnson, Customer CEO",
                    "meeting_type": "Proposal",
                    "deal_id": "3"
                }
            }
        ]
    
    def _get_simple_meeting_notes(self):
        """Get simple meeting notes for fallback when Chroma is unavailable"""
        return [
            {
                "id": "MTG001",
                "document": "Customer expressed strong interest in our enterprise solution. Key concerns were around security and compliance. They need integration with their existing CRM system. Budget approved for Q2 implementation.",
                "metadata": {
                    "company_name": "Acme Corporation",
                    "meeting_type": "Discovery",
                    "deal_id": "1"
                }
            },
            {
                "id": "MTG002", 
                "document": "Technical requirements discussion. Customer needs cloud-native solution with 99.9% uptime SLA. Discussed scalability requirements for 10,000+ users. Integration with Salesforce is critical.",
                "metadata": {
                    "company_name": "TechStart Inc",
                    "meeting_type": "Technical",
                    "deal_id": "2"
                }
            },
            {
                "id": "MTG003",
                "document": "Final proposal presentation. Customer very satisfied with our AI platform capabilities. Discussed implementation timeline - 6 months phased rollout. Decision expected by month end.",
                "metadata": {
                    "company_name": "Global Dynamics",
                    "meeting_type": "Proposal", 
                    "deal_id": "3"
                }
            }
        ]
    
    def _query_structured_data(self, query: str) -> Tuple[str, str, pd.DataFrame]:
        """Query PostgreSQL for structured data (mimics Cortex Analyst)"""
        if not self._session:
            return "No database session available", "", pd.DataFrame()
        
        # Simple text-to-SQL logic for common queries
        sql_query = self._generate_sql_from_query(query)
        
        try:
            # Execute the query
            result = self._session.sql(sql_query)
            df = result.to_pandas()
            
            # Generate response text
            if len(df) > 0:
                response_text = f"Found {len(df)} records from sales metrics data.\n"
                response_text += f"Results summary:\n{df.to_string(index=False, max_rows=10)}"
            else:
                response_text = "No records found matching the query criteria."
            
            return response_text, sql_query, df
            
        except Exception as e:
            error_msg = f"SQL execution error: {str(e)}"
            return error_msg, sql_query, pd.DataFrame()
    
    def _generate_sql_from_query(self, query: str) -> str:
        """
        Generate SQL query from natural language (simplified text-to-SQL)
        In production, this would use a more sophisticated NL2SQL model
        """
        query_lower = query.lower()
        schema = os.getenv("POSTGRES_SCHEMA", "data")
        
        # Base query structure
        base_query = f"SELECT * FROM {schema}.sales_metrics"
        conditions = []
        
        # Common patterns and their SQL translations
        if "closed won" in query_lower or "won deals" in query_lower:
            conditions.append("deal_status = 'Closed Won'")
        
        if "negotiation" in query_lower:
            conditions.append("deal_status = 'Negotiation'")
        
        if "enterprise software" in query_lower:
            conditions.append("product_line = 'Enterprise Software'")
        
        if "ai platform" in query_lower:
            conditions.append("product_line = 'AI Platform'")
        
        if "cloud services" in query_lower:
            conditions.append("product_line = 'Cloud Services'")
        
        if "data analytics" in query_lower:
            conditions.append("product_line = 'Data Analytics'")
        
        if "machine learning" in query_lower:
            conditions.append("product_line = 'Machine Learning'")
        
        # Company name patterns
        companies = ["acme", "techstart", "global dynamics", "innovatecorp", "nextgen"]
        for company in companies:
            if company in query_lower:
                conditions.append(f"LOWER(company_name) LIKE '%{company}%'")
        
        # Date patterns
        if "2024" in query_lower:
            conditions.append("EXTRACT(YEAR FROM close_date) = 2024")
        
        if "this year" in query_lower or "current year" in query_lower:
            conditions.append("EXTRACT(YEAR FROM close_date) = EXTRACT(YEAR FROM CURRENT_DATE)")
        
        # Value patterns
        if "top" in query_lower and ("deals" in query_lower or "value" in query_lower):
            base_query = f"SELECT * FROM {schema}.sales_metrics WHERE deal_status = 'Closed Won'"
            return f"{base_query} ORDER BY deal_value DESC LIMIT 10"
        
        if "total" in query_lower and "value" in query_lower:
            return f"SELECT product_line, SUM(deal_value) as total_value, COUNT(*) as deal_count FROM {schema}.sales_metrics GROUP BY product_line ORDER BY total_value DESC"
        
        if "average" in query_lower or "avg" in query_lower:
            return f"SELECT product_line, AVG(deal_value) as avg_value, COUNT(*) as deal_count FROM {schema}.sales_metrics GROUP BY product_line ORDER BY avg_value DESC"
        
        # Sales rep patterns
        if "sales rep" in query_lower or "salesperson" in query_lower:
            return f"SELECT sales_rep, COUNT(*) as total_deals, SUM(CASE WHEN deal_status = 'Closed Won' THEN deal_value ELSE 0 END) as won_value FROM {schema}.sales_metrics GROUP BY sales_rep ORDER BY won_value DESC"
        
        # Build final query
        if conditions:
            where_clause = " AND ".join(conditions)
            final_query = f"{base_query} WHERE {where_clause}"
        else:
            # Default: return recent deals
            final_query = f"{base_query} ORDER BY close_date DESC LIMIT 20"
        
        return final_query
    
    def _query_unstructured_data(self, query: str, max_results: int = 5) -> Tuple[str, List[Dict]]:
        """Query Chroma for unstructured data (mimics Cortex Search) with fallback"""
        
        # Try Chroma first if available
        if self._chroma_collection:
            try:
                # Perform semantic search
                results = self._chroma_collection.query(
                    query_texts=[query],
                    n_results=max_results
                )
                
                # Process results
                citations = []
                response_parts = []
                
                if results['ids'] and results['ids'][0]:
                    response_parts.append(f"Found {len(results['ids'][0])} relevant meeting notes:")
                    
                    for i, (doc_id, document, metadata, distance) in enumerate(zip(
                        results['ids'][0],
                        results['documents'][0],
                        results['metadatas'][0],
                        results['distances'][0]
                    )):
                        # Create citation
                        citation = {
                            "source_id": doc_id,
                            "doc_id": doc_id,
                            "company_name": metadata.get("company_name", "Unknown"),
                            "meeting_type": metadata.get("meeting_type", "Unknown"),
                            "relevance": 1 - distance
                        }
                        citations.append(citation)
                        
                        # Add to response
                        response_parts.append(
                            f"\n{i+1}. {metadata.get('company_name', 'Unknown')} - "
                            f"{metadata.get('meeting_type', 'Unknown')} "
                            f"({metadata.get('meeting_date', 'Unknown date')}):\n"
                            f"{document[:200]}{'...' if len(document) > 200 else ''}"
                        )
                else:
                    response_parts.append("No relevant meeting notes found for this query.")
                
                return "\n".join(response_parts), citations
                
            except Exception as e:
                # Fall through to simple search
                pass
        
        # Fallback to simple text search
        return self._simple_text_search(query, max_results)
    
    def _simple_text_search(self, query: str, max_results: int = 5) -> Tuple[str, List[Dict]]:
        """Simple text search fallback when Chroma is unavailable"""
        if not hasattr(self, '_simple_meeting_notes'):
            return "No meeting notes available", []
        
        query_lower = query.lower()
        matches = []
        
        # Simple keyword matching
        for note in self._simple_meeting_notes:
            document = note["document"].lower()
            metadata = note["metadata"]
            
            # Calculate simple relevance score based on keyword matches
            score = 0
            for word in query_lower.split():
                if word in document:
                    score += document.count(word)
            
            if score > 0:
                matches.append((note, score))
        
        # Sort by relevance and limit results
        matches.sort(key=lambda x: x[1], reverse=True)
        matches = matches[:max_results]
        
        if matches:
            response_parts = [f"Found {len(matches)} relevant meeting notes (simple text search):"]
            citations = []
            
            for i, (note, score) in enumerate(matches):
                metadata = note["metadata"]
                document = note["document"]
                
                citation = {
                    "source_id": note["id"],
                    "doc_id": note["id"],
                    "company_name": metadata.get("company_name", "Unknown"),
                    "meeting_type": metadata.get("meeting_type", "Unknown"),
                    "relevance": score / 10  # Normalize score
                }
                citations.append(citation)
                
                response_parts.append(
                    f"\n{i+1}. {metadata.get('company_name', 'Unknown')} - "
                    f"{metadata.get('meeting_type', 'Unknown')}:\n"
                    f"{document[:200]}{'...' if len(document) > 200 else ''}"
                )
            
            return "\n".join(response_parts), citations
        else:
            return "No relevant meeting notes found for this query.", []
    
    def _combine_results(self, query: str, structured_text: str, unstructured_text: str, 
                        citations: List[Dict], sql: str) -> str:
        """Combine structured and unstructured results using LLM"""
        if not self._openai_client:
            # Simple text combination without LLM
            combined = f"Query: {query}\n\n"
            
            if structured_text and "error" not in structured_text.lower():
                combined += f"Structured Data Results:\n{structured_text}\n\n"
            
            if unstructured_text and "error" not in unstructured_text.lower():
                combined += f"Meeting Notes:\n{unstructured_text}\n\n"
            
            if citations:
                combined += f"Citations: {citations}\n\n"
            
            if sql:
                combined += f"SQL Query: {sql}"
            
            return combined
        
        # Use LLM to create coherent response
        try:
            prompt = f"""
You are an AI assistant analyzing sales data. Combine the following information to answer the user's query comprehensively:

User Query: {query}

Structured Data (from sales metrics):
{structured_text}

Meeting Notes (from sales conversations):
{unstructured_text}

Please provide a comprehensive answer that:
1. Directly answers the user's question
2. Combines insights from both structured data and meeting notes
3. Highlights key findings and patterns
4. Keeps the response concise but informative

Answer:"""

            response = self._openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.1
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            # Fallback to simple combination
            return f"Combined Results for: {query}\n\nStructured Data:\n{structured_text}\n\nMeeting Notes:\n{unstructured_text}"
    
    def run(self, query: str, **kwargs) -> Tuple[str, str, str, str]:
        """
        Main entry point - mimics Snowflake CortexAgentTool.run() interface
        Returns: (text_response, citations, sql_query, results_string)
        """
        # Query both structured and unstructured data
        structured_text, sql_query, df = self._query_structured_data(query)
        unstructured_text, citations = self._query_unstructured_data(query)
        
        # Combine results
        combined_response = self._combine_results(
            query, structured_text, unstructured_text, citations, sql_query
        )
        
        # Format results string
        results_string = ""
        if not df.empty:
            results_string = df.to_string(index=False)
        
        # Format citations string
        citations_string = str(citations) if citations else ""
        
        return combined_response, citations_string, sql_query, results_string


def create_local_cortex_agent(session: Optional[LocalSnowparkSession] = None) -> Optional[LocalCortexAgentTool]:
    """
    Create a local Cortex agent tool
    """
    try:
        return LocalCortexAgentTool(session=session)
    except Exception as e:
        warnings.warn(f"Failed to create local Cortex agent: {e}")
        return None
