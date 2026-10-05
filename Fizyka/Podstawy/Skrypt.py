import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Konfiguracja strony
st.set_page_config(page_title="Fizyka dla Siódmoklasisty", layout="wide", page_icon="🧪")

# Główny tytuł
st.title("🚀 Witaj w świecie Fizyki! (Klasa 7)")
st.markdown("---")

# Tworzenie zakładek dla kolejnych tematów
tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 1. Po co nam fizyka?",
    "🧊 2. Stany skupienia",
    "⚖️ 3. Gęstość, masa i objętość",
    "🎮 4. Sprawdź swoją wiedzę (Quiz)"
])


# 1: Cp tp jest Fizyka?

with tab1:
    st.header("🧠 Co to w ogóle jest ta fizyka?")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        Słowo **fizyka** pochodzi z języka greckiego i oznacza *naturę*. 
        Fizyka to nie jest nudna nauka zakuwania wzorów na pamięć. To instrukcja obsługi całego wszechświata!

        **Do czego służy fizyka w życiu codziennym?**
        * **W Twojej kieszeni:** Smartfon działa dzięki fizyce kwantowej i elektromagnetyzmowi.
        * **W konsoli/PC:** Gry komputerowe mają tzw. *silnik fizyczny*, który oblicza jak spada kamień, jak odbija się piłka albo jak rozpada się budynek po wybuchu.
        * **Na rowerze i deskorolce:** Hamowanie, skręcanie i nieprzewracanie się to czysta fizyka sił i tarcia.

        Fizyka odpowiada na pytania: 
        * 🌌 Dlaczego niebo jest niebieskie? 
        * 🧲 Dlaczego magnes przyciąga metalowe drzwi lodówki? 
        * 🚢 Jak to się dzieje, że wielki metalowy statek nie tonie w oceanie?
        """)
    with col2:
        st.info(
            "💡 **Zapamiętaj:** Fizyk to taki detektyw, który zamiast złodziei, tropi zasady, jakimi rządzi się przyroda. Narzędziami fizyka są **obserwacja** oraz **eksperyment**.")


# 2. Stany skupienia

with tab2:
    st.header("💧 Trzy stany skupienia materii")
    st.write(
        "Wszystko wokół nas (materia) składa się z malutkich klocków – **atomów i cząsteczek**. To, jak blisko siebie stoją i jak bardzo się ruszają, decyduje o stanie skupienia:")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.subheader("🧊 Ciała stałe")
        st.markdown("""
        * **Przykłady:** lód, kamień, smartfon, biurko.
        * **Jak wyglądają cząsteczki?** Stoją ciasno ramię w ramię jak pasażerowie w zatłoczonym autobusie. Nie mogą się przemieszczać, tylko lekko drżą.
        * **Cechy:** Mają swój **własny, stały kształt** i **określoną objętość**. Trudno je ścisnąć czy rozciągnąć.
        """)

    with c2:
        st.subheader("💧 Ciecze")
        st.markdown("""
        * **Przykłady:** woda, sok, płynny miód, olej.
        * **Jak wyglądają cząsteczki?** Są blisko siebie, ale mogą się swobodnie przemieszczać i ślizgać jedna po drugiej (jak tłum ludzi na koncercie).
        * **Cechy:** Mają określoną objętość, ale **nie mają stałego kształtu** – przybierają kształt naczynia, do którego je wlejesz. Są prawie nieściśliwe.
        """)

    with c3:
        st.subheader("💨 Gazy")
        st.markdown("""
        * **Przykłady:** powietrze, para wodna, hel w balonie.
        * **Jak wyglądają cząsteczki?** Są bardzo daleko od siebie i latają we wszystkie strony jak szalone (jak dzieci na przerwie szkolnej).
        * **Cechy:** **Nie mają ani stałego kształtu, ani stałej objętości**. Zajmują całą dostępną przestrzeń. Są bardzo ściśliwe (możesz wtłoczyć dużo powietrza do małej opony).
        """)


# 3. GĘSTOŚĆ, MASA I OBJĘTOŚĆ

with tab3:
    st.header("⚖️ Laboratorium Gęstości")
    st.write(
        "Dlaczego kilogram żelaza zajmuje mało miejsca, a kilogram pierza zająłby cały worek? Odpowiedzią jest **GĘSTOŚĆ**.")

    st.markdown("""
    Zanim przejdziemy do wzoru, musimy wiedzieć, jak zdobyć dwie kluczowe informacje:
    1. **Masa ($m$):** Informuje nas, ile materii jest w ciele. Wyznaczamy ją za pomocą **wagi**. Główną jednostką jest kilogram ($kg$) lub gram ($g$).
    2. **Objętość ($V$):** Informuje nas, ile miejsca zajmuje ciało.
       * *Dla ciał regularnych:* Liczymy ze wzoru (np. boki kostki: $V = a \\cdot b \\cdot c$).
       * *Dla ciał nieregularnych (np. kamień):* Używamy **menzurki** z wodą! Wrzucony przedmiot wypycha wodę do góry dokładnie o tyle, ile sam wynosi jego objętość.
    """)

    st.subheader("📊 Wzór na gęstość")
    st.latex(r"\rho = \frac{m}{V}")
    st.write("Gdzie: $\\rho$ (ro) to gęstość, $m$ to masa, a $V$ to objętość.")

    st.markdown("---")
    st.subheader("🧪 Interaktywne Doświadczenie: Pomiar w menzurce")

    col_param, col_vis = st.columns(2)

    with col_param:
        substancja = st.selectbox(
            "Wybierz materiał przedmiotu:",
            ["Drewno (Sosna)", "Aluminium", "Żelazo", "Złoto"]
        )

        gestosci = {"Drewno (Sosna)": 0.5, "Aluminium": 2.7, "Żelazo": 7.9, "Złoto": 19.3}
        rho_wybrana = gestosci[substancja]

        st.metric(label=f"Gęstość substancji ({substancja})", value=f"{rho_wybrana} g/cm³")

        # Suwak objętości wrzucanego przedmiotu
        V_przedmiotu = st.slider("Wybierz objętość przedmiotu (w cm³):", min_value=10, max_value=100, value=40, step=10)

        # Początkowy stan wody w menzurce
        V_wody_start = 100
        V_wody_koniec = V_wody_start + V_przedmiotu

        # Wyliczenie masy ze wzoru m = rho * V
        m_wyliczona = rho_wybrana * V_przedmiotu

        st.success("📝 **Krok po kroku w laboratorium:**")
        st.write(f"1. Wlewamy do menzurki dokładnie **{V_wody_start} cm³** wody.")
        st.write(f"2. Wrzucamy **{substancja}**. Poziom wody rośnie do **{V_wody_koniec} cm³**.")
        st.write(
            f"3. Obliczamy objętość przedmiotu: ${V_wody_koniec} - {V_wody_start} = {V_przedmiotu}\\text{{ cm³}}$.")
        st.write(f"4. Kładziemy przedmiot na wagę. Ponieważ znamy gęstość, waga wskaże:")
        st.latex(r"m = \rho \cdot V = " + f"{rho_wybrana} \\cdot {V_przedmiotu} = {m_wyliczona:.1f} \\text{{ g}}")

    with col_vis:
        st.subheader("🏺 Wizualizacja eksperymentu")

        # Rysowanie menzurki przed i po wrzuceniu
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7, 5))

        # Menzurka 1 - tylko woda
        ax1.bar(0, V_wody_start, width=0.6, color='skyblue', edgecolor='black', linewidth=2)
        ax1.set_xlim(-0.5, 0.5)
        ax1.set_ylim(0, 220)
        ax1.set_title("1. Sama woda")
        ax1.set_ylabel("Objętość (cm³ / ml)")
        ax1.set_xticks([])
        ax1.grid(axis='y', linestyle='--', alpha=0.7)

        # Menzurka 2 - woda + przedmiot
        ax2.bar(0, V_wody_koniec, width=0.6, color='skyblue', edgecolor='black', linewidth=2)
        # Rysowanie przedmiotu na dnie lub na powierzchni
        if rho_wybrana < 1.0:
            # Drewno pływa na powierzchni wody
            ax2.plot(0, V_wody_koniec - 5, 's', ms=25, color='peru', label='Przedmiot (pływa)')
        else:
            # Reszta tonie na dno
            ax2.plot(0, 15, 's', ms=25, color='grey', label='Przedmiot (utonął)')

        ax2.set_xlim(-0.5, 0.5)
        ax2.set_ylim(0, 220)
        ax2.set_title("2. Po wrzuceniu ciała")
        ax2.set_xticks([])
        ax2.grid(axis='y', linestyle='--', alpha=0.7)
        ax2.legend(loc='upper right')

        st.pyplot(fig)
        plt.close(fig)


# 4: mini - quiz

with tab4:
    st.header("🎮 Sprawdź, czy jesteś gotowy na lekcję!")
    st.write("Odpowiedz na 3 szybkie pytania i zobacz swój wynik:")

    punkty = 0

    # Pytanie 1
    q1 = st.radio(
        "**Pytanie 1:** Który stan skupienia materii NIE ma stałej objętości i zajmuje całą przestrzeń, jaką ma do dyspozycji?",
        ["Ciała stałe", "Ciecze", "Gazy"]
    )
    if q1 == "Gazy":
        punkty += 1

    # Pytanie 2
    q2 = st.radio(
        "**Pytanie 2:** Jak nazywa się naczynie laboratoryjne z podziałką, służące do mierzenia objętości cieczy lub ciał nieregularnych?",
        ["Probówka", "Menzurka (cylinder miarowy)", "Pipeta"]
    )
    if q2 == "Menzurka (cylinder miarowy)":
        punkty += 1

    # Pytanie 3
    q3 = st.radio(
        "**Pytanie 3:** Kawałek metalu ma masę 20g i objętość 10 cm³. Jaka jest jego gęstość? (Wskazówka: podziel masę przez objętość!)",
        ["2 g/cm³", "200 g/cm³", "0.5 g/cm³"]
    )
    if q3 == "2 g/cm³":
        punkty += 1

    # Przycisk sprawdzający wynik
    if st.button("Sprawdź mój wynik! 🏆"):
        if punkty == 3:
            st.success(f"🔥 Idealnie! Zdobywasz {punkty}/3 punktów. Fizyka w 7 klasie będzie dla Ciebie prościzną!")
        elif punkty == 2:
            st.info(f"👍 Dobrze! Masz {punkty}/3 punktów. Jeden mały błąd, ale i tak świetny wynik!")
        else:
            st.warning(f"Ups! Twój wynik to {punkty}/3. Przejrzyj zakładki jeszcze raz, na pewno szybko załapiesz!")

# Stopka edukacyjna
st.markdown("---")
st.caption("Aplikacja stworzona jako interaktywny pomocnik do nauki fizyki dla uczniów klasy 7 szkół podstawowych.")
