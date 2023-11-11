import flask
import json
import sql_service_report_dc
from flask import Flask, request, render_template, send_from_directory
import excel_service_report_dc



app = Flask(__name__)

@app.route('/report_dc/<params>', methods=['GET'])
def get_report_dc(params):
    p = params.split(',')
    station_name = p[0]
    type_traffic = p[1]
    from_month_uto5 = p[2]
    to_month_uto5 = p[3]
    from_date = p[4]
    to_date = p[5]
    uto_5 = sql_service_report_dc.uto_5_sql(station_name, type_traffic, from_month_uto5, to_month_uto5, from_date, to_date)
    return json.dumps(uto_5)


@app.route('/stations_list', methods = ['GET'])
def get_stations_list():
    stations = sql_service_report_dc.uto_5_stations_list()
    return json.dumps(stations)


@app.route('/update_report_reasons', methods = ['POST'])
def update_reason():
    reasons = request.get_json()
    sql_service_report_dc.update_reasons(reasons)
    return 'ok'


@app.route('/report')
def send_report():
    return send_from_directory('resource', 'index.html')


@app.route('/excel_report/<params>', methods=['GET'])
def excel_report_dc(params):
    p = params.split(',')
    station_name = p[0]
    type_traffic = p[1]
    from_month_uto5 = p[2]
    to_month_uto5 = p[3]
    from_date = p[4]
    to_date = p[5]
    excel_service_report_dc.uto_5_excel(station_name, type_traffic, from_month_uto5, to_month_uto5, from_date, to_date)
    return send_from_directory('file', 'import_excel_uto5.xlsx')


if __name__ == '__main__':
    app.run(port = 5300)

