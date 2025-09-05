import streamlit as st
import time

# --- Farb-Definitionen pro Typ ---
TYP_FARBEN = {
    "disjunktiv": "#E63946",  # kräftiges Rot
    "konjunktiv": "#F1FA3C",  # kräftiges Gelb
    "additiv": "#2A9D8F"      # kräftiges Grün
}

# --- Emoji pro Typ ---
TYP_EMOJI = {
    "disjunktiv": "⭐",
    "konjunktiv": "⛓️",
    "additiv": "➕"
}

# --- Funktion für animierte Progress Bars ---
def animated_progress(value, max_value, color, text, speed=0.02):
    placeholder = st.empty()
    max_value = max_value if max_value > 0 else 1
    for i in range(1, value + 1):
        percent = min(i / max_value, 1.0)  # nie > 1.0
        placeholder.progress(percent, text=f"{text}: {i}")
        time.sleep(speed)
    st.markdown(f"<span style='color:{color}; font-weight:bold'>{text}: {value}</span>", unsafe_allow_html=True)

# --- Typ-Box für Ergebnisse ---
def typ_box(title, bericht, color):
    st.markdown(f"""
    <div style='border:2px solid {color}; padding:15px; border-radius:10px; background-color:#f9f9f9; margin-bottom:15px'>
    <h3 style='color:{color}'>{title}</h3>
    {bericht}
    </div>
    """, unsafe_allow_html=True)

# --- Hauptfunktion ---
def aufgabenanalyse():
    st.set_page_config(page_title="Aufgaben-Entscheidungshelfer", layout="wide")
    st.title("Willkommen zum Aufgaben-Entscheidungshelfer!")

    st.write("""
    In Teams, Projekten oder Organisationen gibt es unterschiedliche Arten von Aufgaben.
    Je nachdem, wie der Erfolg zustande kommt, sind verschiedene Strategien für Zusammenarbeit und Entscheidungen sinnvoll.

    **Diese App hilft dir herauszufinden, welche Art von Aufgabe du gerade vor dir hast.**
    """)

    with st.expander("ℹ️ So funktioniert es:"):
        st.write("""
        - Beantworte **12 kurze Fragen** auf einer Skala von **1 bis 7**  
          *(1 = trifft überhaupt nicht zu, 7 = trifft voll zu)*.
        - Die App analysiert deine Antworten und ordnet deine Aufgabe einem oder mehreren Typen zu:
            - **Disjunktiv ⭐:** Erfolg hängt von der besten Leistung ab  
            - **Konjunktiv ⛓️:** Erfolg hängt vom schwächsten Glied ab  
            - **Additiv ➕:** Jeder Beitrag zählt, die Summe aller Leistungen ist entscheidend
        - Du erhältst eine **ausführliche Empfehlung**, wie du Entscheidungen treffen und dein Team organisieren kannst.
        """)

    with st.expander("💡 Nutzen:"):
        st.write("""
        - Klarheit darüber, wie dein Team zusammenarbeiten sollte  
        - Die richtige Entscheidungsstrategie für dein aktuelles Projekt wählen  
        - Stärken und Schwächen im Team erkennen
        """)

    st.info("Beantworte die Fragen ehrlich – es gibt keine richtigen oder falschen Antworten.")
    st.divider()

    # --- FRAGEN ---
    st.title("🎯 Aufgaben-Analyse")
    st.write("Bitte beantworte die folgenden Fragen auf einer Skala von 1–7:")
    st.caption("1 = trifft überhaupt nicht zu, 4 = teils zutreffend, 7 = trifft voll zu")

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

    # --- FORMULAR ---
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
        # --- Fun Feature: keine Aufgabe ---
        durchschnitt = sum([antwort for _, antwort in antworten]) / len(antworten)
        if durchschnitt < 2.0:
            st.warning("🎭 Ergebnis: Keine Aufgabe erkannt")
            st.write("Offenbar gibt es aktuell keine echte Aufgabe – oder du hast die Fragen komplett auf Autopilot beantwortet. 😌")
            return

        # --- Punkte summieren ---
        for typ, antwort in antworten:
            punkte[typ] += antwort

        gesamtpunkte = sum(punkte.values())
        prozentuale_verteilung = {typ: round((wert / gesamtpunkte) * 100, 1) for typ, wert in punkte.items()}

        sorted_typen = sorted(punkte.items(), key=lambda x: x[1], reverse=True)
        max_punkte = sorted_typen[0][1]

        # --- Hybridlogik: alle Typen innerhalb Schwellenwert ---
        hybrid_typen = [typ for typ, wert in punkte.items() if max_punkte - wert <= SCHWELLENWERT_HYBRID]

        st.success("✅ Analyse abgeschlossen!")

        # --- Ergebnisse animiert ---
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📊 Punktestände")
            for typ, wert in punkte.items():
                animated_progress(value=wert, max_value=7, color=TYP_FARBEN[typ], text=f"{TYP_EMOJI[typ]} {typ.capitalize()}")
        with col2:
            st.subheader("📈 Prozentuale Verteilung")
            for typ, prozent in prozentuale_verteilung.items():
                animated_progress(value=int(prozent), max_value=100, color=TYP_FARBEN[typ], text=f"{TYP_EMOJI[typ]} {typ.capitalize()} %", speed=0.01)

        st.divider()
        st.subheader("🎯 Empfehlung")

        # --- Bericht dynamisch für Hybrid oder klaren Typ ---
        typ_name = " + ".join([f"{TYP_EMOJI[typ]} {typ.capitalize()}" for typ in hybrid_typen])
        bericht = ""
        for typ in hybrid_typen:
            if typ == "disjunktiv":
                bericht += """
**Disjunktiv ⭐:** Erfolg hängt stark von der besten Leistung ab.
- Spitzenkräfte erkennen und fördern
- Kreativität fördern
- Teammitglieder gezielt einsetzen
- Kernleistungen regelmäßig kontrollieren
"""
            elif typ == "konjunktiv":
                bericht += """
**Konjunktiv ⛓️:** Erfolg hängt vom schwächsten Mitglied ab.
- Schwache Mitglieder trainieren und unterstützen
- Zusammenarbeit intensiv pflegen
- Faire Aufgabenverteilung
- Risiken absichern
"""
            elif typ == "additiv":
                bericht += """
**Additiv ➕:** Jeder Beitrag zählt, die Summe aller Leistungen ist entscheidend.
- Breite Beteiligung fördern
- Arbeit gleichmäßig verteilen
- Fortschritte sichtbar machen
- Motivation hochhalten
"""
        typ_box(typ_name, bericht, "#2A9D8F")  # neutrale Farbe für Hybrid
        

if __name__ == "__main__":
    aufgabenanalyse()
