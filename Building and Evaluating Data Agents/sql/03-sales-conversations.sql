-- Create sales_conversations table for meeting transcripts
CREATE TABLE IF NOT EXISTS data.sales_conversations (
    conversation_id SERIAL PRIMARY KEY,
    deal_id INTEGER REFERENCES data.sales_metrics(deal_id),
    company_name VARCHAR(255),
    meeting_date DATE,
    meeting_type VARCHAR(50),
    participants TEXT,
    transcript_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample meeting transcripts
INSERT INTO data.sales_conversations (deal_id, company_name, meeting_date, meeting_type, participants, transcript_text) VALUES
(1, 'Acme Corporation', '2024-03-10', 'Discovery', 'John Smith (Customer CTO), Sarah Johnson (Sales Rep)', 
'Good morning John, thank you for taking the time to meet with us today. I understand you''re looking for an enterprise solution that can help streamline your operations. 

John: Yes, that''s correct. We''ve been evaluating several vendors and we''re particularly interested in your AI platform capabilities. Our main concerns are around security and compliance - we operate in a highly regulated industry.

Sarah: Absolutely, security is paramount in our solution. We have SOC 2 Type II certification and we''re compliant with GDPR, HIPAA, and other major regulatory frameworks. Can you tell me more about your current infrastructure?

John: We''re primarily cloud-based, running on AWS. We need something that can integrate seamlessly with our existing CRM system - we use Salesforce extensively. The solution needs to handle about 5,000 users initially, but we''re planning to scale to 15,000 over the next two years.

Sarah: That''s well within our capabilities. Our platform is built for enterprise scale and we have native Salesforce integration. I''d like to show you some case studies of similar implementations. We recently helped TechGlobal Inc implement a similar solution for 12,000 users.

John: That sounds promising. What about the implementation timeline? We''re hoping to have something in production by Q2.

Sarah: For a deployment of your size, we typically see 3-4 month implementation cycles. Given your Q2 target, we could definitely make that work. I''ll have our technical team prepare a detailed implementation plan for you.

John: Excellent. One more thing - budget. We''ve allocated $2.5M for this project. Is that in the right ballpark?

Sarah: Yes, that aligns well with our enterprise pricing model. I''ll prepare a detailed proposal for you by end of week. Should I include the premium support package in that?

John: Yes, please include that. We''ll need 24/7 support given our global operations.

Sarah: Perfect. I''ll get that proposal over to you by Friday. Thank you for your time today, John.'),

(2, 'TechStart Inc', '2024-03-18', 'Technical', 'Jane Doe (Customer CTO), Mike Chen (Solutions Engineer)', 
'Hi Jane, thanks for joining our technical deep-dive session today. I understand you have some specific questions about our platform architecture.

Jane: Yes, we''ve reviewed your initial proposal and we''re impressed with the feature set. However, we need to understand the technical details better. Our primary requirement is a cloud-native solution with 99.9% uptime SLA.

Mike: Absolutely. Our platform is built on a microservices architecture running on Kubernetes. We use auto-scaling and have redundancy across multiple availability zones. We consistently achieve 99.95% uptime across our customer base.

Jane: That''s good to hear. What about data processing capabilities? We generate about 10TB of data daily and need real-time analytics.

Mike: Our platform can definitely handle that volume. We use Apache Kafka for real-time data streaming and our analytics engine can process petabytes of data. We have customers processing similar volumes without any issues.

Jane: Integration is critical for us. Besides Salesforce, we also use HubSpot, Tableau, and several custom APIs. How flexible is your integration layer?

Mike: Very flexible. We have pre-built connectors for all the platforms you mentioned, plus a robust REST API for custom integrations. We also support webhooks for real-time data synchronization.

Jane: Security is obviously a concern. Can you walk me through your security model?

Mike: Of course. We implement zero-trust architecture with end-to-end encryption. All data is encrypted at rest using AES-256 and in transit using TLS 1.3. We have role-based access control and support SSO integration with SAML and OAuth.

Jane: What about compliance? We need to be SOX compliant.

Mike: We''re SOX compliant and we can provide all the necessary documentation and audit trails. We also have automated compliance reporting built into the platform.

Jane: This all sounds very promising. What would the implementation look like for our environment?

Mike: Given your requirements, I''d recommend a phased approach. Phase 1 would be core platform deployment and basic integrations - about 6 weeks. Phase 2 would be advanced analytics and custom integrations - another 4 weeks. We''d have you fully operational in about 10 weeks.

Jane: That timeline works for us. Can you send me the technical specifications and architecture diagrams?

Mike: Absolutely. I''ll have those over to you by tomorrow, along with some reference architectures from similar deployments.'),

(3, 'Global Dynamics', '2024-02-25', 'Proposal', 'Mike Johnson (Customer CEO), Lisa Wang (Account Executive)', 
'Good afternoon Mike, I''m excited to present our final proposal for Global Dynamics'' digital transformation initiative.

Mike: Thank you Lisa. We''ve been very impressed with your team throughout this process. The technical demos were particularly compelling.

Lisa: I''m glad to hear that. Based on our discussions, I''ve put together a comprehensive solution that addresses all your key requirements - AI-powered analytics, seamless integration, and enterprise-grade security.

Mike: Yes, those are our top priorities. Can you walk me through the proposal?

Lisa: Certainly. We''re proposing our Enterprise AI Platform with the following components: Core analytics engine, real-time data processing, advanced visualization tools, and our premium AI modules for predictive analytics and natural language processing.

Mike: The AI capabilities are really what sets you apart from the competition. How quickly can we expect to see ROI?

Lisa: Based on similar implementations, our customers typically see 15-20% efficiency gains within the first 6 months. For an organization of your size, that translates to approximately $3-4M in annual savings.

Mike: That''s significant. What about the implementation timeline?

Lisa: We''re proposing a 6-month phased rollout. Phase 1 covers core platform deployment and basic integrations - 8 weeks. Phase 2 adds advanced analytics and AI modules - 10 weeks. Phase 3 is full deployment and optimization - 8 weeks.

Mike: That timeline aligns with our fiscal planning. We need to have everything operational by the start of our next fiscal year.

Lisa: Perfect. We can definitely meet that deadline. I''ve also included our premium support package which provides 24/7 technical support and a dedicated customer success manager.

Mike: The support package is important to us. We''re making a significant investment and we need to ensure smooth operations.

Lisa: Absolutely. Our customer success team will work closely with your IT department throughout the implementation and beyond. We also provide comprehensive training for your team.

Mike: What about the commercial terms?

Lisa: The total investment is $4.2M over three years, which includes all licensing, implementation, training, and support. We can structure the payments to align with your budget cycles.

Mike: That''s within our approved budget range. When do you need a decision?

Lisa: We''d like to have a signed agreement by month-end to ensure we can meet your implementation timeline. I can have the contracts prepared by Wednesday.

Mike: That works for us. I''ll need to get final approval from our board, but I''m confident we can move forward. This solution really addresses all our strategic objectives.

Lisa: Excellent. I''ll coordinate with our legal team to prepare the agreements. Thank you for your confidence in our solution, Mike.'),

(4, 'DataFlow Systems', '2024-04-05', 'Follow-up', 'Robert Chen (Customer VP Engineering), Alex Rodriguez (Sales Rep)', 
'Hi Robert, thanks for the follow-up call. I wanted to address the questions that came up in last week''s technical review.

Robert: Yes, our engineering team had some concerns about the scalability of your solution. We''re planning significant growth over the next 18 months.

Alex: I understand the concern. Let me share some specifics about our scalability. Our platform is designed to auto-scale based on demand. We have customers who''ve grown from 1,000 to 50,000 users without any performance degradation.

Robert: That''s reassuring. What about data processing? We expect our data volumes to increase by 300% over the next year.

Alex: Our architecture handles that easily. We use distributed processing and can scale horizontally as needed. The beauty of our cloud-native design is that scaling is transparent to your users.

Robert: Cost is always a concern with scaling. How does your pricing model work as we grow?

Alex: We have a tiered pricing model that actually becomes more cost-effective as you scale. The per-user cost decreases at higher volumes, so your unit economics improve as you grow.

Robert: That''s important for our business case. What about customization? We have some unique workflows that might need custom development.

Alex: We have a robust customization framework. Most customizations can be done through configuration rather than custom code. For unique requirements, we have a professional services team that can develop custom modules.

Robert: How long would custom development take?

Alex: It depends on complexity, but most custom modules can be developed and deployed within 4-6 weeks. We''d work closely with your team to ensure everything meets your specifications.

Robert: This addresses most of our concerns. I think we''re ready to move to the next phase. What are the next steps?

Alex: Great! I''ll set up a meeting with our implementation team to start the technical planning. We can also begin the contract process in parallel to save time.

Robert: Sounds good. Let''s target a start date of June 1st if possible.

Alex: That''s definitely achievable. I''ll have our project manager reach out to coordinate the detailed planning.');

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_sales_conversations_deal_id ON data.sales_conversations(deal_id);
CREATE INDEX IF NOT EXISTS idx_sales_conversations_company ON data.sales_conversations(company_name);
CREATE INDEX IF NOT EXISTS idx_sales_conversations_date ON data.sales_conversations(meeting_date);
