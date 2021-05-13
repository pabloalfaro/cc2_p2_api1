from flask import Flask, Response, jsonify
import json
import pickle
import pandas as pd
import pmdarima as pm
import os
from statsmodels.tsa.arima_model import ARIMA
import time
from datetime import datetime, timedelta
from zipfile import ZipFile

import modeloArima

app = Flask(__name__)

def predecir_tiempo(intervalo):
	with ZipFile('./mTemperatura.pic.zip', 'r') as myzip:
		myzip.extractall('./')

	with ZipFile('./mHumedad.pic.zip', 'r') as myzip:
		myzip.extractall('./')

	mod_temperatura = pickle.load( open( './mTemperatura.pic', "rb" ) )
	pred_temperatura, _ = mod_temperatura.predict(n_periods=intervalo, return_conf_int=True)

	mod_humedad = pickle.load( open( './mHumedad.pic', "rb" ) )
	pred_humedad, _ = mod_humedad.predict(n_periods=intervalo, return_conf_int=True)
	
	fecha_hoy = datetime.now() + timedelta(hours=3)
	fecha_intervalo = pd.date_range(fecha_hoy.replace(second=0, microsecond=0), periods=intervalo, freq='H')
	pred= []

	for fecha, temperatura, humedad in zip(fecha_intervalo, pred_temperatura, pred_humedad):
		dt = time.mktime(fecha.timetuple())
		pred.append({'hour': datetime.utcfromtimestamp(dt).strftime('%d-%m %H:%M'),
		'temp': temperatura, 
		'hum': humedad})
		
	return pred


@app.route("/servicio/v1/prediccion/24horas",methods=['GET'])
def hours_24():
    response = Response(json.dumps(predecir_tiempo(24)), status=200)
    response.headers['Content-Type']='application/json'
    return response

@app.route("/servicio/v1/prediccion/48horas",methods=['GET'])
def hours_48():
    response = Response(json.dumps(predecir_tiempo(48)), status=200)
    response.headers['Content-Type']='application/json'
    return response

@app.route("/servicio/v1/prediccion/72horas",methods=['GET'])
def hours_72():
    response = Response(json.dumps(predecir_tiempo(72)), status=200)
    response.headers['Content-Type']='application/json'
    return response

