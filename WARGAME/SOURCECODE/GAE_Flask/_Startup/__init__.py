from flask import Flask, url_for
import settings

app = Flask('_Startup')
app.config.from_object('_Startup.settings')

from _API import api_Handler
from _API import api_Users
from _API import api_Units
from _API import api_Missions
from _API import api_Battles