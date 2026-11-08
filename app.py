import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Gapminder Explorer", layout="wide")
st.title("Country Data Explorer")
st.write("Pick a continent, countries, and a metric to see how they change over time.")

df = px.data.gapminder()

continent = st.selectbox("Continent", sorted(df["continent"].unique()))
countries_in_continent = sorted(df[df["continent"] == continent]["country"].unique())
countries = st.multiselect("Countries", countries_in_continent, default=countries_in_continent[:3])
metric = st.selectbox("Metric", ["lifeExp", "pop", "gdpPercap"])
chart_type = st.radio("Chart type", ["Line", "Bar"], horizontal=True)
years = st.slider("Year range", 1952, 2007, (1952, 2007), step=5)

filtered = df[(df["country"].isin(countries)) & (df["year"] >= years[0]) & (df["year"] <= years[1])]

if filtered.empty:
    st.warning("Please select at least one country.")
else:
    if chart_type == "Line":
        fig = px.line(filtered, x="year", y=metric, color="country", markers=True)
    else:
        fig = px.bar(filtered, x="year", y=metric, color="country", barmode="group")
    fig.update_layout(title=f"{metric} over time", xaxis_title="Year", yaxis_title=metric)
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("Show data table"):
        st.dataframe(filtered)
