import streamlit as st
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_pdf import PdfPages
import io
import textwrap
import json

# -------------------------
# Decision Compass - Modular, Export, Visuals, Mehrsprachig
# -------------------------

st.set_page_config(page_title="Decision Compass", layout="wide")

# --- Minimaler Sprachkern (DE / EN) ---
LANG = {
    "de": {
        "home_title": "🧭 Decision Compass",
        "home_intro": "Ein Tool, das gängige Management-Methoden unter einem Dach vereint.",
        "choose_module": "Wähle Modul:",
        "modules": ["🏠 Start", "🔎 Aufgaben-Analyse", "📊 SWOT-Analyse", "⏳ Eisenhower-Matrix", "👥 RACI-Matrix", "⚖️ Balanced Scorecard"],
        "download_pdf": "PDF herunterladen",
        "download_excel": "Excel herunterladen",
        "export_all": "Gesamtratgeber exportieren",
        "lang_label": "Sprache"
    },
    "en": {
        "home_title": "🧭 Decision Compass",
        "home_intro": "A tool that unites common management frameworks in one place.",
        "choose_module": "Choose module:",
        "modules": ["🏠 Start", "🔎 Task Analysis", "📊 SWOT Analysis", "⏳ Eisenhower Matrix", "👥 RACI Matrix", "⚖️ Balanced Scorecard"],
        "download_pdf": "Download PDF",
        "download_excel": "Download Excel",
        "export_all": "Export full report",
        "lang_label": "Language"
    }
}

# --- Sidebar: Sprache + Navigation ---
lang = st.sidebar.selectbox("Sprache / Language", options=["DE", "EN"], index=0)
L = LANG["de"] if lang == "DE" else LANG["en"]

st.sidebar.title(L["home_title"])
module = st.sidebar.radio(L["choose_module"], L["modules"])

# -------------------------
# Utility Funktionen (zentral, damit Code schlank bleibt)
# -------------------------

def format_text_for_html(text):
    """Wandelt Zeilen in HTML-Listenelemente um"""
    if not text:
        return "<em>Keine Einträge</em>"
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if not lines:
        return "<em>Keine Einträge</em>"
    # sichere Zeichenbrechung
    lines_wrapped = [textwrap.fill(ln, width=60) for ln in lines]
    return "<br>• " + "<br>• ".join(lines_wrapped)


def render_box(title, body_html, color_left="#000000", bg="#f8f9fa"):
    st.markdown(f"""
    <div style='background:{bg}; padding:12px; border-radius:10px; margin-bottom:10px; border-left:6px solid {color_left}'>
      <h4 style='margin:0 0 8px 0'>{title}</h4>
      <div style='line-height:1.35'>{body_html}</div>
    </div>
    """, unsafe_allow_html=True)


def animated_progress(value, max_value, color, text, speed=0.01):
    placeholder = st.empty()
    max_value = max(1, max_value)
    steps = int(max(1, min(value, max_value)))
    for i in range(1, steps + 1):
        pct = min(i / max_value, 1.0)
        placeholder.progress(pct, text=f"{text}: {i}")
        time.sleep(speed)
    st.markdown(f"<span style='color:{color}; font-weight:bold'>{text}: {value}</span>", unsafe_allow_html=True)


def to_excel_bytes(sheets: dict):
    """Erzeugt Excel im Arbeitsspeicher. sheets: dict mit name -> DataFrame"""
    output = io.BytesIO()
    try:
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            for name, df in sheets.items():
                if isinstance(df, pd.DataFrame):
                    df.to_excel(writer, sheet_name=name[:31], index=False)
                else:
                    pd.DataFrame(df).to_excel(writer, sheet_name=name[:31], index=False)
            writer.save()
    except Exception:
        # Fallback: einfacher Excel mit pandas (kann kleiner Formatverlust haben)
        with pd.ExcelWriter(output) as writer:
            for name, df in sheets.items():
                pd.DataFrame(df).to_excel(writer, sheet_name=name[:31], index=False)
    output.seek(0)
    return output


def figs_to_pdf_bytes(figs):
    buf = io.BytesIO()
    with PdfPages(buf) as pdf:
        for fig in figs:
            pdf.savefig(fig, bbox_inches='tight')
            plt.close(fig)
    buf.seek(0)
    return buf

# -------------------------
# Visual Helfer: Plots
# -------------------------

def create_swot_figure(staerken, schwaechen, chancen, risiken):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 2)
    ax.axis('off')

    # Rechtecke füllen (vier Felder)
    ax.add_patch(patches.Rectangle((0, 1), 1, 1, facecolor='#d4edda', edgecolor='none'))  # Stärken
    ax.add_patch(patches.Rectangle((1, 1), 1, 1, facecolor='#f8d7da', edgecolor='none'))  # Schwächen
    ax.add_patch(patches.Rectangle((0, 0), 1, 1, facecolor='#cce7ff', edgecolor='none'))  # Chancen
    ax.add_patch(patches.Rectangle((1, 0), 1, 1, facecolor='#fff3cd', edgecolor='none'))  # Risiken

    # Titel in Feldern
    ax.text(0.5, 1.85, 'Stärken', ha='center', va='center', fontsize=12, weight='bold', color='#155724')
    ax.text(1.5, 1.85, 'Schwächen', ha='center', va='center', fontsize=12, weight='bold', color='#721c24')
    ax.text(0.5, 0.85, 'Chancen', ha='center', va='center', fontsize=12, weight='bold', color='#004085')
    ax.text(1.5, 0.85, 'Risiken', ha='center', va='center', fontsize=12, weight='bold', color='#856404')

    # Inhalte platzieren
    def place_text(box_x, box_y, text_lines):
        x = box_x + 0.05
        y = box_y + 0.8
        wrapped = [textwrap.fill(ln, 40) for ln in text_lines]
        ax.text(x, y, '
'.join(['• ' + ln for ln in wrapped]), ha='left', va='top', fontsize=10)

    place_text(0, 1, [ln for ln in staerken.splitlines() if ln.strip()])
    place_text(1, 1, [ln for ln in schwaechen.splitlines() if ln.strip()])
    place_text(0, 0, [ln for ln in chancen.splitlines() if ln.strip()])
    place_text(1, 0, [ln for ln in risiken.splitlines() if ln.strip()])

    return fig


def create_eisenhower_figure(tasks):
    fig, axes = plt.subplots(2, 2, figsize=(8, 8))
    plt.subplots_adjust(hspace=0.3)
    # Quadrant Farben
    colors = [['#ff6b6b', '#51cf66'], ['#ffd43b', '#868e96']]
    titles = [['Q1: Wichtig & Dringend', 'Q2: Wichtig & Nicht Dringend'], ['Q3: Nicht Wichtig & Dringend', 'Q4: Nicht Wichtig & Nicht Dringend']]

    # Gruppen
    groups = {'Q1': [], 'Q2': [], 'Q3': [], 'Q4': []}
    for t in tasks:
        q = t.get('quadrant')
        groups.setdefault(q, []).append(t['beschreibung'])

    for i in range(2):
        for j in range(2):
            ax = axes[i, j]
            ax.axis('off')
            ax.set_facecolor('#ffffff')
            col = colors[i][j]
            ax.add_patch(patches.Rectangle((0, 0), 1, 1, facecolor=col + '20', edgecolor='none'))
            ax.text(0.5, 0.95, titles[i][j], ha='center', va='top', fontsize=12, weight='bold')
            items = groups[['Q1','Q2','Q3','Q4'][i*2+j]]
            y = 0.8
            for it in items:
                ax.text(0.05, y, f'• {it}', fontsize=10, va='top')
                y -= 0.1
    return fig

# -------------------------
# Module: Start
# -------------------------
if module.startswith('🏠'):
    st.title(L['home_title'])
    st.write(L['home_intro'])
    st.divider()
    st.subheader('Kurz:')
    st.write('- Task Analyse: Typbestimmung (disjunktiv / konjunktiv / additiv)')
    st.write('- SWOT: 4-Felder mit Handlungsvorlagen')
    st.write('- Eisenhower: Priorität nach Wichtig/Dringend')
    st.write('- RACI: Rollen & Verantwortungen')
    st.write('- BSC: Ziele & KPI in 4 Perspektiven')
    st.divider()
    st.info('Nutze Menu links, um Modul zu wählen. Export per Button am Modulende.')

# -------------------------
# Module: Aufgaben-Analyse
# -------------------------
elif module.startswith('🔎'):
    st.title('🔎 Aufgaben-Analyse')

    colors = {"disjunktiv": "#E63946", "konjunktiv": "#F1FA3C", "additiv": "#2A9D8F"}

    st.write('Beantworte 12 kurze Fragen auf einer Skala von 1 bis 7.')
    fragen = [
        {"text": "Je mehr Mitglieder aktiv mitwirken, desto besser – auch kleine Beiträge summieren sich.", "typ": "additiv"},
        {"text": "Wenn auch nur eine Person ihre Aufgabe nicht erfüllt, ist das Projekt gefährdet.", "typ": "konjunktiv"},
        {"text": "Eine einzelne Spitzenidee kann den gesamten Erfolg sicherstellen.", "typ": "disjunktiv"},
        {"text": "Die Kooperation leidet, wenn ein Mitglied nicht nötige Qualität liefert.", "typ": "konjunktiv"},
        {"text": "Erfolg entsteht durch die Summe vieler Beiträge, nicht nur Spitzenleistung.", "typ": "additiv"},
        {"text": "Die Leistung der besten Person entscheidet oft über Erfolg.", "typ": "disjunktiv"},
        {"text": "Fehler einzelner wirken stark auf Gesamtleistung.", "typ": "konjunktiv"},
        {"text": "Wenn alle gleichmäßig mitwirken, steigt Erfolgswahrscheinlichkeit.", "typ": "disjunktiv"},
        {"text": "Die Leistung des schwächsten Mitglieds bestimmt oft das Ergebnis.", "typ": "konjunktiv"},
        {"text": "Jeder Beitrag trägt bei, ein Ausfall führt nicht sofort zum Scheitern.", "typ": "additiv"},
        {"text": "Kleine, regelm. Beiträge können zusammen sehr stark werden.", "typ": "additiv"},
        {"text": "Für Erfolg reicht oft, wenn eine Person Aufgabe vollständig meistert.", "typ": "disjunktiv"},
    ]

    if 'antworten' not in st.session_state:
        st.session_state.antworten = [4] * len(fragen)

    with st.form('form_aufgaben'):
        for i, f in enumerate(fragen, start=1):
            st.write(f"{i}. {f['text']}")
            val = st.slider('', 1, 7, st.session_state.antworten[i-1], key=f"a_{i}")
            st.session_state.antworten[i-1] = val
        if st.form_submit_button('Analyse starten'):
            # Auswertung
            punkte = {'disjunktiv': 0, 'konjunktiv': 0, 'additiv': 0}
            for ans, f in zip(st.session_state.antworten, fragen):
                punkte[f['typ']] += ans
            ges = sum(punkte.values()) or 1
            proz = {k: round(v/ges*100,1) for k,v in punkte.items()}

            st.subheader('Ergebnis')
            for k,v in punkte.items():
                animated_progress(v, 7, colors[k], f"{k} ({proz[k]}%)")

            # Empfehlung
            emp = []
            if punkte['disjunktiv'] == max(punkte.values()):
                emp.append('Disjunktiv: Fokus auf Spitzenleistung, klare Kernverantwortung.')
            if punkte['konjunktiv'] == max(punkte.values()):
                emp.append('Konjunktiv: Support für schwache Teammitgl, enge Koordination.')
            if punkte['additiv'] == max(punkte.values()):
                emp.append('Additiv: Alle einbinden, Microziele, Sichtbarkeit von Fortschritt.')

            render_box('Empfehlung', '<br>'.join(emp), color_left='#0d6efd')

# -------------------------
# Module: SWOT
# -------------------------
elif module.startswith('📊'):
    st.title('📊 SWOT-Analyse')
    col1, col2 = st.columns(2)
    with col1:
        staerken = st.text_area('Stärken (eine pro Zeile)')
        chancen = st.text_area('Chancen (eine pro Zeile)')
    with col2:
        schwaechen = st.text_area('Schwächen (eine pro Zeile)')
        risiken = st.text_area('Risiken (eine pro Zeile)')

    if st.button('SWOT visualisieren / exportieren'):
        fig = create_swot_figure(staerken, schwaechen, chancen, risiken)
        st.pyplot(fig)

        # Excel
        df_swot = pd.DataFrame({'Stärken': [ln for ln in staerken.splitlines() if ln.strip()],
                                'Schwächen': pd.NA,
                                'Chancen': pd.NA,
                                'Risiken': pd.NA})
        # Sicherer Aufbau: jede Spalte als eigene Liste der gleichen Länge
        maxlen = max(len(staerken.splitlines()), len(schwaechen.splitlines()), len(chancen.splitlines()), len(risiken.splitlines()))
        def col_list(txt):
            lst = [ln for ln in txt.splitlines() if ln.strip()]
            lst += [''] * (maxlen - len(lst))
            return lst
        sheets = {
            'SWOT': pd.DataFrame({
                'Stärken': col_list(staerken),
                'Schwächen': col_list(schwaechen),
                'Chancen': col_list(chancen),
                'Risiken': col_list(risiken)
            })
        }
        excel_bytes = to_excel_bytes(sheets)
        st.download_button(L['download_excel'], data=excel_bytes, file_name='swot.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        # PDF mit Plot
        pdf_bytes = figs_to_pdf_bytes([fig])
        st.download_button(L['download_pdf'], data=pdf_bytes, file_name='swot.pdf', mime='application/pdf')

    # Anleitung
    with st.expander('Wie vorgehen?'):
        st.write('''
- Formuliere klare, kurze Stichpunkte pro Feld.
- Nutze SO / WO / ST / WT Ableitungen, um Handlungsfelder zu definieren.
- Priorisiere 2–3 Kerninitiativen aus Kombinationen der Felder.
''')

# -------------------------
# Module: Eisenhower
# -------------------------
elif module.startswith('⏳'):
    st.title('⏳ Eisenhower-Matrix')
    if 'e_tasks' not in st.session_state:
        st.session_state.e_tasks = []

    with st.form('e_task_form'):
        tname = st.text_input('Aufgabe')
        wichtig = st.checkbox('Wichtig', value=True)
        dringend = st.checkbox('Dringend', value=False)
        if st.form_submit_button('Hinzufügen') and tname:
            quad = 'Q1' if wichtig and dringend else 'Q2' if wichtig and not dringend else 'Q3' if not wichtig and dringend else 'Q4'
            st.session_state.e_tasks.append({'beschreibung': tname, 'quadrant': quad})
            st.experimental_rerun()

    if st.session_state.e_tasks:
        fig = create_eisenhower_figure(st.session_state.e_tasks)
        st.pyplot(fig)

        # Excel
        df_tasks = pd.DataFrame(st.session_state.e_tasks)
        excel = to_excel_bytes({'Eisenhower': df_tasks})
        st.download_button(L['download_excel'], data=excel, file_name='eisenhower.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        # PDF
        pdf = figs_to_pdf_bytes([fig])
        st.download_button(L['download_pdf'], data=pdf, file_name='eisenhower.pdf', mime='application/pdf')

    with st.expander('Vorgehen'):
        st.write('''
- Sammle alle Aufgaben für ein konkretes Projekt oder einen Tag.
- Bewerte Wichtigkeit und Dringlichkeit real.
- Handle Q1 sofort, plane Q2, delegiere Q3, und streiche Q4.
''')

# -------------------------
# Module: RACI
# -------------------------
elif module.startswith('👥'):
    st.title('👥 RACI-Matrix')
    if 'raci_roles' not in st.session_state:
        st.session_state.raci_roles = ['Projektleitung', 'Team']
    if 'raci_tasks' not in st.session_state:
        st.session_state.raci_tasks = []

    st.subheader('Rollen')
    col1, col2 = st.columns([3,1])
    with col1:
        new_role = st.text_input('Neue Rolle')
    with col2:
        if st.button('Rolle anlegen') and new_role:
            st.session_state.raci_roles.append(new_role)
            st.experimental_rerun()

    st.subheader('Aufgabe mit Zuweisung')
    with st.form('raci_task_form'):
        task = st.text_input('Aufgabenbezeichnung')
        assigns = {}
        for r in st.session_state.raci_roles:
            assigns[r] = st.selectbox(f'{r}', ['-', 'R', 'A', 'C', 'I'], key=f'r_{r}_{len(st.session_state.raci_tasks)}')
        if st.form_submit_button('Zuweisen') and task:
            st.session_state.raci_tasks.append({'aufgabe': task, 'zuweisungen': assigns})
            st.experimental_rerun()

    if st.session_state.raci_tasks:
        rows = []
        for t in st.session_state.raci_tasks:
            row = {'Aufgabe': t['aufgabe']}
            row.update(t['zuweisungen'])
            rows.append(row)
        df = pd.DataFrame(rows)
        st.dataframe(df)

        # Export
        excel = to_excel_bytes({'RACI': df})
        st.download_button(L['download_excel'], data=excel, file_name='raci.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    with st.expander('Hinweis'):
        st.write('RACI hilft, Klarheit bei Rollen zu schaffen. Nutze es in Kickoff Meeting, wenn Aufgaben klar verteilt werden.')

# -------------------------
# Module: Balanced Scorecard
# -------------------------
elif module.startswith('⚖️'):
    st.title('⚖️ Balanced Scorecard')
    if 'bsc' not in st.session_state:
        st.session_state.bsc = []

    with st.form('bsc_form'):
        pers = st.selectbox('Perspektive', ['Finanzen', 'Kunden', 'Interne Prozesse', 'Lernen & Entwicklung'])
        ziel = st.text_input('Ziel')
        kpi = st.text_input('KPI')
        zielwert = st.text_input('Zielwert')
        mass = st.text_area('Maßnahme')
        if st.form_submit_button('Ziel anlegen') and ziel and kpi:
            st.session_state.bsc.append({'perspektive': pers, 'ziel': ziel, 'kpi': kpi, 'zielwert': zielwert, 'massnahme': mass})
            st.experimental_rerun()

    if st.session_state.bsc:
        df = pd.DataFrame(st.session_state.bsc)
        st.dataframe(df)
        # Zusammenfassung als Balken
        counts = df['perspektive'].value_counts()
        fig, ax = plt.subplots(figsize=(6,3))
        counts.plot.bar(ax=ax)
        ax.set_ylabel('Anzahl Ziele')
        st.pyplot(fig)

        excel = to_excel_bytes({'BSC': df})
        st.download_button(L['download_excel'], data=excel, file_name='bsc.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        pdf = figs_to_pdf_bytes([fig])
        st.download_button(L['download_pdf'], data=pdf, file_name='bsc.pdf', mime='application/pdf')

    with st.expander('Vorgehen'):
        st.write('''
- Formuliere für jede Perspektive 2–3 klare Ziele.
- Lege KPI fest, die messbar sind.
- Definiere Maßnahme, die Ziel erreicht.
- Review zyklisch, z. B. quartal.
''')

# -------------------------
# Export gesamter Bericht (alle aktiven Module)
# -------------------------

# Sammler für alle Daten (einfacher Export)
all_sheets = {}
if 'e_tasks' in st.session_state and st.session_state.e_tasks:
    all_sheets['Eisenhower'] = pd.DataFrame(st.session_state.e_tasks)
if 'raci_tasks' in st.session_state and st.session_state.raci_tasks:
    rows = []
    for t in st.session_state.raci_tasks:
        row = {'Aufgabe': t['aufgabe']}
        row.update(t['zuweisungen'])
        rows.append(row)
    all_sheets['RACI'] = pd.DataFrame(rows)
if 'bsc' in st.session_state and st.session_state.bsc:
    all_sheets['BSC'] = pd.DataFrame(st.session_state.bsc)
# SWOT kann man bei Bedarf hinzufügen hier, via same logic

if all_sheets:
    st.sidebar.divider()
    st.sidebar.subheader('Export')
    excel_all = to_excel_bytes(all_sheets)
    st.sidebar.download_button(L['download_excel'], data=excel_all, file_name='decision_compass_export.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    # PDF: wir bauen einfache PDF mit Plots falls vorhanden
    figs = []
    # If SWOT plot present in current session show add
    # For demo: add empty
    if figs:
        pdf_all = figs_to_pdf_bytes(figs)
        st.sidebar.download_button(L['download_pdf'], data=pdf_all, file_name='decision_compass_report.pdf', mime='application/pdf')

# Ende Datei
