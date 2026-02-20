from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, Regexp

class IncidentForm(FlaskForm):
    fio = StringField('ФИО', validators=[
        DataRequired(message='ФИО обязательно для заполнения'),
        Length(min=2, message='ФИО должно содержать минимум 2 символа')
    ])
    
    event_datetime = StringField(
        'Дата и время события',
        validators=[
            DataRequired(message='Дата и время обязательны'),
            Regexp(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$', message='Неверный формат даты (YYYY-MM-DDTHH:MM)')
        ]
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
        Optional(),
        NumberRange(min=1, max=365, message='Значение должно быть от 1 до 365 дней')
    ])
    
    event_description = TextAreaField('Описание события', validators=[
        Optional()
    ])
    
    engineer_actions = TextAreaField('Действия инженера', validators=[
        Optional()
    ])
