import streamlit as st
import sympy as sp
import random
import re



# Konfiguracja strony
st.set_page_config(page_title="Metoda Podstawiania Step-by-Step", layout="centered")

st.title("🧮 Rozwiązywanie układu równań metodą podstawiania")

def napraw_skladnie(tekst):
    """Automatycznie wstawia gwiazdki mnożenia tam, gdzie uczeń ich zapomniał."""
    tekst = tekst.strip().lower()
    # Cyfra przed literą (np. 2x -> 2*x)
    tekst = re.sub(r'(\d)([a-z])', r'\1*\2', tekst)
    # Litera przed cyfrą (np. x2 -> x*2)
    tekst = re.sub(r'([a-z])(\d)', r'\1*\2', tekst)
    # Litera obok litery (np. xy -> x*y)
    tekst = re.sub(r'([a-z])([a-z])', r'\1*\2', tekst)
    return tekst

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
                "i utrzymania portfolio bezpłatnych aplikacji."
            )



# 📝 MULTI-BRUDNOPIS W SIDEBARZE
st.sidebar.header("📝 Brudnopis Ucznia")

from streamlit_drawable_canvas import st_canvas

zakladka_rysuj, zakladka_pisz = st.sidebar.tabs(["🎨 Rysuj", "✍️ Pisz"])

with zakladka_rysuj:
    st.caption("Rysuj myszką lub palcem. Klawisz kosza czyści rysunek.")
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
        placeholder="Np. y = 5 - 2x...",
        key="brudnopis_globalny",
        height=180
    )
    st.button("Wyczyść notatnik 🧹", on_click=czysc_notatnik, use_container_width=True)




# Logika matematyczna

x, y = sp.symbols('x y')

st.write("Wpisz równania w postaci standardowej (przyrównane do zera).")
st.info("Pamiętaj o używaniu gwiazdki `*` do mnożenia, np. `2*x + y - 5` zamiast `2x`")

col1, col2 = st.columns(2)
with col1:
    eq1_input = st.text_input("Równanie 1:", "2*x + y - 5")
with col2:
    eq2_input = st.text_input("Równanie 2:", "x - 3*y - 6")

if st.button("Rozwiąż układ krok po kroku", type="primary", use_container_width=True):
    try:
        # Przetwarzamy wejście ucznia przed podaniem do SymPy
        eq1_clean = napraw_skladnie(eq1_input)
        eq2_clean = napraw_skladnie(eq2_input)

        eq1 = sp.sympify(eq1_clean)
        eq2 = sp.sympify(eq2_clean)

        st.subheader("🤖 Twój układ równań wyjściowych:")
        st.latex(r"\begin{cases} " + sp.latex(eq1) + r" = 0 \\ " + sp.latex(eq2) + r" = 0 \end{cases}")

        # Automatyczny wybór zmiennej z pierwszego równania
        dostepne_zmienne = [s for s in [x, y] if eq1.has(s)]

        if not dostepne_zmienne:
            st.error("Pierwsze równanie nie zawiera zmiennych x ani y!")
        else:
            zmienna_1 = dostepne_zmienne[0]  # Pierwsza znaleziona zmienna (np. x)
            zmienna_2 = y if zmienna_1 == x else x  # Druga zmienna (np. y)


            # KROK 1: Wyznaczenie zmiennej

            st.subheader("📝 Krok 1: Wyznaczenie zmiennej z pierwszego równania")
            sol_1 = sp.solve(eq1, zmienna_1)

            if not sol_1:
                st.error("Nie udało się wyznaczyć zmiennej z pierwszego równania.")
            else:
                expr_1 = sol_1[0]
                st.write(
                    f"Wyznaczamy zmienną ${sp.latex(zmienna_1)}$ poprzez przeniesienie reszty składników na prawą stronę:")
                st.latex(sp.latex(zmienna_1) + " = " + sp.latex(expr_1))


                # KROK 2: Podstawienie z nawiasami

                st.subheader("📝 Krok 2: Podstawienie wyrażenia do drugiego równania")
                st.write(f"W miejsce zmiennej ${sp.latex(zmienna_1)}$ wstawiamy całe wyznaczone wyrażenie w nawiasie:")

                latex_eq2 = sp.latex(eq2)
                podstawienie_latex = r"\left(" + sp.latex(expr_1) + r"\right)"

                # Podmieniamy zmienną na wersję z nawiasem
                eq2_pokazowe_latex = latex_eq2.replace(sp.latex(zmienna_1), podstawienie_latex)
                st.latex(eq2_pokazowe_latex + " = 0")


                # KROK 3: Rozwiązywanie równania z jedną zmienną

                st.subheader("📝 Krok 3: Opuszczenie nawiasów i obliczenie wartości")

                eq2_uproszczone = eq2.subs(zmienna_1, expr_1)
                st.write(
                    f"Po pomnożeniu przez nawias i zredukowaniu wyrazów podobnych otrzymujemy równanie z jedną zmienną ${sp.latex(zmienna_2)}$:")
                st.latex(sp.latex(eq2_uproszczone) + " = 0")

                # Rozwiązujemy uproszczone równanie
                sol_2 = sp.solve(eq2_uproszczone, zmienna_2)

                if not sol_2:
                    if sp.simplify(eq2_uproszczone) == 0:
                        st.warning("Układ jest nieoznaczony (nieskończenie wiele rozwiązań).")
                    else:
                        st.error("Układ jest sprzeczny (brak rozwiązań).")
                else:
                    val_2 = sol_2[0]

                    # Wizualne przeniesienie wyrazu wolnego dla lepszej widoczności
                    wyraz_wolny = eq2_uproszczone.subs(zmienna_2, 0)
                    skladnik_z_zmienna = eq2_uproszczone - wyraz_wolny

                    st.write("Przenosimy niewiadome na lewą stronę, a liczby na prawą:")
                    st.latex(sp.latex(skladnik_z_zmienna) + " = " + sp.latex(-wyraz_wolny))

                    st.write("Dzielimy obustronnie przez współczynnik i otrzymujemy:")
                    st.latex(sp.latex(zmienna_2) + " = " + sp.latex(val_2))


                    # KROK 4: Powrót do pierwszego równania

                    st.subheader("📝 Krok 4: Powrót do pierwszego wzoru")
                    st.write(
                        f"Podstawiamy obliczoną wartość ${sp.latex(zmienna_2)} = {sp.latex(val_2)}$ do wzoru z Kroku 1:")

                    latex_expr_1 = sp.latex(expr_1)
                    liczba_podstawiona_latex = r"\left(" + sp.latex(val_2) + r"\right)"
                    wzor_z_podstawieniem_latex = latex_expr_1.replace(sp.latex(zmienna_2), liczba_podstawiona_latex)

                    st.latex(sp.latex(zmienna_1) + " = " + wzor_z_podstawieniem_latex)

                    val_1 = expr_1.subs(zmienna_2, val_2)
                    st.write("Po wykonaniu działań arytmetycznych:")
                    st.latex(sp.latex(zmienna_1) + " = " + sp.latex(val_1))

                # Wynik Końcowy

                st.success("🎉 Ostateczna odpowiedź:")
                wynik_x = val_1 if zmienna_1 == x else val_2
                wynik_y = val_2 if zmienna_2 == y else val_1
                st.latex(r"\begin{cases} x = " + sp.latex(wynik_x) + r" \\ y = " + sp.latex(wynik_y) + r" \end{cases}")

    except Exception as e:
        st.error(f"Błąd obliczeń! Sprawdź czy poprawnie wpisałeś równanie. Szczegóły: {e}")

# Sekcja wsparcia
wyswietl_sekcje_wsparcia()
