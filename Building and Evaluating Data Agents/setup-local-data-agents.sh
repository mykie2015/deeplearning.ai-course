#!/bin/bash

# Setup Local Data Agents - Replace Snowflake with PostgreSQL + Chroma
# This script sets up local infrastructure for the "Building and Evaluating Data Agents" course

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
POSTGRES_CONTAINER="postgres-data-agent"
CHROMA_CONTAINER="chroma-vector-db"
POSTGRES_USER="agent_user"
POSTGRES_PASSWORD="password"
POSTGRES_DB="sales_intelligence"
POSTGRES_PORT="5432"
CHROMA_PORT="8000"

echo -e "${BLUE}🚀 Setting up Local Data Agents Infrastructure${NC}"
echo "This will replace Snowflake with PostgreSQL + Chroma for local development"
echo ""

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        echo -e "${RED}❌ Docker is not running. Please start Docker and try again.${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ Docker is running${NC}"
}

# Function to check if container exists and is running
check_container() {
    local container_name=$1
    if docker ps -q -f name=$container_name | grep -q .; then
        echo -e "${YELLOW}⚠️  Container $container_name is already running${NC}"
        return 0
    elif docker ps -aq -f name=$container_name | grep -q .; then
        echo -e "${YELLOW}⚠️  Container $container_name exists but is stopped. Removing...${NC}"
        docker rm $container_name
        return 1
    else
        return 1
    fi
}

# Function to wait for service to be ready
wait_for_service() {
    local service_name=$1
    local port=$2
    local max_attempts=30
    local attempt=1
    
    echo -e "${YELLOW}⏳ Waiting for $service_name to be ready...${NC}"
    
    while [ $attempt -le $max_attempts ]; do
        if nc -z localhost $port 2>/dev/null; then
            echo -e "${GREEN}✅ $service_name is ready!${NC}"
            return 0
        fi
        echo -n "."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    echo -e "${RED}❌ $service_name failed to start within $((max_attempts * 2)) seconds${NC}"
    return 1
}

# Function to setup PostgreSQL
setup_postgresql() {
    echo -e "${BLUE}📊 Setting up PostgreSQL database...${NC}"
    
    if check_container $POSTGRES_CONTAINER; then
        echo -e "${GREEN}✅ PostgreSQL container is already running${NC}"
    else
        echo "Starting PostgreSQL container..."
        docker run --name $POSTGRES_CONTAINER \
            -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
            -e POSTGRES_USER=$POSTGRES_USER \
            -e POSTGRES_DB=$POSTGRES_DB \
            -p $POSTGRES_PORT:5432 \
            -v postgres_data:/var/lib/postgresql/data \
            -d postgres:latest
        
        # Wait for PostgreSQL to be ready
        wait_for_service "PostgreSQL" $POSTGRES_PORT
    fi
    
    # Create schema and sample data
    echo "Creating database schema..."
    docker exec $POSTGRES_CONTAINER psql -U $POSTGRES_USER -d $POSTGRES_DB -c "
        CREATE SCHEMA IF NOT EXISTS data;
        
        DROP TABLE IF EXISTS data.sales_metrics;
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
        
        CREATE INDEX IF NOT EXISTS idx_company_name ON data.sales_metrics(company_name);
        CREATE INDEX IF NOT EXISTS idx_deal_status ON data.sales_metrics(deal_status);
        CREATE INDEX IF NOT EXISTS idx_close_date ON data.sales_metrics(close_date);
    "
    
    # Insert sample data
    echo "Inserting sample CRM data..."
    docker exec $POSTGRES_CONTAINER psql -U $POSTGRES_USER -d $POSTGRES_DB -c "
        INSERT INTO data.sales_metrics (company_name, deal_value, sales_rep, close_date, deal_status, product_line) VALUES
        ('Acme Corporation', 150000.00, 'John Smith', '2024-03-15', 'Closed Won', 'Enterprise Software'),
        ('TechStart Inc', 75000.00, 'Jane Doe', '2024-03-20', 'Negotiation', 'Cloud Services'),
        ('Global Dynamics', 250000.00, 'Mike Johnson', '2024-02-28', 'Closed Won', 'AI Platform'),
        ('InnovateCorp', 45000.00, 'Sarah Wilson', '2024-04-05', 'Proposal', 'Data Analytics'),
        ('NextGen Solutions', 180000.00, 'David Brown', '2024-03-10', 'Qualified', 'Machine Learning'),
        ('FutureTech Ltd', 95000.00, 'Emily Davis', '2024-04-12', 'Negotiation', 'Cloud Services'),
        ('DataMax Systems', 320000.00, 'Robert Taylor', '2024-01-20', 'Closed Won', 'Enterprise Software'),
        ('CloudFirst Inc', 67000.00, 'Lisa Anderson', '2024-04-18', 'Discovery', 'Data Analytics'),
        ('AI Innovations', 210000.00, 'James Wilson', '2024-02-14', 'Closed Won', 'AI Platform'),
        ('SmartData Corp', 85000.00, 'Maria Garcia', '2024-04-25', 'Proposal', 'Machine Learning'),
        ('TechPioneer Ltd', 125000.00, 'Chris Martinez', '2024-03-30', 'Qualified', 'Cloud Services'),
        ('DataVision Inc', 195000.00, 'Amanda Thompson', '2024-01-15', 'Closed Won', 'Enterprise Software'),
        ('CloudLogic Systems', 78000.00, 'Kevin Lee', '2024-04-08', 'Negotiation', 'Data Analytics'),
        ('AI Forward Corp', 340000.00, 'Jennifer White', '2024-02-05', 'Closed Won', 'AI Platform'),
        ('SmartCloud Inc', 92000.00, 'Daniel Harris', '2024-04-20', 'Discovery', 'Machine Learning')
        ON CONFLICT DO NOTHING;
    "
    
    echo -e "${GREEN}✅ PostgreSQL setup completed${NC}"
}

# Function to setup Chroma Vector Database
setup_chroma() {
    echo -e "${BLUE}🔍 Setting up Chroma Vector Database...${NC}"
    
    if check_container $CHROMA_CONTAINER; then
        echo -e "${GREEN}✅ Chroma container is already running${NC}"
    else
        echo "Starting Chroma container..."
        docker run --name $CHROMA_CONTAINER \
            -p $CHROMA_PORT:8000 \
            -v chroma_data:/chroma/chroma \
            -d chromadb/chroma:latest
        
        # Wait for Chroma to be ready
        wait_for_service "Chroma" $CHROMA_PORT
    fi
    
    echo -e "${GREEN}✅ Chroma setup completed${NC}"
}

# Function to create sample meeting notes data
setup_sample_data() {
    echo -e "${BLUE}📝 Setting up sample meeting notes...${NC}"
    
    # Create Python script to populate Chroma with sample data
    cat > temp_setup_chroma.py << 'EOF'
import chromadb
import json
import sys

try:
    # Connect to Chroma
    client = chromadb.HttpClient(host="localhost", port=8000)
    
    # Create or get collection
    try:
        collection = client.get_collection("meeting_notes")
        print("✅ Collection 'meeting_notes' already exists")
    except:
        collection = client.create_collection("meeting_notes")
        print("✅ Created new collection 'meeting_notes'")
    
    # Sample meeting notes data
    meeting_notes = [
        {
            "id": "MTG001",
            "document": "Customer expressed strong interest in our enterprise solution. Key concerns were around security and compliance. They need integration with their existing CRM system. Budget approved for Q2 implementation. Next steps: technical demo scheduled for next week.",
            "metadata": {
                "meeting_id": "MTG001",
                "company_name": "Acme Corporation",
                "meeting_date": "2024-03-10",
                "participants": "John Smith, Customer CTO, Customer VP Sales",
                "meeting_type": "Discovery"
            }
        },
        {
            "id": "MTG002", 
            "document": "Technical requirements discussion. Customer needs cloud-native solution with 99.9% uptime SLA. Discussed scalability requirements for 10,000+ users. Integration with Salesforce is critical. Pricing discussion - budget range $70-80k confirmed.",
            "metadata": {
                "meeting_id": "MTG002",
                "company_name": "TechStart Inc",
                "meeting_date": "2024-03-18",
                "participants": "Jane Doe, Customer CTO, Technical Team",
                "meeting_type": "Technical"
            }
        },
        {
            "id": "MTG003",
            "document": "Final proposal presentation. Customer very satisfied with our AI platform capabilities. Discussed implementation timeline - 6 months phased rollout. Security audit requirements discussed. Legal team needs to review contract terms. Decision expected by month end.",
            "metadata": {
                "meeting_id": "MTG003",
                "company_name": "Global Dynamics", 
                "meeting_date": "2024-02-25",
                "participants": "Mike Johnson, Customer CEO, Customer CFO",
                "meeting_type": "Proposal"
            }
        },
        {
            "id": "MTG004",
            "document": "Initial discovery call. Customer evaluating data analytics solutions. Current pain points: manual reporting, lack of real-time insights. Team of 50 analysts. Looking for self-service BI capabilities. Competitive evaluation in progress.",
            "metadata": {
                "meeting_id": "MTG004",
                "company_name": "InnovateCorp",
                "meeting_date": "2024-04-02",
                "participants": "Sarah Wilson, Customer Analytics Director",
                "meeting_type": "Discovery"
            }
        },
        {
            "id": "MTG005",
            "document": "Machine learning platform demo. Customer impressed with AutoML capabilities. Discussed model deployment and monitoring features. Integration with their existing data lake is essential. ROI projections look promising. Technical POC proposed for next month.",
            "metadata": {
                "meeting_id": "MTG005",
                "company_name": "NextGen Solutions",
                "meeting_date": "2024-03-08",
                "participants": "David Brown, Customer Data Science Team",
                "meeting_type": "Demo"
            }
        }
    ]
    
    # Add documents to collection
    for note in meeting_notes:
        try:
            collection.add(
                documents=[note["document"]],
                ids=[note["id"]],
                metadatas=[note["metadata"]]
            )
            print(f"✅ Added meeting note: {note['metadata']['company_name']}")
        except Exception as e:
            print(f"⚠️  Note {note['id']} might already exist: {e}")
    
    print(f"✅ Sample meeting notes setup completed")
    print(f"Collection count: {collection.count()}")
    
except Exception as e:
    print(f"❌ Error setting up Chroma data: {e}")
    sys.exit(1)
EOF

    # Run the setup script
    if command -v python3 &> /dev/null; then
        python3 -c "
import subprocess
import sys
try:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'chromadb', '--quiet'])
    print('✅ ChromaDB installed')
except:
    print('⚠️  Failed to install ChromaDB - you may need to install it manually')
"
        python3 temp_setup_chroma.py
    else
        echo -e "${YELLOW}⚠️  Python3 not found. Please install ChromaDB and run the setup manually.${NC}"
    fi
    
    # Clean up
    rm -f temp_setup_chroma.py
    
    echo -e "${GREEN}✅ Sample data setup completed${NC}"
}

# Function to create environment template
create_env_template() {
    echo -e "${BLUE}⚙️  Creating environment configuration...${NC}"
    
    cat > .env.local << EOF
# Local Data Agents Configuration
# Replace Snowflake variables with these local alternatives

# OpenAI API (required for embeddings and LLM)
OPENAI_API_KEY=your_openai_api_key_here

# Tavily API (for web research)
TAVILY_API_KEY=your_tavily_api_key_here

# PostgreSQL Configuration (replaces Snowflake)
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=agent_user
POSTGRES_PASSWORD=password
POSTGRES_DB=sales_intelligence
POSTGRES_SCHEMA=data

# Chroma Vector Database Configuration
CHROMA_HOST=localhost
CHROMA_PORT=8000
CHROMA_COLLECTION=meeting_notes

# Legacy Snowflake variables (for compatibility - leave empty)
SNOWFLAKE_ACCOUNT=
SNOWFLAKE_USER=
SNOWFLAKE_PAT=
SNOWFLAKE_DATABASE=
SNOWFLAKE_SCHEMA=
SNOWFLAKE_ROLE=
SNOWFLAKE_WAREHOUSE=
EOF

    echo -e "${GREEN}✅ Environment template created: .env.local${NC}"
    echo -e "${YELLOW}📝 Please update your API keys in .env.local${NC}"
}

# Function to verify setup
verify_setup() {
    echo -e "${BLUE}🔍 Verifying setup...${NC}"
    
    # Check PostgreSQL connection
    if docker exec $POSTGRES_CONTAINER psql -U $POSTGRES_USER -d $POSTGRES_DB -c "SELECT COUNT(*) FROM data.sales_metrics;" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ PostgreSQL connection verified${NC}"
        RECORD_COUNT=$(docker exec $POSTGRES_CONTAINER psql -U $POSTGRES_USER -d $POSTGRES_DB -t -c "SELECT COUNT(*) FROM data.sales_metrics;" | tr -d ' ')
        echo -e "   📊 Sales records available: $RECORD_COUNT"
    else
        echo -e "${RED}❌ PostgreSQL connection failed${NC}"
    fi
    
    # Check Chroma connection
    if curl -s http://localhost:$CHROMA_PORT/api/v1/heartbeat > /dev/null; then
        echo -e "${GREEN}✅ Chroma connection verified${NC}"
    else
        echo -e "${RED}❌ Chroma connection failed${NC}"
    fi
    
    echo ""
    echo -e "${GREEN}🎉 Local Data Agents setup completed successfully!${NC}"
    echo ""
    echo -e "${BLUE}📋 Next Steps:${NC}"
    echo "1. Update API keys in .env.local file"
    echo "2. Copy .env.local to each lesson folder (L2/, L3/, L4/, L5/, L6/)"
    echo "3. Run the lesson notebooks - they should work with local data!"
    echo ""
    echo -e "${BLUE}🔗 Service URLs:${NC}"
    echo "   PostgreSQL: localhost:$POSTGRES_PORT"
    echo "   Chroma:     localhost:$CHROMA_PORT"
    echo ""
    echo -e "${BLUE}🛠️  Management Commands:${NC}"
    echo "   Stop services:    docker stop $POSTGRES_CONTAINER $CHROMA_CONTAINER"
    echo "   Start services:   docker start $POSTGRES_CONTAINER $CHROMA_CONTAINER"
    echo "   Remove services:  docker rm -f $POSTGRES_CONTAINER $CHROMA_CONTAINER"
    echo "   View logs:        docker logs $POSTGRES_CONTAINER"
    echo ""
}

# Function to show help
show_help() {
    echo "Local Data Agents Setup Script"
    echo ""
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  --help, -h     Show this help message"
    echo "  --clean        Remove existing containers and start fresh"
    echo "  --verify       Only run verification checks"
    echo "  --stop         Stop all containers"
    echo "  --start        Start stopped containers"
    echo ""
    echo "Examples:"
    echo "  $0              # Run full setup"
    echo "  $0 --clean     # Clean install"
    echo "  $0 --verify    # Check if services are running"
    echo ""
}

# Function to clean existing setup
clean_setup() {
    echo -e "${YELLOW}🧹 Cleaning existing setup...${NC}"
    
    echo "Stopping containers..."
    docker stop $POSTGRES_CONTAINER $CHROMA_CONTAINER 2>/dev/null || true
    
    echo "Removing containers..."
    docker rm $POSTGRES_CONTAINER $CHROMA_CONTAINER 2>/dev/null || true
    
    echo "Removing volumes..."
    docker volume rm postgres_data chroma_data 2>/dev/null || true
    
    echo -e "${GREEN}✅ Cleanup completed${NC}"
}

# Function to stop services
stop_services() {
    echo -e "${YELLOW}⏹️  Stopping services...${NC}"
    docker stop $POSTGRES_CONTAINER $CHROMA_CONTAINER 2>/dev/null || true
    echo -e "${GREEN}✅ Services stopped${NC}"
}

# Function to start services
start_services() {
    echo -e "${BLUE}▶️  Starting services...${NC}"
    docker start $POSTGRES_CONTAINER $CHROMA_CONTAINER 2>/dev/null || true
    sleep 5
    wait_for_service "PostgreSQL" $POSTGRES_PORT
    wait_for_service "Chroma" $CHROMA_PORT
    echo -e "${GREEN}✅ Services started${NC}"
}

# Main execution
main() {
    case "${1:-}" in
        --help|-h)
            show_help
            exit 0
            ;;
        --clean)
            clean_setup
            echo "Starting fresh setup..."
            ;;
        --verify)
            verify_setup
            exit 0
            ;;
        --stop)
            stop_services
            exit 0
            ;;
        --start)
            start_services
            exit 0
            ;;
        "")
            echo -e "${BLUE}🚀 Starting Local Data Agents setup...${NC}"
            ;;
        *)
            echo -e "${RED}❌ Unknown option: $1${NC}"
            show_help
            exit 1
            ;;
    esac
    
    # Run setup steps
    check_docker
    setup_postgresql
    setup_chroma
    setup_sample_data
    create_env_template
    verify_setup
}

# Check for required tools
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is required but not installed.${NC}"
    echo "Please install Docker and try again."
    exit 1
fi

if ! command -v nc &> /dev/null; then
    echo -e "${YELLOW}⚠️  netcat (nc) not found. Service readiness checks may not work.${NC}"
fi

# Run main function with all arguments
main "$@"
