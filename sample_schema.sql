-- ❄️ Snowflake Customer Dashboard - Sample Schema
-- Run these commands in your Snowflake console to create the required tables

-- ==================================================
-- Customer Details Table
-- ==================================================
CREATE TABLE IF NOT EXISTS CUSTOMER_DETAILS (
    CUSTOMER_ID VARCHAR(50) PRIMARY KEY,
    CUSTOMER_NAME VARCHAR(100) NOT NULL,
    EMAIL VARCHAR(100),
    PHONE VARCHAR(20),
    ADDRESS VARCHAR(200),
    CITY VARCHAR(50),
    STATE VARCHAR(50),
    COUNTRY VARCHAR(50),
    POSTAL_CODE VARCHAR(20),
    ACCOUNT_TYPE VARCHAR(50),
    SUBSCRIPTION_LEVEL VARCHAR(50),
    CREATED_DATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    LAST_LOGIN_DATE TIMESTAMP,
    STATUS VARCHAR(20) DEFAULT 'Active'
);

-- ==================================================
-- Customer Configurations Table
-- ==================================================
CREATE TABLE IF NOT EXISTS CUSTOMER_CONFIGURATIONS (
    CONFIG_ID VARCHAR(50) PRIMARY KEY,
    CUSTOMER_ID VARCHAR(50),
    CUSTOMER_NAME VARCHAR(100),
    CONFIGURATION_TYPE VARCHAR(100),
    CONFIGURATION_VALUE VARCHAR(500),
    CREATED_DATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    UPDATED_DATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    STATUS VARCHAR(20) DEFAULT 'Active',
    REGION VARCHAR(50),
    FOREIGN KEY (CUSTOMER_ID) REFERENCES CUSTOMER_DETAILS(CUSTOMER_ID)
);

-- ==================================================
-- Sample Data - Customer Details
-- ==================================================
INSERT INTO CUSTOMER_DETAILS VALUES
('CUST_0001', 'Acme Corporation', 'contact@acme.com', '+1-555-0101', '123 Business St', 'New York', 'NY', 'USA', '10001', 'Enterprise', 'Premium', '2024-01-15 10:00:00', '2024-01-25 14:30:00', 'Active'),
('CUST_0002', 'TechStart Inc', 'info@techstart.com', '+1-555-0102', '456 Innovation Ave', 'San Francisco', 'CA', 'USA', '94102', 'Startup', 'Standard', '2024-01-16 11:30:00', '2024-01-24 09:15:00', 'Active'),
('CUST_0003', 'Global Solutions Ltd', 'hello@globalsol.com', '+44-20-7123-4567', '789 International Way', 'London', '', 'UK', 'SW1A 1AA', 'Enterprise', 'Premium', '2024-01-17 09:45:00', '2024-01-25 16:20:00', 'Active'),
('CUST_0004', 'DataDriven Co', 'team@datadriven.co', '+1-555-0104', '321 Analytics Blvd', 'Austin', 'TX', 'USA', '73301', 'SMB', 'Standard', '2024-01-18 13:20:00', '2024-01-23 11:45:00', 'Inactive'),
('CUST_0005', 'CloudFirst Systems', 'support@cloudfirst.io', '+1-555-0105', '654 Cloud Ave', 'Seattle', 'WA', 'USA', '98101', 'Enterprise', 'Premium', '2024-01-19 15:10:00', '2024-01-25 13:30:00', 'Active'),
('CUST_0006', 'AI Innovations', 'contact@aiinnovations.ai', '+33-1-12-34-56-78', '987 Future St', 'Paris', '', 'France', '75001', 'Startup', 'Basic', '2024-01-20 08:30:00', '2024-01-22 10:15:00', 'Pending'),
('CUST_0007', 'SecureNet Ltd', 'info@securenet.com', '+49-30-12345678', '147 Security Rd', 'Berlin', '', 'Germany', '10115', 'Enterprise', 'Premium', '2024-01-21 12:00:00', '2024-01-25 15:45:00', 'Active'),
('CUST_0008', 'Mobile First Inc', 'hello@mobilefirst.app', '+1-555-0108', '258 Mobile Way', 'Los Angeles', 'CA', 'USA', '90210', 'SMB', 'Standard', '2024-01-22 14:45:00', '2024-01-24 12:30:00', 'Active'),
('CUST_0009', 'GreenTech Solutions', 'team@greentech.eco', '+61-2-1234-5678', '369 Eco Street', 'Sydney', 'NSW', 'Australia', '2000', 'Enterprise', 'Premium', '2024-01-23 16:20:00', '2024-01-25 17:00:00', 'Active'),
('CUST_0010', 'FinTech Pioneers', 'contact@fintechpioneers.com', '+1-555-0110', '741 Financial Ave', 'Chicago', 'IL', 'USA', '60601', 'Startup', 'Standard', '2024-01-24 10:15:00', '2024-01-25 08:45:00', 'Active');

-- ==================================================
-- Sample Data - Customer Configurations
-- ==================================================
INSERT INTO CUSTOMER_CONFIGURATIONS VALUES
('CONF_0001', 'CUST_0001', 'Acme Corporation', 'Security', 'Two-Factor Authentication Enabled', '2024-01-15 10:30:00', '2024-01-25 14:00:00', 'Active', 'US-East'),
('CONF_0002', 'CUST_0001', 'Acme Corporation', 'Performance', 'High-Performance Warehouse', '2024-01-15 10:35:00', '2024-01-20 16:30:00', 'Active', 'US-East'),
('CONF_0003', 'CUST_0002', 'TechStart Inc', 'Integration', 'API Rate Limit: 1000/hour', '2024-01-16 12:00:00', '2024-01-24 09:30:00', 'Active', 'US-West'),
('CONF_0004', 'CUST_0002', 'TechStart Inc', 'Security', 'IP Whitelist Configuration', '2024-01-16 12:05:00', '2024-01-22 11:15:00', 'Active', 'US-West'),
('CONF_0005', 'CUST_0003', 'Global Solutions Ltd', 'Reporting', 'Daily Automated Reports', '2024-01-17 10:00:00', '2024-01-25 16:45:00', 'Active', 'Europe'),
('CONF_0006', 'CUST_0003', 'Global Solutions Ltd', 'Performance', 'Auto-scaling Enabled', '2024-01-17 10:05:00', '2024-01-23 14:20:00', 'Active', 'Europe'),
('CONF_0007', 'CUST_0004', 'DataDriven Co', 'Custom', 'Machine Learning Pipeline', '2024-01-18 13:45:00', '2024-01-19 15:30:00', 'Inactive', 'US-Central'),
('CONF_0008', 'CUST_0005', 'CloudFirst Systems', 'Security', 'Advanced Encryption', '2024-01-19 15:30:00', '2024-01-25 13:45:00', 'Active', 'US-West'),
('CONF_0009', 'CUST_0005', 'CloudFirst Systems', 'Integration', 'Multi-Cloud Sync', '2024-01-19 15:35:00', '2024-01-24 10:20:00', 'Active', 'US-West'),
('CONF_0010', 'CUST_0006', 'AI Innovations', 'Performance', 'GPU Computing Cluster', '2024-01-20 09:00:00', '2024-01-22 10:30:00', 'Pending', 'Europe'),
('CONF_0011', 'CUST_0007', 'SecureNet Ltd', 'Security', 'Zero-Trust Architecture', '2024-01-21 12:30:00', '2024-01-25 16:00:00', 'Active', 'Europe'),
('CONF_0012', 'CUST_0008', 'Mobile First Inc', 'Integration', 'Mobile SDK Configuration', '2024-01-22 15:00:00', '2024-01-24 12:45:00', 'Active', 'US-West'),
('CONF_0013', 'CUST_0009', 'GreenTech Solutions', 'Reporting', 'Carbon Footprint Tracking', '2024-01-23 16:45:00', '2024-01-25 17:15:00', 'Active', 'Asia-Pacific'),
('CONF_0014', 'CUST_0009', 'GreenTech Solutions', 'Custom', 'Sustainability Metrics', '2024-01-23 16:50:00', '2024-01-25 12:30:00', 'Active', 'Asia-Pacific'),
('CONF_0015', 'CUST_0010', 'FinTech Pioneers', 'Security', 'Financial Compliance Suite', '2024-01-24 10:30:00', '2024-01-25 09:00:00', 'Active', 'US-Central');

-- ==================================================
-- Optional: Create Views for Common Queries
-- ==================================================

-- Active customers with their configuration count
CREATE OR REPLACE VIEW ACTIVE_CUSTOMERS_SUMMARY AS
SELECT 
    cd.CUSTOMER_ID,
    cd.CUSTOMER_NAME,
    cd.ACCOUNT_TYPE,
    cd.SUBSCRIPTION_LEVEL,
    cd.STATUS,
    COUNT(cc.CONFIG_ID) as TOTAL_CONFIGURATIONS,
    COUNT(CASE WHEN cc.STATUS = 'Active' THEN 1 END) as ACTIVE_CONFIGURATIONS,
    MAX(cc.UPDATED_DATE) as LAST_CONFIG_UPDATE
FROM CUSTOMER_DETAILS cd
LEFT JOIN CUSTOMER_CONFIGURATIONS cc ON cd.CUSTOMER_ID = cc.CUSTOMER_ID
WHERE cd.STATUS = 'Active'
GROUP BY cd.CUSTOMER_ID, cd.CUSTOMER_NAME, cd.ACCOUNT_TYPE, cd.SUBSCRIPTION_LEVEL, cd.STATUS
ORDER BY TOTAL_CONFIGURATIONS DESC;

-- Configuration summary by type and region
CREATE OR REPLACE VIEW CONFIGURATION_SUMMARY AS
SELECT 
    CONFIGURATION_TYPE,
    REGION,
    STATUS,
    COUNT(*) as CONFIG_COUNT,
    COUNT(DISTINCT CUSTOMER_ID) as UNIQUE_CUSTOMERS
FROM CUSTOMER_CONFIGURATIONS
GROUP BY CONFIGURATION_TYPE, REGION, STATUS
ORDER BY CONFIG_COUNT DESC;

-- ==================================================
-- Grant Permissions (adjust role as needed)
-- ==================================================
GRANT SELECT ON CUSTOMER_DETAILS TO ROLE ACCOUNTADMIN;
GRANT SELECT ON CUSTOMER_CONFIGURATIONS TO ROLE ACCOUNTADMIN;
GRANT SELECT ON ACTIVE_CUSTOMERS_SUMMARY TO ROLE ACCOUNTADMIN;
GRANT SELECT ON CONFIGURATION_SUMMARY TO ROLE ACCOUNTADMIN;

-- ==================================================
-- Verification Queries
-- ==================================================
-- Run these to verify your data was inserted correctly

-- Check customer count
SELECT 'Customer Details' as TABLE_NAME, COUNT(*) as RECORD_COUNT FROM CUSTOMER_DETAILS
UNION ALL
SELECT 'Customer Configurations' as TABLE_NAME, COUNT(*) as RECORD_COUNT FROM CUSTOMER_CONFIGURATIONS;

-- Check data distribution
SELECT 
    STATUS,
    COUNT(*) as CUSTOMER_COUNT,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as PERCENTAGE
FROM CUSTOMER_DETAILS
GROUP BY STATUS
ORDER BY CUSTOMER_COUNT DESC;

-- Test the views
SELECT * FROM ACTIVE_CUSTOMERS_SUMMARY LIMIT 5;
SELECT * FROM CONFIGURATION_SUMMARY LIMIT 10; 