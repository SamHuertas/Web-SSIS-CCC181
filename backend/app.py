from flask import Flask
from routes.students import students_bp
from routes.colleges import colleges_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  

# Register routes
app.register_blueprint(students_bp)
app.register_blueprint(colleges_bp)

if __name__ == "__main__":
    app.run(debug=True)
