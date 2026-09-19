import streamlit as st
import random
from fractions import Fraction


st.set_page_config(page_title="Matematyka Klasa 6: Procenty", page_icon="🔢", layout="centered")

st.title("🔢 Mistrz Konwersji: Procenty i Ułamki")
st.write(
    "Witaj! Ta aplikacja pomoże ci opanować zamianę między procentami i ułamkami oraz wyliczanie obniżek cen towarów.")

tab1, tab2 = st.tabs(["📚 Teoria i Wyjaśnienia", "📝 Interaktywny Quiz"])


def wyswietl_sekcje_wsparcia():

    if "parent_verified" not in st.session_state:
        st.session_state.parent_verified = False
    if "num1" not in st.session_state:
        st.session_state.num1 = random.randint(5, 15)
    if "num2" not in st.session_state:
        st.session_state.num2 = random.randint(5, 15)

    LINK_DO_KAWY = "https://buycoffee.to/gigawiedza"


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

# Teoria
with tab1:
    st.header("Jak to działa? Podstawy")
    st.markdown("""
    * **Procent na ułamek dziesiętny:** Podziel przez 100. *Przykład: $50\\% = 0,5$*
    * **Procent na ułamek zwykły:** Zapisz z mianownikiem 100 i skróć. *Przykład: $25\\% = \\frac{25}{100}= \\frac{1}{4}$*
    * **Ułamek dziesiętny na procent:** Pomnóż przez 100 i dopisz %. *Przykład: $0,75 \\cdot 100 = 75\\%$*
    * **Ułamek zwykły na procent:** Rozszerz mianownik do 10 lub 100. *Przykład: $\\frac{3}{4}= \\frac{75}{100}= 75\\%$*
    """)

    st.header("🛒 Jak liczyć obniżki cen?")

    st.subheader("1. Pojedyncza obniżka")
    st.markdown("""
    Wyobraź sobie, że bluza kosztuje **100 zł** i zostaje obniżona o **20%**.
    * Najpierw oblicz, ile wynosi obniżka: $20\\% \\text{ z } 100\\text{ zł} = \\frac{20}{100} \\cdot 100=0,20 \\cdot 100 = 20\\text{ zł}$.
    * Teraz odejmij obniżkę od starej ceny: $100\\text{ zł} - 20\\text{ zł} = \\mathbf{80\\text{ zł}}$.
    """)

    st.subheader("2. Haczyk: Dwukrotna obniżka (Zadanie dla mistrzów!)")
    st.info("⚠️ PAMIĘTAJ: Procentów z dwóch kolejnych obniżek NIE MOŻNA do siebie dodawać!")
    st.markdown("""
    Zobacz na przykładzie butów za **100 zł**. Najpierw obniżamy je o **20%**, a potem o **10%**.
    * **Krok 1 (Pierwsza obniżka):** Buty po obniżce o 20% kosztują **80 zł** (tak jak w przykładzie powyżej).
    * **Krok 2 (Druga obniżka):** Teraz obniżamy cenę o 10%, ale **liczymy to z nowej ceny (80 zł)**, a nie ze starej!
      $10\\% \\text{ z } 80\\text{ zł} = 0,10 \\cdot 80 = 8\\text{ zł}$.
    * **Krok 3 (Cena końcowa):** Odejmujemy: $80\\text{ zł} - 8\\text{ zł} = \\mathbf{72\\text{ zł}}$.

    **Ile łącznie procent zaoszczędziliśmy?**
    Początkowa cena to 100 zł, końcowa to 72 zł. Zyskaliśmy 28 zł, czyli łączna obniżka to **28%** (a nie 30%!). Druga obniżka „urwała” mniej, bo kwota była już mniejsza.
    """)

    st.subheader("🔢 Interaktywny Symulator Konwersji")
    procent = st.slider("Wybierz procent, aby zobaczyć jego ułamki:", min_value=1, max_value=100, value=50)

    dziesiętny = procent / 100
    ułamek_zwykł = Fraction(procent, 100)

    col1, col2, col3 = st.columns(3)
    col1.metric("Procent", f"{procent}%")
    col2.metric("Ułamek dziesiętny", f"{dziesiętny}")
    col3.metric("Ułamek zwykły", f"{ułamek_zwykł.numerator}/{ułamek_zwykł.denominator}")

# Quiz
with tab2:
    st.header("Sprawdź swoją wiedzę!")


    pula_liczby = [10, 20, 25, 40, 50, 75, 90]
    pula_ceny = [60, 80, 100, 120, 150, 200, 300]
    pula_procent_obnizek = [10, 20, 25, 30, 50]


    if 'punkty' not in st.session_state: st.session_state.punkty = 0
    if 'proby' not in st.session_state: st.session_state.proby = 0
    if 'feedback' not in st.session_state: st.session_state.feedback = None
    if 'quiz_typ' not in st.session_state:
        st.session_state.quiz_typ = random.choice(['p_na_d', 'p_na_z', 'd_na_p', 'obnizka_cena', 'obnizka_laczna'])
        st.session_state.liczba = random.choice(pula_liczby)
        st.session_state.cena_start = random.choice(pula_ceny)
        st.session_state.procent1 = random.choice(pula_procent_obnizek)
        st.session_state.procent2 = random.choice(pula_procent_obnizek)
        st.session_state.odpowiedziano = False

    st.sidebar.metric("Twój Wynik", f"{st.session_state.punkty} pkt", f"Próby: {st.session_state.proby}")

    # 📝 MULTI-BRUDNOPIS W SIDEBARZE (TEKST + RYSOWANIE)
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
    with st.sidebar:
        wyswietl_sekcje_wsparcia()


    def nowe_pytanie():
        st.session_state.quiz_typ = random.choice(['p_na_d', 'p_na_z', 'd_na_p', 'obnizka_cena', 'obnizka_laczna'])
        st.session_state.liczba = random.choice(pula_liczby)
        st.session_state.cena_start = random.choice(pula_ceny)
        st.session_state.procent1 = random.choice(pula_procent_obnizek)
        st.session_state.procent2 = random.choice(pula_procent_obnizek)
        st.session_state.odpowiedziano = False


    # GENEROWANIE Pytań
    if st.session_state.quiz_typ == 'p_na_d':
        st.markdown(f"### Zamień **{st.session_state.liczba}%** na ułamek dziesiętny.")
        odp_user = st.number_input("Wpisz wynik (np. 0.5):", min_value=0.0, max_value=1.0, step=0.01, format="%.2f")
        poprawna_odp = round(st.session_state.liczba / 100, 2)
        komunikat_bledu = f"Poprawna odpowiedź to: {poprawna_odp}"

    elif st.session_state.quiz_typ == 'p_na_z':
        st.markdown(f"### Zmień **{st.session_state.liczba}%** na ułamek zwykły (skrócony).")
        col_l, col_m = st.columns(2)
        with col_l:
            l = st.number_input("Licznik:", min_value=1, step=1)
        with col_m:
            m = st.number_input("Mianownik:", min_value=1, step=1)
        u = Fraction(st.session_state.liczba, 100)
        poprawna_odp, odp_user = (u.numerator, u.denominator), (l, m)
        komunikat_bledu = f"Poprawna odpowiedź to: {u.numerator}/{u.denominator}"

    elif st.session_state.quiz_typ == 'd_na_p':
        st.markdown(f"### Zamień ułamek **{st.session_state.liczba / 100}** na procenty.")
        odp_user = st.number_input("Wpisz samą liczbę (bez %):", min_value=0, max_value=100, step=1)
        poprawna_odp = st.session_state.liczba
        komunikat_bledu = f"Poprawna odpowiedź to: {poprawna_odp}%"

    elif st.session_state.quiz_typ == 'obnizka_cena':
        cena = st.session_state.cena_start
        proc = st.session_state.procent1
        st.markdown(
            f"### 🧥 Zadanie tekstowe\nKurtka zimowa kosztowała **{cena} zł**. Obniżono jej cenę o **{proc}%**. Ile kosztuje kurtka teraz?")
        odp_user = st.number_input("Wpisz nową cenę w zł:", min_value=0.0, step=0.5, format="%.2f")
        poprawna_odp = round(cena * (1 - proc / 100), 2)
        komunikat_bledu = f"Poprawna odpowiedź to: {poprawna_odp} zł"

    elif st.session_state.quiz_typ == 'obnizka_laczna':
        p1 = st.session_state.procent1
        p2 = st.session_state.procent2
        st.markdown(
            f"### 🏷️ Zadanie dla mistrzów!\nCenę butów obniżono najpierw o **{p1}%**, a po miesiącu nową cenę obniżono powtórnie o kolejne **{p2}%**. O ile **łącznie procent** obniżono początkową cenę butów?")
        odp_user = st.number_input("Wpisz łączny procent obniżki (sama liczba bez %):", min_value=0.0, max_value=100.0,
                                   step=0.1, format="%.1f")

        pozostala_wartosc = (1 - p1 / 100) * (1 - p2 / 100)
        poprawna_odp = round((1 - pozostala_wartosc) * 100, 1)
        komunikat_bledu = f"Poprawna odpowiedź to: {poprawna_odp}%.\n\n*Podpowiedź jak to policzyć:* Gdyby buty kosztowały 100 zł, po pierwszej obniżce kosztowałyby {round(100 - p1, 1)} zł. Druga obniżka ({p2}%) z tej nowej kwoty to {round((100 - p1) * (p2 / 100), 1)} zł. Po odjęciu obu obniżek zostaje {round(100 * pozostala_wartosc, 1)} zł. Łączny spadek ceny ze 100 zł to właśnie {poprawna_odp}%!"

    # PRZYCISKI
    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        if st.button("Sprawdź odpowiedź", disabled=st.session_state.odpowiedziano):
            st.session_state.proby += 1
            st.session_state.odpowiedziano = True

            if odp_user == poprawna_odp:
                st.session_state.punkty += 1
                st.session_state.feedback = {"type": "success", "text": "🎉 Doskonale! To poprawna odpowiedź."}
            else:
                st.session_state.feedback = {"type": "error", "text": f"❌ Niestety to błąd. {komunikat_bledu}"}
            st.rerun()

    with col_btn2:
        if st.button("Następne pytanie"):
            nowe_pytanie()
            st.session_state.feedback = None
            st.rerun()

    # WYŚWIETLANIE PO ODŚWIEŻENIU STRONY
    feedback = st.session_state.get("feedback")

    if feedback:
        if feedback["type"] == "success":
            st.success(feedback["text"])
        elif feedback["type"] == "error":
            st.error(feedback["text"])

# --- STOPKA ---
st.divider()
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")
