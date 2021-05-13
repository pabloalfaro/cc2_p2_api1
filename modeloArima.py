from statsmodels.tsa.arima_model import ARIMA
import pandas as pd
import pmdarima as pm
import pymongo
import pickle
from datetime import datetime, timedelta
from zipfile import ZipFile
import zipfile
import time

class Modelo:
	def __init__(self):
		client = pymongo.MongoClient("mongodb+srv://cc-user:P8jVmeMpzSLfYIvY@cluster0.pupdc.mongodb.net/ccairflow?retryWrites=true&w=majority")
		bbdd = client.ccairflow['sanfrancisco']

		bbdd = pd.DataFrame(list(bbdd.find()))
		bbdd = bbdd.dropna()

		mTemperatura = pm.auto_arima(
			bbdd['TEMP'].dropna(),
			start_p=1, start_q=1,
			test='adf',       # use adftest to find optimal 'd'
			max_p=3, max_q=3, # maximum p and q
			m=1,              # frequency of series
			d=None,           # let model determine 'd'
			seasonal=False,   # No Seasonality
			start_P=0,
			D=0,
			trace=True,
			error_action='ignore',
			suppress_warnings=True,
			stepwise=True)
		pickle.dump(mTemperatura, open("./mTemperatura.pic", "wb" ) )
        
		model_hum = pm.auto_arima(
			bbdd['HUM'].dropna(),
			start_p=1, start_q=1,
			test='adf',       # use adftest to find optimal 'd'
			max_p=3, max_q=3, # maximum p and q
			m=1,              # frequency of series
			d=None,           # let model determine 'd'
			seasonal=False,   # No Seasonality
			start_P=0,
			D=0,
			trace=True,
			error_action='ignore',
			suppress_warnings=True,
			stepwise=True)
		pickle.dump(mTemperatura, open("./mHumedad.pic","wb"))
        
	def comprimir(self):
		with ZipFile('./mTemperatura.pic.zip', 'w', zipfile.ZIP_DEFLATED) as zip:
			zip.write('./mTemperatura.pic')

		with ZipFile('./mHumedad.pic.zip', 'w', zipfile.ZIP_DEFLATED) as zip:
			zip.write('./mHumedad.pic')   


if __name__ == "__main__":
    m = Modelo()
    m.comprimir()
