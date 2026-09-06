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

# Wywołanie funkcji
baza_slowa = load_words()
baza_zdania = None  # Czeka na Twoje pliki ze zdaniami w przyszłości

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
        if min_r < max_r:
            nr_roz = st.slider("Wybierz rozdzial", min_r, max_r, key="s_slider")

        dane_roz = baza_slowa[baza_slowa['rozdzial'] == nr_roz]
        dane_roz = baza_slowa[baza_slowa['rozdzial'] == nr_roz]
        tryb_s = st.radio("Wybierz tryb pracy:", ["Nauka", "Quiz"], horizontal=True, key="mode_s")

        # Pobranie czystych nazw kolumn tekstowych ze słownika lang_map
        czysty_jezyk = kolumna_jezyk.get("slowo") if isinstance(kolumna_jezyk, dict) else kolumna_jezyk
        kolumna_wymowa = kolumna_jezyk.get("wymowa") if isinstance(kolumna_jezyk, dict) else f"{czysty_jezyk}_wym"

        if tryb_s == "Nauka":
            # Budujemy dynamiczną listę kolumn do wyświetlenia
            kolumny_do_tabeli = ['polski']
            
            if czysty_jezyk in dane_roz.columns:
                kolumny_do_tabeli.append(czysty_jezyk)
                
            if kolumna_wymowa in dane_roz.columns:
                kolumny_do_tabeli.append(kolumna_wymowa)

            # Wyświetlamy tabelę, jeśli znaleźliśmy przynajmniej kolumnę językową
            if len(kolumny_do_tabeli) > 1:
                st.table(dane_roz[kolumny_do_tabeli])
            else:
                st.error(f"Nie znaleziono kolumny '{czysty_jezyk}' w pliku CSV. Dostępne kolumny: {list(dane_roz.columns)}")
        else:
            if st.session_state.get('last_id') != nr_roz:
                st.session_state.slowo_id = random.choice(dane_roz.index)
                st.session_state.last_id = nr_roz
                st.session_state.input_val = ""

            slowo_pl = baza_slowa.loc[st.session_state.slowo_id, 'polski']
            poprawna = str(baza_slowa.loc[st.session_state.slowo_id, czysty_jezyk])
            
            wymowa_txt = ""
            if kolumna_wymowa in baza_slowa.columns:
                wymowa_txt = str(baza_slowa.loc[st.session_state.slowo_id, kolumna_wymowa])
                else:
                    st.warning("Wybierz język w panelu bocznym, aby wyświetlić tabelę.")
        else:
            if st.session_state.get('last_id') != nr_roz:
                st.session_state.slowo_id = random.choice(dane_roz.index)
                st.session_state.last_id = nr_roz
                st.session_state.input_val = ""

            slowo_pl = baza_slowa.loc[st.session_state.slowo_id, 'polski']
            poprawna = str(baza_slowa.loc[st.session_state.slowo_id, kolumna_jezyk])
            
            wymowa_txt = ""
            if kolumna_wymowa in baza_slowa.columns:
                wymowa_txt = str(baza_slowa.loc[st.session_state.slowo_id, kolumna_wymowa])

            with st.container(border=True):
                st.subheader(f"Jak przetlumaczysz: {slowo_pl}?")

                znaki = SPECIAL_CHARS.get(wybrany_jezyk, [])
                if znaki:
                    cols = st.columns(len(znaki) + 1)
                    for i, z in enumerate(znaki):
                        if cols[i].button(z, key=f"btn_{z}"):
                            st.session_state.input_val += z
                            st.rerun()
                    if cols[-1].button("Usun", help="Cofnij ostatni znak"):
                        st.session_state.input_val = st.session_state.input_val[:-1]
                        st.rerun()

                user_ans = st.text_input("Twoja odpowiedz:", value=st.session_state.input_val)
                st.session_state.input_val = user_ans

                c1, c2 = st.columns(2)
                if c1.button("Sprawdz", use_container_width=True):
                    st.session_state.total += 1
                    if user_ans.lower().strip() == poprawna.lower().strip():
                        komunikat = f"Prawidlowo! Wynik: {poprawna}"
                        if wymowa_txt and wymowa_txt.lower() != 'nan':
                            komunikat += f" (Wymowa: [{wymowa_txt}])"
                        st.success(komunikat)
                        
                        st.session_state.score += 1
                        st.session_state.slowo_id = random.choice(dane_roz.index)
                        st.session_state.input_val = ""
                        st.rerun()
                    else:
                        st.error(f"Blad. Prawidlowa odpowiedz to: {poprawna}")

                if c2.button("Nastepne", use_container_width=True):
                    st.session_state.slowo_id = random.choice(dane_roz.index)
                    st.session_state.input_val = ""
                    st.rerun()

st.divider()
st.metric("Statystyki odpowiedzi", f"{st.session_state.score} / {st.session_state.total}")
if st.button("Czysc statystyki"):
    st.session_state.score = 0
    st.session_state.total = 0
    st.rerun()

st.caption("Najcierpliwszy portal do nauki języków obcych")
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")
