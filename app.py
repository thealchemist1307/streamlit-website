import streamlit as st
import pandas as pd 
import numpy as np 
import pydeck as pdk
import plotly.express as px
DATA_URL=("/home/nishit/ML Website/Website/Motor_Vehicle_Collisions_-_Crashes.csv")

st.title("Motor Vehovle Collision in NY")
st.markdown("A streamlit dashboard that shows collision data visualization")


data=pd.read_csv(DATA_URL,nrows=100000,parse_dates=[['CRASH_DATE','CRASH_TIME']])
data = data.filter(['CRASH_DATE_CRASH_TIME','LATITUDE','LONGITUDE','INJURED_PERSONS'], axis=1)
data=data.dropna(axis=0,how="any")
lowercase=lambda x : str(x).lower()
data.rename(lowercase,axis='columns',inplace=True)
data.rename(columns={'crash_date_crash_time':'date/time'},inplace=True)
st.header("Where are the most people injured")
injured_people=st.slider("No. of people injured in collision",0,19)
st.map(data.query("injured_persons>=@injured_people")[["latitude","longitude"]].dropna(how="any"))

st.header("How many collsion occur during a a given time of day?")
hour=st.slider("Hour to look at",0,23)
data=data[data['date/time'].dt.hour==hour]

st.markdown("Vehicle Collision between %i:00 and %i:00" %(hour,(hour+1)%24)) 
data.dropna(subset=['longitude', 'latitude'])
st.write(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state={"latitude":40.730610,
                        "longitude":-73.935242,
                        "zoom":11,
                        "pitch":50},
    layers=[pdk.Layer("HexagonLayer",
                      data=data[['date/time','latitude','longitude']],
                      get_position=['longitude','latitude'],
                      radius=100,
                      extruded=True,
                      pickable=True,
                      elevation_scale=4,
                      elevation_range=[0,1000])]
))
st.subheader("Breakdown in minutes between %i:00 and %i:00" %(hour,(hour+1)%24)) 
filtered=data[
    (data['date/time'].dt.hour>=hour) & (data['date/time'].dt.hour<((hour+1)%24))
]
hist=np.histogram(filtered['date/time'].dt.minute,bins=60,range=(0,60))[0]
chart_data=pd.DataFrame({'minute':range(60),'crashes':hist})
fig=px.bar(chart_data,x='minute',y='crashes',hover_data=['minute','crashes'],height=400)
st.write(fig)

if st.checkbox("Show Raw Data",False):
    st.subheader('Raw Data')
    st.write(data)
