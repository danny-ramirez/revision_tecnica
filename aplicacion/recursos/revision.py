#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse
from flask import request, send_file
from datetime import datetime
from aplicacion.modelos.revision import RevisionModel
from aplicacion.modelos.vehiculo import VehiculoModel
from aplicacion.modelos.persona import PersonaModel
from aplicacion.modelos.tipo_revision import TipoRevisionModel
from aplicacion.modelos.inspeccion import InspeccionModel

from aplicacion.helpers.utilidades import Utilidades

class UpdateEstadoRevision(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('revision_id',type=int,required=True,help="Debe ingresar id de revision")
	parser.add_argument('estado',type=str,required=True,help="Debe ingresar estado de la revision")
	
	def put(self):
		data = UpdateEstadoRevision.parser.parse_args()
		revision_id = data['revision_id']
		tipo_estado = data['estado']
		try:
			estado = None
			if tipo_estado.lower() == 'aprobada':
				estado = 1
			elif tipo_estado.lower() == 'rechazada':
				estado = 0
								
			dataJson = {'aprobado':estado}
			upRevision = RevisionModel.update_data(revision_id, dataJson)
			if upRevision:
				return {"success":True, "message":"Acción realizada con éxito", "data":data}, 200
			return {"success":False, "message":"Fallo la actualizacion", "data":data}, 200	
		except Exception as e:
			return {'success': False, 'message': str(e)}, 500


class RevisionesVehiculo(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('patente',type=str,required=True,help="Debe ingresar patente del vehiculo")
	
	def get(self):
		data = RevisionesVehiculo.parser.parse_args()
		patente = data['patente']
		try:
			dataTipoInspecciones = TipoRevisionModel.buscar_all()
			tipoInspeccion = {}
			for tipo in dataTipoInspecciones:
				tipoInspeccion[tipo.id] = tipo.nombre_tipo

			historial = {}
			vehiculoData = VehiculoModel.buscar_por_patente(patente)
			if vehiculoData :
				historial = {
					"Patente" : patente,
					"Marca" : vehiculoData.marca,
					"Modelo" : vehiculoData.modelo,
					"Año" : vehiculoData.ano,
					"Historial" : []
				}

				vehiculoAllRegistros = VehiculoModel.buscar_por_patente_all(patente)

				for vehiculo in vehiculoAllRegistros:
					registro = {}
					# ---------------------------------------------------------------------
					# Buscamos al propietario, para el registro 
					# ---------------------------------------------------------------------
					propietario = PersonaModel.buscar_por_id(vehiculo.personaId)
					registro_propietario = {
						"propietario" : propietario.nombre + " " + propietario.apellido,
						"identificacion" : propietario.identificacion,
						"revisiones" : []
					}
					# ---------------------------------------------------------------------
					# Buscamos las revisiones ordenadas por fecha descendiente
					# ---------------------------------------------------------------------
					revisionesRegistroVehiculoId = RevisionModel.lista_all_revisiones_vehiculo(vehiculo.id)
					
					for revision in revisionesRegistroVehiculoId:
						registro_revisiones = {}
						estado = None
						if revision.aprobado is not None:
							if revision.aprobado:
								estado = 'Aprobada'
							else :
								estado = 'Rechazada'
						fecha = revision.fecha_revision
						registro_revisiones = {
							"Fecha_revision": fecha.strftime("%d-%m-%Y"),
							"Estado" : estado,
							"Observacion" : revision.observaciones,
							"inspecciones" : []
						}
						# ---------------------------------------------------------------------
						# Buscamos las inspecciones asociadas al registro de la revision
						# ---------------------------------------------------------------------
						inspeccionesRevision = InspeccionModel.buscar_inspeccion_revision_all(revision.id)
						for inspecciones in inspeccionesRevision:
							
							inspeccion = tipoInspeccion[inspecciones.tipoInspeccionId]
							name_estado = None
							if inspecciones.estado is not None:
								if inspecciones.estado:
									name_estado = 'Aprobada'
								else:
									name_estado = 'Rechazada'

							dataInspecciones = {
								"Inspeccion" : inspeccion,
								"Estado": name_estado,
								"Observaciones": inspecciones.observaciones
							}
							registro_revisiones['inspecciones'].append(dataInspecciones)

						registro_propietario["revisiones"].append(registro_revisiones)

					historial['Historial'].append(registro_propietario)

				return {"success":True, "data": historial}, 200	
			return {"success":False, "message":"Vehiculo no esta registrado"}, 200	 
		except Exception as e:
			return {'success': False, 'message': str(e)}, 500


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
						newPropietario = PersonaModel(identificacion_dueno, nombre, apellido)
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