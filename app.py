import streamlit as st
import gspread as gs
import os
import pandas as pd
from src.helpers import get_items, save_into_csv
import datetime

all_items = os.listdir('img')

if 'count' not in st.session_state:
    st.session_state.count = 0
    st.session_state.answers = 0

credentials = {
    "type": "service_account",
    "project_id": "labeling2",
    "private_key_id": st.secrets["private_key_id"],
    "private_key": st.secrets["private_key"],
    "client_email": st.secrets["client_email"],
    "client_id": st.secrets["client_id"],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": st.secrets['client_x509_cert_url']
}
gs_url = st.secrets["url"]

gc = gs.service_account_from_dict(credentials)
sh = gc.open_by_url(gs_url)
worksheet = sh.get_worksheet(0)
data = worksheet.get_all_records()


labeled_items = pd.DataFrame(data)['Filename'].unique()

final_list = list(set(all_items) - set(labeled_items))

filename = final_list[st.session_state.count]
path = "img/{}".format(filename)


with st.sidebar:
    st.image(path)
    skipped = st.checkbox('Skipped?', False)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.subheader('Overal')

    types = st.multiselect(
        'Motivational Type',
        ['Mondän', 'Rational', 'Fürsorglich', 'Traditionel', 'Unabhängig'],
        ['Mondän', 'Rational', 'Fürsorglich', 'Traditionel', 'Unabhängig'],
        key='type')

    styles = st.multiselect(
        'Style',
        ['Midcentury', 'Landhause', 'Modern', 'Classic', 'Industrial', 'Other'],
        ['Midcentury'],
        key='style')

    symetrie = st.checkbox('Is symetric?', True)
    eckig = st.checkbox('Is curvy (alt. eckig)?', True)
    light = st.checkbox('Lights?', True)
    glass = st.checkbox('Transparent doors?', True)

with col2:
    st.subheader('Legs')
    nlegs = st.slider('Wie viele Biene', min_value=0,
                      max_value=5, value=4, key='nleg')

    leg_length = st.multiselect(
        'Leg length',
        ['lang', 'mittel', 'kurz'],
        ['mittel'],
        key='llength')

    leg_width = st.multiselect(
        'Leg thickness',
        ['extra thin', 'thin', 'mittel', 'thick'],
        ['thin'],
        key='lthick')

    leg_direction = st.checkbox('Standing out legs?')

    leg_color = st.multiselect(
        'Leg color',
        ['light holz', 'dark holz', 'chrom', 'gold',
         'schwarz', 'weiß', 'other'],
        [],
        key='lcol')

with col4:
    st.subheader('Griff')
    griff = st.multiselect(
        'Griff form',
        ['rund', 'thin', 'curvy', 'long', 'squire'],
        [],
        key='blength')

    griff_mat = st.multiselect(
        'Griff Material',
        ['holz', 'metal', 'other'],
        [],
        key='bform')


with col3:
    st.subheader('Türe')
    ntuere = st.slider('Wie viele Türe', min_value=0,
                       max_value=5, value=4, key='ntuer')
    nschub = st.slider('Wie viele Schubladen', min_value=0,
                       max_value=5, value=4, key='nschub')
    nregal = st.slider('Wie viele offene Regale', min_value=0,
                       max_value=5, value=4, key='nreg')

    colors = st.multiselect(
        'Pattern',
        ['light holz', 'dark holz', 'grau',
         'schwarz', 'weiß', 'textured pannel', 'multicolor', 'other'],
        ['weiß'],
        key='pattern'
    )

    spiegel = st.checkbox('Spiegel?', False)
    schiebetür = st.checkbox('Schiebetür?', False)

increment = st.button('Confirm')
if increment:
    st.session_state.count += 1
    save_into_csv(str(filename), str(types), str(styles),
                  str(colors), str(light), str(glass), str(
                      nlegs), str(nschub), str(ntuere), str(nregal),
                  str(symetrie), str(eckig), str(
                      leg_length), str(leg_width),
                  str(leg_direction), str(leg_color), str(
                      griff), str(griff_mat), str(spiegel),
                  str(schiebetür), str(skipped))

    st.write('Thanks! Saved!')
    with st.sidebar:
        st.button('Next')
