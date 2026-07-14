import streamlit as st
import random


def rok_na_wiek_rzymski(rok, era):
    if rok <= 0: return "Błąd wartości", 0
    wiek = (rok - 1) // 100 + 1
    rzymskie = {
        1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI", 7: "VII", 8: "VIII", 9: "IX", 10: "X",
        11: "XI", 12: "XII", 13: "XIII", 14: "XIV", 15: "XV", 16: "XVI", 17: "XVII", 18: "XVIII",
        19: "XIX", 20: "XX", 21: "XXI"
    }
    r_wiek = rzymskie.get(wiek, str(wiek))
    str_wiek = f"{r_wiek} p.n.e." if era == "p.n.e." else f"{r_wiek} n.e."
    return str_wiek, wiek


def polowa_wieku(rok, era):
    reszta = rok % 100
    if era == "n.e.":
        if reszta == 0:
            return "II połowa"  # np. rok 200 n.e. to koniec II połowy II wieku
        return "I połowa" if reszta <= 50 else "II połowa"
    else:
        if reszta == 0:
            return "II połowa"  # np. rok 300 p.n.e. to sam początek (od tyłu) III wieku, czyli II połowa
        # W p.n.e. końcówki 01-50 to I połowa (bliżej przełomu er), a 51-100 to II połowa
        return "II połowa" if reszta <= 50 else "I połowa"


def oblicz_roznice(rok1, era1, rok2, era2):
    punkt1 = rok1 if era1 == "n.e." else -rok1
    punkt2 = rok2 if era2 == "n.e." else -rok2
    roznica = abs(punkt1 - punkt2)
    if era1 != era2:
        roznica -= 1  # Korekta o brak roku zerowego
    return roznica
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

# Inicjalizacja zmiennych sesyjnych
if 'streak' not in st.session_state:
    st.session_state.streak = 0
if 'best_streak' not in st.session_state:
    st.session_state.best_streak = 0
if 'quiz_odpowiedziano' not in st.session_state:
    st.session_state.quiz_odpowiedziano = False

st.set_page_config(page_title="Rzymski Mistrz Wieków", layout="centered")
st.title("🏛️ Mistrz Wieków Historycznych")

tryb = st.sidebar.radio("Wybierz moduł:", ["Nauka zasad", "Quiz historyczny", "Kalkulator czasu"])

with st.sidebar:
    wyswietl_sekcje_wsparcia()

if tryb == "Nauka zasad":
    st.header("Jak określamy wiek i połowę?")

    c1, c2 = st.columns(2)
    with c1:
        test_rok = st.number_input("Wpisz rok:", value=44, min_value=1, step=1)
    with c2:
        test_era = st.selectbox("Wybierz erę:", ["p.n.e.", "n.e."], index=0)

    wynik_wiek, nr_wieku = rok_na_wiek_rzymski(test_rok, test_era)
    wynik_polowa = polowa_wieku(test_rok, test_era)
    st.subheader(f"Rok {test_rok} {test_era} to: **{wynik_wiek}**, **{wynik_polowa}**")

    st.markdown("### 💡 Wyjaśnienie teorii:")

    if test_era == "n.e.":
        st.write(f"1. **Wiek:** Rok {test_rok} należy do **{nr_wieku} wieku n.e.** (wiek trwa od roku {(nr_wieku-1)*100 + 1} do {nr_wieku*100}).")
    
        if test_rok % 100 == 0:
            st.write(f"2. **Połowa:** Rok kończy się na '00', więc to dokładnie ostatni rok tego stulecia. Jest to **{wynik_polowa}**.")
        else:
            koncowka = test_rok % 100
            st.write(f"2. **Połowa:** Końcówka roku to {koncowka}. W erze n.e. lata 1–50 to I połowa, a 51–100 to II połowa. Stąd wynik: **{wynik_polowa}**.")

    else:  # p.n.e.
        st.write(f"1. **Wiek:** Rok {test_rok} p.n.e. należy do **{nr_wieku} wieku p.n.e.** (w p.n.e. czas biegnie wstecz, wiek trwa od roku {nr_wieku*100} do {(nr_wieku-1)*100 + 1} p.n.e.).")
    
        if test_rok % 100 == 0:
            st.write(f"2. **Połowa:** Rok kończy się na '00'. W erze p.n.e. oznacza to pierwszy (początkowy) rok tego stulecia. Jest to **{wynik_polowa}**.")
        else:
            koncowka = test_rok % 100
            st.write(f"2. **Połowa:** Ponieważ czas płynie wstecz, końcówki 51–99 (bliższe setki) to I połowa, a końcówki 1–50 (bliższe zera) to II połowa. Końcówka {koncowka} to **{wynik_polowa}**.")

elif tryb == "Quiz historyczny":
    st.header("Quiz: Który to wiek?")

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.metric("Aktualna seria (Streak) 🔥", st.session_state.streak)
    with col_s2:
        st.metric("Najlepszy wynik 🏆", st.session_state.best_streak)

    if 'quiz_rok' not in st.session_state:
        st.session_state.quiz_rok = random.randint(1, 2100)
        st.session_state.quiz_era = random.choice(["p.n.e.", "n.e."])
        st.session_state.quiz_odpowiedziano = False

    rok = st.session_state.quiz_rok
    era = st.session_state.quiz_era

    poprawny_wiek, _ = rok_na_wiek_rzymski(rok, era)
    poprawna_polowa = polowa_wieku(rok, era)

    st.subheader(f"Zadanie: Określ wiek dla roku: **{rok} {era}**")

    wieki_opcje = [f"{w} p.n.e." for w in
                   ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV",
                    "XVI", "XVII", "XVIII", "XIX", "XX", "XXI"]] + \
                  [f"{w} n.e." for w in
                   ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV",
                    "XVI", "XVII", "XVIII", "XIX", "XX", "XXI"]]

    if st.session_state.quiz_odpowiedziano:
        if st.session_state.quiz_odp_status == "sukces":
            st.balloons()
            st.success(f"🎉 Doskonale! Rok {rok} {era} to rzeczywiście **{poprawny_wiek}**, **{poprawna_polowa}**.")
        else:
            st.error(
                f"❌ Pomyłka! Prawidłowa odpowiedź dla roku {rok} {era} to: **{poprawny_wiek}**, **{poprawna_polowa}**.")

        if st.button("Następny rok ➡️"):
            del st.session_state.quiz_rok
            st.session_state.quiz_odpowiedziano = False
            st.rerun()
    else:
        u_wiek = st.selectbox("Wybierz wiek:", wieki_opcje)
        u_polowa = st.radio("Która to połowa?", ["I połowa", "II połowa"])

        if st.button("Sprawdź!"):
            st.session_state.quiz_odpowiedziano = True
            if u_wiek == poprawny_wiek and u_polowa == poprawna_polowa:
                st.session_state.quiz_odp_status = "sukces"
                st.session_state.streak += 1
                if st.session_state.streak > st.session_state.best_streak:
                    st.session_state.best_streak = st.session_state.streak
            else:
                st.session_state.quiz_odp_status = "blad"
                st.session_state.streak = 0
            st.rerun()

elif tryb == "Kalkulator czasu":
    st.header("Ile lat upłynęło?")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Wydarzenie A**")
        rok_a = st.number_input("Rok A:", value=753, min_value=1, key="ra")
        era_a = st.selectbox("Era A:", ["p.n.e.", "n.e."], index=0, key="ea")
    with col2:
        st.markdown("**Wydarzenie B**")
        rok_b = st.number_input("Rok B:", value=1000, min_value=1, key="rb")
        era_b = st.selectbox("Era B:", ["p.n.e.", "n.e."], index=1, key="eb")

    lata = oblicz_roznice(rok_a, era_a, rok_b, era_b)
    st.metric(label="Upłynęło łącznie:", value=f"{lata} lat(a)")

    st.markdown("### 📘 Jak to zostało obliczone?")
    if era_a == era_b:
        st.write(
            f"Oba wydarzenia miały miejsce w tej samej erze ({era_a}). Zastosowano proste odejmowanie wartości: Większa - Mniejsza.")
        st.latex(f"|{rok_a} - {rok_b}| = {lata}")
    else:
        st.write(
            "Wydarzenia miały miejsce w różnych erach. Zastosowano wzór uwzględniający **brak roku zerowego** w kalendarzu:")
        st.latex(rf"\text{{Lata}} = \text{{Rok p.n.e.}} + \text{{Rok n.e.}} - 1")
        st.write(f"Podstawiając Twoje dane: **{rok_a} + {rok_b} - 1 = {lata}**.")
        st.info(
            "ℹ️ Wyjaśnienie: Ponieważ po 1 roku p.n.e. następuje bezpośrednio 1 rok n.e., od standardowej sumy lat musimy odjąć jeden nieistniejący rok zerowy.")
# STOPKA
st.divider()
st.caption("Najcierpliwszy portal do historii - klasa 4")
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")
