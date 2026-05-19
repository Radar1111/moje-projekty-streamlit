import random
import streamlit as st
import datetime

# Funkcje Pomocnicze
ROMAN_MAP = [
    (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
    (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
    (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
]


def to_roman(n):
    roman = ''
    for value, symbol in ROMAN_MAP:
        while n >= value:
            roman += symbol
            n -= value
    return roman


# Funkcja weryfikacji
def weryfikuj_quiz():
    wpisane = st.session_state.wpisana_odp_quiz.strip()

    if st.session_state.mode == "A->R":
        wpisane = wpisane.upper()
        poprawna_odp = to_roman(st.session_state.quiz_num)
    else:
        poprawna_odp = str(st.session_state.quiz_num)

    if wpisane == poprawna_odp:
        st.session_state.odpowiedz_prawidlowa = True
    else:
        st.session_state.odpowiedz_prawidlowa = False

    st.session_state.pokazuj_wyjasnienie = True


# Konfig strony
st.set_page_config(page_title="Rzymski Mistrz", layout="centered")
st.title("🏛️ Rzymskie Liczby - Nauka i Zabawa")

menu = st.sidebar.radio("Wybierz sekcję:", ["Nauka", "Konwerter Dat", "Quiz"])

if menu == "Nauka":
    st.header("Powtórka Wiadomości")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Podstawowe znaki")
        st.table({
            "Arabska": [1, 5, 10, 50, 100, 500, 1000],
            "Rzymska": ["I", "V", "X", "L", "C", "D", "M"]
        })
    with col2:
        st.subheader("Zasady")
        st.write("- Max 3 te same znaki obok siebie (III=3, ale 4=IV).")
        st.write("- Mniejsza przed większą = odejmowanie (IX = 10-1).")
        st.write("- Mniejsza po większej = dodawanie (XI = 10+1).")

elif menu == "Konwerter Dat":
    st.header("Daty i Liczby")
    try:
        num = st.number_input("Wpisz liczbę (1-3999):", min_value=1, max_value=3999, value=10)
        rzymski_wynik = to_roman(num)
        st.info(f"Rzymski zapis: **{rzymski_wynik}**")

        st.divider()

        st.subheader("Konwerter pełnej daty")

        # Zakres lat 1900-2099 w opisie
        d = st.date_input(
            "Wybierz lub wpisz datę RRRR/MM/DD (zakres: od 1900 do 2099 roku):",
            value=datetime.date(2000, 1, 1),
            min_value=datetime.date(1900, 1, 1),
            max_value=datetime.date(2099, 12, 31)
        )

        if d is not None:
            rzym_dzien = to_roman(d.day)
            rzym_miesiac = to_roman(d.month)
            rzym_rok = to_roman(d.year)

            rzym_data_str = f"{rzym_dzien}.{rzym_miesiac}.{rzym_rok}"
            st.success(f"Data rzymska: **{rzym_data_str}**")
        else:
            st.warning("Czekam na podanie poprawnej daty...")

    except Exception as e:
        # Komunikat błędu
        st.error("⚠️ Coś poszło nie tak. Upewnij się, że wpisana data mieści się w przedziale lat 1900-2099.")

elif menu == "Quiz":
    st.header("Quiz: Sprawdź się")

    if 'quiz_num' not in st.session_state:
        st.session_state.quiz_num = random.randint(1, 100)
        st.session_state.mode = random.choice(["A->R", "R->A"])
        st.session_state.pokazuj_wyjasnienie = False
        st.session_state.odpowiedz_prawidlowa = False

    if st.session_state.mode == "A->R":
        zagadka = f"Jak zapisać liczbę **{st.session_state.quiz_num}** po rzymsku?"
        odpowiedz_wzorcowa = to_roman(st.session_state.quiz_num)
    else:
        rzymska_zagadka = to_roman(st.session_state.quiz_num)
        zagadka = f"Jaka to liczba arabska: **{rzymska_zagadka}**?"
        odpowiedz_wzorcowa = str(st.session_state.quiz_num)

    st.write(zagadka)

    if st.session_state.pokazuj_wyjasnienie:
        if st.session_state.odpowiedz_prawidlowa:
            st.balloons()
            st.success("Brawo! Poprawna odpowiedź!")
        else:
            st.error(f"Niestety nie. Poprawna odpowiedź to: **{odpowiedz_wzorcowa}**")

        if st.button("Następne pytanie ➡️"):
            st.session_state.quiz_num = random.randint(1, 100)
            st.session_state.mode = random.choice(["A->R", "R->A"])
            st.session_state.pokazuj_wyjasnienie = False
            st.rerun()
    else:
        st.text_input(
            "Twoja odpowiedź (zatwierdź Enterem):",
            key="wpisana_odp_quiz",
            on_change=weryfikuj_quiz
        )

# STOPKA
st.divider()
st.caption("Najcierpliwszy portal do historii - klasa 4")
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")
