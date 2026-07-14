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

def wyswietl_sekcje_wsparcia():
    # Inicjalizacja sesji wewnątrz funkcji (bezpieczne dla każdej strony)
    if "parent_verified" not in st.session_state:
        st.session_state.parent_verified = False
    if "num1" not in st.session_state:
        st.session_state.num1 = random.randint(5, 15)
    if "num2" not in st.session_state:
        st.session_state.num2 = random.randint(5, 15)

    LINK_DO_KAWY = "https://buycoffee.to/gigawiedza"

    # Separator odcinający treść edukacyjną
    st.divider()

    # Expander na dole strony
    with st.expander("👪 Dla Rodziców / Starszych Uczniów (Strefa Wspierania)"):
        if not st.session_state.parent_verified:
            st.write("Aby wejść, potwierdź że jesteś osobą dorosłą:")
            pytanie = f"Ile to jest {st.session_state.num1} + {st.session_state.num2}?"
            
            # Użycie unikalnego klucza w widgetach zapobiega konfliktom w Streamlit
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

with st.sidebar:
    wyswietl_sekcje_wsparcia()
    
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
