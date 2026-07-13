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

# Sekcja Donate na samym dole panelu bocznego
st.sidebar.markdown("---")
st.sidebar.subheader("☕ Wesprzyj projekt")
st.sidebar.caption("Tworzenie darmowych narzędzi to moja pasja! Jeśli moje aplikacje okazały się dla Ciebie przydatne i chcesz docenić czas, który poświęcam na ich rozwijanie, możesz postawić mi wirtualne espresso.Każda kawa to dla mnie ogromna motywacja i bezinteresowne wsparcie, dzięki któremu mogę dalej dzielić się swoją pasją ze społecznością.")
st.sidebar.link_button("☕ Postaw mi kawę", "https://buycoffee.to/gigawiedza")
st.sidebar.caption(
    "**Informacja o wsparciu:**"
    "Wszelkie wpłaty realizowne za posrednictwem platformy BuyCoffee.to maja charakter "
    "całkowicie dobrowolnego, bezinteresownego wsparcia (darowizny) na rzecz dalszego rozwoju "
    "i utrzymania portfolio bezpłatnych aplikacji. Wpłata nie wiąże sie z zakupem żadnych "
    "cyfrowych towarów, usług ani dodatkowych funkcji w aplikacji."
)

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
