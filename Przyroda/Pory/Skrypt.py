import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Konfiguracja strony
st.set_page_config(page_title="Edukator: Pory Roku", page_icon="🌍", layout="wide")

# Menu boczne
st.sidebar.title("Nawigacja")
strona = st.sidebar.radio("Wybierz sekcję:", ["Pory Roku & Daty", "Oświetlenie Ziemi", "Quiz wiedzy"])

# Pory Roku & Daty
if strona == "Pory Roku & Daty":
    st.title("Pory roku na Ziemi i ich daty")
    st.write(
        "Pory roku zmieniają się z powodu nachylenia osi Ziemi pod kątem 23,5 stopnia oraz ruchu obiegowego wokół Słońca.")
    # Tabela
    dane_pory = {
        "Pora roku": ["Wiosna", "Lato", "Jesień", "Zima"],
        "Początek astronomiczny": ["20/21 marca (Równonoc)", "21/22 czerwca (Przesilenie)", "22/23 września (Równonoc)",
                                   "21/22 grudnia (Przesilenie)"],
        "Początek kalendarzowy": ["21 marca", "22 czerwca", "23 września", "22 grudnia"],
        "Zjawisko": ["Dzień równy nocy", "Najdłuższy dzień w roku", "Dzień równy nocy", "Najkrótszy dzień w roku"]
    }
    df = pd.DataFrame(dane_pory)
    st.table(df)
    st.info(
        "**Czy wiesz, że?** Kiedy na półkuli północnej (np. w Polsce) zaczyna się lato, na półkuli południowej (np. w Australii) startuje astronomiczna zima!")

# Sekcja Oświetlenie Ziemi
elif strona == "Oświetlenie Ziemi":
    st.title("Jak oświetlona jest Ziemia")
    st.write("Wybierz porę roku poniżej, aby zobaczyć, jak promienie słoneczne padają na naszą planetę.")
    pora_wybor = st.selectbox("Wybierz moment w roku:",
                              ["Przesilenie letnie (Czerwiec/Wakacje)", "Równonoc (Marzec/Wrzesień)",
                               "Przesilenie zimowe (Grudzień/Święta)"])
    # Wykres oświetlenia
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#0e1117')
    # Ustawienie kąta nachylenia OSI obrotu względem pionu
    if "letnie" in pora_wybor:
        kat_osi = -23.5  # Pochylenie w prawo (do Słońca)
        opis = "Spójrz na wykres: lewa strona planety to noc, a prawa to dzień. Ponieważ oś obrotu jest pochylona w prawą stronę (do Słońca), biegun północny (N) oraz Polska leżą głęboko po jasnej stronie. Nawet podczas obrotu Ziemi wokół własnej osi, Polska spędza większość czasu w świetle. Dzień jest bardzo długi!"
        polska_info = "🔴 **Polska w czerwcu:** Nasz region jest zwrócony ku Słońcu. Dzień trwa u nas ponad 16 godzin, a Słońce wznosi się wysoko nad horyzont."
    elif "zimowe" in pora_wybor:
        kat_osi = 23.5  # Odchylenie w lewo (w stronę nocy)
        opis = "Spójrz na wykres: lewa strona to noc, prawa to dzień. Oś obrotu jest odchylona w lewą stronę (w cień). Biegun północny (N) jest całkowicie schowany w mroku (trwa tam noc polarna). Polska znajduje się bardzo blisko granicy cienia i szybko w nią wkracza. Dzień jest bardzo krótki!"
        polska_info = "🔵 **Polska w grudniu:** Nasz region jest odchylony od Słońca. Ziemia obracając się, błyskawicznie chowa nas w cień (noc), dlatego dzień trwa tylko ok. 7,5 godziny."
    else:
        kat_osi = 0  # Brak nachylenia względem Słońca
        opis = "Oś Ziemi jest ustawiona idealnie pionowo względem promieni. Granica dnia i nocy przechodzi dokładnie przez oba bieguny. Obie półkule są oświetlone identycznie."
        polska_info = "🟢 **Polska podczas równonocy:** Dzień i noc trwają na całej planecie dokładnie tyle samo – po 12 godzin."

    # 1. RYSOWANIE ZIEMI (Prawa, jasna połowa dnia)
    ziemia_dzien = plt.Circle((0, 0), 1, color='#4a90e2', ec='white', lw=1.5, zorder=1)
    ax.add_patch(ziemia_dzien)

    # 2. PODZIAŁ: LEWO NOC, PRAWO DZIEŃ
    y_pien = np.linspace(-1, 1, 200)
    x_gora = -np.sqrt(1 - y_pien ** 2)
    x_dol = np.zeros_like(y_pien)  # Linia pionowa x = 0
    ax.fill_betweenx(y_pien, x_gora, x_dol, color='#1c2833', alpha=0.9, zorder=2)

    # Granica dnia i nocy
    ax.axvline(0, color="yellow", linestyle=":", alpha=0.5, zorder=3)

    # 3. RYSOWANIE OSI OBROTU ZIEMI
    rad_osi = np.radians(kat_osi)
    x_n, y_n = -1.2 * np.sin(rad_osi), 1.2 * np.cos(rad_osi)
    x_s, y_s = 1.2 * np.sin(rad_osi), -1.2 * np.cos(rad_osi)
    ax.plot([x_s, x_n], [y_s, y_n], color="#ff4b4b", linestyle="--", lw=2, zorder=4)
    ax.text(x_n * 1.1, y_n * 1.1, "N", color="#ff4b4b", weight="bold", fontsize=12, ha='center', zorder=5)
    ax.text(x_s * 1.1, y_s * 1.1, "S", color="#ff4b4b", weight="bold", fontsize=12, ha='center', zorder=5)

    # 4. RYSOWANIE RÓWNIKA
    x_row_1, y_row_1 = -1.0 * np.cos(rad_osi), -1.0 * np.sin(rad_osi)
    x_row_2, y_row_2 = 1.0 * np.cos(rad_osi), 1.0 * np.sin(rad_osi)
    ax.plot([x_row_1, x_row_2], [y_row_1, y_row_2], color="white", linestyle="-.", alpha=0.6, zorder=3)
    ax.text(x_row_2 * 1.1, y_row_2 * 1.1, "Równik", color="white", fontsize=9, va='center', zorder=5)

    # 5. POZYCJA POLSKI
    szerokosc_pl = np.radians(52)
    x_pl = -np.sin(rad_osi) * np.sin(szerokosc_pl) + np.cos(rad_osi) * np.cos(szerokosc_pl) * 0.4
    y_pl = np.cos(rad_osi) * np.sin(szerokosc_pl) + np.sin(rad_osi) * np.cos(szerokosc_pl) * 0.4
    ax.scatter(x_pl, y_pl, color="#ff4b4b", s=90, edgecolors="white", linewidths=1.5, zorder=6)
    ax.text(x_pl + 0.1, y_pl + 0.05, "Polska", color="white", weight="bold", fontsize=10, zorder=6)

    # 6. PROMIENIE SŁONECZNE
    for y_pos in np.linspace(-0.7, 0.7, 6):
        x_start = 1.6
        x_end = np.sqrt(1 - y_pos ** 2) if y_pos ** 2 <= 1 else 0
        ax.annotate('', xy=(x_end, y_pos), xytext=(x_start, y_pos),
                    arrowprops=dict(arrowstyle="->", color="#f1c40f", lw=2), zorder=4)
    ax.text(1.3, 0.8, "Promienie\nSłoneczne", color="#f1c40f", weight="bold", fontsize=10, ha='center')

    ax.set_xlim(-1.6, 1.8)
    ax.set_ylim(-1.6, 1.6)
    ax.axis("off")

    st.pyplot(fig)
    st.success(opis)
    st.info(polska_info)

# Sekcja 3 -- Quiz wiedzy
elif strona == "Quiz wiedzy":
    st.title("Quiz o porach roku i oświetleniu Ziemi")
    st.write("Odpowiedz na poniższe pytania i sprawdź swoją wiedzę. Powodzenia!")

    # 1. BAZA PYTAŃ
    if 'baza_pytan' not in st.session_state:
        st.session_state.baza_pytan = [
            {
                "id": 1,
                "pytanie": "Pod jakim kątem nachylona jest oś obrotu Ziemi do płaszczyzny jej orbity?",
                "opcje": ["0 stopni (jest prostopadła)", "23,5 stopnia", "45 stopni", "90 stopni"],
                "poprawna": "23,5 stopnia"
            },
            {
                "id": 2,
                "pytanie": "Kiedy na półkuli północnej występuje najkrótszy dzień w roku?",
                "opcje": ["21 marca", "22 czerwca", "23 września", "21/22 grudnia"],
                "poprawna": "21/22 grudnia"
            },
            {
                "id": 3,
                "pytanie": "Co oznacza termin 'równonoc'?",
                "opcje": ["Dzień trwa tyle samo co noc", "Słońce w ogóle nie zachodzi", "Ziemia jest najbliżej Słońca",
                          "Księżyc zasłania Słońce"],
                "poprawna": "Dzień trwa tyle samo co noc"
            },
            {
                "id": 4,
                "pytanie": "Jak nazywa się zjawisko, gdy wokół bieguna Słońce nie zachodzi przez całą dobę?",
                "opcje": ["Noc polarna", "Dzień polarny", "Przesilenie letnie", "Równonoc jesienna"],
                "poprawna": "Dzień polarny"
            },
            {
                "id": 5,
                "pytanie": "Jaka pora roku panuje w Australii, gdy w Polsce rozpoczyna się astronomiczne lato?",
                "opcje": ["Wiosna", "Lato", "Jesień", "Zima"],
                "poprawna": "Zima"
            }
        ]

    # Inicjalizacja stanu sprawdzenia quizu
    if 'quiz_sprawdzony' not in st.session_state:
        st.session_state.quiz_sprawdzony = False
    if 'zapisane_odpowiedzi' not in st.session_state:
        st.session_state.zapisane_odpowiedzi = {}

    # Formularz wyświetlający quiz
    with st.form("formularz_quizu"):
        odpowiedzi_uzytkownika = {}
        for p in st.session_state.baza_pytan:
            # Wymuszamy unikalny i bezpieczny klucz tekstowy
            klucz_pytania = str(p['id'])

            st.markdown(f"##### Pytanie {klucz_pytania}: {p['pytanie']}")
            odpowiedzi_uzytkownika[klucz_pytania] = st.radio(
                "Wybierz odpowiedź:",
                p['opcje'],
                key=f"pyt_{klucz_pytania}",
                index=None
            )
            st.write("")

        przycisk_sprawdz = st.form_submit_button("Sprawdź odpowiedzi")

    # Logika po kliknięciu przycisku
    if przycisk_sprawdz:
        # Sprawdzanie czy użytkownik pominął jakieś pytania
        puste_pytania = [k for k, v in odpowiedzi_uzytkownika.items() if v is None]

        if puste_pytania:
            st.warning(
                f"Proszę odpowiedzieć na wszystkie pytania! Brak odpowiedzi na pytania nr: {', '.join(puste_pytania)}")
            st.session_state.quiz_sprawdzony = False
        else:
            st.session_state.quiz_sprawdzony = True
            st.session_state.zapisane_odpowiedzi = odpowiedzi_uzytkownika

    # Wyświetlanie wyników (poza formularzem)
    if st.session_state.quiz_sprawdzony:
        punkty = 0
        ilosc_pytan = len(st.session_state.baza_pytan)
        st.markdown("### Wyniki quizu:")

        for p in st.session_state.baza_pytan:
            # Używamy dokładnie tego samego klucza tekstowego co w formularzu
            klucz_pytania = str(p['id'])
            ans = st.session_state.zapisane_odpowiedzi.get(klucz_pytania)

            if ans == p['poprawna']:
                punkty += 1
                st.success(f"**Pytanie {klucz_pytania}**: Poprawnie! (Twoja odpowiedź: {ans})")
            else:
                st.error(
                    f"**Pytanie {klucz_pytania}**: Błędna odpowiedź. Twoja odpowiedź: *{ans}*. Poprawna to: **{p['poprawna']}**")

        # Wyświetlenie końcowego wyniku
        st.metric(label="Twój końcowy wynik to:", value=f"{punkty} / {ilosc_pytan}")
        if punkty == ilosc_pytan:
            st.balloons()
            st.success("Doskonale! Wszystkie odpowiedzi są poprawne! 🌟")
st.divider()
st.caption("Najcierpliwszy portal do przyrody - klasa 4")
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")
