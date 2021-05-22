import sqlite3


class UserDatabase():
    def __init__(self, db_location):
        self.__DB_LOCATION = db_location
        self.__connection = sqlite3.connect(self.__DB_LOCATION)
        self.cursor = self.__connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username VARCHAR(20) UNIQUE,
                first_name VARCHAR(20),
                last_name VARCHAR(20),
                email VARCHAR(20),
                password TEXT,
                gender VARCHAR (5),
                age INTEGER,
                chronic_symptons TEXT,
                medical_record_path TEXT,
                access INTEGER
                
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS doctors (
                doc_id INTEGER PRIMARY KEY,
                username VARCHAR(20) UNIQUE,
                first_name VARCHAR(20),
                last_name VARCHAR(20),
                email VARCHAR(20),
                password TEXT,
                gender VARCHAR (5),
                age INTEGER,
                previous_workplaces TEXT,
                medical_certification TEXT,
                access INTEGER
                
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS diseases (
                id INTEGER PRIMARY KEY,
                disease_name VARCHAR(30) UNIQUE,
                cause VARCHAR(200),
                body_affected VARCHAR(100),
                spreading VARCHAR(200),
                vaccination TEXT,
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS blogs (
                blog_id INTEGER PRIMARY KEY,
                blog_name VARCHAR(30) UNIQUE,
                blog_title VARCHAR(40),
                date INTEGER,
                doctor_id REFERENCES doctors(doc_id)
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                question_id INTEGER PRIMARY KEY,
                question_title VARCHAR(30) UNIQUE,
                question_text Text,
                date INTEGER,
                doctor_id REFERENCES doctors(doc_id)
                user_id REFERENCES users(user_id)
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS answers (
                answer_id INTEGER PRIMARY KEY,
                answer_text Text,
                date INTEGER,
                q_id REFERENCES questions(question_id)
                doctor_id REFERENCES doctors(doc_id)
                user_id REFERENCES users(user_id)
            )
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS roles (
                role_id INTEGER PRIMARY KEY,
                name VARCHAR(32) UNIQUE,
                description VARCHAR(300),
                colour VARCHAR(6) DEFAULT f0ffff
            )
        """)
        

    def insert_user(self, username, first_name, last_name, email, password, gender, age, chronic_symptons, medical_record_path):
            sql = """
                INSERT INTO users (username, first_name, last_name, email, password, gender, age, chronic_symptons, medical_record_path, access)
                VALUES (?, ?, ?, ? , ? , ?, ?, ?, ?, ? )
            """
            self.cursor.execute(sql, (username, first_name, last_name, email, password, gender, age, chronic_symptons, medical_record_path, 2))
            self.__connection.commit()

    def insert_doc(self, username, first_name, last_name, email, password, gender, age, previous_workplaces, medical_certification):
            sql = """
                INSERT INTO doctors  (username, first_name, last_name, email, password, gender, age, previous_workplaces, medical_certification, access)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ? )
            """
            self.cursor.execute(sql, (username, first_name, last_name, email, password, gender, age, previous_workplaces, medical_certification, 4))
            self.__connection.commit()

    def insert_q(self, question_title, question_text, date, doctor_id, user_id):
            sql = """
                INSERT INTO questions  (question_title, question_text, date, doctor_id, user_id)
                VALUES (?, ?, ?, ?, ?)
            """
            self.cursor.execute(sql, (question_title, question_text, date, doctor_id, user_id))
            self.__connection.commit()
    
    def insert_a(self, answer_text, date, q_id,  doctor_id, user_id):
            sql = """
                INSERT INTO answers  ( answer_text, date, q_id,  doctor_id, user_id)
                VALUES (?, ?, ?, ?, ?)
            """
            self.cursor.execute(sql, (answer_text, date, q_id,  doctor_id, user_id))
            self.__connection.commit()
    
    def insert_blog(self, blog_name, blog_title, date, doctor_id):
            sql = """
                INSERT INTO answers  ( blog_name, blog_title, date, doctor_id)
                VALUES (?, ?, ?, ?)
            """
            self.cursor.execute(sql, (blog_name, blog_title, date, doctor_id))
            self.__connection.commit()

    def check_user(self, username):
            sql = """
                SELECT username, password, user_id, access
                FROM users
                WHERE username = ?
            """
            self.cursor.execute(sql, (username, ))
            return self.cursor.fetchone()
    
    def check_doc(self, username):
            sql = """
                SELECT username, password, doc_id, access
                FROM doctors
                WHERE username = ?
            """
            self.cursor.execute(sql, (username, ))
            return self.cursor.fetchone()

    def get_users(self):
            sql = """
                SELECT * FROM users
            """
            self.cursor.execute(sql, )
            return self.cursor.fetchall()

    def get_doctors(self):
            sql = """
                SELECT * FROM doctors
            """
            self.cursor.execute(sql, )
            return self.cursor.fetchall()

    def remove_user(self, username):
            """ Deletes user and user_role mappings """
            sql = """
                DELETE FROM users
                WHERE username =?
            """
            self.cursor.execute(sql, (username, ))
            self.__connection.commit()
            return

    def remove_doctor(self, username):
            """ Deletes user and user_role mappings """
            sql = """
                DELETE FROM doctors
                WHERE username =?
            """
            self.cursor.execute(sql, (username, ))
            self.__connection.commit()
            return

    def insert_role(self, name):
            sql = """
                INSERT INTO roles (name)
                VALUES (?)
            """
            self.cursor.execute(sql, (name, ))
            self.__connection.commit()
            return True

    def check_role(self, name):
            sql = """
                SELECT *
                FROM roles
                WHERE name = ?
            """
            self.cursor.execute(sql, (name, ))
            return self.cursor.fetchone()

    def check_role_id(self, role_id):
            sql = """
                SELECT *
                FROM roles
                WHERE role_id = ?
            """
            self.cursor.execute(sql, (role_id, ))
            selected_role=self.cursor.fetchone()
            if not selected_role:
                selected_role=(0,"no role","", "808080")
            return selected_role

    def update_userrole_id(self, role_id, user_id):
            sql = """
                UPDATE users
                SET access=?
                WHERE user_id =? 
            """
            self.cursor.execute(sql, (role_id, user_id ))
            self.__connection.commit()
            return True

    def update_docrole_id(self, role_id, doc_id):
            sql = """
                UPDATE doctors
                SET access=?
                WHERE doc_id =? 
            """
            self.cursor.execute(sql, (role_id, doc_id ))
            self.__connection.commit()
            return True

    def update_q(self, question_title, question_text, date, question_id):
            sql = """
                UPDATE questions 
                SET question_title=?, question_text=?, date= ? 
                WHERE question_id  =? 
            """
            self.cursor.execute(sql, ( question_title, question_text, date, question_id))
            self.__connection.commit()
            return True

    def update_a(self, answer_text, date, answer_id):
            sql = """
                UPDATE answers
                SET answer_text= ?, date= ?
                WHERE answer_id= ? 
            """
            self.cursor.execute(sql, (answer_text, date, answer_id ))
            self.__connection.commit()
            return True

    def update_blog(self, blog_name, blog_title, date, blog_id):
            sql = """
                UPDATE blogs
                SET blog_name= ?, blog_title= ?, date= ?
                WHERE blog_id= ? 
            """
            self.cursor.execute(sql, (blog_name, blog_title, date, blog_id ))
            self.__connection.commit()
            return True   

    def get_roles(self):
            sql = """
                SELECT *
                FROM roles
            """
            self.cursor.execute(sql, )
            return self.cursor.fetchall()

    def get_logged_user(self, loggedusername):
            sql = """
                SELECT username, first_name, last_name, email, password, gender, age, chronic_symptons
                FROM users
                WHERE username = ?
            """
            self.cursor.execute(sql, (loggedusername,))
            loggeduser = self.cursor.fetchall()
            return loggeduser

    def get_logged_doctor(self, loggedusername):
            sql = """
                SELECT username, first_name, last_name, email, password, gender, age, previous_workplaces
                FROM doctors
                WHERE username = ?
            """
            self.cursor.execute(sql, (loggedusername,))
            loggeduser = self.cursor.fetchall()
            return loggeduser

    def get_userID(self, loggedusername):
            sql = """
                SELECT user_id
                FROM users
                WHERE username = ?
            """
            self.cursor.execute(sql, (loggedusername,))
            loggeduser = self.cursor.fetchall()
            return loggeduser
    
    def get_docID(self, docIDint):
        sql = """
                SELECT doc_id
                FROM doctors
                WHERE userID = ?
            """
        self.cursor.execute(sql, (docIDint,))
        currentuserfarmID = self.cursor.fetchall()
        return currentuserfarmID
    
    def get_q(self, qID):
        sql = """
                SELECT question_title , question_text, date
                FROM questions 
                WHERE question_id  = ?
            """
        self.cursor.execute(sql, (qID,))
        Qinfo = self.cursor.fetchall()
        return Qinfo

    def get_a(self, aID):
        sql = """
                SELECT answer_text , date 
                FROM answers  
                WHERE answer_id   = ?
            """
        self.cursor.execute(sql, (aID,))
        Ainfo = self.cursor.fetchall()
        return Ainfo

    def get_blog(self, bID):
        sql = """
                SELECT blog_name, blog_title, date 
                FROM blogs   
                WHERE blog_id    = ?
            """
        self.cursor.execute(sql, (bID,))
        bloginfo = self.cursor.fetchall()
        return bloginfo
    

    def __del__(self):
            self.__connection.close()