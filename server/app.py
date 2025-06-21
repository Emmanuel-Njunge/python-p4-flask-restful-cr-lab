#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plant_list=[plant.to_dict() for plant in Plant.query.all()]
        response=make_response(
            jsonify(plant_list),
            200
        )

        return response
    

    def post(self):
        data =request.get_json()
        added_plant=Plant(
            name=data.get('name'),
            image=data.get('image'),
            price=data.get('price')
        )
        db.session.add(added_plant)
        db.session.commit()

        response_body=added_plant.to_dict()

        response=make_response(
            response_body,
            201
        )

        return response

api.add_resource(Plants,'/plants')



class PlantByID(Resource):
    def get(self,id):
        plant=Plant.query.get(id)
        response_body=plant.to_dict()

        response=make_response(
            jsonify(response_body),
            200
        )

        return response


api.add_resource(PlantByID,'/plants/<int:id>')



        

if __name__ == '__main__':
    app.run(port=5555, debug=True)