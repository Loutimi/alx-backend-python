import asyncio
import aiosqlite
import random
from typing import List, Dict, Any


async def create_sample_database():
    """Create a sample database with users table and sample data."""
    async with aiosqlite.connect("users.db") as db:
        # Create users table
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                email TEXT NOT NULL
            )
        """
        )

        # Clear existing data
        await db.execute("DELETE FROM users")

        # Insert sample data
        sample_users = [
            ("Alice Johnson", 28, "alice@email.com"),
            ("Bob Smith", 45, "bob@email.com"),
            ("Charlie Brown", 32, "charlie@email.com"),
            ("Diana Davis", 52, "diana@email.com"),
            ("Eve Wilson", 38, "eve@email.com"),
            ("Frank Miller", 41, "frank@email.com"),
            ("Grace Lee", 29, "grace@email.com"),
            ("Henry Clark", 55, "henry@email.com"),
            ("Ivy Taylor", 33, "ivy@email.com"),
            ("Jack Wilson", 47, "jack@email.com"),
        ]

        await db.executemany(
            "INSERT INTO users (name, age, email) VALUES (?, ?, ?)", sample_users
        )

        await db.commit()
        print("Sample database created with 10 users")


async def async_fetch_users() -> List[Dict[str, Any]]:
    """Fetch all users from the database."""
    print("Starting to fetch all users...")

    async with aiosqlite.connect("users.db") as db:
        # Add a small delay to simulate real database query time
        await asyncio.sleep(0.5)

        cursor = await db.execute("SELECT id, name, age, email FROM users")
        rows = await cursor.fetchall()

        users = []
        for row in rows:
            users.append({"id": row[0], "name": row[1], "age": row[2], "email": row[3]})

    print(f"Fetched {len(users)} total users")
    return users


async def async_fetch_older_users() -> List[Dict[str, Any]]:
    """Fetch users older than 40 from the database."""
    print("Starting to fetch users older than 40...")

    async with aiosqlite.connect("users.db") as db:
        # Add a small delay to simulate real database query time
        await asyncio.sleep(0.3)

        cursor = await db.execute(
            "SELECT id, name, age, email FROM users WHERE age > ?", (40,)
        )
        rows = await cursor.fetchall()

        older_users = []
        for row in rows:
            older_users.append(
                {"id": row[0], "name": row[1], "age": row[2], "email": row[3]}
            )

    print(f"Fetched {len(older_users)} users older than 40")
    return older_users


async def fetch_concurrently():
    """Execute both fetch functions concurrently using asyncio.gather."""
    print("Starting concurrent database queries...")
    start_time = asyncio.get_event_loop().time()

    # Use asyncio.gather to run both queries concurrently
    all_users, older_users = await asyncio.gather(
        async_fetch_users(), async_fetch_older_users()
    )

    end_time = asyncio.get_event_loop().time()
    execution_time = end_time - start_time

    print(f"\nConcurrent queries completed in {execution_time:.2f} seconds")
    print("=" * 50)

    # Display results
    print("\nALL USERS:")
    print("-" * 30)
    for user in all_users:
        print(
            f"ID: {user['id']}, Name: {user['name']}, Age: {user['age']}, Email: {user['email']}"
        )

    print("\nUSERS OLDER THAN 40:")
    print("-" * 30)
    for user in older_users:
        print(
            f"ID: {user['id']}, Name: {user['name']}, Age: {user['age']}, Email: {user['email']}"
        )

    return all_users, older_users


async def sequential_comparison():
    """Run the same queries sequentially for comparison."""
    print("\nRunning sequential queries for comparison...")
    start_time = asyncio.get_event_loop().time()

    # Run queries one after another
    all_users = await async_fetch_users()
    older_users = await async_fetch_older_users()

    end_time = asyncio.get_event_loop().time()
    execution_time = end_time - start_time

    print(f"Sequential queries completed in {execution_time:.2f} seconds")
    return all_users, older_users


async def main():
    """Main function to demonstrate concurrent database queries."""
    print("Asyncio Database Concurrency Demo")
    print("=" * 40)

    # Create sample database
    await create_sample_database()

    print("\n1. Running concurrent queries...")
    await fetch_concurrently()

    print("\n2. Running sequential queries for comparison...")
    await sequential_comparison()

    print("\nDemo completed!")


if __name__ == "__main__":
    # Run the concurrent fetch function
    asyncio.run(main())
