import streamlit as st
import random


# --- FUNKCJE POMOCNICZE ---
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


# --- INICJALIZACJA STANU ---
if 'zadanie' not in st.session_state:
    st.session_state.zadanie, st.session_state.wynik = generuj_zadanie()
if 'punkty' not in st.session_state:
    st.session_state.punkty = 0

# --- INTERFEJS ---
st.title("🧮 Kolejność Działań")

# Tworzymy zakładki
tab1, tab2 = st.tabs(["📖 Tryb Nauki", "🏆 Quiz"])

# --- ZAKŁADKA 1: NAUKA ---
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

# --- ZAKŁADKA 2: QUIZ ---
with tab2:
    st.header("Sprawdź co potrafisz!")
    st.write(f"Twoje punkty: ⭐ **{st.session_state.punkty}**")

    st.subheader(f"Ile to jest?")
    st.code(st.session_state.zadanie, language="markdown")

    odp = st.number_input("Wpisz wynik:", step=1, key="input_quiz")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Sprawdź odpowiedź"):
            if odp == st.session_state.wynik:
                st.success("Brawo! Poprawnie!")
                st.balloons()
                st.session_state.punkty += 1
            else:
                st.error(f"Niestety nie. Poprawny wynik to: {st.session_state.wynik}")
                st.session_state.punkty = 0  # Reset punktów przy błędzie (opcjonalnie)

    with col2:
        if st.button("Następne zadanie ➡️"):
            st.session_state.zadanie, st.session_state.wynik = generuj_zadanie()
            st.rerun()

st.divider()
st.caption("Najcierpliwszy portal do matematyki - klasa 4")
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")
