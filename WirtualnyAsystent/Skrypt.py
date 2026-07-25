import streamlit as st
import pandas as pd

# Konfiguracja strony
st.set_page_config(page_title="Asystent Lekcyjny", page_icon="🤖", layout="centered")

st.title("🤖 Twój Inteligentny Asystent")


# Automatyczne ładowanie bazy z pliku
@st.cache_data(ttl=60)
def pobierz_baze():
    try:
        df = pd.read_csv("lekcje.csv")
        # Zamienia puste pola (NaN) na pusty tekst, aby uniknąć błędów float
        df = df.fillna("")
        return df if not df.empty else None
    except FileNotFoundError:
        st.error("Błąd: nie znaleziono pliku 'lekcje.csv' w repozytorium!")
        return None


df_lekcje = pobierz_baze()

if df_lekcje is not None:
    # Powitanie bota w stylu czatu
    with st.chat_message("assistant"):
        st.write("Cześć! W czym mogę Ci dzisiaj pomóc? Wpisz temat lekcji, której szukasz.")

    # Komponent wejściowy stylizowany na czat
    zapytanie = st.chat_input("Zacznij pisać tutaj (np. ułamki, present, czasownik)...", max_chars=100)

    if zapytanie:
        # Podwójne zabezpieczenie w kodzie (na wypadek prób oszukania pakietów HTTP)
        czyste_zapytanie = zapytanie.strip()[:100]

        if not czyste_zapytanie or len(czyste_zapytanie) < 2:
            with st.chat_message("assistant"):
                st.warning("Wpisz przynajmniej 2 znaki, abym mógł coś znaleźć! 😉")
        else:
            with st.chat_message("user"):
                st.write(czyste_zapytanie)

            # Usunięcie znaków specjalnych dla bezpieczeństwa
            do_analizy = "".join(e for e in czyste_zapytanie if e.isalnum() or e.isspace())
            slowa = do_analizy.lower().split()

            kontekst = (df_lekcje['dzial'].astype(str) + " " +
                        df_lekcje['lekcja'].astype(str) + " " +
                        df_lekcje['slowa_kluczowe'].astype(str)).str.lower()

            trafnosc = pd.Series(0, index=df_lekcje.index)

            for slowo in slowa:
                rdzen = slowo[:4] if len(slowo) > 4 else slowo
                maska_w_bazie = kontekst.str.contains(rdzen, case=False, na=False)
                trafnosc += maska_w_bazie.astype(int)

                for idx, tekst_wiersza in kontekst.items():
                    slowa_bazy = str(tekst_wiersza).split()
                    if any(s_bazy[:4] in slowo for s_bazy in slowa_bazy if len(s_bazy) > 3):
                        trafnosc.loc[idx] += 1

            wyniki = df_lekcje[trafnosc > 0].copy()
            wyniki['trafnosc'] = trafnosc[trafnosc > 0]
            wyniki = wyniki.sort_values(by='trafnosc', ascending=False)

            with st.chat_message("assistant"):
                if not wyniki.empty:
                    # Zapamiętujemy łączną liczbę znalezionych lekcji
                    wszystkie_wyniki = len(wyniki)
                    # Ograniczamy DataFrame do maksymalnie 5 pierwszych wierszy
                    wyniki_top5 = wyniki.head(5)

                    st.write(f"### Znalezione lekcje ({wszystkie_wyniki}):")

                    # Iterujemy tylko po 5 najlepszych wynikach
                    for _, lekcja in wyniki_top5.iterrows():
                        with st.container(border=True):
                            st.markdown(f"**{lekcja['dzial']}** > {lekcja['lekcja']}")
                            st.link_button("Przejdź do lekcji", lekcja["url"], type="primary")

                    # Opcjonalny komunikat, jeśli wyników było więcej niż 5
                    if wszystkie_wyniki > 5:
                        st.caption(
                            f"*Pokazuję 5 najbardziej trafnych z {wszystkie_wyniki} znalezionych lekcji. Skonkretyzuj zapytanie, aby zawęzić wyniki.*")
                else:
                    st.warning("Nie znalazłem idealnego dopasowania. Spróbuj wpisać krótszą frazę.")
