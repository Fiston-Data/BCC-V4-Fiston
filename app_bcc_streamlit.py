import streamlit as st
import pandas as pd
import plotly.express as px
import psycopg2

st.set_page_config(page_title="BCC 24,1M Dashboard", layout="wide")
st.title("BANQUE CENTRALE DU CONGO - Dashboard 24,1M")
st.caption("BDD reelle : banque_centrale - Fiston NZALAYALA")

DB_CONFIG = {
    "host": "localhost",
    "database": "banque_centrale",
    "user": "postgres",
    "password": "ton_password",
    "port": "5432"
}

@st.cache_data
def get_data():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        df = pd.read_sql("SELECT * FROM bcc_table", conn)
        conn.close()
        st.success("Connecté à PostgreSQL")
        return df
    except Exception as e:
        st.warning(f"Mode démo CSV (DB non connectée)")
        # Charge CSV et normalise les colonnes
        try:
            df = pd.read_csv("data_bcc.csv")
        except:
            df = pd.read_csv("data_bcc.csv", encoding='latin-1', sep=';')
        
        # Nettoie les noms de colonnes
        df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]
        return df

df = get_data()

st.write("Aperçu données :", df.head())
st.write("Colonnes :", list(df.columns))

# --- CORRECTION AUTOMATIQUE DES COLONNES ---
# On cherche la colonne montant
montant_col = None
for col in df.columns:
    if 'montant' in col or 'total' in col or 'value' in col or 'amount' in col:
        montant_col = col
        break
if not montant_col:
    # prend la première colonne numérique
    montant_col = df.select_dtypes(include='number').columns[0]

devise_col = None
for col in df.columns:
    if 'devise' in col or 'currency' in col or 'code' in col:
        devise_col = col
        break
if not devise_col:
    devise_col = df.columns[0]

st.subheader(f"TOTAL PAR DEVISE - basé sur {montant_col} / {devise_col}")

# Graphiques qui marchent peu importe le nom des colonnes
fig1 = px.bar(df, x=devise_col, y=montant_col, title=f"Total par {devise_col}")
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.pie(df, values=montant_col, names=devise_col, title="Répartition")
st.plotly_chart(fig2, use_container_width=True)

# Menu BCC
st.sidebar.title("Menu BCC")
choix = st.sidebar.selectbox("TOTAL 24,1M", [str(x) for x in df[devise_col].unique()[:10]])
