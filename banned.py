import streamlit as st
import json
import pandas as pd
import folium
from streamlit_folium import st_folium
import joblib
import pandas as pd
import google.generativeai as genai
from sklearn.feature_extraction.text import TfidfVectorizer
from fuzzywuzzy import fuzz
import subprocess
if not isinstance(st.session_state, dict):
    st.session_state = {}

#Loads models
model = joblib.load('Prediction/model.joblib')
tfidf = joblib.load('Prediction/tfidf.joblib')
df_db = pd.read_csv("Prediction/merged_dataset.csv")
'''
Function Definitions for checking if 
title in db/predict banned/checking from gemini
'''

def check_pd(query_title, df_path="Prediction/merged_dataset.csv", threshold=60):
    df = df_db
    
    best_match = None
    highest_ratio = 0

    for _, row in df.iterrows():
        title = row['Title']
        banned_status = row['Banned']

        ratio = fuzz.ratio(query_title.lower(), title.lower())

        if ratio >= threshold and ratio > highest_ratio:
            best_match = (title, banned_status)
            highest_ratio = ratio

    # If a match is found, return the banned status of the highest-matching title
    return best_match[1] if best_match else False
def predict_banned(title: str, description: str, genre: str):
    text_input = title + " " + description + " " + genre
    embeddings= tfidf.transform([text_input])
    res=model.predict(embeddings)
    print(res)
def check_banned(title, author):
    API_KEY = "AIzaSyD8e6MpbO8uLTZvU4Ldxca2esUzgCfTkCg"
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
    PROMPT: Given a book name + author determine on a scale of 1 to 10 how likely it is to be [challenged to be removed in a school/public library], if they are outright banned give 10 if there is no record of challenge or possibility of censorship give it 0 Book: Keep in mind that books with sexeul content or involved in sexuality, communism, racism, gay/lgbtq, occult, suicidal thoughts, slavery, racism, revolutions, genocide, anti-government sentiments, war, and beastality, slanderour, pegan rituals or more likely to be challenged 
    Title: {title}, Author: {author}. RESPONSE FORMAT: STRICTLY IN NUMBER"""
    num = int((model.generate_content(prompt).text))
    
    return num
#Reading in datasets
df22 = pd.read_csv("data/PENAmericaBannedBooks21-22.csv")
df23 = pd.read_csv("data/PENAmericaBannedBooks22-23.csv")
df24 = pd.read_csv("data/PENAmericaBannedBooks23-24.csv")
dfAll = pd.concat([df22,df23,df24])

grdf = pd.read_csv("Training_data/goodreads_data.csv")[["Book", "Author", "Description", "Genres"]]
grdf_filtered = grdf[~grdf["Book"].isin(dfAll["Title"])]
grdf_banned = grdf[grdf["Book"].isin(dfAll["Title"])]


col1, col2 = st.columns([.15,.85])

with col1:
    st.image("banbooklogo.png", width=100)
with col2:
    st.title("Book Bans Across the U.S")

with st.form("form"):
    l_col, r_col = st.columns(2)
    title = l_col.text_input("Title")
    author = r_col.number_input("author", value=None, format='%0.0f')
    submit = st.form_submit_button("Search")

if "html_str" not in st.session_state:
    st.session_state['html_str'] = "<p>Enter details and click Search.</p>"

if submit:
    st.session_state['html_str'] = f"<p>{title}, {author}</p>"
    search_list = [title, author]
    status = check_pd(title)
    if status==1:
        description ="Book is Banned/Challenged"
        st.session_state['html_str'] =description
    else:
        num = check_banned(title, author)
        if(num>=7): 
            description ="Book is Banned/Challenged"
        elif num>=3:
            description ="Book is potentially Challenged"
        else:
            description ="Book is not Challenged"
        st.session_state['html_str'] =description
    

st.markdown(st.session_state['html_str'], unsafe_allow_html=True)


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

