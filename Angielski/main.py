import streamlit as st
import csv
import random


st.set_page_config(page_title="Apka do Słówek", page_icon="✏️")
st.title("Moja Nauka Słówek")


def laduj_slowka(sciezka_do_pliku):
    """Pobiera bazę słów z CSV i robi z nich listę słowników"""
    pobrane_dane = []
    try:
        # Użycie bardziej opisowej nazwy zmiennej pliku zamiast 'f'
        with open(sciezka_do_pliku, 'r', encoding='utf-8') as surowy_plik:
            obiekt_csv = csv.reader(surowy_plik)
            for wiersz in obiekt_csv:
                # Rozbijamy wiersz na konkretne części, zamiast operować na indeksach w append
                if len(wiersz) >= 2:
                    pl_word = wiersz[0].strip()
                    en_word = wiersz[1].strip()
                    # Pakujemy do słownika krok po kroku
                    wpis = {'pl': pl_word, 'en': en_word}
                    pobrane_dane.append(wpis)
    except FileNotFoundError:
        st.warning(f"Błąd: Nie widzę pliku o nazwie {sciezka_do_pliku} w folderze.")
    return pobrane_dane


def nastepne_pytanie():
    # Pobieramy to, co wpisał użytkownik
    odp_usera = st.session_state.temp_odp.lower().strip()
    prawidlowe = st.session_state.lista_slowek[st.session_state.index][st.session_state.target_lang]

    # Porównanie odpowiedzi
    if odp_usera == prawidlowe.lower().strip():
        st.session_state.feedback = ("dobrze", "Super! Dobra odpowiedź.")
        st.session_state.punkty += 1
    else:
        st.session_state.feedback = ("zle", f"Niestety nie. Miało być: {prawidlowe}")

    # Przeskakujemy do kolejnego elementu
    st.session_state.index += 1
    st.session_state.temp_odp = ""


# PANEL BOCZNY (SIDEBAR)
with st.sidebar:
    st.header("Panel sterowania")
    wybrany_numer = st.selectbox("Który rozdział?", range(1, 22))
    wybrany_tryb = st.radio("Czego się uczysz:", ["Polski na Angielski", "Angielski na Polski"])

    # Mapowanie kierunku tłumaczenia
    t_source = 'pl' if "Polski" in wybrany_tryb else 'en'
    t_target = 'en' if "Polski" in wybrany_tryb else 'pl'

# Inicjalizacja sesji - sprawdzamy czy coś się zmieniło
if ('aktualny_rozdzial' not in st.session_state or
        st.session_state.aktualny_rozdzial != wybrany_numer or
        st.session_state.ostatni_tryb != wybrany_tryb):
    st.session_state.aktualny_rozdzial = wybrany_numer
    st.session_state.ostatni_tryb = wybrany_tryb
    # Budujemy nazwę pliku dynamicznie
    nazwa_pliku = f'ang_kl4_rozdzial{wybrany_numer}.csv'
    st.session_state.lista_slowek = laduj_slowka(nazwa_pliku)

    random.shuffle(st.session_state.lista_slowek)
    st.session_state.index = 0
    st.session_state.punkty = 0
    st.session_state.feedback = None
    st.session_state.target_lang = t_target
    st.session_state.source_lang = t_source

# GŁÓWNY WIDOK APLIKACJI
if st.session_state.lista_slowek:
    ile_wszystkich = len(st.session_state.lista_slowek)
    ktore_teraz = st.session_state.index

    # Pasek postępu z własnym tekstem
    procent_postepu = ktore_teraz / ile_wszystkich if ile_wszystkich > 0 else 0
    st.progress(procent_postepu)

    st.info(f"Pytanie {min(ktore_teraz + 1, ile_wszystkich)} z {ile_wszystkich} | Wynik: {st.session_state.punkty}")

    if ktore_teraz < ile_wszystkich:
        aktualna_para = st.session_state.lista_slowek[ktore_teraz]
        pytanie_txt = aktualna_para[st.session_state.source_lang]

        st.markdown(f"### Przetłumacz: **{pytanie_txt}**")

        st.text_input(
            "Twoja propozycja:",
            key="temp_odp",
            on_change=nastepne_pytanie,
            placeholder="Wpisz i zatwierdź Enterem"
        )

        if st.session_state.feedback:
            wynik_typ, tresc_info = st.session_state.feedback
            if wynik_typ == "dobrze":
                st.success(tresc_info)
            else:
                st.error(tresc_info)
    else:
        # Koniec nauki
        st.balloons()
        st.header("Koniec nauki!")
        st.success(f"Twój wynik końcowy to: {st.session_state.punkty} na {ile_wszystkich}")

        if st.button("Powtórz ten rozdział ?"):
            st.session_state.index = 0
            st.session_state.punkty = 0
            st.session_state.feedback = None
            random.shuffle(st.session_state.lista_slowek)
            st.rerun()


# --- STOPKA ---
st.divider()
st.caption("Najcierpliwszy portal do angielskiego - klasa 4")
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")
