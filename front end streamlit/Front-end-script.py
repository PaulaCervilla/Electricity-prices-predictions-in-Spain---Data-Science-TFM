import streamlit as st
import pandas as pd
import numpy as np
pd.options.display.max_columns = None
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn.metrics import mean_squared_error
from math import sqrt
import datetime
import re
import base64


st.markdown(
    """
    <style>
    .reportview-container {
        background: url("https://raw.githubusercontent.com/PaulaCervilla/Electricity-prices-predictions-in-Spain---Data-Science-TFM/main/front%20end%20streamlit/electricity3.jpeg");
	background-size: cover
    }

    </style>
    """,
    unsafe_allow_html=True
)


#st.set_page_config(layout="wide")

st.title("Electricity Price Predictions In Spain. Data Science Master's Dissertation By Paula Cervilla García")

st.write("The aim of this project was to predict the overall daily electricity price in Spain, after deeply studying and understanding all the relevant variables that make up the mentioned price.")


path = "https://raw.githubusercontent.com/PaulaCervilla/Electricity-prices-predictions-in-Spain---Data-Science-TFM/main/front%20end%20streamlit/electricity_brent_weather.csv"

electricity_brent_weather = pd.read_csv(path, header= 0, dtype = str, engine= "python", sep=";", error_bad_lines= False, encoding= "utf-8")

 
st.header('Electricity Prices, Brent Crude Oil Futures And Weather Variables')

st.write("Here you can explore the raw data used to forecast future electricity prices:")


#Changing all data types to numeric and the using the Date as the index


electricity_brent_weather["Date"] = pd.to_datetime(electricity_brent_weather['Date'], format= "%d/%m/%Y", errors = "ignore")
electricity_brent_weather.set_index("Date", inplace=True)
electricity_brent_weather["Date"] = electricity_brent_weather.index



electricity_brent_weather = electricity_brent_weather[['Date','Day','Energía final MWh', 'Mercado diario €/MWh','Mercado intradiario €/MWh', 
							'Restricciones €/MWh', 'Procesos OS €/MWh',
							'Garantía potencia Pagos capacidad €/MWh', 'Total €/MWh',
       							'Coste s.interrrumpibilidad', 'Precio cierre Brent',
       							'Precio apertura Brent', 'Precio Máximo Brent', 'Precio mínimo Brent',
       							'Tmax', 'Tmin', 'Tmed', 'Vmax', 'TPrec']]




electricity_brent_weather['Precio cierre Brent'] = electricity_brent_weather["Precio cierre Brent"].str.replace(",", ".")
electricity_brent_weather['Precio apertura Brent'] = electricity_brent_weather["Precio apertura Brent"].str.replace(",", ".")
electricity_brent_weather['Precio Máximo Brent'] = electricity_brent_weather["Precio Máximo Brent"].str.replace(",", ".")
electricity_brent_weather['Precio mínimo Brent'] = electricity_brent_weather["Precio mínimo Brent"].str.replace(",", ".")

electricity_brent_weather["Energía final MWh"] = pd.to_numeric(electricity_brent_weather["Energía final MWh"], downcast="float")
electricity_brent_weather["Mercado diario €/MWh"] = pd.to_numeric(electricity_brent_weather["Mercado diario €/MWh"], downcast="float")
electricity_brent_weather["Mercado intradiario €/MWh"] = pd.to_numeric(electricity_brent_weather["Mercado intradiario €/MWh"], downcast="float")
electricity_brent_weather["Restricciones €/MWh"] = pd.to_numeric(electricity_brent_weather["Restricciones €/MWh"], downcast="float")
electricity_brent_weather["Procesos OS €/MWh"] = pd.to_numeric(electricity_brent_weather["Procesos OS €/MWh"], downcast="float")
electricity_brent_weather["Garantía potencia Pagos capacidad €/MWh"] = pd.to_numeric(electricity_brent_weather["Garantía potencia Pagos capacidad €/MWh"], downcast="float")
electricity_brent_weather["Total €/MWh"] = pd.to_numeric(electricity_brent_weather["Total €/MWh"], downcast="float")
electricity_brent_weather["Coste s.interrrumpibilidad"] = pd.to_numeric(electricity_brent_weather["Coste s.interrrumpibilidad"], downcast="float")
electricity_brent_weather["Precio cierre Brent"] = pd.to_numeric(electricity_brent_weather["Precio cierre Brent"], downcast="float")
electricity_brent_weather["Precio apertura Brent"] = pd.to_numeric(electricity_brent_weather["Precio apertura Brent"], downcast="float")
electricity_brent_weather["Precio Máximo Brent"] = pd.to_numeric(electricity_brent_weather["Precio Máximo Brent"], downcast="float")
electricity_brent_weather["Precio mínimo Brent"] = pd.to_numeric(electricity_brent_weather["Precio mínimo Brent"], downcast="float")
electricity_brent_weather["Tmax"] = pd.to_numeric(electricity_brent_weather["Tmax"], downcast="float")
electricity_brent_weather["Tmin"] = pd.to_numeric(electricity_brent_weather["Tmin"], downcast="float")
electricity_brent_weather["Tmed"] = pd.to_numeric(electricity_brent_weather["Tmed"], downcast="float")
electricity_brent_weather["Vmax"] = pd.to_numeric(electricity_brent_weather["Vmax"], downcast="float")
electricity_brent_weather["TPrec"] = pd.to_numeric(electricity_brent_weather["TPrec"], downcast="float")


st.write(electricity_brent_weather)



#Adding a checkbox to be able to filter the dataframe

date_choice = st.selectbox('Select the date you wish to see data for:', electricity_brent_weather["Date"])

st.write(electricity_brent_weather.loc[(electricity_brent_weather["Date"] == date_choice)])


#Plotting different variables

st.write("Below there is a graph showing historical electricity prices since 2013:")

electricity_brent_weather.index = pd.DatetimeIndex(electricity_brent_weather.index, dayfirst= True)

st.subheader('Electricity Prices 2013-2021')

st.line_chart(electricity_brent_weather["Total €/MWh"])

#Models dataframe

models_dataset = electricity_brent_weather.drop(["Day", "Coste s.interrrumpibilidad", "Mercado diario €/MWh",
                                  "Mercado intradiario €/MWh", "Restricciones €/MWh",
                                  "Procesos OS €/MWh", "Garantía potencia Pagos capacidad €/MWh", 
                                  "Precio apertura Brent", "Precio Máximo Brent",
                                  "Precio mínimo Brent"], axis = 1)

#Showing some metrics

st.write("Here you can see the maximum price per year and the variation Year on Year:")


years = models_dataset.resample("Y").max()
years["diff_total€/MWh"] = years["Total €/MWh"].diff()
years["diff_total€/MWh%"] = years["Total €/MWh"].diff()/years["Total €/MWh"]*100

col1, col2, col3 = st.columns(3)
col1.metric("Max. Total €/MWh 2013 (May-Dec)", "103.2 €", delta_color="inverse")
col2.metric("Max. Total €/MWh 2014", "81.6 €", "-26.5%", delta_color="inverse")
col3.metric("Max. Total €/MWh 2015", "79.8 €", "-2.2%", delta_color="inverse")

col4, col5, col6 = st.columns(3)
col4.metric("Max. Total €/MWh 2016", "74.4 €", "-7.3%", delta_color="inverse")
col5.metric("Max. Total €/MWh 2017", "99.4 €", "25.2%", delta_color="inverse")
col6.metric("Max. Total €/MWh 2018", "81.2 €", "-22.4%", delta_color="inverse")

col7, col8, col9 = st.columns(3)
col7.metric("Max. Total €/MWh 2019", "74.4 €", "-9.12%", delta_color="inverse")
col8.metric("Max. Total €/MWh 2020", "62.7 €", "-18.7%", delta_color="inverse")
col9.metric("Max. Total €/MWh 2021 (Jan-Sep)", "196.18 €", "68.0%", delta_color="inverse")

st.caption("Please note that 2013 maximum price only takes into account May to December prices. For 2021, the 196.18€ was the maximum price up to September.")


#Electricity prices dataframe

electricity_price = pd.DataFrame(models_dataset["Total €/MWh"])


#Plotting ARIMA results (order(10,1,0)

st.subheader("In order to forecast electricity prices, ARIMA models were used, using the historical electricity prices to predict future prices of the same variable. Below in red you can see the predictions:")

st.header('ARIMA Order(10,1,0)')


path = "https://raw.githubusercontent.com/PaulaCervilla/Electricity-prices-predictions-in-Spain---Data-Science-TFM/main/front%20end%20streamlit/predictions_actuals_ARIMA_1321.csv"

predictions = pd.read_csv(path, header= 0, dtype = str, engine= "python", sep=";", error_bad_lines= False, encoding= "utf-8")

predictions.set_index("Date", inplace=True)
predictions["Date"] = predictions.index
predictions["Date"] = pd.to_datetime(predictions['Date'], format= "%d/%m/%Y", errors = "ignore")
predictions.index = pd.DatetimeIndex(predictions.index, dayfirst= True)
predictions['Total €/MWh'] = pd.to_numeric(predictions['Total €/MWh'],errors= "raise", downcast="float")
predictions['pred'] = pd.to_numeric(predictions['pred'],errors= "raise", downcast="float")


#Plotting actual values and predictions out of sample

fig, ax = plt.subplots(figsize=(10,7));

ax.plot(predictions.index, predictions["Total €/MWh"].values)
ax.plot(predictions.index, predictions["pred"].values, color='red')

st.pyplot(fig)

with st.expander("Notes"):
     st.write("Based on the nature of the ARIMA equations, out-of-sample forecasts tend to converge to the sample mean for long forecasting periods.")


#Importing predictions ARIMA order(10,1,0)

predictions = pd.read_csv("https://raw.githubusercontent.com/PaulaCervilla/Electricity-prices-predictions-in-Spain---Data-Science-TFM/main/front%20end%20streamlit/predictions_ARIMA_1321.csv", header= 0, dtype = str, engine= "python", sep=";", error_bad_lines= False, encoding= "utf-8")

predictions.set_index("Date", inplace=True)
predictions["Date"] = predictions.index
predictions["Date"] = pd.to_datetime(predictions['Date'], format= "%d/%m/%Y", errors = "ignore")
predictions.index = pd.DatetimeIndex(predictions.index, dayfirst= True).to_period("D")
predictions['Total €/MWh'] = pd.to_numeric(predictions['Total €/MWh'],errors= "raise", downcast="float")
predictions['pred'] = pd.to_numeric(predictions['pred'],errors= "raise", downcast="float")

predictions['Total €/MWh'].fillna(0, inplace= True)
predictions['pred'].fillna(0, inplace= True)

predictions['Total €/MWh + Predictions'] = np.where(predictions['Total €/MWh'] == 0, predictions['pred'], predictions['Total €/MWh'])

predictions = predictions[["Date", "Total €/MWh + Predictions", "Total €/MWh", "pred"]]


#Datetime filter

def df_filter(message,df):


	slider_1, slider_2 = st.slider('%s' % (message), min_value = 0, max_value = len(df)-1, value = [0,len(df)-1], step = 1, key = 1)

	start_date = df.iloc[slider_1][0]
      
	end_date = df.iloc[slider_2][0]

	st.info('Start: **%s** End: **%s**' % (start_date,end_date))
        
	filtered_df = df.iloc[slider_1:slider_2+1][:].reset_index(drop=True)

	filtered_df.index = pd.to_datetime(filtered_df['Date'], dayfirst= True, errors = "ignore").dt.date

	return filtered_df


st.subheader('Date Filter:')
filtered_df = df_filter('Move sliders to filter dataframe with Actual prices and Predictions',predictions)

st.subheader('Data Frame')
st.write(filtered_df)

st.subheader('Line Chart Actual Electricity prices + Predictions')
st.line_chart(filtered_df['Total €/MWh + Predictions'])


#Plotting ARIMA results(order(4,1,5)

st.header('ARIMA Order(4,1,5)')

st.write("This ARIMA model was fitted with different parameters to make it more precise and optimal:")

path = "https://raw.githubusercontent.com/PaulaCervilla/Electricity-prices-predictions-in-Spain---Data-Science-TFM/main/front%20end%20streamlit/predictions_actuals_optARIMA_1321.csv"

predictions = pd.read_csv(path, header= 0, dtype = str, engine= "python", sep=";", error_bad_lines= False, encoding= "utf-8")

predictions.set_index("Date", inplace=True)
predictions["Date"] = predictions.index
predictions["Date"] = pd.to_datetime(predictions['Date'], format= "%d/%m/%Y", errors = "ignore")
predictions.index = pd.DatetimeIndex(predictions.index, dayfirst= True)
predictions['Total €/MWh'] = pd.to_numeric(predictions['Total €/MWh'],errors= "raise", downcast="float")
predictions['pred'] = pd.to_numeric(predictions['pred'],errors= "raise", downcast="float")



#Plotting actual values and predictions out of sample

fig, ax = plt.subplots(figsize=(10,7));

ax.plot(predictions.index, predictions["Total €/MWh"].values)
ax.plot(predictions.index, predictions["pred"].values, color='red')

st.pyplot(fig)

with st.expander("Notes"):
     st.write("Based on the nature of the ARIMA equations, out-of-sample forecasts tend to converge to the sample mean for long forecasting periods.")


#Importing predictions ARIMA order(4,1,5)

predictions_optARIMA = pd.read_csv("https://raw.githubusercontent.com/PaulaCervilla/Electricity-prices-predictions-in-Spain---Data-Science-TFM/main/front%20end%20streamlit/predictions_optimisedARIMA_1321.csv", header= 0, dtype = str, engine= "python", sep=";", error_bad_lines= False, encoding= "utf-8")

predictions_optARIMA.set_index("Date", inplace=True)
predictions_optARIMA["Date"] = predictions_optARIMA.index
predictions_optARIMA["Date"] = pd.to_datetime(predictions_optARIMA['Date'], format= "%d/%m/%Y", errors = "ignore")
predictions_optARIMA.index = pd.DatetimeIndex(predictions_optARIMA.index, dayfirst= True).to_period("D")
predictions_optARIMA['Total €/MWh'] = pd.to_numeric(predictions_optARIMA['Total €/MWh'],errors= "raise", downcast="float")
predictions_optARIMA['pred'] = pd.to_numeric(predictions_optARIMA['pred'],errors= "raise", downcast="float")

predictions_optARIMA['Total €/MWh'].fillna(0, inplace= True)
predictions_optARIMA['pred'].fillna(0, inplace= True)

predictions_optARIMA['Total €/MWh + Predictions'] = np.where(predictions_optARIMA['Total €/MWh'] == 0, predictions_optARIMA['pred'], predictions_optARIMA['Total €/MWh'])

predictions_optARIMA = predictions_optARIMA[["Date", "Total €/MWh + Predictions", "Total €/MWh", "pred"]]


#Datetime filter

def df_filter2(message,df):


	slider_3, slider_4 = st.slider('%s' % (message), min_value = 0, max_value = len(df)-1, value = [0,len(df)-1], step = 1, key = 2)

	start_date = df.iloc[slider_3][0]
      
	end_date = df.iloc[slider_4][0]

	st.info('Start: **%s** End: **%s**' % (start_date,end_date))
        
	filtered_df2 = df.iloc[slider_3:slider_4+1][:].reset_index(drop=True)

	filtered_df2.index = pd.to_datetime(filtered_df2['Date'], dayfirst= True, errors = "ignore").dt.date

	return filtered_df2

st.subheader('Date Filter:')
filtered_df2 = df_filter2('Move sliders to filter dataframe with Actual prices and Predictions',predictions_optARIMA)

st.subheader('Data Frame')
st.write(filtered_df2)

st.subheader('Line Chart Actual Electricity prices + Predictions')
st.line_chart(filtered_df2['Total €/MWh + Predictions'])


#VAR model

st.subheader("Relationships between different variables were studied and used to predict electricity prices and themselves. This was done using a Vector Auto Regresion Model (VAR).")

st.write('In a VAR model, each variable is a linear function of the past values of itself and the past values of all the other variables.')

st.write('The following variables were used: Final energy that was negotiated for each day measured in MWh, Average final price of energy measured in EUR by MWh, Brent Oil crude futures closing prices of the session for the day in EUR, Maximum Temperature (ºC), Minimum Temperature (ºC) and Average Wind Speed (Km/h).')


st.header('VAR model')

st.subheader("Firstly, Let's See Historical Data For These Variables:")

#Loading VAR predictions

path = "https://raw.githubusercontent.com/PaulaCervilla/Electricity-prices-predictions-in-Spain---Data-Science-TFM/main/front%20end%20streamlit/predictions_VAR_1321.csv"

forecast_VAR = pd.read_csv(path, header= 0, dtype = str, engine= "python", sep=";", error_bad_lines= False, encoding= "utf-8", names = (["Date","Energía final MWh", "Total €/MWh", "Precio cierre Brent","Tmax", "Tmin", "Vmax" ]))

forecast_VAR["Date"] = pd.to_datetime(forecast_VAR['Date'], format= "%d/%m/%Y", errors = "ignore")
forecast_VAR.set_index("Date", inplace=True)
forecast_VAR["Date"] = forecast_VAR.index

forecast_VAR["Energía final MWh"] = pd.to_numeric(forecast_VAR["Energía final MWh"], downcast="float")
forecast_VAR["Total €/MWh"] = pd.to_numeric(forecast_VAR["Total €/MWh"], downcast="float")
forecast_VAR["Precio cierre Brent"] = pd.to_numeric(forecast_VAR["Precio cierre Brent"], downcast="float")
forecast_VAR["Tmax"] = pd.to_numeric(forecast_VAR["Tmax"], downcast="float")
forecast_VAR["Tmin"] = pd.to_numeric(forecast_VAR["Tmin"], downcast="float")
forecast_VAR["Vmax"] = pd.to_numeric(forecast_VAR["Vmax"], downcast="float")

forecast_VAR = forecast_VAR[["Date", "Energía final MWh", "Total €/MWh", "Precio cierre Brent","Tmax","Tmin", "Vmax"]]

#Plotting some historical data

st.write("Below there is a graph showing historical Energy that was negotiated for each day measured in MWh since 2013:")

st.subheader('Total Energy MWh 2013-2021')

st.line_chart(electricity_brent_weather["Energía final MWh"])


st.write("Below there is a graph showing historical Brent Oil crude futures closing price of the session for the day in EUR since 2013:")

st.subheader('Brent Oil Crude Futures Closing Price Of The Session For The Day In EUR 2013-2021')

st.line_chart(electricity_brent_weather["Precio cierre Brent"])


st.write("Below there is a graph showing historical Maximum Temperature (ºC) since 2013:")

st.subheader('Maximum Temperature (ºC) 2013-2021')

st.line_chart(electricity_brent_weather["Tmax"])


st.write("Below there is a graph showing historical Minimum Temperature (ºC) since 2013:")

st.subheader('Minimum Temperature (ºC) 2013-2021')

st.line_chart(electricity_brent_weather["Tmin"])

st.write("Below there is a graph showing historical Average Wind Speed (Km/h) since 2013:")

st.subheader('Average Wind Speed (Km/h) 2013-2021')

st.line_chart(electricity_brent_weather["Vmax"])

with st.expander("Notes"):
     st.write("Weather data from 737 weather stations was used. In oder to get to a single daily value, a weighted average by each Spanish province population was done. In this way, the values for those provinces with more inhabitants were more important, in order to get to a final daily number.")

#Datetime filter

def df_filter3(message,df):


	slider_4, slider_5 = st.slider('%s' % (message), min_value = 0, max_value = len(df)-1, value = [0,len(df)-1], step = 1, key = 3)

	start_date = df.iloc[slider_4][0]
      
	end_date = df.iloc[slider_5][0]

	st.info('Start: **%s** End: **%s**' % (start_date,end_date))
        
	filtered_df3 = df.iloc[slider_4:slider_5+1][:].reset_index(drop=True)

	filtered_df3.index = pd.to_datetime(filtered_df3['Date'], dayfirst= True, errors = "ignore").dt.date

	return filtered_df3

st.subheader('Date Filter:')
filtered_df3 = df_filter3('Move sliders to filter dataframe with Predictions for 1 year ahead starting on the 10th of October 2021',forecast_VAR)

st.subheader('Data Frame')
st.write(filtered_df3)

st.subheader('Chart Predictions')
st.line_chart(filtered_df3['Total €/MWh'])

st.write("What we can see above is that, looking at what historically has happened, it was impossible to accurately forecast electricity prices. The reason behind this is that, as well as ARIMA models, out-of-sample forecasts tend to converge to the sample mean for long forecasting periods.")
st.write("Furthermore, 2021 and 2022 are seeing increases never seen in the market before, and therefore, impossible for Machine Learning models to predict.")


