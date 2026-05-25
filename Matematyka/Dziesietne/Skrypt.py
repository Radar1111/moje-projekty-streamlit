import streamlit as st
import random
import math

# Wstępna konfiguracja strony
st.set_page_config(page_title="Mistrz Dziesiętnych")

# Menu boczne
with st.sidebar:
    st.title("Nawigacja")
    tryb = st.radio(
        "Wybierz rodzaj zadania:",
        ["Działania (+/-)", "Porównywanie (< = >)", "Zamiana ułamków"]
    )
    st.info("Pamiętaj: w Pythonie używamy (.) zamiast przecinka!")

st.title(f"Tryb: {tryb}")

# SEKCJA: Działania (+/-)
if tryb == "Działania (+/-)":
    st.subheader("Oblicz wynik")

    # Czyszczenie pola tekstowego
    if 'clear_dz' not in st.session_state:
        st.session_state.clear_dz = 0

    if 'dzialanie' not in st.session_state:
        a = round(random.uniform(0.1, 9.9), 1)
        b = round(random.uniform(0.1, 9.9), 1)
        op = random.choice(['+', '-'])
        if op == '-' and a < b:
            a, b = b, a

        # Zaokrąglamy sam poprawny wynik od razu do 1 miejsca
        wynik_dzialania = round(a + b if op == "+" else a - b, 1)
        st.session_state.dzialanie = (a, op, b, wynik_dzialania)

    a, op, b, poprawny = st.session_state.dzialanie
    st.write(f"### Ile to jest: **{a} {op} {b}**?")

    odp = st.text_input("Twoja odpowiedź (wpisz i naciśnij Enter):", key=f"ans_dz_{st.session_state.clear_dz}")

    if odp:
        try:
            wynik_user = float(odp.replace(',', '.').strip())


            if round(wynik_user, 1) == poprawny:
                st.success("Brawo! Poprawny wynik!")
                st.balloons()
            else:
                st.error(f"Prawie! Poprawny wynik to {poprawny}. Spróbuj jeszcze raz")
                st.info("Wskazówka: Podpisz przecinek pod przecinkiem!")
        except ValueError:
            st.warning("Wpisz poprawną liczbę!")

    if st.button("Następne zadanie"):
        del st.session_state.dzialanie
        st.session_state.clear_dz += 1
        st.rerun()

# SEKCJA: Porównywanie (< = >)
elif tryb == "Porównywanie (< = >)":
    st.subheader("Wstaw odpowiedni znak")

    if 'clear_por' not in st.session_state:
        st.session_state.clear_por = 0

    if 'porownanie' not in st.session_state:
        v1 = round(random.uniform(0.1, 5.0), 2)
        v2 = v1 if random.random() < 0.2 else round(random.uniform(0.1, 5.0), 2)
        znak = "=" if v1 == v2 else ("<" if v1 < v2 else ">")
        st.session_state.porownanie = (v1, v2, znak)

    v1, v2, poprawny_znak = st.session_state.porownanie
    st.write(f"### Porównaj: **{v1}** ? **{v2}**")

    wybór = st.text_input("Wpisz znak <, = lub > i naciśnij Enter:", key=f"ans_por_{st.session_state.clear_por}")

    if wybór:
        wybór_czysty = wybór.strip()
        if wybór_czysty in ["<", "=", ">"]:
            if wybór_czysty == poprawny_znak:
                st.success("Świetnie! Znak jest poprawny!!")
                st.balloons()
            else:
                st.error(f"Nie, poprawny znak to : {poprawny_znak}")
        else:
            st.warning("Wpisz tylko jeden ze znaków: < , = , >")

    if st.button("Nowe liczby"):
        del st.session_state.porownanie
        st.session_state.clear_por += 1
        st.rerun()

# SEKCJA: Zamiana ułamków
elif tryb == "Zamiana ułamków":
    st.subheader("Zapisz ułamek zwykły jak dziesiętny")

    if 'clear_zam' not in st.session_state:
        st.session_state.clear_zam = 0

    if 'zamiana' not in st.session_state:
        mianowniki = [10, 100]
        mianownik = random.choice(mianowniki)
        licznik = random.randint(1, mianownik - 1)

        poprawny_dz = round(licznik / mianownik, 2)

        # Skracanie ułamków
        # Znajdujemy największy wspólny dzielnik (NWD)
        nwd = math.gcd(licznik, mianownik)
        skrocony_licznik = licznik // nwd
        skrocony_mianownik = mianownik // nwd

        st.session_state.zamiana = (skrocony_licznik, skrocony_mianownik, poprawny_dz)

    l, m, poprawny_dz = st.session_state.zamiana
    st.write(f"Zapisz ułamek jako dziesiętny: **{l}/{m}**?")

    odp_z = st.text_input("Twoja odpowiedź (wpisz i naciśnij Enter):", key=f"ans_zam_{st.session_state.clear_zam}")

    if odp_z:
        try:
            wynik_user = float(odp_z.replace(',', '.').strip())
            if wynik_user == poprawny_dz:
                st.success("Doskonale! Umiesz zamieniać ułamki!")
                st.balloons()
            else:
                st.error(f"Błąd. Poprawny zapis to {poprawny_dz}")
        except ValueError:
            st.warning("Wpisz liczbę w formacie 0.X")

    if st.button("Kolejny ułamek"):
        del st.session_state.zamiana
        st.session_state.clear_zam += 1
        st.rerun()

# STOPKA
st.divider()
st.caption("Najcierpliwszy portal do matematyki - klasa 4")
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")
