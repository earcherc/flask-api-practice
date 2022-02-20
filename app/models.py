from . import db


class Role(db.Model):
    # Explicitly set the table name to follow good convention of plural table names
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    # Contains the back reference to the relationship so we can access role.users.all()
    # lazy loaded so we can add filters if we query the relationship form this direction.
    users = db.relationship("User", backref="role", lazy="dynamic")

    # Not necessary but good for debugging
    def __repr__(self):
        return "<Role %s>" % self.name


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    age = db.Column(db.Integer)

    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    def __repr__(self):
        return "<User %s>" % self.username
