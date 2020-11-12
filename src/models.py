from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    all_users_todos = db.relationship('Todo', lazy=True)

    def __repr__(self):
        return f'username: {self.username}'

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "users": self.all_users_todos
            # do not serialize the password, its a security breach
        }

    def add_new_user(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_user(cls, username):
        user = User.query.filter_by(username = username)
        return user.serialize()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(250), unique=False, nullable=False)
    done = db.Column(db.Boolean(False), unique=False, nullable=False)
    user_id = db.Column(db.String(120), db.ForeignKey("user.username"))

    def __repr__(self):
        return f'label: {self.label}, done: {self.done}'

    def serialize(self):
        return {
            "id": self.id,
            "label": self.label,
            "user_id": self.user_id,
            "done": self.done,
        }

    def add_todo(self):
        db.session.add(self)
        db.session.commit()


    # @classmethod
    # def get_todo(cls):
    #     todos = Todo.query.all()
    #     # user = User.query.filter_by(id = userid)
    #     all_todos = list(map(lambda x: x.serialize(), todos))
    #     return all_todos