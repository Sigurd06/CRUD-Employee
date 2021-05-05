# run
import os 

from app import create_app

config_name = os.environ.get('FLASK_CONFIG')
app = create_app(config_name)


if __name__ == '__main__':
    app.run()