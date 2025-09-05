def aufgabenanalyse():
    print("Willkommen zum Aufgaben-Entscheidungshelfer!")
    print("Bitte beantworte die folgenden Fragen auf einer Skala von 1–7:")
    print("1 = trifft überhaupt nicht zu, 4 = teils zutreffend, 7 = trifft voll zu\n")

    # Neutral gemischte Fragen
    fragen = [
        {"text": "Jeder einzelne Beitrag summiert sich direkt zum Gesamtergebnis, sodass das Team umso erfolgreicher ist, je mehr jeder leistet.", "typ": "additiv"},
        {"text": "Es ist entscheidend, dass alle Mitglieder aktiv zusammenarbeiten, sich gegenseitig unterstützen und koordinieren, um das gemeinsame Ziel zu erreichen.", "typ": "konjunktiv"},
        {"text": "Für den Erfolg des Teams oder Projekts reicht es, wenn eine einzelne Person die Aufgabe vollständig meistert, während die anderen weniger beitragen oder sogar ausfallen könnten.", "typ": "disjunktiv"},
        {"text": "Wenn alle Mitglieder gleichmäßig mitwirken und ihre Anstrengungen kombinieren, steigt die Wahrscheinlichkeit für einen erfolgreichen Abschluss deutlich.", "typ": "additiv"},
        {"text": "Wenn einzelne Mitglieder weniger leisten oder schwächer sind, hat das keinen entscheidenden Einfluss auf den Gesamterfolg des Teams.", "typ": "disjunktiv"},
        {"text": "Damit das Team oder Projekt erfolgreich ist, müssen alle Mitglieder ihre Aufgaben erfüllen, da das Gesamtergebnis sonst gefährdet ist.", "typ": "konjunktiv"},
        {"text": "Die Leistung der leistungsstärksten Person bestimmt weitgehend, ob das Team sein Ziel erreicht, unabhängig davon, wie die anderen abschneiden.", "typ": "disjunktiv"},
        {"text": "Der Erfolg hängt stark von der Leistung des schwächsten Mitglieds ab – selbst eine kleine Schwäche kann das Ergebnis gefährden.", "typ": "konjunktiv"},
        {"text": "Damit das Team erfolgreich ist, zählt jeder Beitrag, die Gesamtsumme aller Anstrengungen bestimmt den Erfolg.", "typ": "additiv"}
    ]

    # Punktespeicher
    punkte = {"disjunktiv": 0, "konjunktiv": 0, "additiv": 0}

    # Fragen abfragen
    for i, frage in enumerate(fragen, start=1):
        while True:
            try:
                antwort = int(input(f"{i}. {frage['text']}\nAntwort (1–7): "))
                if 1 <= antwort <= 7:
                    punkte[frage["typ"]] += antwort
                    break
                else:
                    print("Bitte eine Zahl zwischen 1 und 7 eingeben.")
            except ValueError:
                print("Ungültige Eingabe. Bitte eine Zahl zwischen 1 und 7 eingeben.")

    # Analyse
    sorted_typen = sorted(punkte.items(), key=lambda x: x[1], reverse=True)
    max_typ, max_punkte = sorted_typen[0]
    zweit_typ, zweit_punkte = sorted_typen[1]

    print("\n--- Analyse abgeschlossen ---")

    # Entscheidung Hybrid oder klarer Typ
    if max_punkte - zweit_punkte <= 5:  # Schwellenwert für Hybrid
        print(f"Hybride Aufgabe erkannt: {max_typ.capitalize()} + {zweit_typ.capitalize()}")
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
        print(f"Wahrscheinlichster Aufgabentyp: {max_typ.capitalize()}")
        # Empfehlung für klaren Typ
        if max_typ == "disjunktiv":
            print("Strategieempfehlung: Fokussiere auf die leistungsstärksten Mitglieder. Schwächere können unterstützend wirken.")
        elif max_typ == "konjunktiv":
            print("Strategieempfehlung: Achte besonders auf die schwächsten Mitglieder oder Faktoren – sie bestimmen den Erfolg. Förderung und Kooperation sicherstellen.")
        elif max_typ == "additiv":
            print("Strategieempfehlung: Jeder Beitrag zählt. Verteile Arbeit gleichmäßig und motiviere alle Beteiligten, aktiv mitzuwirken.")

# Programm starten
if __name__ == "__main__":
    aufgabenanalyse()
