# -*- coding: utf8 -*-
from flask import render_template_string, session, render_template, request, flash, redirect, url_for, send_from_directory
from flask_user import login_required, UserManager, allow_unconfirmed_email, current_user
from flask_admin.contrib.sqla import ModelView
from models import User, Guest, City, Room
from config import app, db, admin
from forms import ProfileForm
from views_guests import new_guest, edit_guest, del_guest, del_guest_picture, guest_picture, send_guest_image, toggle_guest_active, list_guests
from views_rooms import new_room, edit_room, del_room, del_room_image, room_picture, send_room_image, toggle_room_active, list_rooms

# Add Admin views
admin.add_view(ModelView(User, db.session))
# Setup Flask-User and specify the User data-model
user_manager = UserManager(app, db, User)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/account', methods=['GET', 'POST'])
@allow_unconfirmed_email
@login_required
def account():
    form = ProfileForm(request.form)
    if request.method == 'GET':
        form.populateForm(current_user)
    if request.method == 'POST' and form.validate():
        current_user.first_name = form.first_name.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        current_user.show_whats = form.show_whats.data
        current_user.can_email = form.can_email.data
        db.session.commit()
        flash('Conta atualizada', 'success')
        return redirect(url_for('index'))
    return render_template('account.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@allow_unconfirmed_email
@login_required
def dashboard():
    guests = db.session.query(Guest).filter(Guest.user_id == current_user.id).all()
    rooms = db.session.query(Room).filter(Room.user_id == current_user.id).all()
    return render_template('dashboard.html', guests=guests, rooms=rooms, user=current_user)

@app.route('/get_cities/<string:state>/', methods=['GET'])
def get_cities(state):
    cities = db.session.query(City).filter(City.state == state).all()
    temp_string = """{% for city in cities %}
                        <option value='{{city.id}}'>{{city.desc}}</option>
                    {% endfor %}"""
    return render_template_string(temp_string, cities=cities)


@app.route('/search')
def search():
    return render_template('search.html')

# Start development web server
if __name__ == '__main__':
    if not User.query.filter(User.email == 'member@example.com').first():
        user = User(email='member@example.com', password=user_manager.hash_password('Password1'))
        db.session.add(user)
        db.session.commit()
    app.run(host='127.0.0.1', port=5000, debug=True)