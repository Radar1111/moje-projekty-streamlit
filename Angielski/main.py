import streamlit as st
from datasets import load_dataset
import random

st.set_page_config(page_title="Apka do Słówek", page_icon="✏️")
st.title("Moja Nauka Słówek")

# 1. MAPOWANIE NAZW ROZDZIAŁÓW NA PLIKI CSV
SŁOWNIK_ROZDZIAŁOW = {
    "Rozdział 1: Liczebniki (Numerals)": "ang_kl4_rozdzial1.csv",
    "Rozdział 2: Szkoła (School)": "ang_kl4_rozdzial2.csv",
    # Tutaj możesz dopisywać kolejne rozdziały według wzoru:
    # "Nazwa wyświetlana w menu": "nazwa_pliku_na_hf.csv"
}

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
            pobrane_dane.append({'pl': wiersz['pl'].strip(), 'en': wiersz['en'].strip()})
        return pobrane_dane
    except Exception as e:
        st.error(f"Problem z połączeniem lub brakiem pliku: {e}")
        return []

def sprawdz_odpowiedz():
    """Sprawdza wpisaną odpowiedź i blokuje ponowne sprawdzenie tego samego słowa"""
    klucz = f"temp_odp_{st.session_state.index}"
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
    
    st.session_state.sprawdzone = True

def nastepne_slowko():
    """Resetuje stan feedbacku i przechodzi do kolejnego słowa"""
    st.session_state.feedback = None
    st.session_state.sprawdzone = False
    st.session_state.index += 1

# PANEL BOCZNY (SIDEBAR)
with st.sidebar:
    st.header("Panel sterowania")
    
    # Wybór rozdziału za pomocą ładnej nazwy
    wybrany_opis = st.selectbox("Który rozdział?", list(SŁOWNIK_ROZDZIAŁOW.keys()))
    nazwa_pliku = SŁOWNIK_ROZDZIAŁOW[wybrany_opis] # Pobranie właściwej nazwy pliku .csv
    
    wybrany_tryb = st.radio("Czego się uczysz:", ["Polski na Angielski", "Angielski na Polski"])
    
    # 2. WYBÓR LICZBY SŁÓWEK
    wybrany_limit = st.selectbox("Ile słówek chcesz powtórzyć?", ["5", "10", "Wszystkie"])

    if wybrany_tryb == "Polski na Angielski":
        t_source = 'pl'
        t_target = 'en'
    else:
        t_source = 'en'
        t_target = 'pl'

# INICJALIZACJA SESJI LUB ZMIANA USTAWIEŃ
if ('aktualny_rozdzial' not in st.session_state or
        st.session_state.aktualny_rozdzial != nazwa_pliku or
        st.session_state.ostatni_tryb != wybrany_tryb or
        st.session_state.ostatni_limit != wybrany_limit):
    
    st.session_state.aktualny_rozdzial = nazwa_pliku
    st.session_state.ostatni_tryb = wybrany_tryb
    st.session_state.ostatni_limit = wybrany_limit
    
    wszystkie_slowka = laduj_slowka(nazwa_pliku)

    if wszystkie_slowka:
        random.shuffle(wszystkie_slowka)
        
        # 3. ZABEZPIECZENIE LICZBY SŁÓWEK
        if wybrany_limit == "Wszystkie":
            st.session_state.lista_slowek = wszystkie_slowka
        else:
            limit_int = int(wybrany_limit)
            # Jeśli w bazie jest mniej słówek niż żądany limit, bierzemy tylko tyle, ile jest dostępnych
            if len(wszystkie_slowka) < limit_int:
                st.session_state.lista_slowek = wszystkie_slowka
                st.sidebar.warning(f"Baza zawiera tylko {len(wszystkie_slowka)} słówek!")
            else:
                st.session_state.lista_slowek = wszystkie_slowka[:limit_int]
    else:
        st.session_state.lista_slowek = []
    
    st.session_state.index = 0
    st.session_state.punkty = 0
    st.session_state.feedback = None
    st.session_state.sprawdzone = False
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

        klucz_pola = f"temp_odp_{st.session_state.index}"

        st.text_input(
            "Twoja propozycja:",
            key=klucz_pola,
            placeholder="Wpisz słowo...",
            autocomplete="off",
            disabled=st.session_state.sprawdzone,
            on_change=sprawdz_odpowiedz if not st.session_state.sprawdzone else None
        )

        if not st.session_state.sprawdzone:
            if st.button("Sprawdź ➔", use_container_width=True, type="primary"):
                sprawdz_odpowiedz()
                st.rerun()
        else:
            if st.session_state.feedback:
                typ, tresc = st.session_state.feedback
                if typ == "dobrze":
                    st.success(tresc)
                else:
                    st.error(tresc)
            
            if st.button("Następne słówko ➔", use_container_width=True, type="secondary"):
                nastepne_slowko()
                st.rerun()
    else:
        st.balloons()
        st.header("Koniec nauki!")
        st.success(f"Wynik: {st.session_state.punkty}/{ile_wszystkich}")
        if st.button("Powtórz rozdział", use_container_width=True):
            st.session_state.index = 0
            st.session_state.punkty = 0
            st.session_state.feedback = None
            st.session_state.sprawdzone = False
            random.shuffle(st.session_state.lista_slowek)
            st.rerun()

# --- STOPKA ---
st.divider()
st.caption("Najcierpliwszy portal do angielskiego - klasa 4")
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")
