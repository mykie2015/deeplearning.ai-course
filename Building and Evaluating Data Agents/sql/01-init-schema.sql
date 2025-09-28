-- Initialize database schema for sales intelligence
-- This script replaces Snowflake schema with PostgreSQL equivalent

-- Create the data schema to match Snowflake structure
CREATE SCHEMA IF NOT EXISTS data;

-- Create sales_metrics table matching Snowflake structure
DROP TABLE IF EXISTS data.sales_metrics;
CREATE TABLE data.sales_metrics (
    deal_id SERIAL PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    deal_value DECIMAL(10,2),
    sales_rep VARCHAR(255),
    close_date DATE,
    deal_status VARCHAR(50),
    product_line VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for optimal query performance
CREATE INDEX IF NOT EXISTS idx_sales_metrics_company_name ON data.sales_metrics(company_name);
CREATE INDEX IF NOT EXISTS idx_sales_metrics_deal_status ON data.sales_metrics(deal_status);
CREATE INDEX IF NOT EXISTS idx_sales_metrics_close_date ON data.sales_metrics(close_date);
CREATE INDEX IF NOT EXISTS idx_sales_metrics_sales_rep ON data.sales_metrics(sales_rep);
CREATE INDEX IF NOT EXISTS idx_sales_metrics_product_line ON data.sales_metrics(product_line);
CREATE INDEX IF NOT EXISTS idx_sales_metrics_deal_value ON data.sales_metrics(deal_value);

-- Create function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger to automatically update updated_at
CREATE TRIGGER update_sales_metrics_updated_at 
    BEFORE UPDATE ON data.sales_metrics 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Create additional tables for comprehensive testing
CREATE TABLE IF NOT EXISTS data.companies (
    company_id SERIAL PRIMARY KEY,
    company_name VARCHAR(255) UNIQUE NOT NULL,
    industry VARCHAR(100),
    size VARCHAR(50),
    location VARCHAR(255),
    website VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS data.sales_reps (
    rep_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    territory VARCHAR(100),
    hire_date DATE,
    quota DECIMAL(12,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Grant permissions
GRANT ALL PRIVILEGES ON SCHEMA data TO agent_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA data TO agent_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA data TO agent_user;

-- Set default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA data GRANT ALL ON TABLES TO agent_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA data GRANT ALL ON SEQUENCES TO agent_user;
