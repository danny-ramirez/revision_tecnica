import datetime

class Utilidades():

    @staticmethod
    def mayusculas(texto):
        try:
            return str(texto).upper()
        except Exception as e:
            return texto

    @staticmethod
    def formatoFecha(fecha):
    	dia = str(fecha.day)
    	dia = "0"+dia if len(dia) == 1 else dia
    	mes = str(fecha.month)
    	mes = "0"+mes if len(mes) == 1 else mes
    	anio = str(fecha.year)

    	fechaFormateada =  dia + "-" + mes + "-" + anio
    	return fechaFormateada

    """
        Valida fecha en formato dd-mm-YYYY
    """
    @staticmethod
    def validarDate(date_text, formato):
        try:
            if str(date_text) != datetime.datetime.strptime(str(date_text), formato).strftime(formato):
                raise ValueError
            return True
        except ValueError:
            return False
 
