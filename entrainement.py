import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

df = pd.read_csv("consoelecgaz2024.csv",sep="\t")

df["Conso totale (MWh)"] = df["Conso totale (MWh)"].str.replace(",", ".").astype(float)
df["Conso moyenne (MWh)"] = df["Conso moyenne (MWh)"].str.replace(",", ".").astype(float)

df["Code Région"] = df["Code Région"].astype(object)
numeric_cols = df.select_dtypes(exclude="object").columns.to_list()

categorical_cols = df.select_dtypes(include="object").columns.to_list()


st.title("Dashboard sur des données énergétiques !")
st.caption("C'est la première fois que j'utilise streamlit, je vais m'entrainer en utilisant un fichier CSV recensant différentes variables permettant de réaliser une analyse complète.")

st.subheader("Voici le fichier CSV sur lequel j'ai réaliser ce Dashboard : ")

st.dataframe(df)

st.markdown(f"Voici les dimensions de notre DataFrame {df.shape} et voici les différentes colonnes associées : ")

st.write(df.columns)

st.header("Analyse exploratoire des variables qualitatives")

st.subheader(f"Différentes variables qualitatives issues du fichier : ")
st.write(df.select_dtypes(include="object").columns)

var_quali = st.selectbox("Choisissez la variable catégorielle à analyser", categorical_cols)

filtre = st.radio("Voulez-vous ajouter un filtre ?", ["Non", "Oui"])

filtered_col = [col for col in categorical_cols if col != "Année"]

# --- FILTRE SUR L'ANNÉE ---
if "Année" in df.columns:
    annees = sorted(df["Année"].dropna().unique())
    annee_choisie = st.select_slider("Filtrer par année", ["Toutes"] + annees)

    if annee_choisie != "Toutes":
        df = df[df["Année"] == annee_choisie]

df_filtered = df

if filtre == "Oui":
    var_filtre = st.selectbox("Choisissez une variable de filtre", filtered_col)

    modalites = ["Toutes"] + sorted(df[var_filtre].dropna().unique().tolist())
    modalite_choisie = st.selectbox(f"Choisissez une modalité de {var_filtre}", modalites)

    if modalite_choisie != "Toutes":
        df_filtered = df[df[var_filtre] == modalite_choisie]

df_quali = df_filtered[var_quali].value_counts().reset_index()
df_quali.columns = [var_quali, "count"]

if len(df_quali) > 10:
    df_quali_top10 = df_quali.sort_values("count", ascending=False).head(10)
    fig_quali = px.bar(
        data_frame=df_quali_top10,
        x=var_quali,
        y="count",
        title=f"Top 10 des modalités de {var_quali}"
    )
else:
    fig_quali = px.pie(
        data_frame=df_quali,
        names=var_quali,
        values="count",
        title=f"Répartition des modalités de {var_quali}"
    )

st.plotly_chart(fig_quali)

var_x = st.selectbox("Choisi la variable en Abscisse",df.drop(columns=["Code Département","Code Région"]).columns)
var_y = st.selectbox("Choisi la variable en Ordonnée ",df[["Conso totale (MWh)","Conso moyenne (MWh)","Nb sites"]].columns)

def repartition(var_x, var_y):
    df_grouped = df.groupby(var_x)[var_y].sum().reset_index()
    nb_modalite =df_grouped[var_x].nunique()

    if  nb_modalite <= 6 :
        fig = px.pie(
        df_grouped,
        names=var_x,
        values=var_y,
        title=f" Repartition de {var_y} selon {var_x}",
        
    )
    

    elif 6 <= nb_modalite <= 15 :
        fig = px.bar(
            df_grouped,
            x=var_x,
            y=var_y,
            title=f"{var_y} par {var_x}",
            labels={var_x: var_x, var_y: var_y},
            text_auto=True,
            color=var_y
        )


    else:
    
        fig = px.line(
            df_grouped,
            x=var_x,
            y=var_y,
            title=f"{var_y} par {var_x}",
            labels={var_x: var_x, var_y: var_y}
        )

    st.plotly_chart(fig)

repartition(var_x, var_y)
