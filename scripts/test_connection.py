from db_connection import WordPressDB

# Test the database connection
db = WordPressDB()
if db.test_connection():
    print("Connection test successful!")
    
    # Test query to get WooCommerce product count
    query = "SELECT COUNT(*) as count FROM wp_posts WHERE post_type = 'product'"
    result = db.execute_query(query)
    if result:
        print(f"Number of products in WooCommerce: {result[0]['count']}")

db.close()
