import streamlit as st
import random
from decimal import Decimal, ROUND_HALF_UP

st.set_page_config(page_title="Matematyka - Ułamki Dziesiętne", page_icon="🔢", layout="wide")
st.title("🔢 Interaktywna Nauka Ułamków Dziesiętnych")
st.write("Witaj! Ta aplikacja pomoże Ci opanować mnożenie i dzielenie ułamków dziesiętnych!")


# Pomocnicze
def pl_format(val):
    """Zamienia kropkę na polski przecinek w tekście"""
    return str(val).replace('.', ',')


def gen_decimal(min_val=0, max_val=10, places=2):
    """Generuje ładny ułamek dziesiętny jako obiekt Decimal"""
    val = random.uniform(min_val, max_val)
    return Decimal(str(val)).quantize(Decimal('1.' + '0' * places), rounding=ROUND_HALF_UP)


def generuj_nowe_zadanie():
    """Losuje nowe dane do zadania i zapisuje je stabilnie w sesji"""
    st.session_state.ułamek1 = gen_decimal(0, 10, places=random.randint(1, 2))
    st.session_state.ułamek2 = gen_decimal(0, 5, places=random.randint(1, 2))
    st.session_state.liczba_calkowita = random.randint(2, 9)
    st.session_state.potega_dziesieciu = random.choice([10, 100, 1000])

    # Bezpieczne losowanie dla dzielenia przez liczbę całkowitą (aby wynik był ładny i skończony)
    wynik_dziel_calkowita = gen_decimal(1, 5, places=1)
    st.session_state.liczba_calkowita_dziel = random.randint(2, 5)
    st.session_state.ułamek_dziel = (
                wynik_dziel_calkowita * Decimal(st.session_state.liczba_calkowita_dziel)).normalize()

    # Bezpieczne dzielenie ułamka przez ułamek
    st.session_state.u2 = Decimal(str(random.randint(2, 9))) / 10
    wynik_ułamek_ułamek = Decimal(str(random.randint(11, 49))) / 10
    st.session_state.u1 = (wynik_ułamek_ułamek * st.session_state.u2).normalize()


# Stan sesji
if 'ułamek1' not in st.session_state:
    generuj_nowe_zadanie()
if 'poprzedni_typ' not in st.session_state:
    st.session_state.poprzedni_typ = "Mnożenie: Ułamek × Liczba całkowita"

#TEORIA: PRZESUWANIE PRZECINKA
with st.expander("💡 Zobacz jak działa przesuwanie przecinka (Mnożenie i dzielenie przez 10, 100, 1000)"):
    st.markdown("""
    ### 🚀 Szybka metoda: Przesuwanie przecinka
    Kiedy mnożysz lub dzielisz ułamek dziesiętny przez **10, 100, 1000 itd.**, nie musisz liczyć tego pisemnie! Wystarczy przesunąć przecinek o tyle miejsc, ile zer ma liczba.

    #### ✖️ MNOŻENIE = Przesuwamy przecinek w PRAWO (liczba rośnie)
    * Pomnożenie przez **10** (1 zero) $\\rightarrow$ przesunięcie o **1 miejsce** w prawo. np. $2{,}35 \\times 10 = 23{,}5$
    * Pomnożenie przez **100** (2 zera) $\\rightarrow$ przesunięcie o **2 miejsca** w prawo. np. $0{,}123 \\times 100 = 12{,}3$
    * *Jeśli brakuje cyfr, dopisujemy zera na końcu!* np. $4{,}5 \\times 100 = 450$

    #### ➗ DZIELENIE = Przesuwamy przecinek w LEWO (liczba maleje)
    * Podzielenie przez **10** (1 zero) $\\rightarrow$ przesunięcie o **1 miejsce** w lewo. np. $14{,}5 : 10 = 1{,}45$
    * Podzielenie przez **100** (2 zera) $\\rightarrow$ przesunięcie o **2 miejsca** w lewo. np. $7{,}2 : 100 = 0{,}072$
    """)

st.header("🎯 Czas na praktykę! Rozwiąż zadanie:")

typ_zadania = st.selectbox(
    "Wybierz co chcesz ćwiczyć:",
    [
        "Mnożenie: Ułamek × Liczba całkowita",
        "Mnożenie: Ułamek × Ułamek",
        "Mnożenie przez 10, 100, 1000",
        "Dzielenie: Ułamek ÷ Liczba całkowita",
        "Dzielenie: Ułamek ÷ Ułamek",
        "Dzielenie przez 10, 100, 1000"
    ]
)


if typ_zadania != st.session_state.poprzedni_typ:
    st.session_state.poprzedni_typ = typ_zadania
    generuj_nowe_zadanie()
    st.rerun()

# Pobranie wylosowanych wartości
ułamek1 = st.session_state.ułamek1
ułamek2 = st.session_state.ułamek2
liczba_calkowita = st.session_state.liczba_calkowita
liczba_calkowita_dziel = st.session_state.liczba_calkowita_dziel
potega_dziesieciu = st.session_state.potega_dziesieciu
ułamek_dziel = st.session_state.ułamek_dziel
u1, u2 = st.session_state.u1, st.session_state.u2

# LOGIKA ZADAŃ 
if typ_zadania == "Mnożenie: Ułamek × Liczba całkowita":
    pytanie_tekst = f"Ile to jest: ${pl_format(ułamek1)} \\times {liczba_calkowita}$"
    poprawny_wynik = ułamek1 * Decimal(liczba_calkowita)
    u1_bez_przecinka = int(str(ułamek1).replace('.', ''))
    wynik_bez_przecinka = u1_bez_przecinka * liczba_calkowita
    miejsca = abs(ułamek1.as_tuple().exponent)
    wyjasnienie = f"""
    **Krok po kroku:**
    1. Pomnóż te liczby tak, jakby nie było przecinka: ${u1_bez_przecinka} \\times {liczba_calkowita} = {wynik_bez_przecinka}$
    2. Policz miejsca po przecinku w liczbie początkowej: liczba **{pl_format(ułamek1)}** ma ich **{miejsca}**.
    3. Odlicz od końca wyniku dokładnie tyle samo miejsc i wstaw przecinek: **{pl_format(poprawny_wynik.normalize())}**.
    """

elif typ_zadania == "Mnożenie: Ułamek × Ułamek":
    pytanie_tekst = f"Ile to jest: ${pl_format(ułamek1)} \\times {pl_format(ułamek2)}$"
    poprawny_wynik = ułamek1 * ułamek2
    u1_bez_przecinka = int(str(ułamek1).replace('.', ''))
    u2_bez_przecinka = int(str(ułamek2).replace('.', ''))
    wynik_bez_przecinka = u1_bez_przecinka * u2_bez_przecinka
    miejsca1 = abs(ułamek1.as_tuple().exponent)
    miejsca2 = abs(ułamek2.as_tuple().exponent)
    wyjasnienie = f"""
    **Krok po kroku:**
    1. Pomnóż liczby ignorując przecinki: ${u1_bez_przecinka} \\times {u2_bez_przecinka} = {wynik_bez_przecinka}$
    2. Zlicz wszystkie miejsca po przecinku w obu ułamkach razem: {miejsca1} + {miejsca2} = {miejsca1 + miejsca2} miejsca.
    3. Wstaw przecinek w końcowym wyniku, odliczając od prawej strony {miejsca1 + miejsca2} miejsca: **{pl_format(poprawny_wynik.normalize())}**.
    """

elif typ_zadania == "Mnożenie przez 10, 100, 1000":
    pytanie_tekst = f"Ile to jest: ${pl_format(ułamek1)} \\times {potega_dziesieciu}$"
    poprawny_wynik = ułamek1 * Decimal(potega_dziesieciu)
    zera = len(str(potega_dziesieciu)) - 1
    wyjasnienie = f"""
    **Krok po kroku:**
    1. Mnożysz przez {potega_dziesieciu}, czyli liczbę z **{zera}** zerami.
    2. Przesuń przecinek w liczbie {pl_format(ułamek1)} o **{zera}** miejsca w **PRAWO**.
    3. Wynik to: **{pl_format(poprawny_wynik.normalize())}**.
    """

elif typ_zadania == "Dzielenie: Ułamek ÷ Liczba całkowita":
    pytanie_tekst = f"Ile to jest: ${pl_format(ułamek_dziel)} \\div {liczba_calkowita_dziel}$"
    poprawny_wynik = ułamek_dziel / Decimal(liczba_calkowita_dziel)
    wyjasnienie = f"""
    **Krok po kroku:**
    1. Zapisz działanie metodą pisemną (pod kreską).
    2. Wykonaj dzielenie tak, jak na liczbach całkowitych, ignorując na chwilę przecinek.
    3. Postaw przecinek w wyniku dokładnie nad przecinkiem dzielonej liczby.

    > **Przykład ($1,2 \\div 3$):**
    > Zauważ, jak przecinek w wyniku stoi dokładnie nad przecinkiem pod kreską:
    > $$
    > \\begin{{array}}{{l}}
    > \\phantom{{-}}\\mathbf{{0,4}} \\\\
    > \\hline
    > \\phantom{{-}}1,2 \\div 3 \\\\
    > -0 \\\\
    > \\hline
    > \\phantom{{-}}12 \\\\
    > -12 \\\\
    > \\hline
    > \\phantom{{-}}=
    > \\end{{array}}
    > $$

    4. Stosując tę zasadę do naszego zadania, otrzymujemy wynik: **{pl_format(poprawny_wynik.normalize())}**.
    """

elif typ_zadania == "Dzielenie: Ułamek ÷ Ułamek":
    pytanie_tekst = f"Ile to jest: ${pl_format(u1)} \\div {pl_format(u2)}$"
    poprawny_wynik = u1 / u2
    wyjasnienie = f"""
    **Krok po kroku:**
    1. Aby podzielić przez ułamek dziesiętny, zamień dzielnik ({pl_format(u2)}) na liczbę całkowitą.
    2. Przesuń przecinek w obu liczbach w prawo o 1 miejsce: ${pl_format((u1 * 10).normalize())} \\div {pl_format((u2 * 10).normalize())}$
    3. Teraz wykonaj zwykłe dzielenie. Wynik to: **{pl_format(poprawny_wynik.normalize())}**.
    """

else:
    pytanie_tekst = f"Ile to jest: ${pl_format(ułamek1)} \\div {potega_dziesieciu}$"
    poprawny_wynik = ułamek1 / Decimal(potega_dziesieciu)
    zera = len(str(potega_dziesieciu)) - 1
    wyjasnienie = f"""
    **Krok po kroku:**
    1. Dzielisz przez {potega_dziesieciu}, czyli liczbę z **{zera}** zerami.
    2. Przesuń przecinek w liczbie {pl_format(ułamek1)} o **{zera}** miejsca w **LEWO**.
    3. Wynik to: **{pl_format(poprawny_wynik.normalize())}**.
    """

st.markdown(pytanie_tekst)

# Formularz odpowiedzi
user_ans_str = st.text_input("Wpisz swój wynik (użyj kropki lub przecinka):", value="", key="user_answer")

# SPRAWDZANIE ODPOWIEDZI 
if st.button("Sprawdź odpowiedź", type="primary"):
    if user_ans_str.strip() == "":
        st.warning("Najpierw wpisz jakąś odpowiedź!")
    else:
        try:
            normalized_ans = user_ans_str.replace(',', '.')
            user_wynik = Decimal(normalized_ans).normalize()
            poprawny_wynik_normalized = poprawny_wynik.normalize()

            if user_wynik == poprawny_wynik_normalized:
                st.success("🎉 Świetnie! To jest poprawna odpowiedź!")
            else:
                st.error(
                    f"❌ Blisko, ale to nie to. Twój wynik to {pl_format(user_wynik)}, a poprawny to {pl_format(poprawny_wynik_normalized)}.")
        except Exception:
            st.error("Upewnij się, że wpisałeś poprawną liczbę ułamkową!")

# Krok po kroku
if st.checkbox("Pokaż wyjaśnienie krok po kroku"):
    st.info(wyjasnienie)

# --- STOPKA ---
st.divider()
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")

# Przycisk nowego zadania
if st.button("Następne zadanie ➡️"):
    generuj_nowe_zadanie()
    st.rerun()
