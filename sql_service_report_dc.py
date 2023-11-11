import psycopg2
from datetime import datetime

# open to github

def uto_5_sql(station_name, type_traffic, from_month, to_month, to_date, from_date):
    conn = psycopg2.connect(dbname = 'postgres', user = 'postgres', password = 'b335a2', host = 'localhost')
    curs = conn.cursor()
    
    from_month = from_month.replace('-', '')
    to_month = to_month.replace('-', '')
    
    print(from_month, to_month)
    type_traffic_where = "AND uto_5.type_traffic_rout = '" + type_traffic + "' " if type_traffic != 'Все' else ''
    to_month_uto5_where = "AND uto_5.month_uto5 <= '" + to_month +"' " if to_month != '' else ''
    from_month_uto5_where = "AND uto_5.month_uto5 >= '" + from_month + "' " if from_month != '' else ''
    
    to_date_uto5_where = "AND uto_5.time_start_station >= '" + to_date + " 00:00:00' " if to_date != '' else ''
    from_date_uto5_where = "AND uto_5.time_start_station <= '" + from_date + " 23:59:59' " if from_date != '' else ''
    
    select_uto5 = (("SELECT uto_5.uid, uto_5.start_station_name, uto_5.type_traffic_rout, uto_5.numb_driver, "
                    "depot.title, driver_boys.fio, locomotive.locomotive_serial, driver_rout.locomotive_number, "
                    "uto_5.turnout_time, uto_5.accept_tps_time, uto_5.time_start_station, uto_5.train_number, "
                    "uto_5.service, uto_5.reason, uto_5.reason_comments, "
                    "uto_5.time_start_station - uto_5.turnout_time - '2:00:00' as tps_time FROM public.uto_5 "
                    "JOIN driver_rout ON driver_rout.uid = uto_5.uid_driver_rout JOIN driver_boys "
                    "ON driver_rout.uid_driver = driver_boys.uid JOIN locomotive ON "
                    "locomotive.locomotive_numb = driver_rout.locomotive_serial JOIN depot "
                    "ON depot.numb = driver_rout.depot_numb WHERE uto_5.subgroup_offence = 'Всего' "
                    "AND uto_5.start_station_name = '") + station_name + "'" + type_traffic_where +
                    to_date_uto5_where + from_date_uto5_where +
                    to_month_uto5_where + from_month_uto5_where + " ORDER BY uto_5.turnout_time ASC")
    print(select_uto5)
    curs.execute(select_uto5)
    records = curs.fetchall()
    

    
    # добавляем все из sql в список
    select_uto_5 = []
    for i in records:
        select_uto_5.append(i)

    result = []
    
    for x in select_uto_5:
        record = {}
        record['uid'] = x[0]
        record['station'] = x[1]
        record['type_traffic'] = x[2]
        record['numb_driver'] = x[3]
        record['depot_title'] = x[4]
        record['fio'] = x[5]
        record['locomotive_serial'] = x[6]
        record['locomotive_number'] = x[7]
        record['turnout_time'] = x[8].strftime("%d.%m.%Y %H:%M")
        record['accept_tps_time'] = x[9].strftime("%d.%m.%Y %H:%M")
        record['time_start_station'] = x[10].strftime("%d.%m.%Y %H:%M")
        record['train_number'] = x[11]
        record['service'] = '' if x[12] == None else x[12]
        record['reason'] = '' if x[13] == None else x[13]
        record['reason_comments'] = '' if x[14] == None else x[14]
        record['tps_time'] = str(x[15])
        
        result.append(record)
    curs.close()
    conn.close()
    return result


def uto_5_stations_list():
    conn = psycopg2.connect(dbname = 'postgres', user = 'postgres', password = 'b335a2', host = 'localhost')
    curs = conn.cursor()
    
    # извлекаем из SQL данные и выводим в массив long_routs
    curs.execute("SELECT DISTINCT start_station_name FROM uto_5 "
                 "ORDER BY start_station_name ASC ")
    
    records = curs.fetchall()
    
    # добавляем все из sql в список
    stations = []
    for i in records:
        stations.append(i[0])
    curs.close()
    conn.close()
    return stations


def update_reasons(reasons):
    conn = psycopg2.connect(dbname = 'postgres', user = 'postgres', password = 'b335a2', host = 'localhost')
    curs = conn.cursor()
    for i in reasons:
        reasons_sql = (f"UPDATE uto_5 SET service = '{i['service']}', "
                       f"reason = '{i['reason']}', "
                       f"reason_comments = '{i['reason_comments']}' "
                       f"WHERE uto_5.uid = '{i['uid']}'")
        curs.execute(reasons_sql)
        conn.commit()
    curs.close()
    conn.close()
    return 'ok'
