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

class InspeccionModel(db.Model):
    __tablename__ = 'inspeccion'
    __table_args__ = {'schema': 'revision_tecnica'}
    
    id = db.Column(db.Integer, primary_key=True, nullable=False, server_default=db.FetchedValue(), autoincrement=True)
    revisionId = db.Column(db.Integer,nullable=False)
    tipoInspeccionId= db.Column(db.Integer, nullable=False)
    personaId= db.Column(db.Integer, nullable=False)
    estado = db.Column(db.Integer, nullable=True , server_default=db.FetchedValue())
    observaciones= db.Column(db.Text(collation='latin1_spanish_ci'), nullable=True)
    
    def __init__(self, revisionId, tipoInspeccionId, personaId, estado, observaciones):
        self.revisionId = revisionId
        self.tipoInpeccionId = tipoInspeccionId
        self.personaId = personaId
        self.estado = estado
        self.observaciones = observaciones
        
    
    def obtener_datos(self):
        return {'revisionId': self.revisionId, 'tipoInspeccionId': self.tipoInspeccionId, 'personaId': self.personaId, 'estado': self.estado, 'observaciones':self.observaciones}

    @classmethod
    def buscar_por_id(cls,_id):
        return cls.query.filter_by(id=_id).first()

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
