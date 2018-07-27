# -*- coding: utf8 -*-
import os, sys
from werkzeug.utils import secure_filename
from PIL import Image
import datetime
from io import BytesIO
from models import Views

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_upload_file(request):
    if 'file' not in request.files:
        return (False, 'Nenhum arquivo carregado')
    file = request.files['file']
    if file.filename == '':
        return (False, 'Nenhum arquivo selecionado')
    file_size = request.form['file_size']
    file_size = float(file_size)
    if file_size > 1000:
        return (False, 'Arquivo muito grande, máximo de 1MB'.decode('utf-8'))
    if not(allowed_file(file.filename)):
        return (False, 'Formato de arquivo não aceito - Selecione somente arquivos JPG, JPEG ou PNG'.decode('utf-8'))
    return (True, 'validado')


def save_guest_picture(guest, file):
    filename = secure_filename(file.filename)
    filename2 = filename.split('.')
    ext = filename2[len(filename2) - 1]
    filename = 'guest' + str(guest.id) + '.' + ext
    file.save(os.path.join('guests', filename))
    return filename


def save_room_picture(room, files):
    path = "rooms/room" + str(room.id)
    size = 800, 600
    for file in files:
        im = Image.open(BytesIO(file.read()))
        im.thumbnail(size)
        filename = secure_filename(file.filename)
        im.save(os.path.join(path, filename))





