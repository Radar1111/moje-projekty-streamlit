import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy as np
import random

# Konfiguracja strony
st.set_page_config(page_title="Stereometria Klasa 8", page_icon="📐", layout="wide")

# Styl CSS
st.markdown("""
    <style>
    .big-font { font-size:18px !important; font-weight: 500; }
    .step-box { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #4A90E2; margin-bottom: 10px; }
    .step-box-success { background-color: #f4f9f4; padding: 15px; border-radius: 10px; border-left: 5px solid #2ECC71; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("📐 Interaktywna Stereometria Klasa 8")
st.markdown(
    "Wybierz bryłę w panelu bocznym, zmieniaj wymiary i zobacz **bryłę 3D** oraz **Twierdzenie Pitagorasa** w akcji!")
st.markdown("---")


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


# Wybór bryły w sidebarze
st.sidebar.header("⚙️ Ustawienia bryły")
bryla = st.sidebar.selectbox(
    "Wybierz bryłę geometryczną:",
    ["Graniastosłup czworokątny", "Walec", "Ostrosłup czworokątny", "Stożek"]
)

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

# Generowanie schematów 3D
def rysuj_bryle_3d(typ, a_lub_r, H, dodatkowe=None):
    fig = plt.figure(figsize=(4, 4))
    fig.patch.set_alpha(0.0)
    ax = fig.add_subplot(111, projection='3d')
    ax.patch.set_alpha(0.0)

    if typ == "Graniastosłup czworokątny":
        # Wierzchołki dolnej i górnej podstawy
        x = [0, a_lub_r, a_lub_r, 0, 0]
        y = [0, 0, a_lub_r, a_lub_r, 0]

        # Margines
        offset = 0.1 * a_lub_r

        # Dolna podst
        # Linie WIDOCZNE
        ax.plot(x[0:3], y[0:3], [0, 0, 0], color="#2C3E50", linewidth=2)
        # Linie NIEWIDOCZNE
        ax.plot(x[2:5], y[2:5], [0, 0, 0], color="#2C3E50", linewidth=2, linestyle="--")

        # Górna podst
        ax.plot(x, y, [H, H, H, H, H], color="#2C3E50", linewidth=2)

        # Krawędzie boczne w pionie
        for i in range(4):
            if i == 3:
                ax.plot([x[i], x[i]], [y[i], y[i]], [0, H], color="#2C3E50", linewidth=2, linestyle="--")
            else:
                ax.plot([x[i], x[i]], [y[i], y[i]], [0, H], color="#2C3E50", linewidth=2)

        # Podpis krawędzi
        # Podstawa 'a'
        ax.text(a_lub_r / 2, -offset, -offset, "a", color="#2C3E50", fontsize=12, fontweight="bold", ha="center")

        # Drugi podpis 'a'
        ax.text(a_lub_r + offset, a_lub_r / 2, -offset, "a", color="#2C3E50", fontsize=12, fontweight="bold",
                ha="center")

        # Podpis wysokości 'H'
        ax.text(a_lub_r + offset, -offset, H / 2, "H", color="#2C3E50", fontsize=12, fontweight="bold", va="center")

    elif typ == "Walec":
        theta = np.linspace(0, 2 * np.pi, 50)
        x = a_lub_r * np.cos(theta)
        y = a_lub_r * np.sin(theta)

        # Dolna i górna podstawa
        ax.plot(x, y, 0, color="#2C3E50", linewidth=2)
        ax.plot(x, y, H, color="#2C3E50", linewidth=2)

        # Linie boczne skrajne
        ax.plot([a_lub_r, a_lub_r], [0, 0], [0, H], color="#2C3E50", linewidth=2)
        ax.plot([-a_lub_r, -a_lub_r], [0, 0], [0, H], color="#2C3E50", linewidth=2)

        # Linia promienia i podpisy

        # Linia promienia (r) na dolnej podstawie
        ax.plot([0, a_lub_r], [0, 0], [0, 0], color="#E74C3C", linestyle="--", linewidth=1.5)

        # Podpis promienia r
        ax.text(a_lub_r / 2, 0.1 * a_lub_r, 0, "$r$", color="#E74C3C", fontsize=12, ha='center')

        # Podpis wysokości H

        ax.text(a_lub_r * 1.1, 0, H / 2, "$H$", color="#2C3E50", fontsize=12, va='center')

    elif typ == "Ostrosłup czworokątny":
        # Podstawa
        x = [-a_lub_r / 2, a_lub_r / 2, a_lub_r / 2, -a_lub_r / 2, -a_lub_r / 2]
        y = [-a_lub_r / 2, -a_lub_r / 2, a_lub_r / 2, a_lub_r / 2, -a_lub_r / 2]
        z = [0, 0, 0, 0, 0]
        ax.plot(x, y, z, color="#2C3E50", linewidth=2)

        # Krawędzie boczne
        for i in range(4):
            ax.plot([x[i], 0], [y[i], 0], [0, H], color="#2C3E50", linewidth=2)

        # Trójkąt Pitagorasa (H, a/2, h_b)
        # Odcinek od środka podstawy do środka boku
        ax.plot([0, a_lub_r / 2], [0, 0], [0, 0], color="#27AE60", linewidth=3, label="a/2")

        # Wysokość bryły H
        ax.plot([0, 0], [0, 0], [0, H], color="#E74C3C", linewidth=3, label="H")

        # 3. Wysokość ściany bocznej h_b: od wierzchołka  do środka boku

        ax.plot([0, a_lub_r / 2], [0, 0], [H, 0], color="#2980B9", linewidth=3, label="h_b")

        # Podpisy
        # Podpis wysokości bryły H
        ax.text(-0.05 * a_lub_r, 0, H / 2, "$H$", color="#E74C3C", fontsize=12, ha='right', va='center')

        # Podpis wysokości ściany bocznej h_b

        ax.text(a_lub_r / 4, 0.05 * a_lub_r, H / 2, "$h_b$", color="#2980B9", fontsize=12, ha='center', va='bottom')

    elif typ == "Stożek":
        theta = np.linspace(0, 2 * np.pi, 50)
        x = a_lub_r * np.cos(theta)
        y = a_lub_r * np.sin(theta)
        ax.plot(x, y, 0, color="#2C3E50", linewidth=2)

        # Tworzące stożka (skrajne krawędzie)
        ax.plot([a_lub_r, 0], [0, 0], [0, H], color="#2C3E50", linewidth=2)
        ax.plot([-a_lub_r, 0], [0, 0], [0, H], color="#2C3E50", linewidth=2)

        # Linia promienia, wysokości i tworzącej

        # 1. Wysokość stożka H
        ax.plot([0, 0], [0, 0], [0, H], color="#E74C3C", linestyle="--", linewidth=2)

        # 2. Promień podstawy r
        ax.plot([0, a_lub_r], [0, 0], [0, 0], color="#27AE60", linestyle="--", linewidth=2)

        # Podpisy
        # Podpis promienia r
        ax.text(a_lub_r / 2, 0.1 * a_lub_r, 0, "$r$", color="#27AE60", fontsize=12, ha='center')

        # Podpis wysokości H
        ax.text(-0.05 * a_lub_r, 0, H / 2, "$H$", color="#E74C3C", fontsize=12, ha='right', va='center')

        # Podpis tworzącej l
        ax.text(a_lub_r / 2, 0.05 * a_lub_r, H / 2, "$l$", color="#2C3E50", fontsize=12, ha='center', va='bottom')

        # ZAZNACZENIE TRÓJKĄTA PITAGORASA (H, r, l)
        ax.plot([0, a_lub_r], [0, 0], [0, 0], color="#27AE60", linewidth=3, label="r")  # Promień podstawy
        ax.plot([0, 0], [0, 0], [0, H], color="#E74C3C", linewidth=3, label="H")  # Wysokość stożka
        ax.plot([0, a_lub_r], [0, 0], [H, 0], color="#2980B9", linewidth=3, label="l")  # Tworząca

    ax.axis('off')

    ax.set_box_aspect([1, 1, 1])
    st.pyplot(fig, clear_figure=True)


# Funkcja pomocnicza do rysowania płaskiego trójkąta Pitagorasa
def rysuj_trojkat_pitagorasa(pion, poziom, przeciwprostokatna, etykieta_pion, etykieta_poziom, etykieta_skos):
    plt.rcParams['font.family'] = 'sans-serif'
    fig, ax = plt.subplots(figsize=(4.5, 3.5))
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)

    x = [0, poziom, 0, 0]
    y = [0, 0, pion, 0]

    ax.plot(x, y, color="#2C3E50", linewidth=3, zorder=2)
    ax.fill(x, y, color="#4A90E2", alpha=0.15, zorder=1)

    ax.text(-poziom * 0.08, pion / 2, f"{etykieta_pion}\n({pion:.1f})", va='center', ha='right', color="#E74C3C",
            fontsize=11, fontweight='bold')
    ax.text(poziom / 2, -pion * 0.08, f"{etykieta_poziom}\n({poziom:.1f})", va='top', ha='center', color="#27AE60",
            fontsize=11, fontweight='bold')
    ax.text(poziom / 2 + poziom * 0.05, pion / 2 + pion * 0.05, f"{etykieta_skos}\n({przeciwprostokatna:.1f})",
            va='bottom', ha='left', color="#2980B9", fontsize=11, fontweight='bold')

    kwadrat_x = [0, poziom * 0.06, poziom * 0.06, 0]
    kwadrat_y = [pion * 0.06, pion * 0.06, 0, 0]
    ax.plot(kwadrat_x[:3], kwadrat_y[:3], color="#7F8C8D", linewidth=1.5)
    ax.scatter([poziom * 0.025], [pion * 0.025], color="#7F8C8D", s=15)

    ax.set_xlim(-poziom * 0.2, poziom * 1.3)
    ax.set_ylim(-pion * 0.2, pion * 1.3)
    ax.axis('off')
    st.pyplot(fig, clear_figure=True)


#  GRANIASTOSŁUP
if bryla == "Graniastosłup czworokątny":
    st.subheader("🧱 Graniastosłup prawidłowy czworokątny")

    col_input, col_space, col_output = st.columns([1.5, 0.2, 2])

    with col_input:
        st.markdown("### 🎛️ Wymiary i Podgląd 3D")
        a = st.slider("Krawędź podstawy (a):", min_value=1.0, max_value=20.0, value=5.0, step=0.5)
        H = st.slider("Wysokość graniastosłupa (H):", min_value=1.0, max_value=30.0, value=10.0, step=0.5)
        rysuj_bryle_3d("Graniastosłup czworokątny", a, H)

    P_p = a ** 2
    P_b = 4 * a * H
    P_c = 2 * P_p + P_b
    V = P_p * H

    with col_output:
        st.markdown("### 🏆 Główne wyniki")
        c1, c2 = st.columns(2)
        c1.metric(label="Pole całkowite (Pc)", value=f"{P_c:.2f}")
        c2.metric(label="Objętość (V)", value=f"{V:.2f}")

        st.markdown("### 📝 Obliczenia krok po kroku")
        with st.container(border=True):
            st.markdown("**1. Pole podstawy (kwadrat):**")
            st.latex(f"P_p = a^2 = {a}^2 = {P_p:.2f}")
            st.markdown("---")

            st.markdown("**2. Pole powierzchni bocznej (4 prostokąty):**")
            st.latex(f"P_b = 4 \\cdot a \\cdot H = 4 \\cdot {a} \\cdot {H} = {P_b:.2f}")

# WALEC
elif bryla == "Walec":
    st.subheader("🛢️ Walec (bryła obrotowa)")

    col_input, col_space, col_output = st.columns([1.5, 0.2, 2])

    with col_input:
        st.markdown("### 🎛️ Wymiary i Podgląd 3D")
        r = st.slider("Promień podstawy (r):", min_value=1.0, max_value=20.0, value=4.0, step=0.5)
        H = st.slider("Wysokość walca (H):", min_value=1.0, max_value=30.0, value=12.0, step=0.5)
        dokladne_pi = st.checkbox("Użyj dokładnego symbolu π zamiast 3.14", value=True)
        rysuj_bryle_3d("Walec", r, H)

    P_p = math.pi * (r ** 2)
    P_b = 2 * math.pi * r * H
    P_c = 2 * P_p + P_b
    V = P_p * H

    with col_output:
        st.markdown("### 🏆 Główne wyniki")
        c1, c2 = st.columns(2)
        c1.metric(label="Pole całkowite (Pc)", value=f"{P_c:.2f}")
        c2.metric(label="Objętość (V)", value=f"{V:.2f}")

        st.markdown("### 📝 Obliczenia krok po kroku")
        with st.container(border=True):
            if dokladne_pi:
                st.markdown("**1. Pole podstawy (koło):**")
                st.latex(f"P_p = \\pi \\cdot r^2 = {r ** 2:.2f}\\pi \\approx {P_p:.2f}")

                st.markdown("---")  # Delikatna linia oddzielająca kroki

                st.markdown("**2. Pole powierzchni bocznej:**")
                st.latex(
                    f"P_b = 2\\pi r H = 2 \\cdot \\pi \\cdot {r} \\cdot {H} = {2 * r * H:.2f}\\pi \\approx {P_b:.2f}")
            else:
                pi_aprox = 3.14
                Pp_ap = pi_aprox * (r ** 2)
                Pb_ap = 2 * pi_aprox * r * H

                st.markdown("**1. Pole podstawy ($\\pi \\approx 3.14$):**")
                st.latex(f"P_p \\approx 3.14 \\cdot {r}^2 = {Pp_ap:.2f}")

                st.markdown("---")

                st.markdown("**2. Pole powierzchni bocznej:**")
                st.latex(f"P_b \\approx 2 \\cdot 3.14 \\cdot {r} \\cdot {H} = {Pb_ap:.2f}")

# OSTROSŁUP
elif bryla == "Ostrosłup czworokątny":
    st.subheader("📐 Ostrosłup prawidłowy czworokątny")

    col_input, col_space, col_output = st.columns([1.5, 0.2, 2])

    polowa_a = 0.0
    h_b = 0.0

    with col_input:
        st.markdown("### 🎛️ Wymiary i Lokalizacja trójkąta w 3D")
        a = st.slider("Krawędź podstawy (a):", min_value=1.0, max_value=20.0, value=6.0, step=0.5)
        H = st.slider("Wysokość ostrosłupa (H):", min_value=1.0, max_value=30.0, value=4.0, step=0.5)

        polowa_a = a / 2
        h_b = math.sqrt(H ** 2 + polowa_a ** 2)

        # Wyświetlenie bryły z zaznaczonym środkiem
        rysuj_bryle_3d("Ostrosłup czworokątny", a, H)

        st.markdown("### 🎯 Krok 0: Wycięty trójkąt Pitagorasa")
        rysuj_trojkat_pitagorasa(H, polowa_a, h_b, "H", "a/2", "h_b")

    P_p = a ** 2
    P_b = 4 * (0.5 * a * h_b)
    P_c = P_p + P_b
    V = (1 / 3) * P_p * H

    with col_output:
        st.markdown("### 🏆 Główne wyniki")
        c1, c2 = st.columns(2)
        c1.metric(label="Pole całkowite (Pc)", value=f"{P_c:.2f}")
        c2.metric(label="Objętość (V)", value=f"{V:.2f}")

        st.markdown("### 📝 Obliczenia krok po kroku")
        with st.container(border=True):
            st.markdown("**🎯 Krok 0: Wynik z Twierdzenia Pitagorasa:**")
            st.latex(
                f"H^2 + (\\frac{{a}}{{2}})^2 = h_b^2 \\implies {H}^2 + {polowa_a}^2 = h_b^2 \\implies h_b \\approx {h_b:.2f}")

            st.markdown("---")  # Delikatna linia oddzielająca kroki

            st.markdown("**1. Pole podstawy (kwadrat):**")
            st.latex(f"P_p = a^2 = {a}^2 = {P_p:.2f}")

            st.markdown("---")

            st.markdown("**2. Pole powierzchni bocznej (4 trójkąty):**")
            st.latex(
                f"P_b = 4 \\cdot (\\frac{{1}}{{2}} \\cdot a \\cdot h_b) = 4 \\cdot (\\frac{{1}}{{2}} \\cdot {a} \\cdot {h_b:.2f}) \\approx {P_b:.2f}")

            st.markdown("---")

            st.markdown("**3. Pole powierzchni całkowitej:**")
            st.latex(f"P_c = P_p + P_b = {P_p:.2f} + {P_b:.2f} = {P_c:.2f}")

            st.markdown("---")

            st.markdown("**4. Objętość ostrosłupa:**")
            st.latex(
                f"V = \\frac{{1}}{{3}} \\cdot P_p \\cdot H = \\frac{{1}}{{3}} \\cdot {P_p:.2f} \\cdot {H} \\approx {V:.2f}")

# STOŻEK
elif bryla == "Stożek":
    st.subheader("🍦 Stożek (bryła obrotowa)")

    col_input, col_space, col_output = st.columns([1.5, 0.2, 2])

    with col_input:
        st.markdown("### 🎛️ Wymiary i Lokalizacja trójkąta w 3D")
        r = st.slider("Promień podstawy (r):", min_value=1.0, max_value=20.0, value=3.0, step=0.5)
        H = st.slider("Wysokość stożka (H):", min_value=1.0, max_value=30.0, value=4.0, step=0.5)
        dokladne_pi = st.checkbox("Użyj dokładnego symbolu π zamiast 3.14", value=True, key="cone_pi")

        l = math.sqrt(r ** 2 + H ** 2)
        rysuj_bryle_3d("Stożek", r, H)

        st.markdown("### 🎯 Krok 0: Wycięty trójkąt Pitagorasa")
        rysuj_trojkat_pitagorasa(H, r, l, "H", "r", "l")


    P_p = math.pi * (r ** 2)
    P_b = math.pi * r * l
    P_c = P_p + P_b
    V = (1 / 3) * P_p * H

    with col_output:
        st.markdown("### 🏆 Główne wyniki")
        c1, c2 = st.columns(2)
        c1.metric(label="Pole całkowite (Pc)", value=f"{P_c:.2f}")
        c2.metric(label="Objętość (V)", value=f"{V:.2f}")

        st.markdown("### 📝 Obliczenia krok po kroku")
        with st.container(border=True):
            st.markdown("**🎯 Krok 0: Wynik z Twierdzenia Pitagorasa:**")
            st.latex(f"H^2 + r^2 = l^2 \\implies {H}^2 + {r}^2 = l^2 \\implies l \\approx {l:.2f}")

            st.markdown("---")

            if dokladne_pi:
                st.markdown("**1. Pole podstawy (koło):**")
                st.latex(f"P_p = \\pi \\cdot r^2 = {r ** 2:.2f}\\pi \\approx {P_p:.2f}")

                st.markdown("---")

                st.markdown("**2. Pole powierzchni bocznej:**")
                st.latex(
                    f"P_b = \\pi \\cdot r \\cdot l = \\pi \\cdot {r} \\cdot {l:.2f} = {r * l:.2f}\\pi \\approx {P_b:.2f}")

                st.markdown("---")

                st.markdown("**3. Pole powierzchni całkowitej:**")
                st.latex(
                    f"P_c = P_p + P_b = {r ** 2:.2f}\\pi + {r * l:.2f}\\pi = {r ** 2 + r * l:.2f}\\pi \\approx {P_c:.2f}")

                st.markdown("---")

                st.markdown("**4. Objętość stożka:**")
                st.latex(
                    f"V = \\frac{{1}}{{3}} \\cdot P_p \\cdot H = \\frac{{1}}{{3}} \\cdot {r ** 2:.2f}\\pi \\cdot {H} \\approx {V:.2f}")
            else:
                pi_aprox = 3.14
                Pp_ap = pi_aprox * (r ** 2)
                Pb_ap = pi_aprox * r * l
                Pc_ap = Pp_ap + Pb_ap
                V_ap = (1 / 3) * Pp_ap * H

                st.markdown("**1. Pole podstawy ($\\pi \\approx 3.14$):**")
                st.latex(f"P_p \\approx 3.14 \\cdot {r}^2 = {Pp_ap:.2f}")

                st.markdown("---")

                st.markdown("**2. Pole powierzchni bocznej:**")
                st.latex(f"P_b \\approx 3.14 \\cdot {r} \\cdot {l:.2f} = {Pb_ap:.2f}")

                st.markdown("---")

                st.markdown("**3. Pole powierzchni całkowitej:**")
                st.latex(f"P_c = P_p + P_b \\approx {Pp_ap:.2f} + {Pb_ap:.2f} = {Pc_ap:.2f}")

                st.markdown("---")

                st.markdown("**4. Objętość stożka:**")
                st.latex(f"V \\approx \\frac{{1}}{{3}} \\cdot {Pp_ap:.2f} \\cdot {H} = {V_ap:.2f}")


