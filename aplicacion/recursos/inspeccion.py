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

class DeleteInspeccion(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('patente',type=str,required=True,help="Debe ingresar patente del vehiculo")
	parser.add_argument('tipo_inspeccion',type=str,required=True,help="Debe ingresar Tipo inspeccion")
	
	def delete(self):
		data = DeleteInspeccion.parser.parse_args()
		patente = data['patente']
		tipo_inspeccion = data['tipo_inspeccion']
		try:
			id_tipo_inspeccion = 0
			if tipo_inspeccion.lower() == 'frenos':
				id_tipo_inspeccion = 1
			elif tipo_inspeccion.lower() == 'gases':
				id_tipo_inspeccion = 2;
			elif tipo_inspeccion.lower() == 'luces':
				id_tipo_inspeccion = 3
			
			if id_tipo_inspeccion == 0:
				return {"success":False, "message":"tipo inspeccion no valido", "data": data}, 404
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
					# -----------------------------------------------------------
					# Buscamos si la inspeccion que se quiere eliminar
					# -----------------------------------------------------------
					InspeccionEliminar = InspeccionModel.buscar_inspeccion(revisionId, personaId, id_tipo_inspeccion)
					if InspeccionEliminar:
						InspeccionEliminar.eliminar()
						return {"success":True, "message":"Acción realizada con éxito"}, 200
					return {"success":False, "message":"Vehiculo patente "+patente+" no  posee inspeccion de "+tipo_inspeccion}, 200
				return {"success":False, "message":"Vehiculo no esta registrado para revision"}, 200	
			return {"success":False, "message":"Vehiculo no esta registrado"}, 200		
				
		except Exception as e:
			return {'success': False, 'message': str(e)}, 500	



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
		
		estados_revision = {
			0 : 'Rechazada',
			1 : 'Aprobada'
		}

		estado_inspecciones = {
			0 : 'Rechazada',
			1 : 'Aprobada'
		}

		id_tipo_inspeccion = 0
		if tipo_inspeccion.lower() == 'frenos':
			id_tipo_inspeccion = 1
		elif tipo_inspeccion.lower() == 'gases':
			id_tipo_inspeccion = 2;
		elif tipo_inspeccion.lower() == 'luces':
			id_tipo_inspeccion = 3
		
		if id_tipo_inspeccion == 0:
			return {"success":False, "message":"tipo inspeccion no valido", "data": data}, 404


		id_estado = None	
		estado = data['estado_inspeccion']
		if estado.lower()=='aprobada':
			id_estado = 1
		elif estado.lower()=='rechazada':
			id_estado=0

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
					
					if vehiculoRevision.aprobado is None:
						# -----------------------------------------------------------
						# Buscamos si la inspeccion que se quiere ingresar ya existe 
						# -----------------------------------------------------------
						buscarInspeccion = InspeccionModel.buscar_inspeccion(revisionId, personaId, id_tipo_inspeccion)
						if not buscarInspeccion:
							newInspeccion = InspeccionModel(revisionId, id_tipo_inspeccion, personaId, id_estado, observaciones)
							newInspeccion.guardar()
							if newInspeccion:
								data['id_inspeccion'] = newInspeccion.id
								return {"success":True, "message":"Acción realizada con éxito", "new encargado": data}, 200
							
							return {"success":False, "message":"No se pudo registrar la inspeccion"}, 404								
						return {"success":False, "message":"Vehiculo patente "+patente+" ya posee inspeccion de "+tipo_inspeccion+" con estado: "+estado_inspecciones[buscarInspeccion.estado]}, 200								
					return {"success":False, "message":"Vehiculo patente "+patente+" ya posee revision con estado: "+estados_revision[vehiculoRevision.aprobado]}, 200						
				return {"success":False, "message":"Vehiculo no esta registrado para revision"}, 200	
			return {"success":False, "message":"Vehiculo no esta registrado"}, 200	
		
		except Exception as e:
			return {'success': False, 'message': str(e)}, 500