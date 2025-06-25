import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from supabase import create_client, Client # Assumi che siano già installate

# Funzione astratta per caricare i dati
@st.cache_data(ttl=600) # Cacha i dati per performance
def load_data(source_type, connection_details):
    df = pd.DataFrame() # Inizializza un DataFrame vuoto
    try:
        if source_type == "Supabase":
            # Per Supabase, connection_details potrebbe contenere URL e KEY
            supabase_url = connection_details.get("url")
            supabase_key = connection_details.get("key")
            table_name = connection_details.get("table_name")

            if not supabase_url or not supabase_key or not table_name:
                st.error("Configurazione Supabase incompleta.")
                return df

            supabase: Client = create_client(supabase_url, supabase_key)
            response = supabase.from_(table_name).select('*').execute()
            if response.data:
                df = pd.DataFrame(response.data)
            else:
                st.warning("Nessun dato trovato nella tabella Supabase.")

        elif source_type == "API Esterna (JSON)":
            # Per API, connection_details potrebbe contenere l'URL dell'API
            api_url = connection_details.get("url")
            if not api_url:
                st.error("URL API mancante.")
                return df
            
            response = requests.get(api_url)
            response.raise_for_status() # Lancia un errore per status codes non 2xx
            df = pd.DataFrame(response.json())

        elif source_type == "File CSV (Upload)":
            # Per CSV, connection_details conterrà l'oggetto file uploadato
            uploaded_file = connection_details.get("file")
            if uploaded_file:
                df = pd.read_csv(uploaded_file)
            else:
                st.info("Carica un file CSV.")

        # Qui puoi aggiungere altri tipi di fonti dati (es. PostgreSQL diretto, BigQuery, ecc.)

    except Exception as e:
        st.error(f"Errore nel caricamento dei dati da {source_type}: {e}")
    return df

st.set_page_config(layout="wide", page_title="Dashboard Dati Dinamica")
st.title("Dashboard Dati Dinamica 📊")

# --- Selezione della Fonte Dati ---
st.sidebar.header("Configurazione Fonte Dati")
source_type = st.sidebar.selectbox(
    "Scegli la Fonte Dati:",
    ["Supabase", "API Esterna (JSON)", "File CSV (Upload)", "Seleziona..." ], # Aggiungi "Seleziona..." come opzione predefinita
    index=3 # Imposta l'indice per "Seleziona..."
)

connection_details = {}
if source_type == "Supabase":
    # In una vera app, questi verrebbero da st.secrets o da input dell'utente con password
    connection_details["url"] = st.sidebar.text_input("URL Supabase", type="password")
    connection_details["key"] = st.sidebar.text_input("Anon Key Supabase", type="password")
    connection_details["table_name"] = st.sidebar.text_input("Nome Tabella Supabase", value="your_table_name")
elif source_type == "API Esterna (JSON)":
    connection_details["url"] = st.sidebar.text_input("URL API (JSON)")
elif source_type == "File CSV (Upload)":
    uploaded_file = st.sidebar.file_uploader("Carica un file CSV", type=["csv"])
    connection_details["file"] = uploaded_file

load_button = st.sidebar.button("Carica Dati")

data = pd.DataFrame()
if load_button and source_type != "Seleziona...":
    with st.spinner(f"Caricamento dati da {source_type}..."):
        data = load_data(source_type, connection_details)
    if data.empty:
        st.warning("Impossibile caricare dati o dataset vuoto.")

# --- Visualizzazione Dinamica dei Dati ---
if not data.empty:
    st.write(f"### Dati Caricati ({source_type})")
    st.dataframe(data)

    st.write("---")
    st.write("### Esplorazione e Visualizzazione Dinamica")

    # Ottieni le colonne disponibili
    available_columns = data.columns.tolist()

    if not available_columns:
        st.info("Nessuna colonna trovata per l'analisi.")
    else:
        # Widget per la selezione della colonna X
        x_axis_column = st.selectbox("Seleziona Colonna per Asse X:", available_columns, key="x_axis_select")

        if x_axis_column:
            # Widget per la selezione della colonna Y (se disponibile per grafici numerici)
            numeric_columns = data.select_dtypes(include=['number']).columns.tolist()
            y_axis_column = None
            if numeric_columns:
                y_axis_column = st.selectbox("Seleziona Colonna per Asse Y (numerica):", ["Nessuna"] + numeric_columns, key="y_axis_select")
                if y_axis_column == "Nessuna":
                    y_axis_column = None
            else:
                st.info("Nessuna colonna numerica disponibile per l'asse Y.")

            # Widget per il tipo di grafico
            chart_type = st.selectbox(
                "Seleziona Tipo di Grafico:",
                ["Bar Chart", "Line Chart", "Scatter Plot", "Histogram"],
                key="chart_type_select"
            )

            # Genera il grafico basandosi sulle selezioni
            if chart_type == "Bar Chart" and y_axis_column:
                try:
                    fig = px.bar(data, x=x_axis_column, y=y_axis_column, title=f"{y_axis_column} per {x_axis_column}")
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.warning(f"Impossibile creare Bar Chart: {e}. Controlla i tipi di dato.")
            elif chart_type == "Line Chart" and y_axis_column:
                try:
                    fig = px.line(data.sort_values(by=x_axis_column), x=x_axis_column, y=y_axis_column, title=f"{y_axis_column} su {x_axis_column}")
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.warning(f"Impossibile creare Line Chart: {e}. Assicurati che l'asse X sia ordinabile (es. data/tempo).")
            elif chart_type == "Scatter Plot" and y_axis_column:
                try:
                    fig = px.scatter(data, x=x_axis_column, y=y_axis_column, title=f"Relazione tra {x_axis_column} e {y_axis_column}")
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.warning(f"Impossibile creare Scatter Plot: {e}.")
            elif chart_type == "Histogram":
                try:
                    fig = px.histogram(data, x=x_axis_column, title=f"Distribuzione di {x_axis_column}")
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.warning(f"Impossibile creare Istogramma: {e}. La colonna potrebbe non essere numerica.")
            else:
                st.info("Seleziona le colonne e il tipo di grafico per visualizzare i dati.")

else:
    st.info("Seleziona una fonte dati e clicca 'Carica Dati' per iniziare.")

st.sidebar.markdown("---")
st.sidebar.info("Questa app dimostra come Streamlit può adattarsi a diverse fonti dati dinamicamente.")
