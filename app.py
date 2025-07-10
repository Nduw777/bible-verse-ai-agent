import streamlit as st
import requests
import json
from datetime import datetime
import random

# Page configuration
st.set_page_config(
    page_title="Bible Verse AI Agent",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E4057;
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    .verse-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .interpretation-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .language-badge {
        background: #667eea;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 0.2rem;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# Language translations
LANGUAGES = {
    'en': 'English',
    'fr': 'Français',
    'sw': 'Kiswahili',
    'rw': 'Kinyarwanda'
}

TRANSLATIONS = {
    'en': {
        'title': 'Bible Verse AI Agent',
        'subtitle': 'Discover, Learn, and Reflect on Scripture',
        'search_placeholder': 'Search for verses (e.g., "John 3:16" or "love")',
        'get_random': 'Get Random Verse',
        'search_button': 'Search Verses',
        'verse_of_day': 'Verse of the Day',
        'interpretations': 'Interpretations & Perspectives',
        'historical': 'Historical Context',
        'theological': 'Theological Perspective',
        'practical': 'Practical Application',
        'cross_references': 'Cross References',
        'select_language': 'Select Language',
        'no_results': 'No verses found. Try different keywords.',
        'error': 'An error occurred. Please try again.',
        'loading': 'Loading...'
    },
    'fr': {
        'title': 'Agent IA des Versets Bibliques',
        'subtitle': 'Découvrez, Apprenez et Réfléchissez sur les Écritures',
        'search_placeholder': 'Rechercher des versets (ex: "Jean 3:16" ou "amour")',
        'get_random': 'Verset Aléatoire',
        'search_button': 'Rechercher des Versets',
        'verse_of_day': 'Verset du Jour',
        'interpretations': 'Interprétations et Perspectives',
        'historical': 'Contexte Historique',
        'theological': 'Perspective Théologique',
        'practical': 'Application Pratique',
        'cross_references': 'Références Croisées',
        'select_language': 'Sélectionner la Langue',
        'no_results': 'Aucun verset trouvé. Essayez différents mots-clés.',
        'error': 'Une erreur est survenue. Veuillez réessayer.',
        'loading': 'Chargement...'
    },
    'sw': {
        'title': 'Wakala wa AI wa Mstari wa Biblia',
        'subtitle': 'Gundua, Jifunze, na Tafakari kuhusu Maandiko',
        'search_placeholder': 'Tafuta mistari (mf: "Yohana 3:16" au "upendo")',
        'get_random': 'Pata Mstari wa Nasibu',
        'search_button': 'Tafuta Mistari',
        'verse_of_day': 'Mstari wa Siku',
        'interpretations': 'Maelezo na Mitazamo',
        'historical': 'Mazingira ya Kihistoria',
        'theological': 'Mtazamo wa Kiteolojia',
        'practical': 'Matumizi ya Vitendo',
        'cross_references': 'Marejeleo ya Msalaba',
        'select_language': 'Chagua Lugha',
        'no_results': 'Hakuna mistari iliyopatikana. Jaribu maneno mengine.',
        'error': 'Hitilafu imetokea. Tafadhali jaribu tena.',
        'loading': 'Inapakia...'
    },
    'rw': {
        'title': 'Umukozi wa AI w\'Amagambo y\'Inyandiko',
        'subtitle': 'Menya, Wige, kandi Utekereze ku Nyandiko',
        'search_placeholder': 'Shakisha amagambo (urugero: "Yohana 3:16" cyangwa "urukundo")',
        'get_random': 'Boneka Ijambo ry\'Amahirwe',
        'search_button': 'Shakisha Amagambo',
        'verse_of_day': 'Ijambo ry\'Umunsi',
        'interpretations': 'Ibisobanuro n\'Ibitekerezo',
        'historical': 'Ibidahwitse',
        'theological': 'Ikitekerezo cy\'Idini',
        'practical': 'Ibikorwa by\'Ukuri',
        'cross_references': 'Indango z\'Ingenzi',
        'select_language': 'Hitamo Ururimi',
        'no_results': 'Nta magambo yabonetse. Gerageza amagambo menshi.',
        'error': 'Habaye ikosa. Nyamuneka ongera ugerageze.',
        'loading': 'Birarimo kwikora...'
    }
}

# Sample Bible verses database (in practice, you'd use a real API)
SAMPLE_VERSES = [
    {
        'reference': 'John 3:16',
        'text': {
            'en': 'For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life.',
            'fr': 'Car Dieu a tant aimé le monde qu\'il a donné son Fils unique, afin que quiconque croit en lui ne périsse point, mais qu\'il ait la vie éternelle.',
            'sw': 'Kwa maana Mungu aliupenda ulimwengu hivi, hata akamtoa Mwanawe wa pekee, ili kila amwaminiye asipotee, bali awe na uzima wa milele.',
            'rw': 'Kuko Imana yakundaga isi cyane, maze ihaye Umwana wayo w\'imwe gusa, kugirango uwimwizera adatsimbagara, ahubwo agire ubuzima buhoraho.'
        }
    },
    {
        'reference': 'Psalm 23:1',
        'text': {
            'en': 'The Lord is my shepherd, I lack nothing.',
            'fr': 'L\'Éternel est mon berger: je ne manquerai de rien.',
            'sw': 'Bwana ni mchungaji wangu, sitakosa kitu.',
            'rw': 'Uwiteka ni umushumba wanjye, sinzaba nshonje.'
        }
    },
    {
        'reference': 'Philippians 4:13',
        'text': {
            'en': 'I can do all this through him who gives me strength.',
            'fr': 'Je puis tout par celui qui me fortifie.',
            'sw': 'Naweza vyote katika yeye anipaye nguvu.',
            'rw': 'Nshobora byose mu mwene yampa imbaraga.'
        }
    },
    {
        'reference': 'Romans 8:28',
        'text': {
            'en': 'And we know that in all things God works for the good of those who love him.',
            'fr': 'Nous savons, du reste, que toutes choses concourent au bien de ceux qui aiment Dieu.',
            'sw': 'Na tunajua kwamba mambo yote yamfanyia mema mtu aimpendaye Mungu.',
            'rw': 'Kandi tuzi ko ibintu byose bifatanya kubera ibyiza by\'abo bamukunda Imana.'
        }
    }
]

def get_ai_interpretation(verse_text, reference, language, perspective):
    """Generate AI interpretation based on perspective"""
    # This is a mock function - in practice, you'd call an AI API like OpenAI
    interpretations = {
        'historical': {
            'en': f"The verse {reference} was written in a specific historical context. Understanding the cultural and social circumstances of that time helps us grasp the deeper meaning intended for the original audience.",
            'fr': f"Le verset {reference} a été écrit dans un contexte historique spécifique. Comprendre les circonstances culturelles et sociales de cette époque nous aide à saisir le sens profond destiné au public original.",
            'sw': f"Mstari {reference} uliandikwa katika mazingira maalum ya kihistoria. Kuelewa hali za kitamaduni na kijamii za wakati huo kunatusaidia kuelewa maana ya kina iliyokusudiwa kwa wasomaji wa awali.",
            'rw': f"Ijambo {reference} ryanditswe mu bidahwitse byihariye. Kumenya ibidahwitse by\'umuco n\'ubusabane bw\'icyo gihe bitufasha kumva ibisobanuro by\'imbere byiganjwe ku bafashije ba mbere."
        },
        'theological': {
            'en': f"From a theological perspective, {reference} reveals important truths about God's nature, His relationship with humanity, and His plan for salvation.",
            'fr': f"D'un point de vue théologique, {reference} révèle des vérités importantes sur la nature de Dieu, Sa relation avec l'humanité et Son plan de salut.",
            'sw': f"Kwa mtazamo wa kiteolojia, {reference} inafunua ukweli muhimu kuhusu asili ya Mungu, uhusiano Wake na wanadamu, na mpango Wake wa wokovu.",
            'rw': f"Mu buryo bw\'idini, {reference} irerekana ukuri gukomeye ku kamere ka Imana, isano Ye n\'abantu, n\'igitekerezo cye cyo gutabara."
        },
        'practical': {
            'en': f"In practical terms, {reference} offers guidance for daily living, encouraging believers to apply these principles in their relationships, work, and spiritual journey.",
            'fr': f"En termes pratiques, {reference} offre des conseils pour la vie quotidienne, encourageant les croyants à appliquer ces principes dans leurs relations, leur travail et leur parcours spirituel.",
            'sw': f"Kwa maelezo ya vitendo, {reference} inatoa mwongozo wa maisha ya kila siku, ikiwahimiza waumini kutumia kanuni hizi katika mahusiano yao, kazi, na safari yao ya kiroho.",
            'rw': f"Mu buryo bw\'ibikorwa, {reference} ritanga ubuyobozi bw\'ubuzima bwa buri munsi, rishishikariza abizera gukoresha ayo mahame mu mibanire yabo, umurimo, n\'urugendo rwabo rw\'umuzimu."
        }
    }
    
    return interpretations.get(perspective, {}).get(language, "Interpretation not available in this language.")

def search_verses(query, language):
    """Search for Bible verses (mock function)"""
    # In practice, this would call a Bible API
    results = []
    for verse in SAMPLE_VERSES:
        if query.lower() in verse['reference'].lower() or query.lower() in verse['text'][language].lower():
            results.append(verse)
    return results

def get_random_verse():
    """Get a random Bible verse"""
    return random.choice(SAMPLE_VERSES)

def main():
    # Initialize session state
    if 'language' not in st.session_state:
        st.session_state.language = 'en'
    
    # Sidebar for language selection
    with st.sidebar:
        st.markdown("### 🌍 Language / Langue / Lugha / Ururimi")
        selected_lang = st.selectbox(
            "Select Language",
            options=list(LANGUAGES.keys()),
            format_func=lambda x: LANGUAGES[x],
            index=list(LANGUAGES.keys()).index(st.session_state.language)
        )
        st.session_state.language = selected_lang
    
    # Get translations for selected language
    t = TRANSLATIONS[st.session_state.language]
    
    # Main header
    st.markdown(f"<h1 class='main-header'>📖 {t['title']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #666; font-size: 1.2rem;'>{t['subtitle']}</p>", unsafe_allow_html=True)
    
    # Search section
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input(
            "",
            placeholder=t['search_placeholder'],
            key="search_input"
        )
    
    with col2:
        if st.button(t['get_random'], type="secondary"):
            st.session_state.current_verse = get_random_verse()
            st.session_state.show_verse = True
    
    if st.button(t['search_button'], type="primary"):
        if search_query:
            results = search_verses(search_query, st.session_state.language)
            if results:
                st.session_state.current_verse = results[0]  # Show first result
                st.session_state.show_verse = True
            else:
                st.warning(t['no_results'])
    
    # Show verse of the day by default
    if 'current_verse' not in st.session_state:
        st.session_state.current_verse = get_random_verse()
        st.session_state.show_verse = True
    
    # Display verse
    if st.session_state.get('show_verse', False):
        verse = st.session_state.current_verse
        
        # Verse container
        st.markdown(f"""
        <div class='verse-container'>
            <h2 style='margin-bottom: 1rem;'>{verse['reference']}</h2>
            <p style='font-size: 1.3rem; line-height: 1.6; font-style: italic;'>
                "{verse['text'][st.session_state.language]}"
            </p>
            <div style='margin-top: 1rem;'>
                <span class='language-badge'>{LANGUAGES[st.session_state.language]}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Interpretations section
        st.markdown(f"## 🎯 {t['interpretations']}")
        
        # Create tabs for different perspectives
        tab1, tab2, tab3 = st.tabs([t['historical'], t['theological'], t['practical']])
        
        with tab1:
            st.markdown(f"""
            <div class='interpretation-box'>
                <h4>📜 {t['historical']}</h4>
                <p>{get_ai_interpretation(verse['text'][st.session_state.language], verse['reference'], st.session_state.language, 'historical')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with tab2:
            st.markdown(f"""
            <div class='interpretation-box'>
                <h4>⛪ {t['theological']}</h4>
                <p>{get_ai_interpretation(verse['text'][st.session_state.language], verse['reference'], st.session_state.language, 'theological')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with tab3:
            st.markdown(f"""
            <div class='interpretation-box'>
                <h4>🌟 {t['practical']}</h4>
                <p>{get_ai_interpretation(verse['text'][st.session_state.language], verse['reference'], st.session_state.language, 'practical')}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: #888;'>Made with ❤️ for spiritual growth and reflection</p>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()