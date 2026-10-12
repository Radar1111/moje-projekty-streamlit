import streamlit as st
import json
import random
from huggingface_hub import hf_hub_download


# 1. Konfiguracja strony i ładowanie danych
st.set_page_config(page_title="Niemiecki Klasa 7 - Trener", page_icon="🇩🇪", layout="centered")


@st.cache_data
def load_data():
    repo_id = "Radar1111/Niemiecki"
    filename = "words.json"
    
    # Pobranie tokenu ze Streamlit Secrets
    hf_token = st.secrets.get("HF_TOKEN")
    if not hf_token:
        st.error("Brak tokenu HF_TOKEN w konfiguracji Streamlit Secrets!")
        return get_fallback_data()
        
    try:
        # Pobranie pliku z prywatnego repozytorium HF
        local_file_path = hf_hub_download(
            repo_id=repo_id,
            filename=filename,
            repo_type="dataset",
            token=hf_token
        )
        
        with open(local_file_path, "r", encoding="utf-8") as f:
            return json.load(f)
            
    except Exception as e:
        st.warning(f"Nie udało się pobrać danych z Hugging Face ({e}). Wczytano bazę awaryjną.")
        return get_fallback_data()

def get_fallback_data():
    """Zwraca awaryjną bazę danych w przypadku błędu pobierania."""
    return {
        "words": [
            {"id": 1, "category": "Rodzina", "type": "noun", "german_article": "die", "german_singular": "Mutter",
             "german_plural": "die Mütter", "polish_singular": "mama", "polish_plural": "mamy"},
            {"id": 2, "category": "Kolory", "type": "phrase", "german": "rot", "polish": "czerwony"}
        ]
    }

# Wywołanie funkcji i przypisanie danych
data = load_data()
all_words = data.get("words", [])

# Wyciąganie unikalnych kategorii z bazy danych
available_categories = sorted(list(set(w.get("category", "Inne") for w in all_words)))


# 2. Funkcja resetująca stan przy zmianie słowa lub filtrów
def reset_word_state():
    st.session_state.is_flipped = False
    st.session_state.answer_checked = False
    st.session_state.user_correct = False

    # Czyszczenie pól tekstowych
    if "noun_input" in st.session_state:
        st.session_state.noun_input = ""
    if "phrase_input" in st.session_state:
        st.session_state.phrase_input = ""


# Funkcja losująca słowo z przefiltrowanej puli
def draw_next_word(filtered_pool):
    if filtered_pool:
        st.session_state.current_word = random.choice(filtered_pool)
    else:
        st.session_state.current_word = None
    reset_word_state()


# 3. MENU BOCZNE 
with st.sidebar:
    st.header("🇩🇪 Menu główne")

    # Wybór trybu (Dodany tryb Wstępu teoretycznego)
    mode = st.radio(
        "Wybierz tryb pracy:",
        ["💡 Wstęp (Zasady gry)", "🎴 Nauka (Fiszki)", "🔢 Rozgrzewka (ABCD)", "📝 Sprawdzian (Pisanie)"],
        on_change=reset_word_state
    )

    st.markdown("---")
    st.subheader("⚙️ Filtrowanie bazy")

    # Wybór Tematu / Kategorii
    selected_cat = st.selectbox(
        "Wybierz temat słówek:",
        ["Wszystkie"] + available_categories,
        on_change=reset_word_state
    )

    # Wybór Typu (Rzeczownik / Zdanie)
    type_filter = st.radio(
        "Co chcesz ćwiczyć?",
        ["Wszystko", "Rzeczowniki (noun)", "Zwroty i zdania (phrase)"],
        on_change=reset_word_state
    )

# 4. Zaawansowana logika filtrowania bazy danych (Kategoria + Typ)
words_pool = all_words

if selected_cat != "Wszystkie":
    words_pool = [w for w in words_pool if w.get("category", "Inne") == selected_cat]

if type_filter == "Rzeczowniki (noun)":
    words_pool = [w for w in words_pool if w["type"] == "noun"]
elif type_filter == "Zwroty i zdania (phrase)":
    words_pool = [w for w in words_pool if w["type"] == "phrase"]

with st.sidebar:
    st.caption(f"Słówek w tej konfiguracji: **{len(words_pool)}**")

if "current_word" not in st.session_state or st.session_state.current_word not in words_pool:
    draw_next_word(words_pool)

current_item = st.session_state.current_word
colors = {"der": "blue", "die": "red", "das": "green"}

# 5. GŁÓWNY INTERFEJS
st.title("🇩🇪 Niemiecki Klasa 7: Trener Słówek")
st.subheader(f"Tryb: {mode}")
st.markdown("---")


# WSTĘP TEORETYCZNY

if mode == "💡 Wstęp (Zasady gry)":
    st.markdown("### 🎯 Zanim zaczniesz: Dwie złote zasady niemieckiego")

    with st.expander("🔑 1. O co chodzi z tymi rodzajnikami (der, die, das)?", expanded=True):
        st.write("""
        W języku niemieckim każdy rzeczownik ma swój rodzajnik. Najważniejsze jest to, że **rodzaj gramatyczny w niemieckim rzadko pokrywa się z polskim!**
        * Dziewczyna to po polsku rodzaj żeński, ale po niemiecku to **das Mädchen** (rodzaj nijaki).
        * Krzesło to po polsku rodzaj nijaki, ale po niemiecku to **der Stuhl** (rodzaj męski).

        **W tej aplikacji kolory pomogą Ci je zapamiętać:**
        """)
        st.markdown("- :blue[**DER**] – rodzaj męski (np. *der Vater* – tata)")
        st.markdown("- :red[**DIE**] – rodzaj żeński (np. *die Mutter* – mama)")
        st.markdown("- :green[**DAS**] – rodzaj nijaki (np. *das Kind* – dziecko)")
        st.info(
            "💡 **Złota rada:** Nigdy nie ucz się samego słówka! Zawsze ucz się go w pakiecie z rodzajnikiem (np. nie 'pies = Hund', tylko 'pies = der Hund').")

    with st.expander("🗣️ 2. Jak to się czyta? Szybka ściągawka", expanded=False):
        st.write("Niemiecka wymowa jest bardzo regularna. Zapamiętaj te zbitki literowe, a przeczytasz większość słów:")

        col_v1, col_v2 = st.columns(2)
        with col_v1:
            st.markdown("**Samogłoski i połączenia:**")
            st.markdown("- **ei** czytamy jak **aj** (np. *mein* -> majn)")
            st.markdown("- **ie** czytamy jak długie **i** (np. *nie* -> nii)")
            st.markdown("- **eu** czytamy jak **oj** (np. *neu* -> noj)")
            st.markdown("- **ä** czytamy jak **e** lub **ae**")
        with col_v2:
            st.markdown("**Spółgłoski:**")
            st.markdown("- **sch** czytamy jak **sz** (np. *Schule* -> szule)")
            st.markdown("- **st / sp** na początku słowa to **szt / szp**")
            st.markdown("- **v** czytamy zazwyczaj jak **f** (np. *vater* -> fater)")
            st.markdown("- **ß** czytamy jak zwykłe **s**")

    st.success(
        "💪 Gotowy? Przełącz tryb w menu bocznym na **Nauka (Fiszki)** lub **Sprawdzian (Quiz)** i zaczniesz działać!")

elif not current_item:
    st.warning("⚠️ Brak słówek spełniających wybrane kryteria w menu bocznym!")

else:
    
    # FISZKI
    
    if mode == "🎴 Nauka (Fiszki)":
        st.markdown(f"### Temat: **{current_item.get('category', 'Brak kategorii')}** | Zastanów się nad tłumaczeniem:")

        with st.container(border=True):
            st.write("")
            if not st.session_state.get("is_flipped", False):
                st.caption("🇵🇱 PO POLSKU")
                if current_item["type"] == "noun":
                    st.subheader(f"{current_item['polish_singular']}")
                    if current_item.get("polish_plural"):
                        st.text(f"Liczba mnoga: {current_item['polish_plural']}")
                else:
                    st.subheader(f"{current_item['polish']}")
            else:
                if current_item["type"] == "noun":
                    st.caption(f"🇵🇱 PO POLSKU: **{current_item['polish_singular']}**")
                    st.markdown("---")
                    st.caption("🇩🇪 PO NIEMIECKU")
                    art = current_item["german_article"].lower()
                    color = colors.get(art, "gray")
                    st.markdown(f"## :{color}[**{art.upper()}**] {current_item['german_singular']}")
                    if current_item.get("german_plural"):
                        st.markdown(f"Liczba mnoga: *{current_item['german_plural']}*")
                else:
                    st.caption(f"🇵🇱 PO POLSKU: **{current_item['polish']}**")
                    st.markdown("---")
                    st.caption("🇩🇪 PO NIEMIECKU")
                    st.markdown(f"## {current_item['german']}")

                hint = current_item.get("hint") or current_item.get("context_tip")
                if hint:
                    st.write("")
                    st.info(f"💡 Wskazówka: {hint}")
            st.write("")

        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Obróć fiszkę 🔄", use_container_width=True, type="primary"):
                st.session_state.is_flipped = not st.session_state.is_flipped
                st.rerun()
        with col2:
            if st.button("Następne słówko ➡️", use_container_width=True, key="btn_next_flashcard"):
                st.session_state.is_flipped = False  # Reset obrotu przed losowaniem
                draw_next_word(words_pool)
                st.rerun()

    
    # ROZGRZEWKA ABCD
   
    elif mode == "🔢 Rozgrzewka (ABCD)":
        st.markdown(f"### Temat: **{current_item['category']}** | Wybierz poprawne tłumaczenie:")
        if current_item["type"] == "noun":
            st.info(f"**{current_item['polish_singular']}** (l.mn. {current_item['polish_plural'] or 'brak'})")
            correct_ans = f"{current_item['german_article'].upper()} {current_item['german_singular']}"
        else:
            st.info(f"**{current_item['polish']}**")
            correct_ans = current_item["german"]

        current_word_key = current_item['polish_singular'] if current_item['type'] == 'noun' else current_item['polish']

        if "abcd_options" not in st.session_state or st.session_state.get("last_word_key") != current_word_key:
            if current_item["type"] == "noun":
                wrong_pool = [f"{w['german_article'].upper()} {w['german_singular']}" for w in words_pool if
                              w['type'] == 'noun' and w.get('german_singular') != current_item.get('german_singular')]
            else:
                wrong_pool = [w['german'] for w in words_pool if
                              w['type'] != 'noun' and w.get('german') != current_item.get('german')]

            import random

            wrong_answers = random.sample(wrong_pool, min(3, len(wrong_pool))) if wrong_pool else []
            options = wrong_answers + [correct_ans]
            random.shuffle(options)

            st.session_state.abcd_options = options
            st.session_state.last_word_key = current_word_key

        user_choice = st.radio(
            "Wybierz właściwą odpowiedź:",
            options=st.session_state.abcd_options,
            key="abcd_hint_radio"
        )

        st.markdown("---")
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("Sprawdź odpowiedź 🏁", key="btn_check_abcd", use_container_width=True, type="primary"):
                if user_choice == correct_ans:
                    st.success("🎉 Doskonale! To jest prawidłowa odpowiedź.")
                else:
                    st.error(f"❌ Pomyłka. Prawidłowa odpowiedź to: **{correct_ans}**")

        with col_btn2:
            if st.button("Następne słówko ➡️", key="btn_next_abcd", use_container_width=True):
                draw_next_word(words_pool)
                st.rerun()
        
        # SPRAWDZIAN (PISANIE)
        
    elif mode == "📝 Sprawdzian (Pisanie)":
        st.markdown(f"### Temat: **{current_item['category']}** | Jak jest po niemiecku:")
        if current_item["type"] == "noun":
            st.info(f"**{current_item['polish_singular']}** (l.mn. {current_item['polish_plural'] or 'brak'})")
        else:
            st.info(f"**{current_item['polish']}**")

        # Inicjalizacja stanów sprawdzania, jeśli nie istnieją
        if "answer_checked" not in st.session_state:
            st.session_state.answer_checked = False
        if "user_correct" not in st.session_state:
            st.session_state.user_correct = False

        # SEKCJA DLA RZECZOWNIKÓW 
        if current_item["type"] == "noun":
            article_options = ["Wybierz...", "DER", "DIE", "DAS"]
            selected_art_upper = st.radio(
                "Wybierz rodzajnik:",
                options=article_options,
                horizontal=True,
                disabled=st.session_state.answer_checked
            )

            # Inicjalizacja bezpiecznego stanu pomocniczego
            if "_noun_text" not in st.session_state:
                st.session_state._noun_text = ""

            user_word = st.text_input(
                "Wpisz słówko (z wielkiej litery, bez rodzajnika):",
                value=st.session_state._noun_text,
                disabled=st.session_state.answer_checked
            )
            st.session_state._noun_text = user_word

            # Niemieckie litery
            if not st.session_state.answer_checked:
                st.caption("Kliknij literę, aby dodać do pola tekstowego:")
                cols = st.columns(8)
                german_chars = ['ä', 'ö', 'ü', 'ß', 'Ä', 'Ö', 'Ü']
                for idx, char in enumerate(german_chars):
                    with cols[idx]:
                        if st.button(char, key=f"char_{char}"):
                            st.session_state._noun_text += char
                            st.rerun()

            if not st.session_state.answer_checked:
                if st.button("Sprawdź", type="primary", use_container_width=True):
                    if selected_art_upper == "Wybierz...":
                        st.warning("⚠️ Musisz najpierw wybrać rodzajnik!")
                    elif not user_word.strip():
                        st.warning("⚠️ Wpisz słówko!")
                    else:
                        st.session_state.answer_checked = True
                        correct_art = current_item["german_article"].lower()
                        correct_word = current_item["german_singular"].strip()

                        if selected_art_upper.lower() == correct_art and user_word.strip() == correct_word:
                            st.session_state.user_correct = True
                        else:
                            st.session_state.user_correct = False
                        st.rerun()

        # SEKCJA DLA ZWROTÓW I ZDAŃ
        else:
            if "_phrase_text" not in st.session_state:
                st.session_state._phrase_text = ""

            user_phrase = st.text_input(
                "Wpisz całe zdanie/zwrot:",
                value=st.session_state._phrase_text,
                disabled=st.session_state.answer_checked
            )
            st.session_state._phrase_text = user_phrase

            # Niemieckie litery dla zdań
            if not st.session_state.answer_checked:
                st.caption("Kliknij literę, aby dodać do pola tekstowego:")
                cols = st.columns(8)
                german_chars = ['ä', 'ö', 'ü', 'ß', 'Ä', 'Ö', 'Ü']
                for idx, char in enumerate(german_chars):
                    with cols[idx]:
                        if st.button(char, key=f"char_phrase_{char}"):
                            st.session_state._phrase_text += char
                            st.rerun()

            if not st.session_state.answer_checked:
                if st.button("Sprawdź", type="primary", use_container_width=True):
                    if not user_phrase.strip():
                        st.warning("⚠️ Wpisz zwrot!")
                    else:
                        st.session_state.answer_checked = True
                        correct_phrase = current_item["german"].strip()

                        if user_phrase.strip().lower() == correct_phrase.lower():
                            st.session_state.user_correct = True
                        else:
                            st.session_state.user_correct = False
                        st.rerun()

        # BLOK WYŚWIETLANIA WYNIKÓW
        if st.session_state.answer_checked:
            if st.session_state.user_correct:
                st.success("🎉 Doskonale! Dobra odpowiedź.")
            else:
                st.error("❌ Niestety, to nie tak.")
                if current_item["type"] == "noun":
                    art_upper = current_item["german_article"].upper()
                    st.info(f"Poprawna odpowiedź to: **{art_upper} {current_item['german_singular']}**")
                else:
                    st.info(f"Poprawna odpowiedź to: **{current_item['german']}**")

            # Przycisk "Następne" pojawia się dopiero po sprawdzeniu odpowiedzi, żeby użytkownik widział wynik
            if st.button("Następne słówko ➡️", use_container_width=True):
                st.session_state.answer_checked = False
                st.session_state.user_correct = False
                if "_noun_text" in st.session_state:
                    st.session_state._noun_text = ""
                if "_phrase_text" in st.session_state:
                    st.session_state._phrase_text = ""
                draw_next_word(words_pool)
                st.rerun()
