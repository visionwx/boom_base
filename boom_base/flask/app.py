import os
import json
import argparse

from flask import Flask
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from boom_base.parameters import getEnvPara
from boom_base.configParser import BoomConfig

from gevent import monkey
monkey.patch_all()

class App:
    # flask app
    app = None

    def __init__(self, name, host="0.0.0.0", port=80,):
        self.TAG = name
        self.host = host
        self.port = port
        self.app = self.initApp()

    def initApp(self):
        # 初始化Flask Application对象
        app = Flask(__name__)
        if BoomConfig.getEnableCORS():
            CORS(app, supports_credentials=True)
            cors = CORS()
            cors.init_app(app=app, resources={r"*": {"origins": "*"}})

        # 把当前app放到堆里面，方便其他地方使用
        ctx = app.app_context()
        ctx.push()

        @app.route('/')
        def home():
            return 'hello'
        
        return app
    
    def registerBlueprint(self, bluePrint):
        self.app.register_blueprint(bluePrint, 
            url_prefix='/' + bluePrint.name)

    def run(self):
        print("app run on " + self.host + ":" + str(self.port))
        http_server = WSGIServer(
            (self.host, self.port), 
            self.app, 
            handler_class=WebSocketHandler)
        http_server.serve_forever()
    
