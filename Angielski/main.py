import streamlit as st
from datasets import load_dataset
import random

st.set_page_config(page_title="Apka do Słówek", page_icon="✏️")
st.title("Moja Nauka Słówek")

# 1. MAPOWANIE NAZW ROZDZIAŁÓW NA PLIKI CSV
SŁOWNIK_ROZDZIAŁOW = {
    "Rozdział 1: Liczebniki (Numerals)": "ang_kl4_rozdzial1.csv",
    "Rozdział 2: Szkoła (School)": "ang_kl4_rozdzial2.csv",
    "Rozdział 3: Owoce (Fruits)": "ang_kl4_rozdzial3.csv",
    "Rozdział 4: Warzywa (Vegetables)": "ang_kl4_rozdzial4.csv",
    "Rozdział 5: Rodzina (Family)": "ang_kl4_rozdzial5.csv",
    "Rozdział 6: Zwierzęta (Animals)": "ang_kl4_rozdzial6.csv",
    "Rozdział 7: Pokoje w domu (Rooms)": "ang_kl4_rozdzial7.csv",
    "Rozdział 8: Kolory (Colors)": "ang_kl4_rozdzial8.csv",
    "Rozdział 9: Części ciała (Body parts)": "ang_kl4_rozdzial9.csv",
    "Rozdział 10: Miejsca w szkole (School places)": "ang_kl4_rozdzial10.csv",
    "Rozdział 11: Polecenia nauczyciela (Teacher's instruction)": "ang_kl4_rozdzial11.csv",
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

def sprawdz_odpowiedz_wpisywanie():
    """Sprawdza wpisaną odpowiedź w trybie Wpisywania"""
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
    st.session_state.fiszka_obrocona = False
    st.session_state.opcje_abcd = []
    st.session_state.index += 1

# PANEL BOCZNY (SIDEBAR)
with st.sidebar:
    st.header("Panel sterowania")
    
    wybrany_opis = st.selectbox("Który rozdział?", list(SŁOWNIK_ROZDZIAŁOW.keys()))
    nazwa_pliku = SŁOWNIK_ROZDZIAŁOW[wybrany_opis]
    
    wybrany_tryb = st.radio("Czego się uczysz:", ["Polski na Angielski", "Angielski na Polski"])
    wybrany_limit = st.selectbox("Ile słówek chcesz powtórzyć?", ["5", "10", "Wszystkie"])
    
    # NOWOŚĆ: Wybór modułu nauki
    wybrany_modul = st.radio("Metoda nauki:", ["Fiszki 📇", "Test ABCD 🎯", "Wpisywanie ✏️"])

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
        st.session_state.ostatni_limit != wybrany_limit or
        st.session_state.ostatni_modul != wybrany_modul):
    
    st.session_state.aktualny_rozdzial = nazwa_pliku
    st.session_state.ostatni_tryb = wybrany_tryb
    st.session_state.ostatni_limit = wybrany_limit
    st.session_state.ostatni_modul = wybrany_modul
    
    wszystkie_slowka = laduj_slowka(nazwa_pliku)

    if wszystkie_slowka:
        random.shuffle(wszystkie_slowka)
        
        if wybrany_limit == "Wszystkie":
            st.session_state.lista_slowek = wszystkie_slowka
        else:
            limit_int = int(wybrany_limit)
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
    st.session_state.fiszka_obrocona = False
    st.session_state.opcje_abcd = []
    st.session_state.target_lang = t_target
    st.session_state.source_lang = t_source

# GŁÓWNY WIDOK APLIKACJI
if st.session_state.lista_slowek:
    ile_wszystkich = len(st.session_state.lista_slowek)
    ktore_teraz = st.session_state.index

    st.progress(ktore_teraz / ile_wszystkich if ile_wszystkich > 0 else 0)
    st.info(f"Metoda: {wybrany_modul} | Pytanie {min(ktore_teraz + 1, ile_wszystkich)} z {ile_wszystkich} | Wynik: {st.session_state.punkty}")

    if ktore_teraz < ile_wszystkich:
        aktualna_para = st.session_state.lista_slowek[ktore_teraz]
        pytanie_txt = aktualna_para[st.session_state.source_lang]
        prawidlowe_odp = aktualna_para[st.session_state.target_lang]

        #1. MODUŁ: FISZKI
        if wybrany_modul == "Fiszki 📇":
            st.markdown(f"### Słowo do przetłumaczenia:")
            st.info(f"## **{pytanie_txt}**")
            
            if not st.session_state.fiszka_obrocona:
                if st.button("Obróć fiszkę 🔄", use_container_width=True, type="primary"):
                    st.session_state.fiszka_obrocona = True
                    st.rerun()
            else:
                st.markdown("### Tłumaczenie:")
                st.success(f"## **{prawidlowe_odp}**")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Umiem 👍", use_container_width=True, type="primary"):
                        st.session_state.punkty += 1
                        nastepne_slowko()
                        st.rerun()
                with col2:
                    if st.button("Nie umiem 👎", use_container_width=True, type="secondary"):
                        nastepne_slowko()
                        st.rerun()

        # 2. MODUŁ: TEST ABCD
        elif wybrany_modul == "Test ABCD 🎯":
            st.markdown(f"### Przetłumacz: **{pytanie_txt}**")
            
            # Generowanie opcji ABCD, jeśli jeszcze nie zostały stworzone dla tego pytania
            if not st.session_state.opcje_abcd:
                pula_blednych = [s[st.session_state.target_lang] for s in st.session_state.lista_slowek if s[st.session_state.target_lang] != prawidlowe_odp]
                bledne_wylosowane = random.sample(pula_blednych, min(len(pula_blednych), 3))
                
                warianty = bledne_wylosowane + [prawidlowe_odp]
                random.shuffle(warianty)
                st.session_state.opcje_abcd = warianty
            
            # Formularz wyboru odpowiedzi
            with st.form("form_abcd"):
                odp_wybrana = st.radio("Wybierz poprawną odpowiedź:", st.session_state.opcje_abcd, index=None)
                przycisk_wyslij = st.form_submit_button("Sprawdź odpowiedź ➔", use_container_width=True, disabled=st.session_state.sprawdzone)
                
                if przycisk_wyslij:
                    if odp_wybrana is None:
                        st.warning("Zaznacz jedną z opcji przed sprawdzeniem!")
                    elif odp_wybrana == prawidlowe_odp:
                        st.session_state.feedback = ("dobrze", f"Doskonale! '{prawidlowe_odp}' to właściwy wybór.")
                        st.session_state.punkty += 1
                        st.session_state.sprawdzone = True
                    else:
                        st.session_state.feedback = ("zle", f"Błąd. Poprawna odpowiedź to: {prawidlowe_odp}")
                        st.session_state.sprawdzone = True
                    st.rerun()
            
            if st.session_state.sprawdzone:
                typ, tresc = st.session_state.feedback
                if typ == "dobrze":
                    st.success(tresc)
                else:
                    st.error(tresc)
                
                if st.button("Następne słówko ➔", use_container_width=True, type="secondary"):
                    nastepne_slowko()
                    st.rerun()

        # ==================== 3. MODUŁ: WPISYWANIE ====================
        elif wybrany_modul == "Wpisywanie ✏️":
            st.markdown(f"### Przetłumacz: **{pytanie_txt}**")
            klucz_pola = f"temp_odp_{st.session_state.index}"

            st.text_input(
                "Twoja propozycja:",
                key=klucz_pola,
                placeholder="Wpisz słowo...",
                autocomplete="off",
                disabled=st.session_state.sprawdzone,
                on_change=sprawdz_odpowiedz_wpisywanie if not st.session_state.sprawdzone else None
            )

            if not st.session_state.sprawdzone:
                if st.button("Sprawdź ➔", use_container_width=True, type="primary"):
                    sprawdz_odpowiedz_wpisywanie()
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
                    
    # TEN BLOK ODPOWIADA ZA KONIEC NAUKI (gdy ktore_teraz >= ile_wszystkich)
    else:
        st.balloons()
        st.header("Koniec nauki!")
        st.success(f"Wynik: {st.session_state.punkty}/{ile_wszystkich}")
        if st.button("Powtórz rozdział", use_container_width=True):
            st.session_state.index = 0
            st.session_state.punkty = 0
            st.session_state.feedback = None
            st.session_state.sprawdzone = False
            st.session_state.fiszka_obrocona = False
            st.session_state.opcje_abcd = []
            random.shuffle(st.session_state.lista_slowek)
            st.rerun()

# --- STOPKA ---
st.divider()
st.caption("Najcierpliwszy portal do angielskiego")
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")
