from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    user_todos = db.relationship('Todo', lazy=True)

    def __repr__(self):
        return f'username: {self.username}'

    def serialize(self):
        return {
            "username": self.username,
            # do not serialize the password, its a security breach
        }

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(250), unique=False, nullable=False)
    done = db.Column(db.Boolean(False), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f'id: {self.id} label: {self.label}, done: {self.done}'

    def serialize(self):
        return {
            "id": self.id,
            "label": self.label,
            "done": self.done,
        }

    def add_todo(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_todo(cls):
        todos = Todo.query.all()
        # user = User.query.filter_by(id = userid)
        all_todos = list(map(lambda x: x.serialize(), todos))
        return all_todos