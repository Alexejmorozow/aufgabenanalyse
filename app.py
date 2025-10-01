import streamlit as st
import time

# --- Page config ---
st.set_page_config(page_title="Decision Compass", layout="wide")

# --- Shared definitions for "Aufgaben-Analyse" (disjunktiv / konjunktiv / additiv) ---
TYP_EMOJI = {
    "disjunktiv": "⭐",
    "konjunktiv": "⛓️",
    "additiv": "➕"
}

FARBEN = {
    "light": {
        "disjunktiv": "#E63946",
        "konjunktiv": "#F1FA3C",
        "additiv": "#2A9D8F",
        "background": "#FFFFFF",
        "text": "#000000",
        "box": "#f9f9f9"
    },
    "dark": {
        "disjunktiv": "#FF6B6B",
        "konjunktiv": "#FFD93D",
        "additiv": "#4ECDC4",
        "background": "#121212",
        "text": "#FFFFFF",
        "box": "#1E1E1E"
    }
}

def animated_progress(value, max_value, color, text, speed=0.02):
    """Simple animated progress for visual feedbac k. Note: keep steps small to avoid long block."""
    placeholder = st.empty()
    max_value = max(max_value, 1)
    for i in range(1, value + 1):
        percent = min(i / max_value, 1.0)
        placeholder.progress(percent, text=f"{text}: {i}")
        time.sleep(speed)
    st.markdown(f"<span style='color:{color}; font-weight:bold'>{text}: {value}</span>", unsafe_allow_html=True)


def typ_box(title, bericht, box_color):
    st.markdown(f"""
    <div style='border:2px solid #888888; padding:15px; border-radius:10px; background-color:{box_color}; margin-bottom:15px'>
    <h3>{title}</h3>
    {bericht}
    </div>
    """, unsafe_allow_html=True)

# --- Sidebar / global navigation ---
st.sidebar.title("🧭 Decision Compass")
module = st.sidebar.radio(
    "Wähle ein Modul:",
    [
        "🏠 Start",
        "🔎 Aufgaben-Analyse",
        "📊 SWOT-Analyse",
        "⏳ Eisenhower-Matrix",
        "👥 RACI-Matrix",
        "⚖️ Balanced Scorecard",
    ]
)

# --- START ---
if module == "🏠 Start":
    st.title("🧭 Decision Compass")
    st.write("""
    Willkommen zum Decision Compass! Dieses Tool vereint bewährte Methoden der Entscheidungsfindung unter einem Dach.

    Wähle ein Modul in der linken Leiste und arbeite Schritt für Schritt.
    """)
    st.divider()
    st.subheader("Kurzer Abriss der Module")
    st.markdown(
        """
        - **Aufgaben-Analyse** (disjunktiv / konjunktiv / additiv) – dein originäres Tool, nun als Modul
        - **SWOT** – Stärken, Schwächen, Chancen, Risiken
        - **Eisenhower** – Priorität nach wichtig/urgent
        - **RACI** – Rollen & Verantwortlichkeit
        - **Balanced Scorecard** – Ziele & KPI in vier Perspektiven
        """,
        unsafe_allow_html=True,
    )

# --- AUFGABEN-ANALYSE (dein originärer Fragebogen) ---
elif module == "🔎 Aufgaben-Analyse":
    # Wir integrieren deinen Originalcode, leicht refactored in eine Funktion
    st.title("🔎 Aufgaben-Analyse (Disjunktiv / Konjunktiv / Additiv)")

    # Dark mode toggle
    dark_mode = st.checkbox("🌙 Dark Mode aktivieren", value=False)
    mode = "dark" if dark_mode else "light"
    colors = FARBEN[mode]

    st.markdown(f"""
    <style>
    .stApp {{
        background-color: {colors['background']};
        color: {colors['text']};
    }}
    .css-1d391kg, .css-1d391kg * {{
        color: {colors['text']} !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    st.write("Beantworte 12 kurze Fragen auf einer Skala von 1 bis 7.")

    SCHWELLENWERT_HYBRID = 6

    fragen = [
        {"text": "Je mehr Mitglieder aktiv mitwirken, desto besser – auch kleine Beiträge summieren sich zu einem großen Ergebnis.", "typ": "additiv"},
        {"text": "Wenn auch nur eine Person ihre Aufgabe nicht erfüllt, ist das gesamte Projekt gefährdet.", "typ": "konjunktiv"},
        {"text": "Eine einzelne Spitzenidee oder herausragende Leistung kann den gesamten Projekterfolg sicherstellen.", "typ": "disjunktiv"},
        {"text": "Die Zusammenarbeit scheitert, wenn ein einzelnes Mitglied nicht die nötige Qualität liefert.", "typ": "konjunktiv"},
        {"text": "Erfolg entsteht vor allem durch die Summe vieler Einzelbeiträge, nicht durch einzelne Spitzenleistungen.", "typ": "additiv"},
        {"text": "Die Leistung der besten Person bestimmt weitgehend, ob das Team erfolgreich ist, unabhängig von den anderen.", "typ": "disjunktiv"},
        {"text": "Fehler oder Ausfälle einzelner wirken sich sofort und stark auf den Gesamterfolg aus.", "typ": "konjunktiv"},
        {"text": "Wenn alle gleichmäßig mitwirken, steigt die Wahrscheinlichkeit für einen erfolgreichen Abschluss deutlich.", "typ": "disjunktiv"},
        {"text": "Die Leistung des schwächsten Mitglieds bestimmt maßgeblich, ob das Team sein Ziel erreicht.", "typ": "konjunktiv"},
        {"text": "Jeder Beitrag trägt zum Gesamterfolg bei, aber kein einzelner Ausfall bringt alles zum Scheitern.", "typ": "additiv"},
        {"text": "Auch kleine und regelmäßige Beiträge aller Beteiligten können zusammen zu einem sehr starken Gesamtergebnis führen.", "typ": "additiv"},
        {"text": "Für den Erfolg reicht es, wenn eine Person die Aufgabe vollständig meistert – andere Beiträge sind nicht entscheidend.", "typ": "disjunktiv"},
    ]

    punkte = {"disjunktiv": 0, "konjunktiv": 0, "additiv": 0}

    with st.form("fragen_form"):
        antworten = []
        for i, frage in enumerate(fragen, start=1):
            st.markdown(f"<span style='color:{colors['text']}; font-weight:bold'>{i}. {frage['text']}</span>", unsafe_allow_html=True)
            antwort = st.slider("", min_value=1, max_value=7, value=4, key=f"slider_{i}")
            antworten.append((frage['typ'], antwort))
        submitted = st.form_submit_button("Analyse starten")

    if submitted:
        durchschnitt = sum([antwort for _, antwort in antworten]) / len(antworten)
        if durchschnitt < 2.0:
            st.warning("🎭 Ergebnis: Keine Aufgabe erkannt – Zeit für einen Kaffee ☕")
        else:
            for typ, antwort in antworten:
                punkte[typ] += antwort

            gesamtpunkte = sum(punkte.values())
            prozentuale_verteilung = {typ: round((wert / gesamtpunkte) * 100, 1) for typ, wert in punkte.items()}
            max_punkte = max(punkte.values())

            hybrid_typen = [typ for typ, wert in punkte.items() if max_punkte - wert <= SCHWELLENWERT_HYBRID]

            st.success("✅ Analyse abgeschlossen!")

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📊 Punktestände")
                for typ, wert in punkte.items():
                    animated_progress(value=wert, max_value=7, color=colors[typ], text=f"{TYP_EMOJI[typ]} {typ.capitalize()}")
            with col2:
                st.subheader("📈 Prozentuale Verteilung")
                for typ, prozent in prozentuale_verteilung.items():
                    animated_progress(value=int(prozent), max_value=100, color=colors[typ], text=f"{TYP_EMOJI[typ]} {typ.capitalize()} %", speed=0.01)

            st.divider()
            st.subheader("🎯 Empfehlung")

            typ_name = " + ".join([f"{TYP_EMOJI[typ]} {typ.capitalize()}" for typ in hybrid_typen])
            bericht = ""
            for typ in hybrid_typen:
                if typ == "disjunktiv":
                    bericht += f"""
**Um was für eine Aufgabe handelt es sich?**  
Disjunktiv ⭐: Erfolg hängt von der besten Leistung im Team ab. Nur die stärksten Mitglieder zählen.  

**Stolpersteine:**  
- Schwache Mitglieder vernachlässigt  
- Überlastung der Spitzenkräfte  

**Strategie & Vorgehensweise:**  
- Stärken gezielt fördern  
- Kreativität zulassen, andere unterstützen  
- Kontrolle der Kernleistungen  
- Entscheidungen eher autokratisch
"""
                elif typ == "konjunktiv":
                    bericht += f"""
**Um was für eine Aufgabe handelt es sich?**  
Konjunktiv ⛓️: Erfolg hängt vom schwächsten Glied ab. Die Kette ist nur so stark wie ihr schwächstes Glied.  

**Stolpersteine:**  
- Schwache Mitglieder gefährden den Erfolg  
- Fehlende Kooperation ist kritisch  

**Strategie & Vorgehensweise:**  
- Unterstützung für schwache Mitglieder  
- Intensive Zusammenarbeit, Aufgaben fair verteilen  
- Entscheidungen demokratisch
"""
                elif typ == "additiv":
                    bericht += f"""
**Um was für eine Aufgabe handelt es sich?**  
Additiv ➕: Jeder Beitrag zählt, die Summe entscheidet.  

**Stolpersteine:**  
- Einzelne Beiträge werden unterschätzt  
- Motivation könnte schwanken  

**Strategie & Vorgehensweise:**  
- Alle aktiv einbeziehen  
- Arbeit gleichmäßig verteilen  
- Fortschritte sichtbar machen  
- Motivation hochhalten
"""
            typ_box(typ_name, bericht, colors["box"])

# --- SWOT ---
elif module == "📊 SWOT-Analyse":
    st.title("📊 SWOT-Analyse")
    st.write("Analysiere Stärken, Schwächen, Chancen und Risiken.")

    col1, col2 = st.columns(2)
    with col1:
        staerken = st.text_area("Stärken (Strengths)")
        chancen = st.text_area("Chancen (Opportunities)")
    with col2:
        schwaechen = st.text_area("Schwächen (Weaknesses)")
        risiken = st.text_area("Risiken (Threats)")

    if st.button("Analyse erstellen"):
        st.success("SWOT-Analyse fertig")
        st.write("### Ergebnisse")
        st.write("**Stärken:**", staerken)
        st.write("**Schwächen:**", schwaechen)
        st.write("**Chancen:**", chancen)
        st.write("**Risiken:**", risiken)

        # Einfache 2x2 Matrix als HTML
        st.markdown(
            f"""
            <div style='display:grid; grid-template-columns:1fr 1fr; gap:10px'>
              <div style='border:1px solid #ddd; padding:10px'><h4>Stärken</h4><div>{staerken.replace('
','<br>')}</div></div>
              <div style='border:1px solid #ddd; padding:10px'><h4>Schwächen</h4><div>{schwaechen.replace('
','<br>')}</div></div>
              <div style='border:1px solid #ddd; padding:10px'><h4>Chancen</h4><div>{chancen.replace('
','<br>')}</div></div>
              <div style='border:1px solid #ddd; padding:10px'><h4>Risiken</h4><div>{risiken.replace('
','<br>')}</div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# --- EISENHOWER ---
elif module == "⏳ Eisenhower-Matrix":
    st.title("⏳ Eisenhower-Matrix")
    st.write("Priorisiere Aufgaben nach Wichtigkeit und Dringlichkeit.")

    if 'tasks' not in st.session_state:
        st.session_state.tasks = []

    with st.form("task_form"):
        t_name = st.text_input("Aufgabe")
        t_wichtig = st.radio("Wichtigkeit", ["hoch", "mittel", "niedrig"], index=1)
        t_dringend = st.checkbox("dringend")
        add = st.form_submit_button("Aufgabe anlegen")
        if add and t_name:
            st.session_state.tasks.append({"name": t_name, "wichtig": t_wichtig, "dringend": t_dringend})

    if st.session_state.tasks:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Quadrant: Sofort tun (wichtig + dringend)")
            for t in st.session_state.tasks:
                if (t['wichtig'] == 'hoch') and t['dringend']:
                    st.write(f"- {t['name']}")
        with col2:
            st.subheader("Quadrant: Planen (wichtig, nicht dringend)")
            for t in st.session_state.tasks:
                if (t['wichtig'] == 'hoch') and (not t['dringend']):
                    st.write(f"- {t['name']}")
        st.divider()
        col3, col4 = st.columns(2)
        with col3:
            st.subheader("Quadrant: Delegieren (nicht wichtig, dringend)")
            for t in st.session_state.tasks:
                if (t['wichtig'] != 'hoch') and t['dringend']:
                    st.write(f"- {t['name']}")
        with col4:
            st.subheader("Quadrant: Eliminieren (nicht wichtig, nicht dringend)")
            for t in st.session_state.tasks:
                if (t['wichtig'] != 'hoch') and (not t['dringend']):
                    st.write(f"- {t['name']}")

# --- RACI ---
elif module == "👥 RACI-Matrix":
    st.title("👥 RACI-Matrix")
    st.write("Definiere Rollen für Aufgaben: Responsible, Accountable, Consulted, Informed")

    aufgabenliste = st.text_area("Aufgaben (eine pro Zeile)")
    team = st.text_area("Teammitglieder (eine pro Zeile)")

    if st.button("Matrix generieren"):
        aufgaben = [a.strip() for a in aufgabenliste.splitlines() if a.strip()]
        mitglieder = [m.strip() for m in team.splitlines() if m.strip()]
        if not aufgaben or not mitglieder:
            st.warning("Bitte Aufgaben und Team eintragen")
        else:
            # Einfache interaktive Tabelle: nutzer wählt für jede Aufgabe pro rolle eine Person
            st.write("### Matrix")
            cols = st.columns(len(mitglieder) + 1)
            cols[0].write("Aufgabe")
            for i, m in enumerate(mitglieder, start=1):
                cols[i].write(m)
            for a in aufgaben:
                row = []
                row.append(a)
                cols = st.columns(len(mitglieder) + 1)
                cols[0].write(a)
                for i, m in enumerate(mitglieder, start=1):
                    val = cols[i].selectbox(f"{a}-{m}", ["-", "R", "A", "C", "I"], key=f"{a}-{m}")

# --- BALANCED SCORECARD ---
elif module == "⚖️ Balanced Scorecard":
    st.title("⚖️ Balanced Scorecard")
    st.write("Ziele & KPI in vier Perspektiven definieren")

    perspektiven = ["Finanzen", "Kunden", "Prozesse", "Lernen & Entwicklung"]
    kpi_data = {}
    for p in perspektiven:
        st.subheader(p)
        ziele = st.text_area(f"Ziele für {p}", key=f"ziel_{p}")
        kpis = st.text_area(f"KPI für {p} (eine pro Zeile)", key=f"kpi_{p}")
        kpi_data[p] = {"ziele": ziele, "kpis": kpis}

    if st.button("Scorecard speichern"):
        st.success("Scorecard erfasst")
        st.write(kpi_data)

# --- Footer mit next step hint ---
st.markdown("---")
st.write("Hinweis: Das ist ein Grundgerüst. Gern baue ich Export, MultiUser, Auth oder Team-Mode ein.")
