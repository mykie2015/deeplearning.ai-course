# Snowflake Command Translations for Local Setup

This document explains how Snowflake-specific commands are handled in the local PostgreSQL setup.

## Automatic Command Handling

The `LocalSnowparkSession` automatically handles Snowflake-specific commands:

### 1. USE Commands (Skipped)
These commands don't exist in PostgreSQL and are safely skipped:

```sql
USE WAREHOUSE SALES_INTELLIGENCE_WH  -- ✅ Skipped
USE DATABASE SALES_INTELLIGENCE      -- ✅ Skipped  
USE SCHEMA DATA                      -- ✅ Skipped
```

**Result**: Returns `{"STATUS": "SKIPPED", "MESSAGE": "..."}`

### 2. SHOW Commands (Translated)
These are automatically translated to PostgreSQL equivalents:

```sql
SHOW TABLES    -- ✅ Translated to PostgreSQL information_schema query
SHOW DATABASES -- ✅ Translated to pg_database query  
SHOW SCHEMAS   -- ✅ Translated to information_schema.schemata query
```

**Result**: Returns actual PostgreSQL data in Snowflake-compatible format

### 3. Schema References (Translated)
Database.schema.table references are automatically converted:

```sql
-- Snowflake format:
SELECT * FROM sales_intelligence.data.sales_metrics

-- Automatically becomes:
SELECT * FROM data.sales_metrics  -- ✅ PostgreSQL format
```

## What You See in Notebooks

When running notebook cells with Snowflake commands, you'll see helpful messages:

```
ℹ️  Skipping Snowflake-specific command: USE WAREHOUSE SALES_INTELLIGENCE_WH
ℹ️  Translating Snowflake SHOW command: SHOW TABLES  
ℹ️  Translated schema reference: select * from data.sales_metrics limit 5
```

## Available Tables

Your local PostgreSQL setup includes these tables in the `data` schema:

- `sales_metrics` - Main sales data with deals, values, and status
- `companies` - Company information  
- `sales_reps` - Sales representative details
- `rep_performance` - Performance metrics view
- `sales_summary` - Summary statistics view

## No Code Changes Needed

All lesson notebooks work without modification! The adapter layer handles all translations automatically.
