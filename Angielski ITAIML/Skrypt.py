import json
import os
import streamlit as st
from huggingface_hub import hf_hub_download  


# Konfiguracja strony 
st.set_page_config(page_title="DevVocab: IT, AI i ML", page_icon="💻")


@st.cache_data
def load_app_data():
    """Wczytuje kompletną bazę słów z prywatnego pliku JSON na Hugging Face."""
    
    REPO_ID = "Radar1111/AngielskiITAIML" 
    FILENAME = "words.json"
    
    try:
        # Pobieranie tokenu 
        if "HF_TOKEN" not in st.secrets:
            st.sidebar.error("Błąd: Brak klucza HF_TOKEN w zakładce Secrets Streamlita!")
            return []
            
        token = st.secrets["HF_TOKEN"]
        
        # Bezpieczne pobranie pliku z Hugging Face 
        local_file_path = hf_hub_download(
            repo_id=REPO_ID, 
            filename=FILENAME, 
            token=token,
            repo_type="dataset" 
        )
        
        # 3. Wczytanie pobranego pliku JSON
        with open(local_file_path, "r", encoding="utf-8") as f:
            words = json.load(f)
        return words

    except Exception as e:
        
        st.sidebar.error(f"Szczegóły błędu połączenia z HF: {e}")
        return []

def wyswietl_sekcje_wsparcia():
    # Inicjalizacja sesji wewnątrz funkcji (bezpieczne dla każdej strony)
    if "parent_verified" not in st.session_state:
        st.session_state.parent_verified = False
    if "num1" not in st.session_state:
        st.session_state.num1 = random.randint(5, 15)
    if "num2" not in st.session_state:
        st.session_state.num2 = random.randint(5, 15)

    LINK_DO_KAWY = "https://buycoffee.to/gigawiedza"

    # Separator odcinający treść edukacyjną
    st.divider()

    # Expander na dole strony
    with st.expander("👪 Dla Rodziców / Starszych Uczniów (Strefa Wspierania)"):
        if not st.session_state.parent_verified:
            st.write("Aby wejść, potwierdź że jesteś osobą dorosłą:")
            pytanie = f"Ile to jest {st.session_state.num1} + {st.session_state.num2}?"
            
            # Użycie unikalnego klucza w widgetach zapobiega konfliktom w Streamlit
            odpowiedz_rodzica = st.number_input(pytanie, step=1, value=0, key="footer_parent_input")

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
            "i utrzymania portfolio bezpłatnych aplikacji. Wpłata nie wiąże się z zakupem żadnych "
            "cyfrowych towarów, usług ani dodatkowych funkcji w aplikacji."
        )

# Wywołanie funkcji
WORDS_DATA = load_app_data()

st.title("💻 DevVocab: IT, AI i ML")
st.subheader("Nauka angielskiego do IT, AI i ML")
st.markdown("##### *Naucz się angielskiego, którego naprawdę używa się w biurze. Oficjalne pojęcia, quizy i żywy slang bez podręcznikowej nudy.*")

# Pamięć sesji
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "show_translation" not in st.session_state:
    st.session_state.show_translation = False
if "quiz_answered" not in st.session_state:
    st.session_state.quiz_answered = False

# Panel boczny
st.sidebar.header("Ustawienia nauki")
level = st.sidebar.selectbox("Wybierz poziom trudności:", ["Junior", "Mid", "Senior"])
mode = st.sidebar.radio("Wybierz tryb:", ["Fiszki słówek", "Slang biurowy (Ponglish)", "Quiz (Zdania z luką)"])

with st.sidebar:
    wyswietl_sekcje_wsparcia()

# Filtrowanie danych po poziomie trudności
filtered_data = [w for w in WORDS_DATA if w.get("level") == level]

# Reset indeksu przy zmianie poziomu lub trybu
if "last_level" not in st.session_state or st.session_state.last_level != level or st.session_state.last_mode != mode:
    st.session_state.current_index = 0
    st.session_state.show_translation = False
    st.session_state.quiz_answered = False
    st.session_state.last_level = level
    st.session_state.last_mode = mode

# Zabezpieczenie przed brakiem danych
if not filtered_data:
    st.warning(f"Brak danych dla poziomu {level} w pliku JSON lub baza się jeszcze nie załadowała.")
else:
    if st.session_state.current_index >= len(filtered_data):
        st.session_state.current_index = 0

    item = filtered_data[st.session_state.current_index]

    # FISZKI SŁÓWEK
    if mode == "Fiszki słówek":
        st.info(f"Kategoria: {item.get('category', 'Ogólne')} | Karta {st.session_state.current_index + 1} z {len(filtered_data)}")

        with st.container(border=True):
            word_en = item.get("word_en", item.get("word", "Brak słowa"))
            part_speech = item.get("part_of_speech", "noun")
            
            st.markdown(f"### EN: `{word_en}` *({part_speech})*")
            st.write(f"*Definition:* {item.get('definition_en', '')}")

            if st.session_state.show_translation:
                st.divider()
                word_pl = item.get("word_pl", "Brak tłumaczenia")
                st.markdown(f"### PL: **{word_pl}**")
                st.write(f"*Definicja:* {item.get('definition_pl', '')}")

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Pokaż/Ukryj tłumaczenie"):
                st.session_state.show_translation = not st.session_state.show_translation
                st.rerun()
        with col3:
            if st.button("Dalej"):
                st.session_state.current_index = (st.session_state.current_index + 1) % len(filtered_data)
                st.session_state.show_translation = False
                st.rerun()

    # SLANG BIUROWY
    elif mode == "Slang biurowy (Ponglish)":
        if "office_slang" in item and item["office_slang"]:
            slang = item["office_slang"]
            word_en = item.get("word_en", item.get("word", "Brak słowa"))

            st.success(f"Jak przetrwać w korpo? | Słowo: {word_en} | {st.session_state.current_index + 1} z {len(filtered_data)}")

            with st.container(border=True):
                st.markdown(f"### 💬 W biurze usłyszysz: **„{slang.get('term', '')}”**")
                st.write(f"💡 *Co to naprawdę znaczy:* {slang.get('meaning', '')}")
                
                st.divider()
                st.markdown("##### 🎧 Przykładowy cytat z Daily / czatu:")
                st.info(f"„{slang.get('live_example', '')}”")

            col1, col2, col3 = st.columns(3)
            with col3:
                if st.button("Następny slang"):
                    st.session_state.current_index = (st.session_state.current_index + 1) % len(filtered_data)
                    st.rerun()
        else:
            st.warning(f"Słowo `{item.get('word_en', '')}` nie ma jeszcze przypisanego slangu.")
            if st.button("Pomiń i idź dalej"):
                st.session_state.current_index = (st.session_state.current_index + 1) % len(filtered_data)
                st.rerun()

    # QUIZ
    elif mode == "Quiz (Zdania z luką)":
        if "cloze_test" in item and item["cloze_test"]:
            cloze = item["cloze_test"]

            st.warning(f"Uzupełnij brakujące słowo IT, AI lub ML | Zdanie {st.session_state.current_index + 1} z {len(filtered_data)}")

            with st.container(border=True):
                st.markdown(f"### `{cloze.get('text_with_gap', '')}`")
                st.caption(f"Tłumaczenie: {item.get('example_sentence_pl', '')}")

            options = sorted(list(set(cloze.get("distractors", []) + [cloze.get("correct_answer", "")])))

            user_choice = st.radio("Wybierz poprawną odpowiedź:", options, key=f"quiz_radio_{st.session_state.current_index}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Sprawdź odpowiedź"):
                    st.session_state.quiz_answered = True
                    st.rerun()

            if st.session_state.quiz_answered:
                if user_choice == cloze.get("correct_answer"):
                    st.success("Doskonale! To poprawna odpowiedź.")
                else:
                    st.error(f"Błąd. Poprawna odpowiedź to: **{cloze.get('correct_answer')}**")

            with col2:
                if st.button("Następne pytanie"):
                    st.session_state.current_index = (st.session_state.current_index + 1) % len(filtered_data)
                    st.session_state.quiz_answered = False
                    st.rerun()
        else:
            st.warning(f"Słowo `{item.get('word_en', '')}` nie posiada przygotowanego quizu.")
            if st.button("Następne słowo"):
                st.session_state.current_index = (st.session_state.current_index + 1) % len(filtered_data)
                st.rerun()
