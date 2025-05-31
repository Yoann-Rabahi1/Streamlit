import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

df = pd.read_csv("consoelecgaz2024.csv",sep="\t")

df["Conso totale (MWh)"] = df["Conso totale (MWh)"].str.replace(",", ".").astype(float)
df["Conso moyenne (MWh)"] = df["Conso moyenne (MWh)"].str.replace(",", ".").astype(float)

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

var_quali = st.selectbox("Choisi une variable qualitative",categorical_cols)

df_quali = df[var_quali].value_counts().reset_index()
df_quali.columns = [var_quali, "count"]

if len(df_quali) > 10:
    df_quali_top10 = df_quali.sort_values("count", ascending=False).head(10)

    fig_quali = px.bar(
        data_frame=df_quali_top10,
        x=var_quali,
        y="count",
        title=f"Répartition du top 10 de la variable {var_quali}"
    )
    st.plotly_chart(fig_quali)

else:
    fig_quali = px.pie(
        data_frame=df_quali,
        names=var_quali,
        values="count",
        title=f"Répartition de la variable {var_quali}"
    )
    st.plotly_chart(fig_quali)


var_x = st.selectbox("Choisi la variable en Abscisse",numeric_cols)
var_y = st.selectbox("Choisi la variable en Ordonnée ",numeric_cols)



var_categorical = st.selectbox("Choisi la couleur en fonction des variables qualitatives", categorical_cols)


fig_1 = px.bar(
    data_frame = df,
    x = var_x,
    y = var_y,
    color=var_categorical,
    title=str(var_x) + " VS " + str(var_y)
)

st.plotly_chart(fig_1)

