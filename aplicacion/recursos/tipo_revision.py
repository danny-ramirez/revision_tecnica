#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse
from flask import request, send_file
from datetime import datetime
from aplicacion.modelos.tipo_revision import TipoRevisionModel
from aplicacion.helpers.utilidades import Utilidades

class TipoRevision(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('id',type=int,required=True,help="Debe ingresar id tipo de revision")
	def get(self):
		data = TipoRevision.parser.parse_args()
		_id = data['id']
		try:
			print(_id)
			tipo_revision = TipoRevisionModel.buscar_por_id(_id)
			if tipo_revision:
				return tipo_revision.obtener_datos()
			return {'message': 'No se encontró el recurso solicitado'}, 404
		except Exception as e:
			return {'success': False, 'message': str(e)}, 500	

class TipoRevisionAll(Resource):	
	def get(self):
		try:
			tipo_revision = TipoRevisionModel.buscar_all()
			if tipo_revision:
				result = []
				for tipo in tipo_revision:
					data = {
						'id' : tipo.id,
						'nombre_tipo' : tipo.nombre_tipo
					}
					result.append(data)
				return {"success":True, "message":"Acción realizada con éxito", "data":result }, 200
			return {'message': 'No se encontró el recurso solicitado'}, 404
		except Exception as e:
			return {'success': False, 'message': str(e)}, 500			