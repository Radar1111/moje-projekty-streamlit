import streamlit as st
import random
import math


# Funkcja generująca zadanie dopasowane do IV klasy
def generuj_zadanie(dzialanie):
    # Losujemy mianowniki od 2 do 9
    m1 = random.randint(2, 9)
    m2 = random.randint(2, 9)
    while m1 == m2:
        m2 = random.randint(2, 9)

    # Liczniki (ułamki właściwe)
    l1 = random.randint(1, m1 - 1)
    l2 = random.randint(1, m2 - 1)

    # Najmniejszy wspólny mianownik (NWW)
    wspolny = math.lcm(m1, m2)

    mnoznik1 = wspolny // m1
    mnoznik2 = wspolny // m2

    nowy_l1 = l1 * mnoznik1
    nowy_l2 = l2 * mnoznik2

    # ZABEZPIECZENIE DLA ODEJMOWANIA: Pierwszy ułamek musi być większy lub równy drugiemu
    if dzialanie == "Odejmowanie" and nowy_l1 < nowy_l2:
        # Zamieniamy ułamki miejscami, aby wynik nie był ujemny
        l1, l2 = l2, l1
        m1, m2 = m2, m1
        nowy_l1, nowy_l2 = nowy_l2, nowy_l1
        mnoznik1, mnoznik2 = mnoznik2, mnoznik1

    # Obliczenie licznika wyniku w zależności od wybranego działania
    if dzialanie == "Dodawanie":
        wynik_l = nowy_l1 + nowy_l2
        znak = "+"
        nazwa_dzialania = "Dodajemy liczniki (góry ułamków)"
        opis_dzialania = f"{nowy_l1} + {nowy_l2} = {wynik_l}"
        ikona_kroku = "➕"
    else:
        wynik_l = nowy_l1 - nowy_l2
        znak = "-"
        nazwa_dzialania = "Odejmujemy liczniki (góry ułamków)"
        opis_dzialania = f"{nowy_l1} - {nowy_l2} = {wynik_l}"
        ikona_kroku = "➖"

    # Skracanie i wyciąganie całości
    if wynik_l == 0:
        dzielnik = 1
        skrocony_l = 0
        skrocony_m = wspolny
        calosci = 0
        reszta_l = 0
    else:
        dzielnik = math.gcd(wynik_l, wspolny)
        skrocony_l = wynik_l // dzielnik
        skrocony_m = wspolny // dzielnik
        calosci = skrocony_l // skrocony_m
        reszta_l = skrocony_l % skrocony_m

    # Dynamiczne generowanie wielokrotności tak, aby ZAWSZE pokazać wspólny mianownik
    zasieg_m1 = (wspolny // m1) + 1
    zasieg_m2 = (wspolny // m2) + 1
    
    wielokrotnosci_m1 = [m1 * i for i in range(1, zasieg_m1 + 1)]
    wielokrotnosci_m2 = [m2 * i for i in range(1, zasieg_m2 + 1)]

    # Przyjazne, szkolne wyjaśnienie krok po kroku
    wyjasnienie = (
        f"### 🎯 Krok 1: Szukamy wspólnego mianownika\n"
        f"Wypisujemy wielokrotności liczb **{m1}** i **{m2}**, aż znajdziemy pierwszą wspólną liczbę:\n"
        f"* Wielokrotności liczby {m1}: {', '.join(map(str, wielokrotnosci_m1))}...\n"
        f"* Wielokrotności liczby {m2}: {', '.join(map(str, wielokrotnosci_m2))}...\n\n"
        f"Nasza wspólna liczba to **{wspolny}**. To będzie nasz nowy mianownik!\n\n"

        f"### 📈 Krok 2: Rozszerzamy ułamki\n"
        f"Teraz musimy pomnożyć góry i doły ułamków, aby na dole była liczba {wspolny}.\n"
        f"* Pierwszy ułamek rozszerzamy przez **{mnoznik1}** (bo {wspolny} : {m1} = {mnoznik1}):  \n"
        f"  ({l1} * {mnoznik1}) / ({m1} * {mnoznik1}) = **{nowy_l1}/{wspolny}**\n"
        f"* Drugi ułamek rozszerzamy przez **{mnoznik2}** (bo {wspolny} : {m2} = {mnoznik2}):  \n"
        f"  ({l2} * {mnoznik2}) / ({m2} * {mnoznik2}) = **{nowy_l2}/{wspolny}**\n\n"

        f"### {ikona_kroku} Krok 3: {nazwa_dzialania}\n"
        f"Wykonujemy działanie tylko na górze, a dół zostaje bez zmian:\n"
        f"**{nowy_l1}/{wspolny} {znak} {nowy_l2}/{wspolny}**\n\n"
        f"Działanie na licznikach: {opis_dzialania}  \n"
        f"Nasz wynik na tym etapie to: **{wynik_l}/{wspolny}**."
    )

    # Krok 4: Skracanie (z informacją gdy nie zachodzi)
    if wynik_l > 0:
        if dzielnik > 1:
            wyjasnienie += (
                f"\n\n### ✂️ Krok 4: Skracanie ułamka\n"
                f"Zarówno licznik, jak i mianownik możemy podzielić przez **{dzielnik}**.\n"
                f"{wynik_l} : {dzielnik} = {skrocony_l}  \n"
                f"{wspolny} : {dzielnik} = {skrocony_m}  \n"
                f"Otrzymujemy ułamek: **{skrocony_l}/{skrocony_m}**."
            )
        else:
            wyjasnienie += (
                f"\n\n### ✂️ Krok 4: Skracanie ułamka\n"
                f"Licznik i mianownik nie mają wspólnego dzielnika (poza 1).  \n"
                f"Tego ułamka **nie da się skrócić**. Zostaje tak, jak jest: **{wynik_l}/{wspolny}**."
            )

    # Krok 5: Całości lub Zero (z informacją gdy nie zachodzi)
    if wynik_l == 0:
        wyjasnienie += f"\n\n### 📦 Krok 5: Wynik końcowy\nJeśli na górze mamy 0, to cały ułamek jest równy **0**."
    elif calosci > 0:
        if reszta_l == 0:
            wyjasnienie += f"\n\n### 📦 Krok 5: Wyciągamy całości\nWynik tworzy pełną liczbę: **{calosci}**."
        else:
            wyjasnienie += (
                f"\n\n### 📦 Krok 5: Wyciągamy całości\n"
                f"W liczbie {skrocony_l} mieści się {calosci} pełnych mianowników {skrocony_m}.\n"
                f"Zostaje nam reszta {reszta_l}.  \n"
                f"Ostateczny wynik to: **{calosci} i {reszta_l}/{skrocony_m}**."
            )
    else:
        wyjasnienie += (
            f"\n\n### 📦 Krok 5: Wyciągamy całości\n"
            f"Licznik ({skrocony_l}) jest mniejszy od mianownika ({skrocony_m}).  \n"
            f"Jest to ułamek właściwy, więc **nie wyciągamy z niego całości**."
        )

    # Przygotowanie poprawnych odpowiedzi do ukrytej weryfikacji
    # Jeśli wynik to 0, to całości=0, licznik=0, mianownik=wspolny
    poprawne_odpowiedzi = {
        "calosci": calosci,
        "licznik": reszta_l if wynik_l > 0 else 0,
        "mianownik": skrocony_m if wynik_l > 0 else wspolny
    }

    return f"{l1}/{m1} {znak} {l2}/{m2}", wyjasnienie, poprawne_odpowiedzi


# --- KONFIGURACJA STREAMLIT ---
st.set_page_config(page_title="Mistrz Ułamków dla Klasy 4", page_icon="🎒")

st.title("🎒 Mistrz Ułamków – Trener Klasy 4")
st.write("Rozwiąż zadanie w zeszycie, wpisz swój wynik i sprawdź, czy masz rację!")

# --- PANEL BOCZNY ---
st.sidebar.header("⚙️ Ustawienia treningu")
rodzaj_dzialania = st.sidebar.radio(
    "Wybierz działanie:",
    ("Dodawanie", "Odejmowanie")
)

st.sidebar.markdown("---")
st.sidebar.write("Stworzone dla Twojej nauki! 🚀")

# Inicjalizacja stanu sesji
if 'pytanie' not in st.session_state:
    st.session_state.pytanie = "Kliknij przycisk poniżej, aby wylosować pierwsze zadanie!"
    st.session_state.wyjasnienie = ""
    st.session_state.odpowiedzi = None

# Losowanie zadania z uwzględnieniem wybranego działania
if st.button('🎲 Losuj nowe zadanie'):
    pytanie, wyjasnienie, odpowiedzi = generuj_zadanie(rodzaj_dzialania)
    st.session_state.pytanie = pytanie
    st.session_state.wyjasnienie = wyjasnienie
    st.session_state.odpowiedzi = odpowiedzi

# Wyświetlanie aktualnego zadania
st.subheader("Twoje zadanie:")
st.success(f"## {st.session_state.pytanie}")

# --- SEKCJA WPISYWANIA WYNIKU PRZEZ UCZNIA ---
if st.session_state.odpowiedzi is not None:
    st.markdown("### 📝 Wpisz swój ostateczny wynik po skróceniu i wyciągnięciu całości:")
    st.write("_Jeśli w Twoim wyniku nie ma całości lub ułamek zniknął, wpisz tam po prostu cyfrę 0._")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        user_calosci = st.number_input("Całości:", min_value=0, step=1, value=0, key="user_c")
    with col2:
        user_licznik = st.number_input("Licznik:", min_value=0, step=1, value=0, key="user_l")
    with col3:
        user_mianownik = st.number_input("Mianownik:", min_value=1, step=1, value=1, key="user_m")
        
    if st.button("🎯 Sprawdź mój wynik"):
        poprawne = st.session_state.odpowiedzi
        if (user_calosci == poprawne["calosci"] and 
            user_licznik == poprawne["licznik"] and 
            user_mianownik == poprawne["mianownik"]):
            st.balloons()
            st.success("🎉 Genialnie! Twój wynik jest w 100% poprawny! Jesteś mistrzem!")
        else:
            st.error("🤔 Blisko! Coś poszło nie tak. Sprawdź rozwiązanie krok po kroku poniżej, aby odnaleźć błąd.")

# Ukryte rozwiązanie
if st.session_state.wyjasnienie:
    with st.expander("🔍 Zobacz pełne rozwiązanie krok po kroku (kliknij tutaj)"):
        st.markdown(st.session_state.wyjasnienie)

st.divider()
st.caption("Najcierpliwszy portal do matematyki - klasa 4")
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")
