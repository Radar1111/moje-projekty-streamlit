import streamlit as st
import random


# FUNKCJE POMOCNICZE

def generuj_zadanie():
    # Losujemy liczby przyjazne dla 4. klasy
    a, b, c = random.randint(2, 9), random.randint(2, 9), random.randint(5, 20)
    operacja = random.choice(['+', '-'])
    if operacja == '+':
        zadanie = f"{c} + {a} * {b}"
        wynik = c + (a * b)
    else:
        # Zapewniamy, żeby wynik nie był ujemny
        wynik_mnozenia = a * b
        start = wynik_mnozenia + random.randint(1, 10)
        zadanie = f"{start} - {a} * {b}"
        wynik = start - (a * b)
    return zadanie, wynik


def generuj_zadanie_klasa5():
    # Losujemy trudniejsze liczby (mnożenie do 20) oraz dodajemy nawiasy
    typ = random.choice(['mnozenie_duze', 'z_nawiasem'])

    if typ == 'mnozenie_duze':
        # Mnożenie liczby do 20 przez liczbę jednocyfrową (np. 14 * 7 + 15)
        a = random.randint(11, 20)
        b = random.randint(3, 9)
        c = random.randint(10, 50)
        operacja = random.choice(['+', '-'])

        if operacja == '+':
            zadanie = f"{a} * {b} + {c}"
            wynik = (a * b) + c
        else:
            zadanie = f"{a} * {b} - {c}"
            wynik = (a * b) - c

    else:
        # Działanie z nawiasem (wymuszenie pierwszeństwa) np. (12 + 8) * 13
        a = random.randint(5, 20)
        b = random.randint(2, 15)
        c = random.randint(2, 20)  # Mnożnik do 20

        operacja_w_nawiasie = random.choice(['+', '-'])
        if operacja_w_nawiasie == '+':
            zadanie = f"({a} + {b}) * {c}"
            wynik = (a + b) * c
        else:
            # Zabezpieczenie przed ujemnym wynikiem w nawiasie
            if a < b:
                a, b = b, a
            zadanie = f"({a} - {b}) * {c}"
            wynik = (a - b) * c

    return zadanie, wynik


# INICJALIZACJA STANU
if 'zadanie' not in st.session_state:
    st.session_state.zadanie, st.session_state.wynik = generuj_zadanie()
if 'zadanie5' not in st.session_state:
    st.session_state.zadanie5, st.session_state.wynik5 = generuj_zadanie_klasa5()
if 'punkty' not in st.session_state:
    st.session_state.punkty = 0
if 'punkty5' not in st.session_state:
    st.session_state.punkty5 = 0

# INTERFEJS
st.title("🧮 Kolejność Działań")

# Trzy zakładki
tab1, tab2, tab3 = st.tabs(["📖 Tryb Nauki", "🏅 Quiz (Klasa 4)", "🏆 Quiz (Klasa 5 - do 20)"])

# NAUKA
with tab1:
    st.header("Cierpliwy Korepetytor")
    st.write("Wpisz przykład z zeszytu, a ja pokażę Ci jak go rozwiązać.")

    przyklad = st.text_input("Twoje działanie (używaj * dla mnożenia):", placeholder="np. 4 + 5 * 2")

    if przyklad:
        try:
            # Prosta zamiana polskiego zapisu na matematyczny
            czyste_dzialanie = przyklad.replace(':', '/').replace(',', '.')
            wynik_nauka = eval(czyste_dzialanie)

            st.info("### Jak to obliczyć?")
            st.write("1. Najpierw sprawdź czy są **nawiasy**.")
            st.write("2. Wykonaj **mnożenie i dzielenie**.")
            st.write("3. Na koniec zrób **dodawanie i odejmowanie**.")
            st.success(f"Wynik Twojego działania to: **{wynik_nauka}**")
        except:
            st.error("Oj, nie rozumiem tego zapisu. Sprawdź czy nie ma tam błędu!")

# QUIZ KLASA 4
with tab2:
    st.header("Sprawdź co potrafisz - Klasa 4")
    st.write(f"Twoje punkty: ⭐ **{st.session_state.punkty}**")

    st.subheader(f"Ile to jest?")
    st.code(st.session_state.zadanie, language="markdown")

    odp = st.number_input("Wpisz wynik:", step=1, key="input_quiz_k4")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Sprawdź odpowiedź", key="btn_check_k4"):
            if odp == st.session_state.wynik:
                st.success("Brawo! Poprawnie!")
                st.balloons()
                st.session_state.punkty += 1
            else:
                st.error(f"Niestety nie. Poprawny wynik to: {st.session_state.wynik}")
                st.session_state.punkty = 0  # Reset punktów przy błędzie

    with col2:
        if st.button("Następne zadanie ➡️", key="btn_next_k4"):
            st.session_state.zadanie, st.session_state.wynik = generuj_zadanie()
            st.rerun()

# QUIZ KLASA 5 
with tab3:
    st.header("Wyzwanie dla mistrzów - Klasa 5")
    st.write("Tutaj mnożymy do 20 i uważamy na nawiasy!")
    st.write(f"Twoje punkty: 🔥 **{st.session_state.punkty5}**")

    st.subheader(f"Ile to jest?")
    st.code(st.session_state.zadanie5, language="markdown")

    odp5 = st.number_input("Wpisz wynik:", step=1, key="input_quiz_k5")

    col1_5, col2_5 = st.columns(2)

    with col1_5:
        if st.button("Sprawdź odpowiedź", key="btn_check_k5"):
            if odp5 == st.session_state.wynik5:
                st.success("Genialnie! Klasa 5 to dla Ciebie błahostka! 🎉")
                st.snow()
                st.session_state.punkty5 += 1
            else:
                st.error(f"Blisko! Prawidłowa odpowiedź to: {st.session_state.wynik5}")
                st.session_state.punkty5 = 0

    with col2_5:
        if st.button("Następne zadanie ➡️", key="btn_next_k5"):
            st.session_state.zadanie5, st.session_state.wynik5 = generuj_zadanie_klasa5()
            st.rerun()

st.divider()
st.caption("Najcierpliwszy portal do matematyki")
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")
