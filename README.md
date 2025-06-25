# Demo: `streamlit hello` as a native multipage app

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/streamlit/docs/main/python/api-examples-source/mpa-hello/Hello.py)

This project highlights Streamlit's new multipage app functionality. 

![In-use Animation](https://github.com/streamlit/hello/blob/main/mpa-hero.gif?raw=true "In-use Animation")


## How to run this demo
The demo can be accessed via Streamlit Community Cloud [here](https://share.streamlit.io/streamlit/docs/main/python/api-examples-source/mpa-hello/Hello.py) or locally via the following steps:

```
pip install streamlit
streamlit hello
```

## Learn more 

- [Documentation](https://docs.streamlit.io/library/get-started/multipage-apps)
- [Blog post](https://blog.streamlit.io/introducing-multipage-apps/)

## Questions? Comments?

Please ask in the [community forum](https://discuss.streamlit.io).

## API pubbliche di test

Ecco alcune URL di API pubbliche, gratuite e senza autenticazione (o con autenticazione molto semplice/opzionale) che sono perfette per scopi di testing:

### 1. JSONPlaceholder (Consigliatissimo per iniziare)
È una **fake REST API gratuita e affidabile** per test e prototipazione. Offre dati strutturati (post, commenti, utenti, foto, ecc.) e supporta tutti i metodi HTTP (GET, POST, PUT, DELETE).

* **Endpoint di esempio (GET):**
    * **Posts:** `https://jsonplaceholder.typicode.com/posts`
    * **Comments:** `https://jsonplaceholder.typicode.com/comments`
    * **Users:** `https://jsonplaceholder.typicode.com/users`
    * **Photos:** `https://jsonplaceholder.typicode.com/photos` (questo ha molti dati, ottimo per testare la gestione di dataset più grandi)

* **Vantaggi:** Molto stabile, non richiede chiavi API, dati ben strutturati e predicibili. È la scelta di default per molti tutorial e prototipi.
* **Per il tuo caso:** Puoi semplicemente inserire l'URL di uno di questi endpoint nel campo "URL API (JSON)" della tua app Streamlit.

### 2. DummyJSON
Simile a JSONPlaceholder, ma offre una maggiore varietà di dati fake, inclusi prodotti, carrelli, utenti, post, commenti, ecc.

* **Endpoint di esempio (GET):**
    * **Products:** `https://dummyjson.com/products`
    * **Users:** `https://dummyjson.com/users`
    * **Posts:** `https://dummyjson.com/posts`
* **Vantaggi:** Dati fake vari e utili per simulare scenari di e-commerce o social media.

### 3. CoinDesk API (Bitcoin Price Index)
Se vuoi dati numerici e di serie temporali, il Bitcoin Price Index di CoinDesk è un'ottima scelta.

* **Endpoint di esempio (GET):**
    * **Current Price Index:** `https://api.coindesk.com/v1/bpi/currentprice.json`
    * **Historical Data (ultimi 31 giorni):** `https://api.coindesk.com/v1/bpi/history/latest.json`
* **Vantaggi:** Dati reali e aggiornati, buoni per testare grafici di serie temporali.

### 4. REST Countries API
Un'API molto utile per ottenere informazioni sui paesi.

* **Endpoint di esempio (GET):**
    * **Tutti i paesi:** `https://restcountries.com/v3.1/all` (Questo è un dataset molto grande!)
    * **Paese per nome (es. Italy):** `https://restcountries.com/v3.1/name/italy`
* **Vantaggi:** Dati geografici e statistici interessanti, con molte colonne diverse.

### 5. PokeAPI
Se sei un fan dei Pokémon, questa API offre una vasta gamma di dati su Pokémon, abilità, mosse, ecc.

* **Endpoint di esempio (GET):**
    * **Lista Pokémon (offset 0, limite 20):** `https://pokeapi.co/api/v2/pokemon?offset=0&limit=20`
* **Vantaggi:** Dataset gerarchico, ottimo per esplorare dati complessi.

### 6. Random User Generator API
Genera dati di utenti fittizi, perfetti per popolare interfacce utente o testare scenari con dati di persone.

* **Endpoint di esempio (GET):**
    * **Un utente casuale:** `https://randomuser.me/api/`
    * **Più utenti (es. 5):** `https://randomuser.me/api/?results=5`
* **Vantaggi:** Genera dati di persone (nomi, indirizzi, foto, ecc.), utili per dashboard che mostrano profili utente.

### 7. Open-Meteo
Fornisce dati meteo aperti e gratuiti. Richiede di specificare latitudine e longitudine.

* **Endpoint di esempio (GET) (Brescia, Italia):**
    * `https://api.open-meteo.com/v1/forecast?latitude=45.5416&longitude=10.2117&current_weather=true&hourly=temperature_2m,relative_humidity_2m`
    * **Vantaggi:** Dati meteo reali, ottimi per testare grafici a linee o tabelle di previsioni. Richiede un po' più di configurazione lato client per le query.

---

**Consiglio per la tua app Streamlit:**

Inizia con **JSONPlaceholder** o **DummyJSON** per l'opzione "API Esterna (JSON)" nel tuo selettore. Sono i più semplici da integrare e forniscono dati puliti che si prestano bene all'analisi.

Ricorda che la tua funzione `load_data` dovrebbe essere in grado di gestire le diverse strutture JSON che queste API possono restituire. `pandas.DataFrame(response.json())` funziona bene per API che restituiscono un array di oggetti JSON, ma per API che hanno dati annidati (come CoinDesk o Random User), potresti dover fare un po' di "appiattimento" (`pd.json_normalize`) o estrarre solo la parte relevante del JSON prima di convertirla in DataFrame.
