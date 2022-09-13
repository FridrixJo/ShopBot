import sqlite3


class CategoriesDB:
    def __init__(self, db_file):
        self.db = sqlite3.connect(db_file, check_same_thread=False)
        self.sql = self.db.cursor()

    def close(self):
        self.db.close()

    def add_category(self, product_name, category):
        try:
            self.sql.execute("INSERT INTO `categories` (`name`, `category`) VALUES (?, ?)", (product_name, category))
        except Exception as e:
            print(e, "add_category")
        return self.db.commit()

    def edit_category_name(self, product_name, category_name, new_category_name):
        try:
            self.sql.execute("UPDATE `categories` SET category = ? WHERE name = ? AND category = ?", (new_category_name, product_name, category_name,))
        except Exception as e:
            print(e, "edit_category_name")
        return self.db.commit()

    def get_all_categories_by_product(self, product_name):
        try:
            result = self.sql.execute("SELECT category FROM categories WHERE name = ?", (product_name,))
            return result.fetchall()
        except Exception as e:
            print(e, "get_all_categories_by_product")

    def delete_category_by_name(self, product_name, category):
        try:
            self.sql.execute("DELETE FROM categories WHERE name = ? AND category = ?", (product_name, category))
        except Exception as e:
            print('delete_category_by_name')
        return self.db.commit()

    def set_price(self, product_name, category, price):
        try:
            self.sql.execute("UPDATE `categories` SET price = ? WHERE name = ? AND category = ?", (price, product_name, category,))
        except Exception as e:
            print(e, "set_price")
        return self.db.commit()

    def get_price(self, product_name, category):
        try:
            result = self.sql.execute("SELECT price FROM categories WHERE name = ? AND category = ?", (product_name, category))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_price")
