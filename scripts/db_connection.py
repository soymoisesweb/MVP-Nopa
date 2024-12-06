"""
Database connection handler for WordPress/WooCommerce
"""

import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

class WordPressDB:
    def __init__(self):
        self.connection = None
        try:
            config = DB_CONFIG.copy()
            unix_socket = config.pop('unix_socket', None)
            prefix = config.pop('prefix', 'wp_')
            self.prefix = prefix
            
            if unix_socket:
                config['unix_socket'] = unix_socket
            
            self.connection = mysql.connector.connect(**config)
            print("Successfully connected to the database")
        except Error as e:
            print(f"Error connecting to MySQL Database: {e}")

    def execute_query(self, query, params=None):
        """Execute a query and return results"""
        cursor = self.connection.cursor(dictionary=True)
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if query.strip().upper().startswith(('SELECT', 'SHOW')):
                return cursor.fetchall()
            else:
                self.connection.commit()
                return cursor.rowcount
        except Error as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            cursor.close()

    def close(self):
        """Close the database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed.")

    def test_connection(self):
        """Test the database connection"""
        if self.connection and self.connection.is_connected():
            cursor = self.connection.cursor()
            cursor.execute("SELECT VERSION()")
            db_version = cursor.fetchone()
            print(f"Connected to MySQL version: {db_version[0]}")
            cursor.close()
            return True
        return False
