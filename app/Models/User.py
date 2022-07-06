from config.database import db, ma
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    username = db.Column(db.String(100))
    mobile = db.Column(db.String(100))
    age = db.Column(db.String(100))
    state = db.Column(db.String(100))
    city = db.Column(db.String(100))

    def to_json(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'mobile': self.mobile,
            'age': self.age,
            'state': self.state,
            'city': self.city,
        }

# class User(Schema):
#     __tablename__ = "users"
#     id = db.Column(db.Integer, primary_key = True)
#     first_name = db.Column(db.String(100))
#     last_name = db.Column(db.String(100))
#     username = db.Column(db.String(100), unique = True)
#     email = db.Column(db.String(100), unique = True)

    # id = 1
    # first_name = 'a'
    # last_name = 'b'
    # username = 'c'
    # email = 'd'

    # def __init__(self, first_name, last_name):
    #     self.first_name = first_name
    #     self.last_name = last_name

    # def toJSON(self):
    #     return json.dumps(self, default=lambda o: o.__dict__, 
    #         sort_keys=True, indent=4)
# db.create_all()

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'username', 'email')

user_schema = UserSchema() 
users_schema = UserSchema(many=True)