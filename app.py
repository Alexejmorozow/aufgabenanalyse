import streamlit as st

def aufgabenanalyse():
    # --- EINLEITUNG ---
    st.title("Willkommen zum Aufgaben-Entscheidungshelfer!")

    st.write("""
    In Teams, Projekten oder Organisationen gibt es unterschiedliche Arten von Aufgaben.
    Je nachdem, wie der Erfolg zustande kommt, sind unterschiedliche Strategien für Zusammenarbeit und Entscheidungsfindung notwendig.

    **Diese App hilft dir herauszufinden, welche Art von Aufgabe du gerade vor dir hast.**
    """)

    with st.expander("ℹ️ So funktioniert es:"):
        st.write("""
        - Du beantwortest **12 kurze Fragen** zu deiner Aufgabe auf einer Skala von **1 bis 7**  
          *(1 = trifft überhaupt nicht zu, 7 = trifft voll zu)*.
        - Die App analysiert deine Antworten und ordnet deine Aufgabe einem oder mehreren Aufgabentypen zu:
            - **Disjunktiv:** Erfolg hängt stark von der besten Leistung im Team ab.  
            - **Konjunktiv:** Erfolg hängt vom schwächsten Glied ab – alle müssen gut zusammenarbeiten.  
            - **Additiv:** Jeder Beitrag zählt – die Summe aller Leistungen bestimmt den Erfolg.
        - Du erhältst eine **ausführliche Empfehlung**, wie du Entscheidungen treffen und dein Team optimal organisieren kannst.
        """)

    with st.expander("💡 Nutzen:"):
        st.write("""
        - Klarheit darüber, wie dein Team zusammenarbeiten sollte  
        - Die richtige Entscheidungsstrategie für dein aktuelles Projekt finden  
        - Stärken und Schwächen im Team besser verstehen
        """)

    st.info("Hinweis: Beantworte die Fragen ehrlich und spontan – es gibt keine richtigen oder falschen Antworten.")
    st.divider()

    # --- FRAGEN ---
    st.title("🎯 Aufgaben-Analyse")
    st.write("Bitte beantworte die folgenden Fragen auf einer Skala von 1–7:")
    st.caption("1 = trifft überhaupt nicht zu, 4 = teils zutreffend, 7 = trifft voll zu")

    SCHWELLENWERT_HYBRID = 6  # Unterschied, ab dem wir von Hybrid sprechen

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
        # --- FUN FEATURE: KEINE ECHTE AUFGABE ---
        durchschnitt = sum([antwort for _, antwort in antworten]) / len(antworten)
        if durchschnitt < 2.0:
            st.warning("🎭 Ergebnis: Keine Aufgabe erkannt")
            st.write("""
            Offenbar hast du aktuell gar keine echte Aufgabe – oder du hast die Fragen komplett auf Autopilot beantwortet.  
            Vielleicht läuft bei dir einfach alles so perfekt, dass es nichts zu analysieren gibt. 😌  

            💡 Tipp: Wenn das nicht stimmt, probiere es nochmal mit ehrlichen Antworten.  
            Und falls doch: Gönn dir einen Kaffee und genieße den Leerlauf. ☕
            """)
            return

        # --- PUNKTE SUMMIEREN ---
        for typ, antwort in antworten:
            punkte[typ] += antwort

        gesamtpunkte = sum(punkte.values())
        prozentuale_verteilung = {
            typ: round((wert / gesamtpunkte) * 100, 1) for typ, wert in punkte.items()
        }

        sorted_typen = sorted(punkte.items(), key=lambda x: x[1], reverse=True)
        max_typ, max_punkte = sorted_typen[0]
        zweit_typ, zweit_punkte = sorted_typen[1]

        st.success("Analyse abgeschlossen!")

        # --- ERGEBNISSE VISUALISIEREN ---
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📊 Punktestände")
            for typ, wert in punkte.items():
                st.write(f"{typ.capitalize()}: {wert} Punkte")
        with col2:
            st.subheader("📈 Prozentuale Verteilung")
            for typ, prozent in prozentuale_verteilung.items():
                st.progress(prozent / 100, text=f"{typ.capitalize()}: {prozent}%")

        st.divider()
        st.subheader("🎯 Empfehlung")

        # --- HYBRID-LOGIK ---
        if max_punkte - zweit_punkte <= SCHWELLENWERT_HYBRID:
            if {"disjunktiv", "konjunktiv"} == {max_typ, zweit_typ}:
                typ = "Hybrid Disjunktiv + Konjunktiv"
                bericht = """
**Um was für eine Aufgabe handelt es sich?**  
Eine Mischung aus disjunktiv und konjunktiv: Sowohl Spitzenleistung als auch das schwächste Glied beeinflussen den Erfolg.

**Was bezeichnet diese Aufgabe?**  
Die Aufgabe kombiniert Extreme: Spitzenleistungen treiben voran, aber Engpässe können alles stoppen.

**Strategien:**  
- Spitzenkräfte gezielt einsetzen und entlasten  
- Schwächere Teammitglieder trainieren und unterstützen  
- Klare Rollen und Verantwortlichkeiten  
- Risikomanagement und kontinuierliche Abstimmung

**Wer soll entscheiden?**  
- Mix aus autokratisch (Spitzenkraft) und demokratisch (Teamkonsultation)
"""
            elif {"disjunktiv", "additiv"} == {max_typ, zweit_typ}:
                typ = "Hybrid Disjunktiv + Additiv"
                bericht = """
**Um was für eine Aufgabe handelt es sich?**  
Erfolg hängt sowohl von der besten Leistung als auch von der Summe aller Beiträge ab.

**Was bezeichnet diese Aufgabe?**  
Spitzenkraft treibt das Projekt voran, alle Beiträge erhöhen die Qualität.

**Strategien:**  
- Spitzenkräfte fördern  
- Alle zu kleinen Beiträgen motivieren  
- Regelmäßiges Monitoring  
- Kombination aus Einzel- und Team-Feedback

**Wer soll entscheiden?**  
- Autokratisch bei Kernentscheidungen, demokratisch bei ergänzenden Aufgaben
"""
            elif {"konjunktiv", "additiv"} == {max_typ, zweit_typ}:
                typ = "Hybrid Konjunktiv + Additiv"
                bericht = """
**Um was für eine Aufgabe handelt es sich?**  
Der Erfolg hängt vom schwächsten Mitglied und von der Summe aller Beiträge ab.

**Was bezeichnet diese Aufgabe?**  
Alle müssen mitarbeiten, individuelle Leistungen summieren sich zum Gesamterfolg.

**Strategien:**  
- Alle aktiv einbinden  
- Schwächste Mitglieder gezielt fördern  
- Arbeit transparent verteilen  
- Kleine Teilergebnisse sichern

**Wer soll entscheiden?**  
- Demokratisch, Teamkonsens ist wichtig
"""
            else:
                typ = "Triple-Hybrid"
                bericht = """
**Um was für eine Aufgabe handelt es sich?**  
Extrem komplex: Beste Leistung, schwächstes Glied und Summe aller Beiträge beeinflussen den Erfolg.

**Was bezeichnet diese Aufgabe?**  
Universell komplex: Erfolg nur durch Spitzenleistung, Vermeidung von Engpässen und Teambeiträge.

**Strategien:**  
- Spitzenkräfte identifizieren, fördern und entlasten  
- Schwache Mitglieder gezielt trainieren und unterstützen  
- Breite Beteiligung aller Teammitglieder sicherstellen  
- Klare Rollen, Risikomanagement, regelmäßige Reviews  
- Mischung aus autokratischen Kernentscheidungen und demokratischer Abstimmung für Teamaktivitäten

**Wer soll entscheiden?**  
- Hybrider Ansatz: Autokratisch bei Kernentscheidungen, demokratisch bei Teamaktivitäten
"""
        else:
            # --- KLARE TYPEN ---
            typ = max_typ.capitalize()
            if max_typ == "disjunktiv":
                bericht = """
**Um was für eine Aufgabe handelt es sich?**  
Disjunktive Aufgabe: Der Erfolg hängt stark von der besten Leistung im Team ab.

**Was bezeichnet diese Aufgabe?**  
Eine einzelne Spitzenleistung kann den Gesamterfolg sicherstellen, andere Beiträge sind weniger entscheidend.

**Strategien:**  
- Spitzenkräfte erkennen und gezielt fördern  
- Freiraum für Kreativität geben  
- Teammitglieder als Unterstützung einsetzen  
- Regelmäßige Kontrolle der Kernleistung

**Wer soll entscheiden?**  
- Autokratisch oder auf Experten fokussiert
"""
            elif max_typ == "konjunktiv":
                bericht = """
**Um was für eine Aufgabe handelt es sich?**  
Konjunktive Aufgabe: Der Erfolg hängt vom schwächsten Mitglied ab.

**Was bezeichnet diese Aufgabe?**  
Alle müssen ihre Aufgabe erfüllen, sonst ist das Ergebnis gefährdet.

**Strategien:**  
- Schwächste Mitglieder trainieren und unterstützen  
- Intensive Zusammenarbeit und klare Kommunikation  
- Aufgaben fair verteilen und Engpässe vermeiden  
- Risikomanagement implementieren

**Wer soll entscheiden?**  
- Demokratisch, Teamkonsens ist wichtig
"""
            elif max_typ == "additiv":
                bericht = """
**Um was für eine Aufgabe handelt es sich?**  
Additive Aufgabe: Jeder Beitrag zählt, die Summe aller Leistungen bestimmt den Erfolg.

**Was bezeichnet diese Aufgabe?**  
Keine einzelne Person kann den Erfolg allein sichern oder gefährden.

**Strategien:**  
- Breite Beteiligung fördern  
- Aufgaben gleichmäßig verteilen  
- Fortschritte sichtbar machen  
- Motivation aller Teammitglieder hochhalten

**Wer soll entscheiden?**  
- Demokratisch, kollektiver Input ist sinnvoll
"""
        st.markdown(f"### {typ}")
        st.write(bericht)

# --- APP STARTEN ---
if __name__ == "__main__":
    aufgabenanalyse()
