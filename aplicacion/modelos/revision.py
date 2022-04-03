#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aplicacion.db import db
from sqlalchemy import Table, Column, Integer, ForeignKey, or_, and_
from sqlalchemy.orm import relationship
from aplicacion.helpers.utilidades import Utilidades
from sqlalchemy.sql import expression
from datetime import datetime
import json, os, sys
import requests
from aplicacion.app import app_config
import math

class RevisionModel(db.Model):
    __tablename__ = 'revision'
    __table_args__ = {'schema': 'revision_tecnica'}
  
    id = db.Column(db.Integer, primary_key=True, nullable=False, server_default=db.FetchedValue(), autoincrement=True)
    vehiculoId = db.Column(db.Integer, nullable=False)
    personaId= db.Column(db.Integer, nullable=False)
    aprobado = db.Column(db.Integer,nullable=True , server_default=db.FetchedValue())
    observaciones= db.Column(db.Text(collation='latin1_spanish_ci'), nullable=True)
    fecha_revision = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    def __init__(self, vehiculoId, personaId, aprobado, observaciones, fecha_revision):
        self.vehiculoId = vehiculoId
        self.personaId = personaId
        self.aprobado = aprobado
        self.observaciones = observaciones
        self.fecha_revision = fecha_revision
        
    
    def obtener_datos(self):
        fecha_revision = None
        if self.fecha_revision != None:
            fecha_revision = Utilidades.formatoFechaHora(self.fecha_revision)
        return {'vehiculoId': self.vehiculoId, 'personaId': self.personaId, 'aprobado': self.aprobado, 'observaciones':self.observaciones, 'fecha_revision': fecha_revision}

    @classmethod
    def buscar_por_vehiculo(cls,vehiculoId):
        return cls.query.filter_by(vehiculoId=vehiculoId).first()

    @classmethod
    def buscar_por_encargado(cls,personaId):
        return cls.query.filter_by(personaId=personaId).all()

    @classmethod
    def buscar_por_propietario_vehiculo(cls,personaId, vehiculoId):
        return cls.query.filter_by(personaId=personaId).filter_by(vehiculoId=vehiculoId).first()        

    @classmethod
    def buscar_por_fecha_revision(cls,fecha_revision):
        return cls.query.filter_by(fecha_revision=fecha_revision).all()        


    @classmethod
    def buscar_por_id(cls,_id):
        return cls.query.filter_by(id=_id).first()

    def guardar(self):
        db.session.add(self)
        db.session.commit()
        
    def add(self):
        db.session.add(self)
        db.session.flush()

    def eliminar(self):
        db.session.delete(self)
        db.session.commit()
