import mysql.connector as mysql_con

from libs.algorithm import library as algo_lib
# import mysql.connector.locales.eng.client_error
from mysql.connector.locales.eng import client_error

@algo_lib.singleton
class DBVersionUp:
    def __init__(self):
        self.connect = mysql_con.connect(
            host="localhost",
            user="root",
            password="skfk1493",
            database="version_db"
        )
        self.cursor = self.connect.cursor()

    def __del__(self):
        if self.connect.is_connected():
            # self.cursor.close()
            self.connect.close()

    def get_final_id(self) -> list:  # return final file_id
        q = '''
        select * from version_final_table;
        '''
        self.cursor.execute(q)
        res = list(map(lambda x: x[0], self.cursor.fetchall()))
        return res

    def get_cache_id_by_fid(self, fid) -> list:
        q = '''
        select * from cache_table WHERE final_id = %s;
        '''
        self.cursor.execute(q, (fid,))
        res = list(map(lambda x: x[0], self.cursor.fetchall()))
        return res

    def get_depart_by_name(self, name) -> list:
        q = '''
        SELECT depart FROM user_table WHERE user = %s;
        '''
        self.cursor.execute(q, name)
        res = self.cursor.fetchall()
        return res

    def get_userid_by_user(self, name) -> list:
        q = '''
        SELECT id FROM user_table WHERE user=%s;
        '''
        self.cursor.execute(q, (name,))
        res = self.cursor.fetchall()
        return res

    def get_version_by_cache_name(self, f_name) -> list:
        q = '''
        SELECT * FROM version_final_table WHERE cache_name = %s;
        '''
        self.cursor.execute(q, (f_name,))
        res = self.cursor.fetchall()
        return res

    def update_version_time(self, f_name, uid) -> int:
        q = '''
        UPDATE version_final_table SET updated_time = NOW(), user_id = %s WHERE cache_name = %s;
        '''
        try:
            self.cursor.execute(q, (uid, f_name))
            self.connect.commit()
            self.cursor.execute("SELECT id FROM version_final_table WHERE cache_name = %s", (f_name,))
            f_id = self.cursor.fetchone()

            if f_id:
                return f_id[0]
            else:
                return -1
        except Exception as err:
            self.connect.rollback()
            print(err)
            return -1

    def add_cache_and_get_id(self, f_id, path) -> int:
        q = '''
        INSERT INTO cache_table (final_id, cache_path) VALUES (%s, %s);
        '''
        try:
            self.cursor.execute(q, (f_id, path))
            self.connect.commit()
            self.cursor.execute("SELECT id FROM cache_table WHERE cache_path = %s", (path,))
            c_id = self.cursor.fetchone()
            if c_id:
                return c_id[0]
            else:
                return -1
        except Exception as err:
            self.connect.rollback()
            print(err)
            return -1

    def add_version(self, data: list) -> int:
        assert isinstance(data, list)
        assert len(data) == 3
        q = '''
        INSERT INTO version_final_table (cache_name, updated_time, user_id) 
        VALUES (%s, %s, %s);
        '''
        try:
            self.cursor.execute(q, data)
            self.connect.commit()
            f_id = self.cursor.lastrowid
            return f_id
        except Exception as err:
            self.connect.rollback()
            print(err)
            return -1

    def add_note(self, note, c_id) -> bool:
        q = '''
        INSERT INTO ref_note_table (note, cache_id) VALUES (%s, %s);
        '''
        try:
            self.cursor.execute(q, (note, c_id))
            self.connect.commit()
            return True
        except Exception as err:
            self.connect.rollback()
            print(err)
            return False

    def count_cache_by_name(self, name: str) -> int:
        q = '''
        SELECT COUNT(*) FROM cache_table WHERE final_id = (
            SELECT id FROM version_final_table WHERE cache_name = %s
        );
        '''
        try:
            self.cursor.execute(q, (name,))
            result = self.cursor.fetchone()
            if result:
                return result[0]
            else:
                return 0  # 0개니까
        except Exception as err:
            print(err)
            return -1

    def get_final_name(self) -> list:
        q = '''
        SELECT cache_name FROM version_final_table;
        '''
        self.cursor.execute(q)
        res = self.cursor.fetchall()
        return res

    def get_cache_files(self) -> list:  # get final_id of each cache file
        q = '''
        SELECT * FROM cache_table;
        '''
        self.cursor.execute(q)
        res = list(map(lambda x: x[1], self.cursor.fetchall()))
        return res

    def get_one_cache_path(self, f_id) -> list:
        q = '''
        SELECT cache_path FROM cache_table WHERE final_id = %s;
        '''
        self.cursor.execute(q, (f_id,))
        res = self.cursor.fetchall()
        return res

    def get_note_by_cid(self, cid) -> str:
        q = '''
        SELECT note FROM ref_note_table WHERE cache_id = %s;
        '''
        self.cursor.execute(q, (cid,))
        res = self.cursor.fetchone()
        return res

    def get_cache_path(self) -> list:
        q = '''
        SELECT cache_path FROM cache_table;
        '''
        self.cursor.execute(q)
        res = self.cursor.fetchall()
        return res

    def get_username_by_id(self, uid) -> list:
        q = '''
        SELECT user FROM user_table WHERE id = %s;
        ''' % uid
        self.cursor.execute(q)
        res = self.cursor.fetchall()
        return res

    def get_note_by_cache_id(self, cid) -> list:
        q = '''
        SELECT * FROM ref_note_table WHERE id = %s; 
        '''
        self.cursor.execute(q, (cid, ))
        res = list(map(lambda x: x[1], self.cursor.fetchall()))
        return res

    def get_id(self):
        return self.cursor.lastrowid

    def add_user(self, u_lst: list) -> bool:
        q = '''
        INSERT INTO user_table (user, depart) VALUES (%s, %s);
        '''
        try:
            self.cursor.execute(q, u_lst)
            self.connect.commit()
            return True
        except Exception as err:
            self.connect.rollback()
            print(err)
            return False

    def del_user_id(self, data_id: int) -> bool:
        q = '''
        DELETE FROM final_version_table WHERE user_id=%s;
        ''' % data_id
        try:
            self.cursor.execute(q)
            self.connect.commit()
            return True
        except Exception as err:
            self.connect.rollback()
            print(err)
            return False


if __name__ == '__main__':
    db_version = DBVersionUp()
    db_version2 = DBVersionUp()

    print(db_version)
    print(db_version2)

