import sqlite3


class LocationsDB:
    def __init__(self, db_file):
        self.db = sqlite3.connect(db_file, check_same_thread=False)
        self.sql = self.db.cursor()

    def close(self):
        self.db.close()

    def add_location(self, location):
        try:
            self.sql.execute("INSERT INTO `locations` (`location`) VALUES (?)", (location,))
        except Exception as e:
            print(e, "add_location")
        return self.db.commit()

    def edit_location(self, location, new_location):
        try:
            self.sql.execute("UPDATE `locations` SET location = ? WHERE location = ?", (new_location, location,))
        except Exception as e:
            print(e, "edit_location")
        return self.db.commit()

    def get_all_locations(self):
        try:
            result = self.sql.execute("SELECT location FROM locations")
            return result.fetchall()
        except Exception as e:
            print(e, "get_all_locations")

    def delete_location(self, location):
        try:
            self.sql.execute("DELETE FROM locations WHERE location = ?", (location,))
        except Exception as e:
            print('delete_location')
        return self.db.commit()
