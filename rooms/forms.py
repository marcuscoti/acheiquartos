# -*- coding: utf8 -*-
from wtforms import Form, StringField, TextAreaField, BooleanField, DateField, FileField, SelectField, validators, IntegerField
from models import City, Guest, Room
from config import db
import re

class ProfileForm(Form):
    email = StringField('E-mail', [validators.email(), validators.InputRequired()])
    first_name = StringField('Nome', [validators.InputRequired()])
    phone = StringField('Telefone', [validators.Length(max=40)])
    show_whats = BooleanField('Mostrar Telefone no site')
    can_email = BooleanField('Permitir o envio de emails')

    def populateForm(self, current_user):
        self.first_name.data = current_user.first_name
        self.email.data = current_user.email
        self.phone.data = current_user.phone
        self.show_whats.data = current_user.show_whats
        self.can_email.data = current_user.can_email

class GuestForm(Form):

    state_choices = [('0', '- Escolha o estado -'), ('sp', 'SP'), ('rj', 'RJ')]
    description = TextAreaField('Descrição'.decode('utf-8'), [validators.Length(max=800)])
    work = BooleanField('Eu trabalho')
    study = BooleanField('Eu estudo')
    pet = BooleanField('Possuo animais')
    car = BooleanField('Possuo carro/moto)')
    smoking = BooleanField('Sou fumante')
    gender = SelectField('Sexo', choices=[('M', 'Homem'), ('F', 'Mulher')])
    age = IntegerField('Idade', [validators.InputRequired(), validators.NumberRange(min=18, message='Você precisa ser maior de 18 anos'.decode('utf-8'))])
    state = SelectField('Estado', choices=state_choices, default=0, validators=[validators.NoneOf(values=['0'], message='Selecione um Estado')])
    city = SelectField('Cidade', coerce=int, default=1, validators=[validators.NumberRange(min=2, message='Selecione uma Cidade')])
    maxValue = IntegerField("Valor Máximo".decode('utf-8'), [validators.InputRequired()])


    def getObj(self, guest):
        guest.age = self.age.data
        guest.gender = self.gender.data
        guest.description = self.description.data
        guest.maxValue = self.maxValue.data
        guest.work = self.work.data
        guest.study = self.study.data
        guest.pet = self.pet.data
        guest.smoking = self.smoking.data
        guest.car = self.car.data
        guest.city_id = self.city.data
        return guest

    def populateForm(self, guest):
        self.description.data = guest.description
        self.work.data = guest.work
        self.study.data = guest.study
        self.pet.data = guest.pet
        self.car.data = guest.car
        self.smoking.data = guest.smoking
        self.gender.data = guest.gender
        self.age.data = guest.age
        city_temp = db.session.query(City).filter(City.id == guest.city_id).one()
        self.state.data = city_temp.state
        self.city.data = guest.city_id
        self.maxValue.data = guest.maxValue


class RoomForm(Form):

    state_choices = [('0', '- Escolha o estado -'), ('sp', 'SP'), ('rj', 'RJ')]
    building_choices = [('apto', 'Apartamento'), ('house', 'Casa'), ('hostel', 'Pousada/Pensionato'), ('hotel', 'Hotel')]
    room_choices = [('single', 'Solteiro'), ('singlec', 'Solteiro Coletivo'), ('couple', 'Casal')]
    bathroom_choices = [('single', 'Individual'), ('public', 'Coletivo'), ('half', 'Compartilhado para dois quartos')]

    title = StringField('Titulo'.decode('utf-8'), [validators.Length(max=50)])
    description = TextAreaField('Descrição'.decode('utf-8'), [validators.Length(max=400)])
    address = StringField('Endereço'.decode('utf-8'), [validators.Length(max=50)])
    number = StringField('Número'.decode('utf-8'), [validators.Length(max=7)])
    region = StringField('Bairro'.decode('utf-8'), [validators.Length(max=50)])
    state = SelectField('Estado', choices=state_choices, default=0, validators=[validators.NoneOf(values=['0'], message='Selecione um Estado')])
    city = SelectField('Cidade', coerce=int, default=1, validators=[validators.NumberRange(min=2, message='Selecione uma Cidade')])
    cep = StringField('CEP'.decode('utf-8'), [validators.Length(max=15)])
    building = SelectField('Tipo de Construção'.decode('utf-8'), choices=building_choices)
    type = SelectField('Tipo de Quarto'.decode('utf-8'), choices=room_choices)
    bathroom = SelectField('Tipo de Banheiro'.decode('utf-8'), choices=bathroom_choices)
    price = IntegerField("Mensalidade em R$".decode('utf-8'), [validators.InputRequired()])
    minRent = IntegerField("Tempo mínimo (meses)".decode('utf-8'), [validators.InputRequired()])
    gender = SelectField('Quarto somente para', choices=[('M', 'Homem'), ('F', 'Mulher'), ('B', 'Homem/Mulher')])
    furniture = BooleanField('Mobiliado')
    include_bills = BooleanField('Contas inclusas')
    smoking = BooleanField('Aceita Fumantes')
    pet = BooleanField('Aceita animais')
    visits = BooleanField('Permite receber visitas')
    aircond = BooleanField('Tem arcondicionado')
    internet = BooleanField('Tem internet')
    parking = BooleanField('Tem estacionamento')
    elevator = BooleanField('Tem elevador')

    def getObj(self, room):
        room.title = self.title.data
        room.description = self.description.data
        room.address = self.address.data
        room.number = self.number.data
        room.region = self.region.data
        room.city_id = self.city.data
        room.cep = self.cep.data
        room.building = self.building.data
        room.type = self.type.data
        room.bathroom = self.bathroom.data
        room.minRent = self.minRent.data
        room.price = self.price.data
        room.gender = self.gender.data
        room.furniture = self.furniture.data
        room.include_bills = self.include_bills.data
        room.smoking = self.smoking.data
        room.pet = self.pet.data
        room.visits = self.visits.data
        room.internet = self.internet.data
        room.parking = self.parking.data
        room.elevator = self.elevator.data
        return room

    def populateForm(self, room):
        self.title.data = room.title
        self.description.data = room.description
        self.address.data = room.address
        self.number.data = room.number
        self.region.data = room.region
        city_temp = db.session.query(City).filter(City.id == room.city_id).one()
        self.state.data = city_temp.state
        self.city.data = room.city_id
        self.cep.data = room.cep
        self.building.data = room.building
        self.bathroom.data = room.bathroom
        self.minRent.data = room.minRent
        self.price.data = room.price
        self.gender.data = room.gender
        self.furniture.data = room.furniture
        self.include_bills.data = room.include_bills
        self.smoking.data = room.smoking
        self.pet.data = room.pet
        self.visits.data = room.visits
        self.internet.data = room.internet
        self.parking.data = room.parking
        self.elevator.data = room.elevator

class FilterGuestForm(Form):
    city = StringField('Cidade'.decode('utf-8'), [validators.Length(max=50)])
    gender = SelectField('Sexo', choices=[('M', 'Homem'), ('F', 'Mulher'), ('B', 'Homem/Mulher')], default='B')
    value_range = StringField('')
    age_range = StringField('')

class FilterRoomForm(Form):
    building_choices = [('all', 'Todos'), ('apto', 'Apartamento'), ('house', 'Casa'), ('hostel', 'Pousada/Pensionato'),
                        ('hotel', 'Hotel')]
    room_choices = [('all', 'Todos'), ('single', 'Individual'), ('singlec', 'Coletivo'), ('couple', 'Casal')]

    city = StringField('Cidade'.decode('utf-8'), [validators.Length(max=50)])
    #building = SelectField('Tipo de Moradia'.decode('utf-8'), choices=building_choices)
    type = SelectField('Tipo de Quarto'.decode('utf-8'), choices=room_choices)
    gender = SelectField('Sexo', choices=[('M', 'Homem'), ('F', 'Mulher'), ('B', 'Homem/Mulher')], default='B')
    value_range = StringField('')
    furniture = BooleanField('Mobiliado')
    include_bills = BooleanField('Contas inclusas')
    smoking = BooleanField('Aceita Fumantes')
    pet = BooleanField('Aceita animais')
    visits = BooleanField('Permite receber visitas')
    aircond = BooleanField('Ar-condicionado')
    internet = BooleanField('Internet')
    parking = BooleanField('Estacionamento')
    elevator = BooleanField('Elevador')