#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse
from flask import request, send_file
from datetime import datetime
from aplicacion.modelos.revision import RevisionModel
from aplicacion.modelos.vehiculo import VehiculoModel
from aplicacion.modelos.persona import PersonaModel
from aplicacion.modelos.inspeccion import InspeccionModel
from aplicacion.helpers.utilidades import Utilidades



class AddInspeccion(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('patente',type=str,required=True,help="Debe ingresar patente del vehiculo")
	parser.add_argument('tipo_inspeccion',type=str,required=True,help="Debe ingresar Tipo inspeccion")
	parser.add_argument('estado_inspeccion',type=str,required=True,help="Debe ingresar estado inspeccion")
	parser.add_argument('observaciones',type=str,required=False,help="Debe ingresar observaciones")	

	def post(self):
		data = AddInspeccion.parser.parse_args()
		patente = data['patente']
		tipo_inspeccion = data['tipo_inspeccion']
		estado = data['estado_inspeccion']
		observaciones = data['observaciones'] if 'observaciones' in data else None
		
		try:
			# --------------------------------------------------------------
			# Buscamos la patente en revision
			# --------------------------------------------------------------
			vehiculo = VehiculoModel.buscar_por_patente(patente)
			if vehiculo :
				vehiculoId = vehiculo.id
				vehiculoRevision = RevisionModel.buscar_por_vehiculo(vehiculoId)
				if vehiculoRevision:
					personaId = vehiculoRevision.personaId
					revisionId = vehiculoRevision.id
					print('---------------------------------------------')
					print(personaId)
					print(revisionId)
					print('---------------------------------------------')


					
				return {"success":False, "message":"Vehiculo no esta registrado para revision"}, 200	
			return {"success":False, "message":"Vehiculo no esta registrado"}, 200	
		except Exception as e:
			return {'success': False, 'message': str(e)}, 500