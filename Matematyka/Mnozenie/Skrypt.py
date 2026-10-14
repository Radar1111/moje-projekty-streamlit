import streamlit as st
import random
import re


# FUNKCJE POMOCNICZE 

def generuj_zadanie_krok_po_kroku(klasa=4):
    """Generuje zadanie oraz listę kroków obliczeniowych."""
    kroki = []

    if klasa == 4:
        a, b, c = random.randint(2, 9), random.randint(2, 9), random.randint(5, 20)
        operacja = random.choice(['+', '-'])

        if operacja == '+':
            zadanie = f"{c} + {a} * {b}"
            mnozenie = a * b
            wynik = c + mnozenie

            kroki.append(f"Najpierw wykonujemy mnożenie: **{a} * {b} = {mnozenie}**")
            kroki.append(f"Zapisujemy działanie po pierwszym kroku: **{c} + {mnozenie}**")
            kroki.append(f"Na koniec dodajemy: **{c} + {mnozenie} = {wynik}**")
        else:
            mnozenie = a * b
            start = mnozenie + random.randint(1, 10)
            zadanie = f"{start} - {a} * {b}"
            wynik = start - mnozenie

            kroki.append(f"Najpierw wykonujemy mnożenie: **{a} * {b} = {mnozenie}**")
            kroki.append(f"Zapisujemy działanie po pierwszym kroku: **{start} - {mnozenie}**")
            kroki.append(f"Na koniec odejmujemy: **{start} - {mnozenie} = {wynik}**")

    else:  # Klasa 5
        typ = random.choice(['mnozenie_duze', 'z_nawiasem'])

        if typ == 'mnozenie_duze':
            a, b, c = random.randint(11, 20), random.randint(3, 9), random.randint(10, 50)
            operacja = random.choice(['+', '-'])
            mnozenie = a * b

            if operacja == '+':
                zadanie = f"{a} * {b} + {c}"
                wynik = mnozenie + c
                kroki.append(f"Najpierw mnożymy większe liczby: **{a} * {b} = {mnozenie}**")
                kroki.append(f"Następnie dodajemy: **{mnozenie} + {c} = {wynik}**")
            else:
                zadanie = f"{a} * {b} - {c}"
                wynik = mnozenie - c
                kroki.append(f"Najpierw mnożymy większe liczby: **{a} * {b} = {mnozenie}**")
                kroki.append(f"Następnie odejmujemy: **{mnozenie} - {c} = {wynik}**")

        else:  # z nawiasem
            a, b, c = random.randint(5, 20), random.randint(2, 15), random.randint(2, 20)
            operacja_w_nawiasie = random.choice(['+', '-'])

            if operacja_w_nawiasie == '+':
                zadanie = f"({a} + {b}) * {c}"
                nawias = a + b
                wynik = nawias * c
                kroki.append(f"Najważniejszy jest nawias! Obliczamy to, co w środku: **{a} + {b} = {nawias}**")
                kroki.append(f"Zastępujemy nawias wynikiem i mnożymy przez resztę: **{nawias} * {c} = {wynik}**")
            else:
                if a < b: a, b = b, a
                zadanie = f"({a} - {b}) * {c}"
                nawias = a - b
                wynik = nawias * c
                kroki.append(f"Najważniejszy jest nawias! Obliczamy to, co w środku: **{a} - {b} = {nawias}**")
                kroki.append(f"Zastępujemy nawias wynikiem i mnożymy przez resztę: **{nawias} * {c} = {wynik}**")

    return zadanie, wynik, kroki


def rozwiaz_krok_po_kroku_manualnie(tekst):
    """
    Zaawansowany parser, który potrafi rozwiązać KAŻDE standardowe działanie
    krok po kroku, dynamicznie podmieniając obliczone fragmenty.
    """
    # Czyszczenie wpisu
    tekst = tekst.replace(' ', '').replace(':', '/').replace(',', '.')

    # Zzabezpieczenie na wypadek 'x'
    tekst = tekst.replace('x', '*')

    kroki = []
    dzialanie_aktualne = tekst

    # Pętla wykonuje się, dopóki w tekście są jakiekolwiek znaki działań
    
    licznik_bezpieczenstwa = 0
    while błędy := any(c in dzialanie_aktualne for c in ['+', '-', '*', '/']) and licznik_bezpieczenstwa < 10:
        licznik_bezpieczenstwa += 1

        # Ignorujemy sytuację, gdy została już tylko jedna liczba ujemna (np. "-5")
        if re.match(r"^-\d+(\.\d+)?$", dzialanie_aktualne):
            break

        # Krok 1: Szukamy nawiasów najgłębiej osadzonych
        nawiasy = re.search(r"\(([^()]+)\)", dzialanie_aktualne)
        if nawiasy:
            wnetrze = nawiasy.group(1)
            # Wewnątrz nawiasu też obowiązuje kolejność (mnożenie/dzielenie przed dodawaniem)
            sub_kroki, wynik_nawiasu = rozwiaz_krok_po_kroku_manualnie(wnetrze)

            wzorzec_do_zamiany = f"({wnetrze})"
            dzialanie_stare = dzialanie_aktualne
            dzialanie_aktualne = dzialanie_aktualne.replace(wzorzec_do_zamiany, str(wynik_nawiasu), 1)

            kroki.append(f"Najpierw obliczamy środek nawiasu **({wnetrze})** = **{wynik_nawiasu}**")
            kroki.append(f"Nasze działanie wygląda teraz tak: **{dzialanie_aktualne}**")
            continue

        # KROK 2: Mnożenie i dzielenie (od lewej do prawej)
        mnoz_dziel = re.search(r"(\d+(?:\.\d+)?)([\*/])(\d+(?:\.\d+)?)", dzialanie_aktualne)
        if mnoz_dziel:
            num1 = float(mnoz_dziel.group(1)) if '.' in mnoz_dziel.group(1) else int(mnoz_dziel.group(1))
            znak = mnoz_dziel.group(2)
            num2 = float(mnoz_dziel.group(3)) if '.' in mnoz_dziel.group(3) else int(mnoz_dziel.group(3))

            if znak == '*':
                wynik_czesciowy = num1 * num2
                nazwa_dzialania = "mnożenie"
            else:
                wynik_czesciowy = num1 / num2
                nazwa_dzialania = "dzielenie"

            caly_wzorzec = mnoz_dziel.group(0)
            dzialanie_aktualne = dzialanie_aktualne.replace(caly_wzorzec, str(wynik_czesciowy), 1)

            kroki.append(f"Wykonujemy **{nazwa_dzialania}**: {num1} {znak} {num2} = **{wynik_czesciowy}**")
            kroki.append(f"Nasze działanie wygląda teraz tak: **{dzialanie_aktualne}**")
            continue

        # KROK 3: Dodawanie i odejmowanie (od lewej do prawej)
        # Uwzględniamy opcjonalny minus na początku pierwszej liczby
        dodaj_odej = re.search(r"(-?\d+(?:\.\d+)?)([+-])(\d+(?:\.\d+)?)", dzialanie_aktualne)
        if dodaj_odej:
            num1 = float(dodaj_odej.group(1)) if '.' in dodaj_odej.group(1) else int(dodaj_odej.group(1))
            znak = dodaj_odej.group(2)
            num2 = float(dodaj_odej.group(3)) if '.' in dodaj_odej.group(3) else int(dodaj_odej.group(3))

            if znak == '+':
                wynik_czesciowy = num1 + num2
                nazwa_dzialania = "dodawanie"
            else:
                wynik_czesciowy = num1 - num2
                nazwa_dzialania = "odejmowanie"

            caly_wzorzec = dodaj_odej.group(0)
            dzialanie_aktualne = dzialanie_aktualne.replace(caly_wzorzec, str(wynik_czesciowy), 1)

            kroki.append(f"Wykonujemy **{nazwa_dzialania}**: {num1} {znak} {num2} = **{wynik_czesciowy}**")
            if any(c in dzialanie_aktualne for c in ['+', '-', '*', '/']) and not re.match(r"^-\d+(\.\d+)?$",
                                                                                           dzialanie_aktualne):
                kroki.append(f"Nasze działanie wygląda teraz tak: **{dzialanie_aktualne}**")
            continue

        break

    # Koncowy wynik formatowany
    ostateczny_wynik = eval(tekst)
    if isinstance(ostateczny_wynik, float) and ostateczny_wynik.is_integer():
        ostateczny_wynik = int(ostateczny_wynik)

    return kroki, ostateczny_wynik

# INICJALIZACJA STANU
if 'zadanie' not in st.session_state:
    st.session_state.zadanie, st.session_state.wynik, st.session_state.kroki = generuj_zadanie_krok_po_kroku(klasa=4)
if 'zadanie5' not in st.session_state:
    st.session_state.zadanie5, st.session_state.wynik5, st.session_state.kroki5 = generuj_zadanie_krok_po_kroku(klasa=5)
if 'punkty' not in st.session_state:
    st.session_state.punkty = 0
if 'punkty5' not in st.session_state:
    st.session_state.punkty5 = 0
if 'pokaz_wyjasnienie_k4' not in st.session_state:
    st.session_state.pokaz_wyjasnienie_k4 = False
if 'pokaz_wyjasnienie_k5' not in st.session_state:
    st.session_state.pokaz_wyjasnienie_k5 = False

# INTERFEJS
st.title("🧮 Kolejność Działań z Wyjaśnieniami")

tab1, tab2, tab3 = st.tabs(["📖 Tryb Nauki", "🏅 Quiz (Klasa 4)", "🏆 Quiz (Klasa 5)"])

# 1. NAUKA
with tab1:
    st.header("Cierpliwy Korepetytor")
    st.write("Wpisz przykład, a ja rozpiszę go na kroki.")

    przyklad = st.text_input("Twoje działanie (np. 4 + 5 * 2 lub (10 - 2) * 3):", placeholder="Wpisz tutaj...")

    if przyklad:
        try:
            kroki_nauka, wynik_nauka = rozwiaz_krok_po_kroku_manualnie(przyklad)
            st.info("### 📝 Rozwiązanie krok po kroku:")
            for i, krok in enumerate(kroki_nauka, 1):
                st.write(f"{i}. {krok}")
            st.success(f"Ostateczny wynik: **{wynik_nauka}**")
        except Exception:
            st.error("Coś poszło nie tak. Upewnij się, że wpisałeś poprawne liczby i znaki (+, -, *).")

# 2. QUIZ KLASA 4
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
                st.session_state.pokaz_wyjasnienie_k4 = False
            else:
                st.error("Niestety to zły wynik. Zobacz poniżej, jak należało to obliczyć.")
                st.session_state.punkty = 0
                st.session_state.pokaz_wyjasnienie_k4 = True

    with col2:
        if st.button("Następne zadanie ➡️", key="btn_next_k4"):
            st.session_state.zadanie, st.session_state.wynik, st.session_state.kroki = generuj_zadanie_krok_po_kroku(
                klasa=4)
            st.session_state.pokaz_wyjasnienie_k4 = False
            st.rerun()

    # Wyświetlanie kroków po błędzie
    if st.session_state.pokaz_wyjasnienie_k4:
        st.warning("### 💡 Wyjaśnienie:")
        for k in st.session_state.kroki:
            st.write(k)

# 3. QUIZ KLASA 5
with tab3:
    st.header("Wyzwanie dla mistrzów - Klasa 5")
    st.write(f"Twoje punkty: 🔥 **{st.session_state.punkty5}**")

    st.subheader(f"Ile to jest?")
    st.code(st.session_state.zadanie5, language="markdown")

    odp5 = st.number_input("Wpisz wynik:", step=1, key="input_quiz_k5")

    col1_5, col2_5 = st.columns(2)

    with col1_5:
        if st.button("Sprawdź odpowiedź", key="btn_check_k5"):
            if odp5 == st.session_state.wynik5:
                st.success("Genialnie! Klasa 5 opanowana! 🎉")
                st.snow()
                st.session_state.punkty5 += 1
                st.session_state.pokaz_wyjasnienie_k5 = False
            else:
                st.error("Ups! Popełniłeś błąd. Zobacz wyjaśnienie poniżej.")
                st.session_state.punkty5 = 0
                st.session_state.pokaz_wyjasnienie_k5 = True

    with col2_5:
        if st.button("Następne zadanie ➡️", key="btn_next_k5"):
            st.session_state.zadanie5, st.session_state.wynik5, st.session_state.kroki5 = generuj_zadanie_krok_po_kroku(
                klasa=5)
            st.session_state.pokaz_wyjasnienie_k5 = False
            st.rerun()

    if st.session_state.pokaz_wyjasnienie_k5:
        st.warning("### 💡 Wyjaśnienie:")
        for k in st.session_state.kroki5:
            st.write(k)

st.divider()
st.caption("Najcierpliwszy portal do matematyki")
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")
