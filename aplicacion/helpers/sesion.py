#!/usr/bin/env python
# -*- coding: utf-8 -*-
from aplicacion.db import db
from sqlalchemy import text
import random
import hashlib
from datetime import datetime
from aplicacion.redis import redis


class Sesion():

    @staticmethod
    def generar_tokenid(username, password):
        try:
            fecha_actual = datetime.now()
            base = username+password+str(fecha_actual.minute)+str(fecha_actual.second)
            token_id = hashlib.md5(base.encode()).hexdigest()
            data = {"username":username}
            redis.setex(token_id, 10000, data)
            datos = redis.get(token_id)
            return token_id
        except Exception as e:
            return None


    @staticmethod
    def eliminar_tokenid(token_id):
        try:
            redis.delete(dato)
            return True
        except Exception as e:
            return None

    @staticmethod
    def validar_token(token_id):
        existe = redis.exists(token_id)
        return existe
