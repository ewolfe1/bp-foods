import streamlit as st
state = st.session_state
import pandas as pd
import base64
import requests
from scripts import tools

tools.page_config()
tools.get_data()

head_cols = st.columns((7,2,1))
with head_cols[0]:
    st.write('# Good for your heart foods')
    st.write('A guide to heart healthy vegetarian foods that can help to lower blood pressure.')
with head_cols[1]:
    st.image(tools.round_corners('res/head_img.jpg'), width=400)

st.write('## Raw foods')
rf_cols = st.columns((5,1))
with rf_cols[0]:
    st.write('*See the nutritional value of some common foods. The progress bar displays the value in relation to the other foods in the list. Click any column header to change the sort order.*')
with rf_cols[1]:
    hide_pb_rf = st.checkbox('Hide progress bars', key="hide_pb_rf")

if hide_pb_rf:
    st.dataframe(state.ing_df, use_container_width=True)
else:
    st.data_editor(state.ing_df,column_config={
                c: st.column_config.ProgressColumn(
                format="%f", min_value=int(state.ing_df[c].min()),
                max_value=int(state.ing_df[c].max())) for c in state.ing_df},
                use_container_width=True)

st.write('## Prepared foods')
meal_tabs1, meal_tabs2 = st.tabs(['Recipe ideas', 'Nutritional value'])

with meal_tabs1:

    pf_cols = st.columns((5,1))
    with pf_cols[0]:
        st.write('*See the nutritional value of some prepared foods. The progress bar displays the value in relation to the other foods in the list. Click any column header to change the sort order.*')
    with pf_cols[1]:
        hide_pb_pf = st.checkbox('Hide progress bars', key="hide_pb_pf")

    if hide_pb_pf:
        st.dataframe(state.prep_df, use_container_width=True)
    else:
        st.data_editor(state.prep_df,column_config={
                    c: st.column_config.ProgressColumn(
                    format="%d", min_value=state.prep_df[c].min(),
                    max_value=state.prep_df[c].max()) for c in state.prep_df},
                    use_container_width=True)

with meal_tabs2:

    st.write('## Meal ideas')
    ing_search_cols = st.columns((3,1,4))
    with ing_search_cols[0]:
        ing_filter = st.text_input('*Filter by ingredient (separate multiple ingredients with a comma)*',
                                    key="ing_filter")
    if ing_filter.strip() != '':
        ings = ing_filter.split(',')

        try:
            ings = [tools.get_lemma(i) for i in ings]
        except:
            pass

        conditions = [state.meals_df['ingredients'].str.contains(i.strip(), case=False) for i in ings]
        state.meals_df_filtered = state.meals_df[pd.DataFrame(conditions).all(axis=0)]

        # state.meals_df = state.meals_df[
        #                 state.meals_df.ingredients.str.contains('|'.join([i.strip() \
        #                 for i in ing_filter.split(',')]), case=False)]
    else:
        state.meals_df_filtered = state.meals_df
    with ing_search_cols[1]:
        st.button("clear text input", on_click=tools.clear_text)

    meal_cols = st.columns(4)
    ct = 0
    for i,r in state.meals_df_filtered.iterrows():

        with meal_cols[ct]:
            try:
                img = requests.get(r.image)
                img.raise_for_status()  # Check if the request was successful
                thumb = img.content
            except requests.RequestException as e:
                print(f"Error fetching the image: {e}")
            st.markdown(
                    f"""<a href="{r.url}">
                    <img src="data:image/png;base64,{base64.b64encode(thumb).decode()}" height="250">
                    </a><p><a href={r.url}>{r.meal}</a></p>""",unsafe_allow_html=True,)

            # st.write(html, unsafe_allow_html=True)
            if ct < 3:
                 ct += 1
            else:
                ct = 0

with st.expander('Sources'):
    st.write('Dataset: Food suitable for diabetes and blood pressure. [https://www.kaggle.com/datasets/nandagopll/food-suitable-for-diabetes-and-blood-pressure](https://www.kaggle.com/datasets/nandagopll/food-suitable-for-diabetes-and-blood-pressure)')
