import streamlit as st
import random
from fractions import Fraction

st.set_page_config(page_title="Matematyka - Ułamki", page_icon="🧮", layout="wide")

st.title("🧮 Interaktywna Nauka Ułamków")
st.write("Witaj! Ta aplikacja pomoże Ci opanować mnożenie i dzielenie ułamków zwykłych oraz niewłaściwych!")


def wyswietl_sekcje_wsparcia():
    # Inicjalizacja sesji
    if "parent_verified" not in st.session_state:
        st.session_state.parent_verified = False
    if "num1" not in st.session_state:
        st.session_state.num1 = random.randint(5, 15)
    if "num2" not in st.session_state:
        st.session_state.num2 = random.randint(5, 15)

    LINK_DO_KAWY = "https://buycoffee.to/gigawiedza"

    # Separator
    st.divider()

    # Expander na dole strony
    with st.expander("👪 Dla Rodziców / Starszych Uczniów (Strefa Wspierania)"):
        if not st.session_state.parent_verified:
            st.write("Aby wejść, potwierdź że jesteś osobą dorosłą:")
            pytanie = f"Ile to jest {st.session_state.num1} + {st.session_state.num2}?"


            odpowiedz_rodzica = st.number_input(pytanie, step=1, value=0, key="footer_parent_input")

            if st.button("Zatwierdź", key="footer_parent_btn", use_container_width=True):
                poprawny_wynik = st.session_state.num1 + st.session_state.num2
                if odpowiedz_rodzica == poprawny_wynik:
                    st.session_state.parent_verified = True
                    st.rerun()
                else:
                    st.error("Nieprawidłowy wynik. Spróbuj ponownie!")
        else:
            st.success("Weryfikacja pomyślna!")
            st.markdown(
                """
                **Drogi Rodzicu / Starszy Uczniu!**  
                Tworzę te aplikacje z myślą o bezpiecznym i skutecznym rozwoju oraz nauce. 
                Udostępniam je całkowicie **za darmo i bez reklam**.

                Utrzymanie projektów wymaga jednak realnych kosztów i setek godzin pracy. 
                Jeśli aplikacja pomogła w nauce i chcesz wesprzeć rozwój kolejnych programów 
                – możesz postawić mi wirtualną kawę. Dziękuję!
                """
            )
            st.link_button("☕ Postaw wirtualną kawę", LINK_DO_KAWY, type="primary", use_container_width=True)

            if st.button("Zablokuj strefę", type="secondary", use_container_width=True, key="footer_lock_btn"):
                st.session_state.parent_verified = False
                st.session_state.num1 = random.randint(5, 15)
                st.session_state.num2 = random.randint(5, 15)
                st.rerun()

            st.caption(
                "**Informacja o wsparciu:** "
                "Wszelkie wpłaty realizowane za pośrednictwem platformy BuyCoffee.to mają charakter "
                "całkowicie dobrowolnego, bezinteresownego wsparcia (darowizny) na rzecz dalszego rozwoju "
                "i utrzymania portfolio bezpłatnych aplikacji. Wpłata nie wiąże się z zakupem żadnych "
                "cyfrowych towarów, usług ani dodatkowych funkcji w aplikacji."
            )

st.sidebar.title("Ustawienia")
with st.sidebar:
    wyswietl_sekcje_wsparcia()

# 📝 MULTI-BRUDNOPIS W SIDEBARZE
st.sidebar.markdown("---")
st.sidebar.header("📝 Brudnopis Ucznia")

zakladka_rysuj, zakladka_pisz = st.sidebar.tabs(["🎨 Rysuj", "✍️ Pisz"])

with zakladka_rysuj:
    st.caption("Rysuj myszką lub palcem. Kliknij ikonę kosza pod tablicą, aby wyczyścić.")
    from streamlit_drawable_canvas import st_canvas

    st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=3,
        stroke_color="#000000",
        background_color="#ffffff",
        update_streamlit=False,
        height=250,
        drawing_mode="freedraw",
        key="globalny_canvas_brudnopis",
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
    

# TEORIA: SKRACANIE NA KRZYŻ
with st.expander("💡 Zobacz jak działa skracanie na krzyż (Wytłumaczenie)"):
    st.markdown("""
    ### Na czym polega skracanie na krzyż?
    Kiedy mnożymy dwa ułamki, możemy **podzielić licznik jednego ułamka i mianownik drugiego ułamka** przez tę samą liczbę. Działa to "po przekątnej" (na krzyż). Dzięki temu działamy na mniejszych liczbach i łatwiej się liczy!

    #### Przykład:
    Wyobraź sobie działanie:
    $$\\frac{3}{4} \\times \\frac{8}{9}$$

    1. **Sprawdzamy pierwszą przekątną:** Licznik pierwszego ($3$) i mianownik drugiego ($9$). Obie liczby dzielą się przez **3**.
       * $3 : 3 = 1$
       * $9 : 3 = 3$
    2. **Sprawdzamy drugą przekątną:** Mianownik pierwszego ($4$) i licznik drugiego ($8$). Obie liczby dzielą się przez **4**.
       * $4 : 4 = 1$
       * $8 : 4 = 2$

    #### Nowe działanie po skróceniu:
    $$\\frac{1}{1} \\times \\frac{2}{3} = \\frac{1 \\times 2}{1 \\times 3} = \\frac{2}{3}$$

    *Bez skracania działanie wyglądałoby tak: $\\frac{3 \\times 8}{4 \\times 9} = \\frac{24}{36}$, co i tak trzeba na koniec skrócić do $\\frac{2}{3}$. Skracanie na krzyż jest po prostu szybsze!*
    """)

# Generator zadań
st.header("🎯 Czas na praktykę! Rozwiąż zadanie:")

# Inicjalizacja stanu sesji
if 'random_seed' not in st.session_state:
    st.session_state.random_seed = random.randint(1, 100000)
    st.session_state.user_answered = False

random.seed(st.session_state.random_seed)

# Wybór rodzaju zadania
typ_zadania = st.selectbox(
    "Wybierz co chcesz ćwiczyć:",
    [
        "Mnożenie: Ułamek × Liczba",
        "Mnożenie: Ułamek × Ułamek",
        "Dzielenie: Ułamek ÷ Liczba",
        "Dzielenie: Ułamek ÷ Ułamek"
    ]
)

# Generowanie losowych ułamków (zwykłe i niewłaściwe)
l1 = random.randint(1, 12)
m1 = random.randint(2, 12)
l2 = random.randint(1, 12)
m2 = random.randint(2, 12)
liczba_calkowita = random.randint(2, 9)

# Zapobieganie ułamkom o mianowniku 0
if m1 == 0: m1 = 2
if m2 == 0: m2 = 3

ułamek1 = Fraction(l1, m1)
ułamek2 = Fraction(l2, m2)


# Funkcja pomocnicza ułamka w LaTeX
def latex_frac(l, m):
    return f"\\frac{{{l}}}{{{m}}}"


if typ_zadania == "Mnożenie: Ułamek × Liczba":
    pytanie_tekst = f"Ile to jest: $${latex_frac(l1, m1)} \\times {liczba_calkowita}$$"
    poprawny_wynik = ułamek1 * liczba_calkowita

    wyjasnienie = f"""
    **Krok po kroku:**
    1. Aby pomnożyć ułamek przez liczbę, pomnóż licznik tego ułamka przez tę liczbę, a mianownik pozostaw bez zmian:
    $$\\frac{{{l1} \\times {liczba_calkowita}}}{{{m1}}} = \\frac{{{l1 * liczba_calkowita}}}{{{m1}}}$$
    2. Wynik w najprostszej postaci (po skróceniu i ewentualnym wyciągnięciu całości) to: **{poprawny_wynik}**
    """

elif typ_zadania == "Mnożenie: Ułamek × Ułamek":
    pytanie_tekst = f"Ile to jest: $${latex_frac(l1, m1)} \\times {latex_frac(l2, m2)}$$"
    poprawny_wynik = ułamek1 * ułamek2

    wyjasnienie = f"""
    **Krok po kroku:**
    1. Pomnóż licznik przez licznik, a mianownik przez mianownik:
    $$\\frac{{{l1} \\times {l2}}}{{{m1} \\times {m2}}} = \\frac{{{l1 * l2}}}{{{m1 * m2}}}$$
    2. Wynik w najprostszej postaci to: **{poprawny_wynik}**
    *(Wskazówka: Przed pomnożeniem warto sprawdzić, czy da się zastosować skracanie na krzyż!)*
    """

elif typ_zadania == "Dzielenie: Ułamek ÷ Liczba":
    pytanie_tekst = f"Ile to jest: $${latex_frac(l1, m1)} \\div {liczba_calkowita}$$"
    poprawny_wynik = ułamek1 / liczba_calkowita

    wyjasnienie = f"""
    **Krok po kroku:**
    1. Dzielenie przez liczbę to mnożenie przez jej odwrotność. Odwrotność liczby ${liczba_calkowita}$ to $\\frac{{1}}{{{liczba_calkowita}}}$.
    2. Zamień dzielenie na mnożenie:
    $$\\frac{{{l1}}}{{{m1}}} \\times \\frac{{1}}{{{liczba_calkowita}}} = \\frac{{{l1} \\times 1}}{{{m1} \\times {liczba_calkowita}}} = \\frac{{{l1}}}{{{m1 * liczba_calkowita}}}$$
    3. Wynik w najprostszej postaci to: **{poprawny_wynik}**
    """

else:  # Dzielenie: Ułamek ÷ Ułamek
    pytanie_tekst = f"Ile to jest: $${latex_frac(l1, m1)} \\div {latex_frac(l2, m2)}$$"
    poprawny_wynik = ułamek1 / ułamek2

    wyjasnienie = f"""
    **Krok po kroku:**
    1. Dzielenie ułamków to mnożenie pierwszego ułamka przez odwrotność drugiego.
    2. Znajdź odwrotność drugiego ułamka: $\\frac{{{l2}}}{{{m2}}} \\rightarrow \\frac{{{m2}}}{{{l2}}}$
    3. Zamień działanie na mnożenie:
    $$\\frac{{{l1}}}{{{m1}}} \\times \\frac{{{m2}}}{{{l2}}} = \\frac{{{l1} \\times {m2}}}{{{m1} \\times {l2}}}$$
    4. Wynik w najprostszej postaci to: **{poprawny_wynik}**
    *(Wskazówka: Przed pomnożeniem warto sprawdzić, czy da się zastosować skracanie na krzyż!)*
    """
# Wyświetlenie zadania
st.markdown(pytanie_tekst)

# Formularz odpowiedzi
col1, col2 = st.columns(2)
with col1:
    user_l = st.number_input("Wpisz LICZNIK wyniku:", step=1, value=1)
with col2:
    user_m = st.number_input("Wpisz MIANOWNIK wyniku (jeśli wynik to liczba całkowita, wpisz mianownik 1):", step=1,
                             value=1)

# Sprawdzenie wyniku
if st.button("Sprawdź odpowiedź"):
    try:
        user_wynik = Fraction(int(user_l), int(user_m))
        if user_wynik == poprawny_wynik:
            st.success("🎉 Doskonale! To poprawna odpowiedź!")
        else:
            st.error(f"❌ Niestety to nie to. Twój ułamek to {user_wynik}, a poprawny wynik to {poprawny_wynik}.")
    except ZeroDivisionError:
        st.error("Mianownik nie może być równy 0!")

# Przycisk pokazujący rozwiązanie krok po kroku
if st.checkbox("Pokaż wyjaśnienie krok po kroku"):
    st.info(wyjasnienie)

# Przycisk nowego zadania
if st.button("Następne zadanie ➡️"):
    st.session_state.random_seed = random.randint(1, 100000)
    st.rerun()

# STOPKA
st.divider()
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")
