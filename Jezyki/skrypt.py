import streamlit as st
import pandas as pd
import random
import os

st.set_page_config(page_title="Master Jezykow", layout="wide")

SPECIAL_CHARS = {
    "Niemiecki": ["ä", "ö", "ü", "ß"],
    "Hiszpański": ["á", "é", "í", "ó", "ú", "ü", "ñ", "¿", "¡"],
    "Francuski": ["à", "â", "ç", "é", "è", "ê", "ë", "î", "ï", "ô", "û", "ù", "œ"],
    "Włoski": ["à", "è", "é", "ì", "ò", "ó", "ù"],
    "Angielski": []
}

URL_SLOWA = "https://huggingface.co/datasets/Radar1111/baza-jezykowa/raw/main/jezyki_slowa.csv"
URL_ZDANIA = "https://huggingface.co/datasets/Radar1111/baza-jezykowa/raw/main/jezyki_zdania.csv"

@st.cache_data(ttl=3600)
def load_words():
    try:
        token = st.secrets.get("HF_TOKEN") if "HF_TOKEN" in st.secrets else os.getenv("HF_TOKEN")
        naglowki_auth = {"Authorization": f"Bearer {token}"} if token else None
        
        naglowki = list(pd.read_csv(URL_SLOWA, storage_options=naglowki_auth, nrows=0).columns)
        dane = pd.read_csv(
            URL_SLOWA, 
            sep=',', 
            encoding='utf-8-sig', 
            storage_options=naglowki_auth,
            usecols=range(len(naglowki))
        )
        dane.columns = dane.columns.str.strip()
        return dane
    except Exception as e:
        st.error(f"Problem z pobraniem bazy z Hugging Face: {e}")
        return pd.DataFrame(columns=['rozdzial', 'polski', 'angielsk', 'niemiecki', 'hiszpanski', 'wloski', 'francuski'])


@st.cache_data(ttl=3600)
def load_sentences():
    try:
        token = st.secrets.get("HF_TOKEN") if "HF_TOKEN" in st.secrets else os.getenv("HF_TOKEN")
        naglowki_auth = {"Authorization": f"Bearer {token}"} if token else None
        
        naglowki = list(pd.read_csv(URL_ZDANIA, storage_options=naglowki_auth, nrows=0).columns)
        dane = pd.read_csv(
            URL_ZDANIA, 
            sep=',', 
            encoding='utf-8-sig', 
            storage_options=naglowki_auth,
            usecols=range(len(naglowki))
        )
        dane.columns = dane.columns.str.strip()
        return dane
    except Exception as e:
        st.error(f"Szczegóły błędu pobierania zdań: {e}")
        return pd.DataFrame(columns=['rozdzial', 'polski', 'angielski', 'niemiecki', 'hiszpanski', 'wloski', 'francuski'])

baza_slowa = load_words()
baza_zdania = load_sentences()

# Inicjalizacja podstawowych zmiennych stanu
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'total' not in st.session_state:
    st.session_state.total = 0

# Zmienne stanu dla losowania pytań i odpowiedzi ABCD
if 'slowo_id' not in st.session_state:
    st.session_state.slowo_id = None
if 'opcje_s' not in st.session_state:
    st.session_state.opcje_s = []
if 'sprawdzone_s' not in st.session_state:
    st.session_state.sprawdzone_s = False

if 'zdanie_id' not in st.session_state:
    st.session_state.zdanie_id = None
if 'opcje_z' not in st.session_state:
    st.session_state.opcje_z = []
if 'sprawdzone_z' not in st.session_state:
    st.session_state.sprawdzone_z = False

st.sidebar.header("Ustawienia aplikacji")

lang_map = {
    "Angielski": {"slowo": "angielsk", "wymowa": "angielsk_wym"},
    "Niemiecki": {"slowo": "niemiecki", "wymowa": "niemiecki_wym"},
    "Hiszpanski": {"slowo": "hiszpanski", "wymowa": "hiszpanski_wym"},
    "Wloski": {"slowo": "wloski", "wymowa": "wloski_wym"},
    "Francuski": {"slowo": "francuski", "fancy_wym": "francuski_wym"}
}

wybrany_jezyk = st.sidebar.selectbox("Wybierz jezyk", list(lang_map.keys()))

kolumna_jezyk = lang_map[wybrany_jezyk]["slowo"]
kolumna_wymowa = lang_map[wybrany_jezyk].get("wymowa") or lang_map[wybrany_jezyk].get("fancy_wym")

st.title(f"Nauka jezyka: {wybrany_jezyk}")

# Licznik punktów na górze ekranu
st.write(f"📊 Wynik: **{st.session_state.score}** / {st.session_state.total}")

tab_slowka, tab_zdania = st.tabs(["Slowka", "Zdania"])

# Funkcja pomocnicza do generowania opcji ABCD
def generuj_opcje(baza_filtrowana, poprawna_odp, kolumna):
    wszystkie_odp = baza_filtrowana[kolumna].dropna().astype(str).str.strip().unique().tolist()
    if poprawna_odp in wszystkie_odp:
        wszystkie_odp.remove(poprawna_odp)
    liczba_blednych = min(3, len(wszystkie_odp))
    bledne = random.sample(wszystkie_odp, liczba_blednych)
    pula = bledne + [poprawna_odp]
    random.shuffle(pula)
    return pula


# ==========================================
#  SŁÓWKA 
# ==========================================
with tab_slowka:
    if baza_slowa.empty:
        st.warning("Tabela słówek jest pusta lub plik CSV nie został wczytany.")
    elif kolumna_jezyk not in baza_slowa.columns:
        st.error(f"Nie znaleziono kolumny '{kolumna_jezyk}' w pliku słówek.")
    else:
        baza_slowa['rozdzial'] = pd.to_numeric(baza_slowa['rozdzial'], errors='coerce')
        baza_slowa = baza_slowa.dropna(subset=['rozdzial'])

        min_r = int(baza_slowa['rozdzial'].min())
        max_r = int(baza_slowa['rozdzial'].max())

        nr_roz = min_r
        if min_r < max_r:
            nr_roz = st.slider("Wybierz rozdzial", min_r, max_r, key="s_slider")

        dane_roz = baza_slowa[baza_slowa['rozdzial'] == nr_roz]
        tryb_s = st.radio("Wybierz tryb pracy:", ["Nauka", "Quiz ABCD"], horizontal=True, key="mode_s")

        if tryb_s == "Nauka":
            widoczne_kolumny = ['polski', kolumna_jezyk]
            if kolumna_wymowa in dane_roz.columns:
                widoczne_kolumny.append(kolumna_wymowa)
            st.table(dane_roz[widoczne_kolumny])
        else:
            # Losowanie słówka przy zmianie rozdziału, języka lub braku ID
            if (st.session_state.get('last_id') != nr_roz or
                    st.session_state.get('last_lang') != kolumna_jezyk or
                    st.session_state.get('slowo_id') not in dane_roz.index):
                st.session_state.slowo_id = random.choice(dane_roz.index)
                st.session_state.last_id = nr_roz
                st.session_state.last_lang = kolumna_jezyk
                st.session_state.sprawdzone_s = False
                if "wynik_s" in st.session_state: del st.session_state.wynik_s
                
                poprawna = str(baza_slowa.loc[st.session_state.slowo_id, kolumna_jezyk]).strip()
                st.session_state.opcje_s = generuj_opcje(dane_roz, poprawna, kolumna_jezyk)

            slowo_pl = baza_slowa.loc[st.session_state.slowo_id, 'polski']
            poprawna = str(baza_slowa.loc[st.session_state.slowo_id, kolumna_jezyk]).strip()

            with st.container(border=True):
                st.subheader(f"Jak przetlumaczysz: {slowo_pl}")

                # Wyłączenie radio po sprawdzeniu, żeby użytkownik nie zmieniał zaznaczenia
                wybor_s = st.radio(
                    "Wybierz poprawna odpowiedz:", 
                    st.session_state.opcje_s, 
                    key="radio_s", 
                    index=None, 
                    disabled=st.session_state.sprawdzone_s
                )

                c1, c2 = st.columns(2)
                
                # Przycisk "Sprawdź" działa tylko przed sprawdzeniem
                if c1.button("Sprawdz", key="chk_s", use_container_width=True, disabled=(wybor_s is None or st.session_state.sprawdzone_s)):
                    st.session_state.total += 1
                    st.session_state.sprawdzone_s = True
                    if wybor_s == poprawna:
                        st.session_state.score += 1
                        st.session_state.wynik_s = ("success", f"Prawidlowo! Odpowiedz to: {poprawna}")
                    else:
                        st.session_state.wynik_s = ("error", f"Blad. Twoja odpowiedz: {wybor_s}. Prawidlowa to: {poprawna}")
                    st.rerun()

                # Dynamiczna nazwa przycisku Następne
                tekst_nxt_s = "Nastepne" if st.session_state.sprawdzone_s else "Nastepne (Pomin)"
                if c2.button(tekst_nxt_s, key="nxt_s", use_container_width=True):
                    st.session_state.sprawdzone_s = False
                    if "wynik_s" in st.session_state: del st.session_state.wynik_s
                    
                    st.session_state.slowo_id = random.choice(dane_roz.index)
                    poprawna_nowa = str(baza_slowa.loc[st.session_state.slowo_id, kolumna_jezyk]).strip()
                    st.session_state.opcje_s = generuj_opcje(dane_roz, poprawna_nowa, kolumna_jezyk)
                    st.rerun()

                # Stałe wyświetlanie komunikatu pod przyciskami (nie znika przy odświeżeniu)
                if st.session_state.sprawdzone_s and "wynik_s" in st.session_state:
                    typ, tekst = st.session_state.wynik_s
                    if typ == "success": st.success(tekst)
                    else: st.error(tekst)

# ZDANIA
with tab_zdania:
    if baza_zdania.empty:
        st.warning("Tabela zdań jest pusta lub plik CSV nie został wczytany.")
    elif kolumna_jezyk not in baza_zdania.columns:
        st.error(f"Nie znaleziono kolumny '{kolumna_jezyk}' w pliku zdań.")
    else:
        baza_zdania['rozdzial'] = pd.to_numeric(baza_zdania['rozdzial'], errors='coerce')
        baza_zdania = baza_zdania.dropna(subset=['rozdzial'])

        min_z = int(baza_zdania['rozdzial'].min())
        max_z = int(baza_zdania['rozdzial'].max())

        nr_roz_z = min_z
        if min_z < max_z:
            nr_roz_z = st.slider("Wybierz rozdział", min_z, max_z, key="z_slider")

        dane_roz_z = baza_zdania[baza_zdania['rozdzial'] == nr_roz_z]
        tryb_z = st.radio("Wybierz tryb pracy:", ["Nauka", "Quiz ABCD"], horizontal=True, key="mode_z")

        if tryb_z == "Nauka":
            widoczne_kolumny_z = ['polski', kolumna_jezyk]
            if kolumna_wymowa in dane_roz_z.columns:
                widoczne_kolumny_z.append(kolumna_wymowa)
            st.table(dane_roz_z[widoczne_kolumny_z])
        else:
            # Losowanie zdania przy zmianie rozdziału, języka lub braku ID
            if (st.session_state.get('last_id_z') != nr_roz_z or
                    st.session_state.get('last_lang_z') != kolumna_jezyk or
                    st.session_state.get('zdanie_id') not in dane_roz_z.index):
                st.session_state.zdanie_id = random.choice(dane_roz_z.index)
                st.session_state.last_id_z = nr_roz_z
                st.session_state.last_lang_z = kolumna_jezyk
                st.session_state.sprawdzone_z = False
                if "wynik_z" in st.session_state: del st.session_state.wynik_z
                
                poprawna_z = str(baza_zdania.loc[st.session_state.zdanie_id, kolumna_jezyk]).strip()
                st.session_state.opcje_z = generuj_opcje(dane_roz_z, poprawna_z, kolumna_jezyk)

            zdanie_pl = baza_zdania.loc[st.session_state.zdanie_id, 'polski']
            poprawna_z = str(baza_zdania.loc[st.session_state.zdanie_id, kolumna_jezyk]).strip()

            with st.container(border=True):
                st.subheader(f"Jak przetłumaczysz zdanie: {zdanie_pl}")

                # Wyłączenie wyboru odpowiedzi po sprawdzeniu
                wybor_z = st.radio(
                    "Wybierz poprawna odpowiedz:", 
                    st.session_state.opcje_z, 
                    key="radio_z", 
                    index=None,
                    disabled=st.session_state.sprawdzone_z
                )

                c1, c2 = st.columns(2)
                
                # Przycisk "Sprawdź"
                if c1.button("Sprawdź", key="chk_z", use_container_width=True, disabled=(wybor_z is None or st.session_state.sprawdzone_z)):
                    st.session_state.total += 1
                    st.session_state.sprawdzone_z = True
                    if wybor_z == poprawna_z:
                        st.session_state.score += 1
                        st.session_state.wynik_z = ("success", f"Prawidłowo! Odpowiedź to: {poprawna_z}")
                    else:
                        st.session_state.wynik_z = ("error", f"Błąd. Twoja odpowiedź: {wybor_z}. Prawidłowa to: {poprawna_z}")
                    st.rerun()

                # Dynamiczny tekst przycisku Następne
                tekst_nxt_z = "Następne" if st.session_state.sprawdzone_z else "Następne (Pomiń)"
                if c2.button(tekst_nxt_z, key="nxt_z", use_container_width=True):
                    st.session_state.sprawdzone_z = False
                    if "wynik_z" in st.session_state: del st.session_state.wynik_z
                    
                    st.session_state.zdanie_id = random.choice(dane_roz_z.index)
                    poprawna_nowa_z = str(baza_zdania.loc[st.session_state.zdanie_id, kolumna_jezyk]).strip()
                    st.session_state.opcje_z = generuj_opcje(dane_roz_z, poprawna_nowa_z, kolumna_jezyk)
                    st.rerun()

                # Wyświetlanie komunikatu (nie znika przy odświeżeniu aplikacji)
                if st.session_state.sprawdzone_z and "wynik_z" in st.session_state:
                    typ, tekst = st.session_state.wynik_z
                    if typ == "success": st.success(tekst)
                    else: st.error(tekst)
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
