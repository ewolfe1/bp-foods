import streamlit as st
state = st.session_state
import pandas as pd
from natsort import natsorted
from PIL import Image, ImageDraw
import nltk
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

# set page configuration. Can only be set once per session and must be first st command called
def page_config():
    try:
        st.set_page_config(page_title='Good for your heart', page_icon=':heart:', layout='wide')
    except st.errors.StreamlitAPIException as e:
        if "can only be called once per app" in e.__str__():
            return

def round_corners(url):

    # Load your image
    image = Image.open(url)

    width, height = image.size
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, width, height), 20, fill=255)
    result = Image.new("RGBA", (width, height))
    result.paste(image, (0, 0), mask)
    return result

def get_data():

    df = pd.read_csv('data/pred_food.csv')
    df = df[(~df['Type'].isnull())][[c for c in df if 'Suitable' not in c]]
    rename_cols = {c: c.replace(' Content', '') for c in df.columns}
    df = df.rename(columns=rename_cols)
    df.sort_values(by='Food Name', inplace=True)
    df.set_index('Food Name', inplace=True)

    state.ing_df = df[df.Type=='Ingredient'][[c for c in df if c != 'Type']]
    state.prep_df = df[df.Type=='Prepared food'][[c for c in df if c != 'Type']]
    state.meals_df = pd.read_csv('data/meals.csv')

def get_lemma(word):
    return lemmatizer.lemmatize(word)

def clear_text():
    st.session_state["ing_filter"] = ""
