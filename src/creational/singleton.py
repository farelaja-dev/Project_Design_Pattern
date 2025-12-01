"""
SINGLETON PATTERN - Database Connection
Memastikan hanya ada satu instance koneksi database untuk Restaurant Management System
"""

import psycopg2
from psycopg2 import pool
import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()


class DatabaseConnection:
    """
    Singleton Pattern untuk Database Connection

    Teori:
    - Singleton memastikan class hanya memiliki satu instance
    - Menyediakan global access point ke instance tersebut
    - Cocok untuk resource yang expensive seperti database connection

    Use Case Restaurant:
    - Semua transaksi restaurant (order, menu, payment) pakai 1 connection pool
    - Tidak ada multiple connection yang wasteful
    - Efficient resource management untuk high-traffic restaurant

    Implementasi:
    - Menggunakan __new__ untuk control object creation
    - Menyimpan instance di class variable _instance
    - Thread-safe dengan checking sebelum create new instance
    """

    _instance: Optional["DatabaseConnection"] = None
    _connection_pool: Optional[pool.SimpleConnectionPool] = None

    def __new__(cls):
        """Override __new__ untuk implement singleton pattern"""
        if cls._instance is None:
            print("[SINGLETON] Creating new DatabaseConnection instance...")
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._initialize_pool()
        else:
            print("[SINGLETON] Reusing existing DatabaseConnection instance")
        return cls._instance

    def _initialize_pool(self):
        """Initialize connection pool"""
        try:
            # Store connection info
            self.host = os.getenv("DB_HOST", "localhost")
            self.port = os.getenv("DB_PORT", "5432")
            self.dbname = os.getenv("DB_NAME", "restaurant_db")
            self.user = os.getenv("DB_USER", "postgres")
            self.password = os.getenv("DB_PASSWORD", "")

            self._connection_pool = pool.SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                host=self.host,
                port=self.port,
                database=self.dbname,
                user=self.user,
                password=self.password,
            )
            self._is_connected = True
            print("[SINGLETON] Connection pool initialized successfully")
        except Exception as e:
            print(f"[SINGLETON ERROR] Failed to initialize connection pool: {e}")
            self._is_connected = False
            # Store connection info even if failed
            self.host = os.getenv("DB_HOST", "localhost")
            self.port = os.getenv("DB_PORT", "5432")
            self.dbname = os.getenv("DB_NAME", "restaurant_db")
            self.user = os.getenv("DB_USER", "postgres")
            self.password = "****"
            # Don't raise, allow app to continue
            print("[SINGLETON WARNING] Application will run with limited functionality")

    def get_connection(self):
        """Get connection from pool"""
        if self._connection_pool:
            return self._connection_pool.getconn()
        raise Exception("Connection pool not initialized")

    def return_connection(self, conn):
        """Return connection to pool"""
        if self._connection_pool:
            self._connection_pool.putconn(conn)

    def close_all_connections(self):
        """Close all connections in pool"""
        if self._connection_pool:
            self._connection_pool.closeall()
            print("[SINGLETON] All connections closed")

    def execute_query(self, query: str, params: tuple = None, fetch: bool = True):
        """
        Execute SQL query dengan connection dari pool

        Args:
            query: SQL query string
            params: Query parameters
            fetch: Jika True, return results; jika False, commit changes
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            if fetch:
                results = cursor.fetchall()
                cursor.close()
                return results
            else:
                conn.commit()
                cursor.close()
                return True

        except Exception as e:
            if conn:
                conn.rollback()
            print(f"[DATABASE ERROR] {e}")
            raise
        finally:
            if conn:
                self.return_connection(conn)

    def execute_query_dict(self, query: str, params: tuple = None):
        """Execute query dan return results sebagai list of dictionaries"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            columns = [desc[0] for desc in cursor.description]
            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))

            cursor.close()
            return results

        except Exception as e:
            print(f"[DATABASE ERROR] {e}")
            raise
        finally:
            if conn:
                self.return_connection(conn)

    def __repr__(self):
        return f"<DatabaseConnection Singleton at {hex(id(self))}>"


# Test Singleton Pattern
if __name__ == "__main__":
    print("=" * 60)
    print("TESTING SINGLETON PATTERN - Restaurant System")
    print("=" * 60)

    # Create multiple instances
    db1 = DatabaseConnection()
    print(f"Instance 1: {db1}")

    db2 = DatabaseConnection()
    print(f"Instance 2: {db2}")

    db3 = DatabaseConnection()
    print(f"Instance 3: {db3}")

    # Verify they're the same instance
    print(f"\ndb1 is db2: {db1 is db2}")
    print(f"db2 is db3: {db2 is db3}")
    print(f"All instances are identical: {db1 is db2 is db3}")

    # Test database query
    try:
        print("\n" + "=" * 60)
        print("TESTING DATABASE QUERIES - Restaurant Data")
        print("=" * 60)

        # Test query - count customers
        results = db1.execute_query("SELECT COUNT(*) FROM customers")
        print(f"\nTotal customers in database: {results[0][0]}")

        # Get sample customers
        customers = db1.execute_query_dict("SELECT * FROM customers LIMIT 5")
        print(f"\nSample customers:")
        for customer in customers:
            member_status = "Member" if customer["is_member"] else "Regular"
            print(f"  - {customer['name']} ({customer['phone']}) - {member_status}")

        # Get sample menu
        menu_items = db1.execute_query_dict(
            "SELECT * FROM menu_items WHERE item_type = 'food' LIMIT 5"
        )
        print(f"\nSample menu items (Food):")
        for item in menu_items:
            print(f"  - {item['item_name']}: Rp{item['base_price']:,.0f}")

    except Exception as e:
        print(f"Error testing database: {e}")
        print(
            "Make sure database is setup correctly (see database/restaurant_schema.sql)"
        )
