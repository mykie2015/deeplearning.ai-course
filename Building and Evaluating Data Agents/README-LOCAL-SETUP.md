# Local Data Agents Setup Guide

This guide helps you set up a local development environment for the "Building and Evaluating Data Agents" course using PostgreSQL + Chroma instead of Snowflake.

## 🎯 What This Setup Provides

- **PostgreSQL** for structured data (CRM, sales metrics)
- **Chroma Vector Database** for unstructured data (meeting notes)
- **Drop-in compatibility** with existing course notebooks
- **No cloud dependencies** - everything runs locally
- **Cost-effective** - no Snowflake subscription needed

## 🚀 Quick Start

### 1. Prerequisites

- **Docker & Docker Compose** installed
- **Python 3.11+** with pip
- **Git** for cloning repositories

### 2. One-Command Setup

```bash
# Navigate to the course directory
cd "Building and Evaluating Data Agents"

# Run the automated setup script
./setup-local-data-agents.sh

# This will:
# - Start PostgreSQL and Chroma containers
# - Create database schema and sample data
# - Initialize vector database with meeting notes
# - Generate environment configuration files
```

### 3. Configure API Keys

Update your API keys in the environment files:

```bash
# Copy template to .env for each lesson
cp L2/env.template.local L2/.env
cp L3/env.template.local L3/.env
# ... repeat for L4, L5, L6

# Edit the .env files to add your API keys:
# OPENAI_API_KEY=your_actual_openai_key
# TAVILY_API_KEY=your_actual_tavily_key
```

### 4. Verify Setup

```bash
# Run the validation script
python scripts/test-setup.py

# Should show all tests passing ✅
```

### 5. Run the Lessons

Open any lesson notebook (L2-L6) and run the cells. They should work seamlessly with your local data!

## 📊 Sample Data Overview

### Structured Data (PostgreSQL)
- **25+ sales records** with realistic deal values, statuses, and dates
- **Company information** for various industries and sizes
- **Sales rep performance** data with quotas and territories
- **Pre-built views** for common analytics queries

### Unstructured Data (Chroma)
- **15+ meeting transcripts** from sales conversations
- **Diverse meeting types**: Discovery, Technical, Proposal, Executive
- **Rich metadata**: Company names, dates, participants, deal IDs
- **Semantic search** capabilities for natural language queries

## 🔧 Configuration Details

### Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `POSTGRES_HOST` | PostgreSQL server | `localhost` |
| `POSTGRES_PORT` | PostgreSQL port | `5432` |
| `POSTGRES_USER` | Database user | `agent_user` |
| `POSTGRES_PASSWORD` | Database password | `password` |
| `POSTGRES_DB` | Database name | `sales_intelligence` |
| `CHROMA_HOST` | Chroma server | `localhost` |
| `CHROMA_PORT` | Chroma port | `8000` |
| `OPENAI_API_KEY` | OpenAI API key | *Required* |
| `TAVILY_API_KEY` | Tavily search API | *Required* |

### Docker Services

```yaml
# PostgreSQL Database
postgres:
  image: postgres:latest
  ports: ["5432:5432"]
  
# Chroma Vector Database  
chroma:
  image: chromadb/chroma:latest
  ports: ["8000:8000"]
```

## 🛠️ Management Commands

### Start/Stop Services
```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs postgres
docker-compose logs chroma
```

### Database Management
```bash
# Connect to PostgreSQL
docker exec -it postgres-data-agent psql -U agent_user -d sales_intelligence

# View tables
\dt data.*

# Sample query
SELECT company_name, deal_value FROM data.sales_metrics WHERE deal_status = 'Closed Won';
```

### Chroma Management
```bash
# Check Chroma status
curl http://localhost:8000/api/v1/heartbeat

# View collections (requires Python)
python -c "import chromadb; client = chromadb.HttpClient(); print(client.list_collections())"
```

## 🔍 Testing Queries

### Structured Data Examples
```sql
-- Top deals by value
SELECT company_name, deal_value, deal_status 
FROM data.sales_metrics 
WHERE deal_status = 'Closed Won' 
ORDER BY deal_value DESC 
LIMIT 5;

-- Sales rep performance
SELECT sales_rep, COUNT(*) as deals, SUM(deal_value) as total_value
FROM data.sales_metrics 
GROUP BY sales_rep 
ORDER BY total_value DESC;

-- Pipeline by product line
SELECT product_line, COUNT(*) as deals, AVG(deal_value) as avg_value
FROM data.sales_metrics 
GROUP BY product_line;
```

### Vector Search Examples
```python
import chromadb

client = chromadb.HttpClient(host="localhost", port=8000)
collection = client.get_collection("meeting_notes")

# Search for security-related discussions
results = collection.query(
    query_texts=["security compliance audit"],
    n_results=3
)

# Search by company
results = collection.query(
    query_texts=["Acme Corporation"],
    n_results=2
)
```

## 🐛 Troubleshooting

### Common Issues

**1. "Connection refused" errors**
```bash
# Check if containers are running
docker ps

# Restart if needed
docker-compose restart
```

**2. "No module named 'adapters'" errors**
```bash
# Ensure you're in the correct directory
cd "Building and Evaluating Data Agents"

# Check Python path
python -c "import sys; print(sys.path)"
```

**3. "Permission denied" errors**
```bash
# Fix script permissions
chmod +x setup-local-data-agents.sh
chmod +x scripts/test-setup.py
```

**4. Empty query results**
```bash
# Verify data was loaded
python scripts/test-setup.py

# Re-run setup if needed
./setup-local-data-agents.sh --clean
```

### Getting Help

1. **Run the test script**: `python scripts/test-setup.py`
2. **Check container logs**: `docker-compose logs`
3. **Verify environment**: Check your `.env` files
4. **Clean restart**: `./setup-local-data-agents.sh --clean`

## 📈 Performance Expectations

- **Query Response Time**: < 2 seconds for most queries
- **Setup Time**: 5-10 minutes for complete setup
- **Memory Usage**: ~1GB RAM for both containers
- **Storage**: ~100MB for sample data

## 🔄 Migration Back to Snowflake

If you want to switch back to Snowflake later:

1. Set up your Snowflake credentials in the `.env` files
2. The code automatically falls back to Snowflake if local PostgreSQL is unavailable
3. No code changes needed - the adapters handle both seamlessly

## 🎓 Learning Benefits

This local setup helps you:
- **Understand the data layer** - see exactly what queries are generated
- **Debug more easily** - full access to logs and data
- **Experiment freely** - modify data and test different scenarios
- **Learn SQL and vector search** - hands-on experience with both technologies
- **Reduce costs** - no cloud service fees while learning

---

**Happy Learning!** 🚀

You now have a fully functional local data agents environment that provides the same capabilities as the cloud-based Snowflake setup, but with complete control and transparency.
