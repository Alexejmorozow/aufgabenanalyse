import streamlit as st

def aufgabenanalyse():
    st.title("🎯 Aufgaben-Entscheidungshelfer")
    st.write("Bitte beantworte die folgenden Fragen auf einer Skala von 1–7:")
    st.caption("1 = trifft überhaupt nicht zu, 4 = teils zutreffend, 7 = trifft voll zu")
    
    # Konfiguration
    SCHWELLENWERT_HYBRID = 5

    # Neutral gemischte Fragen
    fragen = [
        {"text": "Jeder Beitrag summiert sich direkt zum Gesamtergebnis.", "typ": "additiv"},
        {"text": "Aktive Zusammenarbeit aller ist entscheidend für den Erfolg.", "typ": "konjunktiv"},
        {"text": "Eine einzelne Person kann den Erfolg sicherstellen, andere sind weniger wichtig.", "typ": "disjunktiv"},
        {"text": "Gleichmäßige Mitwirkung aller erhöht die Erfolgswahrscheinlichkeit.", "typ": "additiv"},
        {"text": "Schwächere Leistungen haben keinen entscheidenden Einfluss auf den Gesamterfolg.", "typ": "disjunktiv"},
        {"text": "Alle müssen ihre Aufgaben erfüllen, sonst ist das Ergebnis gefährdet.", "typ": "konjunktiv"},
        {"text": "Die leistungsstärkste Person bestimmt weitgehend den Erfolg.", "typ": "disjunktiv"},
        {"text": "Der Erfolg hängt stark von der Leistung des schwächsten Mitglieds ab.", "typ": "konjunktiv"},
        {"text": "Jeder Beitrag zählt, die Gesamtsumme bestimmt den Erfolg.", "typ": "additiv"}
    ]

    # Punktespeicher
    punkte = {"disjunktiv": 0, "konjunktiv": 0, "additiv": 0}
    
    # Fragen als Formular
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
        # Punkte berechnen
        for typ, antwort in antworten:
            punkte[typ] += antwort

        # Analyse
        gesamtpunkte = sum(punkte.values())
        prozentuale_verteilung = {typ: round((wert/gesamtpunkte)*100, 1) for typ, wert in punkte.items()}
        
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
                st.progress(prozent/100, text=f"{typ.capitalize()}: {prozent}%")

        # Entscheidung Hybrid oder klarer Typ
        st.divider()
        st.subheader("🎯 Empfehlung")
        
        if max_punkte - zweit_punkte <= SCHWELLENWERT_HYBRID:
            st.info(f"**🔀 HYBRIDE AUFGABE erkannt: {max_typ.capitalize()} + {zweit_typ.capitalize()}**")
            
            # Empfehlung für Hybrid
            if ("disjunktiv" in [max_typ, zweit_typ]) and ("konjunktiv" in [max_typ, zweit_typ]):
                st.write("Achte sowohl auf die stärksten als auch auf die schwächsten Mitglieder. Förderung aller ist entscheidend.")
            elif ("disjunktiv" in [max_typ, zweit_typ]) and ("additiv" in [max_typ, zweit_typ]):
                st.write("Nutze die Stärken der besten Mitglieder, motiviere gleichzeitig alle, Beiträge zu leisten.")
            elif ("konjunktiv" in [max_typ, zweit_typ]) and ("additiv" in [max_typ, zweit_typ]):
                st.write("Stelle Kooperation sicher und achte darauf, dass alle aktiv beitragen.")
            else:
                st.write("Eine Mischung aller Strategien kann sinnvoll sein.")
        else:
            st.success(f"**🎯 KLARER AUFGABENTYP: {max_typ.capitalize()}**")
            
            # Empfehlung für klaren Typ
            if max_typ == "disjunktiv":
                st.write("Fokussiere auf die leistungsstärksten Mitglieder. Schwächere können unterstützend wirken.")
            elif max_typ == "konjunktiv":
                st.write("Achte besonders auf die schwächsten Mitglieder – sie bestimmen den Erfolg. Förderung und Kooperation sicherstellen.")
            elif max_typ == "additiv":
                st.write("Jeder Beitrag zählt. Verteile Arbeit gleichmäßig und motiviere alle Beteiligten, aktiv mitzuwirken.")

# App starten
if __name__ == "__main__":
    aufgabenanalyse()
