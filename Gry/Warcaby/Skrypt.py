import streamlit as st
import numpy as np
import random
import time

# 1. Konfiguracja i CSS
st.set_page_config(page_title="Warcaby Premium", layout="centered")
st.title("Interaktywne Warcaby z Botem")

st.markdown("""
<style>
div.stButton > button {
    width: 60px !important;
    height: 60px !important;
    padding: 0px !important;
    font-size: 28px !important;
    font-weight: bold !important;
    border-radius: 0px !important;
    border: 1px solid #444 !important;
}
</style>
""", unsafe_allow_html=True)

# 2. Inicjalizacja stanu gry
if "plansza" not in st.session_state:
    plansza = np.zeros((8, 8), dtype=int)
    for w in range(3):
        for k in range(8):
            if (w + k) % 2 == 1:
                plansza[w, k] = 1
    for w in range(5, 8):
        for k in range(8):
            if (w + k) % 2 == 1:
                plansza[w, k] = 2
    st.session_state.plansza = plansza
    st.session_state.tura = "Czerwone"
    st.session_state.wybrany_pionek = None
    st.session_state.komunikat = "Zacznij grę! Czerwone zaczynają."
    st.session_state.w_trakcie_bicia = None
    st.session_state.gra_zakonczona = False  # NOWOŚĆ: Flaga końca gry

# Wybór trybu gry w panelu bocznym
tryb_gry = st.sidebar.selectbox("Tryb gry", ["Gra z Botem (Czarne)", "Gra we dwoje (Lokalnie)"])

# Przycisk resetu gry w panelu bocznym
if st.sidebar.button("Resetuj grę"):
    for klucz in list(st.session_state.keys()):
        del st.session_state[klucz]
    st.rerun()


# 3. Funkcje pomocnicze i logika gry
def pobierz_wszystkie_ruchy(w_pocz, k_pocz):
    plansza = st.session_state.plansza
    pionek = plansza[w_pocz, k_pocz]
    if pionek == 0:
        return []

    gracz = 1 if pionek in [1, 11] else 2
    czy_damka = pionek in [11, 22]

    ruchy = []
    kierunki_w = []
    if czy_damka or gracz == 1: kierunki_w.append(1)
    if czy_damka or gracz == 2: kierunki_w.append(-1)
    kierunki_k = [-1, 1]

    # Zwykłe ruchy
    for dw in kierunki_w:
        for dk in kierunki_k:
            w_kon, k_kon = w_pocz + dw, k_pocz + dk
            if 0 <= w_kon < 8 and 0 <= k_kon < 8:
                if plansza[w_kon, k_kon] == 0:
                    ruchy.append((w_kon, k_kon, False))

    # Bicia
    for dw in [-1, 1]:
        for dk in [-1, 1]:
            w_bity, k_bity = w_pocz + dw, k_pocz + dk
            w_kon, k_kon = w_pocz + 2 * dw, k_pocz + 2 * dk
            if 0 <= w_kon < 8 and 0 <= k_kon < 8:
                bity_pionek = plansza[w_bity, k_bity]
                if bity_pionek != 0:
                    bity_gracz = 1 if bity_pionek in [1, 11] else 2
                    if bity_gracz != gracz and plansza[w_kon, k_kon] == 0:
                        ruchy.append((w_kon, k_kon, True))
    return ruchy


def sprawdz_dostepne_bicia_dla_gracza(numer_gracza):
    plansza = st.session_state.plansza
    for w in range(8):
        for k in range(8):
            pionek = plansza[w, k]
            g = 1 if pionek in [1, 11] else 2
            if pionek != 0 and g == numer_gracza:
                ruchy = pobierz_wszystkie_ruchy(w, k)
                if any(r[2] for r in ruchy):
                    return True
    return False


def wykonaj_ruch(w_pocz, k_pocz, w_kon, k_kon):
    plansza = st.session_state.plansza
    pionek = plansza[w_pocz, k_pocz]
    gracz = 1 if pionek in [1, 11] else 2

    ruchy = pobierz_wszystkie_ruchy(w_pocz, k_pocz)
    wybrany_ruch = [r for r in ruchy if r[0] == w_kon and r[1] == k_kon]

    if not wybrany_ruch:
        return False, "Niedozwolony ruch dla tego pionka!"

    czy_bicie = wybrany_ruch[0][2]

    if not czy_bicie and sprawdz_dostepne_bicia_dla_gracza(gracz):
        return False, "Masz obowiązek bicia!"

    plansza[w_kon, k_kon] = pionek
    plansza[w_pocz, k_pocz] = 0

    if czy_bicie:
        w_bity = w_pocz + (w_kon - w_pocz) // 2
        k_bity = k_pocz + (k_kon - k_pocz) // 2
        plansza[w_bity, k_bity] = 0

        sprawdz_promocje(w_kon, k_kon)

        kolejne_ruchy = pobierz_wszystkie_ruchy(w_kon, k_kon)
        kolejne_bicia = [r for r in kolejne_ruchy if r[2]]

        if kolejne_bicia:
            st.session_state.w_trakcie_bicia = (w_kon, k_kon)
            st.session_state.wybrany_pionek = (w_kon, k_kon)
            return True, "Kolejne bicie jest możliwe! Musisz kontynuować ruch tym pionkiem."

    sprawdz_promocje(w_kon, k_kon)
    st.session_state.w_trakcie_bicia = None
    koniec_tury()
    return True, "Ruch wykonany prawidłowo."


def sprawdz_promocje(w, k):
    plansza = st.session_state.plansza
    if plansza[w, k] == 1 and w == 7:
        plansza[w, k] = 11  # Czerwona damka
    elif plansza[w, k] == 2 and w == 0:
        plansza[w, k] = 22  # Czarna damka


def koniec_tury():
    st.session_state.tura = "Czarne" if st.session_state.tura == "Czerwone" else "Czerwone"
    st.session_state.wybrany_pionek = None


def obsluga_klikniecia(w, k):
    if st.session_state.gra_zakonczona:
        return

    plansza = st.session_state.plansza
    tura = st.session_state.tura
    wybrany = st.session_state.wybrany_pionek
    numer_gracza = 1 if tura == "Czerwone" else 2

    if st.session_state.w_trakcie_bicia:
        if (w, k) == st.session_state.w_trakcie_bicia:
            st.session_state.komunikat = "Ten pionek musi dokończyć serię bicia. Wskaż pole docelowe."
        elif wybrany is not None and plansza[w, k] == 0:
            w_pocz, k_pocz = wybrany
            sukces, info = wykonaj_ruch(w_pocz, k_pocz, w, k)
            st.session_state.komunikat = info
        else:
            st.session_state.komunikat = "Musisz dokończyć bicie wybranym pionkiem!"
        return

    pionek = plansza[w, k]
    pionek_gracz = 1 if pionek in [1, 11] else (2 if pionek in [2, 22] else 0)

    if pionek_gracz == numer_gracza:
        st.session_state.wybrany_pionek = (w, k)
        st.session_state.komunikat = f"Wybrano pionek ({w + 1}, {k + 1}). Wskaż pole docelowe."
    elif wybrany is not None and plansza[w, k] == 0:
        w_pocz, k_pocz = wybrany
        sukces, info = wykonaj_ruch(w_pocz, k_pocz, w, k)
        st.session_state.komunikat = info
    else:
        st.session_state.komunikat = "To nie Twój pionek lub nieprawidłowy ruch!"


def ruch_bota():
    """Bot obsługujący Czarne pionki (2 i 22) - priorytetyzuje bicia."""
    if st.session_state.gra_zakonczona:
        return

    plansza = st.session_state.plansza
    bicia = []
    zwykle_ruchy = []

    for w in range(8):
        for k in range(8):
            pionek = plansza[w, k]
            if pionek == 2 or pionek == 22:
                ruchy = pobierz_wszystkie_ruchy(w, k)
                for r in ruchy:
                    dane_ruchu = (w, k, r[0], r[1])
                    if r[2]:  # czy bicie
                        bicia.append(dane_ruchu)
                    else:
                        zwykle_ruchy.append(dane_ruchu)

    if bicia:
        wybrany = random.choice(bicia)
    elif zwykle_ruchy:
        wybrany = random.choice(zwykle_ruchy)
    else:
        st.session_state.komunikat = "Bot nie ma ruchu. Czerwone wygrywają 🎉!"
        st.session_state.gra_zakonczona = True
        return

    w_pocz, k_pocz, w_kon, k_kon = wybrany
    wykonaj_ruch(w_pocz, k_pocz, w_kon, k_kon)


# 4. Rysowanie planszy i wywołanie tury bota
if tryb_gry == "Gra z Botem (Czarne)" and st.session_state.tura == "Czarne" and not st.session_state.gra_zakonczona:
    st.session_state.komunikat = "Bot myśli..."
    time.sleep(0.5)
    ruch_bota()
    st.rerun()

# Wyświetlanie aktualnego stanu gry
if st.session_state.gra_zakonczona:
    st.success(st.session_state.komunikat)
else:
    st.subheader(f"Tura: {st.session_state.tura}")
    st.info(st.session_state.komunikat)


def pobierz_symbol_pionka(wartosc, w, k):
    if st.session_state.wybrany_pionek == (w, k):
        if wartosc == 1: return "🔴✨"
        if wartosc == 11: return "👑🔴"
        if wartosc == 2: return "⚫✨"
        if wartosc == 22: return "👑⚫"
    else:
        if wartosc == 1: return "🔴"
        if wartosc == 11: return "👑🔴"  # Poprawione dla czytelności damki
        if wartosc == 2: return "⚫"
        if wartosc == 22: return "👑⚫"  # Poprawione dla czytelności damki
    return ""


# Rysowanie siatki 8x8 za pomocą kolumn Streamlit
for w in range(8):
    cols = st.columns(8)
    for k in range(8):
        with cols[k]:
            symbol = pobierz_symbol_pionka(st.session_state.plansza[w, k], w, k)

            if (w + k) % 2 == 1:
                # Ciemne pole gry
                st.button(symbol if symbol else " ", key=f"pole_{w}_{k}", on_click=obsluga_klikniecia, args=(w, k))
            else:
                # Jasne pole nieaktywne (wyłączony przycisk)
                st.button(" ", key=f"pole_{w}_{k}", disabled=True)
                
st.divider()
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")
