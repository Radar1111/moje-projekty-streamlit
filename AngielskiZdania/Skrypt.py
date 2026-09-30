import streamlit as st
import json
import os
import random
from huggingface_hub import hf_hub_download  # <-- Dodaj ten import

# Konfiguracja strony
st.set_page_config(
    page_title="Trener Gramatyki",
    page_icon="🎯",
    layout="centered"
)

# Inicjalizacja stanu aplikacji (State Management)
if "current_question_idx" not in st.session_state:
    st.session_state.current_question_idx = 0
if "user_scramble_order" not in st.session_state:
    st.session_state.user_scramble_order = []
if "shuffled_words" not in st.session_state:
    st.session_state.shuffled_words = []

if "score" not in st.session_state:
    st.session_state.score = 0
if "answered_questions" not in st.session_state:
    st.session_state.answered_questions = set()

# Funkcja resetująca stan przy zmianie pytania lub trybu
def reset_question_state(shuffled_list=None):
    st.session_state.user_scramble_order = []
    if shuffled_list is not None:
        st.session_state.shuffled_words = shuffled_list
    else:
        st.session_state.shuffled_words = []

# Ładowanie bazy pytań z prywatnego repozytorium przy użyciu oficjalnej biblioteki
@st.cache_data
def load_quiz_data():
    repo_id = "Radar1111/AngielskiZdani"
    filename = "quiz_data.json"
    
    # Pobranie tokenu z bezpiecznych zmiennych Streamlit (st.secrets)
    hf_token = st.secrets.get("HF_TOKEN")
    
    if not hf_token:
        st.error("Brak tokenu HF_TOKEN w konfiguracji Streamlit Secrets!")
        return []
        
    try:
        # Oficjalna metoda HF pobierająca pojedynczy plik z prywatnego zbioru danych (dataset)
        local_file_path = hf_hub_download(
            repo_id=repo_id,
            filename=filename,
            repo_type="dataset",  # Informuje HF, że szukamy w Datasets, a nie w Models
            token=hf_token
        )
        
        # Wczytanie pobranego i zabezpieczonego przez bibliotekę pliku JSON
        with open(local_file_path, "r", encoding="utf-8") as f:
            return json.load(f)
            
    except Exception as e:
        st.error(f"Nie udało się pobrać bazy danych z Hugging Face: {e}")
        return []

all_questions = load_quiz_data())

# Interfejs użytkownika
st.title("🎯 Trener Gramatyki przed Egzaminem Ósmoklasisty")
st.markdown("Wybierz tryb ćwiczeń i sprawdź swoją wiedzę w formatach zadań prosto z E8!")


st.sidebar.header("Ustawienia ćwiczeń")

# 1. FORMAT ZADANIA
mode = st.sidebar.selectbox(
    "Wybierz format zadania:",
    ["🔠 Wybór ABCD", "📝 Uzupełnianie luk", "🧩 Rozsypanka wyrazowa"]
)

def reset_on_category_change():
    st.session_state.score = 0
    st.session_state.current_question_idx = 0
    st.session_state.answered_questions = set()
    st.session_state.user_scramble_order = []
    st.session_state.shuffled_words = []
    if "shuffled_words_id" in st.session_state:
        st.session_state.shuffled_words_id = None

# 2. DYNAMICZNY FILTR KATEGORII (TENSE)
st.sidebar.subheader("Zakres materiału")
if all_questions:

    unique_tenses = sorted(list(set([q["tense"] for q in all_questions])))

    category_options = ["🌍 Wszystkie kategorie"] + unique_tenses


    selected_category = st.sidebar.selectbox(
        "Wybierz czas gramatyczny:",
        category_options,
        key="tense_filter",
        on_change=reset_on_category_change
    )


    if selected_category == "🌍 Wszystkie kategorie":
        questions = all_questions
    else:
        questions = [q for q in all_questions if q["tense"] == selected_category]
else:
    questions = []


if st.session_state.current_question_idx >= len(questions) and len(questions) > 0:
    st.session_state.current_question_idx = 0
    reset_question_state()


st.sidebar.divider()
st.sidebar.subheader("📈 Twój Wynik")
total_q = len(questions)

if total_q > 0:
    st.sidebar.metric(label="Zdobyte punkty", value=f"{st.session_state.score} / {total_q}")
    pct = (st.session_state.score / total_q) * 100
    st.sidebar.progress(min(pct / 100, 1.0))
    st.sidebar.caption(f"Skuteczność: **{pct:.0f}%**")

if st.sidebar.button("🔄 Resetuj cały quiz i punkty"):
    st.session_state.current_question_idx = 0
    st.session_state.score = 0
    st.session_state.answered_questions = set()
    reset_question_state()
    st.rerun()

# Sprawdzenie czy baza nie jest pusta
if questions:
    q_idx = st.session_state.current_question_idx
    current_q = questions[q_idx]
    q_id = current_q["id"]

    # Pasek postępu nad zadaniem
    st.caption(f"Zadanie {q_idx + 1} z {total_q} | Kategoria: **{current_q['tense']}**")
    st.progress((q_idx + 1) / total_q)

    # Informacja, czy zadanie zostało już zaliczone
    is_answered = q_id in st.session_state.answered_questions
    if is_answered:
        st.warning("⚠️ Udzieliłeś już odpowiedzi na to zadanie. Punkty zostały zablokowane.")

    # Wyświetlenie podpowiedzi w rozwijanym pasku
    with st.expander("💡 Zobacz wskazówkę do zadania"):
        st.write(current_q["hint"])

    st.divider()

    # UZUPEŁNIANIE LUK
    if mode == "📝 Uzupełnianie luk":
        st.subheader("Uzupełnij lukę w zdaniu")
        st.markdown(f"### `{current_q['gap_fill']['question']}`")

        user_ans = st.text_input("Wpisz brakujące słowa:", key=f"gap_{q_idx}", disabled=is_answered).strip()

        if st.button("Sprawdź odpowiedź", key="btn_gap", disabled=is_answered):
            correct = current_q["gap_fill"]["correct_answer"]
            st.session_state.answered_questions.add(q_id)

            if user_ans.lower() == correct.lower():
                st.success("🎉 Doskonale! To poprawna odpowiedź. (+1 pkt)")
                st.session_state.score += 1
            else:
                st.error(f"❌ Niestety to błąd. Twoja odpowiedź: '{user_ans}'")
                st.info(f"👉 Poprawna forma to: **{correct}**")
            st.markdown(f"**Wyjaśnienie:** {current_q['explanation']}")
            st.rerun()

        if is_answered:
            st.markdown(f"**Poprawna odpowiedź:** {current_q['gap_fill']['correct_answer']}")
            st.markdown(f"**Wyjaśnienie:** {current_q['explanation']}")

    #  ABCD
    elif mode == "🔠 Wybór ABCD":
        st.subheader("Wybierz poprawną odpowiedź")
        st.markdown(f"### `{current_q['abcd']['question']}`")

        opts = current_q["abcd"]["options"]
        display_opts = [f"{k}: {v}" for k, v in opts.items()]

        user_choice = st.radio("Dostępne opcje:", display_opts, key=f"abcd_{q_idx}", disabled=is_answered)

        if st.button("Sprawdź odpowiedź", key="btn_abcd", disabled=is_answered):
            chosen_key = user_choice.split(":")[0].strip()
            correct_key = current_q["abcd"]["correct_option"]
            st.session_state.answered_questions.add(q_id)

            if chosen_key == correct_key:
                st.success(f"🎉 Brawo! Odpowiedź {correct_key} jest prawidłowa. (+1 pkt)")
                st.session_state.score += 1
            else:
                st.error(f"❌ Błąd. Wybrałeś opcję {chosen_key}.")
                st.info(f"👉 Poprawna odpowiedź to: **{correct_key} ({opts[correct_key]})**")
            st.markdown(f"**Wyjaśnienie:** {current_q['explanation']}")
            st.rerun()

        if is_answered:
            correct_key = current_q["abcd"]["correct_option"]
            st.markdown(f"**Poprawna odpowiedź:** {correct_key} ({opts[correct_key]})")
            st.markdown(f"**Wyjaśnienie:** {current_q['explanation']}")

            # ROZSYPANKA WYRAZOWA
    elif mode == "🧩 Rozsypanka wyrazowa":
            st.subheader("Ułóż zdanie w poprawnej kolejności")
            st.write(current_q["word_scramble"]["question"])

            #
            base_words = current_q["word_scramble"].get("words", [])

            # Jeśli w bazie nie ma słów, wyświetli ostrzeżenie
            if not base_words:
                st.error("Błąd danych: Słownik pytań nie zawiera listy słów ('words') dla tego pytania.")
            else:
                state_key = f"scramble_words_{q_idx}_{selected_category}"


                if (st.session_state.get("shuffled_words_id") != state_key) or (
                        "shuffled_words" not in st.session_state) or (not st.session_state.shuffled_words):
                    shuffled = base_words.copy()

                    attempts = 0
                    while shuffled == base_words and len(shuffled) > 1 and attempts < 10:
                        random.shuffle(shuffled)
                        attempts += 1

                    st.session_state.shuffled_words = shuffled
                    st.session_state.shuffled_words_id = state_key
                    st.session_state.user_scramble_order = []

                st.write("Dostępne słowa (klikaj, aby ułożyć zdanie):")


                available_words = [word for word in st.session_state.shuffled_words if
                                   word not in st.session_state.user_scramble_order]

                if available_words:
                    cols = st.columns(len(available_words))
                    for i, word in enumerate(available_words):
                        if cols[i].button(word, key=f"word_{word}_{i}_{q_idx}", disabled=is_answered):
                            st.session_state.user_scramble_order.append(word)
                            st.rerun()
                else:
                    st.caption("_Wszystkie słowa zostały wybrane._")

                st.markdown("### Twoje zdanie:")
                current_sentence = " ".join(st.session_state.user_scramble_order)
                st.info(
                    current_sentence if current_sentence else "_Kliknij słowa powyżej, aby zacząć układać zdanie..._")

                if st.button("🔄 Resetuj ułożenie", disabled=is_answered):
                    st.session_state.user_scramble_order = []
                    st.rerun()

                if st.button("Sprawdź ułożenie", key="btn_scramble", disabled=is_answered):
                    target_sentence = current_q["base_sentence"].replace(".", "").strip().lower()
                    user_sentence_clean = current_sentence.replace(".", "").strip().lower()
                    st.session_state.answered_questions.add(q_id)

                    if user_sentence_clean == target_sentence:
                        st.success("🎉 Świetnie! Zdanie zostało ułożone idealnie gramatycznie. (+1 pkt)")
                        st.session_state.score += 1
                    else:
                        st.error("❌ Słowa są w niepoprawnej kolejności.")
                        st.info(f"👉 Prawidłowe zdanie to: **{current_q['base_sentence']}**")
                    st.markdown(f"**Wyjaśnienie:** {current_q['explanation']}")
                    st.rerun()

                if is_answered:
                    st.markdown(f"**Prawidłowe zdanie:** {current_q['base_sentence']}")
                    st.markdown(f"**Wyjaśnienie:** {current_q['explanation']}")

    # NAWIGACJA MIĘDZY PYTANIAMI 
    st.divider()
    col_prev, col_next = st.columns(2)

    with col_prev:
        if st.button("⬅️ Poprzednie zadanie", use_container_width=True) and q_idx > 0:
            st.session_state.current_question_idx -= 1
            reset_question_state()
            st.rerun()

    with col_next:
        if st.button("Następne zadanie ➡️", use_container_width=True) and q_idx < total_q - 1:
            st.session_state.current_question_idx += 1
            reset_question_state()
            st.rerun()
else:
    st.info("Brak pytań w tej kategorii lub baza danych jest pusta.")
