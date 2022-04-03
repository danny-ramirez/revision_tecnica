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

class TipoRevisionModel(db.Model):
    __tablename__ = 'tipo_revision'
    #__table_args__ = {'schema': 'revision_tecnica'}
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_tipo = db.Column(db.String(100, 'latin1_spanish_ci'))
    
    def __init__(self, nombre_revision):
        self.nombre_tipo = nombre_tipo
    
    def obtener_datos(self):
        return {'id':self.id, 'nombre_tipo': self.nombre_tipo}

    @classmethod
    def buscar_por_id(cls,_id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def buscar_all(cls):
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
