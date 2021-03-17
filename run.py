
from app import app
from db import db

db.init_app(app)                # **NOTE**

@app.before_first_request       # **NOTE**
def create_tables():
    db.create_all()             # **NOTE**
