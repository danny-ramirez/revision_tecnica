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

class VehiculoModel(db.Model):
    __tablename__ = 'vehiculo'

    id = db.Column(db.Integer, primary_key=True, nullable=False, server_default=db.FetchedValue(), autoincrement=True)
    modelo = db.Column(db.String(200, 'latin1_spanish_ci'))
    marca = db.Column(db.String(200, 'latin1_spanish_ci'))
    patente = db.Column(db.String(10, 'latin1_spanish_ci'), nullable=False)
    ano = db.Column(db.Integer, nullable=True)
    personaId= db.Column(db.Integer, nullable=False)

    def __init__(self, modelo, marca, patente, ano, personaId):
        self.modelo = modelo
        self.marca = marca
        self.patente = patente
        self.ano = ano
        self.personaId = personaId
    
    def obtener_datos(self):
        return {'id': self.id, 'modelo': self.modelo, 'marca': self.marca,'patente': self.patente, 'ano':self.ano, 'personaId': self.personaId}

    @classmethod
    def buscar_por_persona_id(cls,personaId):
        return cls.query.filter_by(personaId=personaId).first()

    @classmethod
    def buscar_por_patente(cls,patente):
        return cls.query.filter_by(patente=patente).first()

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
