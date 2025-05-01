from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

class EncryptForm(FlaskForm):
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Encrypt")

class DecryptForm(FlaskForm):
    ciphertext = TextAreaField("Ciphertext", validators=[DataRequired()])
    submit = SubmitField("Decrypt")