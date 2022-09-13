import sqlite3


class ProductsDB:
    def __init__(self, db_file):
        self.db = sqlite3.connect(db_file, check_same_thread=False)
        self.sql = self.db.cursor()

    def close(self):
        self.db.close()

    def add_products(self, product_name):
        try:
            self.sql.execute("INSERT INTO `products` (`name`) VALUES (?)", (product_name,))
        except Exception as e:
            print(e, "add_product")
        return self.db.commit()

    def edit_product_name(self, name, new_name):
        try:
            self.sql.execute("UPDATE `products` SET name = ? WHERE name = ?", (new_name, name,))
        except Exception as e:
            print(e, "edit_name")
        return self.db.commit()

    def get_all_products(self):
        try:
            result = self.sql.execute("SELECT name FROM products")
            return result.fetchall()
        except Exception as e:
            print(e, "get_all_products")

    def delete_product(self, name):
        try:
            self.sql.execute("DELETE FROM products WHERE name = ?", (name,))
        except Exception as e:
            print('delete_product')
        return self.db.commit()

    def set_description(self, name, description):
        try:
            self.sql.execute("UPDATE `products` SET description = ? WHERE name = ?", (description, name,))
        except Exception as e:
            print(e, "set_description")
        return self.db.commit()

    def get_description(self, name):
        try:
            result = self.sql.execute("SELECT description FROM products WHERE name = ?", (name,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_description")

    def set_photo_id(self, name, photo_id):
        try:
            self.sql.execute("UPDATE `products` SET photo_id = ? WHERE name = ?", (photo_id, name,))
        except Exception as e:
            print(e, "set_photo_id")
        return self.db.commit()

    def get_photo_id(self, name):
        try:
            result = self.sql.execute("SELECT photo_id FROM products WHERE name = ?", (name,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_photo_id")

