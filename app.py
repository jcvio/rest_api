from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(50), unique=True, nullable=False)
    country = db.Column(db.String(50), unique=True, nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'destination': self.destination,
            'country': self.country,
            'rating': self.rating
        }

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return jsonify(message="Welcome to the Travel Destination API")

@app.route('/destinations', methods=['GET'])
def get_destinations():
    destinations = User.query.all()
    return jsonify([destination.to_dict() for destination in destinations])

@app.route('/destinations/<int:destination_id>', methods=['GET'])
def get_destination(destination_id):
    destination = User.query.get(destination_id)
    if destination:
        return jsonify(destination.to_dict())
    else:
        return jsonify(error="Destination not found"), 404

# POST
@app.route('/destinations', methods=['POST'])
def create_destination():
    data = request.json
    new_destination = User(destination=data['destination'], country=data['country'], rating=data['rating'])
    db.session.add(new_destination)
    db.session.commit()
    return jsonify(new_destination.to_dict()), 201

# PUT
@app.route('/destinations/<int:destination_id>', methods=['PUT'])
def update_destination(destination_id):
    data = request.json
    destination = User.query.get(destination_id)
    if destination:
        destination.destination = data['destination']
        destination.country = data['country']
        destination.rating = data['rating']
        db.session.commit()
        return jsonify(destination.to_dict())
    else:
        return jsonify(error="Destination not found"), 404

# DELETE
@app.route('/destinations/<int:destination_id>', methods=['DELETE'])
def delete_destination(destination_id):
    destination = User.query.get(destination_id)
    if destination:
        db.session.delete(destination)
        db.session.commit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)

