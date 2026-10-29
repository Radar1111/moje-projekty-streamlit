import os
import random
import pandas as pd
import streamlit as st
from huggingface_hub import hf_hub_download

#  ŁADOWANIE DANYCH Z HUGGING FACE 

@st.cache_data(ttl=3600)
def load_words():
    try:
        # Bezpieczne sprawdzenie i pobranie tokenu bez używania metody .get()
        token = None
        if "HF_TOKEN" in st.secrets:
            token = st.secrets["HF_TOKEN"]
        elif os.getenv("HF_TOKEN"):
            token = os.getenv("HF_TOKEN")
        
        if not token:
            st.warning("Brak tokenu HF_TOKEN w sekretach aplikacji (w pliku secrets.toml lub ustawieniach chmury).")

        # Pobranie pliku z prywatnego repozytorium do cache lokalnego
        lokalna_sciezka = hf_hub_download(
            repo_id="Radar1111/Sasiedzi1",
            filename="jezyki_slowa.csv",
            repo_type="dataset",
            token=token
        )
        
        # Odczyt pliku przez Pandas
        dane = pd.read_csv(lokalna_sciezka, sep=',', encoding='utf-8-sig')
        dane.columns = dane.columns.str.strip()
        return dane
        
    except Exception as e:
        # W razie jakiegokolwiek innego błędu, Streamlit pokaże go na ekranie, ułatwiając debugowanie
        st.error(f"Błąd krytyczny pobierania: {e}")
        return pd.DataFrame(columns=['rozdzial', 'polski', 'czeski', 'słowacki', 'węgierski', 'rumuński', 'łotewski'])
        
@st.cache_data(ttl=3600)
def load_sentences():
    try:
        # Bezpieczne sprawdzenie i pobranie tokenu bez używania metody .get()
        token = None
        if "HF_TOKEN" in st.secrets:
            token = st.secrets["HF_TOKEN"]
        elif os.getenv("HF_TOKEN"):
            token = os.getenv("HF_TOKEN")
        
        if not token:
            st.warning("Brak tokenu HF_TOKEN w sekretach aplikacji (w pliku secrets.toml lub ustawieniach chmury).")

        # Pobranie pliku z prywatnego repozytorium do cache lokalnego
        lokalna_sciezka = hf_hub_download(
            repo_id="Radar1111/Sasiedzi1",
            filename="jezyki_zdania.csv",
            repo_type="dataset",
            token=token
        )
        
        # Odczyt pliku przez Pandas
        dane = pd.read_csv(lokalna_sciezka, sep=',', encoding='utf-8-sig')
        dane.columns = dane.columns.str.strip()
        return dane
        
    except Exception as e:
        # W razie jakiegokolwiek innego błędu, Streamlit pokaże go na ekranie, ułatwiając debugowanie
        st.error(f"Błąd krytyczny pobierania zdań: {e}")
        return pd.DataFrame(columns=['rozdzial', 'polski', 'czeski', 'słowacki', 'węgierski', 'rumuński', 'łotewski'])

# Wywołanie funkcji
baza_slowa = load_words()
baza_zdania = load_sentences()

if 'score' not in st.session_state:
    st.session_state.score = 0

if 'total' not in st.session_state:
    st.session_state.total = 0

if 'input_val' not in st.session_state:
    st.session_state.input_val = ""

def wyswietl_sekcje_wsparcia():
    # Inicjalizacja sesji wewnątrz funkcji (bezpieczne dla każdej strony)
    if "parent_verified" not in st.session_state:
        st.session_state.parent_verified = False
    if "num1" not in st.session_state:
        st.session_state.num1 = random.randint(5, 15)
    if "num2" not in st.session_state:
        st.session_state.num2 = random.randint(5, 15)

    LINK_DO_KAWY = "https://buycoffee.to/gigawiedza"

    # Separator odcinający treść edukacyjną
    st.divider()

    # Expander wsparcia
    with st.expander("👪 Dla Rodziców / Starszych Uczniów (Strefa Wspierania)"):
        if not st.session_state.parent_verified:
            st.write("Aby wejść, potwierdź że jesteś osobą dorosłą:")
            pytanie = f"Ile to jest {st.session_state.num1} + {st.session_state.num2}?"
            
            # Użycie unikalnego klucza w widgetach zapobiega konfliktom w Streamlit
            odpowiedz_rodzica = st.number_input(pytanie, step=1, value=0, key="footer_parent_input")

            if st.button("Zatwierdź", key="footer_parent_btn", use_container_width=True):
                poprawny_wynik = st.session_state.num1 + st.session_state.num2
                if odpowiedz_rodzica == poprawny_wynik:
                    st.session_state.parent_verified = True
                    st.rerun()
                else:
                    st.error("Nieprawidłowy wynik. Spróbuj ponownie!")
        else:
            st.success("Weryfikacja pomyślna!")
            st.markdown(
                """
                **Drogi Rodzicu / Starszy Uczniu!**  
                Tworzę te aplikacje z myślą o bezpiecznym i skutecznym rozwoju oraz nauce. 
                Udostępniam je całkowicie **za darmo i bez reklam**.
                
                Utrzymanie projektów wymaga jednak realnych kosztów i setek godzin pracy. 
                Jeśli aplikacja pomogła w nauce i chcesz wesprzeć rozwój kolejnych programów 
                – możesz postawić mi wirtualną kawę. Dziękuję!
                """
            )
            st.link_button("☕ Postaw wirtualną kawę", LINK_DO_KAWY, type="primary", use_container_width=True)
            
            if st.button("Zablokuj strefę", type="secondary", use_container_width=True, key="footer_lock_btn"):
                st.session_state.parent_verified = False
                st.session_state.num1 = random.randint(5, 15)
                st.session_state.num2 = random.randint(5, 15)
                st.rerun()

            st.caption(
            "**Informacja o wsparciu:** "
            "Wszelkie wpłaty realizowane za pośrednictwem platformy BuyCoffee.to mają charakter "
            "całkowicie dobrowolnego, bezinteresownego wsparcia (darowizny) na rzecz dalszego rozwoju "
            "i utrzymania portfolio bezpłatnych aplikacji. Wpłata nie wiąże się z zakupem żadnych "
            "cyfrowych towarów, usług ani dodatkowych funkcji w aplikacji."
        )

st.sidebar.header("Ustawienia aplikacji")
lang_map = {
    "Czeski": {"slowo": "czeski", "wymowa": "czeski_wym"},
    "Słowacki": {"slowo": "słowacki", "wymowa": "słowacki_wym"},
    "Węgierski": {"slowo": "węgierski", "wymowa": "węgierski_wym"},
    "Rumuński": {"slowo": "rumuński", "wymowa": "rumuński_wym"},
    "Łotewski": {"slowo": "łotewski", "wymowa": "łotewski_wym"}
}

wybrany_jezyk = st.sidebar.selectbox("Wybierz jezyk", list(lang_map.keys()))
kolumna_jezyk = lang_map[wybrany_jezyk]

with st.sidebar:
    wyswietl_sekcje_wsparcia()

st.title(f"Nauka jezyka: {wybrany_jezyk}")
tab_slowka, tab_zdania = st.tabs(["Slowka", "Zdania"])

with tab_slowka:
    if baza_slowa.empty:
        st.warning("Tabela jest pusta. Sprawdz komunikat bledu powyzej.")
    else:
        baza_slowa['rozdzial'] = pd.to_numeric(baza_slowa['rozdzial'], errors='coerce')
        baza_slowa = baza_slowa.dropna(subset=['rozdzial'])
        
        min_r = int(baza_slowa['rozdzial'].min())
        max_r = int(baza_slowa['rozdzial'].max())

        nr_roz = min_r
        # UNIKALNY KLUCZ: "s_slider_w"
        if min_r < max_r:
            nr_roz = st.slider("Wybierz rozdzial", min_r, max_r, key="s_slider_w")

        dane_roz = baza_slowa[baza_slowa['rozdzial'] == nr_roz]
        # UNIKALNY KLUCZ: "mode_s_w"
        tryb_s = st.radio("Wybierz tryb pracy:", ["Nauka", "Quiz"], horizontal=True, key="mode_s_w")

        czysty_jezyk = kolumna_jezyk.get("slowo") if isinstance(kolumna_jezyk, dict) else kolumna_jezyk
        kolumna_wymowa = kolumna_jezyk.get("wymowa") if isinstance(kolumna_jezyk, dict) else f"{czysty_jezyk}_wym"

        if tryb_s == "Nauka":
            kolumny_do_tabeli = ['polski']
            if czysty_jezyk in dane_roz.columns:
                kolumny_do_tabeli.append(czysty_jezyk)
            if kolumna_wymowa in dane_roz.columns:
                kolumny_do_tabeli.append(kolumna_wymowa)

            if len(kolumny_do_tabeli) > 1:
                st.table(dane_roz[kolumny_do_tabeli])
            else:
                st.error(f"Nie znaleziono kolumny '{czysty_jezyk}' w pliku CSV. Dostępne kolumny: {list(dane_roz.columns)}")
        
        else: # TRYB QUIZ (ABCD)
            # Inicjalizacja liczników w st.session_state (jeśli nie istnieją)
            if 'total' not in st.session_state: st.session_state.total = 0
            if 'score' not in st.session_state: st.session_state.score = 0

            # Losowanie nowego słowa - UNIKALNE KLUCZE stanu dla słówek
            if st.session_state.get('last_id_w') != nr_roz or 'opcje_abcd_w' not in st.session_state:
                if dane_roz.empty:
                    st.error("Brak danych dla tego rozdziału!")
                else:
                    st.session_state.slowo_id_w = random.choice(dane_roz.index)
                    st.session_state.last_id_w = nr_roz
                    
                    poprawna = str(dane_roz.loc[st.session_state.slowo_id_w, czysty_jezyk]).strip()
                    
                    inne_slowa = dane_roz[czysty_jezyk].dropna().astype(str).str.strip().unique()
                    inne_slowa = [s for s in inne_slowa if s.lower() != poprawna.lower()]
                    
                    liczba_blednych = min(3, len(inne_slowa))
                    bledne = random.sample(inne_slowa, liczba_blednych) if liczba_blednych > 0 else []
                    
                    wszystkie_opcje = bledne + [poprawna]
                    random.shuffle(wszystkie_opcje)
                    
                    st.session_state.opcje_abcd_w = wszystkie_opcje
                    st.session_state.poprawna_odp_w = poprawna
                    st.session_state.wybrana_odp_w = None
                    st.session_state.odpowiedziano_w = False # Blokada wielokrotnego zliczania

            if 'slowo_id_w' in st.session_state and st.session_state.slowo_id_w in dane_roz.index:
                slowo_pl = dane_roz.loc[st.session_state.slowo_id_w, 'polski']

                with st.container(border=True):
                    st.subheader(f"Jak przetlumaczysz: {slowo_pl}?")

                    col1, col2 = st.columns(2)
                    opcje = st.session_state.opcje_abcd_w
                    
                    for idx, opcja in enumerate(opcje):
                        target_col = col1 if idx % 2 == 0 else col2
                        
                        # Przyciski blokują się po jednym kliknięciu. UNIKALNY KLUCZ: "btn_opt_w_{idx}"
                        if target_col.button(opcja, use_container_width=True, key=f"btn_opt_w_{idx}", disabled=st.session_state.odpowiedziano_w):
                            st.session_state.wybrana_odp_w = opcja
                            st.session_state.odpowiedziano_w = True
                            
                            # Bezpieczne, jednorazowe naliczenie punktów
                            st.session_state.total += 1
                            if opcja.lower() == st.session_state.poprawna_odp_w.lower():
                                st.session_state.score += 1

                    # Wyświetlenie informacji zwrotnej
                    if st.session_state.wybrana_odp_w is not None:
                        user_ans = st.session_state.wybrana_odp_w
                        poprawna = st.session_state.poprawna_odp_w
                        
                        if user_ans.lower() == poprawna.lower():
                            st.success(f"Prawidlowo! Wynik: {poprawna}")
                        else:
                            st.error(f"Blad. Twoja odpowiedź: '{user_ans}'. Prawidlowa odpowiedz to: {poprawna}")
                        
                        st.write(f"Twój ogólny wynik: {st.session_state.score} / {st.session_state.total}")

                        # Przycisk przejścia dalej. UNIKALNY KLUCZ: "next_btn_w"
                        if st.button("Nastepne pytanie", use_container_width=True, type="primary", key="next_btn_w"):
                            del st.session_state.opcje_abcd_w
                            st.rerun()
with tab_zdania:
    if baza_zdania.empty:
        st.warning("Tabela jest pusta. Sprawdz komunikat bledu powyzej.")
    else:
        # --- TYMCZASOWY DEBUGGER ---
        st.write("Format kolumn przed konwersją:", baza_zdania.columns.tolist())
        st.write("Pierwsze wiersze kolumny rozdzial:", baza_zdania['rozdzial'].head())
        # ---------------------------
        # 1. Konwersja i usuwanie NaN
        baza_zdania['rozdzial'] = pd.to_numeric(baza_zdania['rozdzial'], errors='coerce')
        baza_zdania = baza_zdania.dropna(subset=['rozdzial'])
        
        # 2. DODATKOWE ZABEZPIECZENIE: Sprawdzenie, czy po czyszczeniu cokolwiek zostało
        if baza_zdania.empty:
            st.error("Błąd: Kolumna 'rozdzial' nie zawiera żadnych poprawnych numerów rozdziałów.")
        else:
            # Teraz wywołanie min() i max() jest w 100% bezpieczne
            min_r = int(baza_zdania['rozdzial'].min())
            max_r = int(baza_zdania['rozdzial'].max())

            nr_roz = min_r
            # UNIKALNY KLUCZ: "s_slider_w"
            if min_r < max_r:
                nr_roz = st.slider("Wybierz rozdzial", min_r, max_r, key="s_slider_w")

            dane_roz = baza_zdania[baza_zdania['rozdzial'] == nr_roz]
        # UNIKALNY KLUCZ: "mode_s_w"
        tryb_s = st.radio("Wybierz tryb pracy:", ["Nauka", "Quiz"], horizontal=True, key="mode_s_w_zdania")

        czysty_jezyk = kolumna_jezyk.get("zdanie") if isinstance(kolumna_jezyk, dict) else kolumna_jezyk
        kolumna_wymowa = kolumna_jezyk.get("wymowa") if isinstance(kolumna_jezyk, dict) else f"{czysty_jezyk}_wym"

        if tryb_s == "Nauka":
            kolumny_do_tabeli = ['polski']
            if czysty_jezyk in dane_roz.columns:
                kolumny_do_tabeli.append(czysty_jezyk)
            if kolumna_wymowa in dane_roz.columns:
                kolumny_do_tabeli.append(kolumna_wymowa)

            if len(kolumny_do_tabeli) > 1:
                st.table(dane_roz[kolumny_do_tabeli])
            else:
                st.error(f"Nie znaleziono kolumny '{czysty_jezyk}' w pliku CSV. Dostępne kolumny: {list(dane_roz.columns)}")
        
        else: # TRYB QUIZ (ABCD)
            # Inicjalizacja liczników w st.session_state (jeśli nie istnieją)
            if 'total' not in st.session_state: st.session_state.total = 0
            if 'score' not in st.session_state: st.session_state.score = 0

            # Losowanie nowego słowa - UNIKALNE KLUCZE stanu dla słówek
            if st.session_state.get('last_id_w') != nr_roz or 'opcje_abcd_w' not in st.session_state:
                if dane_roz.empty:
                    st.error("Brak danych dla tego rozdziału!")
                else:
                    st.session_state.slowo_id_w = random.choice(dane_roz.index)
                    st.session_state.last_id_w = nr_roz
                    
                    poprawna = str(dane_roz.loc[st.session_state.slowo_id_w, czysty_jezyk]).strip()
                    
                    inne_slowa = dane_roz[czysty_jezyk].dropna().astype(str).str.strip().unique()
                    inne_slowa = [s for s in inne_slowa if s.lower() != poprawna.lower()]
                    
                    liczba_blednych = min(3, len(inne_slowa))
                    bledne = random.sample(inne_slowa, liczba_blednych) if liczba_blednych > 0 else []
                    
                    wszystkie_opcje = bledne + [poprawna]
                    random.shuffle(wszystkie_opcje)
                    
                    st.session_state.opcje_abcd_w = wszystkie_opcje
                    st.session_state.poprawna_odp_w = poprawna
                    st.session_state.wybrana_odp_w = None
                    st.session_state.odpowiedziano_w = False # Blokada wielokrotnego zliczania

            if 'slowo_id_w' in st.session_state and st.session_state.slowo_id_w in dane_roz.index:
                slowo_pl = dane_roz.loc[st.session_state.slowo_id_w, 'polski']

                with st.container(border=True):
                    st.subheader(f"Jak przetlumaczysz: {slowo_pl}?")

                    col1, col2 = st.columns(2)
                    opcje = st.session_state.opcje_abcd_w
                    
                    for idx, opcja in enumerate(opcje):
                        target_col = col1 if idx % 2 == 0 else col2
                        
                        # Przyciski blokują się po jednym kliknięciu. UNIKALNY KLUCZ: "btn_opt_w_{idx}"
                        if target_col.button(opcja, use_container_width=True, key=f"btn_opt_w_{idx}", disabled=st.session_state.odpowiedziano_w):
                            st.session_state.wybrana_odp_w = opcja
                            st.session_state.odpowiedziano_w = True
                            
                            # Bezpieczne, jednorazowe naliczenie punktów
                            st.session_state.total += 1
                            if opcja.lower() == st.session_state.poprawna_odp_w.lower():
                                st.session_state.score += 1

                    # Wyświetlenie informacji zwrotnej
                    if st.session_state.wybrana_odp_w is not None:
                        user_ans = st.session_state.wybrana_odp_w
                        poprawna = st.session_state.poprawna_odp_w
                        
                        if user_ans.lower() == poprawna.lower():
                            st.success(f"Prawidlowo! Wynik: {poprawna}")
                        else:
                            st.error(f"Blad. Twoja odpowiedź: '{user_ans}'. Prawidlowa odpowiedz to: {poprawna}")
                        
                        st.write(f"Twój ogólny wynik: {st.session_state.score} / {st.session_state.total}")

                        # Przycisk przejścia dalej. UNIKALNY KLUCZ: "next_btn_w"
                        if st.button("Nastepne pytanie", use_container_width=True, type="primary", key="next_btn_w"):
                            del st.session_state.opcje_abcd_w
                            st.rerun()

st.caption("Najcierpliwszy portal do nauki języków obcych")
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")
