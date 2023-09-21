#!/usr/bin/env python3

from flask import Flask, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Pet, Owner

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///server/instance/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.init_app(app)

migrate = Migrate(app, db)


@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/pet/<int:id>')
def pet_by_id(id):
    pet = Pet.query.get(id)
    if pet:
        response_body = f'''
            <h1>{pet.name}</h1>
            <h2>Species: {pet.species}</h2>
            <h3>Owner: {pet.owner.name}</h3>
        '''
        status_code = 200
    else:
        response_body = '<h1>Pet not found</h1>'
        status_code = 404

    headers = {}
    return make_response(response_body, status_code, headers)

@app.route('/owner/<int:id>')
def owner_by_id(id):
    owner = Owner.query.get(id)
    if owner:
        pets = owner.pets
        response_body = f'''
            <h1>{owner.name}</h1>
            <h2>Phone: {owner.phone}</h2>
            <h3>Pets:</h3>
            <ul>
        '''
        for pet in pets:
            response_body += f'<li>{pet.name} - {pet.species}</li>'
        response_body += '</ul>'
        status_code = 200
    else:
        response_body = '<h1>Owner not found</h1>'
        status_code = 404


    headers = {}
    return make_response(response_body, status_code, headers)

# 

if __name__ == '__main__':

    app.run(port=5555, debug=True)
