import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from analytics import analytics_bp
from auth import auth_bp
from db import init_db
from leads import leads_bp
from projects import projects_bp
from reviews import reviews_bp

load_dotenv(override=True)

app = Flask(__name__)
CORS(app, origins=["*"])

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'skyforge-secret-key-2024')
app.config['MONGO_URI'] = os.environ.get(
    'MONGO_URI',
    'mongodb://localhost:27017/skyforge'
)
app.config['MONGO_DB_NAME'] = os.environ.get('MONGO_DB_NAME', 'skyforge')

init_db(app)

app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(leads_bp, url_prefix='/api')
app.register_blueprint(projects_bp, url_prefix='/api')
app.register_blueprint(reviews_bp, url_prefix='/api')
app.register_blueprint(analytics_bp, url_prefix='/api')

@app.route('/')
def index():
    return {'message': 'SkyForge API Running', 'status': 'ok'}

if __name__ == '__main__':
    app.run(debug=True, port=5000)
