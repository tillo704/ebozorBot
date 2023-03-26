from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(
        self,
        command,
        *args,
        fetch: bool = False,
        fetchval: bool = False,
        fetchrow: bool = False,
        execute: bool = False,
    ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_cats(self):
        sql = """
        CREATE TABLE IF NOT EXISTS cats (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL UNIQUE,
        description varchar(255) NULL,
        image_url VARCHAR(255) NOT NULL 
        );
        """
        await self.execute(sql, execute=True)
    
    
    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL UNIQUE,
        username varchar(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE 
        );
        """
        await self.execute(sql, execute=True)

    
    async def create_table_cart_items(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Items (
        id SERIAL PRIMARY KEY,
        cart_id BIGINT NOT NULL UNIQUE,
        product_id BIGINT NOT NULL,
        quantity BIGINT NOT NULL        
        );
        """
        await self.execute(sql, execute=True)
    
    async def create_table_carts(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Carts (
        id SERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL UNIQUE        
        );
        """
        await self.execute(sql, execute=True)



    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, username, telegram_id):
        sql = "INSERT INTO users (full_name, username, telegram_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, full_name, username, telegram_id, fetchrow=True)
    
    async def add_cat(self, title, description, image_url):
        sql = "INSERT INTO Cats ( title, description, image_url) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, title, description, image_url, fetchrow=True)
    

    async def create_cart(self, user_id):
        sql = "INSERT INTO Carts ( user_id) VALUES($1) returning *"
        return await self.execute(sql, user_id, fetchrow=True)
    
    async def add_cart_item(self, cart_id,product_id,quantity):
        sql = "INSERT INTO Items ( cart_id,product_id,quantity) VALUES($1,$2,$3) returning *"
        return await self.execute(sql, cart_id,product_id,quantity, fetchrow=True)

    
    async def add_praduct(self, title, description, image_url,price,cat_id):
        sql = "INSERT INTO Praducts ( title, description, image_url,price,cat_id) VALUES($1, $2, $3, $4, $5) returning *"
        return await self.execute(sql, title, description, image_url, price,cat_id ,fetchrow=True)


    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)
    
    async def select_all_cats(self):
        sql = "SELECT * FROM Cats"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)
    
    async def select_user_cart(self, **kwargs):
        sql = "SELECT * FROM Carts WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)
    

    async def select_cart_items(self, **kwargs):
        sql = "SELECT * FROM Items WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters,fetchrow=True)
    
    async def select_user_cart_items(self, **kwargs):
        sql = "SELECT * FROM Items WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters,fetch=True)

    async def select_category(self, **kwargs):
        sql = "SELECT * FROM Cats WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)
    

    async def select_product(self, **kwargs):
        sql = "SELECT * FROM Praducts WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)



    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def update_cart_item(self,cart_id,product_id,quantity ):
        sql = "UPDATE Items SET quantity=$1 WHERE cart_id=$2 AND product_id=$3"
        return await self.execute(sql, quantity,cart_id,product_id, execute=True)
    
    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)
   
    async def delete_cats(self):
        await self.execute("DELETE FROM Cats WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)
