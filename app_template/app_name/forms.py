from wtforms import BooleanField, TextField
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField, QuerySelectField
from wtforms.validators import DataRequired, Length
from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired

from models import Category, db

class ApplicationForm(Form):
    package = TextField('Package', [Length(min=4, max=255)])
    name = TextField('Name', [Length(min=4, max=40)])
    summary = TextField('Summary', [Length(min=4, max=255)])
    description = TextField('Description', [Length(min=4)])

    icon = FileField('Icon')

    categories = QuerySelectMultipleField(query_factory=lambda: db.session.query(Category),
            get_label='name')
    #packages = db.relationship('Package', backref='application',
