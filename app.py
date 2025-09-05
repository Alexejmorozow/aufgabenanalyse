import streamlit as st
import time

# --- Farb-Definitionen pro Typ ---
TYP_FARBEN = {
    "disjunktiv": "#E63946",   # kräftiges Rot
    "konjunktiv": "#F1FA3C",   # kräftiges Gelb
    "additiv": "#2A9D8F"       # kräftiges Grün
}

# --- Funktion für animierte Progress Bars ---
def animated_progress(value, max_value, color, text, speed=0.02):
    placeholder = st.empty()
    for i in range(1, value+1):
        percent = i / max_value
        placeholder.progress(percent, text=f"{text}: {i}")
        time.sleep(speed)
    # Farbliche Anzeige nach Animation
    st.markdown(f"<span style='color:{color}; font-weight:bold'>{text}: {value}</span>", unsafe_allow_html=True)

# --- Funktion für Typ-Boxen ---
def typ_box(title, bericht, color):
    st.markdown(f"""
    <div style='border:2px solid {color}; padding:15px; border-radius:10px; background-color:#f9f9f9; margin-bottom:15px'>
    <h3 style='color:{color}'>{title}</h3>
    {bericht}
    </div>
    """, unsafe_allow_html=True)

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
            - **Disjunktiv 🔥:** Erfolg hängt von der besten Leistung ab  
            - **Konjunktiv ⚡:** Erfolg hängt vom schwächsten Glied ab  
            - **Additiv 🌱:** Jeder Beitrag zählt, die Summe aller Leistungen ist entscheidend
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

    SCHWELLENWERT_HYBRID = 6  # Unterschied, ab dem wir Hybrid annehmen

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
        # --- FUN FEATURE: KEINE AUFGABE ---
        durchschnitt = sum([antwort for _, antwort in antworten]) / len(antworten)
        if durchschnitt < 2.0:
            st.warning("🎭 Ergebnis: Keine Aufgabe erkannt")
            st.write("""
            Offenbar gibt es aktuell keine echte Aufgabe – oder du hast die Fragen komplett auf Autopilot beantwortet.  
            Vielleicht läuft bei dir alles so gut, dass es nichts zu analysieren gibt. 😌
            """)
            return

        # --- PUNKTE SUMMIEREN ---
        for typ, antwort in antworten:
            punkte[typ] += antwort

        gesamtpunkte = sum(punkte.values())
        prozentuale_verteilung = {typ: round((wert / gesamtpunkte) * 100, 1) for typ, wert in punkte.items()}

        sorted_typen = sorted(punkte.items(), key=lambda x: x[1], reverse=True)
        max_typ, max_punkte = sorted_typen[0]
        zweit_typ, zweit_punkte = sorted_typen[1]

        st.success("✅ Analyse abgeschlossen!")

        # --- ERGEBNISSE ANIMIERT ---
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📊 Punktestände")
            for typ, wert in punkte.items():
                animated_progress(value=wert, max_value=7, color=TYP_FARBEN[typ], text=f"{typ.capitalize()}")
        with col2:
            st.subheader("📈 Prozentuale Verteilung")
            for typ, prozent in prozentuale_verteilung.items():
                animated_progress(value=int(prozent), max_value=100, color=TYP_FARBEN[typ], text=f"{typ.capitalize()} %", speed=0.01)

        st.divider()
        st.subheader("🎯 Empfehlung")

        # --- HYBRID-LOGIK ---
        if max_punkte - zweit_punkte <= SCHWELLENWERT_HYBRID:
            if {"disjunktiv", "konjunktiv"} == {max_typ, zweit_typ}:
                typ_name = "Hybrid Disjunktiv + Konjunktiv 🔥⚡"
                color = "#E63946"  # Rot-Gelb Mix
                bericht = """
**Um was für eine Aufgabe handelt es sich?**  
Eine Mischung aus Disjunktiv und Konjunktiv: Spitzenleistung und schwächstes Glied beeinflussen den Erfolg.

**Strategien:**  
- Spitzenkräfte gezielt einsetzen  
- Schwache Mitglieder unterstützen  
- Klare Rollen und Verantwortlichkeiten  
- Risikomanagement und kontinuierliche Abstimmung

**Wer soll entscheiden?**  
- Autokratisch bei Kernentscheidungen, demokratisch bei Teamaktivitäten
"""
            elif {"disjunktiv", "additiv"} == {max_typ, zweit_typ}:
                typ_name = "Hybrid Disjunktiv + Additiv 🔥🌱"
                color = "#E63946"  # Rot-Grün Mix
                bericht = """
**Um was für eine Aufgabe handelt es sich?**  
Erfolg hängt von der besten Leistung und von der Summe aller Beiträge ab.

**Strategien:**  
- Spitzenkräfte fördern  
- Alle zu kleinen Beiträgen motivieren  
- Regelmäßiges Monitoring  
- Kombination aus Einzel- und Team-Feedback

**Wer soll entscheiden?**  
- Autokratisch bei Kernentscheidungen, demokratisch bei ergänzenden Aufgaben
"""
            elif {"konjunktiv", "additiv"} == {max_typ, zweit_typ}:
                typ_name = "Hybrid Konjunktiv + Additiv ⚡🌱"
                color = "#F1FA3C"  # Gelb-Grün Mix
                bericht = """
**Um was für eine Aufgabe handelt es sich?**  
Der Erfolg hängt vom schwächsten Mitglied und von der Summe aller Beiträge ab.

**Strategien:**  
- Alle aktiv einbinden  
- Schwächste Mitglieder gezielt fördern  
- Arbeit transparent verteilen  
- Kleine Teilergebnisse sichern

**Wer soll entscheiden?**  
- Demokratisch, Teamkonsens ist wichtig
"""
            else:
                typ_name = "Triple-Hybrid 🔥⚡🌱"
                color = "#FF8800"  # Mix
                bericht = """
**Um was für eine Aufgabe handelt es sich?**  
Extrem komplex: Beste Leistung, schwächstes Glied und Summe aller Beiträge beeinflussen den Erfolg.

**Strategien:**  
- Spitzenkräfte identifizieren, fördern und entlasten  
- Schwache Mitglieder trainieren und unterstützen  
- Breite Beteiligung aller Teammitglieder sicherstellen  
- Klare Rollen, Risikomanagement, regelmäßige Reviews

**Wer soll entscheiden?**  
- Hybrider Ansatz: Autokratisch bei Kernentscheidungen, demokratisch bei Teamaktivitäten
"""
        else:
            typ_name = max_typ.capitalize()
            color = TYP_FARBEN[max_typ]
            if max_typ == "disjunktiv":
                bericht = """
**Um was für eine Aufgabe handelt es sich?**  
Disjunktiv: Erfolg hängt stark von der besten Leistung im Team ab.

**Strategien:**  
- Spitzenkräfte erkennen und fördern  
- Freiraum für Kreativität geben  
- Teammitglieder als Unterstützung einsetzen  
- Regelmäßige Kontrolle der Kernleistung

**Wer soll entscheiden?**  
- Autokratisch oder auf Experten fokussiert
"""
            elif max_typ == "konjunktiv":
                bericht = """
**Um was für eine Aufgabe handelt es sich?**  
Konjunktiv: Erfolg hängt vom schwächsten Mitglied ab.

**Strategien:**  
- Schwächste Mitglieder trainieren und unterstützen  
- Intensive Zusammenarbeit und Kommunikation  
- Aufgaben fair verteilen und Engpässe vermeiden  
- Risikomanagement implementieren

**Wer soll entscheiden?**  
- Demokratisch, Teamkonsens ist wichtig
"""
            elif max_typ == "additiv":
                bericht = """
**Um was für eine Aufgabe handelt es sich?**  
Additiv: Jeder Beitrag zählt, die Summe aller Leistungen ist entscheidend.

**Strategien:**  
- Breite Beteiligung fördern  
- Aufgaben gleichmäßig verteilen  
- Fortschritte sichtbar machen  
- Motivation aller Teammitglieder hochhalten

**Wer soll entscheiden?**  
- Demokratisch, kollektiver Input ist sinnvoll
"""
        typ_box(typ_name, bericht, color)

if __name__ == "__main__":
    aufgabenanalyse()
