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
            - **Disjunktiv:** Erfolg hängt stark von der **besten Leistung** im Team ab.  
            - **Konjunktiv:** Erfolg hängt vom **schwächsten Glied** ab – alle müssen gut zusammenarbeiten.  
            - **Additiv:** Jeder Beitrag zählt – die **Summe aller Leistungen** bestimmt den Erfolg.
        - Du erhältst eine **Empfehlung**, wie du dein Team organisieren und Entscheidungen treffen kannst.
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

    # 12 durchmischte Fragen
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

    # Punkte-Speicher
    punkte = {"disjunktiv": 0, "konjunktiv": 0, "additiv": 0}

    # Formular für Fragen
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

    # --- AUSWERTUNG ---
    if submitted:
        # Punkte summieren
        for typ, antwort in antworten:
            punkte[typ] += antwort

        # Prozentuale Verteilung
        gesamtpunkte = sum(punkte.values())
        prozentuale_verteilung = {
            typ: round((wert / gesamtpunkte) * 100, 1) for typ, wert in punkte.items()
        }

        # Sortieren nach höchstem Wert
        sorted_typen = sorted(punkte.items(), key=lambda x: x[1], reverse=True)
        max_typ, max_punkte = sorted_typen[0]
        zweit_typ, zweit_punkte = sorted_typen[1]

        st.success("Analyse abgeschlossen!")

        # Ergebnisse anzeigen
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

        # Hybrid-Entscheidung
        if max_punkte - zweit_punkte <= SCHWELLENWERT_HYBRID:
            st.info(f"**🔀 Hybride Aufgabe erkannt: {max_typ.capitalize()} + {zweit_typ.capitalize()}**")

            if {"disjunktiv", "konjunktiv"} == {max_typ, zweit_typ}:
                st.write("""
                Diese Aufgabe vereint Elemente von Disjunktiv und Konjunktiv.
                - Fokussiere dich sowohl auf die stärksten Mitglieder, um Top-Leistungen zu ermöglichen,  
                - als auch auf die schwächeren Mitglieder, da diese den Erfolg gefährden können.  
                **Strategie:** intensive Koordination, Training und klare Rollen.
                """)
            elif {"disjunktiv", "additiv"} == {max_typ, zweit_typ}:
                st.write("""
                Diese Aufgabe vereint Elemente von Disjunktiv und Additiv.
                - Nutze gezielt die Stärken der besten Mitglieder,  
                - motiviere gleichzeitig alle anderen, kleine und regelmäßige Beiträge zu leisten.  
                **Strategie:** Mischung aus Talentförderung und breiter Partizipation.
                """)
            elif {"konjunktiv", "additiv"} == {max_typ, zweit_typ}:
                st.write("""
                Diese Aufgabe vereint Elemente von Konjunktiv und Additiv.
                - Stelle sicher, dass **alle aktiv beitragen**,  
                - und kümmere dich besonders um schwächere Mitglieder, um Engpässe zu vermeiden.  
                **Strategie:** klare Aufgabenverteilung und gemeinsame Qualitätsstandards.
                """)
            else:
                st.write("Diese Aufgabe kombiniert verschiedene Aufgabentypen. Nutze eine flexible Strategie.")

        # Klarer Typ
        else:
            st.success(f"**🎯 Klarer Aufgabentyp: {max_typ.capitalize()}**")

            if max_typ == "disjunktiv":
                st.write("""
                **Disjunktive Aufgabe:**  
                - Erfolg hängt stark von den besten Leistungen ab.  
                - Fokussiere dich auf deine Top-Mitglieder, um Spitzenleistungen zu fördern.  
                - Schwächere können unterstützend wirken, sind aber nicht entscheidend.  
                **Strategie:** gezielte Talentförderung und Freiräume für die besten Performer.
                """)
            elif max_typ == "konjunktiv":
                st.write("""
                **Konjunktive Aufgabe:**  
                - Der Erfolg hängt vom schwächsten Mitglied ab.  
                - Stelle sicher, dass alle gut kooperieren und niemand überfordert ist.  
                - Schwächen müssen früh erkannt und aktiv ausgeglichen werden.  
                **Strategie:** Teamtraining, Coaching und gegenseitige Unterstützung.
                """)
            elif max_typ == "additiv":
                st.write("""
                **Additive Aufgabe:**  
                - Jeder Beitrag zählt und die Summe aller Leistungen ist entscheidend.  
                - Verteile Arbeit gleichmäßig und motiviere alle, kontinuierlich beizutragen.  
                **Strategie:** breite Beteiligung fördern und Fortschritte transparent machen.
                """)

# Start der App
if __name__ == "__main__":
    aufgabenanalyse()
