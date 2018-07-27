# -*- coding: utf8 -*-
from flask import render_template_string, session, render_template, request, flash, redirect, url_for, send_from_directory
from flask_user import login_required, allow_unconfirmed_email, current_user
from models import City, Room, User, Views
from config import app, db
from forms import RoomForm, FilterRoomForm
from helpers import validate_upload_file, save_room_picture
import os
import shutil

@app.route('/new_room', methods=['GET', 'POST'])
@allow_unconfirmed_email
@login_required
def new_room():
    form = RoomForm(request.form)
    form.city.choices = [(city.id, city.desc) for city in db.session.query(City).all()]
    if request.method == 'POST' and form.validate():
        room = form.getObj(Room())
        room.user_id = current_user.id
        db.session.add(room)
        db.session.commit()
        path = "rooms/room" + str(room.id)
        os.mkdir(path)
        flash('Anúncio adicionado'.decode('utf-8'), 'success')
        return redirect(url_for('dashboard'))
    return render_template('room/edit_room.html', form=form, action='Adicionar')

@app.route('/edit_room/<string:id>/', methods=['GET', 'POST'])
@allow_unconfirmed_email
@login_required
def edit_room(id):
    room = db.session.query(Room).filter(Room.id == id).one()
    form = RoomForm(request.form, room)
    form.city.choices = [(city.id, city.desc) for city in db.session.query(City).all()]
    if request.method == 'GET':
        city = City.query.get(room.city_id)
        form.city.choices = [(city.id, city.desc) for city in
                             db.session.query(City).filter(City.state == city.state).all()]
        form.populateForm(room)
    if request.method == 'POST' and form.validate():
        room = form.getObj(room)
        db.session.commit()
        flash('Anúncio Atualizado'.decode('utf-8'), 'success')
        return redirect(url_for('dashboard'))
    return render_template('room/edit_room.html', form=form, action='Editar')

@app.route('/toggle_room_active/<string:id>/', methods=['GET', 'POST'])
@allow_unconfirmed_email
@login_required
def toggle_room_active(id):
    room = db.session.query(Room).filter(Room.id == id).one()
    if room.active == 1: room.active = 0
    else: room.active = 1
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/del_room/<string:id>/', methods=['GET', 'POST'])
@allow_unconfirmed_email
@login_required
def del_room(id):
    room = db.session.query(Room).filter(Room.id == id).one()
    db.session.delete(room)
    db.session.commit()
    path = "rooms/room" + str(room.id)
    shutil.rmtree(path, True)
    flash('Anúncio deletado'.decode('utf-8'), 'success')
    return redirect(url_for('dashboard'))

@app.route('/room_picture/<string:id>/', methods=['GET', 'POST'])
@allow_unconfirmed_email
@login_required
def room_picture(id):
    room = db.session.query(Room).filter(Room.id == id).one()
    path = "rooms/room" + str(room.id)
    files = os.listdir(path)
    if request.method == 'POST':
        uploaded_files = request.files.getlist('files')
        save_room_picture(room, uploaded_files)
        flash('Foto atualizada', 'success')
        return redirect(url_for('room_picture', id=id))
    return render_template('room/room_picture.html', room=room, user=current_user, files=files)


@app.route('/del_room_image/<room_id>/<filename>')
def del_room_image(room_id, filename):
    path = "rooms/room" + room_id
    os.remove(os.path.join(path, filename))
    return ('', 204)

@app.route('/set_main_image/<room_id>/<filename>')
def set_main_image(room_id, filename):
    room = db.session.query(Room).filter(Room.id == room_id).one()
    room.main_image = filename
    db.session.commit()
    return redirect(url_for('room_picture', id=room_id))

@app.route('/upload_room_image/<room_id>/<filename>')
def send_room_image(room_id, filename):
    path = "rooms/room"+room_id
    files = os.listdir(path)
    if filename == 'default':
        if len(files) == 0:
            return send_from_directory('rooms', 'new_image.jpg')
        else:
            return send_from_directory(path, files[0])
    else:
        complete_path = "rooms/room" + room_id + '/' + filename
        if os.path.isfile(complete_path):
            return send_from_directory(path, filename)
        else:
            return send_from_directory('rooms', 'new_image.jpg')

@app.route('/room/<string:id>')
def view_room(id):
    room = db.session.query(Room).filter(Room.id == id).one()
    user = db.session.query(User).filter(User.id == room.user_id).one()
    path = "rooms/room" + str(room.id)
    files = os.listdir(path)
    log_view_room(id)
    return render_template('room/room.html', room=room, roomUser=user, current_user=current_user, files=files)

def log_view_room(room_id):
    if hasattr(current_user, 'id'):
        view = Views(current_user.id, 'room', room_id)
    else:
        view = Views(0, 'room', room_id)
    db.session.add(view)
    db.session.commit()

@app.route('/rooms', methods=['GET', 'POST'])
@app.route('/rooms/<string:city_name>/<string:city_id>', methods=['GET', 'POST'])
def list_rooms(city_name=None, city_id=0):
    cities = db.session.query(City).filter(City.id > 1).all()
    if request.method == 'POST' and 'form_filter' in request.form:
        form_filter = FilterRoomForm(request.form)
        print request.form
        if form_filter.validate():
            query = db.session.query(Room)
            if form_filter.city.data != '':
                qcity = db.session.query(City).filter(City.desc == form_filter.city.data).one()
                query = query.filter(Room.city_id == qcity.id)
            if form_filter.gender.data != 'B':
                query = query.filter(Room.gender == form_filter.gender.data)

            min, dump, max = form_filter.value_range.data.split(' ')
            minValue = min[2:]
            maxValue = max[2:]
            query = query.filter(Room.price >= minValue, Room.price <= maxValue)

            if form_filter.type.data != 'all':
                query = query.filter(Room.type == form_filter.type.data)

            if form_filter.furniture.data:
                query = query.filter(Room.furniture == 1)

            if form_filter.include_bills.data:
                query = query.filter(Room.include_bills == 1)

            if form_filter.smoking.data:
                query = query.filter(Room.smoking == 1)

            if form_filter.pet.data:
                query = query.filter(Room.pet == 1)

            if form_filter.visits.data:
                query = query.filter(Room.visits == 1)

            if form_filter.aircond.data:
                query = query.filter(Room.aircond == 1)

            if form_filter.internet.data:
                query = query.filter(Room.internet == 1)

            if form_filter.parking.data:
                query = query.filter(Room.parking == 1)

            if form_filter.elevator.data:
                query = query.filter(Room.elevator == 1)

            query = query.filter(Room.active == 1)
            rooms = query.all()
            ranges = {'minValue': minValue, 'maxValue': maxValue}
            if len(rooms) == 0:
                flash('Não foram encontrados anúncios com estes filtros!'.decode('utf-8'), 'danger')
    else:
        form_filter = FilterRoomForm(request.form)
        ranges = {'minValue': 100, 'maxValue': 1000}
        if city_id > 0:
            rooms = db.session.query(Room).filter(Room.city_id == city_id, Room.active == 1).all()
            form_filter.city.data = city_name
        else:
            rooms = db.session.query(Room).filter(Room.active == 1).all()

    return render_template('search.html', rooms=rooms, current_user=current_user, cities=cities, form_filter=form_filter, ranges=ranges)