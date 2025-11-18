#!/usr/bin/env python3
"""Quick script to query the books table schema"""
import asyncio
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/bookstore.db"

async def get_table_schema():
    async_engine = create_async_engine(DATABASE_URL)
    async_session = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=async_engine,
        class_=AsyncSession
    )
    
    async with async_session() as session:
        query = text("""
            SELECT 
                column_name,
                data_type,
                character_maximum_length,
                numeric_precision,
                numeric_scale,
                is_nullable,
                column_default,
                ordinal_position
            FROM information_schema.columns 
            WHERE table_schema = 'public' AND table_name = 'books'
            ORDER BY ordinal_position;
        """)
        result = await session.execute(query)
        rows = result.fetchall()
        
        print("Books Table Schema:")
        print("=" * 80)
        for row in rows:
            col_name, data_type, char_max_len, num_precision, num_scale, is_nullable, col_default, _ = row
            col_info = f"{col_name:20} {data_type}"
            
            if char_max_len:
                col_info += f"({char_max_len})"
            elif num_precision:
                if num_scale:
                    col_info += f"({num_precision},{num_scale})"
                else:
                    col_info += f"({num_precision})"
            
            if is_nullable == 'NO':
                col_info += " NOT NULL"
            
            if col_default:
                col_info += f" DEFAULT {col_default}"
            
            print(col_info)
        
        await async_engine.dispose()

if __name__ == "__main__":
    asyncio.run(get_table_schema())


