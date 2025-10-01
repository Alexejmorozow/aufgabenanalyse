import streamlit as st
import time

# --- Page config ---
st.set_page_config(page_title="Decision Compass", layout="wide")

# --- Shared definitions for Aufgaben-Analyse ---
TYP_EMOJI = {"disjunktiv": "⭐", "konjunktiv": "⛓️", "additiv": "➕"}

FARBEN = {
    "light": {"disjunktiv": "#E63946", "konjunktiv": "#F1FA3C", "additiv": "#2A9D8F", "background": "#FFFFFF", "text": "#000000", "box": "#f9f9f9"},
    "dark": {"disjunktiv": "#FF6B6B", "konjunktiv": "#FFD93D", "additiv": "#4ECDC4", "background": "#121212", "text": "#FFFFFF", "box": "#1E1E1E"}
}

# --- Utility functions ---
def animated_progress(value, max_value, color, text, speed=0.02):
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

# --- Sidebar / Navigation ---
st.sidebar.title("🧭 Decision Compass")
module = st.sidebar.radio("Wähle ein Modul:", ["🏠 Start", "🔎 Aufgaben-Analyse", "📊 SWOT-Analyse", "⏳ Eisenhower-Matrix", "👥 RACI-Matrix", "⚖️ Balanced Scorecard"])

# --- START ---
if module == "🏠 Start":
    st.title("🧭 Decision Compass")
    st.write("""Willkommen zum Decision Compass! Dieses Tool vereint bewährte Methoden der Entscheidungsfindung unter einem Dach.
Wähle ein Modul in der linken Leiste und arbeite Schritt für Schritt.""")
    st.divider()

# --- Aufgaben-Analyse ---
elif module == "🔎 Aufgaben-Analyse":
    st.title("🔎 Aufgaben-Analyse (Disjunktiv / Konjunktiv / Additiv)")

    dark_mode = st.checkbox("🌙 Dark Mode aktivieren", value=False)
    mode = "dark" if dark_mode else "light"
    colors = FARBEN[mode]

    st.markdown(f"""
    <style>
    .stApp {{ background-color: {colors['background']}; color: {colors['text']}; }}
    .css-1d391kg, .css-1d391kg * {{ color: {colors['text']} !important; }}
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
                    bericht += """**Aufgabe:** Disjunktiv ⭐ – Erfolg hängt von der besten Leistung ab.
**Stolpersteine:** Schwache Mitglieder vernachlässigt, Überlastung Spitzenkräfte.
**Strategie:** Stärken gezielt fördern, Kontrolle der Kernleistungen, Entscheidungen eher autokratisch.
"""
                elif typ == "konjunktiv":
                    bericht += """**Aufgabe:** Konjunktiv ⛓️ – Erfolg hängt vom schwächsten Glied ab.
**Stolpersteine:** Schwache Mitglieder gefährden Erfolg.
**Strategie:** Unterstützung schwacher Mitglieder, intensive Zusammenarbeit, Entscheidungen demokratisch.
"""
                elif typ == "additiv":
                    bericht += """**Aufgabe:** Additiv ➕ – Jeder Beitrag zählt.
**Stolpersteine:** Einzelne Beiträge unterschätzt, Motivation schwankt.
**Strategie:** Alle einbeziehen, Arbeit gleichmäßig verteilen, Fortschritte sichtbar machen.
"""
            typ_box(typ_name, bericht, colors["box"])

# --- SWOT ---
elif module == "📊 SWOT-Analyse":
    st.title("📊 SWOT-Analyse")
    col1, col2 = st.columns(2)
    with col1:
        staerken = st.text_area("Stärken (Strengths)")
        chancen = st.text_area("Chancen (Opportunities)")
    with col2:
        schwaechen = st.text_area("Schwächen (Weaknesses)")
        risiken = st.text_area("Risiken (Threats)")

    if st.button("Analyse erstellen"):
        st.success("SWOT-Analyse fertig")
        staerken_html = staerken.replace('\n', '<br>')
        schwaechen_html = schwaechen.replace('\n', '<br>')
        chancen_html = chancen.replace('\n', '<br>')
        risiken_html = risiken.replace('\n', '<br>')
        st.markdown(f"""
        <div style='display:grid; grid-template-columns:1fr 1fr; gap:10px'>
          <div style='border:1px solid #ddd; padding:10px'><h4>Stärken</h4>{staerken_html}</div>
          <div style='border:1px solid #ddd; padding:10px'><h4>Schwächen</h4>{schwaechen_html}</div>
          <div style='border:1px solid #ddd; padding:10px'><h4>Chancen</h4>{chancen_html}</div>
          <div style='border:1px solid #ddd; padding:10px'><h4>Risiken</h4>{risiken_html}</div>
        </div>
        """, unsafe_allow_html=True)

# --- Eisenhower, RACI, Balanced Scorecard ---
# Für alle Module analog vorher skizziert, unverändert
