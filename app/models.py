from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#
# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@127.0.0.1:3306/movie"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# db = SQLAlchemy(app)
from app import db


# 会员表
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(11), unique=True)
    info = db.Column(db.TEXT)
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    uuid = db.Column(db.String(255), unique=True)
    userlog = db.relationship('Userlog', backref='user')  # 会员日志外键关系
    comments = db.relationship('Comment', backref='user')  # 会员评论外键
    moviecols = db.relationship('Moviecol', backref='user')  # 会员收藏外键关系

    def __repr__(self):
        return "<User %r>" % self.name


# 会员登陆日志
class Userlog(db.Model):
    __tablename__ = "userlog"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<Userlog %r>" % self.id


# 标签
class Tag(db.Model):
    # 是双引号不是单引号 否则无法自增
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    movies = db.relationship("Movie", backref='tag')

    def __repr__(self):
        return "<Tag %r>" % self.name


class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    url = db.Column(db.String(255), unique=True)
    info = db.Column(db.TEXT)
    logo = db.Column(db.String(255), unique=True)
    star = db.Column(db.SmallInteger)
    playnum = db.Column(db.BigInteger)
    commentnum = db.Column(db.BigInteger)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    area = db.Column(db.String(255))
    release_time = db.Column(db.Date)
    length = db.Column(db.String(100))
    additme = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    comments = db.relationship('Comment', backref='movie')
    moviecols = db.relationship('Moviecol', backref='movie')  # 影片收藏外键关系

    def __repr__(self):
        return "<Movie %r>" % self.title


class Preview(db.Model):
    __tablename__ = "preview"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    logo = db.Column(db.String(255), unique=True)
    additme = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<Preview %r>" % self.title


class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.TEXT)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    additme = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<Comment %r>" % self.id


class Moviecol(db.Model):
    __tablename__ = "moviecol"
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    additme = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<Moviecol %r>" % self.id


# 权限
class Auth(db.Model):
    __tablename__ = "auth"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    url = db.Column(db.String(255), unique=True)  # 地址
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 添加时间

    def __repr__(self):
        return "<Auth %r>" % self.name


# 角色
class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    auths = db.Column(db.String(600))  # 权限列表
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 添加时间
    admins = db.relationship('Admin', backref='role')  # 管理员外键关系关联

    def __repr__(self):
        return "<Role %r>" % self.name


# 管理员
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 管理员账号
    pwd = db.Column(db.String(100))  # 管理员密码
    is_super = db.Column(db.SmallInteger)  # 是否为超级管理员，0为超级管理员
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  # 所属角色
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 添加时间
    adminlogs = db.relationship('Adminlog', backref='admin')  # 管理员登录日志外键关系关联
    oplogs = db.relationship('Oplog', backref='admin')  # 操作日志外键关系关联

    def __repr__(self):
        return "<Admin %r>" % self.name

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)  # 验证密码是否正确，返回True和False


# 管理员登录日志
class Adminlog(db.Model):
    __tablename__ = "adminlog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员编号
    ip = db.Column(db.String(100))  # 登录IP
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 登录时间

    def __repr__(self):
        return "<Adminlog %r>" % self.id


# 操作日志
class Oplog(db.Model):
    __tablename__ = "oplog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员编号
    ip = db.Column(db.String(100))  # 登录IP
    reason = db.Column(db.String(600))  # 操作原因
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 登录时间

    def __repr__(self):
        return "<Oplog %r>" % self.id

if __name__ == "__main__":
    # db.create_all()
    # role = Role(
    #     name="超级管理员",
    #     auths=""
    # )
    # db.session.add(role)
    # db.session.commit()
    from werkzeug.security import generate_password_hash

    admin = Admin(
        name="imoocmovie",
        pwd=generate_password_hash("imoocmovie"),
        is_super=0,
        role_id=1
    )
    db.session.add(admin)
    db.session.commit()
