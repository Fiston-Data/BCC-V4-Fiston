import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="BCC 24,1M Dashboard", layout="wide")
st.title("BANQUE CENTRALE DU CONGO - Dashboard 24,1M")
st.caption("BDD reelle : banque_centrale - Fiston NZALAYALA")

@st.cache_data
def get_data():
    df = pd.read_csv("data_bcc.csv")
    return df

df = get_data()

st.success("Donnees BCC 24,1M chargees")
st.dataframe(df, use_container_width=True)

c1, c2, c3 = st.columns(3)
c1.metric("TOTAL USD", f"${df['usd_equivalent'].sum():,}")
c2.metric("Devises", len(df))
c3.metric("Statut", "En ligne")

fig1 = px.bar(df, x='code_devise', y='usd_equivalent', color='nom_devise', title="Repartition 24,1M par devise")
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.pie(df, values='usd_equivalent', names='code_devise', title="Part en %")
st.plotly_chart(fig2, use_container_width=True)

st.sidebar.title("Menu BCC")
st.sidebar.metric("TOTAL", "24,1M USD")
st.sidebar.dataframe(df)

st.sidebar.title("Menu BCC")
st.sidebar.metric("TOTAL", "24,1M USD")
st.sidebar.dataframe(df[['code_devise','solde_actuel','usd_equivalent']])24,1M", [str(x) for x in df[devise_col].unique()[:10]])
