import streamlit as st
from datasets import load_dataset
import random

st.set_page_config(page_title="Apka do Słówek", page_icon="✏️")
st.title("Moja Nauka Słówek")

def laduj_slowka(nazwa_pliku):
    """Pobiera bazę słów z Hugging Face Dataset"""
    try:
        repo_id = "Radar1111/angielski-klasa-4" 
        dataset = load_dataset(
            repo_id, 
            data_files=nazwa_pliku, 
            token=st.secrets["HF_TOKEN"]
        )
        
        pobrane_dane = []
        for wiersz in dataset['train']:
            # strip() usuwa zbędne spacje
            pobrane_dane.append({'pl': wiersz['pl'].strip(), 'en': wiersz['en'].strip()})
        return pobrane_dane
    except Exception as e:
        st.error(f"Problem z połączeniem lub brakiem pliku: {e}")
        return []

def sprawdz_i_dalej(klucz):
    """Funkcja sprawdza odpowiedź pobraną z dynamicznego klucza"""
    if klucz not in st.session_state:
        return
        
    odp_usera = st.session_state[klucz].lower().strip()
    
    if not odp_usera:
        st.warning("Wpisz coś zanim sprawdzisz!")
        return

    prawidlowe = st.session_state.lista_slowek[st.session_state.index][st.session_state.target_lang]

    if odp_usera == prawidlowe.lower().strip():
        st.session_state.feedback = ("dobrze", f"Super! '{prawidlowe}' to poprawna odpowiedź.")
        st.session_state.punkty += 1
    else:
        st.session_state.feedback = ("zle", f"Niestety nie. Miało być: {prawidlowe}")

    # Przeskakujemy do kolejnego elementu
    st.session_state.index += 1

# PANEL BOCZNY (SIDEBAR)
with st.sidebar:
    st.header("Panel sterowania")
    wybrany_numer = st.selectbox("Który rozdział?", range(1, 22)) 
    wybrany_tryb = st.radio("Czego się uczysz:", ["Polski na Angielski", "Angielski na Polski"])

    # NAPRAWIONE MAPOWANIE JĘZYKÓW
    if wybrany_tryb == "Polski na Angielski":
        t_source = 'pl'
        t_target = 'en'
    else:
        t_source = 'en'
        t_target = 'pl'

# INICJALIZACJA SESJI
if ('aktualny_rozdzial' not in st.session_state or
        st.session_state.aktualny_rozdzial != wybrany_numer or
        st.session_state.ostatni_tryb != wybrany_tryb):
    
    st.session_state.aktualny_rozdzial = wybrany_numer
    st.session_state.ostatni_tryb = wybrany_tryb
    
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

    st.progress(ktore_teraz / ile_wszystkich if ile_wszystkich > 0 else 0)
    st.info(f"Pytanie {min(ktore_teraz + 1, ile_wszystkich)} z {ile_wszystkich} | Wynik: {st.session_state.punkty}")

    if ktore_teraz < ile_wszystkich:
        aktualna_para = st.session_state.lista_slowek[ktore_teraz]
        pytanie_txt = aktualna_para[st.session_state.source_lang]

        st.markdown(f"### Przetłumacz: **{pytanie_txt}**")

        # UNIKALNY KLUCZ DLA CZYSZCZENIA POLA
        klucz_pola = f"temp_odp_{st.session_state.index}"

        st.text_input(
            "Twoja propozycja:",
            key=klucz_pola,
            placeholder="Wpisz słowo...",
            autocomplete="off"
        )

        if st.button("Sprawdź i następne ➔", use_container_width=True, type="primary"):
            sprawdz_i_dalej(klucz_pola)
            st.rerun()

        if st.session_state.feedback:
            typ, tresc = st.session_state.feedback
            if typ == "dobrze":
                st.success(tresc)
            else:
                st.error(tresc)
    else:
        st.balloons()
        st.header("Koniec nauki!")
        st.success(f"Wynik: {st.session_state.punkty}/{ile_wszystkich}")
        if st.button("Powtórz rozdział", use_container_width=True):
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
