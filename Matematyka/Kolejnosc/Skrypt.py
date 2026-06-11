import streamlit as st
import random
import matplotlib.pyplot as plt


def pokaz_czekoladke(wiersze, kolumny):
    fig, ax = plt.subplots(figsize=(3.5, 3.5))
    for x in range(wiersze):
        for y in range(kolumny):
            kostka = plt.Rectangle((y, -x - 1), 1, 1, facecolor='#7B3F00', edgecolor='white', linewidth=1.5)
            ax.add_patch(kostka)
    ax.set_xlim(0, kolumny)
    ax.set_ylim(-wiersze, 0)
    ax.set_aspect('equal')
    ax.axis('off')
    st.pyplot(fig)


st.set_page_config(page_title="Mistrz Mnożenia", page_icon="🍫")

# --- STAN GRY DLA CZWARTEJ KLASY ---
if 'punkty_k4' not in st.session_state:
    st.session_state.punkty_k4 = 0
if 'los1' not in st.session_state:
    st.session_state.los1 = random.randint(2, 5)
    st.session_state.los2 = random.randint(2, 5)

# --- STAN GRY DLA PIĄTEJ KLASY ---
if 'punkty_k5' not in st.session_state:
    st.session_state.punkty_k5 = 0
if 'los1_k5' not in st.session_state:
    st.session_state.los1_k5 = random.randint(11, 20)
    st.session_state.los2_k5 = random.randint(2, 10)

st.title("🍫 Mistrz Mnożenia")

karty = st.tabs(["👦 Klasa 4", "🚀 Klasa 5 (Mnożenie do 20)"])

# === CZĘŚĆ DLA KLASY 4 ===
with karty[0]:
    st.subheader("Trening tabliczki mnożenia")

    poziom = st.radio("Wybierz poziom:", ["Łatwy", "Hardcore"], key="level_4")
    if poziom == "Hardcore":
        limit = 15
        st.info("Oho, wjeżdżają duże liczby! Dasz radę?")
    else:
        limit = 10

    st.metric("Twoje punkty", st.session_state.punkty_k4)

    a, b = st.session_state.los1, st.session_state.los2
    lewa, prawa = st.columns(2)

    with lewa:
        st.write(f"### Ile to {a} × {b}?")
        odp_ucznia = st.number_input("Wpisz wynik:", min_value=0, step=1, key="wpis_k4")

        if st.button("Sprawdzam!", key="klik_k4"):
            if odp_ucznia == a * b:
                st.success("Ekstra! Łap wirtualną czekoladę! 🍫")
                st.session_state.punkty_k4 += 1
                st.balloons()
            else:
                if poziom == "Hardcore":
                    st.error("Aj, pomyłka na trudnym poziomie boli! Licznik punktów spada do zera.")
                    st.session_state.punkty_k4 = 0
                else:
                    st.warning("Nie do końca. Spokojnie, policz kwadraciki na czekoladzie obok i wpisz jeszcze raz!")

        if st.button("Daj kolejne zadanie ➡️", key="dalej_k4"):
            st.session_state.los1 = random.randint(2, limit)
            st.session_state.los2 = random.randint(2, limit)
            st.rerun()

    with prawa:
        st.write("#### Podgląd czekolady:")
        pokaz_czekoladke(a, b)

# === CZĘŚĆ DLA KLASY 5 ===
with karty[1]:
    st.subheader("Wyzwanie dla Klasy 5 – Mnożenie do 20!")
    st.info("Zero czekolady, liczy się tylko czysta matma i Twoja szybkość!")

    st.metric("🔥 Twój rekord", st.session_state.punkty_k5)

    a5, b5 = st.session_state.los1_k5, st.session_state.los2_k5

    st.write(f"### Ile to jest: **{a5} × {b5}**?")
    odp_ucznia5 = st.number_input("Wpisz wynik:", min_value=0, step=1, key="wpis_k5")

    b1, b2 = st.columns(2)

    with b1:
        if st.button("Sprawdź wynik", key="klik_k5"):
            if odp_ucznia5 == a5 * b5:
                st.success("Klasa! Rozwalasz tę piątą klasę w pył! 🎉")
                st.session_state.punkty_k5 += 1
                st.snow()
            else:
                st.error(f"Uuu, pudło! Prawidłowy wynik to **{a5 * b5}**. Tracisz punkty, ale próbuj dalej!")
                st.session_state.punkty_k5 = 0

    with b2:
        if st.button("Daj kolejne zadanie ➡️", key="dalej_k5"):
            st.session_state.los1_k5 = random.randint(11, 20)
            st.session_state.los2_k5 = random.randint(2, 20)
            st.rerun()

# STOPKA
st.divider()
st.caption("Najcierpliwszy portal do matematyki - klasa 4 i 5")
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")
