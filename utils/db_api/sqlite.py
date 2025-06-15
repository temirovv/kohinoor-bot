import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_admins(self):
        '''
            Adminlar uchun jadvalni yaratib olish metodi
        '''
        sql = """
        CREATE TABLE IF NOT EXISTS Admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER NOT NULL,
            full_name VARCHAR(200),
            admin_status VARCHAR(40),
            is_superuser BOOL DEFAULT 0
            );
        """
        self.execute(sql, commit=True)

    def create_table_channels(self):
        '''
            foydalanuvchilar uchun qaysi kanalga obuna bo'lishini 
            belgilovchi channels jadvalni hosil qilish metodi
        '''
        sql = """
        CREATE TABLE IF NOT EXISTS channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_name varchar(200)
            );
        """
        self.execute(sql, commit=True)

    def create_table_groups(self):
        '''
            foydalanuvchilar uchun qaysi guruhga obuna bo'lishini 
            belgilovchi groups jadvalni hosil qilish metodi
        '''
        sql = """
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_name varchar(200)
            );
        """
        self.execute(sql, commit=True)

    def create_table_users(self):
        '''
            oddiy foydalanuvchilar uchun jadvalni hosil qilish metodi
        '''
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            telegram_id INTEGER NOT NULL,
            full_name VARCHAR(300),
            phone_number VARCHAR(50),
            people_invited INTEGER DEFAULT 0,
            is_active BOOL DEFAULT 1,
            all_people_invited INTEGER DEFAULT 0,
            invited_from VARCHAR DEFAULT 0,
            full_registered BOOL DEFAULT 0,
            konkurs_count INTEGER DEFAULT 1,
            PRIMARY KEY (telegram_id)
            );
        """
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, telegram_id: int, invited_from=0, konkurs_count=1):
        # SQL_EXAMPLE = "INSERT INTO Users(telegram_id, full_name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT OR IGNORE INTO Users(telegram_id, invited_from, konkurs_count) VALUES(?, ?, ?)
        """
        self.execute(sql, parameters=(telegram_id, invited_from, konkurs_count), commit=True)

    def update_user(self, telegram_id: int, full_name: str, phone_number: str, full_registered=True):
        # SQL_EXAMPLE = "INSERT INTO Users(telegram_id, full_name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        UPDATE Users SET full_name=?, phone_number=?, full_registered=? WHERE telegram_id=?
        """
        self.execute(sql, parameters=(full_name, phone_number, full_registered, telegram_id), commit=True)

    def update_full_registered(self, telegram_id: int, full_registered: bool):
        ''' User to'liq registratsiyadan o'tgandan so'ng true qiymatiga o'zgartiriladi '''
        sql = f"""
        UPDATE Users SET full_registered=? WHERE telegram_id=?
        """
        return self.execute(sql, parameters=(full_registered, telegram_id), commit=True)

    def update_user_people_invited(self, telegram_id: int, people_invited: int):
        sql = f"""
        UPDATE Users SET people_invited=? WHERE telegram_id=?
        """
        return self.execute(sql, parameters=(people_invited, telegram_id), commit=True)

    def update_konkurs_count(self, telegram_id: int, konkurs_count: int):
        sql = '''
        UPDATE Users SET konkurs_count=? where telegram_id=?
        '''
        return self.execute(self, parameters=(konkurs_count, telegram_id), commit=True)

    def update_user_rating_expiration_days(self, telegram_id: int, rating_expiration_days: int):
        sql = f"""
        UPDATE Users SET rating_expiration_days=? WHERE telegram_id=?
        """
        return self.execute(sql, parameters=(rating_expiration_days, telegram_id), commit=True)

    def update_people_invited(self, telegram_id: int, people_invited: int):
        ''' Foydalanuvchi nechta odam taklif etganini yangilash '''
        sql = f"""
        UPDATE Users SET people_invited=? WHERE telegram_id=?
        """
        return self.execute(sql, parameters=(people_invited, telegram_id), commit=True)

    def update_all_people_invited(self, telegram_id: int, all_people_invited: int):
        ''' Foydalanuvchi taklif etgan barcha foydalanuvchini yangilash '''
        sql = f"""
        UPDATE Users SET all_people_invited=? WHERE telegram_id=?
        """
        return self.execute(sql, parameters=(all_people_invited, telegram_id), commit=True)

    def update_user_info(self, telegram_id: str, fullname: str):
        sql = """
        UPDATE Users SET full_name=? WHERE telegram_id=?
        """
        return self.execute(sql, parameters=(fullname, telegram_id), commit=True)

    def select_all_users(self, konkurs_count=1):
        if konkurs_count == 1:
            sql = """
            SELECT full_name, phone_number, people_invited, telegram_id FROM Users where full_registered=1
            """
            return self.execute(sql, fetchall=True)
        else:
            sql = """
            SELECT full_name, phone_number, people_invited, telegram_id FROM Users where full_registered=1 and konkurs_count=?
            """
            return self.execute(sql, parameters=(konkurs_count,), fetchall=True)

    def get_people_invited(self, telegram_id):
        sql = '''
            SELECT people_invited FROM users WHERE telegram_id=?
        '''
        return self.execute(sql=sql, parameters=(telegram_id,), fetchone=True)

    def get_all_people_invited(self, telegram_id):
        sql = '''
            SELECT all_people_invited FROM users WHERE telegram_id=?
        '''
        return self.execute(sql=sql, parameters=(telegram_id,), fetchone=True)

    def get_invited_from(self, telegram_id):
        sql = '''
            SELECT invited_from FROM users WHERE telegram_id=?
        '''
        result = 0
        try:
            result = self.execute(sql=sql, parameters=(telegram_id,), fetchone=True)[0]
        except Exception:
            result = 0
        return result

    def get_rating(self):
        sql = '''
            SELECT full_name, people_invited from Users where full_registered != 0 ORDER BY people_invited DESC
        '''
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def get_all_users_id(self):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT telegram_id FROM Users WHERE full_registered=1"
        return self.execute(sql, fetchall=True)

    def select_all_id(self, konkurs_count=1):
        if konkurs_count == 1:
            sql = ''' SELECT telegram_id FROM Users WHERE is_active=1 '''
            return self.execute(sql, fetchall=True)
        else:
            sql = ''' SELECT telegram_id FROM Users WHERE is_active=1 and konkurs_count=?'''
            return self.execute(sql, parameters=(konkurs_count,), fetchall=True)

    def update_is_active(self, telegram_id, is_active):
        sql = ''' UPDATE Users SET is_active=? WHERE telegram_id=? '''
        self.execute(sql, parameters=(is_active, telegram_id))

    def check_user(self, telegram_id):
        sql = '''
        SELECT * FROM users WHERE telegram_id=?
        '''
        result = self.execute(sql=sql, parameters=(telegram_id,), fetchone=True)
        try:
            if result[0]:
                return True
        except Exception:
            pass
        return False

    def confimr_restart_competition(self):
        sql = '''
            UPDATE Users SET people_invited=0
        '''
        return self.execute(sql, commit=True)

    def check_full_registered(self, telegram_id):
        sql = '''
        SELECT full_registered FROM users WHERE telegram_id=?
        '''
        try:
            result = self.execute(sql=sql, parameters=(telegram_id,), fetchone=True)
        except Exception:
            return False
        if result is not None:
            if result[0]:
                return True
        return False

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    # def count_active_users(self):
    #     return self.execute()

    # def delete_users(self):
    #     self.execute("DELETE FROM Users WHERE TRUE", commit=True)


def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")
