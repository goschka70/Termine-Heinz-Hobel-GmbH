import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="📅 Termin-Zeitband", layout="wide")
st.title("📅 Termin-Zeitband für Riedstadt / Griesheim")

# Datei-Upload oder API
uploaded_file = st.file_uploader("CSV-Datei hochladen", type="csv")

if uploaded_file:
    df_raw = pd.read_csv(uploaded_file, sep=";", encoding="utf-8")

    # Termin-Spalte in datetime konvertieren
    df_raw["Termin"] = pd.to_datetime(df_raw["Termin"], errors="coerce")

    # Filter für heutigen Tag
    today = pd.Timestamp.now().date()
    df_today = df_raw[df_raw["Termin"].dt.date == today]

    # Standortauswahl
    standort = st.selectbox("📍 Standort auswählen", options=["Riedstadt", "Griesheim"])

    # Filter nach Standort
    df_filtered = df_today[df_today["Platz"].str.contains(standort, case=False, na=False)]

    # Sortieren nach Termin
    df_filtered = df_filtered.sort_values("Termin")

    # Nächster Termin bestimmen
    now = pd.Timestamp.now()
    df_future = df_filtered[df_filtered["Termin"] > now]
    next_termin = df_future.iloc[0] if not df_future.empty else None

    # Timeline vorbereiten
    timeline_df = df_filtered.copy()
    timeline_df["Start"] = timeline_df["Termin"]
    timeline_df["End"] = timeline_df["Termin"] + pd.Timedelta(minutes=30)
    timeline_df["Beschreibung"] = (
        timeline_df["Terminart"] + " - " + timeline_df["Nachname"].fillna("") + ", " + timeline_df["Vorname"].fillna("")
    )

    # Farben für Hervorhebung
    timeline_df["Farbe"] = "Blau"
    if next_termin is not None:
        timeline_df.loc[timeline_df["Termin"] == next_termin["Termin"], "Farbe"] = "Rot"

    # Timeline anzeigen
    fig = px.timeline(
        timeline_df,
        x_start="Start",
        x_end="End",
        y="Platz",
        color="Farbe",
        hover_name="Beschreibung",
        title=f"Termine am {today.strftime('%d.%m.%Y')} – Standort: {standort}",
        color_discrete_map={"Blau": "lightblue", "Rot": "red"},
    )
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)

    # Nächster Termin separat anzeigen
    if next_termin is not None:
        st.markdown("### 🔔 Nächster Termin")
        st.info(
            f"**{next_termin['Terminart']}** mit **{next_termin['Nachname']} {next_termin['Vorname']}** um **{next_termin['Termin'].strftime('%H:%M')} Uhr**"
        )
else:
    st.warning("Bitte lade eine CSV-Datei hoch.")
