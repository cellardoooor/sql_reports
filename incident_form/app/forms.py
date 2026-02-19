from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, TextAreaField, DateTimeLocalField
from wtforms.validators import DataRequired, Length, NumberRange

class IncidentForm(FlaskForm):
    fio = StringField('ФИО', validators=[
        DataRequired(message='ФИО обязательно для заполнения'),
        Length(min=2, message='ФИО должно содержать минимум 2 символа')
    ])
    
    event_datetime = DateTimeLocalField(
        'Дата и время события',
        format='%Y-%m-%dT%H:%M',
        validators=[DataRequired(message='Дата и время обязательны')]
    )
    
    tag = SelectField('Тег', choices=[
        ('', 'Выберите тег'),
        ('Мониторинг', 'Мониторинг'),
        ('Латенси', 'Латенси'),
        ('Информация', 'Информация'),
        ('Массовое', 'Массовое'),
        ('ОТМ', 'ОТМ'),
        ('Veeam', 'Veeam')
    ], validators=[DataRequired(message='Выберите тег')])
    
    validity_days = IntegerField('Актуальность (дней)', validators=[
        DataRequired(message='Укажите срок актуальности'),
        NumberRange(min=1, max=365, message='Значение должно быть от 1 до 365 дней')
    ])
    
    event_description = TextAreaField('Описание события', validators=[
        DataRequired(message='Описание обязательно'),
        Length(min=10, message='Описание должно содержать минимум 10 символов')
    ])
    
    engineer_actions = TextAreaField('Действия инженера', validators=[
        DataRequired(message='Укажите действия инженера')
    ])
