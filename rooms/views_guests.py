# -*- coding: utf8 -*-
from flask import render_template_string, session, render_template, request, flash, redirect, url_for, send_from_directory
from flask_user import login_required, allow_unconfirmed_email, current_user
from models import User, Guest, City, Views
from config import app, db
from forms import GuestForm, FilterGuestForm
from helpers import validate_upload_file, save_guest_picture
from sqlalchemy.sql.expression import text
import os

@app.route('/edit_guest/<string:id>/', methods=['GET', 'POST'])
@allow_unconfirmed_email
@login_required
def edit_guest(id):
    guest = db.session.query(Guest).filter(Guest.id == id).one()
    form = GuestForm(request.form, guest)
    form.city.choices = [(city.id, city.desc) for city in db.session.query(City).all()]
    if request.method == 'GET':
        city = City.query.get(guest.city_id)
        form.city.choices = [(city.id, city.desc) for city in
                             db.session.query(City).filter(City.state == city.state).all()]
        form.populateForm(guest)
    if request.method == 'POST' and form.validate():
        guest = form.getObj(guest)
        db.session.commit()
        flash('Anúncio Atualizado'.decode('utf-8'), 'success')
        return redirect(url_for('dashboard'))
    return render_template('guest/edit_guest.html', form=form, action='Editar')

@app.route('/new_guest', methods=['GET', 'POST'])
@allow_unconfirmed_email
@login_required
def new_guest():
    form = GuestForm(request.form)
    form.city.choices = [(city.id, city.desc) for city in db.session.query(City).all()]
    if request.method == 'POST' and form.validate():
        guest = form.getObj(Guest())
        guest.user_id = current_user.id
        guest.picture='picna.jpg'
        db.session.add(guest)
        db.session.commit()
        flash('Anúncio adicionado'.decode('utf-8'), 'success')
        return redirect(url_for('dashboard'))
    return render_template('guest/edit_guest.html', form=form, action='Adicionar')


@app.route('/toggle_guest_active/<string:id>/', methods=['GET', 'POST'])
@allow_unconfirmed_email
@login_required
def toggle_guest_active(id):
    guest = db.session.query(Guest).filter(Guest.id == id).one()
    if guest.active == 1: guest.active = 0
    else: guest.active = 1
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/del_guest/<string:id>/', methods=['GET', 'POST'])
@allow_unconfirmed_email
@login_required
def del_guest(id):
    guest = db.session.query(Guest).filter(Guest.id == id).one()
    db.session.delete(guest)
    db.session.commit()
    flash('Anúncio deletado'.decode('utf-8'), 'success')
    return redirect(url_for('dashboard'))

@app.route('/guest_picture/<string:id>/', methods=['GET', 'POST'])
@allow_unconfirmed_email
@login_required
def guest_picture(id):
    guest = db.session.query(Guest).filter(Guest.id == id).one()
    if request.method == 'POST':
        res, message = validate_upload_file(request)
        if res == False:
            flash(message, 'danger')
            return redirect(request.url)
        guest.picture = save_guest_picture(guest, request.files['file'])
        db.session.commit()
        flash('Foto atualizada', 'success')
        return redirect(url_for('dashboard'))
    return render_template('guest/guest_picture.html', guest=guest, user=current_user)

@app.route('/del_guest_picture/<string:id>/', methods=['GET', 'POST'])
@allow_unconfirmed_email
@login_required
def del_guest_picture(id):
    guest = db.session.query(Guest).filter(Guest.id == id).one()
    os.remove(os.path.join('guests', guest.picture))
    guest.picture = 'picna.jpg'
    db.session.commit()
    flash('Foto removida', 'success')
    return redirect(url_for('dashboard'))

@app.route('/upload_guest/<filename>')
def send_guest_image(filename):
    return send_from_directory("guests", filename)

@app.route('/guest/<string:id>')
def view_guest(id):
    guest = db.session.query(Guest).filter(Guest.id == id).one()
    user = db.session.query(User).filter(User.id == guest.user_id).one()
    log_view_guest(id)
    return render_template('guest/guest.html', guest=guest, guestUser=user, current_user=current_user)

def log_view_guest(guest_id):
    if hasattr(current_user, 'id'):
        view = Views(current_user.id, 'guest', guest_id)
    else:
        view = Views(0, 'room', guest_id)
    db.session.add(view)
    db.session.commit()

@app.route('/guests', methods=['GET', 'POST'])
@app.route('/guests/<string:city_name>/<string:city_id>', methods=['GET', 'POST'])
def list_guests(city_name=None, city_id=0):
    cities = db.session.query(City).filter(City.id > 1).all()
    if request.method == 'POST' and 'form_filter' in request.form:
        form_filter = FilterGuestForm(request.form)
        if form_filter.validate():
            query = db.session.query(Guest)
            if form_filter.city.data != '':
                qcity = db.session.query(City).filter(City.desc == form_filter.city.data).one()
                query = query.filter(Guest.city_id == qcity.id)
            if form_filter.gender.data != 'B':
                query = query.filter(Guest.gender == form_filter.gender.data)

            min, dump, max = form_filter.value_range.data.split(' ')
            minValue = min[2:]
            maxValue = max[2:]
            query = query.filter(Guest.maxValue >= minValue, Guest.maxValue <= maxValue)

            minAge, dump, maxAge = form_filter.age_range.data.split(' ')
            query = query.filter(Guest.age >= minAge, Guest.age <= maxAge)

            query = query.filter(Guest.active == 1)
            guests = query.all()
            ranges = {'minValue': minValue, 'maxValue': maxValue, 'minAge':minAge, 'maxAge':maxAge}
            if len(guests) == 0:
                flash('Não foram encontrados anúncios com estes filtros!'.decode('utf-8'), 'danger')
    else:
        form_filter = FilterGuestForm(request.form)
        ranges = {'minValue': 100, 'maxValue': 1000, 'minAge':18, 'maxAge':99}
        if city_id > 0:
            guests = db.session.query(Guest).filter(Guest.city_id == city_id, Guest.active == 1).all()
            form_filter.city.data = city_name
        else:
            guests = db.session.query(Guest).filter(Guest.active == 1).all()
    return render_template('search.html', guests=guests, current_user=current_user, cities=cities, form_filter=form_filter, ranges=ranges)