"""
Local Snowpark Session Adapter
This module provides a drop-in replacement for Snowflake Snowpark Session
using PostgreSQL as the backend.
"""

import os
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional, Dict, Any, List
import warnings

class LocalSnowparkSession:
    """
    Drop-in replacement for Snowflake Snowpark Session using PostgreSQL
    """
    
    def __init__(self, connection_params: Dict[str, Any]):
        """Initialize with PostgreSQL connection parameters"""
        self.connection_params = connection_params
        self._connection = None
        self._connect()
    
    def _connect(self):
        """Establish PostgreSQL connection"""
        try:
            self._connection = psycopg2.connect(
                host=self.connection_params.get("host", "localhost"),
                port=self.connection_params.get("port", 5432),
                user=self.connection_params.get("user"),
                password=self.connection_params.get("password"),
                database=self.connection_params.get("database"),
            )
            self._connection.autocommit = True
        except psycopg2.Error as e:
            raise ConnectionError(f"Failed to connect to PostgreSQL: {e}")
    
    def sql(self, query: str):
        """Execute SQL query - mimics Snowpark Session.sql() interface"""
        return LocalSnowparkResult(self._connection, query)
    
    def close(self):
        """Close the database connection"""
        if self._connection:
            self._connection.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class LocalSnowparkResult:
    """
    Drop-in replacement for Snowpark query results
    """
    
    def __init__(self, connection, query: str):
        self.connection = connection
        self.query = query
        self._results = None
    
    def collect(self) -> List[Dict[str, Any]]:
        """Execute query and return results as list of dictionaries"""
        if self._results is None:
            # Handle Snowflake-specific commands that don't exist in PostgreSQL
            query_upper = self.query.strip().upper()
            
            # Skip Snowflake-specific USE commands
            if query_upper.startswith('USE WAREHOUSE') or query_upper.startswith('USE DATABASE') or query_upper.startswith('USE SCHEMA'):
                print(f"ℹ️  Skipping Snowflake-specific command: {self.query.strip()}")
                self._results = [{"STATUS": "SKIPPED", "MESSAGE": f"Snowflake command '{self.query.strip()}' not applicable to PostgreSQL"}]
                return self._results
            
            # Handle SHOW commands
            if query_upper.startswith('SHOW'):
                print(f"ℹ️  Translating Snowflake SHOW command: {self.query.strip()}")
                if 'TABLES' in query_upper:
                    # Translate SHOW TABLES to PostgreSQL equivalent
                    translated_query = """
                    SELECT table_name as "NAME", 'TABLE' as "KIND" 
                    FROM information_schema.tables 
                    WHERE table_schema = 'data'
                    ORDER BY table_name
                    """
                elif 'DATABASES' in query_upper:
                    # Show databases
                    translated_query = "SELECT datname as \"NAME\" FROM pg_database WHERE datistemplate = false"
                elif 'SCHEMAS' in query_upper:
                    # Show schemas
                    translated_query = "SELECT schema_name as \"NAME\" FROM information_schema.schemata WHERE schema_name NOT IN ('information_schema', 'pg_catalog', 'pg_toast')"
                else:
                    # Generic fallback for other SHOW commands
                    self._results = [{"STATUS": "UNSUPPORTED", "MESSAGE": f"SHOW command '{self.query.strip()}' not supported in local setup"}]
                    return self._results
                
                # Execute the translated query
                self.query = translated_query
            
            # Handle schema references - translate Snowflake database.schema.table to PostgreSQL schema.table
            if 'sales_intelligence.data.' in self.query:
                self.query = self.query.replace('sales_intelligence.data.', 'data.')
                print(f"ℹ️  Translated schema reference: {self.query.strip()}")
            
            try:
                with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(self.query)
                    
                    # Handle different query types
                    if cursor.description:
                        # SELECT query - convert to uppercase keys to match Snowflake behavior
                        rows = cursor.fetchall()
                        self._results = []
                        for row in rows:
                            # Convert all keys to uppercase to match Snowflake's behavior
                            uppercase_row = {key.upper(): value for key, value in dict(row).items()}
                            self._results.append(uppercase_row)
                    else:
                        # Non-SELECT query (INSERT, UPDATE, DELETE, etc.)
                        self._results = [{"AFFECTED_ROWS": cursor.rowcount}]
                        
            except psycopg2.Error as e:
                raise RuntimeError(f"SQL execution failed: {e}")
        
        return self._results
    
    def to_pandas(self) -> pd.DataFrame:
        """Convert results to pandas DataFrame - mimics Snowpark interface"""
        results = self.collect()
        if not results:
            return pd.DataFrame()
        
        # Convert to DataFrame - column names are already uppercase from collect()
        df = pd.DataFrame(results)
        
        return df


def create_local_snowpark_session() -> Optional[LocalSnowparkSession]:
    """
    Create a local Snowpark session using PostgreSQL connection parameters
    """
    # Try to get PostgreSQL parameters first
    postgres_params = {
        "host": os.getenv("POSTGRES_HOST"),
        "port": int(os.getenv("POSTGRES_PORT", "5432")),
        "user": os.getenv("POSTGRES_USER"),
        "password": os.getenv("POSTGRES_PASSWORD"),
        "database": os.getenv("POSTGRES_DB"),
    }
    
    # Check if PostgreSQL parameters are available
    if all([postgres_params["host"], postgres_params["user"], postgres_params["password"], postgres_params["database"]]):
        try:
            return LocalSnowparkSession(postgres_params)
        except Exception as e:
            warnings.warn(f"Failed to create local PostgreSQL session: {e}")
            return None
    
    # Fallback: try Snowflake parameters (for backward compatibility)
    snowflake_params = {
        "account": os.getenv("SNOWFLAKE_ACCOUNT"),
        "user": os.getenv("SNOWFLAKE_USER"),
        "password": os.getenv("SNOWFLAKE_PAT"),
        "database": os.getenv("SNOWFLAKE_DATABASE"),
        "schema": os.getenv("SNOWFLAKE_SCHEMA"),
        "role": os.getenv("SNOWFLAKE_ROLE"),
        "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
    }
    
    # Check if Snowflake parameters are available
    if all([snowflake_params["account"], snowflake_params["user"], snowflake_params["password"]]):
        try:
            # Import Snowflake modules only when needed
            from snowflake.snowpark import Session
            return Session.builder.configs(snowflake_params).create()
        except ImportError:
            warnings.warn("Snowflake modules not available, cannot create Snowflake session")
            return None
        except Exception as e:
            warnings.warn(f"Failed to create Snowflake session: {e}")
            return None
    
    # No valid configuration found
    return None


# Compatibility function to maintain existing interface
def get_session():
    """Get or create a session (PostgreSQL preferred, Snowflake fallback)"""
    return create_local_snowpark_session()
