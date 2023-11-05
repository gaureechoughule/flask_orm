from flask import Flask
from user.handlers import handlers
from user.models.model import User, Base
from sqlalchemy import create_engine
from user.connections.connection import config

app = Flask(__name__)

# Creating the database engine
engine = create_engine(f"mysql+mysqlconnector://{config['user']}:{config['password']}@{config['host']}/{config['database']}", echo=True)

# Base.metadata.reflect(bind=engine)          # delete
#
# Base.metadata.tables['user'].drop(engine)
#
# engine.dispose()

Base.metadata.create_all(engine)

app.register_blueprint(handlers)

if __name__ == '__main__':
    app.run(debug=True)








