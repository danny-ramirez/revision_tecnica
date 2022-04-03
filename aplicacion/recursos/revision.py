#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse
from flask import request, send_file
from datetime import datetime
from aplicacion.modelos.revision import RevisionModel
from aplicacion.modelos.vehiculo import VehiculoModel
from aplicacion.modelos.persona import PersonaModel
from aplicacion.helpers.utilidades import Utilidades


class IngresarVehiculoRevision(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('identificacion',type=str,required=True,help="Debe ingresar identificacion dueño vehiculo")
	parser.add_argument('nombre',type=str,required=True,help="Debe ingresar nombre  dueño vehiculo")
	parser.add_argument('apellido',type=str,required=True,help="Debe ingresar apellido  dueño vehiculo")
	parser.add_argument('patente',type=str,required=True,help="Debe ingresar patente del vehiculo")
	parser.add_argument('modelo',type=str,required=True,help="Debe ingresar modelo del vehiculo")
	parser.add_argument('marca',type=str,required=True,help="Debe ingresar marca del vehiculo")
	parser.add_argument('ano',type=str,required=True,help="Debe ingresar año del vehiculo")
	parser.add_argument('identificacion_encargado',type=str,required=True,help="Debe ingresar identificacion encargado revision")
	
	def post(self):
		data = IngresarVehiculoRevision.parser.parse_args()
		identificacion_dueno = data['identificacion']
		nombre = data['nombre']
		apellido = data['apellido']
		patente = data['patente']
		modelo = data['modelo']
		marca = data['marca']
		ano_vehiculo = data['ano']
		encargado = data['identificacion_encargado']
		try:
			# ----------------------------------------------------------------------
			# Buscamos que el encargado exista
			# ----------------------------------------------------------------------
			existeEncargado = PersonaModel.buscar_por_encargado(encargado)
			if existeEncargado:
				personaId_encargado = existeEncargado.id
				# ----------------------------------------------------------------------
				# buscamos al vehiculo
				# ----------------------------------------------------------------------	
				existeVehiculo = VehiculoModel.buscar_por_patente(patente)
				if existeVehiculo:
					return {"success":False, "message":"Vehiculo ya se encuentra en revision "}, 200
				else :	
					# ---------------------------------------------------------------------
					# Insertamos/buscamos al dueño de vehiculo
					# ---------------------------------------------------------------------
					existeDueno = PersonaModel.buscar_por_propietario(identificacion_dueno)
					if not existeDueno:
						tipo_persona = "Dueño"
						newPropietario = PersonaModel(identificacion_dueno, nombre, apellido, tipo_persona)
						newPropietario.guardar()
						idPropietario = newPropietario.id
					else:
						idPropietario = existeDueno.id	
					# ----------------------------------------------------------------------
					# Insertamos al vehiculo
					# ----------------------------------------------------------------------	
					newVehiculo = VehiculoModel(modelo, marca, patente, ano_vehiculo, idPropietario)
					newVehiculo.guardar()
					if newVehiculo:
						vehiculoId = newVehiculo.id
						# ----------------------------------------------------------------------
						# Insertamos el vehiculo a la revision
						# ----------------------------------------------------------------------	
						newRevision = RevisionModel(vehiculoId, personaId_encargado, None, None, None)
						newRevision.guardar()
						if newRevision:
							data['id_revision']=newRevision.id
							return {"success":True, "message":"Acción realizada con éxito", "data":data}, 200
						return {"success":False, "message":"No se pudo registrar la revision"}, 200	
					return {"success":False, "message":"Ha ocurrido un error no se pudo registrar el vehiculo"}, 404	
				return {"success":False, "message":"Encargado no esta registrado en el sistema"}, 200		
		except Exception as e:
			return {'success': False, 'message': str(e)}, 500