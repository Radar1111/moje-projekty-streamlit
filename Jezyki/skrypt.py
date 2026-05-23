import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Master Jezykow", layout="wide")

SPECIAL_CHARS = {
    "Niemiecki": ["ä", "ö", "ü", "ß"],
    "Hiszpański": ["á", "é", "í", "ó", "ú", "ü", "ñ", "¿", "¡"],
    "Francuski": ["à", "â", "ç", "é", "è", "ê", "ë", "î", "ï", "ô", "û", "ù", "œ"],
    "Włoski": ["à", "è", "é", "ì", "ò", "ó", "ù"],
    "Angielski": []
}


@st.cache_data
def load_words():
    try:
        # Najpierw czytamy tylko nagłówki, żeby znać oryginalne kolumny
        naglowki = list(pd.read_csv("jezyki_slowa.csv", nrows=0).columns)

        # Wczytujemy dane, ignorując nadmiarowe przecinki na końcach linii
        dane = pd.read_csv(
            "jezyki_slowa.csv",
            sep=',',
            encoding='utf-8-sig',
            usecols=range(len(naglowki))
        )
        dane.columns = dane.columns.str.strip()
        return dane
    except Exception as e:
        st.error(f"Problem z plikiem slowek: {e}")
        return pd.DataFrame(
            columns=['rozdzial', 'polski', 'angielsk', 'niemiecki', 'hiszpanski', 'wloski', 'francuski'])


@st.cache_data
def load_sentences():
    try:
        dane = pd.read_csv("jezyki_zdania.csv", sep=',', encoding='utf-8-sig')
        dane.columns = dane.columns.str.strip()
        return dane
    except Exception:
        return None


baza_slowa = load_words()
baza_zdania = load_sentences()

if 'score' not in st.session_state:
    st.session_state.score = 0

if 'total' not in st.session_state:
    st.session_state.total = 0

if 'input_val' not in st.session_state:
    st.session_state.input_val = ""

st.sidebar.header("Ustawienia aplikacji")
lang_map = {
    "Angielski": "angielsk",
    "Niemiecki": "niemiecki",
    "Hiszpański": "hiszpanski",
    "Włoski": "wloski",
    "Francuski": "francuski"
}
wybrany_jezyk = st.sidebar.selectbox("Wybierz jezyk", list(lang_map.keys()))
kolumna_jezyk = lang_map[wybrany_jezyk]

st.title(f"Nauka jezyka: {wybrany_jezyk}")
tab_slowka, tab_zdania = st.tabs(["Slowka", "Zdania"])

with tab_slowka:
    if baza_slowa.empty:
        st.warning("Tabela jest pusta. Sprawdz komunikat bledu powyzej.")
    else:
        # Konwersja kolumny na liczby, ignorując ewentualne teksty/błędy w pliku
        baza_slowa['rozdzial'] = pd.to_numeric(baza_slowa['rozdzial'], errors='coerce')
        baza_slowa = baza_slowa.dropna(subset=['rozdzial'])

        min_r = int(baza_slowa['rozdzial'].min())
        max_r = int(baza_slowa['rozdzial'].max())

        nr_roz = min_r
        if min_r < max_r:
            nr_roz = st.slider("Wybierz rozdzial", min_r, max_r, key="s_slider")

        dane_roz = baza_slowa[baza_slowa['rozdzial'] == nr_roz]
        tryb_s = st.radio("Wybierz tryb pracy:", ["Nauka", "Quiz"], horizontal=True, key="mode_s")

        if tryb_s == "Nauka":
            st.table(dane_roz[['polski', kolumna_jezyk]])
        else:
            if st.session_state.get('last_id') != nr_roz:
                st.session_state.slowo_id = random.choice(dane_roz.index)
                st.session_state.last_id = nr_roz
                st.session_state.input_val = ""

            slowo_pl = baza_slowa.loc[st.session_state.slowo_id, 'polski']
            poprawna = str(baza_slowa.loc[st.session_state.slowo_id, kolumna_jezyk])

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
                        st.success(f"Prawidlowo! Wynik: {poprawna}")
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
