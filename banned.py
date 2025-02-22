import streamlit as st
import json
import pandas as pd
import folium
from streamlit_folium import st_folium

#Reading in datasets
df22 = pd.read_csv("data/PENAmericaBannedBooks21-22.csv")
df23 = pd.read_csv("data/PENAmericaBannedBooks22-23.csv")
df24 = pd.read_csv("data/PENAmericaBannedBooks23-24.csv")
dfAll = pd.concat([df22,df23,df24])


st.title("Book Bans Across the U.S")

#Dropbox for selecting school year
option = st.selectbox(
    "What school year are you interested in?",
    ("21-22", "22-23", "23-24", "All Available")
)

if option == "21-22":
    df = df22
elif option == "22-23":
    df = df23
elif option == "23-24":
    df = df24
else:
    df = dfAll







#Counting no. of banned books per state
state_counts = df["State"].value_counts().reset_index()
state_counts.columns = ["State", "count"]



#Base map
m = folium.Map(location=[37.0902, -95.7129], zoom_start=4)

#Load US GeoJson
with open("data/us-states.json") as f:
    us_states = json.load(f)

#Adding banned book counts to state features
for feature in us_states["features"]:
    state_name = feature["properties"]["name"]
    count_row = state_counts[state_counts["State"] == state_name]
    
    if not count_row.empty:
        feature["properties"]["banned_books"] = int(count_row.iloc[0]["count"])
    else:
        feature["properties"]["banned_books"] = "N/A"
#Add chloropleth layer to map
folium.Choropleth(
    geo_data=us_states,
    name="choropleth",
    data=state_counts,
    columns=["State", "count"],
    key_on="feature.properties.name",
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Number of Banned Books"
).add_to(m)

#hover
folium.LayerControl().add_to(m)

#making tooltip
style_function = lambda x: {
    "fillColor": "#ffffff",
    "color": "#000000",
    "fillOpacity": 0.1,
    "weight": 0.1
}

highlight_function = lambda x: {
    "fillColor": "#000000",
    "color": "#000000",
    "fillOpacity": 0.50,
    "weight": 0.1
}

NIL = folium.features.GeoJson(
    us_states,
    style_function=style_function,
    control=False,
    highlight_function=highlight_function,
    tooltip=folium.features.GeoJsonTooltip(
        fields=["name", "banned_books"],
        aliases=["state: ", "banned books: "],
        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
    )
)
m.add_child(NIL)
m.keep_in_front(NIL)

#Display map
st_folium(m, width=700, height=500)

#Display dataframe
st.subheader("Banned Books Details")
st.dataframe(df)