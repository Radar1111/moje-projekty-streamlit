import streamlit as st
import random
import json

# Konfiguracja wyglądu strony
st.set_page_config(page_title="Znaki Drogowe: Nauka i Quiz", page_icon="🚗", layout="centered")


# Funkcja wczytująca bazę danych z zewnętrznego pliku JSON
def load_questions_from_json():
    try:
        with open("questions.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            # Zapewnienie, że każde pytanie ma przypisaną kategorię (nawet jeśli jej brakuje w JSON)
            for item in data:
                if "category" not in item or not item["category"]:
                    item["category"] = "Inne"
            return data
    except FileNotFoundError:
        # Awaryjna pusta baza, gdyby plik nie istniał
        return []


# Wczytanie pytań z pliku do zmiennej
ALL_QUIZ_DATA = load_questions_from_json()

# Wyciągnięcie unikalnych kategorii z bazy danych
DOSTEPNE_KATEGORIE = sorted(list(set(item["category"] for item in ALL_QUIZ_DATA)))

# Menu boczne do wyboru trybu
st.sidebar.title("🚦 Nawigacja")
mode = st.sidebar.radio("Wybierz tryb pracy:", ["Nauka 📖", "Quiz 🎮"])

# --- TRYB NAUKI ---
if mode == "Nauka 📖":
    st.title("📖 Panel Nauki Znaków Drogowych")
    st.write("Wybierz kategorię, aby filtrować znaki i uczyć się partiami.")
    st.divider()

    # Filtrowanie po kategoriach w panelu nauki
    wybrana_kat_nauka = st.selectbox(
        "Filtr kategorii:",
        ["Wszystkie"] + DOSTEPNE_KATEGORIE
    )

    # Filtrowanie danych do wyświetlenia
    if wybrana_kat_nauka == "Wszystkie":
        wyswietlane_znaki = ALL_QUIZ_DATA
    else:
        wyswietlane_znaki = [item for item in ALL_QUIZ_DATA if item["category"] == wybrana_kat_nauka]

    # Wyświetlanie przefiltrowanych znaków
    if not wyswietlane_znaki:
        st.info("Brak znaków w tej kategorii.")
    else:
        for index, item in enumerate(wyswietlane_znaki):
            col1, col2 = st.columns([1, 3])

            with col1:
                st.image(item["image"], width=120)

            with col2:
                st.subheader(f"{item['answer']}")
                st.caption(f"Kategoria: {item['category'].capitalize()}")
                st.write(f"**Pytanie w quizie:** {item['question']}")



            st.divider()

# --- TRYB QUIZU ---
else:
    st.title("🚦 Quiz ze Znajomości Znaków Drogowych")

    # Krok 0: Konfiguracja quizu przed startem
    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False

    if not st.session_state.quiz_started:
        st.subheader("⚙️ Konfiguracja Twojego Quizu")

        # 1. Wybór kategorii do quizu
        wybrana_kat_quiz = st.selectbox(
            "Z jakich znaków chcesz rozwiązać quiz?",
            ["Wszystkie kategorie"] + DOSTEPNE_KATEGORIE
        )

        # Filtrowanie puli pytań pod konfigurację
        if wybrana_kat_quiz == "Wszystkie kategorie":
            pula_pytan = ALL_QUIZ_DATA
        else:
            pula_pytan = [item for item in ALL_QUIZ_DATA if item["category"] == wybrana_kat_quiz]

        # 2. Wybór liczby pytań
        maks_pytan = max(1, len(pula_pytan))
        domyslna_liczba = min(5, maks_pytan)
        liczba_pytan = st.number_input(
            f"Ile pytań wylosować? (Maksymalnie dostępnych: {maks_pytan})",
            min_value=1,
            max_value=maks_pytan,
            value=domyslna_liczba
        )

        # Przycisk startu quizu
        if st.button("Rozpocznij Quiz 🚀", use_container_width=True):
            if pula_pytan:
                st.session_state.shuffled_questions = random.sample(pula_pytan, liczba_pytan)
                st.session_state.current_step = 0
                st.session_state.score = 0
                st.session_state.answered = False
                st.session_state.quiz_started = True
                st.rerun()
            else:
                st.error("Wybrana pula pytań jest pusta!")

    # Krok 2: Aktywna rozgrywka (uruchamia się po kliknięciu startu)
    else:
        active_quiz_data = st.session_state.shuffled_questions

        # Sprawdzenie czy quiz dobiegł końca
        if st.session_state.current_step < len(active_quiz_data):
            current_q = active_quiz_data[st.session_state.current_step]

            # Wyświetlanie postępu i punktacji
            st.subheader(f"Pytanie {st.session_state.current_step + 1} z {len(active_quiz_data)}")
            st.metric(label="Twój aktualny wynik", value=f"{st.session_state.score} pkt")
            st.caption(f"Kategoria pytania: {current_q['category'].capitalize()}")

            # Grafika znaku drogowego pobierana z URL
            st.image(current_q["image"], width=200)
            st.write(f"### {current_q['question']}")

            # Wyświetlenie opcji wyboru w formie formularza
            with st.form(key=f"question_form_{st.session_state.current_step}"):
                user_choice = st.radio("Wybierz jedną odpowiedź:", current_q["options"], index=None,
                                       label_visibility="collapsed")
                submit_btn = st.form_submit_button(label="Sprawdź odpowiedź ➡️")

                if submit_btn:
                    if user_choice is None:
                        st.warning("Musisz zaznaczyć jedną z odpowiedzi!")
                    else:
                        st.session_state.answered = True
                        if user_choice == current_q["answer"]:
                            st.success("Brawo! To prawidłowa odpowiedź! 🎉")
                            st.session_state.score += 1
                        else:
                            st.error(f"Niestety to błąd. Prawidłowa odpowiedź to: **{current_q['answer']}**")

            # Przycisk przejścia dalej (pojawia się tylko po udzieleniu odpowiedzi)
            if st.session_state.answered:
                if st.button("Następne pytanie ➡️"):
                    st.session_state.current_step += 1
                    st.session_state.answered = False
                    st.rerun()

        else:
            # Ekran końcowy gry
            st.balloons()
            st.success("## 🎉 Gratulacje! Quiz ukończony!")
            st.markdown(f"### Twój ostateczny wynik to: **{st.session_state.score} / {len(active_quiz_data)}**")

            # Ocena opisowa
            procent = (st.session_state.score / len(active_quiz_data)) * 100
            if procent == 100:
                st.write("Mistrz kierownicy! Znasz wszystkie wylosowane znaki idealnie! 🏆")
            elif procent >= 60:
                st.write("Dobra robota! Jesteś gotowy na wycieczkę rowerową! 🚲")
            else:
                st.write("Warto jeszcze trochę potrenować. 📖")

            # Przycisk powrotu do menu konfiguracji
            if st.button("Zagraj jeszcze raz (Zmień ustawienia) 🔄", use_container_width=True):
                st.session_state.quiz_started = False
                if "shuffled_questions" in st.session_state:
                    del st.session_state.shuffled_questions
                st.session_state.current_step = 0
                st.session_state.score = 0
                st.session_state.answered = False
                st.rerun()

st.divider()
st.caption("Najcierpliwszy portal do nauki znaków drogowych - klasa 4")
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")
