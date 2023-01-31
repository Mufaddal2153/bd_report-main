####### FORMS ###########
from flask_wtf import FlaskForm
from flask import session
from wtforms_alchemy.fields import QuerySelectField
from wtforms import StringField, IntegerField, SubmitField, FloatField, DateField, SelectField
from wtforms.validators import DataRequired
from model import Project,Designation,Task,User,TimeSheet
class AddProject(FlaskForm):
    work = QuerySelectField(query_factory=lambda: Task.query.filter_by(designation_id=session.get("designation_id")).all(),get_label='work')
    hours = FloatField("Enter hours in decimal")
    submit = SubmitField("Save")
class AddUser(FlaskForm):
    user = StringField('Add User name',validators=[(DataRequired())])
    designation = StringField('Add designation',validators=[(DataRequired())])
    submit = SubmitField('Save')
class AddWork(FlaskForm):
    work = StringField('Add work',validators=[(DataRequired())])
    designation = QuerySelectField(query_factory=lambda: Designation.query.all(),get_label='designation')
    submit = SubmitField('Save')
class ViewProject(FlaskForm):
    project_name = QuerySelectField(query_factory=lambda: Project.query.all(), get_label='project_name')
    submit = SubmitField("Tap to view report")
class ViewUser(FlaskForm):
    user = QuerySelectField(query_factory=lambda: User.query.all(),get_label='user')
    submit = SubmitField("Tap to view report")
class ViewWork(FlaskForm):
    work = QuerySelectField(query_factory=lambda: Task.query.all(),get_label='work')
    submit = SubmitField("Tap to view report")
class AskDesignation(FlaskForm):
    designation = QuerySelectField(query_factory=lambda: Designation.query.all(),get_label='designation')
    submit = SubmitField("Add")
