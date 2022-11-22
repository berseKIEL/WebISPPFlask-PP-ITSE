# Importación de Flask
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user

# Desarrollo de la vista Login

usuario = Blueprint('user', __name__)

@usuario.route('/')
def index():
    return render_template('')