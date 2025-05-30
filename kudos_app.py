import streamlit as st
import pandas as pd
from datetime import datetime
import json
import plotly.express as px
import plotly.graph_objects as go

# Konfiguracja strony
st.set_page_config(
    page_title="System TARCZA - Prototyp",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Material-UI inspirowany CSS z animacjami
st.markdown("""
<style>
    /* Font i animacje */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Globalne ustawienia */
    .stApp {
        background: #f5f5f7;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        min-height: 100vh;
    }
    
    /* Gradient tło tylko dla strony logowania */
    .login-page {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    }
    
    /* Domyślny kontener - szeroki dla dashboardu */
    .main .block-container {
        background: white;
        border-radius: 0;
        box-shadow: none;
        border: none;
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
        animation: fadeIn 1s ease-out;
    }
    
    /* Specjalny kontener TYLKO dla strony logowania */
    body.login-page .main .block-container {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(20px) !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        padding: 3rem !important;
        max-width: 500px !important;
        margin: 2rem auto !important;
    }
    
    /* Animacje fade-in */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes grow {
        from {
            opacity: 0;
            transform: scale(0.9);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    /* Usunięcie wszystkich ramek z elementów */
    .element-container {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        border-radius: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        backdrop-filter: none !important;
    }
    
    /* Czysty sidebar */
    .css-1d391kg {
        background: #f5f5f7;
        border: none;
        border-radius: 0;
    }
    
    /* Tytuły w stylu Apple */
    h1 {
        font-weight: 700;
        font-size: 2.5rem;
        color: #1d1d1f;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        font-weight: 600;
        color: #1d1d1f;
        font-size: 1.8rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        font-weight: 500;
        color: #424245;
        font-size: 1.4rem;
        margin-bottom: 0.8rem;
    }
    
    /* Przyciski Apple - czyste, bez dodatkowych ramek */
    .stButton > button {
        background: #007AFF;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 16px 32px;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        font-size: 16px;
        transition: all 0.2s ease;
        box-shadow: 0 2px 12px rgba(0, 122, 255, 0.25);
        min-height: 48px;
    }
    
    .stButton > button:hover {
        background: #0056CC;
        transform: translateY(-1px);
        box-shadow: 0 4px 20px rgba(0, 122, 255, 0.35);
    }
    
    .stButton > button:focus {
        outline: 2px solid #007AFF;
        outline-offset: 2px;
        box-shadow: 0 2px 12px rgba(0, 122, 255, 0.25);
    }
    
    /* Specjalny styl dla przycisku Google - Material-UI */
    .stButton > button[kind="primary"] {
        background: #1976d2;
        font-weight: 600;
        font-size: 1.1rem;
        padding: 1.5rem 2rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        min-height: 56px;
        letter-spacing: 0.5px;
        text-transform: none;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: #1565c0;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.25);
    }
    
    /* Style dla kart użytkowników */
    .user-card {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .user-card:hover {
        background: rgba(0, 122, 255, 0.05);
        transform: translateX(8px);
    }
    
    /* Pola tekstowe - minimalistyczne */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background: white;
        border: 1px solid #d2d2d7;
        border-radius: 8px;
        padding: 12px 16px;
        font-family: 'Inter', sans-serif;
        font-size: 15px;
        transition: border-color 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #007AFF;
        outline: none;
        box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.1);
    }
    
    /* Formularze - czyste */
    .stForm {
        background: white;
        border: 1px solid #e5e5e7;
        border-radius: 12px;
        padding: 24px;
        box-shadow: none;
    }
    
    /* Tabs - minimalistyczne */
    .stTabs [data-baseweb="tab-list"] {
        background: #f5f5f7;
        border-radius: 8px;
        padding: 4px;
        border: none;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: 500;
        color: #424245;
        background: transparent;
    }
    
    .stTabs [aria-selected="true"] {
        background: white;
        color: #007AFF;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #f5f5f7;
        border: 1px solid #e5e5e7;
        border-radius: 8px;
        font-weight: 500;
    }
    
    .streamlit-expanderContent {
        background: white;
        border: 1px solid #e5e5e7;
        border-top: none;
        border-radius: 0 0 8px 8px;
    }
    
    /* Metryki - czyste karty */
    [data-testid="metric-container"] {
        background: white;
        border: 1px solid #e5e5e7;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    /* Alerty */
    .stAlert {
        border-radius: 8px;
        border: none;
        font-weight: 500;
    }
    
    .stSuccess {
        background: #d1f2eb;
        color: #0e7b69;
    }
    
    .stError {
        background: #ffeaa7;
        color: #d63031;
    }
    
    .stInfo {
        background: #e3f2fd;
        color: #1976d2;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: #007AFF;
        border-radius: 4px;
    }
    
    /* Ukrycie elementów Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    
    /* Responsywność dla dashboardu */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
            max-width: 100%;
        }
        
        h1 {
            font-size: 2rem;
        }
        
        .stButton > button {
            padding: 12px 20px;
            font-size: 14px;
        }
    }
    
    @media (max-width: 480px) {
        .main .block-container {
            padding: 0.5rem;
        }
        
        h1 {
            font-size: 1.8rem;
        }
    }
    
    /* Responsywność TYLKO dla strony logowania */
    @media (max-width: 768px) {
        body.login-page .main .block-container {
            padding: 2rem 1rem !important;
            margin: 1rem !important;
            max-width: calc(100% - 2rem) !important;
        }
    }
    
    @media (max-width: 480px) {
        body.login-page .main .block-container {
            padding: 1.5rem 1rem !important;
            margin: 0.5rem !important;
            max-width: calc(100% - 1rem) !important;
        }
    }
    
    /* Scrollbar Apple */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f5f5f7;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #c7c7cc;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #a8a8ad;
    }
</style>
""", unsafe_allow_html=True)

# Inicjalizacja danych w session state
def init_session_state():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "current_user" not in st.session_state:
        st.session_state.current_user = None
    if "current_context" not in st.session_state:
        st.session_state.current_context = None
    if "kudos" not in st.session_state:
        st.session_state.kudos = []
    if "employees" not in st.session_state:
        st.session_state.employees = [
            {"id": 1, "name": "Anna Kowalska", "role": "Pracownik", "department": "IT", "email": "anna.kowalska@energetyka.pl"},
            {"id": 2, "name": "Jan Nowak", "role": "Lider zespołu", "department": "HR", "email": "jan.nowak@energetyka.pl"},
            {"id": 3, "name": "Maria Wiśniewska", "role": "Koordynator HR", "department": "HR", "email": "maria.wisniewska@energetyka.pl"},
            {"id": 4, "name": "Piotr Kowalczyk", "role": "Administrator systemu", "department": "IT", "email": "piotr.kowalczyk@energetyka.pl"},
            {"id": 5, "name": "Katarzyna Zielińska", "role": "Zarząd", "department": "Zarząd", "email": "katarzyna.zielinska@energetyka.pl"},
            {"id": 6, "name": "Tomasz Dąbrowski", "role": "Koordynator programu Mam wpływ", "department": "HR", "email": "tomasz.dabrowski@energetyka.pl"}
        ]
    if "initiatives" not in st.session_state:
        st.session_state.initiatives = []

# Wartości organizacyjne firmy
COMPANY_VALUES = [
    "Przedsiębiorczość",
    "Autonomia", 
    "Transparentność",
    "Współpraca",
    "Odpowiedzialność",
    "Rozwój",
    "Zrównoważony rozwój",
    "Innowacyjność"
]

# Symulacja Google OAuth
def simulate_google_oauth():
    """Symuluje proces autoryzacji Google OAuth"""
    
    # Losowe opóźnienie dla realizmu
    import time
    import random
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    status_text.text("🔄 Przekierowanie do Google...")
    time.sleep(1)
    progress_bar.progress(25)
    
    status_text.text("🔐 Autoryzacja z Google Auth...")
    time.sleep(1)
    progress_bar.progress(50)
    
    status_text.text("✅ Pobieranie danych użytkownika...")
    time.sleep(1)
    progress_bar.progress(75)
    
    status_text.text("🛡️ Sprawdzanie uprawnień w systemie TARCZA...")
    time.sleep(1)
    progress_bar.progress(100)
    
    return True

# Funkcja logowania
def login_page():
    # Dodaj klasę CSS do body dla strony logowania
    st.markdown("""
    <script>
        // Dodaj gradient tło i klasy dla strony logowania
        document.querySelector('.stApp').style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
        document.body.classList.add('login-page');
    </script>
    """, unsafe_allow_html=True)
    
    # Material-UI inspirowana strona logowania
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <div style="
            font-size: 4rem; 
            margin-bottom: 1rem;
            animation: grow 1s ease-out;
        ">🛡️</div>
        <h1 style="
            font-size: 3rem; 
            font-weight: 700; 
            margin: 0; 
            color: #1d1d1f;
            animation: fadeIn 1s ease-out 0.2s both;
        ">TARCZA</h1>
        <p style="
            font-size: 1rem; 
            color: #666; 
            margin: 0.5rem 0;
            animation: fadeIn 1s ease-out 0.4s both;
        ">
            Technologia Aktywnego Rozwoju
        </p>
        <p style="
            font-size: 1rem; 
            color: #666; 
            margin: 0 0 2rem 0;
            animation: fadeIn 1s ease-out 0.6s both;
        ">
            Członków Zespołu i Adaptacji
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Divider jak w Material-UI
    st.markdown("""
    <hr style="
        border: none;
        height: 1px;
        background: rgba(0, 0, 0, 0.1);
        margin: 2rem 0;
        animation: fadeIn 1s ease-out 0.8s both;
    ">
    """, unsafe_allow_html=True)
    
    # Informacja o Google z Material-UI stylingiem
    st.markdown("""
    <div style="
        color: #1976d2;
        font-weight: 500;
        margin-bottom: 1.5rem;
        animation: fadeIn 1s ease-out 1s both;
    ">
        💡 System zintegrowany z Google Workspace
    </div>
    """, unsafe_allow_html=True)
    
    # Jeśli nie kliknięto jeszcze przycisku Google
    if not st.session_state.get("google_authorized", False):
        # Dodatkowy CSS tylko dla przycisku Google
        st.markdown("""
        <style>
        /* Style tylko dla przycisku Google na stronie logowania */
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #4285f4 0%, #1a73e8 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 12px 24px !important;
            font-size: 1rem !important;
            font-weight: 500 !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
            min-height: 56px !important;
            box-shadow: 0 2px 8px rgba(66, 133, 244, 0.3) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            letter-spacing: 0.5px !important;
        }
        
        .stButton > button[kind="primary"]:hover {
            background: linear-gradient(135deg, #1a73e8 0%, #1557b0 100%) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 16px rgba(66, 133, 244, 0.4) !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        google_login = st.button("🔐 Zaloguj się przez Google Workspace", use_container_width=True, type="primary")
        
        if google_login:
            # Krótka animacja autoryzacji
            with st.spinner("Autoryzacja Google..."):
                import time
                time.sleep(0.8)  # Krótka animacja 0.8s
            
            st.success("✅ Autoryzacja Google zakończona pomyślnie!")
            st.session_state.google_authorized = True
            st.rerun()
    
    # Jeśli użytkownik jest "autoryzowany" przez Google
    if st.session_state.get("google_authorized", False):
        # Nagłówek z animacją
        st.markdown("""
        <div style="text-align: center; margin: 2rem 0 1rem 0;">
            <h2 style="
                font-size: 1.5rem;
                font-weight: 600;
                color: #1d1d1f;
                margin: 0;
                animation: fadeIn 0.8s ease-out;
            ">Wybierz swoje konto</h2>
            <p style="
                font-size: 0.9rem;
                color: #666;
                margin: 0.5rem 0 0 0;
                animation: fadeIn 0.8s ease-out 0.2s both;
            ">Autoryzacja Google zakończona pomyślnie</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Lista kont Google z rolami i animacjami
        google_accounts = [
            {"email": "anna.kowalska@energetyka.pl", "name": "Anna Kowalska", "role": "Pracownik", "department": "IT", "avatar": "👩‍💻"},
            {"email": "jan.nowak@energetyka.pl", "name": "Jan Nowak", "role": "Lider zespołu", "department": "HR", "avatar": "👨‍💼"},
            {"email": "maria.wisniewska@energetyka.pl", "name": "Maria Wiśniewska", "role": "Koordynator HR", "department": "HR", "avatar": "👩‍💼"},
            {"email": "piotr.kowalczyk@energetyka.pl", "name": "Piotr Kowalczyk", "role": "Administrator systemu", "department": "IT", "avatar": "👨‍💻"},
            {"email": "katarzyna.zielinska@energetyka.pl", "name": "Katarzyna Zielińska", "role": "Zarząd", "department": "Zarząd", "avatar": "👩‍💼"},
            {"email": "tomasz.dabrowski@energetyka.pl", "name": "Tomasz Dąbrowski", "role": "Koordynator programu Mam wpływ", "department": "HR", "avatar": "👨‍💼"}
        ]
        
        for i, account in enumerate(google_accounts):
            # Karta użytkownika z animacją delay
            user_card = f"""
            <div style="
                background: rgba(255, 255, 255, 0.8);
                border-radius: 12px;
                padding: 1rem;
                margin: 0.5rem 0;
                border: 1px solid rgba(0, 0, 0, 0.05);
                transition: all 0.3s ease;
                animation: grow 0.3s ease-out {0.1 + i * 0.05}s both;
                cursor: pointer;
            " 
            onmouseover="this.style.background='rgba(0, 122, 255, 0.05)'; this.style.transform='translateX(8px)';"
            onmouseout="this.style.background='rgba(255, 255, 255, 0.8)'; this.style.transform='translateX(0)';">
                <div style="display: flex; align-items: center;">
                    <div style="
                        background: rgba(25, 118, 210, 0.1);
                        border-radius: 50%;
                        width: 48px;
                        height: 48px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 1.5rem;
                        margin-right: 1rem;
                    ">{account["avatar"]}</div>
                    <div>
                        <div style="font-weight: 600; color: #1d1d1f; margin-bottom: 2px;">
                            {account["name"]}
                        </div>
                        <div style="font-size: 0.875rem; color: #666;">
                            {account["email"]} • {account["role"]}
                        </div>
                    </div>
                </div>
            </div>
            """
            st.markdown(user_card, unsafe_allow_html=True)
            
            if st.button(f"Wybierz", key=f"google_{account['email']}", use_container_width=True):
                # Znajdź użytkownika w bazie danych
                user = next((emp for emp in st.session_state.employees if emp["email"] == account["email"]), None)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.current_user = user
                    # Automatycznie ustaw kontekst na rolę użytkownika
                    st.session_state.current_context = user["role"]
                    st.session_state.google_authorized = False  # Reset
                    st.success(f"Zalogowano jako {user['name']} ({user['role']})")
                    st.rerun()
    
    # Footer w stylu Material-UI
    if not st.session_state.get("google_authorized", False):
        st.markdown("""
        <div style="
            text-align: center;
            font-size: 0.875rem;
            color: #666;
            border-top: 1px solid rgba(0, 0, 0, 0.1);
            padding-top: 1.5rem;
            margin-top: 2rem;
            animation: fadeIn 1s ease-out 1.2s both;
        ">
            🔒 Połączenie zabezpieczone SSL/TLS<br />
            🛡️ Zgodność z RODO • 🔐 Autoryzacja dwuskładnikowa
        </div>
        """, unsafe_allow_html=True)

# Funkcja wyboru kontekstu
def context_selection():
    # Czysta strona wyboru kontekstu
    st.markdown(f"""
    <div style="text-align: center; padding: 3rem 0;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">👋</div>
        <h1 style="font-size: 2.5rem; font-weight: 600; margin: 0; color: #1d1d1f;">
            Witaj {st.session_state.current_user['name']}!
        </h1>
        <p style="font-size: 1.2rem; color: #86868b; margin: 1rem 0; font-weight: 400;">
            Wybierz kontekst pracy w systemie TARCZA
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Lista dostępnych aktorów/ról
    available_contexts = [
        "Pracownik",
        "Lider zespołu", 
        "Koordynator HR",
        "Administrator systemu",
        "Zarząd",
        "Koordynator programu Mam wpływ"
    ]
    
    # Filtruj konteksty na podstawie roli użytkownika
    user_role = st.session_state.current_user["role"]
    if user_role in available_contexts:
        available_contexts = [user_role]  # Użytkownik może pracować tylko w swojej roli
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Dostępne konteksty pracy:")
        
        # Konteksty jako proste przyciski
        context_icons = {
            "Pracownik": "👤",
            "Lider zespołu": "👨‍💼", 
            "Koordynator HR": "👩‍💼",
            "Administrator systemu": "⚙️",
            "Zarząd": "🏢",
            "Koordynator programu Mam wpływ": "💡"
        }
        
        for i, context in enumerate(available_contexts):
            icon = context_icons.get(context, "🎭")
            if st.button(f"{icon} {context}", key=f"context_{i}", use_container_width=True):
                st.session_state.current_context = context
                st.rerun()
    
    with col2:
        # Informacje o kontekstach - czyste
        st.subheader("ℹ️ Informacja o kontekstach")
        
        st.markdown("""
        **Pracownik:** Podstawowe funkcje pracownicze
        
        **Lider zespołu:** Zarządzanie zespołem i oceny
        
        **Koordynator HR:** Administracja HR i raporty
        
        **Administrator:** Zarządzanie systemem
        
        **Zarząd:** Raporty strategiczne
        
        **Koordynator "Mam wpływ":** Zarządzanie inicjatywami
        """)

# Funkcja głównego menu
def main_menu():
    # Czysty sidebar Apple
    st.sidebar.title("🛡️ System TARCZA")
    st.sidebar.write(f"**Użytkownik:** {st.session_state.current_user['name']}")
    st.sidebar.write(f"**Kontekst:** {st.session_state.current_context}")
    
    # Przycisk wyloguj
    if st.sidebar.button("🚪 Wyloguj", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.session_state.current_context = None
        st.rerun()
    
    st.sidebar.markdown("---")
    
    # Menu opcji w zależności od kontekstu
    context = st.session_state.current_context
    
    menu_options = []
    
    # Opcje wspólne dla wszystkich
    menu_options.append("🏠 Strona główna")
    menu_options.append("👤 Mój profil")
    
    # Opcje specyficzne dla kontekstu
    if context in ["Pracownik", "Lider zespołu", "Koordynator HR", "Administrator systemu", "Zarząd", "Koordynator programu Mam wpływ"]:
        menu_options.append("🏆 Moduł Kudosów")
    
    if context in ["Koordynator HR", "Administrator systemu", "Zarząd"]:
        menu_options.append("👥 Lista pracowników")
    
    if context in ["Koordynator programu Mam wpływ", "Zarząd"]:
        menu_options.append("💡 Program Mam wpływ")
    
    if context in ["Zarząd"]:
        menu_options.append("📊 Raport struktury zatrudnienia")
    
    # Wybór opcji menu
    selected_option = st.sidebar.selectbox("Wybierz opcję:", menu_options)
    
    return selected_option

# Strona główna
def home_page():
    # Czysta strona główna Apple
    st.markdown("""
    <div style="text-align: center; padding: 3rem 0;">
        <div style="font-size: 3.5rem; margin-bottom: 1rem;">🏠</div>
        <h1 style="font-size: 2.8rem; font-weight: 700; margin: 0; color: #1d1d1f;">
            Witamy w systemie TARCZA
        </h1>
        <p style="font-size: 1.2rem; color: #86868b; margin: 1rem 0; font-weight: 400;">
            Twój hub do zarządzania rozwojem i współpracą w zespole
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Ostatnie aktywności")
        
        if st.session_state.kudos:
            recent_kudos = st.session_state.kudos[-3:]  # Ostatnie 3 kudosy
            for kudos in reversed(recent_kudos):
                st.info(f"🏆 {kudos['giver']} przyznał kudosa {kudos['recipient']} za {kudos['value']} • {kudos['date']}")
        else:
            st.info("📭 Brak ostatnich aktywności. Bądź pierwszy i przyznaj Kudosa!")
    
    with col2:
        st.subheader("📈 Statystyki systemu")
        
        # Czyste metryki
        st.metric("🏆 Kudosy", len(st.session_state.kudos))
        st.metric("👥 Pracownicy", len(st.session_state.employees))
        st.metric("💡 Inicjatywy", len(st.session_state.initiatives))

# Moduł profilu użytkownika
def profile_page():
    st.title("👤 Mój profil")
    
    user = st.session_state.current_user
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Dane osobowe")
        st.text_input("Imię i nazwisko", value=user["name"], disabled=True)
        st.text_input("Email", value=user["email"], disabled=True)
        st.text_input("Rola", value=user["role"], disabled=True)
        st.text_input("Departament", value=user["department"], disabled=True)
    
    with col2:
        st.header("Edytowalne dane")
        with st.form("profile_form"):
            phone = st.text_input("Telefon", placeholder="Wprowadź numer telefonu")
            bio = st.text_area("Bio", placeholder="Napisz coś o sobie")
            skills = st.text_input("Umiejętności", placeholder="JavaScript, Python, Zarządzanie projektami")
            
            if st.form_submit_button("Zapisz zmiany"):
                st.success("Profil został zaktualizowany!")

# Moduł Kudosów
def kudos_module():
    st.title("🏆 Moduł Kudosów")
    
    tab1, tab2, tab3 = st.tabs(["Przyznaj Kudosa", "Wszystkie Kudosy", "Statystyki"])
    
    with tab1:
        st.header("Przyznaj Kudosa współpracownikowi")
        
        with st.form("kudos_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                # Lista pracowników (bez siebie)
                employees_list = [emp["name"] for emp in st.session_state.employees 
                                if emp["name"] != st.session_state.current_user["name"]]
                recipient = st.selectbox("Komu przyznajesz Kudosa?", employees_list)
                
                value = st.selectbox("Za jaką wartość organizacyjną?", COMPANY_VALUES)
            
            with col2:
                reason = st.text_area("Uzasadnienie (opisz konkretne działanie)", height=100)
                visibility = st.selectbox("Widoczność", ["Publiczny", "Tylko dla zespołu", "Prywatny"])
            
            submit = st.form_submit_button("🏆 Przyznaj Kudosa", use_container_width=True)
            
            if submit and recipient and reason:
                new_kudos = {
                    "id": len(st.session_state.kudos) + 1,
                    "giver": st.session_state.current_user["name"],
                    "recipient": recipient,
                    "value": value,
                    "reason": reason,
                    "visibility": visibility,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "department": st.session_state.current_user["department"]
                }
                st.session_state.kudos.append(new_kudos)
                st.success(f"🎉 Kudos dla {recipient} za {value} został przyznany!")
                st.rerun()
    
    with tab2:
        st.header("Historia Kudosów")
        
        if st.session_state.kudos:
            # Filtrowanie
            col1, col2, col3 = st.columns(3)
            with col1:
                filter_value = st.selectbox("Filtruj po wartości", ["Wszystkie"] + COMPANY_VALUES)
            with col2:
                filter_recipient = st.selectbox("Filtruj po odbiorcy", ["Wszystkie"] + [emp["name"] for emp in st.session_state.employees])
            with col3:
                sort_by = st.selectbox("Sortuj po", ["Data (najnowsze)", "Data (najstarsze)", "Wartość", "Odbiorca"])
            
            # Przygotowanie danych do wyświetlenia
            kudos_to_display = st.session_state.kudos.copy()
            
            # Filtrowanie
            if filter_value != "Wszystkie":
                kudos_to_display = [k for k in kudos_to_display if k["value"] == filter_value]
            if filter_recipient != "Wszystkie":
                kudos_to_display = [k for k in kudos_to_display if k["recipient"] == filter_recipient]
            
            # Sortowanie
            if sort_by == "Data (najnowsze)":
                kudos_to_display.sort(key=lambda x: x["date"], reverse=True)
            elif sort_by == "Data (najstarsze)":
                kudos_to_display.sort(key=lambda x: x["date"])
            elif sort_by == "Wartość":
                kudos_to_display.sort(key=lambda x: x["value"])
            elif sort_by == "Odbiorca":
                kudos_to_display.sort(key=lambda x: x["recipient"])
            
            # Wyświetlenie kudosów
            for kudos in kudos_to_display:
                with st.expander(f"🏆 {kudos['giver']} → {kudos['recipient']} za {kudos['value']} ({kudos['date']})"):
                    st.write(f"**Uzasadnienie:** {kudos['reason']}")
                    st.write(f"**Widoczność:** {kudos['visibility']}")
                    st.write(f"**Departament:** {kudos['department']}")
        else:
            st.info("Brak przyznanych Kudosów. Bądź pierwszy!")
    
    with tab3:
        st.header("Statystyki Kudosów")
        
        if st.session_state.kudos:
            df = pd.DataFrame(st.session_state.kudos)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Najczęściej nagradzane wartości")
                value_counts = df["value"].value_counts()
                st.bar_chart(value_counts)
                
                st.subheader("Top odbiorcy Kudosów")
                recipient_counts = df["recipient"].value_counts().head(5)
                for name, count in recipient_counts.items():
                    st.write(f"🏆 {name}: {count} Kudosów")
            
            with col2:
                st.subheader("Aktywność w czasie")
                df['date'] = pd.to_datetime(df['date'])
                daily_counts = df.groupby(df['date'].dt.date).size()
                st.line_chart(daily_counts)
                
                st.subheader("Kudosy według departamentów")
                dept_counts = df["department"].value_counts()
                fig = px.pie(values=dept_counts.values, names=dept_counts.index, title="Kudosy według departamentów")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Brak danych do wyświetlenia statystyk")

# Lista pracowników (dla Koordynatorów HR, Administratorów, Zarządu)
def employees_list():
    st.title("👥 Lista pracowników")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.header("Filtrowanie")
        search_name = st.text_input("🔍 Wyszukaj po nazwisku")
        filter_department = st.selectbox("Departament", ["Wszystkie", "IT", "HR", "Zarząd"])
        filter_role = st.selectbox("Rola", ["Wszystkie"] + list(set([emp["role"] for emp in st.session_state.employees])))
    
    with col2:
        st.header("Pracownicy")
        
        # Filtrowanie pracowników
        filtered_employees = st.session_state.employees.copy()
        
        if search_name:
            filtered_employees = [emp for emp in filtered_employees if search_name.lower() in emp["name"].lower()]
        if filter_department != "Wszystkie":
            filtered_employees = [emp for emp in filtered_employees if emp["department"] == filter_department]
        if filter_role != "Wszystkie":
            filtered_employees = [emp for emp in filtered_employees if emp["role"] == filter_role]
        
        # Wyświetlenie pracowników
        for emp in filtered_employees:
            with st.expander(f"👤 {emp['name']} - {emp['role']}"):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write(f"**Email:** {emp['email']}")
                    st.write(f"**Departament:** {emp['department']}")
                with col_b:
                    if st.button(f"Edytuj dane", key=f"edit_{emp['id']}"):
                        st.info("Funkcja edycji zostanie wdrożona w pełnej wersji systemu")
                    if st.button(f"Wyświetl profil", key=f"profile_{emp['id']}"):
                        st.info("Funkcja podglądu profilu zostanie wdrożona w pełnej wersji systemu")

# Program "Mam wpływ"
def mam_wplyw_program():
    st.title("💡 Program 'Mam wpływ'")
    
    tab1, tab2, tab3 = st.tabs(["Zgłoś inicjatywę", "Wszystkie inicjatywy", "Statystyki"])
    
    with tab1:
        st.header("Zgłoś swoją inicjatywę")
        
        with st.form("initiative_form"):
            title = st.text_input("Tytuł inicjatywy")
            description = st.text_area("Opis problemu/możliwości", height=100)
            solution = st.text_area("Proponowane rozwiązanie", height=100)
            category = st.selectbox("Kategoria", [
                "Usprawnienie procesów",
                "Oszczędności",
                "Kultura organizacyjna", 
                "Technologia",
                "Środowisko pracy",
                "Inne"
            ])
            expected_impact = st.selectbox("Oczekiwany wpływ", ["Niski", "Średni", "Wysoki"])
            
            submit = st.form_submit_button("💡 Zgłoś inicjatywę")
            
            if submit and title and description and solution:
                new_initiative = {
                    "id": len(st.session_state.initiatives) + 1,
                    "title": title,
                    "description": description,
                    "solution": solution,
                    "category": category,
                    "expected_impact": expected_impact,
                    "author": st.session_state.current_user["name"],
                    "status": "Nowa",
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "votes": 0,
                    "comments": []
                }
                st.session_state.initiatives.append(new_initiative)
                st.success(f"✅ Inicjatywa '{title}' została zgłoszona!")
                st.rerun()
    
    with tab2:
        st.header("Wszystkie inicjatywy")
        
        if st.session_state.initiatives:
            for init in reversed(st.session_state.initiatives):  # Najnowsze na górze
                with st.expander(f"💡 {init['title']} - {init['status']} ({init['author']})"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"**Opis:** {init['description']}")
                        st.write(f"**Rozwiązanie:** {init['solution']}")
                        st.write(f"**Kategoria:** {init['category']}")
                        st.write(f"**Oczekiwany wpływ:** {init['expected_impact']}")
                    
                    with col2:
                        st.write(f"**Data:** {init['date']}")
                        st.write(f"**Głosy:** {init['votes']}")
                        
                        if st.button(f"👍 Zagłosuj", key=f"vote_{init['id']}"):
                            # Znajdź inicjatywę i zwiększ liczbę głosów
                            for i, initiative in enumerate(st.session_state.initiatives):
                                if initiative['id'] == init['id']:
                                    st.session_state.initiatives[i]['votes'] += 1
                                    break
                            st.rerun()
                        
                        if st.session_state.current_context == "Koordynator programu Mam wpływ":
                            status_options = ["Nowa", "W ocenie", "Zaakceptowana", "W realizacji", "Zrealizowana", "Odrzucona"]
                            new_status = st.selectbox("Status", status_options, 
                                                    index=status_options.index(init['status']), 
                                                    key=f"status_{init['id']}")
                            if st.button(f"Aktualizuj status", key=f"update_{init['id']}"):
                                for i, initiative in enumerate(st.session_state.initiatives):
                                    if initiative['id'] == init['id']:
                                        st.session_state.initiatives[i]['status'] = new_status
                                        break
                                st.success("Status zaktualizowany!")
                                st.rerun()
        else:
            st.info("Brak zgłoszonych inicjatyw. Bądź pierwszy!")
    
    with tab3:
        st.header("Statystyki programu")
        
        if st.session_state.initiatives:
            df = pd.DataFrame(st.session_state.initiatives)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Inicjatywy według kategorii")
                category_counts = df["category"].value_counts()
                st.bar_chart(category_counts)
                
                st.subheader("Status inicjatyw")
                status_counts = df["status"].value_counts()
                fig = px.pie(values=status_counts.values, names=status_counts.index, title="Status inicjatyw")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("Najaktywniej głosujący")
                top_initiatives = df.nlargest(5, 'votes')[['title', 'votes']]
                for _, row in top_initiatives.iterrows():
                    st.write(f"💡 {row['title']}: {row['votes']} głosów")
                
                st.subheader("Metryki")
                st.metric("Łączna liczba inicjatyw", len(st.session_state.initiatives))
                st.metric("Zrealizowane inicjatywy", len(df[df['status'] == 'Zrealizowana']))
                st.metric("Średnia liczba głosów", round(df['votes'].mean(), 1) if len(df) > 0 else 0)
        else:
            st.info("Brak danych do wyświetlenia statystyk")

# Raport struktury zatrudnienia (dla Zarządu)
def employment_structure_report():
    st.title("📊 Raport struktury zatrudnienia")
    
    if st.session_state.current_context != "Zarząd":
        st.error("Brak uprawnień do wyświetlenia tego raportu")
        return
    
    employees_df = pd.DataFrame(st.session_state.employees)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Struktura według departamentów")
        dept_counts = employees_df["department"].value_counts()
        fig = px.pie(values=dept_counts.values, names=dept_counts.index, title="Struktura według departamentów")
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Struktura według ról")
        role_counts = employees_df["role"].value_counts()
        st.bar_chart(role_counts)
    
    with col2:
        st.subheader("Kluczowe wskaźniki")
        st.metric("Łączna liczba pracowników", len(st.session_state.employees))
        st.metric("Liczba departamentów", employees_df["department"].nunique())
        st.metric("Liczba ról", employees_df["role"].nunique())
        
        st.subheader("Szczegółowe dane")
        st.dataframe(employees_df)
    
    # Opcja pobierania raportu
    if st.button("📥 Pobierz raport (CSV)"):
        csv = employees_df.to_csv(index=False)
        st.download_button(
            label="💾 Pobierz plik CSV",
            data=csv,
            file_name=f"raport_zatrudnienia_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

# Główna funkcja aplikacji
def main():
    init_session_state()
    
    # Sprawdzenie statusu logowania
    if not st.session_state.logged_in:
        login_page()
        return
    
    # Usuń klasę logowania po zalogowaniu i przywróć normalne tło
    st.markdown("""
    <script>
        document.querySelector('.stApp').style.background = '#f5f5f7';
        document.body.classList.remove('login-page');
    </script>
    """, unsafe_allow_html=True)
    
    # Jeśli nie ma kontekstu, ustaw na podstawie roli użytkownika
    if not st.session_state.current_context:
        st.session_state.current_context = st.session_state.current_user["role"]
    
    # Główne menu i nawigacja
    selected_option = main_menu()
    
    # Routing do odpowiednich stron
    if selected_option == "🏠 Strona główna":
        home_page()
    elif selected_option == "👤 Mój profil":
        profile_page()
    elif selected_option == "🏆 Moduł Kudosów":
        kudos_module()
    elif selected_option == "👥 Lista pracowników":
        employees_list()
    elif selected_option == "💡 Program Mam wpływ":
        mam_wplyw_program()
    elif selected_option == "📊 Raport struktury zatrudnienia":
        employment_structure_report()

if __name__ == "__main__":
    main()