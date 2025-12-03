from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from routes.student_routes import students_bp
from routes.college_routes import colleges_bp
from routes.program_routes import programs_bp
from routes.dashboard_routes import dashboard_bp
from routes.auth_routes import auth_bp
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 86400  # 24 hours
jwt = JWTManager(app)

# Register routes
app.register_blueprint(auth_bp)
app.register_blueprint(students_bp)
app.register_blueprint(colleges_bp)
app.register_blueprint(programs_bp)
app.register_blueprint(dashboard_bp)

if __name__ == "__main__":
    app.run(debug=True)