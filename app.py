import streamlit as st
import time
import pandas as pd
import json
import io

# --- Page config ---
st.set_page_config(page_title="Decision Compass", layout="wide")

# --- Shared defs for Aufgaben-Analyse ---
TYP_EMOJI = {"disjunktiv": "⭐", "konjunktiv": "⛓️", "additiv": "➕"}

FARBEN = {
    "light": {
        "disjunktiv": "#E63946",
        "konjunktiv": "#F1FA3C",
        "additiv": "#2A9D8F",
        "background": "#FFFFFF",
        "text": "#000000",
        "box": "#f9f9f9",
    },
    "dark": {
        "disjunktiv": "#FF6B6B",
        "konjunktiv": "#FFD93D",
        "additiv": "#4ECDC4",
        "background": "#121212",
        "text": "#FFFFFF",
        "box": "#1E1E1E",
    },
}

# --- Helpers ---
def animated_progress(value, max_value, color, text, speed=0.015):
    placeholder = st.empty()
    max_value = max(max_value, 1)
    steps = int(max(1, value))
    for i in range(1, steps + 1):
        pct = min(i / max_value, 1.0)
        placeholder.progress(pct, text=f"{text}: {i}")
        time.sleep(speed)
    st.markdown(f"<span style='color:{color}; font-weight:bold'>{text}: {value}</span>", unsafe_allow_html=True)

def typ_box(title, bericht, box_color):
    st.markdown(
        f"""
    <div style='border:2px solid #888888; padding:15px; border-radius:10px; background-color:{box_color}; margin-bottom:15px'>
      <h3>{title}</h3>
      {bericht}
    </div>
    """,
        unsafe_allow_html=True,
    )

# --- Navigation ---
st.sidebar.title("🧭 Decision Compass")
mod = st.sidebar.radio(
    "Wähle Modul:",
    [
        "🏠 Start",
        "🔎 Aufgaben-Analyse",
        "📊 SWOT-Analyse",
        "⏳ Eisenhower-Matrix",
        "👥 RACI-Matrix",
        "⚖️ Balanced Scorecard",
    ],
)

# --- Startseite ---
if mod == "🏠 Start":
    st.title("🧭 Decision Compass")
    st.write(
        """
Willkommen zum Decision Compass. Wähle links ein Modul, um zu starten.
- Aufgaben-Analyse (Disjunktiv / Konjunktiv / Additiv)
- SWOT
- Eisenhower
- RACI
- Balanced Scorecard
"""
    )
    st.divider()

# --- Aufgaben-Analyse (dein originärer Fragebogen) ---
elif mod == "🔎 Aufgaben-Analyse":
    st.title("🔎 Aufgaben-Analyse (Disjunktiv / Konjunktiv / Additiv)")

    dark_mode = st.checkbox("🌙 Dark Mode aktivieren", value=False)
    mode = "dark" if dark_mode else "light"
    colors = FARBEN[mode]

    # safer theme injection (no fragile class names)
    st.markdown(
        f"""
    <style>
      .stApp {{ background-color: {colors['background']}; color: {colors['text']}; }}
      .streamlit-expanderHeader {{ color: {colors['text']} !important; }}
    </style>
    """,
        unsafe_allow_html=True,
    )

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
            antworten.append((frage["typ"], antwort))
        submitted = st.form_submit_button("Analyse starten")

    if submitted:
        durchschnitt = sum([a for _, a in antworten]) / len(antworten)
        if durchschnitt < 2.0:
            st.warning("Keine klare Aufgabe erkannt. Probier es erneut.")
        else:
            for typ, wert in antworten:
                punkte[typ] += wert

            gesamt = sum(punkte.values()) or 1
            proz = {t: round((v / gesamt) * 100, 1) for t, v in punkte.items()}
            max_p = max(punkte.values())
            hybrid = [t for t, v in punkte.items() if max_p - v <= SCHWELLENWERT_HYBRID]

            st.info("Analyse abgeschlossen")
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Punktetab")
                for t, v in punkte.items():
                    animated_progress(value=v, max_value=7, color=FARBEN[mode][t], text=f"{TYP_EMOJI[t]} {t.capitalize()}")
            with col2:
                st.subheader("Verteilung")
                for t, p in proz.items():
                    animated_progress(value=int(p), max_value=100, color=FARBEN[mode][t], text=f"{TYP_EMOJI[t]} {t.capitalize()} %", speed=0.01)

            st.divider()
            st.subheader("Empfehlung")
            typ_name = " + ".join([f"{TYP_EMOJI[t]} {t.capitalize()}" for t in hybrid])
            bericht = ""
            for t in hybrid:
                if t == "disjunktiv":
                    bericht += (
                        "**Aufgabe:** Disjunktiv ⭐ – Erfolg hängt von Spitzenleistung ab.\n\n"
                        "**Stolper:** Schwache Ressource, Überbelastung.\n\n"
                        "**Vorgehen:** Stärken fördern, Kernkontrolle, klare Entscheidungslinie.\n\n"
                    )
                elif t == "konjunktiv":
                    bericht += (
                        "**Aufgabe:** Konjunktiv ⛓️ – Erfolg hängt vom schwächsten Glied ab.\n\n"
                        "**Stolper:** Mangelnde Kooperation, Engpässe.\n\n"
                        "**Vorgehen:** Support für schwache Teammitgl, enge Koordination, faire Verteilung.\n\n"
                    )
                elif t == "additiv":
                    bericht += (
                        "**Aufgabe:** Additiv ➕ – Summe der Beiträge zählt.\n\n"
                        "**Stolper:** Unterbewertete Einzelleistung, Motivationstief.\n\n"
                        "**Vorgehen:** Alle einbinden, Fortschritt sichtbar machen, klare Microziele.\n\n"
                    )
            typ_box(typ_name, bericht, FARBEN[mode]["box"])

# --- SWOT ---
elif mod == "📊 SWOT-Analyse":
    st.title("📊 SWOT-Analyse")
    col1, col2 = st.columns(2)
    with col1:
        staerken = st.text_area("Stärken (Strengths)")
        chancen = st.text_area("Chancen (Opportunities)")
    with col2:
        schwaechen = st.text_area("Schwächen (Weaknesses)")
        risiken = st.text_area("Risiken (Threats)")

    if st.button("Analyse erstellen"):
        st.info("SWOT erstellt")
        s_html = staerken.replace("\n", "<br>")
        w_html = schwaechen.replace("\n", "<br>")
        o_html = chancen.replace("\n", "<br>")
        t_html = risiken.replace("\n", "<br>")
        st.markdown(
            f"""
        <div style='display:grid; grid-template-columns:1fr 1fr; gap:10px'>
          <div style='border:1px solid #ddd; padding:10px'><h4>Stärken</h4>{s_html}</div>
          <div style='border:1px solid #ddd; padding:10px'><h4>Schwächen</h4>{w_html}</div>
          <div style='border:1px solid #ddd; padding:10px'><h4>Chancen</h4>{o_html}</div>
          <div style='border:1px solid #ddd; padding:10px'><h4>Risiken</h4>{t_html}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

# --- Eisenhower ---
elif mod == "⏳ Eisenhower-Matrix":
    st.title("⏳ Eisenhower-Matrix")
    if "tasks" not in st.session_state:
        st.session_state["tasks"] = []

    with st.form("task_form"):
        name = st.text_input("Aufgabe")
        wichtig = st.selectbox("Wichtigkeit", ["hoch", "mittel", "niedrig"], index=1)
        dringend = st.checkbox("dringend")
        add = st.form_submit_button("Aufgabe anlegen")
        if add and name:
            st.session_state["tasks"].append({"name": name, "wichtig": wichtig, "dringend": dringend})

    if st.session_state["tasks"]:
        q1 = [t for t in st.session_state["tasks"] if t["wichtig"] == "hoch" and t["dringend"]]
        q2 = [t for t in st.session_state["tasks"] if t["wichtig"] == "hoch" and not t["dringend"]]
        q3 = [t for t in st.session_state["tasks"] if t["wichtig"] != "hoch" and t["dringend"]]
        q4 = [t for t in st.session_state["tasks"] if t["wichtig"] != "hoch" and not t["dringend"]]

        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Sofort tun (wichtig + dringend)")
            for t in q1:
                st.write(f"- {t['name']}")
        with c2:
            st.subheader("Planen (wichtig, nicht dringend)")
            for t in q2:
                st.write(f"- {t['name']}")

        st.divider()
        c3, c4 = st.columns(2)
        with c3:
            st.subheader("Delegieren (nicht wichtig, dringend)")
            for t in q3:
                st.write(f"- {t['name']}")
        with c4:
            st.subheader("Eliminieren (nicht wichtig, nicht dringend)")
            for t in q4:
                st.write(f"- {t['name']}")

    if st.button("Aufgaben löschen"):
        st.session_state["tasks"] = []
        st.experimental_rerun()

# --- RACI ---
elif mod == "👥 RACI-Matrix":
    st.title("👥 RACI-Matrix")
    st.write("Trag Aufgaben und Teammitgl ein, dann wähle pro Paar die Rolle (R/A/C/I).")
    tasks_text = st.text_area("Aufgaben (eine pro Zeile)")
    team_text = st.text_area("Teammitgl (eine pro Zeile)")

    tasks = [t.strip() for t in tasks_text.splitlines() if t.strip()]
    team = [m.strip() for m in team_text.splitlines() if m.strip()]

    if st.button("Matrix erstellen"):
        if not tasks or not team:
            st.warning("Bitte Aufgaben und Team eintragen.")
        else:
            # interaktive Matrix: fülle Zellen via selectbox
            rows = []
            for i, t in enumerate(tasks):
                row = {"Aufgabe": t}
                cols = st.columns(len(team) + 1)
                cols[0].write(f"**{t}**")
                for j, m in enumerate(team, start=1):
                    key = f"raci_{i}_{j}"
                    val = cols[j].selectbox(f"{t} | {m}", ["-", "R", "A", "C", "I"], key=key)
                    row[m] = val
                rows.append(row)
            df = pd.DataFrame(rows)
            st.dataframe(df)

# --- Balanced Scorecard ---
elif mod == "⚖️ Balanced Scorecard":
    st.title("⚖️ Balanced Scorecard")
    perspectives = ["Finanzen", "Kunden", "Prozesse", "Lernen & Entwicklung"]
    kpi_store = {}
    for p in perspectives:
        st.subheader(p)
        z = st.text_area(f"Ziele für {p}", key=f"ziel_{p}")
        k = st.text_area(f"KPI für {p} (eine pro Zeile)", key=f"kpi_{p}")
        kpi_store[p] = {"ziele": z, "kpis": [k1 for k1 in k.splitlines() if k1.strip()]}

    if st.button("Scorecard speichern"):
        st.info("Scorecard erfasst")
        st.write(kpi_store)
        blob = json.dumps(kpi_store, indent=2)
        st.download_button("Download JSON", data=blob, file_name="scorecard.json", mime="application/json")
