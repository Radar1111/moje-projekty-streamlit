import streamlit as st
import random
import math


# Funkcje pomocnicze
def rozklad_na_czynniki(n):
    czynniki = []
    d = 2
    while d * d <= n:
        while (n % d) == 0:
            czynniki.append(d)
            n //= d
        d += 1
    if n > 1:
        czynniki.append(n)
    return czynniki


def nwd(a, b):
    return math.gcd(a, b)


def nww(a, b):
    return abs(a * b) // math.gcd(a, b)

def wyswietl_sekcje_wsparcia():
    if "parent_verified" not in st.session_state:
        st.session_state.parent_verified = False
    if "num1" not in st.session_state:
        st.session_state.num1 = random.randint(5, 15)
    if "num2" not in st.session_state:
        st.session_state.num2 = random.randint(5, 15)

    LINK_DO_KAWY = "https://buycoffee.to"

    st.divider()

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

# Konfiguracja strony
st.set_page_config(page_title="Trener Matematyczny - NWD, NWW i Czynniki Pierwsze", page_icon="🔢", layout="centered")
st.title("🔢 Matematyczny Trener!")
st.write("Wybierz sekcję z menu po lewej stronie, aby rozpocząć naukę lub ćwiczenia.")

# Menu boczne
opcja = st.sidebar.radio(
    "Wybierz tryb:",
    ["Nauka i Kalkulator Krok po Kroku", "Interaktywny Quiz (Ćwiczenia)"]
)

with st.sidebar:
    wyswietl_sekcje_wsparcia()

# 1: NAUKA I KALKULATOR
if opcja == "Nauka i Kalkulator Krok po Kroku":
    st.header("📚 Tryb Nauki & Kalkulator")
    temat = st.selectbox("Wybierz temat do nauki:", ["Rozkład na czynniki pierwsze", "NWD i NWW"])

    if temat == "Rozkład na czynniki pierwsze":
        st.subheader("Formularz rozkładu na czynniki pierwsze")
        st.write(
            "Każdą liczbę złożoną możemy zapisać jako iloczyn liczb premierszych (np. $12 = 2 \\cdot 2 \\cdot 3$).")
        liczba = st.number_input("Wpisz liczbę do rozłożenia (np. 12, 60, 120):", min_value=2, max_value=10000,
                                 value=60, step=1)

        if st.button("Rozłóż liczbę"):
            wyniki = rozklad_na_czynniki(liczba)
            wynik_str = " · ".join(map(str, wyniki))
            st.success(f"**Wynik:** Rozkład liczby **{liczba}** to: **{wynik_str}**")

            st.write("**Jak to dzieliliśmy krok po kroku:**")
            temp = liczba
            for c in wyniki:
                st.write(f"{temp} : {c} = {temp // c}")
                temp //= c

    elif temat == "NWD i NWW":
        st.subheader("Największy Wspólny Dzielnik (NWD) i Najmniejsza Wspólna Wielokrotność (NWW)")
        st.info(
            "💡 **NWD** to największa liczba, przez którą dzielą się obie liczby bez reszty.\n\n💡 **NWW** to najmniejsza liczba, która jest jednocześnie wielokrotnością obu liczb.")

        col1, col2 = st.columns(2)
        with col1:
            l1 = st.number_input("Pierwsza liczba:", min_value=1, max_value=1000, value=12, step=1)
        with col2:
            l2 = st.number_input("Druga liczba:", min_value=1, max_value=1000, value=18, step=1)

        if st.button("Oblicz NWD i NWW"):
            wynik_nwd = nwd(l1, l2)
            wynik_nww = nww(l1, l2)
            st.success(f"**NWD({l1}, {l2})** = **{wynik_nwd}**")
            st.success(f"**NWW({l1}, {l2})** = **{wynik_nww}**")

            st.write("---")
            st.subheader("🧠 Wyjaśnienie metodą czynników pierwszych:")

            czynniki_l1 = rozklad_na_czynniki(l1)
            czynniki_l2 = rozklad_na_czynniki(l2)
            st.write(f"🔹 Rozkład liczby **{l1}**: `{', '.join(map(str, czynniki_l1))}`")
            st.write(f"🔹 Rozkład liczby **{l2}**: `{', '.join(map(str, czynniki_l2))}`")

            wspolne_czynniki = []
            kopia_czynniki_l2 = czynniki_l2.copy()
            for c in czynniki_l1:
                if c in kopia_czynniki_l2:
                    wspolne_czynniki.append(c)
                    kopia_czynniki_l2.remove(c)

            st.write("### 🟥 Jak obliczyliśmy NWD?")
            if wspolne_czynniki:
                wspolne_str = " · ".join(map(str, wspolne_czynniki))
                st.write(
                    f"Wybieramy czynniki, które **powtarzają się w obu rozkładach** (część wspólna): **{wspolne_czynniki}**")
                st.info(f"**NWD** = {wspolne_str} = **{wynik_nwd}**")
            else:
                st.info(f"Liczby nie mają wspólnych czynników pierwszych oprócz 1. **NWD** = **1**")

            st.write("### 🟩 Jak obliczyliśmy NWW?")
            brakujace_czynniki = kopia_czynniki_l2
            caly_rozklad_nww = czynniki_l1 + brakujace_czynniki
            nww_str = " · ".join(map(str, caly_rozklad_nww))
            st.write(
                f"Bierzemy **cały rozkład pierwszej liczby** `{czynniki_l1}` i dorzucamy z drugiej to, czego **brakuje** `{brakujace_czynniki}`.")
            st.write(f"Wszystkie czynniki dla NWW: **{caly_rozklad_nww}**")
            st.info(f"**NWW** = {nww_str} = **{wynik_nww}**")

# 2: QUIZ
elif opcja == "Interaktywny Quiz (Ćwiczenia)":
    st.header("🎯 Interaktywny Quiz")

    if 'streak' not in st.session_state:
        st.session_state.streak = 0
    if 'poprzednia_odpowiedz' not in st.session_state:
        st.session_state.poprzednia_odpowiedz = None

    if st.session_state.streak > 0:
        st.markdown(f"### 🔥 Twoja seria poprawnych odpowiedzi: **{st.session_state.streak}**")
    else:
        st.markdown("### 🎯 Zacznij swoją serię poprawnych odpowiedzi!")

    if 'typ_zadania' not in st.session_state:
        st.session_state.typ_zadania = random.choice(["czynniki", "nwd", "nww"])
        st.session_state.liczba1 = random.randint(12, 60)
        st.session_state.liczba2 = random.randint(8, 40)
        st.session_state.odpowiedziane = False


    def nowe_zadanie():
        st.session_state.typ_zadania = random.choice(["czynniki", "nwd", "nww"])
        st.session_state.liczba1 = random.randint(12, 60)
        st.session_state.liczba2 = random.randint(8, 40)
        st.session_state.odpowiedziane = False
        st.session_state.poprzednia_odpowiedz = None
        st.rerun()


    # Stabilność renderowania danych
    with st.form(key="quiz_form"):
        if st.session_state.typ_zadania == "czynniki":
            st.subheader(f"Zadanie: Rozłóż liczbę **{st.session_state.liczba1}** na czynniki pierwsze.")
            st.write("Wpisz czynniki oddzielone przecinkami (np. dla 12 wpisz: *2,2,3*):")
            user_input = st.text_input("Twoja odpowiedź:", key="quiz_czynniki")

        elif st.session_state.typ_zadania == "nwd":
            st.subheader(
                f"Zadanie: Znajdź NWD dla liczb **{st.session_state.liczba1}** i **{st.session_state.liczba2}**.")
            user_ans = st.number_input("Wpisz NWD:", min_value=1, step=1, key="quiz_nwd")

        elif st.session_state.typ_zadania == "nww":
            st.subheader(
                f"Zadanie: Znajdź NWW dla liczb **{st.session_state.liczba1}** i **{st.session_state.liczba2}**.")
            user_ans = st.number_input("Wpisz NWW:", min_value=1, step=1, key="quiz_nww")

        submit_button = st.form_submit_button(label="Sprawdź odpowiedź")

    # Przetwarzanie odpowiedzi PO wysłaniu formularza
    if submit_button:
        st.session_state.odpowiedziane = True

        if st.session_state.typ_zadania == "czynniki":
            prawidlowe = rozklad_na_czynniki(st.session_state.liczba1)
            try:
                user_list = sorted([int(x.strip()) for x in user_input.split(",") if x.strip()])
                if user_list == sorted(prawidlowe):
                    st.session_state.streak += 1
                    st.session_state.poprzednia_odpowiedz = "poprawna"
                else:
                    st.session_state.streak = 0
                    st.session_state.poprzednia_odpowiedz = "bledna"
            except ValueError:
                st.session_state.poprzednia_odpowiedz = "blad_formatu"

        elif st.session_state.typ_zadania == "nwd":
            poprawne_nwd = nwd(st.session_state.liczba1, st.session_state.liczba2)
            if user_ans == poprawne_nwd:
                st.session_state.streak += 1
                st.session_state.poprzednia_odpowiedz = "poprawna"
            else:
                st.session_state.streak = 0
                st.session_state.poprzednia_odpowiedz = "bledna"

        elif st.session_state.typ_zadania == "nww":
            poprawne_nww = nww(st.session_state.liczba1, st.session_state.liczba2)
            if user_ans == poprawne_nww:
                st.session_state.streak += 1
                st.session_state.poprzednia_odpowiedz = "poprawna"
            else:
                st.session_state.streak = 0
                st.session_state.poprzednia_odpowiedz = "bledna"

    # Wyświetlanie rezultatów i feedbacku edukacyjnego (Zawsze widoczne po sprawdzeniu)
    if st.session_state.odpowiedziane:
        if st.session_state.poprzednia_odpowiedz == "poprawna":
            st.balloons()
            st.success(f"Brawo! Doskonała odpowiedź! 🎉 Aktualna seria: {st.session_state.streak}")
        elif st.session_state.poprzednia_odpowiedz == "bledna":
            st.error("Niestety to nie tym razem. Zobacz wyjaśnienie poniżej, aby dowiedzieć się jak to obliczyć!")
        elif st.session_state.poprzednia_odpowiedz == "blad_formatu":
            st.warning("Upewnij się, że wpisujesz tylko liczby oddzielone przecinkami!")

        # Blok edukacyjny zawsze niezależnie od poprawności wyniku
        st.write("---")
        st.write("### 🧠 Wyjaśnienie matematyczne krok po kroku:")
        c1 = rozklad_na_czynniki(st.session_state.liczba1)

        if st.session_state.typ_zadania == "czynniki":
            prawidlowe = rozklad_na_czynniki(st.session_state.liczba1)
            st.info(f"Prawidłowy rozkład liczby {st.session_state.liczba1} to: **{', '.join(map(str, prawidlowe))}**")

        elif st.session_state.typ_zadania == "nwd":
            poprawne_nwd = nwd(st.session_state.liczba1, st.session_state.liczba2)
            c2 = rozklad_na_czynniki(st.session_state.liczba2)
            wspolne = []
            c2_kopia = c2.copy()
            for c in c1:
                if c in c2_kopia:
                    wspolne.append(c)
                    c2_kopia.remove(c)
            st.write(f"1. Rozkład liczby **{st.session_state.liczba1}** to: `{c1}`")
            st.write(f"2. Rozkład liczby {st.session_state.liczba2} to: {c2}")
            if wspolne:
                st.info(
                f"Część wspólna obu rozkładów to: {wspolne}. Po pomnożeniu otrzymujemy: {' · '.join(map(str, wspolne))} = {poprawne_nwd}.")
            else:
                st.info("Te liczby nie mają wspólnych czynników pierwszych. Ich NWD wynosi 1.")


        elif st.session_state.typ_zadania == "nww":

            poprawne_nww = nww(st.session_state.liczba1, st.session_state.liczba2)

            c2 = rozklad_na_czynniki(st.session_state.liczba2)

            c2_kopia = c2.copy()

            for c in c1:

                if c in c2_kopia:
                    c2_kopia.remove(c)

            cale_nww = c1 + c2_kopia

            st.write(f"1. Rozkład liczby **{st.session_state.liczba1}** to: `{c1}`")

            st.write(
                f"2. Z rozkładu liczby **{st.session_state.liczba2}** (`{c2}`) bierzemy tylko brakujące czynniki: `{c2_kopia}`")

            st.info(f"Mnożymy wszystko razem: **{cale_nww}**. Wynik końcowy NWW = **{poprawne_nww}**.")

        # Przycisk przejścia dalej
        st.write("")
        if st.button("Następne zadanie ➡️"):
            nowe_zadanie()
