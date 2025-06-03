import aiomysql
import asyncio

# Global connection pool
pool = None

async def init_pool():
    """Initialize MySQL connection pool."""
    global pool
    try:
        pool = await aiomysql.create_pool(
            host="localhost",
            port=3306,
            user="root",
            password="",  # Empty password as per your setup
            db="patient_db",
            autocommit=True,
            minsize=1,
            maxsize=10
        )
        print("Database connection pool initialized successfully")
        # Create company table
        conn = await pool.acquire()
        try:
            async with await conn.cursor() as cursor:
                await cursor.execute("""
                    CREATE TABLE IF NOT EXISTS company (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        location VARCHAR(100) NOT NULL
                    )
                """)
                await conn.commit()
                print("Company table created or verified")
        except Exception as e:
            print(f"Error creating company table: {str(e)}")
            raise
        finally:
            conn.close()  # Release connection back to pool
        return pool
    except aiomysql.Error as e:
        print("MySQL pool initialization error: {e}")
        return None
    except Exception as e:
        print("Unexpected error in pool initialization: {str(e)}")
        return None

async def get_db_connection():
    """Get a connection from the pool."""
    global pool
    if pool is None:
        pool = await init_pool()
        if pool is None:
            print("Failed to initialize connection pool")
            return None
    try:
        conn = await pool.acquire()
        print("Database connection acquired")
        return conn
    except aiomysql.Error as e:
        print(f"MySQL connection error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error in database connection: {str(e)}")
        return None

async def close_pool():
    """Close the connection pool."""
    global pool
    if pool is not None:
        pool.close()
        await pool.wait_closed()
        print("Database connection pool closed")
        pool = None