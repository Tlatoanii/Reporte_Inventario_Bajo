import mysql.connector
from logger import Logger

class Connection:
    stations_store = []
    dic_limit_regular = []
    dic_limit_premium = []
    dic_limit_diesel = []
    stations_limits_regular = []
    stations_limits_premium = []
    stations_limits_diesel = []
    def __init__(self, host, user, password, database):
        try:
            log = Logger("log/pfd.log")
            self.cnx = mysql.connector.connect(host= host, port= 3306, user= user, password= password, database= database)
            log.logInfo("[models.py] - Obteniendo datos de estacion por producto")
            self.cur = self.cnx.cursor()
            query = 'SELECT DISTINCT e.nombre_corto, tp.producto, tp.porcentaje, t.capacidad_operativa FROM tanque_porcentaje tp INNER JOIN estacion e ON tp.id_dbm = e.id_dbm INNER JOIN tanques t ON tp.id_dbm = t.id_dbm WHERE tp.id_producto = t.id_producto ORDER BY e.id_dbm;'
            self.cur.execute(query)
            self.assign_arrays_products(self.cur.fetchall())
            self.__getStations(host, user, password, database)
            self.cnx.close()
        except Exception as e:
            log.logError(f'[models.py] - Error al obtener datos de la capacidad por estación de la base de datos: {e}')
            return None
        
    def assign_arrays_products(self, result):
        for station in result:
            dic = { "station": station[0], "percentage": station[2], "capacity": station[3] }
            product = self.get_type_oil(str(station[1]))
            if product == 'REGULAR':
                self.stations_limits_regular.append(dic)
                self.dic_limit_regular.append( str(station[0]) )
            elif product == 'PREMIUM':
                self.stations_limits_premium.append(dic)
                self.dic_limit_premium.append( str(station[0]) )
            elif product == "DIESEL":
                self.stations_limits_diesel.append(dic)
                self.dic_limit_diesel.append( str(station[0]) )
    
    def get_type_oil(self, oil_type):
        array_magna = ['MAGNA', 'REGULAR', 'MAXIMA', 'GASOLINA MAGNA', 'PEMEX MAGNA']
        array_premium = ['PREMIUM', 'SUPREMA', 'GASOLINA PREMIUM', 'PEMEX PREMIUM']
        array_diesel = ['DIESEL', 'PLUS', 'DIESEL PLUS', 'PEMEX DIESEL']
        if oil_type.upper() in array_magna:    return "REGULAR" 
        if oil_type.upper() in array_premium:  return "PREMIUM"
        if oil_type.upper() in array_diesel:   return "DIESEL"
        return "default"
    
    def get_info_store(self, host, user, password, database, first_date, last_date):
        try:
            log = Logger("log/pfd.log")
            self.cnx = mysql.connector.connect( host= host, port= 3306, user= user, password= password, database= database )
            self.cur = self.cnx.cursor()
            query = f'SELECT ln2.fecha, ln2.texto, ln2.texto_corto FROM log_notificaciones ln2 WHERE ln2.fecha BETWEEN "{first_date}" AND "{last_date}" AND ln2.tipo = 1;'
            self.cur.execute(query)
            result =  self.cur.fetchall()
            self.cnx.close()
            return result
        except Exception as e:
            log.logError(f'[models.py] - Error al conectar la base de datos: {e}')
            return None
    
    def __getStations(self, host, user, password, database):
        try:
            log = Logger("log/pfd.log")
            self.cnx = mysql.connector.connect( host= host, port= 3306, user= user, password= password, database= database )
            self.cur = self.cnx.cursor()
            query = f'SELECT e.nombre_corto FROM estacion e;'
            self.cur.execute(query)
            result =  self.cur.fetchall()
            for station in result:
                self.stations_store.append(station[0])
            # print(self.stations_store)
            self.cnx.close()
            return result
        except Exception as e:
            log.logError(f'[models.py] - Error al conectar la base de datos y obtener estaciones: {e}')
            return None
        
        
if __name__ == "__main__":
    pass        