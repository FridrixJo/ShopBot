import sqlite3


class StatementDB:
    def __init__(self, db_file):
        self.db = sqlite3.connect(db_file, check_same_thread=False)
        self.sql = self.db.cursor()

    def close(self):
        self.db.close()

    def set_menu_text(self, menu, id=1):
        try:
            self.sql.execute("UPDATE `statement` SET menu = ? WHERE id = ?", (menu, id,))
        except Exception as e:
            print(e, "set_menu_text")
        return self.db.commit()

    def get_menu_text(self, id=1):
        try:
            result = self.sql.execute("SELECT menu FROM statement WHERE id = ?", (id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_menu_text")

    def set_work_text(self, work, id=1):
        try:
            self.sql.execute("UPDATE `statement` SET work = ? WHERE id = ?", (work, id,))
        except Exception as e:
            print(e, "set_work_text")
        return self.db.commit()

    def get_work_text(self, id=1):
        try:
            result = self.sql.execute("SELECT work FROM statement WHERE id = ?", (id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_work_text")

    def set_support_text(self, support, id=1):
        try:
            self.sql.execute("UPDATE `statement` SET support = ? WHERE id = ?", (support, id,))
        except Exception as e:
            print(e, "set_support_text")
        return self.db.commit()

    def get_support_text(self, id=1):
        try:
            result = self.sql.execute("SELECT support FROM statement WHERE id = ?", (id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_support_text")

    def set_btc_wallet(self, rate, id=1):
        try:
            self.sql.execute("UPDATE `statement` SET btc_wallet = ? WHERE id = ?", (rate, id,))
        except Exception as e:
            print(e, "set_btc_wallet")
        return self.db.commit()

    def get_btc_wallet(self, id=1):
        try:
            result = self.sql.execute("SELECT btc_wallet FROM statement WHERE id = ?", (id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_btc_wallet")

