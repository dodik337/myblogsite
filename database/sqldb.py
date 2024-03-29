import sqlite3 as sq
from flask import Flask, g
import os, time

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'privet _will day its okey'

app = Flask(__name__)
app.config.from_object(Config)
app.config.update(dict(DATABASE=os.path.join(app.root_path,'../posts.db')))

def connect_db():
    conn = sq.connect(app.config['DATABASE'])
    conn.row_factory = sq.Row
    return conn

def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
        return g.link_db

#Подключение базы данных

def create_db():
    '''Вспомогательная функция для создания таблиц БД '''
    db = connect_db()
    with app.open_resource('sql_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()
    return True

class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def addData(self, username, password, email, status, email_status):
        try:
            self.__cur.execute("INSERT INTO user VALUES (NULL, ?, ?, ?, ?, ?)", (username, password, email, status, email_status,))
            self.__db.commit()
        except sq.Error as e:
            print(str(e))
            return False
        return True

    def delData(self, id=0):
        try:
            if id == 0:
                self.__cur.execute("DELETE FROM user")
            else:
                self.__cur.execute(f"DELETE FROM user WHERE id == {id}")
            self.__db.commit()
        except sq.Error as e:
            print(str(e))
            return False
        return True

    def getData(self, username, password):
        try:
            self.__cur.execute("SELECT username, password, email FROM user WHERE ? = email AND ? = password OR ? = username AND ? = password", (username, password, username, password))
            res = self.__cur.fetchall()
            return res
        except sq.Error as e:
            print(str(e))
            return False

    def getStatus(self, username):
        try:
            self.__cur.execute("SELECT status FROM user WHERE ? = username", (username,))
            res = self.__cur.fetchone()
            if res: return res
        except sq.Error as e:
            print(str(e))
            return False

    def UpdateUserPass(self, username, new_password):
        try:
            self.__cur.execute("UPDATE user SET password = ? WHERE ? = email OR ? = username", (new_password, username, username,))
            self.__db.commit()
        except sq.Error as e:
            print(str(e))
            return False
        return True

    def getEmail(self, username):
        try:
            self.__cur.execute("SELECT email FROM user WHERE ? = email OR ? = username", (username, username,))
            res = self.__cur.fetchone()
            if res: return res
        except sq.Error as e:
            print(str(e))
            return False
        return []

    def UpdateEmail(self, email, username):
        try:
            self.__cur.execute("UPDATE user SET email = ? WHERE ? = username", (email, username,))
            self.__db.commit()
        except sq.Error as e:
            print(str(e))
            return False
        return True

    def addMenu(self, title, url):
        try:
            self.__cur.execute("INSERT INTO menu VALUES (NULL, ?, ?)", (title, url))
            self.__db.commit()
        except sq.Error as e:
            print(str(e))
            return False
        return True

    def delMenu(self, id=0):
        try:
            if id == 0:
                self.__cur.execute("DELETE FROM menu")
            else:
                self.__cur.execute(f"DELETE FROM menu WHERE id == {id}")
            self.__db.commit()
        except sq.Error as e:
            print(str(e))
            return False
        return True

    def getMenu(self):
        try:
            self.__cur.execute("SELECT * FROM menu")
            res = self.__cur.fetchall()
            if res: return res
        except sq.Error as e:
            print(str(e))
            return False

    def addPost(self, title, text):
        try:
            tm = time.ctime()
            self.__cur.execute("INSERT INTO post VALUES (NULL, ?, ?, ?)", (title, text, tm))
            self.__db.commit()
        except sq.Error as e:
            print(str(e))
            return False
        return True

    def delPost(self, id=0):
        try:
            if id == 0:
                self.__cur.execute("DELETE FROM post")
            else:
                self.__cur.execute(f"DELETE FROM post WHERE {id} == id")
            self.__db.commit()
        except sq.Error as e:
            print(str(e))
            return False
        return True

    def getPost(self, post_id: int):
        try:
            self.__cur.execute("SELECT * FROM post WHERE ? == id", (post_id,))
            res = self.__cur.fetchall()
            if res: return res
        except sq.Error as e:
            print(str(e))
            return False

    def getPostList(self, posts_ids: list):
        try:
            posts = []
            for i in range(len(posts_ids)):
                self.__cur.execute("SELECT * FROM post WHERE ? == id", (posts_ids[i],))
                res = self.__cur.fetchall()
                posts.append(res)
            return posts
        except sq.Error as e:
            print(str(e))
            return False

    def getAllPostsId(self):
        try:
            self.__cur.execute(f"SELECT id time FROM post ORDER BY time")
            res = self.__cur.fetchall()
            if res: return res
        except sq.Error as e:
            print("Ошибка получения статей из БД" + str(e))
            return False
        return []

    def getAllPosts(self):
        try:
            self.__cur.execute(f"SELECT id, title, text, time FROM post")
            res = self.__cur.fetchall()
            if res: return res
        except sq.Error as e:
            print("Ошибка получения статей из БД" + str(e))
            return False
        return []

    def getLastPosts(self):
        try:
            self.__cur.execute("SELECT id, title, text, time FROM post ORDER BY time LIMIT 3")
            res = self.__cur.fetchall()
            if res: return res
        except sq.Error as e:
            print(str(e))
            return False
        return []

    def getPostAnnocePages(self, last_id: int):
        try:
            self.__cur.execute("SELECT id, title, text, time FROM post WHERE id > ? ORDER BY id ASC LIMIT 5", (last_id,))
            res = self.__cur.fetchall()
            if res: return res
        except sq.Error as e:
            print("Ошибка получения статей из БД" + str(e))
            return False

    def addComment(self, username, text, id_post, login):
        try:
            self.__cur.execute("INSERT INTO comments VALUES (NULL, ?, ?, ?, ?)", (username, text, id_post, login,))
            self.__db.commit()
        except sq.Error as e:
            print(str(e))
            return False
        return True

    def delComment(self, postid=0, id=0):
        try:
            if postid == 0:
                self.__cur.execute("DELETE FROM comments")
            else:
                self.__cur.execute(f"DELETE FROM comments WHERE postid == {postid} AND id == {id}")
            self.__db.commit()
        except sq.Error as e:
            print(str(e))
            return False
        return True

    def getComment(self, id_com: int):
        try:
            self.__cur.execute("SELECT * FROM comments WHERE ? == id", (id_com,))
            res = self.__cur.fetchone()
            if res: return res
        except sq.Error as e:
            print(str(e))
            return False

    def getComments(self, id_post: int):
        try:
            self.__cur.execute("SELECT * FROM comments WHERE ? == postid", (id_post,))
            res = self.__cur.fetchall()
            return res
        except sq.Error as e:
            print(str(e))
            return False

    def addTODO(self, text):
        try:
            tm = time.time()
            self.__cur.execute(f"INSERT INTO todo VALUES (NULL, ?, ?)", (text, tm))
            self.__db.commit()
        except sq.Error as e:
            print(str(e))
            return False
        return True

    def delTODO(self, id=0):
        try:
            if id == 0:
                self.__cur.execute("DELETE FROM todo")
            else:
                self.__cur.execute(f"DELETE FROM todo WHERE id == {id}")
            self.__db.commit()
        except sq.Error as e:
            print(str(e))
            return False
        return True

    def getTODO(self):
        try:
            self.__cur.execute("SELECT * FROM todo")
            res = self.__cur.fetchall()
            return res
        except sq.Error as e:
            print(str(e))
            return False

    def PostUpdate(self, title, text, photo, postid):
        try:
            self.__cur.execute(f"UPDATE post SET title == ?, text == ?, photo == ? WHERE id == ?", (title, text, photo, postid))
            self.__db.commit()
        except sq.Error as e:
            print(str(e))
            return False
        return True

    def addProfile(self, nick, name, age, about, login):
        try:
            self.__cur.execute(f"INSERT INTO profile VALUES(NULL, ?, ?, ?, ?, ?)", (nick, name, age, about, login,))
            self.__db.commit()
            return True
        except sq.Error as e:
            print(str(e))
            return False

    def UpdateProfile(self, nick, name, age, about, login):
        try:
            self.__cur.execute(f"UPDATE profile SET nick == ?, name == ?, age == ?, about == ? WHERE ? = login", (nick, name, age, about, login,))
            self.__db.commit()
            return True
        except sq.Error as e:
            print(str(e))
            return False

    def delProfile(self, id=0):
        try:
            if id == 0:
                self.__cur.execute("DELETE FROM profile")
            else:
                self.__cur.execute(f"DELETE FROM profile WHERE {id} == id")
            self.__db.commit()
        except sq.Error as e:
            print(str(e))
            return False
        return True

    def getProfile(self, login):
        try:
            self.__cur.execute(f"SELECT * FROM profile WHERE ? = login", (login,))
            res = self.__cur.fetchall()
            if res: return res
        except sq.Error as e:
            print(str(e))
            return False

    def UpdateEmailStatus(self, login, status):
        try:
            self.__cur.execute("UPDATE user SET confirmed == ? WHERE ? = username", (status, login,))
            self.__db.commit()
            return True
        except sq.Error as e:
            print(str(e))
            return False

    def getEmailStatus(self, login):
        try:
            self.__cur.execute("SELECT confirmed FROM user WHERE ? = username", (login,))
            res = self.__cur.fetchone()
            return res
        except sq.Error as e:
            print(str(e))
            return False

    def deleteAccount(self, login):
        try:
            self.__cur.execute("DELETE FROM user WHERE ? = username", (login,))
            self.__cur.execute("DELETE FROM profile WHERE ? = login", (login,))
            self.__db.commit()
            return True
        except sq.Error as e:
            print(str(e))
            return False

    def SearchInPosts(self, text: str):
        try:
            searched = []
            text = text.lower()
            for i in range(0, len(self.getAllPosts())):
                post = self.getAllPosts()[i]
                ss = []
                for i in text:
                    if i not in ss:
                        ss.append(i)
                title: str = post['title']
                title: str = title.lower()
                for y in range(len(ss)):
                    titles_count = title.count(''.join(ss[y]))
                    if titles_count >= 1:
                        searched.append(post['id'])
            new_searched = []
            for i in searched:
                if i not in new_searched:
                    new_searched.append(i)
            posts = self.getPostList(new_searched)
            return posts
        except sq.Error as e:
            print(str(e))
            return False

if __name__ == "__main__":
    # from app import connect_db
    db = connect_db()
    db = FDataBase(db)
    # create_db()
    # print(db.delData(0))
    # print(db.addData('admin', '111', 'admin@gmail.com'))
    # print(db.delMenu(0))
    # print(db.addMenu('Main', 'start_page'))
    print(db.addMenu('About', 'about'))
    # print(connect_db().execute('ALTER TABLE profile ADD COLUMN login text not null unique'))
    # print(connect_db().execute('ALTER TABLE user DROP COLUMN status'))
    # print(connect_db().execute('ALTER TABLE user ADD COLUMN status text'))
    # print(connect_db().execute("ALTER TABLE user ADD COLUMN confirmed text not null default 'unconfirmed'"))
    print(connect_db().execute("ALTER TABLE comments ADD COLUMN login text not null default ''"))