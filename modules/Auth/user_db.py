import sqlite3


class UserDatabase():
    def __init__(self, db_location):
        self.__DB_LOCATION = db_location
        self.__connection = sqlite3.connect(self.__DB_LOCATION)
        self.cursor = self.__connection.cursor()

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
                access INTEGER
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS patient_info (
                id INTEGER PRIMARY KEY,
                chronic_symptoms TEXT,
                medical_record_path TEXT,
                user_id REFERENCES users(user_id),
                username REFERENCES users(username)
            ) """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS doctor_info (
                id INTEGER PRIMARY KEY,
                previous_workplaces TEXT,
                medical_position TEXT,
                medical_certification TEXT,
                user_id REFERENCES users(user_id),
                username REFERENCES users(username)
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Viraldiseases (
                id INTEGER PRIMARY KEY,
                disease_name VARCHAR(30) UNIQUE,
                cause VARCHAR(200),
                body_affected VARCHAR(100),
                spreading VARCHAR(200),
                vaccination TEXT
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Bacterialdiseases (
                id INTEGER PRIMARY KEY,
                disease_name VARCHAR(30) UNIQUE,
                cause VARCHAR(200),
                body_affected VARCHAR(100),
                spreading VARCHAR(200),
                vaccination TEXT
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Wormdiseases (
                id INTEGER PRIMARY KEY,
                disease_name VARCHAR(30) UNIQUE,
                pathogen_habitat VARCHAR(200),
                mode_of_transmission VARCHAR(100),
                main_symptoms VARCHAR(200),
                treatment TEXT
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Fungidiseases (
                id INTEGER PRIMARY KEY,
                disease_name VARCHAR(30) UNIQUE,
                pathogen VARCHAR(200),
                mode_of_transmission VARCHAR(100),
                main_symptoms VARCHAR(200),
                treatment TEXT
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS blogs (
                blog_id INTEGER PRIMARY KEY,
                blog_title VARCHAR(30) UNIQUE,
                blog_text TEXT,
                date INTEGER,
                userid REFERENCES users(user_id)
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
        return True

    def insert_patient(
        self, username, first_name, last_name, email, password,
        gender, age, chronic_symptoms, medical_record_path
    ):
        sql = """
            INSERT INTO users (
                username, first_name, last_name, email, password,
                gender, age, access
            )
            VALUES (?, ?, ?, ? , ? , ?, ?, ? )
        """
        try:
            self.cursor.execute(sql, (
                username, first_name, last_name, email, password,
                gender, age, 2))
        except sqlite3.IntegrityError:
            print("Username not unique")
            return False

        user_id = self.cursor.lastrowid
        sql = """
            INSERT INTO patient_info (
                chronic_symptoms, medical_record_path, user_id
            ) VALUES (
                ?, ?, ?
            )
        """
        try:
            self.cursor.execute(sql, (
                chronic_symptoms, medical_record_path, user_id)
            )
            self.__connection.commit()
            return True
        except sqlite3.IntegrityError:
            print("Username not unique")
            return False

    def check_patient(self, username):
        sql = """
            SELECT users.username, users.first_name, users.last_name,
                users.email, users.gender, users.age, users.access,
                patient_info.chronic_symptoms, patient_info.medical_record_path
            FROM users
            INNER JOIN patient_info on users.user_id = patient_info.user_id
            WHERE users.username = ?
        """

        self.cursor.execute(sql, (username, ))
        return self.cursor.fetchone()

    def insert_doctor(
        self, username, first_name, last_name, email, password,
        gender, age, previous_workplaces, medical_position, medical_certification
    ):
        sql = """
            INSERT INTO users (
                username, first_name, last_name, email, password,
                gender, age, access
            )
            VALUES (?, ?, ?, ? , ? , ?, ?, ? )
        """
        try:
            self.cursor.execute(sql, (
                username, first_name, last_name, email, password,
                gender, age, 4))
        except sqlite3.IntegrityError:
            print("Username not unique")
            return False

        user_id = self.cursor.lastrowid
        sql = """
            INSERT INTO doctor_info (
                previous_workplaces, medical_position, medical_certification, user_id
            ) VALUES (
                ?, ?, ?, ?
            )
        """
        try:
            self.cursor.execute(sql, (
                previous_workplaces, medical_position, medical_certification, user_id)
            )
            self.__connection.commit()
            return True
        except sqlite3.IntegrityError:
            print("Username not unique")
            return False

    def check_doctor(self, username):
        sql = """
            SELECT users.username, users.first_name, users.last_name,
                users.email, users.gender, users.age, users.access,
                doctor_info.previous_workplaces, doctor_info.medical_position, doctor_info.medical_certification
            FROM users
            INNER JOIN doctor_info on users.user_id = doctor_info.user_id
            WHERE users.username = ?
        """

        self.cursor.execute(sql, (username, ))
        return self.cursor.fetchone()



    def insert_user(
        self, username, first_name, last_name, email, password,
        gender, age, access
    ):
        sql = """
            INSERT INTO users (
                username, first_name, last_name, email, password,
                gender, age, access
            )
            VALUES (?, ?, ?, ? , ? , ?, ?, ? )
        """
        try:
            self.cursor.execute(sql, (
                username, first_name, last_name, email, password,
                gender, age, access))
            self.__connection.commit()
        except sqlite3.IntegrityError:
            print("Username not unique")
            return False
        return self.cursor.lastrowid

    def check_user(self, user_id):
        sql = """
            SELECT username, password, user_id, access
            FROM users
            WHERE user_id = ?
        """
        self.cursor.execute(sql, (user_id, ))
        return self.cursor.fetchone()

    def check_user_username(self, username):
        sql = """
            SELECT username, password, user_id, access
            FROM users
            WHERE username = ?
        """
        self.cursor.execute(sql, (username, ))
        return self.cursor.fetchone()
    
    def get_users(self):
        sql = """
            SELECT * 
            FROM users
             
        """
        self.cursor.execute(sql, )
        return self.cursor.fetchall()
    
    def get_userid_name(self, username):
        sql = """
            SELECT user_id 
            FROM users
            WHERE username=?
             
        """
        self.cursor.execute(sql, [username,] )
        return self.cursor.fetchall()

    def get_docusers(self):
        sql = """
            SELECT users.username, users.first_name, users.last_name,
                users.email, users.gender, users.age, users.access,
                doctor_info.previous_workplaces, doctor_info.medical_position, doctor_info.medical_certification
            FROM users
            INNER JOIN doctor_info 
            WHERE users.access = ?
        """

        self.cursor.execute(sql, (3, ))
        return self.cursor.fetchone()

    def remove_user(self, username):
            sql = """
                DELETE FROM  users, doctor_info, patient_info
                WHERE username = ?
            """
            self.cursor.execute(sql, (username, ))
            self.__connection.commit()
            return
    


    def update_role(self, username, access):
        sql = """
            UPDATE users
            SET access = ?
            WHERE username = ?  
        """
        self.cursor.execute(sql, (access, username))
        self.__connection.commit()
        return True

    def insert_vd(self, disease_name, cause, body_affected, spreading, vaccination):
        sql = """
            INSERT OR IGNORE INTO Viraldiseases   (disease_name, cause, body_affected, spreading, vaccination)
            VALUES (?, ?, ?, ?, ?)
        """
        self.cursor.execute(sql, (disease_name, cause, body_affected, spreading, vaccination))
        self.__connection.commit()
    
    def update_vd(self, c, b, s, v, d_n):
        sql = """
            UPDATE Viraldiseases 
            SET  cause=?, body_affected= ? , spreading=? ,vaccination=? 
            WHERE disease_name  =? 
        """
        self.cursor.execute(sql, (  c, b, s, v, d_n))
        self.__connection.commit()
        return True

    def get_vd(self):    #Farm portal (All farms for that user)
        sql = """
                SELECT *
                FROM Viraldiseases
                
            """
        self.cursor.execute(sql,)
        currentvddata = self.cursor.fetchall()
        return currentvddata

    def delete_vd(self, vdname):
            sql = """
                DELETE FROM Viraldiseases
                WHERE disease_name = ?

            """
            self.cursor.execute(sql, (vdname,))
            self.__connection.commit()

    def insert_bd(self, disease_name, cause, body_affected, spreading, vaccination):
        sql = """
            INSERT OR IGNORE INTO Bacterialdiseases    (disease_name, cause, body_affected, spreading, vaccination)
            VALUES (?, ?, ?, ?, ?)
        """
        self.cursor.execute(sql, (disease_name, cause, body_affected, spreading, vaccination))
        self.__connection.commit()
    
    def update_bd(self,  cause, body_affected, spreading, vaccination, disease_name):
        sql = """
            UPDATE Bacterialdiseases  
            SET  cause=?, body_affected= ? , spreading=? ,vaccination=? 
            WHERE disease_name  =? 
        """
        self.cursor.execute(sql, (  cause, body_affected, spreading, vaccination, disease_name))
        self.__connection.commit()
        return True

    def get_bd(self):    #Farm portal (All farms for that user)
        sql = """
                SELECT *
                FROM Bacterialdiseases
                
            """
        self.cursor.execute(sql )
        currentbddata = self.cursor.fetchall()
        return currentbddata

    def delete_bd(self, bdname):
            sql = """
                DELETE FROM Bacterialdiseases
                WHERE disease_name = ?

            """
            self.cursor.execute(sql, (bdname,))
            self.__connection.commit()

    def insert_wd(self, disease_name, pathogen_habitat, mode_of_transmission, main_symptoms, treatment):
        sql = """
            INSERT OR IGNORE INTO Wormdiseases (disease_name, pathogen_habitat, mode_of_transmission, main_symptoms, treatment)
            VALUES (?, ?, ?, ?, ?)
        """
        self.cursor.execute(sql, (disease_name, pathogen_habitat, mode_of_transmission, main_symptoms, treatment))
        self.__connection.commit()

    def update_wd(self,  pathogen_habitat, mode_of_transmission, main_symptoms, treatment, disease_name):
        sql = """
            UPDATE Wormdiseases  
            SET pathogen_habitat=?, mode_of_transmission= ? , main_symptoms=? ,treatment=? 
            WHERE disease_name  =? 
        """
        self.cursor.execute(sql, (  pathogen_habitat, mode_of_transmission, main_symptoms, treatment, disease_name))
        self.__connection.commit()
        return True

    def get_wd(self):    #Farm portal (All farms for that user)
        sql = """
                SELECT *
                FROM Wormdiseases
                
            """
        self.cursor.execute(sql,)
        currentwddata = self.cursor.fetchall()
        return currentwddata

    def delete_wd(self, wdname):
            sql = """
                DELETE FROM Wormdiseases
                WHERE disease_name = ?

            """
            self.cursor.execute(sql, (wdname,))
            self.__connection.commit()

    def insert_fd(self, disease_name, pathogen, mode_of_transmission, main_symptoms, treatment):
        sql = """
            INSERT OR IGNORE INTO Fungidiseases  (disease_name, pathogen, mode_of_transmission, main_symptoms, treatment)
            VALUES (?, ?, ?, ?, ?)
        """
        self.cursor.execute(sql, (disease_name, pathogen, mode_of_transmission, main_symptoms, treatment))
        self.__connection.commit()
    
    def update_fd(self,  pathogen, mode_of_transmission, main_symptoms, treatment, disease_name):
        sql = """
            UPDATE Fungidiseases   
            SET pathogen=?, mode_of_transmission= ? , main_symptoms=? ,treatment=? 
            WHERE disease_name  =? 
        """
        self.cursor.execute(sql, (  pathogen, mode_of_transmission, main_symptoms, treatment, disease_name))
        self.__connection.commit()
        return True
    
    def get_fd(self):    #Farm portal (All farms for that user)
        sql = """
                SELECT *
                FROM Fungidiseases
            """
        self.cursor.execute(sql,)
        currentfddata = self.cursor.fetchall()
        return currentfddata

    def delete_fd(self, fdname):
            sql = """
                DELETE FROM Fungidiseases
                WHERE disease_name = ?

            """
            self.cursor.execute(sql, (fdname,))
            self.__connection.commit()
    
    def insert_blog(self,  blog_title, blog_text, date, user_id):
        sql = """
            INSERT INTO blogs  ( blog_title, blog_text , date, userid )
            VALUES (?, ?, ?, ?)
        """
        self.cursor.execute(sql, (blog_title, blog_text, date, user_id,))
        self.__connection.commit()

    def update_blog(self, blog_title, blog_text, date, blog_id):
        sql = """
            UPDATE blogs
            SET blog_title=?, blog_text=?, date= ?
            WHERE blog_id= ? 
        """
        self.cursor.execute(sql, (blog_title, blog_text, date, blog_id ))
        self.__connection.commit()
        return True

    def delete_blog(self, blogid):
            sql = """
                DELETE FROM blogs 
                WHERE blog_id  = ?

            """
            self.cursor.execute(sql, (blogid,))
            self.__connection.commit()

    def get_blogs_admin(self, userid):
        sql="""
            SELECT *
            FROM blogs
            WHERE userid=?

        """
        self.cursor.execute(sql, (userid,))
        currentblogdata = self.cursor.fetchall()
        return currentblogdata

    def get_blogs(self):
        sql="""
            SELECT *
            FROM blogs
        """
        self.cursor.execute(sql, )
        currentblogdata = self.cursor.fetchall()
        return currentblogdata
    
    def get_blogs_ID(self, blogid):
        sql="""
            SELECT *
            FROM blogs
            WHERE blog_id =?
        """
        self.cursor.execute(sql, (blogid))
        currentblogdata = self.cursor.fetchall()
        return currentblogdata

    # EVERYTHING BELOW NEEDS TO BE TESTED
    
    
    

    # TODO
    def remove_user(self, username):
        return False

   

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

    # TODO
    def update_userrole_id(self, role_id, user_id):
        return False

    # TODO
    def update_docrole_id(self, role_id, doc_id):
        return False

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

    

    def get_roles(self):
        sql = """
            SELECT *
            FROM roles
        """
        self.cursor.execute(sql, )
        return self.cursor.fetchall()

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
