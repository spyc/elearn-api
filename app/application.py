import configparser
import importlib
import os

from mysql.connector import Error, errorcode, connection

from tornado.web import Application as App

from .entry import EntryModule
from .handler import Controller


class Application(App):

    dbh = None

    def __init__(self):
        setting = {
            'template_path': os.path.join(os.path.dirname(__file__), '../templates'),
            'static_path': os.path.join(os.path.dirname(__file__), '../static'),
            'ui_modules': {
                'Entry': EntryModule
            },
            'debug': True
        }

        try:
            self.db = {}
            config = configparser.ConfigParser()
            config.read(os.path.join(os.path.dirname(__file__), '../config/database.ini'))
            dbh = connection.MySQLConnection(**dict(config['mysql']))
            self.db['mysql'] = dbh
        except Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)


        super().__init__(**setting)

    def load(self):
        for controller in open(os.path.join(os.path.dirname(__file__), '../config') + '/controllers'):
            controller = controller.strip() + 'Controller'
            module = importlib.import_module('controllers')
            components = controller.split('.')
            for component in components:
                module = getattr(module, component)

            assert issubclass(module, Controller)

            module.register(self)
