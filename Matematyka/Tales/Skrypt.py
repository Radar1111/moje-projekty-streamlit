import streamlit as st
import matplotlib.pyplot as plt
import random


# Konfiguracja strony

st.set_page_config(page_title="Twierdzenie Talesa", page_icon="📐", layout="centered")

st.title("📐 Interaktywne Twierdzenie Talesa")
st.write("Wybierz układ prostych i zmieniaj wymiary suwakami, aby zobaczyć stałość proporcji!")


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

# PANEL BOCZNY
tryb_aplikacji = st.sidebar.radio("Wybierz sekcję:", ["📖 Wizualizacje i Teoria", "📝 Sekcja zadań"])


# Teoria

if tryb_aplikacji == "📖 Wizualizacje i Teoria":
    uklad = st.sidebar.selectbox("Wybierz układ prostych:", ["Klasyczny kąt", "Klepsydra (Motylek)"])

    st.info("💡 **Trzy złote zasady na klasówkę:**")
    st.markdown("- **1. Zawsze sprawdzaj, czy linie są równoległe** – bez tego Tales nie działa (w zadaniach szukaj sformułowania typu $AB \\parallel CD$).")
    st.markdown("- **2. Porównuj ze sobą te same strony / proste** – w ułamkach zestawiaj ze sobą odcinki leżące na tej samej linii lub odpowiadające sobie boki trójkątów.")
    st.markdown("- **3. Uważaj na układ klepsydry** – linie krzyżują się w środku, więc odcinek z góry przechodzi po skosie na dół na tej samej prostej!")

    if uklad == "Klasyczny kąt":
        st.header("📐 Układ standardowy (Ramiona kąta)")

        a = st.slider("Odcinek górny lewy (a):", min_value=1.0, max_value=10.0, value=3.0, step=0.5)
        b = st.slider("Odcinek dolny lewy (b):", min_value=1.0, max_value=10.0, value=5.0, step=0.5)
        c = 4.0
        x = (b * c) / a

        fig, ax = plt.subplots(figsize=(7, 4.5))
        stala_skosu_gora = 0.6
        stala_skosu_dol = 0.2
        x_1, x_2 = a, a + b

        ax.plot([0, x_2 + 2], [0, (x_2 + 2) * stala_skosu_gora], color="black", linewidth=2.5)
        ax.plot([0, x_2 + 2], [0, (x_2 + 2) * stala_skosu_dol], color="black", linewidth=2.5)
        ax.plot([x_1, x_1], [x_1 * stala_skosu_dol, x_1 * stala_skosu_gora], color="#E63946", linestyle="--", linewidth=2)
        ax.plot([x_2, x_2], [x_2 * stala_skosu_dol, x_2 * stala_skosu_gora], color="#1D3557", linestyle="--", linewidth=2)

        ax.text(x_1 / 2, (x_1 / 2) * stala_skosu_gora + 0.4, f"a = {a:.1f}", color="#E63946", fontsize=11, fontweight="bold", ha='center')
        ax.text(x_1 + b / 2, (x_1 + b / 2) * stala_skosu_gora + 0.4, f"b = {b:.1f}", color="#1D3557", fontsize=11, fontweight="bold", ha='center')
        ax.text(x_1 / 2, (x_1 / 2) * stala_skosu_dol - 0.4, f"c = {c:.1f}", color="#E63946", fontsize=11, fontweight="bold", ha='center')
        ax.text(x_1 + b / 2, (x_1 + b / 2) * stala_skosu_dol - 0.4, f"x = {x:.2f}", color="#1D3557", fontsize=11, fontweight="bold", ha='center')

        ax.set_xlim(-1, x_2 + 3)
        ax.set_ylim(-1, (x_2 + 3) * stala_skosu_gora)
        ax.axis("off")
        st.pyplot(fig)

        st.subheader("📊 Sprawdźmy proporcje na żywo:")
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Stosunek odcinków po lewej (a / b)", value=f"{a / b:.2f}")
        with col2:
            st.metric(label="Stosunek odcinków po prawej (c / x)", value=f"{c / x:.2f}")

    elif uklad == "Klepsydra (Motylek)":
        st.header("⏳ Układ klepsydry (Proste przecinające się)")
        st.write("W tym układzie proste krzyżują się w jednym punkcie (środku). Podstawy trójkątów są równoległe.")

        a = st.slider("Górny odcinek pierwszej prostej (a):", min_value=1.0, max_value=10.0, value=3.0, step=0.5)
        b = st.slider("Dolny odcinek pierwszej prostej (b):", min_value=1.0, max_value=10.0, value=5.0, step=0.5)
        c = 4.0
        x = (b * c) / a

        fig, ax = plt.subplots(figsize=(7, 5))

        ax.plot([-a, b], [a * 0.8, -b * 0.8], color="black", linewidth=2.5)
        ax.plot([c, -x], [c * 0.8, -x * 0.8], color="black", linewidth=2.5)
        ax.plot([-a, c], [a * 0.8, c * 0.8], color="#E63946", linestyle="--", linewidth=2)
        ax.plot([b, -x], [-b * 0.8, -x * 0.8], color="#1D3557", linestyle="--", linewidth=2)

        ax.plot(0, 0, 'ko', markersize=6)
        ax.text(0, 0.3, "Środek", fontsize=10, ha='center', fontweight='bold')

        ax.text(-a / 2 - 0.4, (a * 0.8) / 2, f"a = {a:.1f}", color="#E63946", fontsize=11, fontweight="bold", ha='center')
        ax.text(b / 2 + 0.4, (-b * 0.8) / 2, f"b = {b:.1f}", color="#1D3557", fontsize=11, fontweight="bold", ha='center')
        ax.text(c / 2 + 0.4, (c * 0.8) / 2, f"c = {c:.1f}", color="#E63946", fontsize=11, fontweight="bold", ha='center')
        ax.text(-x / 2 - 0.4, (-x * 0.8) / 2, f"x = {x:.2f}", color="#1D3557", fontsize=11, fontweight="bold", ha='center')

        max_val = max(a, b, c, x) + 1
        ax.set_xlim(-max_val, max_val)
        ax.set_ylim(-max_val * 0.8, max_val * 0.8)
        ax.axis("off")
        st.pyplot(fig)

        st.subheader("📊 Sprawdźmy proporcje dla klepsydry:")
        st.write("W klepsydrze dzielimy odcinki należące do **tej samej prostej** przechodzącej przez środek:")

        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Stosunek na pierwszej prostej (a / b)", value=f"{a / b:.2f}")
        with col2:
            st.metric(label="Stosunek na drugiej prostej (c / x)", value=f"{c / x:.2f}")

    st.success("💡 **Wniosek:** Dokładnie tak jak w poprzednim układzie – ułamki dają identyczny wynik! Proporcja została idealnie zachowana.")
    st.subheader("Wyjaśnienie matematyczne: Proporcje:")
    st.info(f"$$\\frac{{a}}{{b}} = \\frac{{{a}}}{{{b}}} = {a/b:.2f}$$")
    st.info(f"$$\\frac{{c}}{{x}} = \\frac{{{c}}}{{{x:.2f}}} = {c/x:.2f}$$")


#  Zadania

elif tryb_aplikacji == "📝 Sekcja zadań":
    st.header("🎯 Trening czyni mistrza!")
    st.write("Wybierz typ zadania, oblicz niewiadomą $x$ na kartce, wpisz wynik z dokładnością do dwóch miejsc po przecinku i sprawdź poprawność!")

    typ_zadania = st.selectbox("Wybierz rodzaj zadania do wygenerowania:", ["Zadanie z x-em (Kąt)", "Zadanie z trapezem", "Zadanie z motylkiem"])

    def losuj_zadanie():
        st.session_state.zad_a = float(random.randint(2, 8))
        st.session_state.zad_b = float(random.randint(3, 9))
        st.session_state.zad_c = float(random.randint(2, 6))
        if st.session_state.zad_a == st.session_state.zad_c:
            st.session_state.zad_c += 1

    if "aktualny_typ" not in st.session_state or st.session_state.aktualny_typ != typ_zadania:
        st.session_state.aktualny_typ = typ_zadania
        losuj_zadanie()

    if st.button("🔄 Wylosuj nowe liczby do zadania"):
        losuj_zadanie()

    za = st.session_state.zad_a
    zb = st.session_state.zad_b
    zc = st.session_state.zad_c

    prawidlowy_x = round((zb * zc) / za, 2)
    fig, ax = plt.subplots(figsize=(6, 4))

    if typ_zadania == "Zadanie z x-em (Kąt)":
        st.write("### 📝 Treść: Wyznacz długość odcinka $x$, wiedząc że czerwona i niebieska prosta są równoległe.")
        st.latex(f"\\frac{{{za:.0f}}}{{{zb:.0f}}} = \\frac{{{zc:.0f}}}{{x}}")

        stala_skosu_gora, stala_skosu_dol = 0.6, 0.2
        x_1, x_2 = za, za + zb
        ax.plot([0, x_2 + 2], [0, (x_2 + 2) * stala_skosu_gora], color="black", linewidth=2)
        ax.plot([0, x_2 + 2], [0, (x_2 + 2) * stala_skosu_dol], color="black", linewidth=2)
        ax.plot([x_1, x_1], [x_1 * stala_skosu_dol, x_1 * stala_skosu_gora], color="red", linestyle="--")
        ax.plot([x_2, x_2], [x_2 * stala_skosu_dol, x_2 * stala_skosu_gora], color="blue", linestyle="--")

        ax.text(x_1 / 2, (x_1 / 2) * stala_skosu_gora + 0.3, f"{za:.0f}", color="black", fontsize=12, fontweight="bold")
        ax.text(x_1 + zb / 2, (x_1 + zb / 2) * stala_skosu_gora + 0.3, f"{zb:.0f}", color="black", fontsize=12,
                fontweight="bold")
        ax.text(x_1 / 2, (x_1 / 2) * stala_skosu_dol - 0.4, f"{zc:.0f}", color="black", fontsize=12, fontweight="bold")
        ax.text(x_1 + zb / 2, (x_1 + zb / 2) * stala_skosu_dol - 0.4, "x = ?", color="blue", fontsize=12,
                fontweight="bold")
        ax.set_xlim(-1, x_2 + 2)
        ax.set_ylim(-1, (x_2 + 2) * stala_skosu_gora)

    elif typ_zadania == "Zadanie z trapezem":
        st.write(
            "### 📝 Treść: W trapezie poprowadzono prostą równoległą do podstaw, która podzieliła ramiona. Oblicz $x$.")
        st.latex(f"\\frac{{{za:.0f}}}{{{zb:.0f}}} = \\frac{{{zc:.0f}}}{{x}}")

        # Rysowanie trapezu z podziałem poprzecznym
        ax.plot([0, 5], [4, 4], color="black", linewidth=2)  # Górna podstawa
        ax.plot([-1, 7], [0, 0], color="black", linewidth=2)  # Dolna podstawa
        ax.plot([0, -1], [4, 0], color="black", linewidth=2)  # Lewe ramię
        ax.plot([5, 7], [4, 0], color="black", linewidth=2)  # Prawe ramię

        # Prosta równoległa w środku (na wysokości y=1.8)
        ax.plot([-0.45, 5.9], [1.8, 1.8], color="purple", linestyle="--", linewidth=2)

        # Podpisy na ramionach
        ax.text(-0.5, 3.0, f"{za:.0f}", fontsize=11, fontweight="bold")
        ax.text(-0.9, 0.8, f"{zb:.0f}", fontsize=11, fontweight="bold")
        ax.text(5.5, 3.0, f"{zc:.0f}", fontsize=11, fontweight="bold")
        ax.text(6.3, 0.8, "x = ?", color="blue", fontsize=11, fontweight="bold")
        ax.set_xlim(-2, 8)
        ax.set_ylim(-1, 5)

    elif typ_zadania == "Zadanie z motylkiem":
        st.write("### 📝 Treść: Ramiona motylka przecinają się w punkcie środkowym. Wyznacz długość boku $x$.")
        st.latex(f"\\frac{{{za:.0f}}}{{{zb:.0f}}} = \\frac{{{zc:.0f}}}{{x}}")

        ax.plot([-za, zb], [za * 0.8, -zb * 0.8], color="black", linewidth=2)
        ax.plot([zc, -prawidlowy_x], [zc * 0.8, -prawidlowy_x * 0.8], color="black", linewidth=2)
        ax.plot([-za, zc], [za * 0.8, zc * 0.8], color="red", linestyle="--")
        ax.plot([zb, -prawidlowy_x], [-zb * 0.8, -prawidlowy_x * 0.8], color="blue", linestyle="--")
        ax.plot(0, 0, 'ko')

        ax.text(-za / 2 - 0.4, (za * 0.8) / 2, f"{za:.0f}", fontsize=11, fontweight="bold")
        ax.text(zb / 2 + 0.4, (-zb * 0.8) / 2, f"{zb:.0f}", fontsize=11, fontweight="bold")
        ax.text(zc / 2 + 0.4, (zc * 0.8) / 2, f"{zc:.0f}", fontsize=11, fontweight="bold")
        ax.text(-prawidlowy_x / 2 - 0.5, (-prawidlowy_x * 0.8) / 2, "x = ?", color="blue", fontsize=11,
                fontweight="bold")

        m_val = max(za, zb, zc, 5) + 1
        ax.set_xlim(-m_val, m_val)
        ax.set_ylim(-m_val * 0.8, m_val * 0.8)

    #  WYŚWIETLANIA 
    ax.axis("off")
    st.pyplot(fig)

    odpowiedz = st.number_input("Wpisz swoją odpowiedź dla x (zaokrąglij do 2 miejsc po przecinku):", min_value=0.0,
                                step=0.01, format="%.2f")

    if st.button("✔️ Sprawdź odpowiedź"):
        if abs(odpowiedz - prawidlowy_x) < 0.02:
            st.success(
                f"🎉 Doskonale! Twoja odpowiedź to {odpowiedz}. To poprawny wynik! (Proporcja: {za:.0f}/{zb:.0f} = {zc:.0f}/{prawidlowy_x:.2f})")
        else:
            st.error(
                f"❌ Niestety to nie jest poprawny wynik. Spróbuj jeszcze raz! Pamiętaj o ułożeniu proporcji na krzyż.")

        with st.expander("👀 Zobacz rozwiązanie krok po kroku"):
            st.write("Zgodnie z Twierdzeniem Talesa układamy równanie proporcji:")
            st.latex(f"\\frac{{{za:.0f}}}{{{zb:.0f}}} = \\frac{{{zc:.0f}}}{{x}}")  # Podwójny backslash przy \\frac
            st.write("Mnożymy 'na krzyż':")
            st.latex(f"{za:.0f} \\cdot x = {zb:.0f} \\cdot {zc:.0f}")
            st.latex(f"{za:.0f}x = {zb * zc:.0f}")
            st.write("Dzielimy obustronnie przez liczbę przy $x$:")
            st.latex(f"x = \\frac{{{zb * zc:.0f}}}{{{za:.0f}}} = {prawidlowy_x:.2f}")

with st.sidebar:
    wyswietl_sekcje_wsparcia()
