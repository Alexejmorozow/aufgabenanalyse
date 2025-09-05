def aufgabenanalyse():
    print("Willkommen zum Aufgaben-Entscheidungshelfer!")
    print("Bitte beantworte die folgenden Fragen auf einer Skala von 1–7:")
    print("1 = trifft überhaupt nicht zu, 4 = teils zutreffend, 7 = trifft voll zu\n")
    
    # Konfiguration
    SCHWELLENWERT_HYBRID = 5

    # Neutral gemischte Fragen (leicht gekürzt für bessere Lesbarkeit)
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

    # Fragen abfragen
    for i, frage in enumerate(fragen, start=1):
        while True:
            try:
                antwort = int(input(f"\n{i}. {frage['text']}\nAntwort (1–7): "))
                if 1 <= antwort <= 7:
                    punkte[frage["typ"]] += antwort
                    break
                else:
                    print("Bitte eine Zahl zwischen 1 und 7 eingeben.")
            except ValueError:
                print("Ungültige Eingabe. Bitte eine Zahl zwischen 1 und 7 eingeben.")

    # Analyse
    gesamtpunkte = sum(punkte.values())
    prozentuale_verteilung = {typ: round((wert/gesamtpunkte)*100, 1) for typ, wert in punkte.items()}
    
    sorted_typen = sorted(punkte.items(), key=lambda x: x[1], reverse=True)
    max_typ, max_punkte = sorted_typen[0]
    zweit_typ, zweit_punkte = sorted_typen[1]

    print("\n" + "="*50)
    print("ANALYSE ABGESCHLOSSEN")
    print("="*50)
    
    print(f"\nPunktestände: {punkte}")
    print(f"Prozentuale Verteilung: {prozentuale_verteilung}")

    # Entscheidung Hybrid oder klarer Typ
    if max_punkte - zweit_punkte <= SCHWELLENWERT_HYBRID:
        print(f"\n🔀 HYBRIDE AUFGABE erkannt: {max_typ.capitalize()} + {zweit_typ.capitalize()}")
        
        # Empfehlung für Hybrid
        if ("disjunktiv" in [max_typ, zweit_typ]) and ("konjunktiv" in [max_typ, zweit_typ]):
            print("Empfehlung: Achte sowohl auf die stärksten als auch auf die schwächsten Mitglieder. Förderung aller ist entscheidend.")
        elif ("disjunktiv" in [max_typ, zweit_typ]) and ("additiv" in [max_typ, zweit_typ]):
            print("Empfehlung: Nutze die Stärken der besten Mitglieder, motiviere gleichzeitig alle, Beiträge zu leisten.")
        elif ("konjunktiv" in [max_typ, zweit_typ]) and ("additiv" in [max_typ, zweit_typ]):
            print("Empfehlung: Stelle Kooperation sicher und achte darauf, dass alle aktiv beitragen.")
        else:
            print("Empfehlung: Eine Mischung aller Strategien kann sinnvoll sein.")
    else:
        print(f"\n🎯 KLARER AUFGABENTYP: {max_typ.capitalize()}")
        
        # Empfehlung für klaren Typ
        if max_typ == "disjunktiv":
            print("Strategieempfehlung: Fokussiere auf die leistungsstärksten Mitglieder. Schwächere können unterstützend wirken.")
        elif max_typ == "konjunktiv":
            print("Strategieempfehlung: Achte besonders auf die schwächsten Mitglieder – sie bestimmen den Erfolg. Förderung und Kooperation sicherstellen.")
        elif max_typ == "additiv":
            print("Strategieempfehlung: Jeder Beitrag zählt. Verteile Arbeit gleichmäßig und motiviere alle Beteiligten, aktiv mitzuwirken.")
    
    print("\n" + "="*50)
    print("Viel Erfolg bei der Umsetzung!")
    print("="*50)

# Programm starten
if __name__ == "__main__":
    aufgabenanalyse()
