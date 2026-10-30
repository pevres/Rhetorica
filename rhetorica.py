import streamlit as st
import json
from google import genai
from google.genai import types

# Configurazione della pagina Streamlit (ottimizzata per l'uso su smartphone)
st.set_page_config(
    page_title="Rhetorica - AI Political Speech Coach",
    page_icon="🎙️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Stile CSS avanzato per ottimizzare l'esperienza touch e mobile
st.markdown(
    """
    <style>
    .main { background-color: #0F172A; color: #F8FAFC; }
    .card { 
        background-color: #1E293B; 
        padding: 16px; 
        border-radius: 16px; 
        border: 1px solid #334155; 
        margin-bottom: 16px; 
    }
    .stButton>button { 
        background-color: #F59E0B; 
        color: #0F172A; 
        font-weight: bold; 
        border-radius: 12px; 
        border: none; 
        width: 100%; 
        padding: 14px; 
        font-size: 16px;
    }
    .stButton>button:hover { 
        background-color: #D97706; 
        color: #FFFFFF; 
    }
    input, textarea, select {
        border-radius: 10px !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- CONFIGURAZIONE CHIAVE API DA STREAMLIT SECRETS E CONTESTO NELLA SIDEBAR ---
st.sidebar.title("🎙️ Rhetorica - Config")

active_api_key = None

try:
    if "GEMINI_API_KEY" in st.secrets:
        active_api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

if active_api_key:
    st.sidebar.success("Stato API: Connesso via Secrets 🟢")
else:
    st.sidebar.error("Stato API: Chiave non trovata nei Secrets 🔴")
    st.sidebar.info("Configura 'GEMINI_API_KEY' nelle impostazioni di Streamlit Cloud (Settings -> Secrets).")

st.sidebar.markdown("---")
st.sidebar.subheader("🌍 Contesto Territoriale")
territorio_corrente = st.sidebar.text_input(
    "Comune / Area di Riferimento:",
    value="Aviano (PN)",
    help="Modifica questo campo per adattare l'intera app a qualsiasi altro comune o territorio."
)

st.sidebar.markdown("---")
st.sidebar.subheader("🧠 Metodo di Lavoro AI")
modalita_logica = st.sidebar.radio(
    "Scegli l'approccio strategico:",
    ["George Lakoff (Framing & Valori)", "Standard Gemini (Dati & Tecnica)"]
)

st.sidebar.markdown("---")
menu = st.sidebar.radio(
    "Navigazione",
    [
        "📊 Dashboard",
        "🎯 Simulatore Intervista Ostile",
        "⚔️ Dibattito TV a Tre Vie",
        "👥 Roleplay Porta a Porta",
        "🏛️ Simulatore Consiglio / Assemblea",
        "📄 Analizzatore PDF & Programmi",
        "🎤 Voice Coach (Audio)",
        "🚪 Door-to-Door Toolkit (Flash)",
        "✍️ Copywriting Lab",
        "🔍 Fact-Check Avversari",
        "📱 Social Media Kit",
        "🚨 Crisis Room",
        "📈 Storico Sessioni Attive",
    ],
)

if "history" not in st.session_state:
    st.session_state.history = []

if "porta_porta_messages" not in st.session_state:
    st.session_state.porta_porta_messages = []

def get_full_gemini_response(prompt_text, additional_parts=None):
    if not active_api_key:
        return "⚠️ Attenzione: Chiave API di Google Gemini non configurata nei Secrets di Streamlit."
    try:
        client = genai.Client(api_key=active_api_key)
        contents = [prompt_text]
        if additional_parts:
            if isinstance(additional_parts, list):
                contents.extend(additional_parts)
            else:
                contents.append(additional_parts)
            
        # Configurazione con temperatura bilanciata e limite token a 4096
        config = types.GenerateContentConfig(
            temperature=0.3,
            max_output_tokens=4096,
        )

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=contents,
            config=config,
        )
        return response.text
    except Exception as e:
        return f"Errore di connessione all'API di Gemini: {str(e)}"

# Definizione delle direttive di sistema in base alle scelte nella sidebar
if modalita_logica == "George Lakoff (Framing & Valori)":
    istruzioni_strategiche = f"Agisci rigorosamente come un esperto di linguistica cognitiva e framing alla George Lakoff per il contesto territoriale di {territorio_corrente}. Focalizzati sui valori morali profondi, sui frame positivi, sul rifiuto del linguaggio avversario e sulle cornici emotive."
    etichetta_metodo = "George Lakoff 🧠"
else:
    istruzioni_strategiche = f"Agisci come un consulente di comunicazione politica standard per il contesto territoriale di {territorio_corrente}. Focalizzati su dati fattuali, risposte tecniche, logica razionale e argomentazioni amministrative puntuali."
    etichetta_metodo = "Standard Gemini 📊"

# --- SEZIONE 1: DASHBOARD ---
if menu == "📊 Dashboard":
    st.title("🎙️ Rhetorica")
    st.markdown(f"**Suite Avanzata di Comunicazione Politica • Territorio: {territorio_corrente}**")

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Rhetoric Score", value="94/100", delta="+18%")
    with col2:
        st.metric(label="Modalità Attiva", value=etichetta_metodo)

    st.markdown("---")
    st.info(f"Suite Completa attiva nel contesto di **{territorio_corrente}** con approccio **{modalita_logica}**.")

# --- SEZIONE 2: INTERVISTA OSTILE ---
elif menu == "🎯 Simulatore Intervista Ostile":
    st.title("🎯 Intervista Ostile")
    st.markdown(f"Mettiti alla prova *(Territorio: {territorio_corrente} | Metodo: {etichetta_metodo})*.")

    scenario = st.text_input("Argomento dell'intervista:", value=f"Sicurezza urbana e quartieri a {territorio_corrente}")
    domanda_utente = st.text_area("La tua risposta verbale:")

    if st.button("Valuta la risposta"):
        if not domanda_utente:
            st.warning("Scrivi prima una risposta.")
        else:
            prompt = f"""
            {istruzioni_strategiche}
            Contesto politico: {territorio_corrente}. Tema: '{scenario}'. 
            Risposta fornita dall'utente: "{domanda_utente}"
            Fornisci un punteggio da 1 a 100, analisi dettagliata e suggerimenti pratici.
            """
            st.markdown("### Analisi in tempo reale:")
            with st.spinner("Elaborazione in corso..."):
                risposta_ai = get_full_gemini_response(prompt)
            st.markdown(risposta_ai)

            st.session_state.history.append({
                "tipo": f"Intervista Ostile ({territorio_corrente})", 
                "dettaglio": scenario,
                "input_utente": domanda_utente,
                "risultato_ai": risposta_ai
            })

# --- SEZIONE 3: DIBATTITO TV ---
elif menu == "⚔️ Dibattito TV a Tre Vie":
    st.title("⚔️ Dibattito TV a Tre Vie")
    st.markdown(f"Affronta moderatore e avversario *(Territorio: {territorio_corrente})*.")

    tema_dibattito = st.text_input("Tema del confronto TV:", value=f"Sviluppo economico e servizi locali a {territorio_corrente}")
    attacco_avversario = st.text_area("Cosa ti ha detto l'avversario politico?:", value="La vostra amministrazione ha ignorato le reali necessità.")
    tua_replica = st.text_area("La tua replica immediata:")

    if st.button("Simula e valuta il dibattito"):
        if not tua_replica:
            st.warning("Inserisci la tua replica.")
        else:
            prompt = f"""
            {istruzioni_strategiche}
            Moderatore di dibattito a {territorio_corrente}. Tema: '{tema_dibattito}'. 
            Attacco: '{attacco_avversario}'. Replica: '{tua_replica}'.
            Fornisci reazione dello studio, valutazione strategica e consigli di chiusura.
            """
            st.markdown("### Analisi del Dibattito:")
            with st.spinner("Lo studio sta reagendo..."):
                risposta_ai = get_full_gemini_response(prompt)
            st.markdown(risposta_ai)

            st.session_state.history.append({
                "tipo": f"Dibattito a Tre Vie ({territorio_corrente})", 
                "dettaglio": tema_dibattito,
                "input_utente": tua_replica,
                "risultato_ai": risposta_ai
            })

# --- SEZIONE 4: ROLEPLAY PORTA A PORTA ---
elif menu == "👥 Roleplay Porta a Porta":
    st.title("👥 Roleplay Porta a Porta")
    st.markdown(f"Dialoga con un cittadino a {territorio_corrente}.")

    profilo_cittadino = st.selectbox(
        "Tipo di cittadino:",
        ["Cittadino scettico / disilluso", "Cittadino arrabbiato per i disservizi", "Cittadino anziano preoccupato per la sicurezza", "Commerciante locale in difficoltà"]
    )

    if st.button("Avvia / Reset Simulazione") or not st.session_state.porta_porta_messages:
        prompt_iniziale = f"""
        {istruzioni_strategiche}
        Inizia una simulazione porta a porta a {territorio_corrente}. Interpreti un {profilo_cittadino}. Apri la porta e pronuncia una prima obiezione.
        """
        with st.spinner("Il cittadino apre la porta..."):
            prima_battuta = get_full_gemini_response(prompt_iniziale)
        st.session_state.porta_porta_messages = [{"role": "model", "content": prima_battuta}]

    for msg in st.session_state.porta_porta_messages:
        if msg["role"] == "model":
            st.info(f"🏠 Cittadino ({profilo_cittadino}):\n\n{msg['content']}")
        else:
            st.success(f"👤 Tu (Candidato):\n\n{msg['content']}")

    risposta_candidato = st.text_input("La tua risposta al cittadino:", key="input_porta_porta")
    if st.button("Rispondi al Cittadino"):
        if risposta_candidato:
            st.session_state.porta_porta_messages.append({"role": "user", "content": risposta_candidato})
            storico_chat = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.porta_porta_messages])
            prompt_continuazione = f"""
            {istruzioni_strategiche}
            Conversazione porta a porta a {territorio_corrente}. Storico:
            {storico_chat}
            Fai proseguire il cittadino reagendo e dai un breve consiglio strategico finale.
            """
            with st.spinner("Il cittadino risponde..."):
                risposta_ai = get_full_gemini_response(prompt_continuazione)
            st.session_state.porta_porta_messages.append({"role": "model", "content": risposta_ai})
            st.rerun()

    if st.button("Salva sessione nello Storico"):
        st.session_state.history.append({
            "tipo": f"Roleplay Porta a Porta ({territorio_corrente})",
            "dettaglio": profilo_cittadino,
            "risultato_ai": json.dumps(st.session_state.porta_porta_messages, ensure_ascii=False)
        })
        st.success("Salvato!")

# --- SEZIONE 5: CONSIGLIO COMUNALE ---
elif menu == "🏛️ Simulatore Consiglio / Assemblea":
    st.title("🏛️ Simulatore Assemblea Pubblica")
    st.markdown(f"Affronta una sala affollata a {territorio_corrente}.")

    clima_sala = st.selectbox("Clima della sala:", ["Teso e polemico", "Freddo e scettico", "Partecipativo ma esigente"])
    intervento_apertura = st.text_area("Il tuo intervento d'apertura:", value="Buonasera a tutti, illustriamo il piano di risanamento del territorio.")

    if st.button("Scatena la Reazione della Sala"):
        if not intervento_apertura:
            st.warning("Inserisci l'intervento.")
        else:
            prompt = f"""
            {istruzioni_strategiche}
            Assemblea pubblica a {territorio_corrente}. Clima: '{clima_sala}'. Intervento: "{intervento_apertura}"
            Simula reazione della sala/opposizione, punti critici e protocollo di reframing.
            """
            st.markdown("### Reazione e Protocollo:")
            with st.spinner("La sala reagisce..."):
                risposta_ai = get_full_gemini_response(prompt)
            st.markdown(risposta_ai)

            st.session_state.history.append({
                "tipo": f"Simulatore Assemblea ({territorio_corrente})",
                "dettaglio": f"Clima: {clima_sala}",
                "input_utente": intervento_apertura,
                "risultato_ai": risposta_ai
            })

# --- SEZIONE 6: ANALIZZATORE PDF ---
elif menu == "📄 Analizzatore PDF & Programmi":
    st.title("📄 Analizzatore PDF")
    st.markdown(f"Analizza documenti a {territorio_corrente}.")

    pdf_file = st.file_uploader("Carica documento PDF:", type=["pdf"])
    obiettivo_analisi = st.text_input("Cosa vuoi cercare nel documento?", value="Trova promesse deboli o criticità")

    if st.button("Analizza Documento"):
        if not pdf_file:
            st.warning("Carica un PDF.")
        else:
            pdf_bytes = pdf_file.getvalue()
            prompt_pdf = f"""
            {istruzioni_strategiche}
            Analizza il PDF per {territorio_corrente}. Obiettivo: '{obiettivo_analisi}'.
            Fornisci riassunto esecutivo, criticità e suggerimenti strategici.
            """
            st.markdown("### Report PDF:")
            with st.spinner("Analisi PDF..."):
                file_part = types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf")
                risposta_ai = get_full_gemini_response(prompt_pdf, additional_parts=file_part)
            st.markdown(risposta_ai)

            st.session_state.history.append({
                "tipo": f"Analisi PDF ({territorio_corrente})",
                "dettaglio": obiettivo_analisi,
                "risultato_ai": risposta_ai
            })

# --- SEZIONE 7: VOICE COACH ---
elif menu == "🎤 Voice Coach (Audio)":
    st.title("🎤 Analizzatore Audio")
    st.markdown(f"Carica un file audio *(Territorio: {territorio_corrente})*.")

    audio_file = st.file_uploader("Carica audio (mp3, wav, aac, m4a):", type=["mp3", "wav", "aac", "m4a"])
    contesto_audio = st.text_input("Descrizione discorso:", value=f"Comizio a {territorio_corrente}")

    if st.button("Analizza Audio"):
        if not audio_file:
            st.warning("Carica un file audio.")
        else:
            bytes_data = audio_file.getvalue()
            prompt_audio = f"""
            {istruzioni_strategiche}
            Analizza audio per {territorio_corrente}. Contesto: '{contesto_audio}'.
            Valuta tono, ritmo e dai 3 consigli pratici.
            """
            st.markdown("### Report Audio:")
            with st.spinner("Analisi audio..."):
                file_part = types.Part.from_bytes(data=bytes_data, mime_type=audio_file.type)
                risposta_ai = get_full_gemini_response(prompt_audio, additional_parts=file_part)
            st.markdown(risposta_ai)

            st.session_state.history.append({
                "tipo": f"Voice Coach Audio ({territorio_corrente})", 
                "dettaglio": contesto_audio,
                "risultato_ai": risposta_ai
            })

# --- SEZIONE 8: DOOR TO DOOR TOOLKIT ---
elif menu == "🚪 Door-to-Door Toolkit (Flash)":
    st.title("🚪 Kit Porta a Porta (Flash)")
    st.markdown(f"Risposte flash *(Territorio: {territorio_corrente})*.")

    problema_cittadino = st.text_input("Cosa lamenta il cittadino?:", value="Parcheggi e illuminazione")

    if st.button("Genera Argomenti Flash"):
        prompt = f"""
        {istruzioni_strategiche}
        Problema a {territorio_corrente}: '{problema_cittadino}'.
        Crea scheda militanti: 1. Ascolto, 2. Soluzione, 3. Chiusura a effetto.
        """
        st.markdown("### Scheda Militanti:")
        with st.spinner("Generazione..."):
            risposta_ai = get_full_gemini_response(prompt)
        st.markdown(risposta_ai)

        st.session_state.history.append({
            "tipo": f"Door-to-Door Toolkit ({territorio_corrente})", 
            "dettaglio": problema_cittadino,
            "risultato_ai": risposta_ai
        })

# --- SEZIONE 9: COPYWRITING ---
elif menu == "✍️ Copywriting Lab":
    st.title("✍️ Copywriting Lab")
    st.markdown(f"Slogan e messaggi *(Territorio: {territorio_corrente})*.")

    concetto = st.text_input("Problema o proposta:", value=f"Riqualificazione a {territorio_corrente}")

    if st.button("Genera Contenuto"):
        prompt = f"""
        {istruzioni_strategiche}
        Concetto: '{concetto}' ({territorio_corrente}). Genera 3 varianti di slogan.
        """
        st.markdown("### Risultati:")
        with st.spinner("Generazione..."):
            risposta_ai = get_full_gemini_response(prompt)
        st.markdown(risposta_ai)

        st.session_state.history.append({
            "tipo": f"Copywriting ({territorio_corrente})", 
            "dettaglio": concetto,
            "risultato_ai": risposta_ai
        })

# --- SEZIONE 10: FACT CHECK ---
elif menu == "🔍 Fact-Check Avversari":
    st.title("🔍 Fact-Check")
    st.markdown(f"Smonta dichiarazioni avversarie *(Territorio: {territorio_corrente})*.")

    dichiarazione = st.text_area("Incolla dichiarazione avversaria:")

    if st.button("Analizza e Confuta"):
        if not dichiarazione:
            st.warning("Incolla una dichiarazione.")
        else:
            prompt = f"""
            {istruzioni_strategiche}
            Analizza dichiarazione a {territorio_corrente}: "{dichiarazione}"
            Fornisci punti deboli e argomenti per confutarla.
            """
            st.markdown("### Risultato Fact-Check:")
            with st.spinner("Analisi..."):
                risposta_ai = get_full_gemini_response(prompt)
            st.markdown(risposta_ai)

            st.session_state.history.append({
                "tipo": f"Fact-Check ({territorio_corrente})", 
                "dettaglio": dichiarazione[:30] + "...",
                "risultato_ai": risposta_ai
            })

# --- SEZIONE 11: SOCIAL MEDIA KIT ---
elif menu == "📱 Social Media Kit":
    st.title("📱 Social Media Kit")
    st.markdown(f"Strategia social *(Territorio: {territorio_corrente})*.")

    tema_social = st.text_input("Argomento post:", value=f"Vivibilità a {territorio_corrente}")

    if st.button("Genera Kit Social"):
        prompt = f"""
        {istruzioni_strategiche}
        Argomento: '{tema_social}' ({territorio_corrente}). Crea post FB, thread X e script video.
        """
        st.markdown("### Kit Social:")
        with st.spinner("Redazione..."):
            risposta_ai = get_full_gemini_response(prompt)
        st.markdown(risposta_ai)

        st.session_state.history.append({
            "tipo": f"Social Kit ({territorio_corrente})", 
            "dettaglio": tema_social,
            "risultato_ai": risposta_ai
        })

# --- SEZIONE 12: CRISIS ROOM ---
elif menu == "🚨 Crisis Room":
    st.title("🚨 Crisis Room")
    st.markdown(f"Gestione emergenze *(Territorio: {territorio_corrente})*.")

    crisi_tipo = st.selectbox("Scenario di crisi:", ["Polemica social", "Emergenza territorio", "Gaffe stampa"])
    dettaglio_crisi = st.text_area(f"Descrivi l'accaduto a {territorio_corrente}:")

    if st.button("Genera Protocollo di Crisi"):
        if not dettaglio_crisi:
            st.warning("Inserisci i dettagli.")
        else:
            prompt = f"""
            {istruzioni_strategiche}
            Crisi a {territorio_corrente}: '{crisi_tipo}'. Dettagli: '{dettaglio_crisi}'.
            Fornisci azioni immediate, bozza comunicato e linee guida.
            """
            st.markdown("### Protocollo di Crisi:")
            with st.spinner("Elaborazione..."):
                risposta_ai = get_full_gemini_response(prompt)
            st.markdown(risposta_ai)

            st.session_state.history.append({
                "tipo": f"Crisis Room ({territorio_corrente})", 
                "dettaglio": crisi_tipo,
                "risultato_ai": risposta_ai
            })

# --- SEZIONE 13: STORICO SESSIONI ATTIVE ---
elif menu == "📈 Storico Sessioni Attive":
    st.title("📈 Storico Attività")
    
    data_to_export = st.session_state.history if st.session_state.history else []
    history_json = json.dumps(data_to_export, ensure_ascii=False, indent=4)

    def genera_markdown_storico(history_data):
        md_content = "# Rhetorica - Storico Sessioni Attive\n\n"
        for idx, item in enumerate(history_data):
            session_num = len(history_data) - idx
            tipo = str(item.get('tipo', ''))
            dettaglio = str(item.get('dettaglio', ''))
            risultato = str(item.get('risultato_ai', ''))

            md_content += f"## #{session_num} - {tipo}\n"
            md_content += f"**Tema/Dettaglio:** {dettaglio}\n\n"
            md_content += f"**Risultato AI:**\n{risultato}\n\n"
            md_content += "---\n\n"
        return md_content

    col_btn1, col_btn2, col_btn3 = st.columns(3)
    
    with col_btn1:
        st.download_button(
            label="📥 Scarica JSON",
            data=history_json,
            file_name="rhetorica_storico.json",
            mime="application/json"
        )

    with col_btn2:
        if st.session_state.history:
            markdown_bytes = genera_markdown_storico(st.session_state.history).encode('utf-8')
            st.download_button(
                label="📄 Scarica Report (MD)",
                data=markdown_bytes,
                file_name="rhetorica_storico.md",
                mime="text/markdown"
            )
        else:
            st.button("📄 Scarica Report (MD)", disabled=True)
            
    with col_btn3:
        if st.session_state.history and st.button("🗑️ Svuota"):
            st.session_state.history = []
            st.session_state.porta_porta_messages = []
            st.rerun()

    st.markdown("---")

    if not st.session_state.history:
        st.info("Nessuna sessione attiva registrata.")
    else:
        for idx, item in enumerate(reversed(st.session_state.history)):
            session_num = len(st.session_state.history) - idx
            with st.expander(f"🟢 #{session_num} — {item['tipo']} (Tema: {item['dettaglio']})"):
                st.markdown(item.get('risultato_ai', 'Nessun testo salvato.'))
