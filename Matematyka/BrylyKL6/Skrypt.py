import streamlit as st
import random
import numpy as np
import plotly.graph_objects as object_3d
from streamlit_drawable_canvas import st_canvas

# --- KONFIGURACJA STRONY ---
st.set_page_config(
    page_title="Matma3D: Bryły Klasa 6", page_icon="📐", layout="wide"
)

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
          
# 1. Funkcja do rysowania prostopadłościanu 3D
def rysuj_prostopadloscian(a, b, c):
    x = [0, a, a, 0, 0, a, a, 0]
    y = [0, 0, b, b, 0, 0, b, b]
    z = [0, 0, 0, 0, c, c, c, c]

    krawedzie = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
    ]

    fig = object_3d.Figure()
    for k in krawedzie:
        fig.add_trace(object_3d.Scatter3d(
            x=[x[k[0]], x[k[1]]], y=[y[k[0]], y[k[1]]], z=[z[k[0]], z[k[1]]],
            mode='lines', line=dict(color='#FF4B4B', width=5), showlegend=False
        ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(title='Długość (a)', range=[-1, max(a, b, c) + 2]),
            yaxis=dict(title='Szerokość (b)', range=[-1, max(a, b, c) + 2]),
            zaxis=dict(title='Wysokość (c)', range=[-1, max(a, b, c) + 2]),
            aspectmode='cube'
        ),
        margin=dict(r=0, l=0, b=0, t=0), height=400
    )
    return fig


# 2. Funkcja do rysowania ogólnego graniastosłupa n-kątnego
def rysuj_graniastoslup_n(n, h=5, promien=3):
    katy = np.linspace(0, 2 * np.pi, n, endpoint=False)

    # Współrzędne podstawy dolnej (z=0) i górnej (z=h)
    x_dol = promien * np.cos(katy)
    y_dol = promien * np.sin(katy)
    z_dol = np.zeros(n)

    x_gora = promien * np.cos(katy)
    y_gora = promien * np.sin(katy)
    z_gora = np.ones(n) * h

    fig = object_3d.Figure()

    # Krawędzie podstaw dolnej i górnej oraz krawędzie boczne
    for i in range(n):
        nastepny = (i + 1) % n
        # Podstawa dolna
        fig.add_trace(object_3d.Scatter3d(x=[x_dol[i], x_dol[nastepny]], y=[y_dol[i], y_dol[nastepny]],
                                          z=[z_dol[i], z_dol[nastepny]], mode='lines',
                                          line=dict(color='#0068C9', width=4), showlegend=False))
        # Podstawa górna
        fig.add_trace(object_3d.Scatter3d(x=[x_gora[i], x_gora[nastepny]], y=[y_gora[i], y_gora[nastepny]],
                                          z=[z_gora[i], z_gora[nastepny]], mode='lines',
                                          line=dict(color='#0068C9', width=4), showlegend=False))
        # Krawędź boczna
        fig.add_trace(
            object_3d.Scatter3d(x=[x_dol[i], x_gora[i]], y=[y_dol[i], y_gora[i]], z=[z_dol[i], z_gora[i]], mode='lines',
                                line=dict(color='#29B09D', width=4), showlegend=False))

    fig.update_layout(
        scene=dict(
            xaxis=dict(title='X', range=[-promien - 1, promien + 1]),
            yaxis=dict(title='Y', range=[-promien - 1, promien + 1]),
            zaxis=dict(title='Wysokość (H)', range=[-1, h + 2]),
            aspectmode='data'
        ),
        margin=dict(r=0, l=0, b=0, t=0), height=450
    )
    return fig


# Inicjalizacja punktów w session_state
if "punkty" not in st.session_state:
    st.session_state.punkty = 0
if "streak" not in st.session_state:
    st.session_state.streak = 0

with st.sidebar:
    st.header("🤖 Panel Sterowania")
    dzial = st.selectbox("Wybierz dział matematyki:", ["1. Prostopadłościany", "2. Graniastosłupy (Dowolna podstawa)"])

    st.write("---")
    st.subheader("🏆 Twoje Statystyki:")
    col_p1, col_p2 = st.columns(2)
    col_p1.metric("Punkty", st.session_state.punkty)
    col_p2.metric("Seria 🔥", st.session_state.streak)

    if st.button("Zresetuj punkty 🔄"):
        st.session_state.punkty = 0
        st.session_state.streak = 0
        st.rerun()

with st.sidebar:
    wyswietl_sekcje_wsparcia()

#  📝 MULTI-BRUDNOPIS W SIDEBARZE (TEKST + RYSOWANIE)
st.sidebar.markdown("---")
st.sidebar.header("📝 Brudnopis Ucznia")

# Tworzymy dwie niezależne zakładki w pasku bocznym
zakladka_rysuj, zakladka_pisz = st.sidebar.tabs(["🎨 Rysuj", "✍️ Pisz"])

with zakladka_rysuj:
    st.caption("Rysuj myszką lub palcem. Kliknij ikonę kosza pod tablicą, aby wyczyścić.")
    from streamlit_drawable_canvas import st_canvas

    # Rysownica w sidebarze działa stabilnie, bo nie blokuje jej główny formularz
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

    
# --- GŁÓWNA TREŚĆ ---
st.title("🚀 Wizualne Bryły 3D dla Klasy 6")

# --- DZIAŁ 1: PROSTOPADŁOŚCIANY ---

if dzial == "1. Prostopadłościany":
    karta_nauka, karta_quiz = st.tabs(["📚 Nauka krok po kroku", "🎯 Trening (Quiz)"])

    with karta_nauka:
        st.header("Konstrukcja Prostopadłościanu")
        col_lewa, col_prawa = st.columns([1, 1])

        with col_lewa:
            st.subheader("🎛️ Zmień wymiary pudełka:")
            a = st.slider("Długość (a) [cm]:", 1, 10, 5)
            b = st.slider("Szerokość (b) [cm]:", 1, 10, 3)
            c = st.slider("Wysokość (c) [cm]:", 1, 10, 4)

            pole = 2 * (a * b + b * c + a * c)
            objetosc = a * b * c

            st.markdown(f"""
            ### 📊 Wyniki obliczeń:
            * **Pole powierzchni całkowitej ($P_c=2 \\cdot (a \\cdot b + b \\cdot c + a \\cdot c)$):** `{pole}` cm²
            * **Objętość ($V=a \\cdot b \\cdot c$):** `{objetosc}` cm³
            """)

        with col_prawa:
            st.subheader("📦 Model 3D (Złap i obróć myszką!)")
            st.plotly_chart(rysuj_prostopadloscian(a, b, c), use_container_width=True)

    with karta_quiz:
        st.header("🎯 Quiz z Prostopadłościanów")
        if "b_typ" not in st.session_state:
            st.session_state.b_typ = random.choice(["wierzcholki", "pole", "objetosc"])
            st.session_state.b_a = random.randint(2, 6)
            st.session_state.b_b = random.randint(2, 5)
            st.session_state.b_c = random.randint(3, 7)
            st.session_state.b_pytanie_idx = random.randint(0, 2)

        col_q1, col_q2 = st.columns(2)
        with col_q1:
            if st.session_state.b_typ == "wierzcholki":
                pytania = [
                    ("Ile wierzchołków (rogów) ma każdy prostopadłościan?", 8),
                    ("Ile ścian ma sześcian?", 6),
                    ("Ile krawędzi (patyczków) ma prostopadłościan?", 12),
                ]
                pytanie, poprawna = pytania[st.session_state.b_pytanie_idx]
                st.markdown(f"### ❓ Pytanie:\n**{pytanie}**")
                ans = st.number_input("Twoja odpowiedź:", min_value=0, step=1, key="ans_w")
            else:
                tryb_nazwa = "Pole Całkowite ($P_c$)" if st.session_state.b_typ == "pole" else "Objętość ($V$)"
                st.markdown(f"### ❓ Zadanie:\nOblicz **{tryb_nazwa}** bryły o wymiarach:")
                st.code(f"a = {st.session_state.b_a} cm\nb = {st.session_state.b_b} cm\nc = {st.session_state.b_c} cm")
                ans = st.number_input("Wpisz swój wynik:", min_value=0, step=1, key="ans_math")

                if st.session_state.b_typ == "pole":
                    poprawna = 2 * (
                                st.session_state.b_a * st.session_state.b_b + st.session_state.b_b * st.session_state.b_c + st.session_state.b_a * st.session_state.b_c)
                else:
                    poprawna = st.session_state.b_a * st.session_state.b_b * st.session_state.b_c

            if st.button("🚀 Sprawdź odpowiedź", use_container_width=True):
                if ans == poprawna:
                    st.balloons()
                    st.success("🎉 Świetnie! Prawidłowa odpowiedź! +10 punktów")
                    st.session_state.punkty += 10
                    st.session_state.streak += 1
                else:
                    st.error(f"❌ Niestety to błąd. Prawidłowy wynik to: {poprawna}")
                    st.session_state.streak = 0
                

        with col_q2:
            if st.session_state.b_typ != "wierzcholki":
                st.write("📐 Podgląd proporcji bryły z zadania:")
                st.plotly_chart(
                    rysuj_prostopadloscian(st.session_state.b_a, st.session_state.b_b, st.session_state.b_c),
                    use_container_width=True)

        if st.button("Następne zadanie ➡️", key="next_b", use_container_width=True):
            del st.session_state.b_typ
            st.rerun()

# --- DZIAŁ 2: GRANIASTOSŁUPY O DOWOLNEJ PODSTAWIE ---
elif dzial == "2. Graniastosłupy (Dowolna podstawa)":
    karta_g_nauka, karta_g_quiz = st.tabs(["📚 Magiczny Generator Brył", "🎯 Wyzwanie Mistrza Krawędzi"])

    with karta_g_nauka:
        st.header("Konstruktor Graniastosłupów Prostych")
        st.write("Wybierz wielokąt, który będzie na dole bryły (w podstawie) i zobacz, jak zmienia się cała figura!")

        col_g1, col_g2 = st.columns([1, 1])

        with col_g1:
            opcje_podstaw = {
                "Trójkąt (3-kąt)": 3, "Czworokąt (4-kat)": 4, "Pięciokąt (5-kąt)": 5,
                "Sześciokąt (6-kąt)": 6, "Ośmiokąt (8-kąt)": 8, "Dziesięciokąt (10-kąt)": 10
            }
            wybrana_nazwa = st.selectbox("📐 Jaka figura ma być podstawą?", list(opcje_podstaw.keys()), index=2)
            n = opcje_podstaw[wybrana_nazwa]
            wysokosc = st.slider("📏 Wysokość graniastosłupa (H):", 2, 10, 6)

            # Wzory z klasy 6 szkoły podstawowej
            liczba_wierzcholkow = 2 * n
            liczba_krawedzi = 3 * n
            liczba_scian = n + 2

            st.subheader("💡 Sekretne wzory 6-klasisty dla tej bryły:")
            st.success(f"**Liczba wierzchołków:** $2 \\cdot n = 2 \\cdot {n} =$ **{liczba_wierzcholkow}**")
            st.info(f"**Liczba krawędzi:** $3 \\cdot n = 3 \\cdot {n} =$ **{liczba_krawedzi}**")
            st.warning(
                f"**Liczba ścian całkowitych:** $n + 2 = {n} + 2 =$ **{liczba_scian}** (w tym 2 podstawy i {n} ścian bocznych)")

        with col_g2:
            st.subheader(f"📦 Model 3D: Graniastosłup {wybrana_nazwa.split()[0].lower()}")
            st.plotly_chart(rysuj_graniastoslup_n(n, h=wysokosc), use_container_width=True)

    with karta_g_quiz:
        st.header("🎯 Quiz z Prostopadłościanów")

        # Inicjalizacja stanu zadania quizowego
        if "b_typ" not in st.session_state:
            st.session_state.b_typ = random.choice(["wierzcholki", "pole", "objetosc"])
            st.session_state.b_a = random.randint(2, 6)
            st.session_state.b_b = random.randint(2, 5)
            st.session_state.b_c = random.randint(3, 7)
            st.session_state.b_pytanie_idx = random.randint(0, 2)

        # Inicjalizacja stanu sprawdzania odpowiedzi
        if "b_sprawdzone" not in st.session_state:
            st.session_state.b_sprawdzone = False
        if "b_wynik_poprawny" not in st.session_state:
            st.session_state.b_wynik_poprawny = False
        if "b_poprawna_odp" not in st.session_state:
            st.session_state.b_poprawna_odp = 0

        col_q1, col_q2 = st.columns(2)

        with col_q1:
            if st.session_state.b_typ == "wierzcholki":
                pytania = [
                    ("Ile wierzchołków (rogów) ma każdy prostopadłościan?", 8),
                    ("Ile ścian ma sześcian?", 6),
                    ("Ile krawędzi (patyczków) ma prostopadłościan?", 12),
                ]
                wybrane_pytanie = pytania[st.session_state.b_pytanie_idx]
                st.markdown(f"### ❓ Pytanie:\n**{wybrane_pytanie[0]}**")
                st.session_state.b_poprawna_odp = wybrane_pytanie[1]
                ans = st.number_input("Twoja odpowiedź:", min_value=0, step=1, key="ans_w")
            else:
                tryb_nazwa = "Pole Całkowite ($P_c$)" if st.session_state.b_typ == "pole" else "Objętość ($V$)"
                st.markdown(f"### ❓ Zadanie:\nOblicz **{tryb_nazwa}** bryły o wymiarach:")
                st.code(f"a = {st.session_state.b_a} cm\nb = {st.session_state.b_b} cm\nc = {st.session_state.b_c} cm")
                ans = st.number_input("Wpisz swój wynik:", min_value=0, step=1, key="ans_math")

                if st.session_state.b_typ == "pole":
                    st.session_state.b_poprawna_odp = 2 * (
                                st.session_state.b_a * st.session_state.b_b + st.session_state.b_b * st.session_state.b_c + st.session_state.b_a * st.session_state.b_c)
                else:
                    st.session_state.b_poprawna_odp = st.session_state.b_a * st.session_state.b_b * st.session_state.b_c

            # Przycisk sprawdzania odpowiedzi
            if st.button("🚀 Sprawdź odpowiedź", key="btn_b_check", use_container_width=True):
                st.session_state.b_sprawdzone = True
                if ans == st.session_state.b_poprawna_odp:
                    st.session_state.b_wynik_poprawny = True
                    st.session_state.punkty += 10
                    st.session_state.streak += 1
                    st.balloons()
                else:
                    st.session_state.b_wynik_poprawny = False
                    st.session_state.streak = 0
                st.rerun()

            # Trwałe wyświetlanie komunikatu o wyniku
            if st.session_state.b_sprawdzone:
                if st.session_state.b_wynik_poprawny:
                    st.success("🎉 Świetnie! Prawidłowa odpowiedź! +10 punktów")
                else:
                    st.error(f"❌ Niestety to błąd. Prawidłowy wynik to: {st.session_state.b_poprawna_odp}")

        with col_q2:
            # WYŚWIETLANIE MODELU: Pokazuje się dla zadań obliczeniowych (pole/objętość)
            if st.session_state.b_typ != "wierzcholki":
                st.write("📐 Podgląd proporcji bryły z zadania:")
                st.plotly_chart(
                    rysuj_prostopadloscian(st.session_state.b_a, st.session_state.b_b, st.session_state.b_c),
                    use_container_width=True)
            else:
                st.info(
                    "💡 W tym pytaniu musisz wykazać się wyobraźnią! Model 3D ukrył się, żeby nie podpowiadać za bardzo. 😉")

            # Przycisk przejścia do kolejnego pytania
            if st.button("Następne zadanie ➡️", key="next_b", use_container_width=True):
                # Czyszczenie stanu przed nowym zadaniem
                del st.session_state.b_typ
                if "b_poprawna_odp" in st.session_state:
                    del st.session_state.b_poprawna_odp
                st.session_state.b_sprawdzone = False
                st.session_state.b_wynik_poprawny = False
                st.rerun()
