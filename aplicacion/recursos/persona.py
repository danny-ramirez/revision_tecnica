#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse
from flask import request, send_file
from datetime import datetime
from aplicacion.modelos.persona import PersonaModel
from aplicacion.helpers.utilidades import Utilidades


class ListaPersona(Resource):
	def get(self):
		try:
			allPersona = PersonaModel.listado_all()
			if allPersona:
				result = []
				for persona in allPersona:
					data = {
						"id" : persona.id,
						"identificacion" : persona.identificacion,
						"nombre" : persona.nombre,
						"apellido" : persona.apellido,
						"tipo_persona" : persona.tipo_persona
					}
					result.append(data)
				return {"success":True, "message":"Acción realizada con éxito", "data":result }
			return {'message': 'No se encontró el recurso solicitado'}, 404	
		except Exception as e:
			return {'success': False, 'message': str(e)}, 500			

class AddEncagadoRevision(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('identificacion',type=str,required=True,help="Debe ingresar identificacion encargado")
	parser.add_argument('nombre',type=str,required=True,help="Debe ingresar nombre encargado")
	parser.add_argument('apellido',type=str,required=True,help="Debe ingresar apellido encargado")

	def post(self):
		data = AddEncagadoRevision.parser.parse_args()
		identificacion = data['identificacion']
		nombre = data['nombre']
		apellido = data['apellido']
		try:
			existeEncargado = PersonaModel.buscar_por_identificacion(identificacion)
			if not existeEncargado:
				tipo_persona = "Encargado"
				newEncargado = PersonaModel(identificacion, nombre, apellido, tipo_persona)
				newEncargado.guardar()
				if newEncargado:
					data['id'] = newEncargado.id
					data['tipo_persona'] = tipo_persona

					return {"success":True, "message":"Acción realizada con éxito", "new encargado": data}, 200
				return {"success":False, "message":"Ha ocurrido un error"},	403
			return {"success":False, "message":"Encargado ya existe", "data": existeEncargado}, 200
		except Exception as e:
			return {'success': False, 'message': str(e)}, 500		