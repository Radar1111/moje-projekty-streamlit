import streamlit as st
import sympy as sp
import random
import re
import math

# Konfiguracja strony Streamlit
st.set_page_config(page_title="Metoda Przeciwnych Współczynników Step-by-Step", layout="centered")

st.title("🧮 Rozwiązywanie układu równań metodą przeciwnych współczynników")

def nww(a, b):
    """Oblicz Najmniejszą Wspólną wielokrotność (NWW) dla liczb całkowitych """
    a, b = abs(int(a)), abs(int(b))
    if a == 0 or b == 0:
        return 0
    return (a * b) //math.gcd(a, b)


def wyswietl_sekcje_wsparcia():
    if "parent_verified_c" not in st.session_state:
        st.session_state.parent_verified_c = False
    if "num1_c" not in st.session_state:
        st.session_state.num1_c = random.randint(5, 15)
    if "num2_c" not in st.session_state:
        st.session_state.num2_c = random.randint(5, 15)

    LINK_DO_KAWY = "https://buycoffee.to"
    st.divider()

    with st.expander("👪 Dla Rodziców / Starszych Uczniów (Strefa Wspierania)"):
        if not st.session_state.parent_verified_c:
            st.write("Aby wejść, potwierdź że jesteś osobą dorosłą:")
            pytanie = f"Ile to jest {st.session_state.num1_c} + {st.session_state.num2_c}?"
            odpowiedz_rodzica = st.number_input(pytanie, step=1, value=0, key="footer_parent_input_c")

            if st.button("Zatwierdź", key="footer_parent_btn_c", use_container_width=True):
                poprawny_wynik = st.session_state.num1_c + st.session_state.num2_c
                if odpowiedz_rodzica == poprawny_wynik:
                    st.session_state.parent_verified_c = True
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
                """
            )
            st.link_button("☕ Postaw wirtualną kawę", LINK_DO_KAWY, type="primary", use_container_width=True)

            if st.button("Zablokuj strefę", type="secondary", use_container_width=True, key="footer_lock_btn_c"):
                st.session_state.parent_verified_c = False
                st.session_state.num1_c = random.randint(5, 15)
                st.session_state.num2_c = random.randint(5, 15)
                st.rerun()


def napraw_skladnie(tekst):
    """Automatycznie wstawia gwiazdki mnożenia."""
    tekst = tekst.strip().lower()
    if tekst.endswith("=0"):
        tekst = tekst[:-2]
    tekst = re.sub(r'(\d)([a-z])', r'\1*\2', tekst)
    tekst = re.sub(r'([a-z])(\d)', r'\1*\2', tekst)
    tekst = re.sub(r'([a-z])([a-z])', r'\1*\2', tekst)
    tekst = re.sub(r'(\d)(\()', r'\1*\2', tekst)
    tekst = re.sub(r'(\))([a-z])', r'\1*\2', tekst)
    return tekst



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
        key="canvas_przeciwne",
    )

with zakladka_pisz:
    if "brudnopis_przeciwne" not in st.session_state:
        st.session_state["brudnopis_przeciwne"] = ""


    def czysc_notatnik():
        st.session_state["brudnopis_przeciwne"] = ""


    st.text_area(
        label="Miejsce na Twoje obliczenia:",
        placeholder="Np. pomnożę pierwsze przez -2...",
        key="brudnopis_przeciwne",
        height=180
    )
    st.button("Wyczyść notatnik 🧹", on_click=czysc_notatnik, use_container_width=True)


# 🧮 GŁÓWNA LOGIKA 

x, y = sp.symbols('x y')

st.write("Wpisz równania w postaci standardowej (przyrównane do zera).")
st.info(
    "Aplikacja automatycznie dopasuje brakujące znaki mnożenia, np. `2x + 3y - 7` oznacza równanie \(2x + 3y = 7\).")

col1, col2 = st.columns(2)
with col1:
    eq1_input = st.text_input("Równanie 1:", "2x + y - 5")
with col2:
    eq2_input = st.text_input("Równanie 2:", "3x - y - 5")

if st.button("Rozwiąż układ metodą przeciwnych współczynników", type="primary", use_container_width=True):
    try:
        eq1_clean = napraw_skladnie(eq1_input)
        eq2_clean = napraw_skladnie(eq2_input)

        eq1 = sp.sympify(eq1_clean)
        eq2 = sp.sympify(eq2_clean)

        st.subheader("🤖 Twój układ równań wyjściowych:")
        st.latex(r"\begin{cases} " + sp.latex(eq1) + r" = 0 \\ " + sp.latex(eq2) + r" = 0 \end{cases}")

        # Pobieranie współczynników przy x i y dla obu równań
        a1 = eq1.coeff(x)
        b1 = eq1.coeff(y)
        c1 = eq1.subs({x: 0, y: 0})

        a2 = eq2.coeff(x)
        b2 = eq2.coeff(y)
        c2 = eq2.subs({x: 0, y: 0})

        
        # Analiza i doprowadzenie do przeciwnych współczynników
        
        st.subheader("📝 Krok 1: Szukanie przeciwnych współczynników")

        # Wskazówka dydaktyczna 
        with st.expander("💡 Wskazówka: Dlaczego najpierw usuwamy zmienną y?"):
            st.write(
                "W metodzie przeciwnych współczynników kolejność eliminacji niewiadomych **nie ma znaczenia** – "
                "zarówno usunięcie najpierw $x$, jak i $y$ doprowadzi do dokładnie tego samego wyniku. "
                "Ten program dla przejrzystości zawsze w pierwszej kolejności dąży do wyeliminowania zmiennej **$y$**."
            )

        # Sprawdzanie warunku jednoznaczności
        W = a1 * b2 - a2 * b1

        if W == 0:
            Wx = c1 * b2 - c2 * b1
            Wy = a1 * c2 - a2 * c1  
            if Wx == 0 and Wy == 0:
                st.error("Układ ma nieskończenie wiele rozwiązań (układ tożsamościowy).")
            else:
                st.error("Układ nie ma rozwiązań (układ sprzeczny).")
        else:
            st.success("Układ jest oznaczony (ma jedno rozwiązanie). Przechodzimy do obliczeń!")

            # Sprawdzamy, czy układ ma obie zmienne w obu równaniach, czy jedna już jest wyeliminowana
            if b1 != 0 and b2 != 0:
                # Eliminacja zmiennej y
                # Szukamy najmniejszej wspólnej wielokrotności (NWW) dla współczynników przy y
                nww_y = sp.lcm(abs(b1), abs(b2))

                # Obliczamy mnożniki dla obu równań
                m1 = nww_y / abs(b1)
                m2 = nww_y / abs(b2)

                # Jeśli b1 i b2 mają ten sam znak, jeden z mnożników musi być ujemny, aby współczynniki były przeciwne
                if (b1 > 0 and b2 > 0) or (b1 < 0 and b2 < 0):
                    m2 = -m2

                st.write(
                    f"Aby uzyskać przeciwne współczynniki przy $y$, mnożymy pierwsze równanie przez **{sp.latex(m1)}**, a drugie przez **{sp.latex(m2)}**.")

                eq1_nowe = sp.simplify(eq1 * m1)
                eq2_nowe = sp.simplify(eq2 * m2)

                st.latex(
                    r"\begin{cases} " + sp.latex(eq1_nowe) + r" = 0 \\ " + sp.latex(eq2_nowe) + r" = 0 \end{cases}")

                
                # Dodawanie równań stronami i wyznaczenie x
                
                st.subheader("➕ Krok 2: Dodawanie równań stronami")
                rownanie_x = sp.simplify(eq1_nowe + eq2_nowe)
                st.write("Po dodaniu obu równań stronami zmienna $y$ się redukuje i otrzymujemy:")
                st.latex(sp.latex(rownanie_x) + " = 0")

                # Rozwiązujemy równanie z jedną niewiadomą x
                rozw_x = sp.solve(rownanie_x, x)[0]
                st.latex(f"x = {sp.latex(rozw_x)}")

                
                # Podstawienie x i wyznaczenie y
                
                st.subheader("🔄 Krok 3: Obliczenie drugiej niewiadomej ($y$)")
                rownanie_y = eq1.subs(x, rozw_x)
                st.write("Podstawiamy obliczony $x$ do pierwszego równania wyjściowego:")
                st.latex(sp.latex(rownanie_y) + " = 0")

                rozw_y = sp.solve(rownanie_y, y)[0]
                st.latex(f"y = {sp.latex(rozw_y)}")

            else:
                # Przypadek szczególny, gdy w jednym z równań od razu nie ma y (np. 2x - 4 = 0)
                st.write("Jedno z równań zawiera już tylko jedną niewiadomą, więc nie trzeba mnożyć równań.")
                rozwiazanie = sp.solve([eq1, eq2], (x, y))
                rozw_x = rozwiazanie[x]
                rozw_y = rozwiazanie[y]

            
            # Podsumowanie wyniku
            
            st.subheader("✅ Ostateczne rozwiązanie układu:")
            st.success(f"Rozwiązaniem układu równań jest para liczb: **x = {rozw_x}** oraz **y = {rozw_y}**")
            st.latex(r"\begin{cases} x = " + sp.latex(rozw_x) + r" \\ y = " + sp.latex(rozw_y) + r" \end{cases}")

    except Exception as e:
        st.error(f"Błąd obliczeń! Sprawdź poprawność zapisu równania. Szczegóły: {e}")

# Wywołanie wsparcia na dole strony
wyswietl_sekcje_wsparcia()
