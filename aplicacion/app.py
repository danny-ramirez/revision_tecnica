#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os,click,json

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restful import Api
from aplicacion.config import app_config
from aplicacion.db import db
from aplicacion.redis import redis
from aplicacion.modelos import *
from aplicacion.helpers.sesion import Sesion
from aplicacion.recursos.login import Login
from aplicacion.recursos.tipo_revision import TipoRevision, TipoRevisionAll
from aplicacion.recursos.persona import AddEncagadoRevision, ListaPersona
from aplicacion.recursos.revision import IngresarVehiculoRevision
from aplicacion.recursos.inspeccion import AddInspeccion


# IMPORTACIÓN DE RECURSOS

app = Flask(__name__)
CORS(app)
db.init_app(app)


#Se establece enviroment como argumento
#enviroment = sys.argv[1]
enviroment ="development"

#enviroment ="production"


#Se setean variables de configuracion segun ambiente(env)
app.config.from_object(app_config[enviroment])
redis.init_app(app)
api = Api(app)

# @app.before_request

# def verifica_token():
# 	if request.method!='OPTIONS':
# 	    if request.endpoint != 'login':
# 	    	if request.endpoint != 'perfiles':
# 		        if request.headers.get('token_id'):
# 		            es_valido = Sesion.validar_token(request.headers.get('token_id'));
# 		            if es_valido == False:
# 		                return jsonify({'message' :'Acceso denegado'}),403
# 		        else:
# 		            return jsonify({'message' :'Acceso denegado'}),403



# SE DEFINEN LOS ENDPOINTS Y LA CLASE QUE SE ENCARGARÁ DE PROCESAR CADA SOLICITUD
# 
api.add_resource(Login, '/login')
api.add_resource(TipoRevision,'/tipo_revision')
api.add_resource(TipoRevisionAll,'/tipo_revision_all')
api.add_resource(AddEncagadoRevision,'/new_encargado_revision')
api.add_resource(ListaPersona,'/listado_persona')
api.add_resource(IngresarVehiculoRevision,'/ingresar_revision')
api.add_resource(AddInspeccion,'/ingresar_inspeccion')


#Se carga host 
app.run(host='0.0.0.0',port=5000)
