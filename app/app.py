#!/usr/bin/env python3
from flask import make_response, jsonify, session, request
from setup import app, Resource,db,api
from flask_bcrypt import Bcrypt
from models import Hero, HeroPower, Power

@app.route('/')
def home():
    return ''


if __name__ == '__main__':
    app.run(port=5555)
