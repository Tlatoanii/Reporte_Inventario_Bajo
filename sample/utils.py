import calendar
from datetime import datetime, timedelta

def get_past_month():
    now = datetime.now()
    first_day_of_current_month = datetime(now.year, now.month, 1)
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
    month_previous = last_day_of_previous_month.month
    year = last_day_of_previous_month.year
    days_in_previous_month = calendar.monthrange(year, month_previous)[1]
    days = [{"first_date": datetime(year, month_previous, day).strftime('%Y-%m-%d') + " 00:00:00",
            "last_date": datetime(year, month_previous, day).strftime('%Y-%m-%d') + " 23:59:59"} for day in range(1, days_in_previous_month + 1)]
    return days

def get_previous_month_name():
    months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    now = datetime.now()
    previous_month_index = (now.month - 2) % 12  # Restamos 2 porque los índices empiezan en 0
    return months[previous_month_index]

def get_difference_times(date_str_1, date_str_2):
    date1 = datetime.strptime(date_str_1, "%Y-%m-%d %H:%M:%S")
    date2 = datetime.strptime(date_str_2, "%Y-%m-%d %H:%M:%S")
    
    difference = date2 - date1
    
    hours, reminder = divmod(difference.seconds, 3600)
    minutes, seconds = divmod(reminder, 60)
    
    result = f'{hours}:{minutes} h'# :{seconds}'
    return result

def get_difference_days(date_str_1, date_str_2):
    date1 = datetime.strptime(date_str_1, "%Y-%m-%d %H:%M:%S")
    date2 = datetime.strptime(date_str_2, "%Y-%m-%d %H:%M:%S")
    
    difference = date2 - date1
    
    days = difference.days
    hours, reminder = divmod(difference.seconds, 3600)
    minutes, seconds = divmod(reminder, 60)
    if seconds >= 45: minutes += 1
    if minutes >= 45: hours += 1
    if hours >= 12: days += 1
    
    # result = f'{hours}:{minutes} h'# :{seconds}'
    return days

def add_stadistics_array(list_station, stations):
    # [{'station': 'CAMINO REAL', 'initial_time': '2025-02-28 09:15:01', 'final_time': '2025-02-28 18:45:01', 'initial_per': '37.54', 'min_per': 21.1, 'initial_vol': '15714.62', 'min_vol': '8832.67', 'tank_capacity': '41861.0', 'time_low': '9:30:0'}, 
    # {'station': 'GRIÑON', 'initial_time': '2025-02-28 17:15:01', 'final_time': '2025-02-28 18:45:01', 'initial_per': '31.31', 'min_per': 29.43, 'initial_vol': '18786.0', 'min_vol': '17658.0', 'tank_capacity': '60000.0', 'time_low': '1:30:0'}]
    # { station: "Camino Real", times_appeared: 15, times_low: [4.5, 5.3, ..., 6.2] }
    for station in stations:
        band = False
        name_station = station['station']
        if station['initial_per'] == 0.0:
            band = True
            continue
        if station['min_per'] == 0.0:
            band = True
            continue
        for index, item in enumerate(list_station):
            if item["station"] == name_station:
                band = True
                list_station[index]['times_appeared'] += 1
                list_station[index]['times_low'].append(station['time_low'])
                list_station[index]['difference_days'].append(get_difference_days(str(list_station[index]['dates'][-1]), str(station['initial_time'])))
                list_station[index]['dates'].append(station['initial_time'])
        
        if band == False:
                list_station.append({"station": name_station, "times_appeared": 1, "times_low": [station['time_low']], "dates": [station['initial_time']], "difference_days": []})
    return list_station

def add_stadistics_bad_lecture_array(list_bad_lecture, list_stations):
    for station in list_stations:
        band = False
        name_station = station['station']
        
        for index, item in enumerate(list_bad_lecture):
            if item["station"] == name_station and (station['initial_per'] == 0.0 or station['min_per'] == 0.0):
                band = True
                list_bad_lecture[index]['times_appeared'] += 1
                list_bad_lecture[index]['times_low'].append(station['time_low'])
                list_bad_lecture[index]['difference_days'].append(get_difference_days(str(list_bad_lecture[index]['dates'][-1]), str(station['initial_time'])))
                list_bad_lecture[index]['dates'].append(station['initial_time'])
        
        if band == False and (station['initial_per'] == 0.0 or station['min_per'] == 0.0):
                list_bad_lecture.append({"station": name_station, "times_appeared": 1, "times_low": [station['time_low']], "dates": [station['initial_time']], "difference_days": []})
    return list_bad_lecture

def get_oil_capacity(list_station, station): 
    for index, item in enumerate(list_station):
        if item["station"] == station:
            return round(list_station[index]["capacity"])

def get_oil_limit_percentage(list_station, station): 
    for index, item in enumerate(list_station):
        if item["station"] == station:
            return round(list_station[index]["percentage"])

def get_oil_volume(list_station, station, per):
    for index, item in enumerate(list_station):
        if item["station"] == station:
            return round((per * (list_station[index]["capacity"])) / 100)

def replace_data(oil_list, new_time, station, percentage, per_limits):
    band = False
    per = round(float(percentage))
    if station == 'GRINON':
        station = 'GRIÑON'
    for index, item in enumerate(oil_list):
        if item["station"] == station:
            band = True
            #* NUEVO DATO
            initial_date = str(oil_list[index]['initial_time'])
            initial_per = str(oil_list[index]['initial_per'])
            initial_vol = str(oil_list[index]['initial_vol'])
            tank_capacity = str(oil_list[index]['tank_capacity'])
            per_capacity = str(oil_list[index]['per_limit'])
            if percentage > 0.0:
                oil_list[index] = { "station": station, "initial_time": initial_date, "final_time": str(new_time), "initial_per": initial_per, "min_per": per, "initial_vol": initial_vol, "min_vol": str(get_oil_volume(per_limits, station, percentage)), "tank_capacity": tank_capacity, "per_limit": per_capacity,  "time_low": str(get_difference_times(initial_date, str(new_time))), "note": get_observation(str(new_time).split(' ')[1]) }
            else:
                oil_list[index] = { "station": station, "initial_time": initial_date, "final_time": str(new_time), "initial_per": initial_per, "min_per": per, "initial_vol": initial_vol, "min_vol": str(get_oil_volume(per_limits, station, percentage)), "tank_capacity": tank_capacity, "per_limit": per_capacity, "time_low": str(get_difference_times(initial_date, str(new_time))), "note": "Mala captura"}
    if band == False:
        if percentage > 0.0:
            oil_list.append({ "station": station, "initial_time": str(new_time), "final_time": str(new_time), "initial_per": percentage, "min_per": per, "initial_vol": str(get_oil_volume(per_limits, station, percentage)), "min_vol": str(get_oil_volume(per_limits, station, percentage)), "tank_capacity": str(get_oil_capacity(per_limits, station)), "per_limit": str(get_oil_limit_percentage(per_limits, station)), "time_low": "", "note": get_observation(str(new_time).split(' ')[1]) })
        else:
            oil_list.append({ "station": station, "initial_time": str(new_time), "final_time": str(new_time), "initial_per": percentage, "min_per": per, "initial_vol": str(get_oil_volume(per_limits, station, percentage)), "min_vol": str(get_oil_volume(per_limits, station, percentage)), "tank_capacity": str(get_oil_capacity(per_limits, station)), "per_limit": str(get_oil_limit_percentage(per_limits, station)), "time_low": "", "note": "Mala captura" })
    # print(oil_list)
    return oil_list

def get_observation(date: str):
    time = date.split(':')
    hours = time[0]
    minutes = time[1]
    
    if hours == "18" and minutes == "45":
        return "Solventado > 19 hrs"
    else: 
        return "Descarga Efectuada"
if __name__ == "__main__":
    # get_difference_times('2025-02-18 09:45:02', '2025-02-18 10:15:01')
    pass

def fil_data_per_station(list_station, list_product, stations_store):
    for list in list_product:
        list_station[stations_store.index(list['station'])].append(list)    
    return list_station 