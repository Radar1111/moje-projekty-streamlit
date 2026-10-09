import streamlit as st
import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np

# Konfiguracja strony
st.set_page_config(page_title="Mistrz Zegara", page_icon="⏰", layout="centered")
st.write("## ⏰ Akademia Zegara")
st.write("Cześć! Wybierz poziom i trenuj zegarek razem ze mną!")

# Dwie zakładki
tab1, tab2 = st.tabs(["🧮 1. Ile czasu minęło?", "🗣️ 2. Jak to powiedzieć?"])

# Inicjalizacja pamięci aplikacji (session_state)
if 'start_time' not in st.session_state: st.session_state.start_time = None
if 'end_time' not in st.session_state: st.session_state.end_time = None
if 'diff_hours' not in st.session_state: st.session_state.diff_hours = 0
if 'diff_minutes' not in st.session_state: st.session_state.diff_minutes = 0
if 'chcked_calcs' not in st.session_state: st.session_state.chcked_calcs = False

if 'trans_h' not in st.session_state: st.session_state.trans_h = 12
if 'trans_m' not in st.session_state: st.session_state.trans_m = 0
if 'checked_trans' not in st.session_state: st.session_state.checked_trans = False


# Funkcja rysująca czysty, czytelny zegar
def rysuj_zegar(h, m):
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)

    # Tarcza zegara
    an = np.linspace(0, 2 * np.pi, 100)
    ax.plot(np.cos(an), np.sin(an), color="black", linewidth=3)

    # Wyraźne cyfry dla dziecka
    for i in range(1, 13):
        kat = np.pi / 2 - i * (2 * np.pi / 12)
        ax.text(0.85 * np.cos(kat), 0.85 * np.sin(kat), str(i),
                va='center', ha='center', fontsize=15, fontweight='bold')

    # Obliczanie pozycji wskazówek
    kat_minut = np.pi / 2 - m * (2 * np.pi / 60)
    kat_godzin = np.pi / 2 - (h % 12 + m / 60.0) * (2 * np.pi / 12)

    # GRUBA CZERWONA wskazówka = GODZINA
    ax.plot([0, 0.5 * np.cos(kat_godzin)], [0, 0.5 * np.sin(kat_godzin)], color="firebrick", linewidth=7,
            solid_capstyle='round')
    # CIENKA NIEBIESKA wskazówka = MINUTA
    ax.plot([0, 0.8 * np.cos(kat_minut)], [0, 0.8 * np.sin(kat_minut)], color="navy", linewidth=4,
            solid_capstyle='round')

    # Środek zegara
    ax.plot(0, 0, 'ko', markersize=8)
    ax.axis('off')
    return fig


# Losowanie zadań dopasowane do poziomu trudności
def losuj_zadanie_obliczen(trudnosc):
    if trudnosc == "🟢 Łatwy (0, 15, 30, 45 min)":
        h_start = random.randint(1, 12)
        m_start = random.choice([0, 15, 30, 45])
        losowe_godziny = random.randint(1, 4)
        losowe_minuty = random.choice([0, 15, 30, 45])
        total_minutes = losowe_godziny * 60 + losowe_minuty
    else:  # Trudny - pełna losowość jak w oryginale
        h_start = random.randint(0, 22)
        m_start = random.randint(0, 59)
        total_minutes = random.randint(5, 715)

    start = datetime.strptime(f"{h_start}:{m_start}", "%H:%M")
    koniec = start + timedelta(minutes=total_minutes)

    st.session_state.start_time = start.strftime("%H:%M")
    st.session_state.end_time = koniec.strftime("%H:%M")
    st.session_state.diff_hours = total_minutes // 60
    st.session_state.diff_minutes = total_minutes % 60
    st.session_state.chcked_calcs = False

    # Automatyczne czyszczenie okienek odpowiedzi
    st.session_state.u_hours = 0
    st.session_state.u_mins = 0


def losuj_godzine_tlumacz(trudnosc):
    if trudnosc == "🟢 Łatwy (0, 15, 30, 45 min)":
        st.session_state.trans_h = random.randint(1, 12)
        st.session_state.trans_m = random.choice([0, 15, 30, 45])
    else:  # Trudny - pełne 24h i minuty co 5 minut
        st.session_state.trans_h = random.randint(0, 23)
        st.session_state.trans_m = random.choice([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55])
    st.session_state.checked_trans = False


def generuj_opis_slowny(h, m):
    godziny_mianownik = ["dwunasta", "pierwsza", "druga", "trzecia", "czwarta", "piąta", "szósta", "siódma", "ósma",
                         "dziewiąta", "dziesiąta", "jedenasta"]
    godziny_odmienione = ["dwunastej", "pierwszej", "drugiej", "trzeciej", "czwartej", "piątej", "szóstej", "siódmej",
                          "ósmej", "dziewiątej", "dziesiątej", "jedenastej"]

    godziny_24h = ["zerowa", "pierwsza", "druga", "trzecia", "czwarta", "piąta", "szósta", "siódma", "ósma",
                   "dziewiąta", "dziesiąta", "jedenasta", "dwunasta", "trzynasta", "czternasta", "piętnasta",
                   "szesnasta", "siedemnasta", "osiemnasta", "dziewiętnasta", "dwudziesta", "dwudziesta pierwsza",
                   "dwudziesta druga", "dwudziesta trzecia"]

    # Oficjalna (24h)
    opis_24h = f"godzina {godziny_24h[h]}"
    if m > 0:
        opis_24h += f" {m:02d}" if m < 10 else f" {m}"

    # Potoczna (12h)
    h_12 = h % 12
    h_nastepna = (h + 1) % 12

    if m == 0:
        opis_12h = f"godzina {godziny_mianownik[h_12]}"
    elif m == 30:
        opis_12h = f"wpół do {godziny_odmienione[h_nastepna]}"
    elif m < 30:
        opis_12h = f"{m} po {godziny_odmienione[h_12]}"
    else:
        minuty_do = 60 - m
        if m == 45:
            opis_12h = f"za piętnaście {godziny_mianownik[h_nastepna]}"
        else:
            opis_12h = f"za {minuty_do} {godziny_mianownik[h_nastepna]}"

    return opis_12h, opis_24h


# Obliczanie upływu czasu
with tab1:
    st.subheader("🧮 Zadanie: Ile czasu minęło?")
    level_calc = st.radio("Wybierz poziom trudności zadań:",
                          ["🟢 Łatwy (0, 15, 30, 45 min)", "🔴 Trudny (Dowolne godziny i minuty)"], key="rad_calc")

    if st.button("🎲 Wylosuj zadanie", key="btn_calc"):
        losuj_zadanie_obliczen(level_calc)

    if st.session_state.start_time:
        st.info(f"Zaczynamy o: **{st.session_state.start_time}**  |  Kończymy o: **{st.session_state.end_time}**")
        st.write("Wpisz ile to godzin i minut:")

        col1, col2 = st.columns(2)
        with col1:
            user_hours = st.number_input("Godziny:", min_value=0, max_value=24, step=1, key="u_hours")
        with col2:
            user_minutes = st.number_input("Minuty:", min_value=0, max_value=59, step=1, key="u_mins")

        if st.button("✔️ Sprawdź odpowiedź", key="btn_check_calc"):
            st.session_state.chcked_calcs = True

        if st.session_state.chcked_calcs:
            if user_hours == st.session_state.diff_hours and user_minutes == st.session_state.diff_minutes:
                st.success("🎉 Super! Doskonała odpowiedź! Łap balony! 🎈")

            else:
                st.error(
                    f"Niestety nie. Prawidłowa odpowiedź to: **{st.session_state.diff_hours} godz. i {st.session_state.diff_minutes} min.** Spróbuj jeszcze raz!")

# Tłumacz godzin
with tab2:
    st.subheader("👀 Przyjrzyj się wskazówkom:")
    level_trans = st.radio("Wybierz poziom trudności zegara:",
                           ["🟢 Łatwy (0, 15, 30, 45 min)", "🔴 Trudny (Wszystkie godziny 24h i minuty co 5 min)"],
                           key="rad_trans")

    if st.button("🔄 Zmień godzinę na zegarze", key="btn_trans"):
        losuj_godzine_tlumacz(level_trans)

    # Rysowanie zegara
    fig_zegar = rysuj_zegar(st.session_state.trans_h, st.session_state.trans_m)
    st.pyplot(fig_zegar)
    plt.close(fig_zegar)

    if st.button("👁️ Sprawdź, która to godzina", key="btn_check_trans"):
        st.session_state.checked_trans = True

    if st.session_state.checked_trans:
        potoczna, oficjalna = generuj_opis_slowny(st.session_state.trans_h, st.session_state.trans_m)
        czas_cyfrowy = f"{st.session_state.trans_h:02d}:{st.session_state.trans_m:02d}"

        st.markdown(f"### ⌚ Na zegarku jest: **{czas_cyfrowy}**")
        st.success(f"🗣️ Mówimy potocznie: **{potoczna}**")
        if "🔴" in level_trans:
            st.info(f"🏢 Wersja oficjalna (24h): {oficjalna}")
            
# --- STOPKA ---
st.divider()
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")
