from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    children = db.relationship('Todo', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "username": self.username,
            # do not serialize the password, its a security breach
        }

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(120), unique=False, nullable=False)
    done = db.Column(db.Boolean(), unique=False, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f'label: {self.label}, done: {self.done}'

    def serialize(self):
        return {
            "label": self.label,
            "done": self.done,
        }