import streamlit as st
import time
import pandas as pd
import json
import io
import base64

# --- Page config ---
st.set_page_config(page_title="Decision Compass", layout="wide")

# --- Internationalization ---
LANGUAGES = {
    "DE": {
        "title": "🧭 Decision Compass",
        "modules": ["🏠 Start", "🔎 Aufgaben-Analyse", "📊 SWOT-Analyse", "⏳ Eisenhower-Matrix", "👥 RACI-Matrix", "⚖️ Balanced Scorecard"],
        "export": "Exportieren",
        "language": "Sprache"
    },
    "EN": {
        "title": "🧭 Decision Compass",
        "modules": ["🏠 Home", "🔎 Task Analysis", "📊 SWOT Analysis", "⏳ Eisenhower Matrix", "👥 RACI Matrix", "⚖️ Balanced Scorecard"],
        "export": "Export",
        "language": "Language"
    }
}

# --- Shared definitions ---
TYP_EMOJI = {"disjunktiv": "⭐", "konjunktiv": "⛓️", "additiv": "➕"}

FARBEN = {
    "light": {"disjunktiv": "#E63946", "konjunktiv": "#F1FA3C", "additiv": "#2A9D8F", "background": "#FFFFFF", "text": "#000000", "box": "#f9f9f9"},
    "dark": {"disjunktiv": "#FF6B6B", "konjunktiv": "#FFD93D", "additiv": "#4ECDC4", "background": "#121212", "text": "#FFFFFF", "box": "#1E1E1E"}
}

# --- Utility Functions ---
def get_text(key, lang):
    """Get translated text for given key"""
    translations = {
        # Start Page
        "welcome": {
            "DE": "Willkommen zum Decision Compass! Dieses Tool vereint bewährte Methoden der Entscheidungsfindung unter einem Dach.",
            "EN": "Welcome to Decision Compass! This tool combines proven decision-making methods under one roof."
        },
        "choose_module": {
            "DE": "Wähle ein Modul in der linken Leiste und arbeite Schritt für Schritt.",
            "EN": "Choose a module in the left sidebar and work step by step."
        },
        # Common
        "export_pdf": {"DE": "📄 Als PDF exportieren", "EN": "📄 Export as PDF"},
        "export_excel": {"DE": "📊 Als Excel exportieren", "EN": "📊 Export as Excel"},
        "export_csv": {"DE": "📝 Als CSV exportieren", "EN": "📝 Export as CSV"},
        "analysis_complete": {"DE": "✅ Analyse abgeschlossen!", "EN": "✅ Analysis complete!"},
        # Task Analysis
        "task_analysis_title": {"DE": "🔎 Aufgaben-Analyse", "EN": "🔎 Task Analysis"},
        "task_analysis_desc": {
            "DE": "Bestimme den Typ deiner Aufgabe: disjunktiv, konjunktiv oder additiv",
            "EN": "Determine your task type: disjunctive, conjunctive or additive"
        },
    }
    return translations.get(key, {}).get(lang, key)

def animated_progress(value, max_value, color, text, speed=0.02):
    """Animated progress bar with final value display"""
    placeholder = st.empty()
    max_value = max(max_value, 1)
    for i in range(1, value + 1):
        percent = min(i / max_value, 1.0)
        placeholder.progress(percent, text=f"{text}: {i}")
        time.sleep(speed)
    st.markdown(f"<span style='color:{color}; font-weight:bold'>{text}: {value}</span>", unsafe_allow_html=True)

def create_colored_box(title, content, bg_color, border_color="#888888"):
    """Create a styled colored box"""
    st.markdown(f"""
    <div style='border:2px solid {border_color}; padding:15px; border-radius:10px; background-color:{bg_color}; margin-bottom:15px'>
    <h3 style='margin-top:0;'>{title}</h3>
    {content}
    </div>
    """, unsafe_allow_html=True)

def format_list_text(text, default_text="Keine Einträge"):
    """Format text with bullet points"""
    if not text:
        return f"<em>{default_text}</em>"
    lines = text.split('\n')
    formatted = '<br>• '.join(lines)
    return f"• {formatted}"

def create_download_link(data, filename, text):
    """Create a download link for data"""
    if isinstance(data, pd.DataFrame):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            data.to_excel(writer, index=False, sheet_name='Results')
        data = output.getvalue()
    
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">{text}</a>'
    return href

def export_to_csv(data, filename):
    """Export data to CSV"""
    if isinstance(data, pd.DataFrame):
        return data.to_csv(index=False)
    return data

# --- Visualization Functions ---
def create_swot_quadrant(strengths, weaknesses, opportunities, threats):
    """Create SWOT analysis as 2x2 quadrant visualization"""
    st.markdown("""
    <style>
    .swot-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 15px;
        margin: 20px 0;
    }
    .swot-item {
        padding: 15px;
        border-radius: 10px;
        min-height: 200px;
    }
    .strengths { background-color: #d4edda; border-left: 5px solid #28a745; }
    .weaknesses { background-color: #f8d7da; border-left: 5px solid #dc3545; }
    .opportunities { background-color: #cce7ff; border-left: 5px solid #007bff; }
    .threats { background-color: #fff3cd; border-left: 5px solid #ffc107; }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="swot-grid">
        <div class="swot-item strengths">
            <h4>💪 Stärken / Strengths</h4>
            {format_list_text(strengths)}
        </div>
        <div class="swot-item weaknesses">
            <h4>📉 Schwächen / Weaknesses</h4>
            {format_list_text(weaknesses)}
        </div>
        <div class="swot-item opportunities">
            <h4>🚀 Chancen / Opportunities</h4>
            {format_list_text(opportunities)}
        </div>
        <div class="swot-item threats">
            <h4>⚠️ Risiken / Threats</h4>
            {format_list_text(threats)}
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_eisenhower_matrix(tasks):
    """Create Eisenhower matrix as colored grid"""
    quadrants = {
        "Q1": {"title": "🔴 Wichtig & Dringend", "tasks": [], "color": "#ff6b6b"},
        "Q2": {"title": "🟢 Wichtig & Nicht Dringend", "tasks": [], "color": "#51cf66"},
        "Q3": {"title": "🟡 Nicht Wichtig & Dringend", "tasks": [], "color": "#ffd43b"},
        "Q4": {"title": "⚫ Nicht Wichtig & Nicht Dringend", "tasks": [], "color": "#868e96"}
    }
    
    for task in tasks:
        quadrants[task["quadrant"]]["tasks"].append(task)
    
    st.markdown("""
    <style>
    .eisenhower-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 15px;
        margin: 20px 0;
    }
    .quadrant {
        padding: 15px;
        border-radius: 10px;
        min-height: 250px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="eisenhower-grid">
        <div class="quadrant" style="background-color: {quadrants['Q1']['color']}20; border-left: 5px solid {quadrants['Q1']['color']}">
            <h4>{quadrants['Q1']['title']}</h4>
            {"<br>".join([f"• {task['beschreibung']}" for task in quadrants['Q1']['tasks']]) or "Keine Aufgaben"}
        </div>
        <div class="quadrant" style="background-color: {quadrants['Q2']['color']}20; border-left: 5px solid {quadrants['Q2']['color']}">
            <h4>{quadrants['Q2']['title']}</h4>
            {"<br>".join([f"• {task['beschreibung']}" for task in quadrants['Q2']['tasks']]) or "Keine Aufgaben"}
        </div>
        <div class="quadrant" style="background-color: {quadrants['Q3']['color']}20; border-left: 5px solid {quadrants['Q3']['color']}">
            <h4>{quadrants['Q3']['title']}</h4>
            {"<br>".join([f"• {task['beschreibung']}" for task in quadrants['Q3']['tasks']]) or "Keine Aufgaben"}
        </div>
        <div class="quadrant" style="background-color: {quadrants['Q4']['color']}20; border-left: 5px solid {quadrants['Q4']['color']}">
            <h4>{quadrants['Q4']['title']}</h4>
            {"<br>".join([f"• {task['beschreibung']}" for task in quadrants['Q4']['tasks']]) or "Keine Aufgaben"}
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- Sidebar / Navigation ---
st.sidebar.title("🧭 Decision Compass")

# Language selector
language = st.sidebar.selectbox("🌐 Sprache / Language", ["DE", "EN"], index=0)

# Navigation
module = st.sidebar.radio("Navigation:", LANGUAGES[language]["modules"])

# Export section in sidebar
st.sidebar.markdown("---")
st.sidebar.subheader(LANGUAGES[language]["export"])

# --- START PAGE ---
if module == LANGUAGES[language]["modules"][0]:
    st.title("🧭 Decision Compass")
    
    st.write(get_text("welcome", language))
    st.write(get_text("choose_module", language))
    
    st.divider()
    
    # Module descriptions
    modules_info = {
        "🔎": {
            "DE": ("Aufgaben-Analyse", "Bestimme den Typ deiner Aufgabe: disjunktiv, konjunktiv oder additiv. Ideal für Team-Projekte und Arbeitsverteilung."),
            "EN": ("Task Analysis", "Determine your task type: disjunctive, conjunctive or additive. Ideal for team projects and work distribution.")
        },
        "📊": {
            "DE": ("SWOT-Analyse", "Analysiere Stärken, Schwächen, Chancen und Risiken. Perfekt für strategische Planung und Entscheidungsfindung."),
            "EN": ("SWOT Analysis", "Analyze strengths, weaknesses, opportunities and threats. Perfect for strategic planning and decision making.")
        },
        "⏳": {
            "DE": ("Eisenhower-Matrix", "Priorisiere Aufgaben nach Dringlichkeit und Wichtigkeit. Hilfreich für persönliches Zeitmanagement."),
            "EN": ("Eisenhower Matrix", "Prioritize tasks by urgency and importance. Helpful for personal time management.")
        },
        "👥": {
            "DE": ("RACI-Matrix", "Definiere Verantwortlichkeiten in Projekten. Essenziell für klare Rollenzuweisung in Teams."),
            "EN": ("RACI Matrix", "Define responsibilities in projects. Essential for clear role assignment in teams.")
        },
        "⚖️": {
            "DE": ("Balanced Scorecard", "Strategische Ziele aus verschiedenen Perspektiven. Ideal für Unternehmenssteuerung."),
            "EN": ("Balanced Scorecard", "Strategic objectives from different perspectives. Ideal for corporate management.")
        }
    }
    
    cols = st.columns(3)
    for idx, (emoji, info) in enumerate(modules_info.items()):
        with cols[idx % 3]:
            title, description = info[language]
            st.subheader(f"{emoji} {title}")
            st.write(description)
            st.button(f"Öffne {title}" if language == "DE" else f"Open {title}", key=f"btn_{idx}")

# --- TASK ANALYSIS ---
elif module == LANGUAGES[language]["modules"][1]:
    st.title("🔎 " + ("Aufgaben-Analyse" if language == "DE" else "Task Analysis"))
    
    with st.expander("ℹ️ " + ("Über dieses Tool" if language == "DE" else "About this tool")):
        st.write("""
        **📋 Methodenbeschreibung:**
        Die Aufgaben-Analyse unterscheidet zwischen drei Aufgabentypen:
        
        • **⭐ Disjunktiv**: Erfolg hängt von der besten Leistung ab (z.B. Forschung, Innovation)
        • **⛓️ Konjunktiv**: Erfolg hängt vom schwächsten Glied ab (z.B. Produktionskette)  
        • **➕ Additiv**: Jeder Beitrag zählt gleich (z.B. Crowdsourcing, Brainstorming)
        
        **🎯 Wann einsetzen?**
        - Bei der Planung von Team-Projekten
        - Zur optimalen Ressourcenverteilung
        - Für die Auswahl geeigneter Arbeitsmethoden
        
        **📝 Vorgehen:**
        1. Beantworte alle 12 Fragen ehrlich
        2. Analysiere die Ergebnisverteilung
        3. Beachte die Handlungsempfehlungen
        """)
    
    dark_mode = st.checkbox("🌙 " + ("Dark Mode aktivieren" if language == "DE" else "Activate Dark Mode"), value=False)
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
        submitted = st.form_submit_button("Analyse starten" if language == "DE" else "Start Analysis")

    if submitted:
        durchschnitt = sum([antwort for _, antwort in antworten]) / len(antworten)
        if durchschnitt < 2.0:
            st.warning("🎭 " + ("Ergebnis: Keine Aufgabe erkannt – Zeit für einen Kaffee ☕" if language == "DE" else "Result: No task recognized - time for coffee ☕"))
        else:
            for typ, antwort in antworten:
                punkte[typ] += antwort

            gesamtpunkte = sum(punkte.values())
            prozentuale_verteilung = {typ: round((wert / gesamtpunkte) * 100, 1) for typ, wert in punkte.items()}
            max_punkte = max(punkte.values())
            hybrid_typen = [typ for typ, wert in punkte.items() if max_punkte - wert <= SCHWELLENWERT_HYBRID]

            st.success(get_text("analysis_complete", language))
            
            # Export Data
            export_data = pd.DataFrame({
                'Aufgabentyp': list(punkte.keys()),
                'Punkte': list(punkte.values()),
                'Prozent': list(prozentuale_verteilung.values())
            })
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📊 " + ("Punktestände" if language == "DE" else "Points"))
                for typ, wert in punkte.items():
                    animated_progress(value=wert, max_value=7, color=colors[typ], text=f"{TYP_EMOJI[typ]} {typ.capitalize()}")
            with col2:
                st.subheader("📈 " + ("Prozentuale Verteilung" if language == "DE" else "Percentage Distribution"))
                for typ, prozent in prozentuale_verteilung.items():
                    animated_progress(value=int(prozent), max_value=100, color=colors[typ], text=f"{TYP_EMOJI[typ]} {typ.capitalize()} %", speed=0.01)

            st.divider()
            st.subheader("🎯 " + ("Empfehlung" if language == "DE" else "Recommendation"))
            typ_name = " + ".join([f"{TYP_EMOJI[typ]} {typ.capitalize()}" for typ in hybrid_typen])
            
            recommendations = {
                "disjunktiv": {
                    "DE": """**Aufgabe:** Disjunktiv ⭐ – Erfolg hängt von der besten Leistung ab.
**Stolpersteine:** Schwache Mitglieder vernachlässigt, Überlastung Spitzenkräfte.
**Strategie:** Stärken gezielt fördern, Kontrolle der Kernleistungen, Entscheidungen eher autokratisch.""",
                    "EN": """**Task:** Disjunctive ⭐ – Success depends on the best performance.
**Pitfalls:** Weak members neglected, overload of top performers.
**Strategy:** Specifically promote strengths, control core performances, rather autocratic decisions."""
                },
                "konjunktiv": {
                    "DE": """**Aufgabe:** Konjunktiv ⛓️ – Erfolg hängt vom schwächsten Glied ab.
**Stolpersteine:** Schwache Mitglieder gefährden Erfolg.
**Strategie:** Unterstützung schwacher Mitglieder, intensive Zusammenarbeit, Entscheidungen demokratisch.""",
                    "EN": """**Task:** Conjunctive ⛓️ – Success depends on the weakest link.
**Pitfalls:** Weak members endanger success.
**Strategy:** Support weak members, intensive collaboration, democratic decisions."""
                },
                "additiv": {
                    "DE": """**Aufgabe:** Additiv ➕ – Jeder Beitrag zählt.
**Stolpersteine:** Einzelne Beiträge unterschätzt, Motivation schwankt.
**Strategie:** Alle einbeziehen, Arbeit gleichmäßig verteilen, Fortschritte sichtbar machen.""",
                    "EN": """**Task:** Additive ➕ – Every contribution counts.
**Pitfalls:** Individual contributions underestimated, motivation fluctuates.
**Strategy:** Include everyone, distribute work evenly, make progress visible."""
                }
            }
            
            bericht = ""
            for typ in hybrid_typen:
                bericht += recommendations[typ][language] + "\n\n"
            
            create_colored_box(typ_name, bericht, colors["box"])
            
            # Export Buttons
            st.divider()
            st.subheader("📤 " + ("Export" if language == "DE" else "Export"))
            col_exp1, col_exp2 = st.columns(2)
            
            with col_exp1:
                if st.button(get_text("export_excel", language)):
                    st.markdown(create_download_link(export_data, "task_analysis.xlsx", "📊 Excel herunterladen"), unsafe_allow_html=True)
            
            with col_exp2:
                if st.button(get_text("export_csv", language)):
                    csv_data = export_to_csv(export_data, "task_analysis.csv")
                    st.download_button(
                        label="📝 CSV herunterladen",
                        data=csv_data,
                        file_name="task_analysis.csv",
                        mime="text/csv"
                    )

# --- SWOT ANALYSIS ---
elif module == LANGUAGES[language]["modules"][2]:
    st.title("📊 " + ("SWOT-Analyse" if language == "DE" else "SWOT Analysis"))
    
    with st.expander("ℹ️ " + ("Über dieses Tool" if language == "DE" else "About this tool")):
        st.write("""
        **📋 Methodenbeschreibung:**
        Die SWOT-Analyse ist ein strategisches Planungsinstrument zur Bewertung von:
        - **Stärken** (interne, positive Faktoren)
        - **Schwächen** (interne, negative Faktoren) 
        - **Chancen** (externe, positive Faktoren)
        - **Risiken** (externe, negative Faktoren)
        
        **🎯 Wann einsetzen?**
        - Vor wichtigen strategischen Entscheidungen
        - Bei der Unternehmens- oder Produktplanung
        - Für persönliche Karriere-Entscheidungen
        - Bei der Bewertung von Projekten oder Investitionen
        
        **📝 Vorgehen:**
        1. Sammle alle relevanten internen Stärken und Schwächen
        2. Identifiziere externe Chancen und Risiken
        3. Analysiere Wechselwirkungen zwischen den Quadranten
        4. Leite strategische Maßnahmen ab
        """)
    
    st.write("Analysiere Stärken, Schwächen, Chancen und Risiken deiner Situation.")

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💪 " + ("Interne Faktoren" if language == "DE" else "Internal Factors"))
        staerken = st.text_area("**" + ("Stärken (Strengths)" if language == "DE" else "Strengths") + "**", 
                               placeholder=("Was sind unsere Stärken?\n• Fachkompetenz\n• Ressourcen\n• Erfahrung\n• Markenimage" if language == "DE" else "What are our strengths?\n• Expertise\n• Resources\n• Experience\n• Brand image"))
        schwaechen = st.text_area("**" + ("Schwächen (Weaknesses)" if language == "DE" else "Weaknesses") + "**", 
                                 placeholder=("Wo haben wir Verbesserungspotenzial?\n• Fehlende Ressourcen\n• Prozessineffizienzen\n• Wissenslücken" if language == "DE" else "Where do we have improvement potential?\n• Missing resources\n• Process inefficiencies\n• Knowledge gaps"))
    
    with col2:
        st.subheader("🌍 " + ("Externe Faktoren" if language == "DE" else "External Factors"))
        chancen = st.text_area("**" + ("Chancen (Opportunities)" if language == "DE" else "Opportunities") + "**", 
                              placeholder=("Welche Chancen bieten sich?\n• Markttrends\n• Technologische Entwicklungen\n• Partnerschaften" if language == "DE" else "What opportunities arise?\n• Market trends\n• Technological developments\n• Partnerships"))
        risiken = st.text_area("**" + ("Risiken (Threats)" if language == "DE" else "Threats") + "**", 
                              placeholder=("Welche Risiken sehen wir?\n• Wettbewerb\n• Marktveränderungen\n• Regulatorische Änderungen" if language == "DE" else "What risks do we see?\n• Competition\n• Market changes\n• Regulatory changes"))

    if st.button("📋 " + ("SWOT-Analyse erstellen" if language == "DE" else "Create SWOT Analysis")):
        if staerken or schwaechen or chancen or risiken:
            st.success("✅ " + ("SWOT-Analyse erfolgreich erstellt!" if language == "DE" else "SWOT analysis successfully created!"))
            
            # Visual SWOT Quadrant
            create_swot_quadrant(staerken, schwaechen, chancen, risiken)
            
            # Strategic Recommendations
            st.subheader("🎯 " + ("Strategische Implikationen" if language == "DE" else "Strategic Implications"))
            col1, col2 = st.columns(2)
            
            with col1:
                if staerken and chancen:
                    st.info("**" + ("SO-Strategien (Stärken + Chancen):" if language == "DE" else "SO Strategies (Strengths + Opportunities):") + "** " + 
                           ("Nutze Stärken, um Chancen zu ergreifen" if language == "DE" else "Use strengths to seize opportunities"))
                if schwaechen and chancen:
                    st.warning("**" + ("WO-Strategien (Schwächen + Chancen):" if language == "DE" else "WO Strategies (Weaknesses + Opportunities):") + "** " + 
                              ("Überwinde Schwächen, um Chancen zu nutzen" if language == "DE" else "Overcome weaknesses to use opportunities"))
            
            with col2:
                if staerken and risiken:
                    st.success("**" + ("ST-Strategien (Stärken + Risiken):" if language == "DE" else "ST Strategies (Strengths + Threats):") + "** " + 
                              ("Verwende Stärken, um Risiken abzuwehren" if language == "DE" else "Use strengths to counter threats"))
                if schwaechen and risiken:
                    st.error("**" + ("WT-Strategien (Schwächen + Risiken):" if language == "DE" else "WT Strategies (Weaknesses + Threats):") + "** " + 
                            ("Minimiere Schwächen und vermeide Risiken" if language == "DE" else "Minimize weaknesses and avoid threats"))
            
            # Export Section
            st.divider()
            st.subheader("📤 " + ("Export" if language == "DE" else "Export"))
            
            swot_data = pd.DataFrame({
                'Kategorie': ['Stärken', 'Schwächen', 'Chancen', 'Risiken'] if language == "DE" else ['Strengths', 'Weaknesses', 'Opportunities', 'Threats'],
                'Inhalt': [staerken, schwaechen, chancen, risiken]
            })
            
            col_exp1, col_exp2 = st.columns(2)
            with col_exp1:
                if st.button(get_text("export_excel", language)):
                    st.markdown(create_download_link(swot_data, "swot_analysis.xlsx", "📊 Excel herunterladen"), unsafe_allow_html=True)
            
            with col_exp2:
                if st.button(get_text("export_csv", language)):
                    csv_data = export_to_csv(swot_data, "swot_analysis.csv")
                    st.download_button(
                        label="📝 CSV herunterladen",
                        data=csv_data,
                        file_name="swot_analysis.csv",
                        mime="text/csv"
                    )
                    
        else:
            st.warning("⚠️ " + ("Bitte fülle mindestens ein Feld aus, um die Analyse zu erstellen." if language == "DE" else "Please fill in at least one field to create the analysis."))

# --- EISENHOWER MATRIX ---
elif module == LANGUAGES[language]["modules"][3]:
    st.title("⏳ " + ("Eisenhower-Matrix" if language == "DE" else "Eisenhower Matrix"))
    
    with st.expander("ℹ️ " + ("Über dieses Tool" if language == "DE" else "About this tool")):
        st.write("""
        **📋 Methodenbeschreibung:**
        Die Eisenhower-Matrix hilft bei der Priorisierung von Aufgaben nach:
        - **Dringlichkeit** (Zeitdruck) 
        - **Wichtigkeit** (Auswirkung auf Ziele)
        
        **🎯 Die vier Quadranten:**
        1. **🔴 Q1: Wichtig & Dringend** → Sofort selbst erledigen
        2. **🟢 Q2: Wichtig & Nicht Dringend** → Terminieren und planen  
        3. **🟡 Q3: Nicht Wichtig & Dringend** → Delegieren möglich
        4. **⚫ Q4: Nicht Wichtig & Nicht Dringend** → Eliminieren oder später
        
        **📝 Vorgehen:**
        1. Liste alle anstehenden Aufgaben auf
        2. Bewerte jede Aufgabe nach Wichtigkeit und Dringlichkeit
        3. Ordne die Aufgaben den Quadranten zu
        4. Handle nach der Priorität: Q1 → Q2 → Q3 → Q4
        """)
    
    # Session State für Aufgaben initialisieren
    if 'aufgaben' not in st.session_state:
        st.session_state.aufgaben = []
    
    # Neue Aufgabe hinzufügen
    with st.form("neue_aufgabe"):
        st.subheader("➕ " + ("Neue Aufgabe hinzufügen" if language == "DE" else "Add new task"))
        aufgabe = st.text_input("Aufgabenbeschreibung" if language == "DE" else "Task description")
        wichtigkeit = st.selectbox("Wichtigkeit" if language == "DE" else "Importance", 
                                 ["Wichtig", "Nicht Wichtig"] if language == "DE" else ["Important", "Not Important"])
        dringlichkeit = st.selectbox("Dringlichkeit" if language == "DE" else "Urgency", 
                                   ["Dringend", "Nicht Dringend"] if language == "DE" else ["Urgent", "Not Urgent"])
        
        if st.form_submit_button("Aufgabe hinzufügen" if language == "DE" else "Add task"):
            if aufgabe:
                quadrant = f"Q{1 if wichtigkeit == 'Wichtig' and dringlichkeit == 'Dringend' else 2 if wichtigkeit == 'Wichtig' and dringlichkeit == 'Nicht Dringend' else 3 if wichtigkeit == 'Nicht Wichtig' and dringlichkeit == 'Dringend' else 4}"
                st.session_state.aufgaben.append({
                    "beschreibung": aufgabe,
                    "wichtigkeit": wichtigkeit,
                    "dringlichkeit": dringlichkeit,
                    "quadrant": quadrant
                })
                st.success("✅ " + ("Aufgabe hinzugefügt!" if language == "DE" else "Task added!"))
    
    # Matrix anzeigen
    if st.session_state.aufgaben:
        st.subheader("📊 " + ("Deine Eisenhower-Matrix" if language == "DE" else "Your Eisenhower Matrix"))
        create_eisenhower_matrix(st.session_state.aufgaben)
        
        # Export Section
        st.divider()
        st.subheader("📤 " + ("Export" if language == "DE" else "Export"))
        
        tasks_data = pd.DataFrame(st.session_state.aufgaben)
        
        col_exp1, col_exp2 = st.columns(2)
        with col_exp1:
            if st.button(get_text("export_excel", language)):
                st.markdown(create_download_link(tasks_data, "eisenhower_matrix.xlsx", "📊 Excel herunterladen"), unsafe_allow_html=True)
        
        with col_exp2:
            if st.button(get_text("export_csv", language)):
                csv_data = export_to_csv(tasks_data, "eisenhower_matrix.csv")
                st.download_button(
                    label="📝 CSV herunterladen",
                    data=csv_data,
                    file_name="eisenhower_matrix.csv",
                    mime="text/csv"
                )
        
        # Lösch-Button
        if st.button("🗑️ " + ("Alle Aufgaben löschen" if language == "DE" else "Delete all tasks")):
            st.session_state.aufgaben = []
            st.rerun()
    else:
        st.info("ℹ️ " + ("Füge deine ersten Aufgaben hinzu, um die Matrix zu sehen." if language == "DE" else "Add your first tasks to see the matrix."))

# --- RACI MATRIX ---  
elif module == LANGUAGES[language]["modules"][4]:
    st.title("👥 " + ("RACI-Matrix" if language == "DE" else "RACI Matrix"))
    
    with st.expander("ℹ️ " + ("Über dieses Tool" if language == "DE" else "About this tool")):
        st.write("""
        **📋 Methodenbeschreibung:**
        Die RACI-Matrix klärt Verantwortlichkeiten in Projekten:
        - **R = Responsible** → Führt die Arbeit aus (kann mehrere Personen)
        - **A = Accountable** → Trägt die Verantwortung (nur eine Person pro Aufgabe)
        - **C = Consulted** → Wird um Rat gefragt (zweiseitige Kommunikation)
        - **I = Informed** → Wird über Ergebnisse informiert (einseitige Kommunikation)
        
        **🎯 Wann einsetzen?**
        - Bei Projektstart zur Klärung von Rollen
        - Bei Schnittstellenproblemen zwischen Abteilungen
        - Für komplexe Projekte mit vielen Beteiligten
        
        **📝 Vorgehen:**
        1. Definiere alle relevanten Aufgaben/Aktivitäten
        2. Liste alle beteiligten Rollen/Personen auf
        3. Weise für jede Aufgabe RACI-Zuordnungen zu
        4. Überprüfe auf Konflikte (mehrere A's, keine R's, etc.)
        """)
    
    # Session State für RACI initialisieren
    if 'raci_aufgaben' not in st.session_state:
        st.session_state.raci_aufgaben = []
    if 'raci_rollen' not in st.session_state:
        st.session_state.raci_rollen = ["Projektleiter", "Team-Mitglied"] if language == "DE" else ["Project Manager", "Team Member"]
    
    # Rollen verwalten
    st.subheader("👥 " + ("Rollen definieren" if language == "DE" else "Define roles"))
    col1, col2 = st.columns([3, 1])
    
    with col1:
        neue_rolle = st.text_input("Neue Rolle hinzufügen" if language == "DE" else "Add new role")
    
    with col2:
        if st.button("Rolle hinzufügen" if language == "DE" else "Add role") and neue_rolle:
            st.session_state.raci_rollen.append(neue_rolle)
            st.rerun()
    
    # Aufgaben verwalten
    st.subheader("📋 " + ("Aufgaben definieren" if language == "DE" else "Define tasks"))
    with st.form("neue_raci_aufgabe"):
        aufgaben_beschreibung = st.text_input("Aufgabenbeschreibung" if language == "DE" else "Task description")
        
        # RACI Auswahl für jede Rolle
        raci_zuweisungen = {}
        for rolle in st.session_state.raci_rollen:
            raci_zuweisungen[rolle] = st.selectbox(
                f"RACI für {rolle}",
                ["-", "R", "A", "C", "I"],
                key=f"raci_{rolle}"
            )
        
        if st.form_submit_button("Aufgabe hinzufügen" if language == "DE" else "Add task"):
            if aufgaben_beschreibung:
                st.session_state.raci_aufgaben.append({
                    "beschreibung": aufgaben_beschreibung,
                    "zuweisungen": raci_zuweisungen.copy()
                })
                st.success("✅ " + ("Aufgabe hinzugefügt!" if language == "DE" else "Task added!"))
    
    # RACI Matrix anzeigen
    if st.session_state.raci_aufgaben:
        st.subheader("📊 " + ("RACI-Matrix" if language == "DE" else "RACI Matrix"))
        
        # Tabellenkopf
        header = "| " + ("Aufgabe" if language == "DE" else "Task") + " | " + " | ".join(st.session_state.raci_rollen) + " |"
        separator = "|" + "|".join(["---"] * (len(st.session_state.raci_rollen) + 1)) + "|"
        
        # Tabellenzeilen
        rows = []
        for aufgabe in st.session_state.raci_aufgaben:
            zuweisungen = " | ".join([aufgabe["zuweisungen"][rolle] for rolle in st.session_state.raci_rollen])
            rows.append(f"| {aufgabe['beschreibung']} | {zuweisungen} |")
        
        # Tabelle anzeigen
        markdown_table = "\n".join([header, separator] + rows)
        st.markdown(markdown_table)
        
        # Legende
        st.markdown("""
        **""" + ("Legende:" if language == "DE" else "Legend:") + """**
        - **R** = """ + ("Responsible (Verantwortlich)" if language == "DE" else "Responsible") + """
        - **A** = """ + ("Accountable (Rechenschaftspflichtig)" if language == "DE" else "Accountable") + """
        - **C** = """ + ("Consulted (Konsultiert)" if language == "DE" else "Consulted") + """
        - **I** = """ + ("Informed (Informiert)" if language == "DE" else "Informed") + """
        """)
        
        # Export Section
        st.divider()
        st.subheader("📤 " + ("Export" if language == "DE" else "Export"))
        
        # Prepare data for export
        export_data = []
        for aufgabe in st.session_state.raci_aufgaben:
            row = {"Aufgabe": aufgabe["beschreibung"]}
            for rolle in st.session_state.raci_rollen:
                row[rolle] = aufgabe["zuweisungen"][rolle]
            export_data.append(row)
        
        raci_df = pd.DataFrame(export_data)
        
        col_exp1, col_exp2 = st.columns(2)
        with col_exp1:
            if st.button(get_text("export_excel", language)):
                st.markdown(create_download_link(raci_df, "raci_matrix.xlsx", "📊 Excel herunterladen"), unsafe_allow_html=True)
        
        with col_exp2:
            if st.button(get_text("export_csv", language)):
                csv_data = export_to_csv(raci_df, "raci_matrix.csv")
                st.download_button(
                    label="📝 CSV herunterladen",
                    data=csv_data,
                    file_name="raci_matrix.csv",
                    mime="text/csv"
                )
        
        if st.button("🗑️ " + ("RACI-Matrix löschen" if language == "DE" else "Delete RACI Matrix")):
            st.session_state.raci_aufgaben = []
            st.rerun()
    else:
        st.info("ℹ️ " + ("Definiere Rollen und Aufgaben, um die RACI-Matrix zu erstellen." if language == "DE" else "Define roles and tasks to create the RACI matrix."))

# --- BALANCED SCORECARD ---
elif module == LANGUAGES[language]["modules"][5]:
    st.title("⚖️ " + ("Balanced Scorecard" if language == "DE" else "Balanced Scorecard"))
    
    with st.expander("ℹ️ " + ("Über dieses Tool" if language == "DE" else "About this tool")):
        st.write("""
        **📋 Methodenbeschreibung:**
        Die Balanced Scorecard betrachtet strategische Ziele aus vier Perspektiven:
        1. **💰 Finanzen** → Wirtschaftliche Erfolgsziele
        2. **👥 Kunden** → Kundenorientierte Ziele  
        3. **⚙️ Interne Prozesse** → Prozessoptimierung und Effizienz
        4. **📚 Lernen & Entwicklung** → Mitarbeiterentwicklung und Innovation
        
        **🎯 Wann einsetzen?**
        - Für strategische Unternehmenssteuerung
        - Bei der Umsetzung von Unternehmensvisionen
        - Für die Leistungsmessung auf mehreren Ebenen
        - Bei der Verbindung operativer und strategischer Ziele
        
        **📝 Vorgehen:**
        1. Definiere Vision und Strategie
        2. Leite Ziele für jede Perspektive ab
        3. Definiere Kennzahlen und Zielwerte
        4. Plane konkrete Maßnahmen
        5. Überwache und passe regelmäßig an
        """)
    
    # Session State für BSC initialisieren
    if 'bsc_ziele' not in st.session_state:
        st.session_state.bsc_ziele = []
    
    # Neue Ziele hinzufügen
    with st.form("neues_bsc_ziel"):
        st.subheader("🎯 " + ("Neues Ziel hinzufügen" if language == "DE" else "Add new objective"))
        
        perspektive = st.selectbox(
            "Perspektive" if language == "DE" else "Perspective",
            ["Finanzen", "Kunden", "Interne Prozesse", "Lernen & Entwicklung"] if language == "DE" 
            else ["Financial", "Customer", "Internal Processes", "Learning & Growth"]
        )
        
        ziel = st.text_input("Strategisches Ziel" if language == "DE" else "Strategic objective")
        kennzahl = st.text_input("Kennzahl / Messgröße" if language == "DE" else "KPI / Metric")
        zielwert = st.text_input("Zielwert" if language == "DE" else "Target value")
        massnahmen = st.text_area("Erforderliche Maßnahmen" if language == "DE" else "Required measures")
        
        if st.form_submit_button("Ziel hinzufügen" if language == "DE" else "Add objective"):
            if ziel and kennzahl:
                st.session_state.bsc_ziele.append({
                    "perspektive": perspektive,
                    "ziel": ziel,
                    "kennzahl": kennzahl,
                    "zielwert": zielwert,
                    "massnahmen": massnahmen
                })
                st.success("✅ " + ("Ziel hinzugefügt!" if language == "DE" else "Objective added!"))
    
    # Balanced Scorecard anzeigen
    if st.session_state.bsc_ziele:
        st.subheader("📈 " + ("Deine Balanced Scorecard" if language == "DE" else "Your Balanced Scorecard"))
        
        perspektiven = {
            "Finanzen": {"emoji": "💰", "color": "#e9ecef"},
            "Kunden": {"emoji": "👥", "color": "#d8f3dc"}, 
            "Interne Prozesse": {"emoji": "⚙️", "color": "#fff3cd"},
            "Lernen & Entwicklung": {"emoji": "📚", "color": "#cce7ff"}
        } if language == "DE" else {
            "Financial": {"emoji": "💰", "color": "#e9ecef"},
            "Customer": {"emoji": "👥", "color": "#d8f3dc"},
            "Internal Processes": {"emoji": "⚙️", "color": "#fff3cd"},
            "Learning & Growth": {"emoji": "📚", "color": "#cce7ff"}
        }
        
        for perspektive, info in perspektiven.items():
            perspektive_ziele = [z for z in st.session_state.bsc_ziele if z["perspektive"] == perspektive]
            
            if perspektive_ziele:
                st.markdown(f"""
                <div style='background-color: {info['color']}; padding: 15px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #495057;'>
                    <h4>{info['emoji']} {perspektive}</h4>
                </div>
                """, unsafe_allow_html=True)
                
                for ziel in perspektive_ziele:
                    with st.expander(f"🎯 {ziel['ziel']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**" + ("Kennzahl:" if language == "DE" else "KPI:") + f"** {ziel['kennzahl']}")
                            st.write(f"**" + ("Zielwert:" if language == "DE" else "Target value:") + f"** {ziel['zielwert']}")
                        with col2:
                            st.write(f"**" + ("Maßnahmen:" if language == "DE" else "Measures:") + f"** {ziel['massnahmen']}")
        
        # Zusammenfassung
        st.subheader("📊 " + ("Zusammenfassung" if language == "DE" else "Summary"))
        col1, col2, col3, col4 = st.columns(4)
        
        for i, (perspektive, info) in enumerate(perspektiven.items()):
            anzahl = len([z for z in st.session_state.bsc_ziele if z["perspektive"] == perspektive])
            with [col1, col2, col3, col4][i]:
                st.metric(f"{info['emoji']} {perspektive}", anzahl)
        
        # Export Section
        st.divider()
        st.subheader("📤 " + ("Export" if language == "DE" else "Export"))
        
        bsc_data = pd.DataFrame(st.session_state.bsc_ziele)
        
        col_exp1, col_exp2 = st.columns(2)
        with col_exp1:
            if st.button(get_text("export_excel", language)):
                st.markdown(create_download_link(bsc_data, "balanced_scorecard.xlsx", "📊 Excel herunterladen"), unsafe_allow_html=True)
        
        with col_exp2:
            if st.button(get_text("export_csv", language)):
                csv_data = export_to_csv(bsc_data, "balanced_scorecard.csv")
                st.download_button(
                    label="📝 CSV herunterladen",
                    data=csv_data,
                    file_name="balanced_scorecard.csv",
                    mime="text/csv"
                )
        
        if st.button("🗑️ " + ("Alle Ziele löschen" if language == "DE" else "Delete all objectives")):
            st.session_state.bsc_ziele = []
            st.rerun()
    else:
        st.info("ℹ️ " + ("Füge strategische Ziele hinzu, um deine Balanced Scorecard zu erstellen." if language == "DE" else "Add strategic objectives to create your Balanced Scorecard."))

# --- GLOBAL EXPORT IN SIDEBAR ---
st.sidebar.markdown("---")
st.sidebar.subheader("📤 " + ("Globale Export-Funktionen" if language == "DE" else "Global Export Features"))

# Placeholder for global export functionality
st.sidebar.info("ℹ️ " + ("Export-Funktionen sind in den einzelnen Modulen verfügbar." if language == "DE" else "Export features are available in individual modules."))

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.markdown("**🧭 Decision Compass**  \n" + 
                   ("Ein umfassendes Tool für strategische Entscheidungsfindung" if language == "DE" else "A comprehensive tool for strategic decision making"))
