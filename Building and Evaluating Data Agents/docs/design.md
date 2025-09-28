# Design Document: Snowflake to PostgreSQL + Chroma Replacement

## Overview
This document outlines the design for replacing Snowflake with local alternatives (PostgreSQL + Chroma) in the "Building and Evaluating Data Agents" course while maintaining full compatibility with existing code.

## Current Architecture

### Snowflake Components
- **Snowflake Cortex Analyst**: Text-to-SQL for structured data
- **Snowflake Cortex Search**: Semantic search for unstructured data  
- **Snowpark Session**: Python integration layer
- **Enterprise Data**: CRM records and meeting transcripts

### Data Sources
1. **Structured Data**: Sales metrics (deals, companies, values, status)
2. **Unstructured Data**: Meeting notes and customer interaction transcripts

## Proposed Architecture

### Replacement Components

| Snowflake Component | Local Replacement | Purpose |
|-------------------|------------------|---------|
| Snowflake Database | PostgreSQL in Docker | Structured data storage |
| Cortex Search | Chroma Vector DB | Semantic search & embeddings |
| Snowpark Session | psycopg2 + SQLAlchemy | Database connectivity |
| Cortex Analyst | Custom SQL agent | Text-to-SQL capabilities |

### Technology Stack

#### Structured Data Layer
- **PostgreSQL 15**: Primary database for CRM data
- **Docker Container**: Isolated, reproducible environment
- **Schema**: `sales_intelligence.data` to match Snowflake structure
- **Connection**: Standard PostgreSQL drivers

#### Unstructured Data Layer  
- **Chroma DB**: Vector database for semantic search
- **Docker Container**: Standalone vector storage
- **Embeddings**: OpenAI text-embedding-ada-002
- **Search**: Similarity search with metadata filtering

### Data Schema Design

#### PostgreSQL Schema
```sql
-- Database: sales_intelligence
-- Schema: data

CREATE TABLE data.sales_metrics (
    deal_id SERIAL PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    deal_value DECIMAL(10,2),
    sales_rep VARCHAR(255),
    close_date DATE,
    deal_status VARCHAR(50),
    product_line VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_company_name ON data.sales_metrics(company_name);
CREATE INDEX idx_deal_status ON data.sales_metrics(deal_status);
CREATE INDEX idx_close_date ON data.sales_metrics(close_date);
```

#### Chroma Collection Schema
```python
{
    "collection_name": "meeting_notes",
    "metadata_schema": {
        "meeting_id": str,
        "company_name": str,
        "meeting_date": str,
        "participants": str,
        "meeting_type": str
    },
    "document_content": "transcript_text"
}
```

## Implementation Strategy

### Phase 1: Infrastructure Setup
1. Docker container orchestration
2. Database initialization
3. Sample data population
4. Connection testing

### Phase 2: Code Adaptation Layer
1. Database connection abstraction
2. Query translation utilities
3. Vector search implementation
4. Error handling and fallbacks

### Phase 3: Agent Integration
1. Modify helper.py connection logic
2. Update environment variable handling
3. Implement Cortex-compatible interfaces
4. Test agent functionality

## Environment Configuration

### Original Snowflake Variables
```env
SNOWFLAKE_ACCOUNT=
SNOWFLAKE_USER=
SNOWFLAKE_PAT=
SNOWFLAKE_DATABASE=SALES_INTELLIGENCE
SNOWFLAKE_SCHEMA=DATA
SNOWFLAKE_ROLE=ACCOUNTADMIN
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
```

### New Local Variables
```env
# PostgreSQL Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=agent_user
POSTGRES_PASSWORD=password
POSTGRES_DB=sales_intelligence
POSTGRES_SCHEMA=data

# Chroma Configuration  
CHROMA_HOST=localhost
CHROMA_PORT=8000
CHROMA_COLLECTION=meeting_notes

# OpenAI for embeddings
OPENAI_API_KEY=your_key_here
```

## Code Compatibility

### Connection Layer Abstraction
```python
# Maintain existing interface
class LocalSnowparkSession:
    """Drop-in replacement for Snowpark Session"""
    
    def sql(self, query: str):
        """Execute SQL query against PostgreSQL"""
        pass
    
    def collect(self):
        """Return results in Snowpark-compatible format"""
        pass
```

### Agent Tool Compatibility
```python
# Maintain CortexAgentTool interface
class LocalCortexAgentTool:
    """Local replacement for Snowflake Cortex Agent"""
    
    def __init__(self, session, postgres_conn, chroma_client):
        self.session = session
        self.postgres_conn = postgres_conn
        self.chroma_client = chroma_client
    
    def invoke(self, query: str):
        """Process query using local components"""
        pass
```

## Benefits of Local Setup

### Development Advantages
- **Full Control**: Complete data ownership and customization
- **No Dependencies**: No external service requirements
- **Cost Effective**: No cloud service fees
- **Privacy**: All data remains local
- **Debugging**: Direct access to all components

### Operational Benefits
- **Reproducible**: Docker ensures consistent environments
- **Portable**: Can run on any Docker-capable system
- **Scalable**: Can upgrade to production databases later
- **Educational**: Better understanding of underlying technologies

## Performance Considerations

### Expected Performance
- **PostgreSQL**: Excellent for structured queries up to millions of records
- **Chroma**: Fast vector similarity search for thousands of documents
- **Local Network**: Sub-millisecond latency for container communication

### Scaling Strategies
- **Database**: Add read replicas, connection pooling
- **Vector Search**: Implement caching, batch processing
- **Memory**: Configure appropriate Docker resource limits

## Risk Mitigation

### Potential Issues
1. **Data Volume**: Large datasets may require optimization
2. **Complexity**: Additional moving parts vs. single service
3. **Maintenance**: Manual updates vs. managed service

### Mitigation Strategies
1. **Monitoring**: Add health checks for all containers
2. **Backup**: Implement data persistence volumes
3. **Documentation**: Clear setup and troubleshooting guides

## Future Considerations

### Migration Path
- Easy transition to managed PostgreSQL (AWS RDS, Google Cloud SQL)
- Chroma can be replaced with Pinecone or Weaviate
- Code abstraction enables swapping backends

### Enhancement Opportunities
- Add Redis for caching frequently accessed data
- Implement proper authentication and authorization
- Add data lineage and audit logging
- Scale to distributed architectures

## Success Criteria

### Functional Requirements
✅ All existing agent functionality preserved  
✅ Same query capabilities for structured data  
✅ Equivalent semantic search for unstructured data  
✅ Compatible with existing lesson notebooks  

### Non-Functional Requirements  
✅ Setup time under 10 minutes  
✅ Query response time under 2 seconds  
✅ Works on all major operating systems  
✅ Minimal additional dependencies  

This design ensures a seamless transition from Snowflake to local alternatives while maintaining the educational value and functionality of the original course materials.
