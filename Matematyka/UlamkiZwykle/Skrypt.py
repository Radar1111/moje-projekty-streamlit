import streamlit as st
from fractions import Fraction
import re
import random
import matplotlib.pyplot as plt

# Ustawienia strony
st.set_page_config(page_title="Ułamki zwykłe i mieszane", page_icon="🍕")
st.title("Twój Cierpliwy Nauczyciel Ułamków")

# SEKCJA: QUIZ - PORÓWNYWANIE UŁAMKÓW (<, =, >)

st.markdown("## 🎮 Mini-Gra: Porównaj ułamki!")

# Inicjalizacja zmiennych w stanie sesji (żeby ułamki się nie zmieniały przy klikaniu)
if 'punkty' not in st.session_state:
    st.session_state.punkty = 0
if 'odpowiedziano' not in st.session_state:
    st.session_state.odpowiedziano = False
if 'komunikat' not in st.session_state:
    st.session_state.komunikat = ""
if 'typ_komunikatu' not in st.session_state:
    st.session_state.typ_komunikatu = "info"


def losuj_nowe_ulamki():
    """Funkcja generuje dwa losowe ułamki do porównania (zwykłe lub mieszane)"""
    mianownik1 = random.randint(2, 10)
    licznik1 = random.randint(1, mianownik1 * 2)  # Czasem ułamki niewłaściwe

    mianownik2 = random.randint(2, 10)
    licznik2 = random.randint(1, mianownik2 * 2)

    # Zapisujemy jako obiekty Fraction
    st.session_state.f1 = Fraction(licznik1, mianownik1)
    st.session_state.f2 = Fraction(licznik2, mianownik2)

    # Tworzymy ładny napis dla dziecka (np. zamiana 5/3 na 1 2/3)
    st.session_state.napis1 = formatuj_ulamek(st.session_state.f1)
    st.session_state.napis2 = formatuj_ulamek(st.session_state.f2)

    st.session_state.odpowiedziano = False
    st.session_state.komunikat = ""


def formatuj_ulamek(f):
    """Pomocnicza funkcja do ładnego wyświetlania ułamków jako liczby mieszane"""
    if f.numerator < f.denominator:
        return f"{f.numerator}/{f.denominator}"
    else:
        cale = f.numerator // f.denominator
        reszta = f.numerator % f.denominator
        if reszta == 0:
            return f"{cale}"
        return f"{cale} {reszta}/{f.denominator}"


# Losujemy ułamki
if 'f1' not in st.session_state:
    losuj_nowe_ulamki()

# Wyświetlanie panelu gry
col1, col2, col3 = st.columns([2, 1, 2])

with col1:
    st.markdown(f"<h2 style='text-align: center; color: #FFD700;'>{st.session_state.napis1}</h2>",
                unsafe_allow_html=True)

with col2:
    st.markdown("<h2 style='text-align: center;'>❓</h2>", unsafe_allow_html=True)

with col3:
    st.markdown(f"<h2 style='text-align: center; color: #FFD700;'>{st.session_state.napis2}</h2>",
                unsafe_allow_html=True)

# Przyciski wyboru znaku
st.write("Wybierz poprawny znak:")
b1, b2, b3, b4 = st.columns(4)

# Określamy poprawny znak
if st.session_state.f1 < st.session_state.f2:
    poprawny_znak = "<"
elif st.session_state.f1 > st.session_state.f2:
    poprawny_znak = ">"
else:
    poprawny_znak = "="

with b1:
    if st.button(" Mniejszy ( < ) ", disabled=st.session_state.odpowiedziano, use_container_width=True):
        st.session_state.odpowiedziano = True
        if poprawny_znak == "<":
            st.session_state.punkty += 1
            st.session_state.komunikat = f"🎉 Brawo! {st.session_state.napis1} jest mniejszy niż {st.session_state.napis2}."
            st.session_state.typ_komunikatu = "success"
        else:
            st.session_state.komunikat = f"❌ Oj, niezupełnie. Prawidłowy znak to: {poprawny_znak}."
            st.session_state.typ_komunikatu = "error"

with b2:
    if st.button(" Równy ( = ) ", disabled=st.session_state.odpowiedziano, use_container_width=True):
        st.session_state.odpowiedziano = True
        if poprawny_znak == "=":
            st.session_state.punkty += 1
            st.session_state.komunikat = f"🎉 Świetnie! Te ułamki są równe."
            st.session_state.typ_komunikatu = "success"
        else:
            st.session_state.komunikat = f"❌ Nie, te ułamki nie są równe. Prawidłowy znak to: {poprawny_znak}."
            st.session_state.typ_komunikatu = "error"

with b3:
    if st.button(" Większy ( > ) ", disabled=st.session_state.odpowiedziano, use_container_width=True):
        st.session_state.odpowiedziano = True
        if poprawny_znak == ">":
            st.session_state.punkty += 1
            st.session_state.komunikat = f"🎉 Super! {st.session_state.napis1} jest większy niż {st.session_state.napis2}."
            st.session_state.typ_komunikatu = "success"
        else:
            st.session_state.komunikat = f"❌ Pudło! Prawidłowy znak to: {poprawny_znak}."
            st.session_state.typ_komunikatu = "error"

with b4:
    if st.button("➡️ Następne", use_container_width=True):
        losuj_nowe_ulamki()
        st.rerun()

# Wyświetlanie komunikatu o wyniku
if st.session_state.komunikat:
    if st.session_state.typ_komunikatu == "success":
        st.success(st.session_state.komunikat)
    elif st.session_state.typ_komunikatu == "error":
        st.error(st.session_state.komunikat)

# Wynik punktowy
st.info(f"🏆 Twoje punkty: **{st.session_state.punkty}**")

st.divider()


# SEKCJA: KALKULATOR

st.markdown("## 🧮 Kalkulator z pizzami i wyjaśnieniem")

query = st.text_input(
    "Wpisz działanie (np. 1/2 + 1/4 lub ułamek z całością 2 1/2):",
    placeholder="np. 2 1/2 + 1/3"
)

if query:
    try:
        clean_query = query.replace(':', '/')
        clean_query = re.sub(r'\s+', ' ', clean_query).strip()

        mixed_pattern = r'(\d+)\s+(\d+)/(\d+)'
        clean_query = re.sub(mixed_pattern, r'(Fraction(\1) + Fraction(\2,\3))', clean_query)

        fraction_pattern = r'(?<!Fraction\()\b(\d+)/(\d+)\b'
        clean_query = re.sub(fraction_pattern, r'Fraction(\1,\2)', clean_query)

        smart_query = re.sub(r'\b(\d+)\b(?![/,\d])(?!(?<=Fraction\()\d*)', r'Fraction(\1)', clean_query)

        allowed_names = {"Fraction": Fraction}
        wynik = eval(smart_query, {"__builtins__": None}, allowed_names)

        st.success(f"Wynik to: **{wynik}**")

        st.markdown("### 🧠 Jak do tego dojść? (Krok po kroku)")
        st.write(f"**1. Sprawdzam Twoje zapytanie:** `{query}`")

        mixed_match = re.search(r'(\d+)\s+(\d+)/(\d+)', query)
        if mixed_match:
            cale_p = int(mixed_match.group(1))
            licz_p = int(mixed_match.group(2))
            mian_p = int(mixed_match.group(3))
            nowy_licznik = (cale_p * mian_p) + licz_p

            st.info(
                f"💡 **Zamiana ułamka mieszanego:** Widzę ułamek mieszany **{cale_p} {licz_p}/{mian_p}**.\n\n"
                f"Zamieniamy go na ułamek niewłaściwy:\n"
                f"* Mnożymy całości przez mianownik: {cale_p} * {mian_p} = {cale_p * mian_p}\n"
                f"* Dodajemy stary licznik: {cale_p * mian_p} + {licz_p} = **{nowy_licznik}**\n"
                f"* Mianownik zostaje bez zmian: **{mian_p}**\n\n"
                f"Otrzymujemy ułamek: **{nowy_licznik}/{mian_p}**"
            )

        st.write(f"**2. Liczę dokładnie:** {wynik.numerator} (licznik) przez {wynik.denominator} (mianownik).")

        # RYSOWANIE PIZZ
        wartosc = float(wynik)
        cale = int(wartosc)
        ulamek = wartosc - cale

        liczba_pizz = cale + (1 if ulamek > 0 else 0)
        if liczba_pizz == 0:
            liczba_pizz = 1

        fig, axes = plt.subplots(1, liczba_pizz, figsize=(liczba_pizz * 3, 3))
        if liczba_pizz == 1:
            axes = [axes]

        for i in range(liczba_pizz):
            ax = axes[i]
            if i < cale:
                sizes = [1]
                colors = ['#FFD700']
            else:
                if ulamek > 0:
                    sizes = [ulamek, 1 - ulamek]
                    colors = ['#FFD700', '#F0F2F6']
                else:
                    sizes = [1]
                    colors = ['#F0F2F6']

            ax.pie(sizes, startangle=90, colors=colors,
                   wedgeprops={'edgecolor': 'white', 'linewidth': 2})
            ax.set_title(f"Pizza {i + 1}")
            ax.axis('equal')

        st.pyplot(fig)
        plt.close(fig)

        st.write(f"**3. Analiza wyniku końcowego:**")
        if wynik.numerator >= wynik.denominator:
            calosc = wynik.numerator // wynik.denominator
            reszta = wynik.numerator % wynik.denominator
            if reszta > 0:
                st.info(f"Wynik {wynik} to inaczej liczba mieszana: **{calosc} i {reszta}/{wynik.denominator}**")
            else:
                st.info(f"Wynik to po prostu całe liczby: **{calosc}**")
        else:
            st.info(f"Wynik to ułamek właściwy (mniejszy niż 1): **{wynik}**")

        st.info("💡 Wskazówka: Wyobraź sobie, że dzielisz pizzę na tyle kawałków, ile wynosi dolna liczba!")

    except Exception as e:
        print(f"Błąd uruchomienia: {e}")
        st.error(f"Oj, coś nie tak wpisałeś. Używaj cyfr i znaków +, -, *, / (np. 1 1/2 + 2/4)")

# Stopka
st.divider()
st.caption("Najcierpliwszy portal do matematyki - klasa 4")
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")
