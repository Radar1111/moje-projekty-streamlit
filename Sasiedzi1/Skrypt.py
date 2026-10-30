import os
import random
import pandas as pd
import streamlit as st
from huggingface_hub import hf_hub_download

# ==========================================
# 1. ŁADOWANIE DANYCH Z HUGGING FACE
# ==========================================

@st.cache_data(ttl=3600)
def load_words():
    try:
        token = None
        if "HF_TOKEN" in st.secrets:
            token = st.secrets["HF_TOKEN"]
        elif os.getenv("HF_TOKEN"):
            token = os.getenv("HF_TOKEN")
        
        if not token:
            st.warning("Brak tokenu HF_TOKEN w sekretach aplikacji.")

        lokalna_sciezka = hf_hub_download(
            repo_id="Radar1111/Sasiedzi1",
            filename="jezyki_slowa.csv",
            repo_type="dataset",
            token=token
        )
        
        dane = pd.read_csv(lokalna_sciezka, sep=',', encoding='utf-8-sig')
        dane.columns = dane.columns.str.strip()
        return dane
        
    except Exception as e:
        st.error(f"Błąd krytyczny pobierania słówek: {e}")
        return pd.DataFrame(columns=['rozdzial', 'polski', 'czeski', 'słowacki', 'węgierski', 'rumuński', 'łotewski'])

@st.cache_data(ttl=3600)
def load_sentences():
    try:
        token = None
        if "HF_TOKEN" in st.secrets:
            token = st.secrets["HF_TOKEN"]
        elif os.getenv("HF_TOKEN"):
            token = os.getenv("HF_TOKEN")

        lokalna_sciezka = hf_hub_download(
            repo_id="Radar1111/Sasiedzi1",
            filename="jezyki_zdania.csv",
            repo_type="dataset",
            token=token
        )
        
        dane = pd.read_csv(lokalna_sciezka, sep=',', encoding='utf-8-sig')
        dane.columns = dane.columns.str.strip()
        return dane
        
    except Exception as e:
        st.error(f"Błąd krytyczny pobierania zdań: {e}")
        return pd.DataFrame(columns=['rozdzial', 'polski', 'czeski', 'słowacki', 'węgierski', 'rumuński', 'łotewski'])

baza_slowa = load_words()
baza_zdania = load_sentences()

# Inicjalizacja globalnych stanów gry
if 'score' not in st.session_state: st.session_state.score = 0
if 'total' not in st.session_state: st.session_state.total = 0
if 'quiz_answered_w' not in st.session_state: st.session_state.quiz_answered_w = False
if 'quiz_answered_z' not in st.session_state: st.session_state.quiz_answered_z = False

# ==========================================
# 2. STREFA WSPARCIA
# ==========================================

def wyswietl_sekcje_wsparcia():
    if "parent_verified" not in st.session_state:
        st.session_state.parent_verified = False
    if "num1" not in st.session_state:
        st.session_state.num1 = random.randint(5, 15)
    if "num2" not in st.session_state:
        st.session_state.num2 = random.randint(5, 15)

    LINK_DO_KAWY = "https://buycoffee.to"
    st.divider()

    with st.expander("👪 Dla Rodziców / Starszych Uczniów (Strefa Wspierania)"):
        if not st.session_state.parent_verified:
            st.write("Aby wejść, potwierdź że jesteś osobą dorosłą:")
            pytanie = f"Ile to jest {st.session_state.num1} + {st.session_state.num2}?"
            
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
                """
            )
            st.link_button("☕ Postaw wirtualną kawę", LINK_DO_KAWY, type="primary", use_container_width=True)
            
            if st.button("Zablokuj strefę", type="secondary", use_container_width=True, key="footer_lock_btn"):
                st.session_state.parent_verified = False
                st.session_state.num1 = random.randint(5, 15)
                st.session_state.num2 = random.randint(5, 15)
                st.rerun()

# ==========================================
# 3. PASEK BOCZNY I CONFIG
# ==========================================

st.sidebar.header("Ustawienia aplikacji")
lang_map = {
    "Czeski": {"slowo": "czeski", "wymowa": "czeski_wym"},
    "Słowacki": {"slowo": "słowacki", "wymowa": "słowacki_wym"},
    "Węgierski": {"slowo": "węgierski", "wymowa": "węgierski_wym"},
    "Rumuński": {"slowo": "rumuński", "wymowa": "rumuński_wym"},
    "Łotewski": {"slowo": "łotewski", "wymowa": "łotewski_wym"}
}

wybrany_jezyk = st.sidebar.selectbox("Wybierz język", list(lang_map.keys()))
kolumna_jezyk = lang_map[wybrany_jezyk]
czysty_jezyk = kolumna_jezyk.get("slowo")
kolumna_wymowa = kolumna_jezyk.get("wymowa")

with st.sidebar:
    wyswietl_sekcje_wsparcia()

st.title(f"Nauka języka: {wybrany_jezyk}")

# Globalny licznik punktów widoczny nad zakładkami
st.metric(label="Twój Ogólny Wynik", value=f"{st.session_state.score} / {st.session_state.total}")

tab_slowka, tab_zdania = st.tabs(["Słówka", "Zdania"])

# ==========================================
# 4. ZAKŁADKA: SŁÓWKA
# ==========================================
with tab_slowka:
    if baza_slowa.empty:
        st.warning("Tabela słówek jest pusta.")
    else:
        baza_slowa['rozdzial'] = pd.to_numeric(baza_slowa['rozdzial'], errors='coerce')
        baza_slowa = baza_slowa.dropna(subset=['rozdzial'])
        
        min_r = int(baza_slowa['rozdzial'].min())
        max_r = int(baza_slowa['rozdzial'].max())

        nr_roz = min_r
        if min_r < max_r:
            nr_roz = st.slider("Wybierz rozdział (Słówka)", min_r, max_r, key="s_slider_w")

        dane_roz = baza_slowa[baza_slowa['rozdzial'] == nr_roz]
        tryb_s = st.radio("Wybierz tryb pracy (Słówka):", ["Nauka", "Quiz"], horizontal=True, key="mode_s_w")

        if tryb_s == "Nauka":
            kolumny_do_tabeli = ['polski']
            if czysty_jezyk in dane_roz.columns: kolumny_do_tabeli.append(czysty_jezyk)
            if kolumna_wymowa in dane_roz.columns: kolumny_do_tabeli.append(kolumna_wymowa)
            st.table(dane_roz[kolumny_do_tabeli])
        
        else: # QUIZ SŁÓWKA
            if dane_roz.empty:
                st.error("Brak danych!")
            else:
                if st.session_state.get('last_id_w') != nr_roz:
                    st.session_state.last_id_w = nr_roz
                    if 'opcje_abcd_w' in st.session_state: del st.session_state.opcje_abcd_w
                    st.session_state.quiz_answered_w = False

                if 'opcje_abcd_w' not in st.session_state:
                    wybrany_wiersz = dane_roz.sample(n=1).iloc[0]
                    st.session_state.pytanie_pl_w = str(wybrany_wiersz['polski']).strip()
                    st.session_state.poprawna_odp_w = str(wybrany_wiersz[czysty_jezyk]).strip()
                    
                    pula = dane_roz[czysty_jezyk].dropna().astype(str).str.strip().unique()
                    bledne = [o for o in pula if o.lower() != st.session_state.poprawna_odp_w.lower()]
                    wylosowane_bledne = random.sample(bledne, min(3, len(bledne))) if bledne else []
                    
                    wszystkie_opcje = wylosowane_bledne + [st.session_state.poprawna_odp_w]
                    random.shuffle(wszystkie_opcje)
                    st.session_state.opcje_abcd_w = wszystkie_opcje
                    st.session_state.quiz_answered_w = False

                st.subheader(f"Jak przetłumaczysz słowo: **{st.session_state.pytanie_pl_w}**?")

                with st.form(key="quiz_form_w"):
                    wybrana_odp = st.radio("Wybierz odpowiedź:", st.session_state.opcje_abcd_w, key="radio_odp_w")
                    if st.form_submit_button("Sprawdź", use_container_width=True) and not st.session_state.quiz_answered_w:
                        st.session_state.total += 1
                        st.session_state.quiz_answered_w = True
                        if wybrana_odp == st.session_state.poprawna_odp_w:
                            st.session_state.score += 1
                            st.success("🎉 Poprawna odpowiedź!")
                        else:
                            st.error(f"❌ Błąd! Poprawna odpowiedź to: {st.session_state.poprawna_odp_w}")

                if st.session_state.quiz_answered_w and st.button("Następne słówko ➡️", use_container_width=True):
                    if 'opcje_abcd_w' in st.session_state: del st.session_state.opcje_abcd_w
                    st.session_state.quiz_answered_w = False
                    st.rerun()

# ==========================================
# 5. ZAKŁADKA: ZDANIA
# ==========================================
with tab_zdania:
    if baza_zdania.empty:
        st.warning("Tabela zdań jest pusta. Sprawdź plik jezyki_zdania.csv na HF.")
    else:
        baza_zdania['rozdzial'] = pd.to_numeric(baza_zdania['rozdzial'], errors='coerce')
        baza_zdania = baza_zdania.dropna(subset=['rozdzial'])
        
        min_r_z = int(baza_zdania['rozdzial'].min())
        max_r_z = int(baza_zdania['rozdzial'].max())

        nr_roz_z = min_r_z
        if min_r_z < max_r_z:
            nr_roz_z = st.slider("Wybierz rozdział (Zdania)", min_r_z, max_r_z, key="s_slider_z")

        dane_roz_z = baza_zdania[baza_zdania['rozdzial'] == nr_roz_z]
        tryb_z = st.radio("Wybierz tryb pracy (Zdania):", ["Nauka", "Quiz"], horizontal=True, key="mode_z_w")

        if tryb_z == "Nauka":
            kolumny_do_tabeli_z = ['polski']
            if czysty_jezyk in dane_roz_z.columns: 
                kolumny_do_tabeli_z.append(czysty_jezyk)
            if kolumna_wymowa in dane_roz_z.columns: 
                kolumny_do_tabeli_z.append(kolumna_wymowa)
            st.table(dane_roz_z[kolumny_do_tabeli_z])
            
        else: # QUIZ ZDANIA
            if dane_roz_z.empty:
                st.error("Brak danych dla tego rozdziału!")
            else:
                if st.session_state.get('last_id_z') != nr_roz_z:
                    st.session_state.last_id_z = nr_roz_z
                    if 'opcje_abcd_z' in st.session_state: 
                        del st.session_state.opcje_abcd_z
                    st.session_state.quiz_answered_z = False

                if 'opcje_abcd_z' not in st.session_state:
                    wybrany_wiersz_z = dane_roz_z.sample(n=1).iloc[0]
                    st.session_state.pytanie_pl_z = str(wybrany_wiersz_z['polski']).strip()
                    st.session_state.poprawna_odp_z = str(wybrany_wiersz_z[czysty_jezyk]).strip()
                    
                    pula_z = dane_roz_z[czysty_jezyk].dropna().astype(str).str.strip().unique()
                    bledne_z = [o for o in pula_z if o.lower() != st.session_state.poprawna_odp_z.lower()]
                    wylosowane_bledne_z = random.sample(bledne_z, min(3, len(bledne_z))) if bledne_z else []
                    
                    wszystkie_opcje_z = wylosowane_bledne_z + [st.session_state.poprawna_odp_z]
                    random.shuffle(wszystkie_opcje_z)
                    st.session_state.opcje_abcd_z = wszystkie_opcje_z
                    st.session_state.quiz_answered_z = False

                st.subheader(f"Jak przetłumaczysz zdanie: **{st.session_state.pytanie_pl_z}**?")

                with st.form(key="quiz_form_z"):
                    wybrana_odp_z = st.radio("Wybierz odpowiedź:", st.session_state.opcje_abcd_z, key="radio_odp_z")
                    if st.form_submit_button("Sprawdź", use_container_width=True) and not st.session_state.quiz_answered_z:
                        st.session_state.total += 1
                        st.session_state.quiz_answered_z = True
                        if wybrana_odp_z == st.session_state.poprawna_odp_z:
                            st.session_state.score += 1
                            st.success("🎉 Poprawna odpowiedź!")
                        else:
                            st.error(f"❌ Błąd! Poprawna odpowiedź to: {st.session_state.poprawna_odp_z}")

                if st.session_state.quiz_answered_z and st.button("Następne zdanie ➡️", use_container_width=True):
                    if 'opcje_abcd_z' in st.session_state: 
                        del st.session_state.opcje_abcd_z
                    st.session_state.quiz_answered_z = False
                    st.rerun()

st.caption("Najcierpliwszy portal do nauki języków obcych")
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")
