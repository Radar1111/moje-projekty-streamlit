import math
import matplotlib.pyplot as plt
import streamlit as st
import random

st.set_page_config(page_title="Geometria", layout="wide")
st.title("Interaktywny Pomocnik do Geometrii")

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


# Menu boczne - rozdzielono elementy w liście
opcja = st.sidebar.radio("Co chcesz robić?", ["Rysowanie figur", "Obliczanie kątów"])

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
        update_streamlit=False,  # Dla płynności rysowania (w sidebarze już nie zablokuje apki!)
        height=250,
        drawing_mode="freedraw",
        key="globalny_canvas_brudnopis",  # Jeden stały klucz, by rysunek nie znikał przy zmianie pytania
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

if opcja == "Rysowanie figur":
    figura = st.selectbox("Wybierz figurę", ["Prostokąt", "Kwadrat", "Koło"])

    col1, col2 = st.columns(2)

    with col1:
        if figura == "Prostokąt":
            a = st.number_input("Bok A", min_value=1.0, value=5.0)
            b = st.number_input("Bok B", min_value=1.0, value=3.0)
            pole = a * b
            obwod = 2 * (a + b)

            # Ściągawka ze wzorami dla ucznia
            st.warning(
                "📐 **Ściągawka ze wzorów:**\n* **Pole:** $P = a \\cdot b$\n* **Obwód:** $Obw = 2 \\cdot a + 2 \\cdot b$")

            st.success(f"**Pole:** {pole:.2f}")
            st.success(f"**Obwód:** {obwod:.2f}")

        elif figura == "Kwadrat":
            a = st.number_input("Bok A", min_value=1.0, value=4.0)
            b = a

            st.warning(
                "📐 **Ściągawka ze wzorów:**\n"
                "* **Pole:** $P = a \\cdot a = a^2$\n"
                "* **Obwód:** $Obw = 4 \\cdot a$"
            )

            st.success(f"**Pole:** {a ** 2:.2f}")
            st.success(f"**Obwód:** {4 * a:.2f}")

        elif figura == "Koło":
            a = st.number_input("Promień (r) - to odcinek, który łączy środek koła z jego brzegiem (okręgiem)", min_value=1.0, value=3.0)
            b = a


            st.warning(
                "📐 **Ściągawka ze wzorów:**\n"
                "* **Pole:** $P = \\pi \\cdot r \\cdot r = \\pi \\cdot r^2$\n"
                "* **Obwód:** $Obw = 2 \\cdot \\pi \\cdot r$\n\n"
                "*Przypomnienie dla czwartoklasisty: $\\pi$ to magiczna liczba, która wynosi około 3.14! "
                "Dlatego Twój obwód liczymy tak: $Obw = 2 \\cdot 3.14 \\cdot r$*"
            )

            st.success(f"**Pole:** {3.14 * (a ** 2):.2f}")
            st.success(f"**Obwód:** {2 * 3.14 * a:.2f}")

    with col2:
        fig, ax = plt.subplots()
        if figura in ["Prostokąt", "Kwadrat"]:
            ksztalt = plt.Rectangle(
                (0, 0), a, b, color="skyblue", ec="blue", lw=2
            )
            ax.add_patch(ksztalt)
            ax.set_xlim(-1, max(a, b) + 2)
            ax.set_ylim(-1, max(a, b) + 2)
        elif figura == "Koło":
            # Dedykowane rysowanie koła
            ksztalt = plt.Circle((0, 0), a, color="skyblue", ec="blue", lw=2)
            ax.add_patch(ksztalt)
            ax.set_xlim(-a - 1, a + 1)
            ax.set_ylim(-a - 1, a + 1)

        ax.set_aspect("equal")
        st.pyplot(fig)

elif opcja == "Obliczanie kątów":
    st.subheader("📐 Ekipa Trzech Kątów — Tajemnica 180 Stopni!")

    # Sekcja edukacyjna dla czwartoklasisty
    with st.expander("💡 Kliknij tutaj, aby dowiedzieć się, jak liczymy kąty!", expanded=True):
        st.markdown("""
        ### 🌟 Złota zasada każdego trójkąta:
        Nieważne, czy trójkąt jest malutki, wielki, chudy czy gruby — gdybyśmy odcięli wszystkie jego trzy rogi i ułożyli je obok siebie, **zawsze stworzą idealną linię prostą** (czyli kąt półpełny).

        * **Suma wszystkich trzech kątów to zawsze dokładnie 180°!**
        * Jeśli znasz dwa kąty, to trzeci znajdziesz bardzo łatwo: odejmij te dwa znane kąty od liczby 180.
        * *Przykład:* Jeśli jeden kąt ma 60°, a drugi 40° (razem 100°), to trzeci musi mieć: 180° - 100° = 80°!
        """)

    col1, col2 = st.columns(2)

    with col1:
        st.write("### 📏 Podaj boki trójkąta:")
        a = st.number_input("Bok a", min_value=0.1, value=3.0)
        b = st.number_input("Bok b", min_value=0.1, value=4.0)
        c = st.number_input("Bok c", min_value=0.1, value=5.0)

        if a + b > c and a + c > b and b + c > a:
            alpha_rad = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))
            beta_rad = math.acos((a ** 2 + c ** 2 - b ** 2) / (2 * a * c))
            gamma_rad = math.acos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b))

            alpha = math.degrees(alpha_rad)
            beta = math.degrees(beta_rad)
            gamma = math.degrees(gamma_rad)

            st.write("### 📊 Wyniki pomiarów:")
            st.success(f"**Kąt α (alfa):** {alpha:.0f}°")
            st.success(f"**Kąt β (beta):** {beta:.0f}°")
            st.success(f"**Kąt γ (gamma):** {gamma:.0f}°")

            # Zaokrąglamy do .0f
            st.info(
                f"🔍 **Sprawdźmy:** {alpha:.0f}° + {beta:.0f}° + {gamma:.0f}° = {alpha + beta + gamma:.0f}°! Widzisz? Zawsze wychodzi 180°!")

            x_c = b * math.cos(alpha_rad)
            y_c = b * math.sin(alpha_rad)
        else:
            st.error(
                "❌ Z tych boków nie da się zbudować trójkąta! Pamiętaj: suma dwóch krótszych boków musi być większa niż najdłuższy bok!")
            x_c, y_c = None, None

    with col2:
        if x_c is not None:
            fig, ax = plt.subplots()
            punkty_x = [0, c, x_c, 0]
            punkty_y = [0, 0, y_c, 0]

            ax.plot(punkty_x, punkty_y, color="blue", lw=3)
            ax.fill(punkty_x, punkty_y, color="skyblue", alpha=0.4)

            # Dodanie podpisów kątów na rysunku
            ax.text(0.3, 0.2, f"{alpha:.0f}°", fontsize=12, fontweight='bold')
            ax.text(c - 0.7, 0.2, f"{beta:.0f}°", fontsize=12, fontweight='bold')
            ax.text(x_c, y_c - 0.4, f"{gamma:.0f}°", fontsize=12, fontweight='bold')

            ax.set_xlim(-1, max(c, x_c) + 1)
            ax.set_ylim(-1, max(max(punkty_y), 1) + 1)
            ax.set_aspect("equal")
            ax.axis('off')  # Ukrywamy osie wykresu
            st.pyplot(fig)
