import streamlit as st
import time

# --- Emojis pro Typ ---
TYP_EMOJI = {
    "disjunktiv": "⭐",
    "konjunktiv": "⛓️",
    "additiv": "➕"
}

# --- Farbdefinitionen für Light/Dark Mode ---
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

# --- Progress Bar Funktion ---
def animated_progress(value, max_value, color, text, speed=0.02):
    placeholder = st.empty()
    max_value = max(max_value, 1)
    for i in range(1, value + 1):
        percent = min(i / max_value, 1.0)
        placeholder.progress(percent, text=f"{text}: {i}")
        time.sleep(speed)
    st.markdown(f"<span style='color:{color}; font-weight:bold'>{text}: {value}</span>", unsafe_allow_html=True)

# --- Typ Box Funktion ---
def typ_box(title, bericht, box_color):
    st.markdown(f"""
    <div style='border:2px solid #888888; padding:15px; border-radius:10px; background-color:{box_color}; margin-bottom:15px'>
    <h3>{title}</h3>
    {bericht}
    </div>
    """, unsafe_allow_html=True)

# --- Hauptfunktion ---
def aufgabenanalyse():
    st.set_page_config(page_title="Aufgaben-Entscheidungshelfer", layout="wide")

    # --- Dark Mode Toggle ---
    dark_mode = st.checkbox("🌙 Dark Mode aktivieren", value=False)
    mode = "dark" if dark_mode else "light"
    colors = FARBEN[mode]

    # --- Globalen Dark Mode via CSS ---
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

    st.title("Willkommen zum Aufgaben-Entscheidungshelfer!")

    st.write("""
    In Teams, Projekten oder Organisationen gibt es unterschiedliche Arten von Aufgaben.
    Je nachdem, wie der Erfolg zustande kommt, sind verschiedene Strategien für Zusammenarbeit und Entscheidungen sinnvoll.

    **Diese App hilft dir herauszufinden, welche Art von Aufgabe du gerade vor dir hast.**
    """)

    with st.expander("ℹ️ So funktioniert es:"):
        st.write("""
        - Beantworte **12 kurze Fragen** auf einer Skala von **1 bis 7**  
        - Die App ordnet deine Aufgabe einem oder mehreren Typen zu:
            - **Disjunktiv ⭐:** Erfolg hängt von der besten Leistung ab  
            - **Konjunktiv ⛓️:** Erfolg hängt vom schwächsten Glied ab  
            - **Additiv ➕:** Jeder Beitrag zählt
        - Du erhältst eine **ausführliche Empfehlung** für Strategie, Stolpersteine und Entscheidungswege.
        """)

    with st.expander("💡 Nutzen:"):
        st.write("""
        - Klarheit, wie dein Team arbeiten sollte  
        - Passende Entscheidungsstrategie wählen  
        - Stärken und Schwächen erkennen
        """)

    st.info("Beantworte die Fragen ehrlich – es gibt keine richtigen oder falschen Antworten.")
    st.divider()

    st.title("🎯 Aufgaben-Analyse")
    st.caption("1 = trifft überhaupt nicht zu, 4 = teils zutreffend, 7 = trifft voll zu")

    SCHWELLENWERT_HYBRID = 6

    fragen = [
        {"text": "Je mehr Mitglieder aktiv mitwirken, desto besser – auch kleine Beiträge summieren sich zu einem grossen Ergebnis.", "typ": "additiv"},
        {"text": "Wenn auch nur eine Person ihre Aufgabe nicht erfüllt, ist das gesamte Projekt gefährdet.", "typ": "konjunktiv"},
        {"text": "Eine einzelne Spitzenidee oder herausragende Leistung kann den gesamten Projekterfolg sicherstellen.", "typ": "disjunktiv"},
        {"text": "Die Zusammenarbeit scheitert, wenn ein einzelnes Mitglied nicht die nötige Qualität liefert.", "typ": "konjunktiv"},
        {"text": "Erfolg entsteht vor allem durch die Summe vieler Einzelbeiträge, nicht durch einzelne Spitzenleistungen.", "typ": "additiv"},
        {"text": "Die Leistung der besten Person bestimmt weitgehend, ob das Team erfolgreich ist, unabhängig von den anderen.", "typ": "disjunktiv"},
        {"text": "Fehler oder Ausfälle einzelner wirken sich sofort und stark auf den Gesamterfolg aus.", "typ": "konjunktiv"},
        {"text": "Wenn alle gleichmässig mitwirken, steigt die Wahrscheinlichkeit für einen erfolgreichen Abschluss deutlich.", "typ": "disjunktiv"},
        {"text": "Die Leistung des schwächsten Mitglieds bestimmt massgeblich, ob das Team sein Ziel erreicht.", "typ": "konjunktiv"},
        {"text": "Jeder Beitrag trägt zum Gesamterfolg bei, aber kein einzelner Ausfall bringt alles zum Scheitern.", "typ": "additiv"},
        {"text": "Auch kleine und regelmässige Beiträge aller Beteiligten können zusammen zu einem sehr starken Gesamtergebnis führen.", "typ": "additiv"},
        {"text": "Für den Erfolg reicht es, wenn eine Person die Aufgabe vollständig meistert – andere Beiträge sind nicht entscheidend.", "typ": "disjunktiv"},
    ]

    punkte = {"disjunktiv": 0, "konjunktiv": 0, "additiv": 0}

    with st.form("fragen_form"):
        antworten = []
        for i, frage in enumerate(fragen, start=1):
            antwort = st.slider(
                f"{i}. {frage['text']}",
                min_value=1,
                max_value=7,
                value=4,
                help="1 = trifft nicht zu, 7 = trifft voll zu"
            )
            antworten.append((frage['typ'], antwort))
        submitted = st.form_submit_button("Analyse starten")

    if submitted:
        durchschnitt = sum([antwort for _, antwort in antworten]) / len(antworten)
        if durchschnitt < 2.0:
            st.warning("🎭 Ergebnis: Keine Aufgabe erkannt – Zeit für einen Kaffee ☕")
            st.write("Offenbar gibt es aktuell keine echte Aufgabe – oder du hast die Fragen komplett auf Autopilot beantwortet. 😌")
            return

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
- Arbeit gleichmässig verteilen  
- Fortschritte sichtbar machen  
- Motivation hochhalten
"""
        typ_box(typ_name, bericht, colors["box"])

if __name__ == "__main__":
    aufgabenanalyse()
