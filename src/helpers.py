import secrets
import streamlit as st
import gspread as gs
import datetime

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


def get_items():
    gc = gs.service_account_from_dict(credentials)
    sh = gc.open_by_url(gs_url)
    worksheet = sh.get_worksheet(0)
    return worksheet.get_all_records()


def save_into_csv(filename, types, styles, colors, light, glass, nlegs, nschub, ntuere, nregal, symetrie, eckig, leg_length, leg_width, leg_direction, leg_color, griff, griff_mat, spiegel, schiebetür, skipped):
    gc = gs.service_account_from_dict(credentials)
    sh = gc.open_by_url(gs_url)
    worksheet = sh.get_worksheet(0)

    new_row = [filename, types, styles, colors, light, glass, nlegs, nschub, ntuere, nregal, symetrie, eckig,
               leg_length, leg_width, leg_direction, leg_color, griff, griff_mat,
               spiegel, schiebetür, str(datetime.datetime.now()), skipped]
    worksheet.append_row(new_row)
