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

class PersonaModel(db.Model):
    __tablename__ = 'persona'
    __table_args__ = {'schema': 'revision_tecnica'}
    
    id = db.Column(db.Integer, primary_key=True, nullable=False, server_default=db.FetchedValue(), autoincrement=True)
    identificacion = db.Column(db.String(20, 'latin1_spanish_ci'))
    nombre = db.Column(db.String(200, 'latin1_spanish_ci'))
    apellido = db.Column(db.String(200, 'latin1_spanish_ci'))
    
    def __init__(self, identificacion, nombre, apellido):
        self.identificacion = identificacion
        self.nombre = nombre
        self.apellido = apellido
            
    def obtener_datos(self):
        return {'id': self.id, 'identificacion': self.identificacion, 'nombre': self.nombre,'apellido': self.apellido}

    @classmethod
    def buscar_por_identificacion(cls,identificacion):
        return cls.query.filter_by(identificacion=identificacion).first()

    @classmethod
    def buscar_por_propietario(cls,identificacion):
        return cls.query.filter_by(identificacion=identificacion).filter_by(tipo_persona="Dueño").first()

    @classmethod
    def buscar_por_encargado(cls,identificacion):
        return cls.query.filter_by(identificacion=identificacion).filter_by(tipo_persona="Encargado").first()

    
    @classmethod
    def buscar_por_id(cls,_id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def listado_all(cls):
        return cls.query.all()    

    def guardar(self):
        db.session.add(self)
        db.session.commit()
        
    def add(self):
        db.session.add(self)
        db.session.flush()

    def eliminar(self):
        db.session.delete(self)
        db.session.commit()
