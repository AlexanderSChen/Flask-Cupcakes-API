"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from models import db, connect_db, Cupcake 

app = Flask(__name__)
CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'
# cors = CORS(app, resources={r"/api/*": {"origins": "*", "allow_headers": "*", "expose_headers": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SECRET_KEY'] = 'SECRETAFKEY'

connect_db(app)

@app.route('/')
# @cross_origin()
def show_index():
    """Render index.html template"""

    return render_template('index.html')

@app.route('/api/cupcakes')
def list_cupcakes():
    """Return JSON with all cupcakes"""

    cupcakes = [cupcake.to_dict() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
    """Return information about cupcake with associated id"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake = cupcake.to_dict())

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """Create a new upcake and return JSON of created cupcake"""

    data = request.json

    cupcake = Cupcake(flavor = data["flavor"], 
                      size = data["size"], 
                      rating = data["rating"], 
                      image = data["image"] or None)

    db.session.add(cupcake)
    db.session.commit()

    return (jsonify(cupcake=cupcake.to_dict()), 201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Update cupcake from data in request and return updated data"""

    data = request.json

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = data['flavor']
    cupcake.rating = data['rating']
    cupcake.size = data['size']
    cupcake.image = data['image']

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake = cupcake.to_dict())

@app.route('/api/cupcakes/<int:cupcake_id>', methods=["DELETE"])
def remove_cupcake(cupcake_id):
    """Delete cupcake and notify user. Return JSON {message: "Deleted" """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Cupcake Successfully Deleted")