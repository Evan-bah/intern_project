from mongoengine.fields import EmbeddedDocumentField, IntField, StringField
from mongoengine import Document


class Instagram_Post(Document):
    username = StringField()
    likes = IntField()
    comments = IntField()
    description = StringField()
    search_tag = StringField()

    def to_dict(self):
        return {'username'    : self.username,
        		'likes'       : self.likes,
        		'comments'    : self.comments,
        		'descriptions': self.description,
                'search_tag'  : self.search_tag}
