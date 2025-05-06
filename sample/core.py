import argparse
import configparser
import json
from utils import get_past_month, replace_data, add_stadistics_array, add_stadistics_bad_lecture_array, get_previous_month_name, fil_data_per_station
from util_report import resume_table, add_title_on_new_page, list_bad_lecture, stations_resume, station_resume_data
from models import Connection
from logger import Logger
from report import Reports
from utils_charts import stadistics_graph


def main(group):
    # ? VARIABLES GLOBALES
    report = Reports()
    data = []
    regular_global = []
    premium_global = []
    diesel_global = []
    regular = []
    premium = []
    disel = []
    bad_lecture = []
    log = Logger("log/pfd.log")
    if group == None:
        log.logWarning("[core.py] - Ingresa un grupo (oktan, pepe6, bapje, debug)")    
        return 
    config = configparser.ConfigParser()
    config.read('docs/conn.ini')
    s_group = str(group).upper()
    models = Connection(config[f'{s_group}']["HOST"], config[f'{s_group}']["USER"], config[f'{s_group}']["PASS"], config[f'{s_group}']["DB"])
    regular_stations = [ [] for _ in range(len(models.stations_store)) ]
    premium_stations = [ [] for _ in range(len(models.stations_store)) ]
    diesel_stations =  [ [] for _ in range(len(models.stations_store)) ]
    days_in_month = get_past_month()
    for day in days_in_month:
        data.append({ "day": day["first_date"], "day_data": models.get_info_store(config[f'{s_group}']["HOST"], config[f'{s_group}']["USER"], config[f'{s_group}']["PASS"], config[f'{s_group}']["DB"], day["first_date"], day["last_date"])})
    for info in data:
        #* INFORMACIÓN DEL DÍA: info['day'] (Día tras día)
        for day in info["day_data"]:
            # print(day[0])
            station = json.loads(day[1])
            for product in station:
                for inventory in product:# {'station': 'SAN ISIDRO', 'name': 'REGULAR', 'percentage': 26.46}
                    type_product = models.get_type_oil(inventory['name'])
                    if type_product == "REGULAR":
                        replace_data(regular, day[0], inventory['station'], inventory['percentage'], models.stations_limits_regular)
                    elif type_product == "PREMIUM":
                        replace_data(premium, day[0], inventory['station'], inventory['percentage'], models.stations_limits_premium)
                    elif type_product == "DIESEL":
                        replace_data(disel, day[0], inventory['station'], inventory['percentage'], models.stations_limits_diesel)
                    continue
        resume_table(report, regular, premium, disel, info['day'])
        fil_data_per_station(regular_stations, regular, models.stations_store)
        fil_data_per_station(premium_stations, premium, models.stations_store)
        fil_data_per_station(diesel_stations, disel, models.stations_store)
        add_stadistics_array(regular_global, regular)
        add_stadistics_array(premium_global, premium)
        add_stadistics_array(diesel_global, disel)
        add_stadistics_bad_lecture_array(bad_lecture, regular)
        regular.clear()
        premium.clear()
        disel.clear()
    # print(json.dumps(regular_stations))
    # print(regular_stations)
    # print(premium_stations)
    # print(diesel_stations)
    stadistics_graph(regular_global, "Regular", get_previous_month_name(), "darkgreen", report)
    stadistics_graph(premium_global, "Premium", get_previous_month_name(), "crimson", report)
    stadistics_graph(diesel_global, "Diesel", get_previous_month_name(), "gold",report)
    station_resume_data(models.stations_store, regular_stations, premium_stations, diesel_stations, report)
    # print(json.dumps(regular_global))
    # print(f'RESUME REGULAR: {regular_global}')
    # print(f'RESUME PREMIUM: {premium_global}')
    # print(f'RESUME DIESEL: {diesel_global}')
    report.createReport()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Grupos Disponibles")
    parser.add_argument('-group', type=str, help="Grupos (oktan, pepe6, debug)")
    argparse = parser.parse_args()
    main(argparse.group)