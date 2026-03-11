import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import re

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="☠️ Cocktail Simulator — Ce que tu manges vraiment",
    page_icon="☠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── GLOBAL CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Bebas+Neue&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --bg:       #080B0F;
    --surface:  #0F1318;
    --border:   #1E252E;
    --red:      #FF2D2D;
    --orange:   #FF6B1A;
    --yellow:   #FFD600;
    --green:    #00FF88;
    --dim:      #4A5568;
    --text:     #E2E8F0;
    --muted:    #718096;
}

html, body, [class*="css"] {
    background-color: var(--bg) !important;
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem; max-width: 1400px; }

/* ── HERO TITLE ── */
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(3rem, 7vw, 6rem);
    line-height: 0.9;
    letter-spacing: 0.02em;
    background: linear-gradient(135deg, #FF2D2D 0%, #FF6B1A 40%, #FFD600 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
}
.hero-sub {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: var(--muted);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 0.5rem;
}

/* ── SCORE GAUGE ── */
.gauge-container {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.gauge-container::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--red), var(--orange), var(--yellow));
}
.score-number {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 5rem;
    line-height: 1;
    margin: 0;
}
.score-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--muted);
    margin-top: 0.25rem;
}

/* ── ADDITIVE CARDS ── */
.additive-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    transition: border-color 0.2s;
    position: relative;
    overflow: hidden;
}
.add-code {
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
    font-weight: 700;
    min-width: 60px;
}
.add-name { font-size: 0.9rem; font-weight: 500; flex: 1; }
.add-diseases {
    font-size: 0.7rem;
    color: var(--muted);
    line-height: 1.4;
    flex: 2;
}
.add-score {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    min-width: 30px;
    text-align: right;
}
.risk-bar {
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 4px;
}

/* ── DISEASE TAGS ── */
.disease-tag {
    display: inline-block;
    font-size: 0.6rem;
    font-family: 'Space Mono', monospace;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    padding: 2px 8px;
    border-radius: 100px;
    margin: 2px;
    font-weight: 700;
}

/* ── METRIC BOXES ── */
.metric-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.25rem;
    text-align: center;
}
.metric-val {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.2rem;
    line-height: 1;
}
.metric-lab {
    font-size: 0.7rem;
    color: var(--muted);
    font-family: 'Space Mono', monospace;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

/* ── SIDEBAR ── */
.css-1d391kg, [data-testid="stSidebar"] {
    background-color: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .stTextInput input {
    background: var(--bg) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    font-family: 'Space Mono', monospace !important;
}
.stTextInput input:focus { border-color: var(--red) !important; box-shadow: 0 0 0 2px rgba(255,45,45,0.2) !important; }

/* ── BUTTONS ── */
.stButton button {
    background: var(--red) !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    padding: 0.5rem 1.2rem !important;
    transition: opacity 0.2s !important;
}
.stButton button:hover { opacity: 0.8 !important; }

/* ── DIVIDER ── */
.toxic-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 1.5rem 0;
}

/* ── ALERT BOX ── */
.alert-box {
    background: rgba(255, 45, 45, 0.08);
    border: 1px solid rgba(255, 45, 45, 0.3);
    border-radius: 10px;
    padding: 1rem 1.25rem;
    font-size: 0.85rem;
}
.alert-box b { color: var(--red); }

/* ── VERDICT ── */
.verdict-text {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.8rem;
    letter-spacing: 0.05em;
}

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
#  DATA — Dictionnaire scientifique complet
# ═══════════════════════════════════════════════════════════════════════════

ADDITIVES_DB = {
    # ── SCORE 3 — Danger établi ─────────────────────────────────────
    "E102": {
        "name": "Tartrazine",
        "score": 3,
        "type": "Colorant",
        "diseases": ["TDAH", "Hyperactivité", "Allergie", "Asthme"],
        "detail": "Colorant azoïque jaune interdit ou déconseillé dans plusieurs pays. Lié à l'hyperactivité chez les enfants dans des études EFSA."
    },
    "E110": {
        "name": "Sunset Yellow FCF",
        "score": 3,
        "type": "Colorant",
        "diseases": ["TDAH", "Allergie", "Asthme"],
        "detail": "Colorant azoïque orange. Fait partie du 'cocktail Southampton' lié au TDAH infantile. Étiquetage avertissement obligatoire en UE."
    },
    "E122": {
        "name": "Carmoisine (Azorubine)",
        "score": 3,
        "type": "Colorant",
        "diseases": ["TDAH", "Allergie", "Hyperactivité"],
        "detail": "Colorant rouge azoïque. Interdit aux États-Unis et en Australie. Lié au comportement hyperactif chez les enfants."
    },
    "E123": {
        "name": "Amarante",
        "score": 3,
        "type": "Colorant",
        "diseases": ["Cancer potentiel", "Allergie"],
        "detail": "Interdit aux États-Unis depuis 1976 (suspicion cancérigène). Encore autorisé dans certains pays pour le caviar."
    },
    "E124": {
        "name": "Ponceau 4R",
        "score": 3,
        "type": "Colorant",
        "diseases": ["TDAH", "Allergie", "Asthme"],
        "detail": "Colorant azoïque rouge. Partie du cocktail Southampton. Interdit aux États-Unis."
    },
    "E129": {
        "name": "Allura Red AC",
        "score": 3,
        "type": "Colorant",
        "diseases": ["TDAH", "Allergie", "Hyperactivité"],
        "detail": "Colorant rouge très répandu (15% des snacks). Cocktail Southampton. Déconseillé aux enfants par l'EFSA."
    },
    "E171": {
        "name": "Dioxyde de Titane",
        "score": 3,
        "type": "Colorant",
        "diseases": ["Cancer potentiel", "Inflammation intestinale", "Génotoxicité"],
        "detail": "Classé 'cancérigène possible' par l'IARC en 2006. Interdit dans l'UE depuis 2022. Toujours utilisé hors UE."
    },
    "E211": {
        "name": "Benzoate de Sodium",
        "score": 3,
        "type": "Conservateur",
        "diseases": ["TDAH", "Leucémie potentielle", "Allergie"],
        "detail": "Combiné à la Vitamine C (E300), forme du benzène cancérigène. Lié au TDAH dans l'étude de McCann (2007)."
    },
    "E250": {
        "name": "Nitrite de Sodium",
        "score": 3,
        "type": "Conservateur",
        "diseases": ["Cancer colorectal", "Cancer de l'estomac", "Méthémoglobinémie"],
        "detail": "Classé 'cancérigène probable' (groupe 2A) par l'IARC. Utilisé dans charcuteries et viandes transformées."
    },
    "E320": {
        "name": "BHA (Butylhydroxyanisole)",
        "score": 3,
        "type": "Antioxydant",
        "diseases": ["Cancer potentiel", "Perturbation endocrinienne"],
        "detail": "Classé 'cancérigène possible' (groupe 2B) par l'IARC. Interdit au Japon. Perturbateur endocrinien suspecté."
    },
    "E321": {
        "name": "BHT (Butylhydroxytoluène)",
        "score": 3,
        "type": "Antioxydant",
        "diseases": ["Cancer potentiel", "Perturbation endocrinienne"],
        "detail": "Perturbateur endocrinien. Interdit dans certains pays. Utilisé comme conservateur dans céréales et graisses."
    },
    "E407": {
        "name": "Carraghénane",
        "score": 3,
        "type": "Épaississant",
        "diseases": ["Inflammation intestinale", "Maladie de Crohn", "Perméabilité intestinale"],
        "detail": "Extrait d'algues. Provoque une inflammation du tractus gastro-intestinal dans de nombreuses études in vitro et animales."
    },
    "E621": {
        "name": "Glutamate Monosodique (MSG)",
        "score": 3,
        "type": "Exhausteur de goût",
        "diseases": ["Obésité", "Troubles métaboliques", "Syndrome du restaurant chinois"],
        "detail": "Stimule l'appétit et favorise la surconsommation. Associé à l'obésité dans des études épidémiologiques asiatiques."
    },
    "E951": {
        "name": "Aspartame",
        "score": 3,
        "type": "Édulcorant",
        "diseases": ["Troubles neurologiques", "Dépression", "Migraines", "Cancer possible"],
        "detail": "Classé 'cancérigène possible' (groupe 2B) par l'IARC en 2023. Métabolisé en phénylalanine, aspartate et méthanol."
    },

    # ── SCORE 2 — Preuve modérée ─────────────────────────────────────
    "E150": {
        "name": "Caramel (IV ammoniacal)",
        "score": 2,
        "type": "Colorant",
        "diseases": ["Cancer potentiel (4-MEI)", "Immunotoxicité"],
        "detail": "Le 4-méthylimidazole (4-MEI) formé pendant la fabrication est cancérigène en Californie (Prop 65)."
    },
    "E338": {
        "name": "Acide Phosphorique",
        "score": 2,
        "type": "Acidifiant",
        "diseases": ["Ostéoporose", "Érosion dentaire", "Insuffisance rénale"],
        "detail": "Réduit la densité osseuse en perturbant l'absorption du calcium. Présent massivement dans les sodas."
    },
    "E433": {
        "name": "Polysorbate 80",
        "score": 2,
        "type": "Émulsifiant",
        "diseases": ["Inflammation intestinale", "Obésité", "Syndrome métabolique"],
        "detail": "Altère le microbiome intestinal et le mucus protecteur. Études sur souris montrent une colite et obésité."
    },
    "E450": {
        "name": "Diphosphate",
        "score": 2,
        "type": "Stabilisant",
        "diseases": ["Insuffisance rénale", "Calcification vasculaire"],
        "detail": "Excès de phosphates lié à une mortalité accrue chez les insuffisants rénaux. Perturbation du métabolisme minéral."
    },
    "E471": {
        "name": "Mono et Diglycérides d'acides gras",
        "score": 2,
        "type": "Émulsifiant",
        "diseases": ["Maladies cardiovasculaires", "Obésité"],
        "detail": "Peuvent contenir des acides gras trans. Souvent issus d'huile de palme ou d'huile hydrogénée."
    },
    "E476": {
        "name": "Polyglycérol Polyricinoleate (PGPR)",
        "score": 2,
        "type": "Émulsifiant",
        "diseases": ["Inflammation intestinale", "Troubles digestifs"],
        "detail": "Utilisé massivement dans le chocolat industriel pour remplacer le beurre de cacao. Perturbation du microbiome."
    },
    "E621_MSG": {
        "name": "Sirop Glucose-Fructose",
        "score": 2,
        "type": "Sucre raffiné",
        "diseases": ["Obésité", "Diabète type 2", "Stéatose hépatique"],
        "detail": "Le fructose libre est métabolisé différemment du glucose, favorisant la lipogenèse hépatique et la résistance à l'insuline."
    },
    "HUILE_PALME": {
        "name": "Huile de Palme",
        "score": 2,
        "type": "Graisse",
        "diseases": ["Maladies cardiovasculaires", "Obésité", "Déforestation"],
        "detail": "Riche en acides gras saturés (palmitique). Lie LDL. Présente dans 17.8% des produits analysés."
    },
    "E960": {
        "name": "Stévioside (Stévia)",
        "score": 2,
        "type": "Édulcorant",
        "diseases": ["Perturbation microbiome", "Effets sur fertilité (études animales)"],
        "detail": "Considéré sûr par l'EFSA mais des études récentes suggèrent des effets sur le microbiome intestinal."
    },

    # ── SCORE 1 — Preuve faible ──────────────────────────────────────
    "E330": {
        "name": "Acide Citrique",
        "score": 1,
        "type": "Acidifiant",
        "diseases": ["Érosion dentaire", "Troubles digestifs légers"],
        "detail": "Généralement sûr mais peut éroder l'émail dentaire à forte consommation. Présent dans 29% des produits."
    },
    "E415": {
        "name": "Gomme Xanthane",
        "score": 1,
        "type": "Épaississant",
        "diseases": ["Troubles digestifs", "Ballonnements"],
        "detail": "Généralement reconnu comme sûr (GRAS). Peut causer des inconforts digestifs en grande quantité."
    },
    "E420": {
        "name": "Sorbitol",
        "score": 1,
        "type": "Édulcorant",
        "diseases": ["Troubles digestifs", "Diarrhée osmotique"],
        "detail": "Polyol non absorbé par l'intestin. Effet laxatif à partir de 10-50g/jour."
    },
    "E500": {
        "name": "Bicarbonate de Sodium",
        "score": 0,
        "type": "Levant",
        "diseases": [],
        "detail": "Aucune preuve de danger aux doses alimentaires. L'un des additifs les plus sûrs."
    },
    "E322": {
        "name": "Lécithine (Soja/Tournesol)",
        "score": 0,
        "type": "Émulsifiant",
        "diseases": [],
        "detail": "Additif naturel considéré sûr. Additif le plus répandu (39% des produits). Issue de soja souvent OGM."
    },
    "E440": {
        "name": "Pectine",
        "score": 0,
        "type": "Épaississant",
        "diseases": [],
        "detail": "Fibre naturelle issue des fruits. Bénéfique pour la santé digestive. Aucun danger connu."
    },

    # ── INGRÉDIENTS CACHÉS ───────────────────────────────────────────
    "HUILE_HYDRO": {
        "name": "Huile Végétale Hydrogénée",
        "score": 3,
        "type": "Graisses trans",
        "diseases": ["Maladies cardiovasculaires", "AVC", "Diabète type 2", "Inflammation"],
        "detail": "Source principale de graisses trans artificielles. L'OMS vise leur élimination mondiale. Augmente le LDL, baisse le HDL."
    },
    "SIROP_GLUC": {
        "name": "Sirop de Glucose-Fructose (HFCS)",
        "score": 3,
        "type": "Sucre industriel",
        "diseases": ["Obésité", "Diabète type 2", "Stéatose hépatique", "Hypertension"],
        "detail": "Le fructose libre bypass la régulation normale de l'appétit. Fortement lié à l'épidémie d'obésité aux USA."
    },
    "SUCRE_RAFFINE": {
        "name": "Sucre Raffiné / Saccharose",
        "score": 2,
        "type": "Sucre",
        "diseases": ["Obésité", "Diabète type 2", "Caries", "Inflammation"],
        "detail": "Index glycémique élevé. Présent dans 70% des produits analysés. L'OMS recommande < 25g/jour."
    },
    "DEXTROSE": {
        "name": "Dextrose / Maltodextrine",
        "score": 2,
        "type": "Sucre rapide",
        "diseases": ["Résistance à l'insuline", "Obésité", "Pic glycémique"],
        "detail": "Index glycémique très élevé (IG=130 pour la maltodextrine vs 100 pour le glucose). Favorise la résistance à l'insuline."
    },
    "E955": {
        "name": "Sucralose",
        "score": 2,
        "type": "Édulcorant",
        "diseases": ["Perturbation microbiome", "Résistance à l'insuline", "Leucémie (études animales)"],
        "detail": "Modifie le microbiome intestinal. Une étude 2023 le relie à une leucémie chez la souris. Reclassifié 'préoccupation possible' par l'IARC."
    },
}

# ─── PRODUITS EXEMPLES ───────────────────────────────────────────────────────
EXAMPLE_PRODUCTS = {
    "🍪 Prince Chocolat": ["E322", "E471", "E476", "SUCRE_RAFFINE", "E500", "E330"],
    "🥤 Coca-Cola": ["E150", "E338", "E211", "SUCRE_RAFFINE"],
    "🍬 Haribo Goldbears": ["E102", "E110", "E122", "E129", "E124", "SUCRE_RAFFINE", "E415"],
    "🥣 Frosties (Kellogg's)": ["E330", "SUCRE_RAFFINE", "DEXTROSE", "E322", "E500"],
    "🧀 Crackers Gruyère": ["E322", "E471", "E450", "HUILE_PALME", "E500"],
    "🍫 Nutella": ["HUILE_PALME", "SUCRE_RAFFINE", "E322", "E476"],
    "🍖 Jambon industriel": ["E250", "E211", "E450", "E322"],
    "🥤 Red Bull": ["E338", "SUCRE_RAFFINE", "E300", "E211"],
}

# ─── DISEASE COLORS ──────────────────────────────────────────────────────────
DISEASE_COLORS = {
    "TDAH": ("#FF2D2D", "#2D0000"),
    "Cancer potentiel": ("#FF2D2D", "#2D0000"),
    "Cancer colorectal": ("#FF2D2D", "#2D0000"),
    "Cancer de l'estomac": ("#FF2D2D", "#2D0000"),
    "Obésité": ("#FF6B1A", "#2D1200"),
    "Diabète type 2": ("#FF6B1A", "#2D1200"),
    "Maladies cardiovasculaires": ("#FFD600", "#2D2200"),
    "Hyperactivité": ("#FF2D2D", "#2D0000"),
    "Inflammation intestinale": ("#FF6B1A", "#2D1200"),
    "Allergie": ("#A855F7", "#1A0D2D"),
    "Asthme": ("#A855F7", "#1A0D2D"),
    "Perturbation endocrinienne": ("#EC4899", "#2D0D1A"),
    "Ostéoporose": ("#FFD600", "#2D2200"),
    "Troubles neurologiques": ("#FF2D2D", "#2D0000"),
    "AVC": ("#FF2D2D", "#2D0000"),
    "default": ("#718096", "#1A1F28"),
}

def get_disease_color(disease):
    for key in DISEASE_COLORS:
        if key.lower() in disease.lower():
            return DISEASE_COLORS[key]
    return DISEASE_COLORS["default"]

def score_color(score):
    return {0: "#00FF88", 1: "#FFD600", 2: "#FF6B1A", 3: "#FF2D2D"}.get(score, "#718096")

def score_label(score):
    return {0: "SÛR", 1: "FAIBLE", 2: "MODÉRÉ", 3: "ÉTABLI"}.get(score, "?")

def parse_input(text):
    """Parse user input: codes E ou noms"""
    found = []
    text_up = text.upper()
    # Cherche les codes E dans le texte
    for code, data in ADDITIVES_DB.items():
        if code in text_up or data["name"].upper() in text_up:
            found.append(code)
    return list(set(found))

def compute_cocktail_score(additives_list):
    """Score cocktail : somme pondérée + bonus pour combinaisons dangereuses"""
    if not additives_list:
        return 0
    scores = [ADDITIVES_DB[a]["score"] for a in additives_list if a in ADDITIVES_DB]
    if not scores:
        return 0
    base = sum(scores)
    # Bonus cocktail : si 2+ score-3 ensemble
    score3 = sum(1 for s in scores if s == 3)
    cocktail_bonus = score3 * (score3 - 1) * 0.5  # pénalité quadratique
    total = base + cocktail_bonus
    max_possible = len(scores) * 3 + (len(scores) * (len(scores)-1) * 0.5 * 0.5)
    normalized = min(100, int((total / max(1, len(scores) * 3)) * 100))
    return normalized

def get_verdict(score):
    if score == 0:
        return ("00FF88", "✅ AUCUN RISQUE DÉTECTÉ", "Ce produit ne contient aucune substance préoccupante connue.")
    elif score < 20:
        return ("00FF88", "🟢 RISQUE NÉGLIGEABLE", "Quelques additifs courants, aucune preuve sérieuse de danger.")
    elif score < 40:
        return ("FFD600", "🟡 RISQUE FAIBLE", "Consommation occasionnelle acceptable. Éviter chez les enfants.")
    elif score < 60:
        return ("FF6B1A", "🟠 RISQUE MODÉRÉ", "Présence de substances à preuves modérées. Limiter la consommation.")
    elif score < 80:
        return ("FF2D2D", "🔴 RISQUE ÉLEVÉ", "Plusieurs substances problématiques. Déconseillé aux enfants et personnes sensibles.")
    else:
        return ("FF2D2D", "☠️ RISQUE TRÈS ÉLEVÉ", "Cocktail de substances dangereuses. Consommation à éviter.")


# ═══════════════════════════════════════════════════════════════════════════
#  APP LAYOUT
# ═══════════════════════════════════════════════════════════════════════════

# ── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom: 2rem;">
  <p class="hero-sub">☠️ Data Science Project · Open Food Facts · EFSA · IARC</p>
  <h1 class="hero-title">COCKTAIL<br>SIMULATOR</h1>
  <p style="color: #718096; font-size: 0.9rem; margin-top: 0.75rem; max-width: 600px;">
    Entre les additifs ou le nom d'un produit alimentaire.<br>
    L'algorithme calcule ton exposition au <em style="color: #FF6B1A;">cocktail effect</em> — 
    la combinaison de substances que personne n'a encore étudiée scientifiquement.
  </p>
</div>
""", unsafe_allow_html=True)

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <p style="font-family: 'Space Mono', monospace; font-size: 0.65rem; 
                  letter-spacing: 0.2em; color: #718096; text-transform: uppercase; margin-bottom: 0.5rem;">
            MODE D'EMPLOI
        </p>
        <p style="font-size: 0.8rem; color: #A0ADB8; line-height: 1.6;">
            Entre des <b style="color:#FF6B1A;">codes E</b> (ex: E102, E211) 
            ou des <b style="color:#FF6B1A;">noms d'ingrédients</b> 
            séparés par des virgules.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Exemples produits
    st.markdown("""<p style="font-family: 'Space Mono', monospace; font-size: 0.65rem; 
                letter-spacing: 0.15em; color: #718096; text-transform: uppercase; margin-bottom: 0.5rem;">
                PRODUITS EXEMPLES</p>""", unsafe_allow_html=True)

    selected_example = st.selectbox(
        "", ["— Choisir un produit —"] + list(EXAMPLE_PRODUCTS.keys()),
        label_visibility="collapsed"
    )

    st.markdown('<div class="toxic-divider"></div>', unsafe_allow_html=True)

    # Input manuel
    st.markdown("""<p style="font-family: 'Space Mono', monospace; font-size: 0.65rem; 
                letter-spacing: 0.15em; color: #718096; text-transform: uppercase; margin-bottom: 0.5rem;">
                ENTRÉE MANUELLE</p>""", unsafe_allow_html=True)

    manual_input = st.text_area(
        "",
        placeholder="E102, E211, E250, huile hydrogénée, aspartame...",
        height=100,
        label_visibility="collapsed"
    )

    analyze_btn = st.button("⚡ ANALYSER", use_container_width=True)

    st.markdown('<div class="toxic-divider"></div>', unsafe_allow_html=True)

    # Légende scores
    st.markdown("""<p style="font-family: 'Space Mono', monospace; font-size: 0.65rem; 
                letter-spacing: 0.15em; color: #718096; text-transform: uppercase; margin-bottom: 0.75rem;">
                ÉCHELLE DE DANGER</p>""", unsafe_allow_html=True)

    for score, label, desc in [
        (3, "ÉTABLI", "Prouvé par EFSA/IARC"),
        (2, "MODÉRÉ", "Preuves convergentes"),
        (1, "FAIBLE", "Études préliminaires"),
        (0, "SÛR", "Aucune preuve de danger"),
    ]:
        col = score_color(score)
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.4rem;">
            <div style="width: 10px; height: 10px; border-radius: 50%; background: {col}; flex-shrink:0;"></div>
            <div>
                <span style="font-family: 'Space Mono', monospace; font-size: 0.65rem; color: {col}; font-weight: 700;">{label}</span>
                <span style="font-size: 0.7rem; color: #718096; margin-left: 0.4rem;">{desc}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-top: 2rem; padding: 0.75rem; background: rgba(255,45,45,0.05); 
                border-radius: 8px; border: 1px solid rgba(255,45,45,0.15);">
        <p style="font-size: 0.65rem; color: #4A5568; line-height: 1.5; margin: 0;">
            ⚠️ Projet exploratoire.<br>
            Corrélations, pas causalité établie.<br>
            Sources : EFSA · IARC · PubMed
        </p>
    </div>
    """, unsafe_allow_html=True)


# ── DETERMINE ACTIVE ADDITIVES ────────────────────────────────────────────────
active_additives = []

if selected_example != "— Choisir un produit —":
    active_additives = EXAMPLE_PRODUCTS[selected_example]
    product_name = selected_example
elif analyze_btn and manual_input.strip():
    active_additives = parse_input(manual_input)
    product_name = "ANALYSE MANUELLE"
else:
    product_name = None


# ── MAIN CONTENT ──────────────────────────────────────────────────────────────
if not active_additives and not product_name:
    # ── ÉTAT INITIAL : Présentation ──────────────────────────────────────────
    st.markdown("""
    <div style="text-align: center; padding: 4rem 2rem; max-width: 700px; margin: 0 auto;">
        <div style="font-size: 4rem; margin-bottom: 1rem; opacity: 0.15;">☠️</div>
        <p style="font-size: 1.1rem; color: #4A5568; line-height: 1.8;">
            Sélectionne un produit dans la sidebar ou entre des codes additifs<br>
            pour simuler ton exposition au <span style="color: #FF6B1A;">cocktail effect</span>.
        </p>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-top: 3rem;">
    """, unsafe_allow_html=True)

    stats = [
        ("2 948", "produits analysés"),
        ("191", "additifs uniques"),
        ("89.8%", "contiennent ≥1 substance à risque"),
    ]
    cols = st.columns(3)
    for i, (val, lab) in enumerate(stats):
        with cols[i]:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-val" style="color: #FF6B1A;">{val}</div>
                <div class="metric-lab">{lab}</div>
            </div>
            """, unsafe_allow_html=True)

elif product_name and not active_additives:
    st.warning("⚠️ Aucun additif reconnu dans l'entrée. Essaie des codes comme E102, E211, ou des mots-clés comme 'aspartame', 'huile hydrogénée'.")

else:
    # ── RÉSULTATS ─────────────────────────────────────────────────────────────
    known = [a for a in active_additives if a in ADDITIVES_DB]
    cocktail_score = compute_cocktail_score(known)
    verdict_color, verdict_text, verdict_desc = get_verdict(cocktail_score)

    # Trier par score décroissant
    known_sorted = sorted(known, key=lambda x: ADDITIVES_DB[x]["score"], reverse=True)

    # Stats
    all_diseases = []
    for a in known:
        all_diseases.extend(ADDITIVES_DB[a]["diseases"])
    unique_diseases = list(set(all_diseases))
    score3_count = sum(1 for a in known if ADDITIVES_DB[a]["score"] == 3)
    score2_count = sum(1 for a in known if ADDITIVES_DB[a]["score"] == 2)

    # ── ROW 1 : Gauge + Métriques ─────────────────────────────────────────────
    col_gauge, col_metrics = st.columns([1, 2])

    with col_gauge:
        st.markdown(f"""
        <div class="gauge-container" style="border-color: #{verdict_color}33;">
            <div style="font-family: 'Space Mono', monospace; font-size: 0.65rem; 
                        letter-spacing: 0.2em; color: #718096; text-transform: uppercase; margin-bottom: 1rem;">
                SCORE COCKTAIL
            </div>
            <div class="score-number" style="color: #{verdict_color};">{cocktail_score}</div>
            <div class="score-label">/100 · INDEX DE RISQUE COMBINÉ</div>
            <div style="margin-top: 1.25rem; padding: 0.75rem; background: rgba({int(verdict_color[:2],16)},{int(verdict_color[2:4],16)},{int(verdict_color[4:],16)},0.1); 
                        border-radius: 8px; border: 1px solid #{verdict_color}33;">
                <div class="verdict-text" style="color: #{verdict_color};">{verdict_text}</div>
                <div style="font-size: 0.75rem; color: #A0ADB8; margin-top: 0.35rem;">{verdict_desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_metrics:
        r1c1, r1c2, r1c3, r1c4 = st.columns(4)
        with r1c1:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-val" style="color: #E2E8F0;">{len(known)}</div>
                <div class="metric-lab">Additifs<br>détectés</div>
            </div>""", unsafe_allow_html=True)
        with r1c2:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-val" style="color: #FF2D2D;">{score3_count}</div>
                <div class="metric-lab">Danger<br>établi</div>
            </div>""", unsafe_allow_html=True)
        with r1c3:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-val" style="color: #FF6B1A;">{score2_count}</div>
                <div class="metric-lab">Preuve<br>modérée</div>
            </div>""", unsafe_allow_html=True)
        with r1c4:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-val" style="color: #A855F7;">{len(unique_diseases)}</div>
                <div class="metric-lab">Maladies<br>associées</div>
            </div>""", unsafe_allow_html=True)

        # Barre cocktail bonus
        if score3_count >= 2:
            st.markdown(f"""
            <div class="alert-box" style="margin-top: 0.75rem;">
                <b>⚠️ COCKTAIL EFFECT DÉTECTÉ</b><br>
                <span style="color: #A0ADB8; font-size: 0.8rem;">
                    {score3_count} substances à danger établi sont présentes simultanément. 
                    Leurs interactions combinées n'ont pas été étudiées scientifiquement. 
                    Le score inclut un malus de pénalité quadratique.
                </span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="toxic-divider"></div>', unsafe_allow_html=True)

    # ── ROW 2 : Radar Chart + Additives list ────────────────────────────────
    col_chart, col_list = st.columns([1, 1.4])

    with col_chart:
        # Radar chart des catégories de maladies
        disease_categories = {
            "🧠 Neuro / Comportement": ["TDAH", "Hyperactivité", "Troubles neurologiques", "Dépression", "Migraines"],
            "🫀 Cardio-vasculaire": ["Maladies cardiovasculaires", "AVC", "Hypertension", "Ostéoporose"],
            "🧬 Cancer": ["Cancer potentiel", "Cancer colorectal", "Cancer de l'estomac", "Leucémie potentielle", "Génotoxicité"],
            "⚗️ Métabolique": ["Obésité", "Diabète type 2", "Résistance à l'insuline", "Stéatose hépatique"],
            "🦠 Microbiome / Intestin": ["Inflammation intestinale", "Maladie de Crohn", "Perméabilité intestinale", "Perturbation microbiome"],
            "🧪 Endocrinien": ["Perturbation endocrinienne", "Méthémoglobinémie"],
        }

        radar_scores = {}
        for cat, disease_list in disease_categories.items():
            count = 0
            for a in known:
                for d in ADDITIVES_DB[a]["diseases"]:
                    if any(dl.lower() in d.lower() for dl in disease_list):
                        count += ADDITIVES_DB[a]["score"]
            radar_scores[cat] = min(10, count)

        cats = list(radar_scores.keys())
        vals = list(radar_scores.values())
        vals_closed = vals + [vals[0]]
        cats_closed = cats + [cats[0]]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=vals_closed,
            theta=cats_closed,
            fill='toself',
            fillcolor='rgba(255, 45, 45, 0.15)',
            line=dict(color='#FF2D2D', width=2),
            name='Exposition'
        ))
        fig_radar.update_layout(
            polar=dict(
                bgcolor='#0F1318',
                angularaxis=dict(
                    tickfont=dict(color='#718096', size=10, family='Space Mono'),
                    linecolor='#1E252E',
                    gridcolor='#1E252E',
                ),
                radialaxis=dict(
                    visible=True, range=[0, 10],
                    tickfont=dict(color='#4A5568', size=9),
                    linecolor='#1E252E',
                    gridcolor='#1E252E',
                )
            ),
            paper_bgcolor='#0F1318',
            plot_bgcolor='#0F1318',
            font=dict(color='#E2E8F0'),
            margin=dict(l=30, r=30, t=50, b=30),
            title=dict(
                text="CARTOGRAPHIE DES RISQUES",
                font=dict(family='Space Mono', size=11, color='#718096'),
                x=0.5
            ),
            height=340,
            showlegend=False
        )
        st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})

        # Maladies uniques
        if unique_diseases:
            st.markdown("""<p style="font-family: 'Space Mono', monospace; font-size: 0.65rem; 
                        letter-spacing: 0.15em; color: #718096; text-transform: uppercase; margin-bottom: 0.5rem;">
                        MALADIES ASSOCIÉES</p>""", unsafe_allow_html=True)
            tags_html = ""
            for d in sorted(unique_diseases):
                fg, bg = get_disease_color(d)
                tags_html += f'<span class="disease-tag" style="color:{fg}; background:{bg}; border: 1px solid {fg}33;">{d}</span>'
            st.markdown(f'<div style="line-height: 2;">{tags_html}</div>', unsafe_allow_html=True)

    with col_list:
        st.markdown("""<p style="font-family: 'Space Mono', monospace; font-size: 0.65rem; 
                    letter-spacing: 0.15em; color: #718096; text-transform: uppercase; margin-bottom: 0.75rem;">
                    SUBSTANCES DÉTECTÉES</p>""", unsafe_allow_html=True)

        for code in known_sorted:
            data = ADDITIVES_DB[code]
            score = data["score"]
            color = score_color(score)
            label = score_label(score)

            # Disease tags
            disease_tags = ""
            for d in data["diseases"][:3]:
                fg, bg = get_disease_color(d)
                disease_tags += f'<span class="disease-tag" style="color:{fg}; background:{bg}; border:1px solid {fg}33;">{d}</span>'
            if len(data["diseases"]) > 3:
                disease_tags += f'<span class="disease-tag" style="color:#718096; background:#1A1F28; border:1px solid #2D3748;">+{len(data["diseases"])-3}</span>'

            st.markdown(f"""
            <div class="additive-card">
                <div class="risk-bar" style="background: {color};"></div>
                <div>
                    <div class="add-code" style="color: {color};">{code}</div>
                    <div style="font-family: 'Space Mono', monospace; font-size: 0.55rem; color: #4A5568; text-transform: uppercase; margin-top: 1px;">{data['type']}</div>
                </div>
                <div style="flex: 1;">
                    <div class="add-name">{data['name']}</div>
                    <div style="margin-top: 0.25rem;">{disease_tags}</div>
                </div>
                <div>
                    <div class="add-score" style="color: {color};">{score}</div>
                    <div style="font-family: 'Space Mono', monospace; font-size: 0.55rem; color: {color}; text-align:right;">{label}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="toxic-divider"></div>', unsafe_allow_html=True)

    # ── ROW 3 : Bar chart horizontal ─────────────────────────────────────────
    st.markdown("""<p style="font-family: 'Space Mono', monospace; font-size: 0.65rem; 
                letter-spacing: 0.15em; color: #718096; text-transform: uppercase; margin-bottom: 0.5rem;">
                PROFIL DE RISQUE PAR SUBSTANCE</p>""", unsafe_allow_html=True)

    bar_names = [f"{code} · {ADDITIVES_DB[code]['name']}" for code in known_sorted]
    bar_scores = [ADDITIVES_DB[code]["score"] for code in known_sorted]
    bar_colors = [score_color(s) for s in bar_scores]

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=bar_scores,
        y=bar_names,
        orientation='h',
        marker=dict(
            color=bar_colors,
            line=dict(width=0),
        ),
        text=[f"  {score_label(s)}" for s in bar_scores],
        textposition='outside',
        textfont=dict(family='Space Mono', size=9, color='#718096'),
        hovertemplate='<b>%{y}</b><br>Score: %{x}/3<extra></extra>',
    ))

    fig_bar.update_layout(
        paper_bgcolor='#0F1318',
        plot_bgcolor='#0F1318',
        font=dict(color='#E2E8F0', family='DM Sans'),
        height=max(200, len(known_sorted) * 45 + 60),
        margin=dict(l=10, r=80, t=20, b=20),
        xaxis=dict(
            range=[0, 4], showgrid=True,
            gridcolor='#1E252E', zeroline=False,
            tickfont=dict(color='#4A5568', family='Space Mono', size=9),
            tickvals=[0, 1, 2, 3],
            ticktext=["0 · SÛR", "1 · FAIBLE", "2 · MODÉRÉ", "3 · ÉTABLI"],
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(color='#A0ADB8', size=11),
        ),
        showlegend=False,
    )

    # Zones colorées
    for y0, y1, color, alpha in [(0, 0.5, '#00FF88', 0.04), (0.5, 1.5, '#FFD600', 0.04),
                                   (1.5, 2.5, '#FF6B1A', 0.05), (2.5, 3.5, '#FF2D2D', 0.07)]:
        fig_bar.add_vrect(x0=y0, x1=y1, fillcolor=color, opacity=alpha, line_width=0)

    st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

    # ── Détails scientifiques ─────────────────────────────────────────────────
    with st.expander("🔬 DÉTAILS SCIENTIFIQUES — Sources & explications", expanded=False):
        for code in known_sorted:
            data = ADDITIVES_DB[code]
            color = score_color(data["score"])
            st.markdown(f"""
            <div style="border-left: 3px solid {color}; padding: 0.75rem 1rem; margin-bottom: 0.75rem; 
                        background: #0F1318; border-radius: 0 8px 8px 0;">
                <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.35rem;">
                    <span style="font-family: 'Space Mono', monospace; font-size: 0.75rem; color: {color}; font-weight: 700;">{code}</span>
                    <span style="font-weight: 600;">{data['name']}</span>
                    <span style="font-family: 'Space Mono', monospace; font-size: 0.65rem; 
                                color: {color}; background: {color}22; padding: 2px 8px; border-radius: 100px;">
                        SCORE {data['score']} · {score_label(data['score'])}
                    </span>
                </div>
                <p style="font-size: 0.8rem; color: #A0ADB8; margin: 0; line-height: 1.6;">{data['detail']}</p>
            </div>
            """, unsafe_allow_html=True)

# ── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="toxic-divider"></div>
<div style="text-align: center; padding: 1rem;">
    <p style="font-family: 'Space Mono', monospace; font-size: 0.6rem; color: #2D3748; letter-spacing: 0.15em;">
        SOURCES : OPEN FOOD FACTS (ODbL) · EFSA · IARC · PUBMED · INFORMATION IS BEAUTIFUL
        &nbsp;|&nbsp; PROJET EXPLORATOIRE — CORRÉLATIONS, PAS CAUSALITÉ ÉTABLIE
    </p>
</div>
""", unsafe_allow_html=True)
