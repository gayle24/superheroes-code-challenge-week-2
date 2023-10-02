#!/usr/bin/env python3
from flask import make_response, jsonify, session, request
from setup import app, Resource, db, api
from flask_bcrypt import Bcrypt
from models import Hero, HeroPower, Power

@app.route('/')
def home():
    return {"message": "Welcome to the Superheroes home page"}

class Heroes(Resource):
    def get(self):
        hero = Hero.query.all()
        response_dict_list = []
        for item in hero:
            response_dict= {
                "id": item.id,
                "name": item.name,
                "super_name": item.super_name 
            }
            response_dict_list.append(response_dict)
        response = make_response(
            jsonify(response_dict_list),
            200
        )
        return response
api.add_resource(Heroes, '/heroes')

# get first hero that matches the id, and display all info in json format; 
# else if the hero doesn't exist return {"error": "Hero not found"} in json format
# along with status code
class HeroByID(Resource):
    def get(self, id):
        hero = Hero.query.filter_by(id=id).first()
        if hero:
            response_dict = hero.to_dict()
            status_code = 200
        else:
            response_dict = {"error": "Hero not found"}
            status_code = 404

        response = make_response(
            jsonify(response_dict),
            200
        )
        return response
api.add_resource(HeroByID, '/heroes/<int:id>')

class Powers(Resource):
    def get(self):
        power = Power.query.all()
        response_dict_list = []
        for item in power:
            response_dict= {
                "id": item.id,
                "name": item.name,
                "description": item.description 
            }
            response_dict_list.append(response_dict)
        response = make_response(
            jsonify(response_dict_list),
            200
        )
        return response
api.add_resource(Powers, '/powers')

#function to validate the new description in patch request
def validate_power(description):
    if len(description) < 50:
        raise ValueError('Description must be at least 50 characters long')


# get first power that matches the id, and display all info in json format; 
# else if the power doesn't exist return {"error": "Power not found"} in json format
# along with status code
class PowerByID(Resource):
    def get(self, id):
        power = Power.query.filter_by(id=id).first()
        if power:
            response_dict= {
                "id": power.id,
                "name": power.name,
                "description": power.description 
            }
            response = make_response(
                jsonify(response_dict),
                200
            )
            return response
        else:
            return {"error": "Power not found"}
        
    def patch(self, id):
        data = request.json
        new_description = data.get('description')

        # Check if the Power with the specified id exists
        power = Power.query.get(id)

        if not power: # if it doesn't exist, raise an error
            return {"error": "Power not found"}, 404

        if new_description: #set the new description as the new value of power.description
            power.description = new_description

        try: #validate the given description before executing patch request
            validate_power(power.description)
        except ValueError as e:
            return {"errors": [str(e)]}, 400

        db.session.commit()

        # Return the updated Power data
        response_dict = {
            "id": power.id,
            "name": power.name,
            "description": power.description
        }
        return response_dict
api.add_resource(PowerByID, '/powers/<int:id>')

class HeroPowers(Resource):
    def post(self):
        data = request.json

        strength = data.get('strength')
        hero_id = data.get('hero_id')
        power_id = data.get('power_id')

        if None in (strength, hero_id, power_id):
            return {"errors": ["Missing required fields"]}, 400

        hero = Hero.query.get(hero_id)
        power = Power.query.get(power_id)

        if not (hero and power):
            return {"errors": ["Hero or Power not found"]}, 404

        if strength not in ['Strong', 'Weak', 'Average']:
            return {"errors": ["Strength must be defined as Strong, Weak, or Average"]}, 400

        hero_power = HeroPower(
            strength=strength,
            hero_id=hero_id,
            power_id=power_id
        )
        db.session.add(hero_power)
        db.session.commit()

        # Retrieve the related powers for the hero
        hero_powers = [power.to_dict() for power in hero.powers]

        response_data = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "powers": hero_powers
        }
        return response_data, 201
api.add_resource(HeroPowers, '/hero_powers')


if __name__ == '__main__':
    app.run(port=5555)
