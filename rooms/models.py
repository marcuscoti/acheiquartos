# -*- coding: utf8 -*-
from flask_user import UserMixin
from config import db
from datetime import datetime

# Define the User data-model.
# NB: Make sure to add flask_user UserMixin !!!
class User(db.Model, UserMixin):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    # User authentication information. The collation='NOCASE' is required
    # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
    email = db.Column(db.String(255, collation='NOCASE'), nullable=False, unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')

    # User information
    first_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    last_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    phone = db.Column(db.String(100), nullable=True)
    show_whats = db.Column('show_whats', db.Integer(), nullable=False, default='1')
    can_email = db.Column('can_email', db.Integer(), nullable=False, default='1')
    status = db.Column(db.String(100), nullable=True)
    active = db.Column('is_active', db.Integer(), nullable=False, default='1')
    last_login = db.Column(db.DateTime())
    created = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    last_modified = db.Column(db.DateTime(), nullable=False, default=datetime.now())

class Guest(db.Model):
    __tablename__ = 'guests'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    gender = db.Column(db.String(2), nullable=True)
    age = db.Column(db.Integer(), nullable=True)
    description = db.Column(db.Text(), nullable=True)
    picture = db.Column(db.String(100), nullable=True, default='picna.jpg')
    work = db.Column(db.Boolean(), nullable=False, server_default='0')
    study = db.Column(db.Boolean(), nullable=False, server_default='0')
    smoking = db.Column(db.Boolean(), nullable=False, server_default='0')
    pet = db.Column(db.Boolean(), nullable=False, server_default='0')
    car = db.Column(db.Boolean(), nullable=False, server_default='0')
    maxValue = db.Column(db.Integer(), nullable=True)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    last_modified = db.Column(db.DateTime(), nullable=False, default=datetime.now())

    def getCity(self):
        city = db.session.query(City).filter(City.id == self.city_id).one()
        return city.desc

    def getUser(self):
        user = db.session.query(User).filter(User.id == self.user_id).one()
        return user

    def get_bool_attr(self, attr):
        value = self.__getattribute__(attr)
        if value: return 'Sim'
        else: return 'Não'.decode('utf-8')

    def get_gender_attr(self):
        if self.gender == 'F': return 'Mulher'
        if self.gender == 'M': return 'Homem'
        if self.gender == 'B': return 'Homem/Mulher'


class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    desc = db.Column(db.String(30), nullable=False)
    state = db.Column(db.String(2), nullable=False)


class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text(), nullable=True)
    address = db.Column(db.String(50), nullable=True)
    number = db.Column(db.String(7), nullable=True)
    region = db.Column(db.String(50), nullable=True)
    cep = db.Column(db.String(15), nullable=True)
    lat = db.Column(db.Float(), nullable=True)
    long = db.Column(db.Float(), nullable=True)
    building = db.Column(db.String(5), nullable=False)
    type = db.Column(db.String(5), nullable=False)
    bathroom = db.Column(db.String(5), nullable=False)
    minRent = db.Column(db.Integer(), nullable=True, default=1)
    price = db.Column(db.Integer(), nullable=False, default=0)
    gender = db.Column(db.String(2), nullable=True)
    main_image = db.Column(db.String(100), nullable=True, default='default')
    imageServer = db.Column(db.String(15), nullable=True)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    views = db.Column(db.Integer(), nullable=True, default=0)
    views7days = db.Column(db.Integer(), nullable=True, default=0)
    furniture = db.Column(db.Boolean(), nullable=False, server_default='0')
    include_bills = db.Column(db.Boolean(), nullable=False, server_default='0')
    smoking = db.Column(db.Boolean(), nullable=False, server_default='0')
    pet = db.Column(db.Boolean(), nullable=False, server_default='0')
    visits = db.Column(db.Boolean(), nullable=False, server_default='0')
    aircond = db.Column(db.Boolean(), nullable=False, server_default='0')
    internet = db.Column(db.Boolean(), nullable=False, server_default='0')
    parking = db.Column(db.Boolean(), nullable=False, server_default='0')
    elevator = db.Column(db.Boolean(), nullable=False, server_default='0')
    last_modified = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    created = db.Column(db.DateTime(), nullable=False, default=datetime.now())


    def getCity(self):
        city = db.session.query(City).filter(City.id == self.city_id).one()
        return city.desc

    def get_bool_attr(self, attr):
        value = self.__getattribute__(attr)
        if value: return 'Sim'
        else: return 'Não'.decode('utf-8')

    def get_gender_attr(self):
        if self.gender == 'F': return 'Mulher'
        if self.gender == 'M': return 'Homem'
        if self.gender == 'B': return 'Homem/Mulher'

    def get_building_attr(self):
        if self.building == 'apto': return 'Apartamento'
        if self.building == 'house': return 'Casa'
        if self.building == 'hostel': return 'Pensionato'
        if self.building == 'hotel': return 'Hotel'

    def get_room_attr(self):
        if self.type == 'single': return 'Individual'
        if self.type == 'singlec': return 'Solteiro Coletivo'
        if self.type == 'couple': return 'Casal'

    def get_bathroom_attr(self):
        if self.bathroom == 'single': return 'Individual'
        if self.bathroom == 'public': return 'Coletivo'
        if self.bathroom == 'half': return 'Compartilhado para dois quartos'


class Views(db.Model):
    __tablename__ = 'views'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(10), nullable=False)
    obj_id = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime(), nullable=False, default=datetime.now())

    def __init__(self, user, type, obj):
        self.user_id=user
        self.type=type
        self.obj_id=obj

if __name__ == '__main__':
    db.create_all()
    # Create 'member@example.com' user with no roles
