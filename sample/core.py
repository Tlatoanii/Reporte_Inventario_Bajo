import argparse
import configparser
import json
from utils import get_past_month, replace_data, add_stadistics_array, add_stadistics_bad_lecture_array, get_previous_month_name
from util_report import resume_table, add_title_on_new_page, list_bad_lecture, stations_resume
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
    days_in_month = get_past_month()
    for day in days_in_month:
        data.append({ "day": day["first_date"], "day_data": models.get_info_store(config[f'{s_group}']["HOST"], config[f'{s_group}']["USER"], config[f'{s_group}']["PASS"], config[f'{s_group}']["DB"], day["first_date"], day["last_date"])})
    add_title_on_new_page(report, "Desglose de Alertas - Estaciones por día")
    for info in data:
        #* INFORMACIÓN DEL DÍA: info['day'] (Día tras día)
        for day in info["day_data"]:
            # print(day[0])
            station = json.loads(day[1])
            for product in station:
                for inventory in product:
                    type_product = models.get_type_oil(inventory['name'])
                    if type_product == "REGULAR":
                        replace_data(regular, day[0], inventory['station'], inventory['percentage'], models.stations_limits_regular)
                    elif type_product == "PREMIUM":
                        replace_data(premium, day[0], inventory['station'], inventory['percentage'], models.stations_limits_premium)
                    elif type_product == "DIESEL":
                        replace_data(disel, day[0], inventory['station'], inventory['percentage'], models.stations_limits_diesel)
                    continue
                
        resume_table(report, regular, premium, disel, info['day'])
        # print(f'RESUMEN REGULAR DIA {info['day']}: {regular}')
        # print(f'RESUMEN PREMIUM DIA {info['day']}: {premium}')
        # print(f'RESUMEN DIESEL DIA {info['day']}: {disel}')
        regular_global = add_stadistics_array(regular_global, regular) 
        premium_global = add_stadistics_array(premium_global, premium)
        diesel_global = add_stadistics_array(diesel_global, disel)
        bad_lecture = add_stadistics_bad_lecture_array(bad_lecture, regular)
        regular.clear()
        premium.clear()
        disel.clear()
    stadistics_graph(diesel_global, "Diesel", get_previous_month_name(), "gold",report)
    stadistics_graph(premium_global, "Premium", get_previous_month_name(), "crimson", report)
    stadistics_graph(regular_global, "Regular", get_previous_month_name(), "darkgreen", report)
    # print(f'RESUME REGULAR: {regular_global}')
    # print(f'RESUME PREMIUM: {premium_global}')
    # print(f'RESUME DIESEL: {diesel_global}')
    #print(bad_lecture)
    add_title_on_new_page(report, "Resúmen")
    list_bad_lecture(bad_lecture, report)
    stations_resume(report, regular_global, premium_global, diesel_global)
    report.createReport()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Grupos Disponibles")
    parser.add_argument('-group', type=str, help="Grupos (oktan, pepe6, debug)")
    argparse = parser.parse_args()
    main(argparse.group)