from flask_security import LoginForm
from flask_security.forms import ChangePasswordForm, Length
from wtforms.validators import DataRequired, EqualTo, InputRequired, Required
from wtforms_components import EmailField, Email, Unique
from flask_wtf import Form
from wtforms import StringField, SelectField, BooleanField, PasswordField, SubmitField
from collections import OrderedDict

from core.database import db


password_required = DataRequired(message='Lozinka nije unesena')
password_length = Length(min=6, max=128, message='Lozinka mora sadrzavati izmedju 6 i 128 karaktera')


def choices_from_dict(source, prepend_blank=True):
    choices = []

    if prepend_blank:
        choices.append(('', 'Izaberite jednu opciju...'))

    for key, value in source.items():
        pair = (key, value)
        choices.append(pair)

    return choices
# end def choices_from_dict


class ModelForm(Form):
    def __init__(self, obj=None, prefix='', **kwargs):
        Form.__init__(
            self, obj=obj, prefix=prefix, **kwargs
        )
        self._obj = obj
# end class ModelForm


class ExtendedLoginForm(LoginForm):
    email = StringField('E-mail adresa',
                        validators=[DataRequired(message='E-mail nije unesen')])
    password = PasswordField('Lozinka',
                             validators=[DataRequired(message='Lozinka nije unesena')])
    submit = SubmitField('Prijavi se')
# end class ExtendedLoginForm


class ExtendedChangePasswordForm(ChangePasswordForm):
    password = PasswordField(
        'Stara lozinka', validators=[password_required])
    new_password = PasswordField(
        'Nova lozinka',
        validators=[password_required, password_length])

    new_password_confirm = PasswordField(
        'Ponovite lozinku',
        validators=[EqualTo('new_password',
                            message='Lozinke se ne poklapaju'),
                    password_required])

    submit = SubmitField('Promijeni lozinku')
# end class  ExtendedChangePasswordForm


class NewUserForm(ModelForm):
    from core.model.user import Role, User
    first_name = StringField('Ime', [DataRequired("Ime ne moze biti prazno")])
    last_name = StringField('Prezime', [DataRequired("Prezime ne moze biti prazno")])

    all_roles = Role.query.all()
    roles_dict = OrderedDict()
    for r in all_roles:
        roles_dict[r.name] = r.description
    role = SelectField('Privilegije', [DataRequired()],
                       choices=choices_from_dict(roles_dict,
                                                 prepend_blank=False),
                       default=all_roles[0].name)

    active = BooleanField('Korisnik je aktivan', default=True)

    email = EmailField('E-mail adresa', validators=[
        Unique(User.email, get_session=lambda: db.session),
        DataRequired("E-mail ne moze biti prazan"), Email("Neispravan e-mail")])

    password_ = PasswordField('Lozinka', [
        EqualTo('confirm', message='Lozinke se moraju poklapati')
    ])
    confirm = PasswordField('Ponovite lozinku')
