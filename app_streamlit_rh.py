
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Pilotage RH - Atelier de la Donnée", layout="wide")

# Chargement des données
@st.cache_data
def load_data():
    return pd.read_csv("dataset_RH_Atelier_de_la_Donnee.csv", parse_dates=['Date_Entrée'])

df = load_data()

# KPIs
effectif_total = len(df)
masse_salariale_totale = df['Salaire Mensuel Brut (€)'].sum()
taux_turnover = df['Turnover_2024'].mean() * 100
age_moyen = df['Âge'].mean().round(1)
anciennete_moyenne = df['Ancienneté (années)'].mean().round(1)
absenteisme_moyen = df["Jours d'absence"].mean().round(1)

st.title("📊 Pilotage RH - Effectifs & Masse Salariale")
st.markdown("Application RH interactive pour visualiser les indicateurs clés d'une entreprise fictive.")

# KPIs en colonnes
col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("Effectif Total", effectif_total)
col2.metric("Masse Salariale (€)", f"{masse_salariale_totale:,.0f}")
col3.metric("Turnover 2024 (%)", f"{taux_turnover:.2f}")
col4.metric("Âge Moyen", age_moyen)
col5.metric("Ancienneté Moyenne", anciennete_moyenne)
col6.metric("Absentéisme Moyen", absenteisme_moyen)

st.markdown("---")

# Filtres
with st.sidebar:
    st.header("🎛️ Filtres")
    departement = st.multiselect("Département", df["Département"].unique(), default=df["Département"].unique())
    statut = st.multiselect("Statut", df["Statut"].unique(), default=df["Statut"].unique())
    grade = st.multiselect("Grade", df["Grade"].unique(), default=df["Grade"].unique())

df_filtered = df[
    df["Département"].isin(departement) &
    df["Statut"].isin(statut) &
    df["Grade"].isin(grade)
]

# Graphiques
col1, col2 = st.columns(2)
with col1:
    fig1 = px.histogram(df_filtered, x="Département", color="Sexe", barmode="group",
                        title="Répartition des effectifs par département")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.pie(df_filtered, names="Sexe", title="Répartition H/F")
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

col3, col4 = st.columns(2)
with col3:
    fig3 = px.box(df_filtered, x="Département", y="Salaire Mensuel Brut (€)", color="Statut",
                  title="Distribution des salaires par département")
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    fig4 = px.bar(df_filtered.groupby("Grade")["Salaire Mensuel Brut (€)"].mean().reset_index(),
                  x="Grade", y="Salaire Mensuel Brut (€)", title="Salaire moyen par grade")
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

st.dataframe(df_filtered.reset_index(drop=True), use_container_width=True)
