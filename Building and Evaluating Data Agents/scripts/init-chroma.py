#!/usr/bin/env python3
"""
Initialize Chroma Vector Database with meeting notes collection
This script sets up the unstructured data component replacing Snowflake Cortex Search
"""

import chromadb
import json
import sys
import os
from typing import List, Dict, Any

def create_chroma_client(host: str = "localhost", port: int = 8000) -> chromadb.HttpClient:
    """Create and return Chroma client"""
    try:
        client = chromadb.HttpClient(host=host, port=port)
        # Test connection
        client.heartbeat()
        print(f"✅ Connected to Chroma at {host}:{port}")
        return client
    except Exception as e:
        print(f"❌ Failed to connect to Chroma: {e}")
        sys.exit(1)

def create_meeting_notes_collection(client: chromadb.HttpClient) -> chromadb.Collection:
    """Create or get the meeting notes collection"""
    collection_name = "meeting_notes"
    
    try:
        # Try to get existing collection
        collection = client.get_collection(collection_name)
        print(f"✅ Found existing collection: {collection_name}")
        return collection
    except:
        # Create new collection if it doesn't exist
        collection = client.create_collection(
            name=collection_name,
            metadata={"description": "Sales meeting transcripts and notes"}
        )
        print(f"✅ Created new collection: {collection_name}")
        return collection

def get_sample_meeting_notes() -> List[Dict[str, Any]]:
    """Generate comprehensive sample meeting notes data"""
    return [
        {
            "id": "MTG001",
            "document": "Customer expressed strong interest in our enterprise solution. Key concerns were around security and compliance. They need integration with their existing CRM system. Budget approved for Q2 implementation. Next steps: technical demo scheduled for next week. Customer mentioned they're currently using a legacy system that's causing data silos. They want to modernize their tech stack.",
            "metadata": {
                "meeting_id": "MTG001",
                "company_name": "Acme Corporation",
                "meeting_date": "2024-03-10",
                "participants": "John Smith, Customer CTO, Customer VP Sales",
                "meeting_type": "Discovery",
                "deal_id": "1",
                "product_line": "Enterprise Software"
            }
        },
        {
            "id": "MTG002",
            "document": "Technical requirements discussion. Customer needs cloud-native solution with 99.9% uptime SLA. Discussed scalability requirements for 10,000+ users. Integration with Salesforce is critical. Pricing discussion - budget range $70-80k confirmed. They're evaluating 3 vendors total. Main competitor is Microsoft. Customer likes our AI capabilities.",
            "metadata": {
                "meeting_id": "MTG002",
                "company_name": "TechStart Inc",
                "meeting_date": "2024-03-18",
                "participants": "Jane Doe, Customer CTO, Technical Team",
                "meeting_type": "Technical",
                "deal_id": "2",
                "product_line": "Cloud Services"
            }
        },
        {
            "id": "MTG003",
            "document": "Final proposal presentation. Customer very satisfied with our AI platform capabilities. Discussed implementation timeline - 6 months phased rollout. Security audit requirements discussed. Legal team needs to review contract terms. Decision expected by month end. CEO mentioned this is their top priority project for 2024.",
            "metadata": {
                "meeting_id": "MTG003",
                "company_name": "Global Dynamics",
                "meeting_date": "2024-02-25",
                "participants": "Mike Johnson, Customer CEO, Customer CFO",
                "meeting_type": "Proposal",
                "deal_id": "3",
                "product_line": "AI Platform"
            }
        },
        {
            "id": "MTG004",
            "document": "Initial discovery call. Customer evaluating data analytics solutions. Current pain points: manual reporting, lack of real-time insights. Team of 50 analysts. Looking for self-service BI capabilities. Competitive evaluation in progress. They want to reduce reporting time from days to hours.",
            "metadata": {
                "meeting_id": "MTG004",
                "company_name": "InnovateCorp",
                "meeting_date": "2024-04-02",
                "participants": "Sarah Wilson, Customer Analytics Director",
                "meeting_type": "Discovery",
                "deal_id": "4",
                "product_line": "Data Analytics"
            }
        },
        {
            "id": "MTG005",
            "document": "Machine learning platform demo. Customer impressed with AutoML capabilities. Discussed model deployment and monitoring features. Integration with their existing data lake is essential. ROI projections look promising. Technical POC proposed for next month. They want to start with fraud detection use case.",
            "metadata": {
                "meeting_id": "MTG005",
                "company_name": "NextGen Solutions",
                "meeting_date": "2024-03-08",
                "participants": "David Brown, Customer Data Science Team",
                "meeting_type": "Demo",
                "deal_id": "5",
                "product_line": "Machine Learning"
            }
        },
        {
            "id": "MTG006",
            "document": "Follow-up technical discussion. Addressed concerns about data migration from legacy systems. Customer worried about downtime during transition. Proposed phased migration approach. They need training for 20 users. Discussed support options and SLA requirements.",
            "metadata": {
                "meeting_id": "MTG006",
                "company_name": "FutureTech Ltd",
                "meeting_date": "2024-04-10",
                "participants": "Emily Davis, Customer IT Director",
                "meeting_type": "Technical",
                "deal_id": "6",
                "product_line": "Cloud Services"
            }
        },
        {
            "id": "MTG007",
            "document": "Executive briefing. Presented business case and ROI analysis. Customer excited about potential cost savings of $2M annually. Discussed change management strategy. Need buy-in from regional offices. CFO wants detailed cost breakdown.",
            "metadata": {
                "meeting_id": "MTG007",
                "company_name": "DataMax Systems",
                "meeting_date": "2024-01-18",
                "participants": "Robert Taylor, Customer CFO, Customer COO",
                "meeting_type": "Executive",
                "deal_id": "7",
                "product_line": "Enterprise Software"
            }
        },
        {
            "id": "MTG008",
            "document": "Startup needs assessment. Limited budget but high growth potential. Looking for scalable solution that grows with them. Interested in usage-based pricing model. Technical founder very hands-on. Want to start small and expand.",
            "metadata": {
                "meeting_id": "MTG008",
                "company_name": "CloudFirst Inc",
                "meeting_date": "2024-04-16",
                "participants": "Lisa Anderson, Customer Founder/CTO",
                "meeting_type": "Discovery",
                "deal_id": "8",
                "product_line": "Data Analytics"
            }
        },
        {
            "id": "MTG009",
            "document": "AI strategy workshop. Customer wants to understand how AI can transform their business. Discussed use cases in customer service, operations, and marketing. They're new to AI but very eager to learn. Want to start with pilot project.",
            "metadata": {
                "meeting_id": "MTG009",
                "company_name": "AI Innovations",
                "meeting_date": "2024-02-12",
                "participants": "James Wilson, Customer Innovation Team",
                "meeting_type": "Workshop",
                "deal_id": "9",
                "product_line": "AI Platform"
            }
        },
        {
            "id": "MTG010",
            "document": "Machine learning consulting engagement. Customer has data science team but needs advanced ML platform. Current tools are fragmented. Want unified platform for model development, training, and deployment. Emphasis on MLOps capabilities.",
            "metadata": {
                "meeting_id": "MTG010",
                "company_name": "SmartData Corp",
                "meeting_date": "2024-04-23",
                "participants": "Maria Garcia, Customer Head of Data Science",
                "meeting_type": "Consulting",
                "deal_id": "10",
                "product_line": "Machine Learning"
            }
        },
        # Additional meeting notes for comprehensive testing
        {
            "id": "MTG011",
            "document": "Competitive analysis discussion. Customer comparing us with Salesforce and HubSpot. Our AI capabilities are differentiator. Price is competitive. Customer concerned about implementation complexity. Want references from similar companies.",
            "metadata": {
                "meeting_id": "MTG011",
                "company_name": "MegaCorp Industries",
                "meeting_date": "2024-01-08",
                "participants": "John Smith, Customer Procurement Team",
                "meeting_type": "Competitive",
                "deal_id": "16",
                "product_line": "Enterprise Software"
            }
        },
        {
            "id": "MTG012",
            "document": "Security and compliance deep-dive. Customer operates in regulated industry. GDPR and SOX compliance mandatory. Discussed security architecture and audit requirements. Need security whitepaper and compliance certifications.",
            "metadata": {
                "meeting_id": "MTG012",
                "company_name": "Enterprise Solutions LLC",
                "meeting_date": "2024-03-03",
                "participants": "Mike Johnson, Customer CISO, Compliance Team",
                "meeting_type": "Security",
                "deal_id": "18",
                "product_line": "AI Platform"
            }
        },
        {
            "id": "MTG013",
            "document": "POC results review. Customer very impressed with proof of concept results. 40% improvement in data processing speed. Users love the interface. Ready to move to pilot phase with 100 users. Discussed rollout timeline.",
            "metadata": {
                "meeting_id": "MTG013",
                "company_name": "DataCorp Ltd",
                "meeting_date": "2024-02-18",
                "participants": "Sarah Wilson, Customer Project Team",
                "meeting_type": "POC Review",
                "deal_id": "19",
                "product_line": "Data Analytics"
            }
        },
        {
            "id": "MTG014",
            "document": "Training and onboarding discussion. Customer needs comprehensive training program for 50+ users. Want mix of online and in-person training. Discussed certification program. Need training materials customized for their industry.",
            "metadata": {
                "meeting_id": "MTG014",
                "company_name": "IntelliData Inc",
                "meeting_date": "2024-01-23",
                "participants": "Emily Davis, Customer Learning & Development",
                "meeting_type": "Training",
                "deal_id": "21",
                "product_line": "Machine Learning"
            }
        },
        {
            "id": "MTG015",
            "document": "Contract negotiation session. Discussed terms and conditions. Customer wants flexibility in user licensing. Negotiated volume discounts. Legal teams working on MSA. Target signature date end of month.",
            "metadata": {
                "meeting_id": "MTG015",
                "company_name": "PipelineCorp",
                "meeting_date": "2024-04-28",
                "participants": "James Wilson, Customer Legal Counsel",
                "meeting_type": "Legal",
                "deal_id": "24",
                "product_line": "AI Platform"
            }
        }
    ]

def populate_collection(collection: chromadb.Collection, meeting_notes: List[Dict[str, Any]]) -> None:
    """Populate the collection with meeting notes"""
    print("📝 Adding meeting notes to collection...")
    
    documents = []
    ids = []
    metadatas = []
    
    for note in meeting_notes:
        documents.append(note["document"])
        ids.append(note["id"])
        metadatas.append(note["metadata"])
    
    try:
        # Add all documents in batch
        collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadatas
        )
        print(f"✅ Successfully added {len(meeting_notes)} meeting notes")
    except Exception as e:
        print(f"⚠️  Some notes might already exist. Adding individually...")
        for note in meeting_notes:
            try:
                collection.add(
                    documents=[note["document"]],
                    ids=[note["id"]],
                    metadatas=[note["metadata"]]
                )
                print(f"✅ Added: {note['metadata']['company_name']} - {note['metadata']['meeting_type']}")
            except Exception as individual_error:
                print(f"⚠️  Skipped {note['id']}: {individual_error}")

def verify_setup(collection: chromadb.Collection) -> None:
    """Verify the collection setup and perform test queries"""
    print("\n🔍 Verifying Chroma setup...")
    
    # Check collection count
    count = collection.count()
    print(f"📊 Total documents in collection: {count}")
    
    # Test basic query
    try:
        results = collection.query(
            query_texts=["enterprise software security compliance"],
            n_results=3
        )
        print(f"✅ Test query successful - found {len(results['ids'][0])} relevant documents")
        
        # Show sample results
        for i, (doc_id, distance) in enumerate(zip(results['ids'][0], results['distances'][0])):
            metadata = results['metadatas'][0][i]
            print(f"   {i+1}. {metadata['company_name']} - {metadata['meeting_type']} (relevance: {1-distance:.3f})")
            
    except Exception as e:
        print(f"❌ Test query failed: {e}")

def main():
    """Main initialization function"""
    print("🚀 Initializing Chroma Vector Database...")
    
    # Get configuration from environment or use defaults
    host = os.getenv("CHROMA_HOST", "localhost")
    port = int(os.getenv("CHROMA_PORT", "8000"))
    
    # Create client and collection
    client = create_chroma_client(host, port)
    collection = create_meeting_notes_collection(client)
    
    # Get sample data and populate
    meeting_notes = get_sample_meeting_notes()
    populate_collection(collection, meeting_notes)
    
    # Verify setup
    verify_setup(collection)
    
    print("\n🎉 Chroma initialization completed successfully!")
    print(f"💡 Collection 'meeting_notes' is ready with {len(meeting_notes)} documents")
    print("💡 You can now use semantic search on meeting transcripts")

if __name__ == "__main__":
    main()
