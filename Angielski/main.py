import streamlit as st
from datasets import load_dataset
import random


st.set_page_config(page_title="Apka do Słówek", page_icon="✏️")
st.title("Moja Nauka Słówek")


def laduj_slowka(nazwa_pliku):
    """Pobiera bazę słów z Hugging Face Dataset"""
    try:
        # TUTAJ WPISZ SWÓJ NICK Z HUGGING FACE ZAMIAST TWÓJ_NICK_Z_HF
        repo_id = "Radar1111/angielski-klasa-4" 
        
        dataset = load_dataset(
            repo_id, 
            data_files=nazwa_pliku, 
            token=st.secrets["HF_TOKEN"]
        )
        
        pobrane_dane = []
        for wiersz in dataset['train']:
            pobrane_dane.append({'pl': wiersz['pl'], 'en': wiersz['en']})
        return pobrane_dane
    except Exception as e:
        st.error(f"Problem z połączeniem: {e}")
        return []


def nastepne_pytanie():
    # Pobieramy to, co wpisał użytkownik
    if st.session_state.temp_odp:
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
    # Tutaj dodaj numery rozdziałów, które masz wgrane jako CSV
    wybrany_numer = st.selectbox("Który rozdział?", [1, 2]) 
    wybrany_tryb = st.radio("Czego się uczysz:", ["Polski na Angielski", "Angielski na Polski"])

    # Mapowanie kierunku tłumaczenia
    t_source = 'pl' if "Polski" in wybrany_tryb else 'en'
    t_target = 'en' if "Polski" in wybrany_tryb else 'pl'

# INICJALIZACJA SESJI
if ('aktualny_rozdzial' not in st.session_state or
        st.session_state.aktualny_rozdzial != wybrany_numer or
        st.session_state.ostatni_tryb != wybrany_tryb):
    st.session_state.aktualny_rozdzial = wybrany_numer
    st.session_state.ostatni_tryb = wybrany_tryb
    
    # Nazwa pliku musi się zgadzać z tym, co masz w Dataset na HF
    nazwa_pliku = f'ang_kl4_rozdzial{wybrany_numer}.csv'
    st.session_state.lista_slowek = laduj_slowka(nazwa_pliku)

    if st.session_state.lista_slowek:
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
        st.balloons()
        st.header("Koniec nauki!")
        st.success(f"Twój wynik końcowy to: {st.session_state.punkty} na {ile_wszystkich}")

        if st.button("Powtórz ten rozdział?"):
            st.session_state.index = 0
            st.session_state.punkty = 0
            st.session_state.feedback = None
            random.shuffle(st.session_state.lista_slowek)
            st.rerun()
else:
    st.warning("Wybierz rozdział, aby rozpocząć naukę.")

# --- STOPKA ---
st.divider()
st.caption("Najcierpliwszy portal do angielskiego - klasa 4")
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")
