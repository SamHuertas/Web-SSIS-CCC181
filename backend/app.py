from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from routes.student_routes import students_bp
from routes.college_routes import colleges_bp
from routes.program_routes import programs_bp
from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(
    __name__,
    static_folder="dist",      
    static_url_path="/"        
)
CORS(app)

# JWT config
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 86400
jwt = JWTManager(app)

# Register API blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(students_bp)
app.register_blueprint(colleges_bp)
app.register_blueprint(programs_bp)
app.register_blueprint(dashboard_bp)    

# Serve frontend
@app.route("/")
def serve_frontend():
    return app.send_static_file("index.html")

if __name__ == "__main__":
    app.run(debug=True)
