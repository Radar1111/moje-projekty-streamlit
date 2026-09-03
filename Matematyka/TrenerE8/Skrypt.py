import json
import os
import random
import streamlit as st
from huggingface_hub import hf_hub_download

# Konfiguracja strony
st.set_page_config(
    page_title="E8 - Trener Ósmoklasisty", page_icon="🧠", layout="centered"
)


# --- 1. BEZPIECZNE WCZYTYWANIE BAZY Z HUGGING FACE (Z AUTOMATYCZNYM RESETEM CACHE) ---
@st.cache_data
def load_app_data(token, wersja_bazy):
    """Wczytuje bazę zadań z Hugging Face. Zmiana parametru wersja_bazy automatycznie czyści cache."""
    REPO_ID = "Radar1111/TrenerE8" 
    FILENAME = "zadania.json"
    
    local_file_path = hf_hub_download(
        repo_id=REPO_ID, 
        filename=FILENAME, 
        token=token,
        repo_type="dataset"
    )
    
    with open(local_file_path, "r", encoding="utf-8") as f:
        return json.load(f)


# Pobranie zadań
tasks = []
if "HF_TOKEN" not in st.secrets:
    st.error("Błąd krytyczny: Brak klucza `HF_TOKEN` w zakładce Secrets Streamlita!")
    st.stop()
else:
    try:
        # 💡 JEŚLI DODASZ NOWE ZADANIA NA HF, ZMIEŃ PONIŻSZĄ WARTOŚĆ (np. na "v2", "v3", itd.), ABY AUTOMATYCZNIE WYCZYŚCIĆ CACHE!
        AKTUALNA_WERSJA_BAZY = "v7" 
        
        tasks = load_app_data(st.secrets["HF_TOKEN"], AKTUALNA_WERSJA_BAZY)
    except Exception as e:
        st.error(f"Nie udało się pobrać bazy zadań z Hugging Face. Szczegóły błędu: {e}")
        st.stop()

# --- 2. INTERFEJS UŻYTKOWNIKA I FILTRY ---
st.title("Egzamin Ósmoklasisty - Trener Matematyki")
st.write("Wybierz dział oraz poziom trudności i zacznij interaktywny trening")

st.sidebar.header("⚙ Filtruj zadania")

# Dynamiczne wyciąganie unikalnych opcji (posortowane alfabetycznie)
lista_dzialow = sorted(list(set(task["dzial"] for task in tasks)))
wybrany_dzial = st.sidebar.selectbox("Wybierz dział:", lista_dzialow)

lista_poziomow = sorted(list(set(task["poziom"] for task in tasks)))
wybrany_poziom = st.sidebar.selectbox("Poziom trudności:", lista_poziomow)

opcje_liczby = ["5", "10", "20", "Wszystkie"]
wybrana_liczba = st.sidebar.selectbox("Liczba zadań w serii:", opcje_liczby)


# --- 3. INICJALIZACJA STANU SESJI ---
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


# Funkcja czyszcząca stan (używana tylko przy twardym resecie lub zmianie filtrów)
def reset_quiz_state():
    st.session_state.current_tasks_index = 0
    st.session_state.form_submitted = False
    st.session_state.score = 0
    st.session_state.quiz_finished = False
    st.session_state.ostatni_wybor = None


# --- 4. LOGIKA GENEROWANIA I ZMIANY PULI ZADAŃ ---
# Tworzymy unikalny klucz dla obecnego wyboru użytkownika
obecny_klucz_puli = f"pula_{wybrany_dzial}_{wybrany_poziom}_{wybrana_liczba}"

# Jeśli użytkownik zmienił filtry w pasku bocznym, czyścimy stary stan
if "zapisany_klucz_puli" not in st.session_state:
    st.session_state.zapisany_klucz_puli = obecny_klucz_puli

if st.session_state.zapisany_klucz_puli != obecny_klucz_puli:
    st.session_state.zapisany_klucz_puli = obecny_klucz_puli
    reset_quiz_state()

# Losujemy zadania TYLKO RAZ dla danej konfiguracji filtrów
if obecny_klucz_puli not in st.session_state:
    wszystkie_pasujace = [
        t for t in tasks
        if t["dzial"] == wybrany_dzial and t["poziom"] == wybrany_poziom
    ]
    
    if wybrana_liczba == "Wszystkie":
        limit = len(wszystkie_pasujace)
    else:
        limit = min(int(wybrana_liczba), len(wszystkie_pasujace))
        
    if wszystkie_pasujace:
        st.session_state[obecny_klucz_puli] = random.sample(wszystkie_pasujace, limit)
    else:
        st.session_state[obecny_klucz_puli] = []

przefiltrowane_zadania = st.session_state[obecny_klucz_puli]


# --- 5. WYŚWIETLANIE INTERFEJSU QUIZU ---
if not przefiltrowane_zadania:
    st.info("Brak zadań w wybranej konfiguracji.")
else:
    # --- 📝 MULTI-BRUDNOPIS W SIDEBARZE (TEKST + RYSOWANIE) ---
    st.sidebar.markdown("---")
    st.sidebar.header("📝 Brudnopis Ucznia")

    # Tworzymy dwie niezależne zakładki w pasku bocznym
    zakladka_rysuj, zakladka_pisz = st.sidebar.tabs(["🎨 Rysuj", "✍️ Pisz"])

    with zakladka_rysuj:
        st.caption("Rysuj myszką lub palcem. Kliknij ikonę kosza pod tablicą, aby wyczyścić.")
        from streamlit_drawable_canvas import st_canvas

        # Rysownica w sidebarze działa stabilnie, bo nie blokuje jej główny formularz
        st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",
            stroke_width=3,
            stroke_color="#000000",
            background_color="#ffffff",
            update_streamlit=False,  # Dla płynności rysowania (w sidebarze już nie zablokuje apki!)
            height=250,
            drawing_mode="freedraw",
            key="globalny_canvas_brudnopis",  # Jeden stały klucz, by rysunek nie znikał przy zmianie pytania
        )

    with zakladka_pisz:
        if "brudnopis_globalny" not in st.session_state:
            st.session_state["brudnopis_globalny"] = ""


        def czysc_notatnik():
            st.session_state["brudnopis_globalny"] = ""


        st.text_area(
            label="Miejsce na Twoje obliczenia:",
            placeholder="Np. wspólny mianownik to 12...",
            key="brudnopis_globalny",
            height=180
        )
        st.button("Wyczyść notatnik 🧹", on_click=czysc_notatnik)

    # A. EKRAN PODSUMOWANIA (KONIEC SERII)
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
            # Usuwamy zapisaną pulę, żeby przy resecie wylosować nowe pytania z tego samego działu
            if obecny_klucz_puli in st.session_state:
                del st.session_state[obecny_klucz_puli]
            reset_quiz_state()
            st.rerun()

    # B. EKRAN ROZWIĄZYWANIA ZADAŃ
    else:
        idx = st.session_state.current_tasks_index
        zadanie = przefiltrowane_zadania[idx]

        st.subheader(f"Zadanie {idx + 1} z {len(przefiltrowane_zadania)}")
        st.caption(f"Aktualny wynik: {st.session_state.score} pkt")

        with st.container(border=True):
            st.markdown(f"### {zadanie['tresc']}")

            # Formularz odpowiedzi
            with st.form(key=f"form_{zadanie['id']}_{idx}"):
                # Blokujemy zaznaczanie innych opcji po sprawdzeniu
                domyslny_indeks = None
                if st.session_state.ostatni_wybor in zadanie["opcje"]:
                    domyslny_indeks = zadanie["opcje"].index(st.session_state.ostatni_wybor)

                wybor = st.radio(
                    "Wybierz poprawną odpowiedź:", 
                    zadanie["opcje"], 
                    index=domyslny_indeks,
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
                        st.rerun()

            # Sekcja informacji zwrotnej (widoczna po kliknięciu sprawdzenia)
            if st.session_state.form_submitted:
                if st.session_state.ostatni_wybor == zadanie["poprawna"]:
                    st.success("Doskonale! To poprawna odpowiedź!")
                else:
                    st.error(f"❌ Błędna odpowiedź. Prawidłowa to: {zadanie['poprawna']}")

                st.info(f"💡 **Wyjaśnienie:** {zadanie['wyjasnienie']}")

                # Dynamiczny tekst na przycisku nawigacji
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

# --- STOPKA ---
st.divider()
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")

