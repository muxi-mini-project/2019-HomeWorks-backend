from flask import Blueprint

app = Blueprint('api', __name__)

from . import login, courses, assign, user, notice, search
from . import email, notice_config
