from mongoengine import connect , Document , StringField , EmailField , IntField


connect(host="mongodb://localhost:27017/ekyc")


class User(Document):
    email = EmailField(required=True , unique=True) #unique : check users email and doesnt accept duplicate emails
    hashed_password = StringField(required=True)
    user_level = IntField(required=True)















