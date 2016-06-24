from mongoengine.fields import EmbeddedDocumentField, IntField, StringField, ListField
from mongoengine import Document


class Instagram_Post(Document):
    username = StringField()
    likes = IntField()
    comments = IntField()
    description = StringField()
    time_posted = StringField()
    hash_tags = ListField(StringField)
    extraction_time = StringField()


    def to_dict(self):
        return {'username'          : self.username,
        		'likes'             : self.likes,
        		'comments'          : self.comments,
        		'description'       : self.description,
                'time_posted'       : self.time_posted,
                'hash_tags'         : self.has_tags,
                'extraction_time'   : self.extraction_time}
