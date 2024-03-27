from mongoengine import Document, StringField, ListField, ReferenceField, CASCADE, BooleanField


class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=50)
    description = StringField()
    meta = {"collection": "authors"}

class Quote(Document):
    tags = ListField(StringField(max_length=20))
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    quote = StringField()
    meta = {"collection": "quotes"}

class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    sent = BooleanField(default=False)
