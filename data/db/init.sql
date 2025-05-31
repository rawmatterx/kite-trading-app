-- Create additional database roles if needed
-- CREATE USER readonly WITH PASSWORD 'readonly';
-- GRANT CONNECT ON DATABASE kiteapp TO readonly;
-- GRANT USAGE ON SCHEMA public TO readonly;
-- GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly;
-- ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO readonly;

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create additional schemas if needed
-- CREATE SCHEMA IF NOT EXISTS reporting;
-- GRANT USAGE ON SCHEMA reporting TO readonly;
-- ALTER DEFAULT PRIVILEGES IN SCHEMA reporting GRANT SELECT ON TABLES TO readonly;
