from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from neo4j_db import get_db, create_user
from routes.auth import auth_route
from routes.story import story_route

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)

if __name__ == "__main__":
    # with app.app_context():
    #     db = get_db()
    #     results = db.write_transaction(create_user, "Milica", "Petkovic", "milica@elfak.rs", "123")
    
    app.register_blueprint(auth_route)
    app.register_blueprint(story_route)
    app.run(debug=True)