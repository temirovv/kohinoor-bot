import sqlite3


class Admin:
    def __init__(self, path_to_db="admin.db"):
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

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def create_table_messages_for_start(self):
        ''' Start bosganda yuborilishi kerak bo'lgan xabarlar jadvalini yaratish '''
        sql = '''
        CREATE TABLE IF NOT EXISTS messages (
        message_id INTEGER PRIMARY KEY AUTOINCREMENT,
        text VARCHAR(9000),
        status BOOL DEFAULT 0
        )
        '''
        self.execute(sql, commit=True)
    
    def create_channel_table(self):
        sql = """CREATE TABLE IF NOT EXISTS channels (
            channel_id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel VARCHAR(255)
        )"""
        self.execute(sql, commit=True)

    def create_table_konkurs(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS konkurs (
        message_id INTEGER PRIMARY KEY AUTOINCREMENT,
        konkurs_count INTEGER DEFAULT 1
        )
        '''
        self.execute(sql, commit=True)        

    def create_adminstrator_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS adminstrator (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admin VARCHAR(30)
        )'''
        self.execute(sql, commit=True)

    def get_adminstrators_as_list(self):
        sql = '''SELECT id, admin FROM adminstrator'''
        data = self.execute(sql, fetchall=True)
        menu = []
        for admin in data:
            admin_id, admin_tg = admin
            menu.append(
                admin_tg
            )

        return menu

    def set_konkurs1(self):
        sql = '''
        insert into konkurs (konkurs_count) values (1)
        '''
        self.execute(sql, commit=True)

    def update_konkurs(self, konkurs_count):
        sql = '''
        UPDATE konkurs SET konkurs_count=? where message_id=1
        '''
        self.execute(sql, parameters=(konkurs_count,), commit=True)

    def get_konkurs_count(self):
        sql = '''
        SELECT konkurs_count FROM konkurs where message_id=1
        '''
        return self.execute(sql, fetchone=True)[0]

    def add_message(self, text, status=False):
        sql = '''
        INSERT INTO messages (text, status) VALUES (?, ?)
        '''
        return self.execute(sql, parameters=(text, status), commit=True)
    
    def set_all_status_false(self):
        sql = '''
        UPDATE messages SET status=0
        '''
        return self.execute(sql, commit=True)

    def get_message(self):
        sql = '''
        SELECT text FROM messages WHERE status=1
        '''
        return self.execute(sql, fetchone=True)

    def add_channel(self, channel: str):
        sql = """INSERT INTO channels (channel) VALUES (?)"""
        self.execute(sql, parameters=(channel,), commit=True)

    def delete_channel(self, channel_id: str):
        sql = """DELETE FROM channels WHERE channel_id=?"""
        self.execute(sql, parameters=(channel_id,), commit=True)

    def get_channels(self):
        sql = """SELECT channel_id, channel FROM channels"""
        return self.execute(sql, fetchall=True)
    
    def get_channels_as_a_list(self):
        sql = """SELECT channel FROM channels"""
        data = self.execute(sql, fetchall=True)
        menu = []

        for channel in data:
            menu.append(
                channel[0]
            )

        return menu

    def add_admin(self, admin):
        sql = '''INSERT INTO adminstrator (admin) VALUES (?)'''
        self.execute(sql, parameters=(admin,), commit=True)


def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")