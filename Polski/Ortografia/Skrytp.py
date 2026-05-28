import os
import random
import streamlit as st

st.set_page_config(
    page_title="Quiz Ortograficzny Żorża", page_icon="🏆", layout="centered"
)


def wczytaj_zadania(nazwa_pliku):
    zadania = {"latwy": [], "sredni": [], "trudny": []}
    sciezka_skryptu = os.path.dirname(__file__)
    pelna_sciezka = os.path.join(sciezka_skryptu, nazwa_pliku)
    try:
        with open(pelna_sciezka, "r", encoding="utf-8") as plik:
            for linia in plik:
                if not linia.strip():
                    continue
                czesci = linia.strip().split(",")
                if len(czesci) == 3:
                    poziom, slowo, zdanie = czesci
                    p_clean = poziom.strip().lower()
                    if p_clean in zadania:
                        zadania[p_clean].append((slowo.strip().lower(), zdanie.strip()))
        return zadania
    except FileNotFoundError:
        st.error(f"❌ Nie znaleziono pliku {nazwa_pliku}")
        return None


if "gra_uruchomiona" not in st.session_state:
    st.session_state.gra_uruchomiona = False
    st.session_state.wynik = 0
    st.session_state.zycia = 3
    st.session_state.numer_pytania = 0
    st.session_state.pytania = []
    st.session_state.feedback = None
    st.session_state.pokazuj_wyjasnienie = False
    st.session_state.typ_bledu = None

st.title("Quiz Ortograficzny Żorża")

if not st.session_state.gra_uruchomiona:
    st.markdown("### Przygotuj się do nauki!")
    baza = wczytaj_zadania("ortografia.txt")
    if baza:
        poziom = st.selectbox("Wybierz poziom trudności:", ["latwy", "sredni", "trudny"])
        liczba_slow = st.selectbox("Wybierz liczbę słówek:", [5, 10, 20])
        st.warning(
            "⚠️ **Uwaga:** Ilość kropek w zdaniu nie odpowiada liczbie liter"
            " w słowie!"
        )
        if st.button("🚀 ROZPOCZNIJ GRĘ"):
            wybrane = baza[poziom]
            if wybrane:
                random.shuffle(wybrane)
                st.session_state.pytania = wybrane[:liczba_slow]
                st.session_state.gra_uruchomiona = True
                st.session_state.wynik = 0
                st.session_state.zycia = 3
                st.session_state.numer_pytania = 0
                st.session_state.poziom_nazwa = poziom
                st.session_state.feedback = None
                st.session_state.pokazuj_wyjasnienie = False
                st.rerun()
else:
    pytania = st.session_state.pytania
    idx = st.session_state.numer_pytania
    if (idx >= len(pytania) or st.session_state.zycia <= 0) and not st.session_state.pokazuj_wyjasnienie:
        if st.session_state.zycia <= 0:
            st.snow()
            st.error(f"💀 KONIEC GRY! Straciłeś wszystkie życia. Wynik: {st.session_state.wynik} PKT")
        else:
            st.balloons()
            st.success(f"🎊 GRATULACJE! Ukończyłeś poziom {st.session_state.poziom_nazwa}!")
            st.write(f"Twój wynik końcowy: **{st.session_state.wynik} / {len(pytania)}**")
        if st.button("Zagraj ponownie"):
            st.session_state.gra_uruchomiona = False
            st.rerun()
    else:
        col1, col2, col3 = st.columns(3)
        col1.metric("⭐ Punkty (XP)", st.session_state.wynik)
        col2.metric("❤️ Życia", "❤️" * st.session_state.zycia)
        col3.metric("Ostatnie", st.session_state.feedback if st.session_state.feedback else "-")
        st.progress(idx / len(pytania))
        poprawne_slowo, zdanie = pytania[idx]
        st.markdown("#### Uzupełnij luki w zdaniu:")
        st.info(zdanie.replace(poprawne_slowo, "........."))

        def sprawdz_odpowiedz():
            wpisane = st.session_state.wpisana_odpowiedz.strip().lower()
            poprawne = poprawne_slowo.lower()
            if wpisane == poprawne:
                st.session_state.wynik += 1
                st.session_state.feedback = "✅ Dobrze!"
                st.session_state.numer_pytania += 1
            else:
                if poprawne.replace("ó", "o") == wpisane:
                    st.session_state.feedback = "⚠️ Blisko! (błąd ó/o)"
                    st.session_state.typ_bledu = "blisko"
                    st.session_state.pokazuj_wyjasnienie = True
                else:
                    st.session_state.zycia -= 1
                    st.session_state.feedback = "❌ Błąd"
                    st.session_state.typ_bledu = "zle"
                    st.session_state.pokazuj_wyjasnienie = True

        if st.session_state.pokazuj_wyjasnienie:
            if st.session_state.typ_bledu == "blisko":
                st.warning(f"Prawie dobrze! Pamiętaj, że słowo **'{poprawne_slowo}'** piszemy przez **ó**.")
            else:
                st.error(f"Niestety to zła odpowiedź. Poprawne słowo to: **{poprawne_slowo}**")
            st.markdown(f"Poprawne zdanie: {zdanie.replace(poprawne_slowo, f'**{poprawne_slowo}**')}")
            if st.button("Dalej ➡️"):
                st.session_state.pokazuj_wyjasnienie = False
                st.session_state.numer_pytania += 1
                st.rerun()
        else:
            st.text_input("Wpisz brakujące słowo:", key="wpisana_odpowiedz", on_change=sprawdz_odpowiedz)


# STOPKA
st.divider()
st.caption("Najcierpliwszy portal do ortografii - klasa 4")
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")
