import streamlit as st
import random

# Konfiguracja strony
st.set_page_config(page_title="Zgadnij Słowo", layout="centered")
st.title("Zgadnij Słowo")
st.markdown(
    """
    <style>
    /* 1. Wymuszenie rzędu poziomowego dla kolumn na każdym ekranie */
    [data-testid="stHorizontalBlock"] {
        flex-direction: row !important;
        gap: 6px !important;
    }

    /* 2. Reset domyślnych szerokości kolumn Streamlita */
    [data-testid="column"] {
        width: calc(20% - 6px) !important;
        flex: 1 1 auto !important;
        min-width: 0 !important;
    }

    /* 3. Likwidacja ogromnych marginesów bocznych Streamlita na telefonach */
    @media (max-width: 640px) {
        .block-container {
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
            padding-top: 1rem !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.write("Odgadnij ukryte 5-literowe słowo! Masz 6 prób")

# Baza słów
WORD_BANK = ["ARBUZ", "BANAN", "BĘBEN", "BILET", "BLUZA", "BRAMA", "BUTIK", "CHLEB", "CISZA",
             "CYFRA", "CYTRA", "DESKA", "DROGA", "DYWAN", "DZIEŃ", "EKRAN", "FILAR", "FLAGA",
             "FOTEL", "GŁOWA", "GUZIK", "HAŁAS", "HOTEL", "INDYK", "ISKRA", "JAJKO", "JĘZYK",
             "KABEL", "KAKAO", "KANAŁ", "KARTA", "KATAR", "KIOSK", "KLASA", "KLUCZ", "KREDA",
             "KWIAT", "LAMPA", "LASKA", "ŁYŻWA", "MAŁPA", "MASŁO", "MLEKO", "MORZE", "MOTYL",
             "NAPIS", "NARTY", "NIEBO", "OBRAZ", "OBRUS", "OGRÓD", "OPERA", "OPONA", "ORDER",
             "OSADA", "OSOBA", "PALEC", "PASEK", "PAŁAC", "PERŁA", "PIŁKA", "PIÓRO", "PLAŻA",
             "POKÓJ", "POLAK", "POMOC", "POTOK", "POŻAR", "PRACA", "PRASA", "PUDEL", "PUDER",
             "PUNKT", "ROWER", "RYNNA", "RYNEK", "SALON", "SCENA", "SERCE", "SEZON", "SKLEP",
             "SKAŁA", "SKÓRA", "SŁAWA", "SŁOWO", "SZNUR", "SZAFA", "SZPAK", "ŚWIAT", "TEATR",
             "TRAWA", "UBIÓR", "UCZEŃ", "UMYSŁ", "URZĄD", "WAGON", "WALKA", "WANNA", "WARTA"]

# Inicjalizacja stanu gry
if "secret_word" not in st.session_state:
    st.session_state.secret_word = random.choice(WORD_BANK).upper()
    st.session_state.guesses = []  # Lista wpisanych słów
    st.session_state.game_over = False
    st.session_state.won = False


# Funkcja restartu
def reset_game():
    st.session_state.secret_word = random.choice(WORD_BANK).upper()
    st.session_state.guesses = []
    st.session_state.won = False
    st.session_state.game_over = False


# Wyświetlanie żyć serduszek
max_attempts = 6
current_attempts = len(st.session_state.guesses)
hearts_left = max_attempts - current_attempts

# Wyświetlamy czerwone serduszka
hearts_display = "❤️" * hearts_left + "💔" * current_attempts
st.subheader(f"Życie: {hearts_display}")

# Formularz wpisywania słowa
with st.form(key="guesses_form", clear_on_submit=True):
    user_guess = st.text_input("Wpisz 5-literowe słowo:", max_chars=5)
    submit_button = st.form_submit_button(label="Sprawdź")

# Logika po zatwierdzeniu słowa
if submit_button and not st.session_state.game_over:
    user_guess = user_guess.upper()  # Zamiana na wielkie litery

    if len(user_guess) != 5:
        st.warning("Słowo musi mieć dokładnie 5 liter!")
    elif user_guess in st.session_state.guesses:
        st.warning("To słowo już było wpisane!")
    else:
        st.session_state.guesses.append(user_guess)

        # Sprawdzanie wygranej
        if user_guess == st.session_state.secret_word:
            st.session_state.won = True
            st.session_state.game_over = True
        # Sprawdzanie przegranej - koniec prób
        elif len(st.session_state.guesses) >= max_attempts:
            st.session_state.game_over = True
        st.rerun()


# Renderowanie planszy z kolorami - WERSJA MOBILNA
st.write("### Twoje próby:")

for attempt in range(max_attempts):
    # Kontener trzymający rząd w poziomie na każdym urządzeniu
    row_html = '<div style="display: flex; flex-direction: row; gap: 8px; justify-content: center; width: 100%; margin-bottom: 8px;">'

    if attempt < len(st.session_state.guesses):
        guess = st.session_state.guesses[attempt]
        secret = st.session_state.secret_word

        for i in range(5):
            letter = guess[i]

            if letter == secret[i]:
                bg_color = "#FF4B4B"  # Czerwony
                text_color = "white"
            elif letter in secret:
                bg_color = "#1C83E1"  # Niebieski
                text_color = "white"
            else:
                bg_color = "#31333F"  # Szary
                text_color = "#A3A8B4"

            row_html += f"""
                <div style="
                    background-color: {bg_color};
                    color: {text_color};
                    text-align: center;
                    font-size: 24px;
                    font-weight: bold;
                    width: 3.5rem;   /* Stała, ładna wielkość na komputerze */
                    height: 3.5rem;  /* Wymuszenie równej wysokości */
                    max-width: 18vw; /* Elastyczność: na bardzo małych telefonach nie przekroczy szerokości ekranu */
                    max-height: 18vw;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    border-radius: 5px;
                    border: 1px solid #464855;
                    box-sizing: border-box;
                ">
                    {letter}
                </div>
            """
    else:
        # Puste pola dla pozostałych prób
        for i in range(5):
            row_html += """
                <div style="
                    background-color: transparent;
                    color: #464855;
                    width: 3.5rem;
                    height: 3.5rem;
                    max-width: 18vw;
                    max-height: 18vw;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    border-radius: 5px;
                    border: 2px dashed #464855;
                    box-sizing: border-box;
                ">
                    &nbsp;
                </div>
            """

    row_html += '</div>'
    st.html(row_html)

# Komunikaty końcowe
if st.session_state.game_over:
    st.write("---")
    if st.session_state.won:
        st.balloons()
        st.success(f"Gratulacje! Odgadłeś słowo: **{st.session_state.secret_word}**")
    else:
        st.error(f"Przegrana! Ukryte słowo to: **{st.session_state.secret_word}**")

# Nowa gra
st.write("---")
st.button("Zagraj jeszcze raz", on_click=reset_game, type="primary")

st.divider()
st.caption("Relaks po nauce")
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")
