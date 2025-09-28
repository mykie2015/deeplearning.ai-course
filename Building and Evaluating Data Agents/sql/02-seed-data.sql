-- Seed data for sales intelligence system
-- This provides comprehensive test data matching Snowflake examples

-- Insert sample companies
INSERT INTO data.companies (company_name, industry, size, location, website) VALUES
('Acme Corporation', 'Manufacturing', 'Enterprise', 'New York, NY', 'acme-corp.com'),
('TechStart Inc', 'Technology', 'Startup', 'San Francisco, CA', 'techstart.com'),
('Global Dynamics', 'Consulting', 'Enterprise', 'Chicago, IL', 'globaldynamics.com'),
('InnovateCorp', 'Healthcare', 'Mid-Market', 'Boston, MA', 'innovatecorp.com'),
('NextGen Solutions', 'Financial Services', 'Enterprise', 'Austin, TX', 'nextgensolutions.com'),
('FutureTech Ltd', 'Technology', 'Mid-Market', 'Seattle, WA', 'futuretech.com'),
('DataMax Systems', 'Data & Analytics', 'Enterprise', 'Denver, CO', 'datamax.com'),
('CloudFirst Inc', 'Cloud Services', 'Startup', 'Portland, OR', 'cloudfirst.com'),
('AI Innovations', 'Artificial Intelligence', 'Mid-Market', 'Atlanta, GA', 'ai-innovations.com'),
('SmartData Corp', 'Data Science', 'Mid-Market', 'Miami, FL', 'smartdata.com')
ON CONFLICT (company_name) DO NOTHING;

-- Insert sample sales reps
INSERT INTO data.sales_reps (name, email, territory, hire_date, quota) VALUES
('John Smith', 'john.smith@company.com', 'Northeast', '2022-01-15', 2000000.00),
('Jane Doe', 'jane.doe@company.com', 'West Coast', '2021-03-10', 1800000.00),
('Mike Johnson', 'mike.johnson@company.com', 'Midwest', '2020-06-01', 2200000.00),
('Sarah Wilson', 'sarah.wilson@company.com', 'Northeast', '2023-02-20', 1500000.00),
('David Brown', 'david.brown@company.com', 'South', '2021-09-15', 1900000.00),
('Emily Davis', 'emily.davis@company.com', 'West Coast', '2022-11-01', 1700000.00),
('Robert Taylor', 'robert.taylor@company.com', 'Midwest', '2019-04-12', 2400000.00),
('Lisa Anderson', 'lisa.anderson@company.com', 'South', '2023-01-08', 1600000.00),
('James Wilson', 'james.wilson@company.com', 'Northeast', '2020-12-03', 2100000.00),
('Maria Garcia', 'maria.garcia@company.com', 'West Coast', '2022-07-25', 1750000.00)
ON CONFLICT (email) DO NOTHING;

-- Insert comprehensive sales metrics data
INSERT INTO data.sales_metrics (company_name, deal_value, sales_rep, close_date, deal_status, product_line) VALUES
-- Closed Won deals
('Acme Corporation', 150000.00, 'John Smith', '2024-03-15', 'Closed Won', 'Enterprise Software'),
('Global Dynamics', 250000.00, 'Mike Johnson', '2024-02-28', 'Closed Won', 'AI Platform'),
('DataMax Systems', 320000.00, 'Robert Taylor', '2024-01-20', 'Closed Won', 'Enterprise Software'),
('AI Innovations', 210000.00, 'James Wilson', '2024-02-14', 'Closed Won', 'AI Platform'),
('DataVision Inc', 195000.00, 'Amanda Thompson', '2024-01-15', 'Closed Won', 'Enterprise Software'),
('AI Forward Corp', 340000.00, 'Jennifer White', '2024-02-05', 'Closed Won', 'AI Platform'),

-- Negotiation stage
('TechStart Inc', 75000.00, 'Jane Doe', '2024-03-20', 'Negotiation', 'Cloud Services'),
('FutureTech Ltd', 95000.00, 'Emily Davis', '2024-04-12', 'Negotiation', 'Cloud Services'),
('CloudLogic Systems', 78000.00, 'Kevin Lee', '2024-04-08', 'Negotiation', 'Data Analytics'),

-- Proposal stage
('InnovateCorp', 45000.00, 'Sarah Wilson', '2024-04-05', 'Proposal', 'Data Analytics'),
('SmartData Corp', 85000.00, 'Maria Garcia', '2024-04-25', 'Proposal', 'Machine Learning'),

-- Qualified leads
('NextGen Solutions', 180000.00, 'David Brown', '2024-03-10', 'Qualified', 'Machine Learning'),
('TechPioneer Ltd', 125000.00, 'Chris Martinez', '2024-03-30', 'Qualified', 'Cloud Services'),

-- Discovery stage
('CloudFirst Inc', 67000.00, 'Lisa Anderson', '2024-04-18', 'Discovery', 'Data Analytics'),
('SmartCloud Inc', 92000.00, 'Daniel Harris', '2024-04-20', 'Discovery', 'Machine Learning'),

-- Additional deals for comprehensive testing
('MegaCorp Industries', 450000.00, 'John Smith', '2024-01-10', 'Closed Won', 'Enterprise Software'),
('StartupXYZ', 35000.00, 'Jane Doe', '2024-04-15', 'Discovery', 'Cloud Services'),
('Enterprise Solutions LLC', 280000.00, 'Mike Johnson', '2024-03-05', 'Negotiation', 'AI Platform'),
('DataCorp Ltd', 165000.00, 'Sarah Wilson', '2024-02-20', 'Closed Won', 'Data Analytics'),
('CloudTech Systems', 98000.00, 'David Brown', '2024-04-10', 'Proposal', 'Cloud Services'),
('IntelliData Inc', 220000.00, 'Emily Davis', '2024-01-25', 'Closed Won', 'Machine Learning'),

-- Lost deals for realistic scenarios
('CompetitorChoice Corp', 150000.00, 'Robert Taylor', '2024-03-01', 'Closed Lost', 'Enterprise Software'),
('BudgetConstrained LLC', 85000.00, 'Lisa Anderson', '2024-02-15', 'Closed Lost', 'Data Analytics'),

-- Future opportunities
('PipelineCorp', 300000.00, 'James Wilson', '2024-05-15', 'Discovery', 'AI Platform'),
('FutureClient Inc', 125000.00, 'Maria Garcia', '2024-05-20', 'Qualified', 'Machine Learning'),
('NextQuarter LLC', 175000.00, 'John Smith', '2024-06-01', 'Discovery', 'Enterprise Software')

ON CONFLICT DO NOTHING;

-- Create view for easy querying (similar to Snowflake views)
CREATE OR REPLACE VIEW data.sales_summary AS
SELECT 
    deal_status,
    product_line,
    COUNT(*) as deal_count,
    SUM(deal_value) as total_value,
    AVG(deal_value) as avg_deal_value,
    MIN(deal_value) as min_deal_value,
    MAX(deal_value) as max_deal_value
FROM data.sales_metrics 
GROUP BY deal_status, product_line
ORDER BY total_value DESC;

-- Create view for rep performance
CREATE OR REPLACE VIEW data.rep_performance AS
SELECT 
    sales_rep,
    COUNT(*) as total_deals,
    COUNT(CASE WHEN deal_status = 'Closed Won' THEN 1 END) as won_deals,
    SUM(CASE WHEN deal_status = 'Closed Won' THEN deal_value ELSE 0 END) as won_value,
    SUM(deal_value) as total_pipeline_value,
    ROUND(
        COUNT(CASE WHEN deal_status = 'Closed Won' THEN 1 END) * 100.0 / COUNT(*), 2
    ) as win_rate_percent
FROM data.sales_metrics 
GROUP BY sales_rep
ORDER BY won_value DESC;

-- Grant permissions on views
GRANT SELECT ON data.sales_summary TO agent_user;
GRANT SELECT ON data.rep_performance TO agent_user;
