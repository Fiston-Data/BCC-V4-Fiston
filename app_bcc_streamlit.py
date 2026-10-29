import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="BCC V4 - Fiston", layout="wide")
st.title("BANQUE CENTRALE DU CONGO - Dashboard 24,1M")
st.markdown("**BDD reelle : banque_centrale - Fiston NZALAYALA**")

DB_CONFIG = {
    "host": "localhost",
    "database": "banque_centrale",
    "user": "postgres",
    "password": "6908"  # <--- CHANGE ICI ton mdp postgres
}

def get_data(query):
    conn = psycopg2.connect(**DB_CONFIG)
    df = pd.read_sql(query, conn)
    conn.close()
    return df

menu = st.sidebar.selectbox("Menu BCC", ["TOTAL 24,1M", "SOLDE COMPTES", "DEVISES"])

if menu == "TOTAL 24,1M":
    st.header("TOTAL PAR DEVISE")
    df = get_data("""
        SELECT d.code_devise, SUM(cr.solde_actuel) as total
        FROM comptes_reserve cr
        JOIN devises d ON cr.id_devise = d.id_devise
        GROUP BY d.code_devise ORDER BY total DESC
    """)
    st.dataframe(df, use_container_width=True)
    c1,c2 = st.columns(2)
    c1.metric("TOTAL", f"{df['total'].sum():,.0f} $")
    c2.metric("NB DEVISES", len(df))
    st.plotly_chart(px.bar(df, x='code_devise', y='total', color='code_devise', title="Repartition 24,1M"), use_container_width=True)
    st.plotly_chart(px.pie(df, values='total', names='code_devise'), use_container_width=True)

elif menu == "SOLDE COMPTES":
    df = get_data("SELECT cr.numero_compte, cr.solde_actuel, d.code_devise FROM comptes_reserve cr JOIN devises d ON cr.id_devise=d.id_devise ORDER BY cr.solde_actuel DESC")
    st.dataframe(df, use_container_width=True)
    st.metric("Plus gros compte", f"{df.iloc[0]['numero_compte']} - {df.iloc[0]['solde_actuel']:,.0f} {df.iloc[0]['code_devise']}")

else:
    df = get_data("SELECT id_devise, code_devise, nom_devise, symbole FROM devises")
    st.dataframe(df, use_container_width=True)