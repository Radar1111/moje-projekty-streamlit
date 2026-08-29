import json
import os
import random
import streamlit as st
from huggingface_hub import hf_hub_download

# Konfiguracja strony
st.set_page_config(
    page_title="E8 - Trener Ósmoklasisty", page_icon="🧠", layout="centered"
)


# 1. Wczytywanie bazy danych z pliku JSON (Bezpieczne cache'owanie)
@st.cache_data
def load_app_data(token):
    """Wczytuje kompletną bazę zadań z prywatnego repozytorium Hugging Face."""
    REPO_ID = "Radar1111/TrenerE8" 
    FILENAME = "zadania.json"
    
    # Bezpieczne pobranie pliku z Hugging Face 
    local_file_path = hf_hub_download(
        repo_id=REPO_ID, 
        filename=FILENAME, 
        token=token,
        repo_type="dataset" # Upewnij się, że to typ "Dataset" na HF
    )
    
    # Wczytanie pobranego pliku JSON
    with open(local_file_path, "r", encoding="utf-8") as f:
        return json.load(f)


# WYWOŁANIE FUNKCJI
tasks = []

if "HF_TOKEN" not in st.secrets:
    st.error("Błąd krytyczny: Brak klucza `HF_TOKEN` w zakładce Secrets Streamlita!")
    st.stop()
else:
    try:
        # Przekazujemy token do funkcji, aby poprawnie zarządzać cachem
        tasks = load_app_data(st.secrets["HF_TOKEN"])
    except Exception as e:
        st.error(f"Nie udało się pobrać bazy zadań z Hugging Face. Szczegóły błędu: {e}")
        st.stop()

# Interfejs użytkownika
st.title("Egzamin Ósmoklasisty - Trener Matematyki")
st.write("Wybierz dział oraz poziom trudności i zacznij interaktywny trening")

# --- SPRAWDZENIE CZY BAZA JEST PUSTA ---
if not tasks:
    st.error("Nie znaleziono pliku `zadania.json` lub plik jest pusty. Dodaj zadania, aby uruchomić aplikację.")
    st.stop()

# Pasek boczny
st.sidebar.header("⚙ Filtruj zadania")

# Dynamiczne wyciąganie unikalnych zadań (z sortowaniem alfabetycznym)
lista_dzialow = sorted(list(set(task["dzial"] for task in tasks)))
wybrany_dzial = st.sidebar.selectbox("Wybierz dział:", lista_dzialow)

lista_poziomow = sorted(list(set(task["poziom"] for task in tasks)))
wybrany_poziom = st.sidebar.selectbox("Poziom trudności:", lista_poziomow)

opcje_liczby = ["5", "10", "20", "Wszystkie"]
wybrana_liczba = st.sidebar.selectbox("Liczba zadań w serii:", opcje_liczby)

# --- INICJALIZACJA STANU SESJI ---
if "current_tasks_index" not in st.session_state:
    st.session_state.current_tasks_index = 0

if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False

if "score" not in st.session_state:
    st.session_state.score = 0

if "quiz_finished" not in st.session_state:
    st.session_state.quiz_finished = False

if "ostatni_wybor" not in st.session_state:
    st.session_state.ostatni_wybor = None


# Funkcja resetująca stan
def reset_quiz():
    st.session_state.current_tasks_index = 0
    st.session_state.form_submitted = False
    st.session_state.score = 0
    st.session_state.quiz_finished = False
    st.session_state.ostatni_wybor = None


# --- FILTROWANIE I LOSOWANIE ZADAŃ ---
przefiltrowane_zadania = []
if wybrany_dzial and wybrany_poziom:
    wszystkie_pasujace = [
        t
        for t in tasks
        if t["dzial"] == wybrany_dzial and t["poziom"] == wybrany_poziom
    ]

    if wybrana_liczba == "Wszystkie":
        limit = len(wszystkie_pasujace)
    else:
        limit = min(int(wybrana_liczba), len(wszystkie_pasujace))

    klucz_puli = f"pula_{wybrany_dzial}_{wybrany_poziom}_{wybrana_liczba}_v1"

    if "aktualny_klucz" not in st.session_state:
        st.session_state.aktualny_klucz = klucz_puli

    if st.session_state.aktualny_klucz != klucz_puli:
        st.session_state.aktualny_klucz = klucz_puli
        if klucz_puli in st.session_state:
            del st.session_state[klucz_puli]
        reset_quiz()

    if klucz_puli not in st.session_state and wszystkie_pasujace:
        st.session_state[klucz_puli] = random.sample(wszystkie_pasujace, limit)
        reset_quiz()

    przefiltrowane_zadania = st.session_state.get(klucz_puli, [])

# --- WYŚWIETLANIE INTERFEJSU ---
if not przefiltrowane_zadania:
    st.info("Brak zadań w wybranej konfiguracji.")
else:
    # 1. EKRAN KOŃCOWY (PODSUMOWANIE)
    if st.session_state.quiz_finished:
        st.success("🎉 Gratulacje! Ukończyłeś całą serię zadań!")
        st.metric(
            label="Twój ostateczny wynik",
            value=f"{st.session_state.score} / {len(przefiltrowane_zadania)}",
        )

        procent = int((st.session_state.score / len(przefiltrowane_zadania)) * 100)
        st.write(f"Twój wynik to **{procent}%**.")

        if procent == 100:
            st.balloons()
            st.write("🥇 Perfekcyjnie! Egzamin ósmoklasisty pójdzie Ci śpiewająco!")
        elif procent >= 70:
            st.write("👍 Bardzo ładnie! Masz solidne podstawy.")
        else:
            st.write("💪 Dobra próba! Przeanalizuj błędy i spróbuj jeszcze raz, aby poćwiczyć.")

        if st.button("Rozpocznij nową serię 🔄"):
            del st.session_state[st.session_state.aktualny_klucz]
            reset_quiz()
            st.rerun()

    # 2. EKRAN ROZWIĄZYWANIA ZADAŃ
    else:
        idx = st.session_state.current_tasks_index
        zadanie = przefiltrowane_zadania[idx]

        st.subheader(f"Zadanie {idx + 1} z {len(przefiltrowane_zadania)}")
        st.caption(f"Aktualny wynik: {st.session_state.score} pkt")

        with st.container(border=True):
            st.markdown(f"### {zadanie['tresc']}")

            # Blok formularza
            with st.form(key=f"form_{zadanie['id']}"):
                # Blokujemy możliwość zmiany odpowiedzi po jej zatwierdzeniu
                wybor = st.radio(
                    "Wybierz poprawną odpowiedź:",
                    zadanie["opcje"],
                    index=None if st.session_state.ostatni_wybor is None else zadanie["opcje"].index(
                        st.session_state.ostatni_wybor),
                    disabled=st.session_state.form_submitted
                )

                submit_button = st.form_submit_button(
                    label="Sprawdź odpowiedź 🚀",
                    disabled=st.session_state.form_submitted
                )

                if submit_button:
                    if wybor is None:
                        st.warning("Zaznacz jedną z opcji przed sprawdzeniem!")
                    else:
                        st.session_state.form_submitted = True
                        st.session_state.ostatni_wybor = wybor
                        if wybor == zadanie["poprawna"]:
                            st.session_state.score += 1
                        st.rerun()  # Wymuszamy odświeżenie, aby zablokować radio i pokazać UI poniżej

            # Logika wyświetlania wyniku (poza formularzem, stabilna dzięki st.rerun())
            if st.session_state.form_submitted:
                if st.session_state.ostatni_wybor == zadanie["poprawna"]:
                    st.success("Doskonale! To poprawna odpowiedź!")
                else:
                    st.error(f"❌ Błędna odpowiedź. Prawidłowa to: {zadanie['poprawna']}")

                st.info(f"💡 **Wyjaśnienie:** {zadanie['wyjasnienie']}")

                napis_na_przycisku = (
                    "Zobacz podsumowanie 🏁"
                    if idx + 1 == len(przefiltrowane_zadania)
                    else "Następne zadanie ➡️"
                )

                if st.button(napis_na_przycisku):
                    if idx + 1 < len(przefiltrowane_zadania):
                        st.session_state.current_tasks_index += 1
                        st.session_state.form_submitted = False
                        st.session_state.ostatni_wybor = None
                    else:
                        st.session_state.quiz_finished = True
                    st.rerun()
