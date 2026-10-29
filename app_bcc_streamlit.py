import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="BCC Dashboard", layout="wide")
st.title("BANQUE CENTRALE DU CONGO - Dashboard")
st.caption("Fiston NZALAYALA - 29/10/2026")

df = pd.read_csv("data_bcc.csv")
st.success("Donnees chargees")
st.dataframe(df)

c1, c2, c3 = st.columns(3)
c1.metric("TOTAL", "24.1M USD")
c2.metric("Devises", len(df))
c3.metric("Statut", "OK")

fig1 = px.bar(df, x='code_devise', y='usd_equivalent', title="Repartition")
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.pie(df, values='usd_equivalent', names='code_devise', title="Parts")
st.plotly_chart(fig2, use_container_width=True)

st.sidebar.title("Menu BCC")
st.sidebar.dataframe(df)
