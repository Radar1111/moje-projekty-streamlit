import streamlit as st
import random
import math

# Wstępna konfiguracja strony
st.set_page_config(page_title="Mistrz Dziesiętnych")
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

# Menu boczne
with st.sidebar:
    st.title("Nawigacja")
    tryb = st.radio(
        "Wybierz rodzaj zadania:",
        ["Działania (+/-)", "Porównywanie (< = >)", "Zamiana ułamków"]
    )
    st.info("Pamiętaj: w Pythonie używamy (.) zamiast przecinka!")
with st.sidebar:
    wyswietl_sekcje_wsparcia()
    
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
