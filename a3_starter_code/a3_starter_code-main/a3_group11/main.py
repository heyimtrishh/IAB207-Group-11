import logging
from craftunityevents import create_app

if __name__ == '__main__':
    logging.basicConfig(filename='error.log', level=logging.DEBUG)
    app = create_app()
    app.run(debug=True)