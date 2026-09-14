import streamlit as st
import json
import os
import random
from huggingface_hub import hf_hub_download

# KONFIGURACJA STRONY
st.set_page_config(
    page_title="Angielski Czas - Krok po Kroku",
    page_icon="🇬🇧",
    layout="wide"
)


def wyswietl_sekcje_wsparcia():

    if "parent_verified" not in st.session_state:
        st.session_state.parent_verified = False
    if "num1" not in st.session_state:
        st.session_state.num1 = random.randint(5, 15)
    if "num2" not in st.session_state:
        st.session_state.num2 = random.randint(5, 15)

    LINK_DO_KAWY = "https://buycoffee.to"

    st.divider()

    with st.expander("👪 Dla Rodziców / Starszych Uczniów (Strefa Wspierania)"):
        if not st.session_state.parent_verified:
            st.write("Aby wejść, potwierdź że jesteś osobą dorosłą:")
            pytanie = f"Ile to jest {st.session_state.num1} + {st.session_state.num2}?"

            
            odpowiedz_rodzica = st.number_input(pytanie, step=1, value=None, key="footer_parent_input")

            if st.button("Zatwierdź", key="footer_parent_btn", use_container_width=True):
                poprawny_wynik = st.session_state.num1 + st.session_state.num2
                if odpowiedz_rodzica == poprawny_wynik:
                    st.session_state.parent_verified = True
                    st.rerun()
                else:
                    st.error("Nieprawidłowy wynik. Spróbuj ponownie!")
        else:
            st.success("Weryfikacja pomyślna!")
            st.markdown(
                """
                **Drogi Rodzicu / Starszy Uczniu!**  
                Tworzę te aplikacje z myślą o bezpiecznym i skutecznym rozwoju oraz nauce. 
                Udostępniam je całkowicie **za darmo i bez reklam**.

                Utrzymanie projektów wymaga jednak realnych kosztów i setek godzin pracy. 
                Jeśli aplikacja pomogła w nauce i chcesz wesprzeć rozwój kolejnych programów 
                – możesz postawić mi wirtualną kawę. Dziękuję!
                """
            )
            st.link_button("☕ Postaw wirtualną kawę", LINK_DO_KAWY, type="primary", use_container_width=True)

            if st.button("Zablokuj strefę", type="secondary", use_container_width=True, key="footer_lock_btn"):
                st.session_state.parent_verified = False
                st.session_state.num1 = random.randint(5, 15)
                st.session_state.num2 = random.randint(5, 15)
                st.rerun()

            st.caption(
                "**Informacja o wsparciu:** "
                "Wszelkie wpłaty realizowane za pośrednictwem platformy BuyCoffee.to mają charakter "
                "całkowicie dobrowolnego, bezinteresownego wsparcia (darowizny) na rzecz dalszego rozwoju "
                "i utrzymania portfolio bezpłatnych aplikacji."
            )


# ŁADOWANIE DANYCH Z PRYWATNEGO REPOZYTORIUM HF
@st.cache_data
def load_tenses_data():
    try:
        # Pobranie tokenu z bezpiecznych sekretów Streamlit
        hf_token = st.secrets["HF_TOKEN"]
        
        # Pobranie ścieżki do pliku z Hugging Face
        repo_file_path = hf_hub_download(
            repo_id="Radar1111/AngielskiCzasy",
            filename="tenses.json",
            repo_type="dataset",                                
            token=hf_token
        )
        
        # Odczytanie pobranego pliku JSON
        with open(repo_file_path, "r", encoding="utf-8") as f:
            return json.load(f)
            
    except Exception as e:
        # Obsługa błędów (brak pliku, błędny token, błąd JSON)
        st.error(f"Błąd podczas ładowania danych z HF: {e}")
        return None


# Główna logika programu
tenses = load_tenses_data()

# Sprawdzenie, czy słownik nie jest pusty i czy plik istnieje
if tenses and isinstance(tenses, dict) and len(tenses) > 0:

    # Nagłówek aplikacji
    st.title("🇬🇧 Interaktywny Przewodnik po Czasach Angielskich")
    st.markdown("Naucz się budowy i zastosowania czasów krok po kroku.")

    # Sidebar do wyboru
    st.sidebar.header("Nawigacja")
    selected_tense = st.sidebar.selectbox("Wybierz czas gramatyczny:", list(tenses.keys()))


    with st.sidebar:
        wyswietl_sekcje_wsparcia()

    data = tenses[selected_tense]

    # Prezentacja wybranego czasu
    st.header(f"Czas: {selected_tense}")
    st.info(f"💡 **Zastosowanie:** {data.get('definition', 'Brak definicji')}")

    # Podział na kolumny
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📝 Forma czasownika")
        st.markdown(f"{data.get('verb_form', 'Brak danych')}")

    with col2:
        st.subheader("📋 Słówka posiłkowe (Operatory)")
        st.markdown(f"{data.get('auxiliary_verbs', 'Brak danych')}")

    # Budowa krok po kroku 
    if 'construction' in data:
        st.subheader("🧱 Budowa zdania krok po kroku")
        for idx, step in enumerate(data['construction'], 1):
            st.markdown(f"**Krok {idx}:** {step}")

    # Przykłady zdań w zakładkach
    if 'examples' in data:
        st.subheader("🔍 Przykłady użycia")
        tab1, tab2, tab3 = st.tabs(["➕ Zdania twierdzące", "➖ Zdania przeczące", "❓ Pytania"])

        with tab1:
            st.code(data['examples'].get('positive', ''), language="text")
        with tab2:
            st.code(data['examples'].get('negative', ''), language="text")
        with tab3:
            st.code(data['examples'].get('question', ''), language="text")

    # Słowa kluczowe
    if 'keywords' in data:
        st.subheader("🔑 Słowa kluczowe (Keywords)")
        keywords_str = ", ".join([f"'{kw}'" for kw in data['keywords']])
        st.markdown(f"Często spotykane wskaźniki czasu: {keywords_str}")

else:

    st.error("Nie znaleziono pliku `tenses.json` lub plik jest uszkodzony / pusty.")
    st.info(
        "Upewnij się, że plik `tenses.json` znajduje się w tym samym katalogu co skrypt i ma poprawną strukturę JSON.")
