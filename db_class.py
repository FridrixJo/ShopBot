from asyncpg import Connection


class DBCommands:
    def __init__(self, db):
        self.pool: Connection = db

    # USERS

    ADD_USER = "INSERT INTO users (user_id, name) VALUES ($1, $2)"
    USER_EXISTS = "SELECT user_id FROM users WHERE user_id = $1"
    COUNT_USERS = "SELECT COUNT(*) FROM users"
    ALL_USERS = "SELECT user_id FROM users"
    GET_USER_NAME = "SELECT name FROM users WHERE user_id = $1"

    # STATEMENT

    SET_STATEMENT_MENU = "UPDATE statement SET menu = $1 WHERE id = $2"
    GET_STATEMENT_MENU = "SELECT menu FROM statement WHERE id = $1"

    SET_STATEMENT_WORK_TEXT = "UPDATE statement SET work_text = $1 WHERE id = $2"
    GET_STATEMENT_WORK_TEXT = "SELECT work_text FROM statement WHERE id = $1"

    SET_STATEMENT_SUPPORT = "UPDATE statement SET support = $1 WHERE id = $2"
    GET_STATEMENT_SUPPORT = "SELECT support FROM statement WHERE id = $1"

    SET_STATEMENT_BTC_WALLET = "UPDATE statement SET btc_wallet = $1 WHERE id = $2"
    GET_STATEMENT_BTC_WALLET = "SELECT btc_wallet FROM statement WHERE id = $1"

    # REQUESTS

    REQUEST_EXISTS = "SELECT request_id FROM requests WHERE request_id = $1"
    REQUEST_USER_EXISTS = "SELECT user_id FROM requests WHERE user_id = $1"

    ADD_REQUEST = "INSERT INTO requests (request_id, user_id, name) VALUES ($1, $2, $3)"
    DELETE_REQUEST = "DELETE FROM requests WHERE request_id = $1"

    GET_ALL_REQUESTS = "SELECT request_id FROM requests"
    COUNT_REQUESTS = "SELECT COUNT(*) FROM requests"

    GET_REQUEST_USER_ID = "SELECT user_id FROM requests WHERE request_id = $1"

    GET_REQUEST_NAME = "SELECT name FROM requests WHERE request_id = $1"

    # PRODUCTS

    ADD_PRODUCT = "INSERT INTO products (name, description, photo_id) VALUES ($1, $2, $3)"
    DELETE_PRODUCT = "DELETE FROM products WHERE name = $1"

    ALL_PRODUCTS = "SELECT name FROM products"
    COUNT_PRODUCTS = "SELECT COUNT(*) FROM products"

    EDIT_PRODUCT_NAME = "UPDATE products SET name = $1 WHERE name = $2"
    EDIT_PRODUCT_DESCR = "UPDATE products SET description = $1 WHERE name = $2"
    EDIT_PRODUCT_PHOTO = "UPDATE products SET photo_id = $1 WHERE name = $2"

    GET_PRODUCT_DESCR = "SELECT description FROM products WHERE name = $1"
    GET_PRODUCT_PHOTO = "SELECT photo_id FROM products WHERE name = $1"

    # CATEGORIES

    ADD_CATEGORY = "INSERT INTO categories (name, category, price) VALUES ($1, $2, $3)"
    DELETE_CATEGORY = "DELETE FROM categories WHERE category = $1 AND name = $2"

    ALL_CATEGORIES_BY_PRODUCT = "SELECT category FROM categories WHERE name = $1"
    COUNT_CATEGORIES = "SELECT COUNT(*) FROM categories"

    EDIT_CATEGORY = "UPDATE categories SET category = $1 WHERE name = $2 AND category = $3"
    EDIT_PRICE = "UPDATE categories SET price = $1 WHERE name = $2 AND category = $3"

    GET_PRICE = "SELECT price FROM categories WHERE name = $1 AND category = $2"

    # LOCATIONS

    ADD_LOCATION = "INSERT INTO locations (location) VALUES ($1)"
    DELETE_LOCATION = "DELETE FROM locations WHERE location = $1"

    ALL_LOCATIONS = "SELECT location FROM locations"
    COUNT_LOCATIONS = "SELECT COUNT(*) FROM locations"

    EDIT_LOCATION = "UPDATE locations SET location = $1 WHERE location = $2"

    # USERS FUNCTIONS

    async def add_user(self, user_id: str, name: str):
        try:
            return await self.pool.fetchval(self.ADD_USER, user_id, name)
        except Exception as e:
            print(e, 'add_user')

    async def get_users_count(self):
        try:
            return await self.pool.fetchval(self.COUNT_USERS)
        except Exception as e:
            print(e, 'user_count')

    async def get_all_users(self):
        try:
            return await self.pool.fetch(self.ALL_USERS)
        except Exception as e:
            print(e, 'get_all_users')

    async def get_name(self, user_id: str):
        try:
            return await self.pool.fetchval(self.GET_USER_NAME, user_id)
        except Exception as e:
            print(e, 'get_user_name')

    async def user_exists(self, user_id: str):
        try:
            result = await self.pool.fetch(self.USER_EXISTS, user_id)
            return bool(len(result))
        except Exception as e:
            print(e, 'user_exists')

    # STATEMENT FUNCTIONS

    async def set_statement_menu(self, menu: str, id=1):
        try:
            await self.pool.fetchval(self.SET_STATEMENT_MENU, menu, id)
        except Exception as e:
            print(e, 'set_statement_menu')

    async def get_statement_menu(self, id=1):
        try:
            return await self.pool.fetchval(self.GET_STATEMENT_MENU, id)
        except Exception as e:
            print(e, 'get_statement_menu')

    async def set_statement_work_text(self, work_text: str, id=1):
        try:
            await self.pool.fetchval(self.SET_STATEMENT_WORK_TEXT, work_text, id)
        except Exception as e:
            print(e, 'set_statement_work_text')

    async def get_statement_work_text(self, id=1):
        try:
            return await self.pool.fetchval(self.GET_STATEMENT_WORK_TEXT, id)
        except Exception as e:
            print(e, 'get_statement_work_text')

    async def set_statement_support(self, support: str, id=1):
        try:
            await self.pool.fetchval(self.SET_STATEMENT_SUPPORT, support, id)
        except Exception as e:
            print(e, 'set_statement_support')

    async def get_statement_support(self, id=1):
        try:
            return await self.pool.fetchval(self.GET_STATEMENT_SUPPORT, id)
        except Exception as e:
            print(e, 'get_statement_support')

    async def set_statement_btc_wallet(self, btc_wallet: str, id=1):
        try:
            await self.pool.fetchval(self.SET_STATEMENT_BTC_WALLET, btc_wallet, id)
        except Exception as e:
            print(e, 'set_statement_btc_wallet')

    async def get_statement_btc_wallet(self, id=1):
        try:
            return await self.pool.fetchval(self.GET_STATEMENT_BTC_WALLET, id)
        except Exception as e:
            print(e, 'get_statement_btc_wallet')

    # REQUESTS FUNCTIONS

    async def add_request(self, request_id: str, user_id: str, name: str):
        try:
            return await self.pool.fetchval(self.ADD_REQUEST, request_id, user_id, name)
        except Exception as e:
            print(e, 'add_request')

    async def delete_request(self, request_id):
        try:
            return await self.pool.fetchval(self.DELETE_REQUEST, request_id)
        except Exception as e:
            print(e, 'delete_request')

    async def get_requests_count(self):
        try:
            return await self.pool.fetchval(self.COUNT_REQUESTS)
        except Exception as e:
            print(e, 'requests_count')

    async def get_request_name(self, request_id: str):
        try:
            return await self.pool.fetchval(self.GET_REQUEST_NAME, request_id)
        except Exception as e:
            print(e, 'get_request_name')

    async def get_request_user_id(self, request_id: str):
        try:
            return await self.pool.fetchval(self.GET_REQUEST_USER_ID, request_id)
        except Exception as e:
            print(e, 'get_request_user_id')

    async def request_exists(self, request_id: str):
        try:
            result = await self.pool.fetch(self.REQUEST_EXISTS, request_id)
            return bool(len(result))
        except Exception as e:
            print(e, 'request_exists')

    async def request_user_exists(self, user_id: str):
        try:
            result = await self.pool.fetch(self.REQUEST_USER_EXISTS, user_id)
            return bool(len(result))
        except Exception as e:
            print(e, 'request_user_exists')

    # PRODUCTS FUNCTIONS

    async def add_product(self, product_name: str, product_descr: str, product_photo: str):
        try:
            return await self.pool.fetchval(self.ADD_PRODUCT, product_name, product_descr, product_photo)
        except Exception as e:
            print(e, 'add_product')

    async def delete_product(self, product_name):
        try:
            return await self.pool.fetchval(self.DELETE_PRODUCT, product_name)
        except Exception as e:
            print(e, 'delete_product')

    async def get_products_count(self):
        try:
            return await self.pool.fetchval(self.COUNT_PRODUCTS)
        except Exception as e:
            print(e, 'products_count')

    async def get_all_products(self):
        try:
            return await self.pool.fetch(self.ALL_PRODUCTS)
        except Exception as e:
            print(e, 'get_all_products')

    async def edit_product_name(self, product_name, name):
        try:
            return await self.pool.fetchval(self.EDIT_PRODUCT_NAME, name, product_name)
        except Exception as e:
            print(e, 'edit_product_name')

    async def edit_product_descr(self, product_name, descr):
        try:
            return await self.pool.fetchval(self.EDIT_PRODUCT_DESCR, descr, product_name)
        except Exception as e:
            print(e, 'edit_product_descr')

    async def edit_product_photo(self, product_name, photo):
        try:
            return await self.pool.fetchval(self.EDIT_PRODUCT_PHOTO, photo, product_name)
        except Exception as e:
            print(e, 'edit_product_descr')

    async def get_product_descr(self, product_name):
        try:
            return await self.pool.fetchval(self.GET_PRODUCT_DESCR, product_name)
        except Exception as e:
            print(e, 'get_product_descr')

    async def get_product_photo(self, product_name):
        try:
            return await self.pool.fetchval(self.GET_PRODUCT_PHOTO, product_name)
        except Exception as e:
            print(e, 'get_product_photo')

    # CATEGORIES FUNCTIONS

    async def add_category(self, product_name: str, category: str, price: str):
        try:
            return await self.pool.fetchval(self.ADD_CATEGORY, product_name, category, price)
        except Exception as e:
            print(e, 'add_category')

    async def delete_category(self, product_name, category):
        try:
            return await self.pool.fetchval(self.DELETE_CATEGORY, category, product_name)
        except Exception as e:
            print(e, 'delete_category')

    async def get_categories_count(self):
        try:
            return await self.pool.fetchval(self.COUNT_CATEGORIES)
        except Exception as e:
            print(e, 'categories_count')

    async def get_all_categories_by_product_name(self, product_name):
        try:
            return await self.pool.fetch(self.ALL_CATEGORIES_BY_PRODUCT, product_name)
        except Exception as e:
            print(e, 'get_all_categories_by_product_name')

    async def edit_category_name(self, name, category, new_category):
        try:
            return await self.pool.fetchval(self.EDIT_CATEGORY, new_category, name, category)
        except Exception as e:
            print(e, 'edit_category_name')

    async def edit_price(self, product_name, category, price: str):
        try:
            return await self.pool.fetchval(self.EDIT_PRICE, price, product_name, category)
        except Exception as e:
            print(e, 'edit_price')

    async def get_price(self, product_name, category):
        try:
            price: str = await self.pool.fetchval(self.GET_PRICE, product_name, category)
            return price
        except Exception as e:
            print(e, 'get_price')

    # LOCATIONS FUNCTIONS

    async def add_location(self, location: str):
        try:
            return await self.pool.fetchval(self.ADD_LOCATION, location)
        except Exception as e:
            print(e, 'add_location')

    async def delete_location(self, location):
        try:
            return await self.pool.fetchval(self.DELETE_LOCATION, location)
        except Exception as e:
            print(e, 'delete_location')

    async def get_locations_count(self):
        try:
            return await self.pool.fetchval(self.COUNT_LOCATIONS)
        except Exception as e:
            print(e, 'locations_count')

    async def get_all_locations(self):
        try:
            return await self.pool.fetch(self.ALL_LOCATIONS)
        except Exception as e:
            print(e, 'get_all_locations')

    async def edit_location(self, location, new_location):
        try:
            return await self.pool.fetchval(self.EDIT_LOCATION, new_location, location)
        except Exception as e:
            print(e, 'edit_location')



