from flask import Flask, Blueprint
from routes.readApi import main
import os
#from flask_heroku import Heroku

app = Flask(__name__)

#heroku = Heroku(app)

port = int(os.environ.get('PORT', 5000))    

app.register_blueprint(main)
if __name__ == '__main__':
    app.run(threaded=True,host='0.0.0.0', port=port)
