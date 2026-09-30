import os
import json
import streamlit as st

# Konfiguracja strony
st.set_page_config(page_title="Trener Ortografii", page_icon="📝")
st.title("Mistrz Ortografii!")


# Funkcja wczytywania danych z JSON
def wczytaj_opowiadania():
    sciezka = "opowiadania.json"
    if not os.path.exists(sciezka):
        st.error(f"Nie znaleziono pliku {sciezka}!")
        return []
    try:
        with open(sciezka, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Błąd pliku JSON: {e}")
        return []


OPOWIADANIA = wczytaj_opowiadania()

if OPOWIADANIA:
    poziomy = ["Łatwy", "Średni", "Trudny"]
    wybrany_poziom = st.radio("Wybierz poziom trudności:", poziomy, horizontal=True)


    pasujace_opowiadania = [op for op in OPOWIADANIA if isinstance(op, dict) and op.get("trudnosc") == wybrany_poziom]

    if not pasujace_opowiadania:
        st.warning(f"Brak opowiadań dla poziomu: {wybrany_poziom}")
    else:

        wybor_tytul = st.selectbox("Wybierz temat opowiadania:", [op["tytul"] for op in pasujace_opowiadania])
        dane_opowiadania = next(op for op in pasujace_opowiadania if op["tytul"] == wybor_tytul)

        # Przygotowanie tekstu z lukami
        tekst_wyswietlany = dane_opowiadania["tekst_wzorcowy"]
        for klucz, info in dane_opowiadania["luki"].items():

            luka_wizualna = klucz.replace(info["odpowiedz"], "_")
            tekst_wyswietlany = tekst_wyswietlany.replace(f"{{{klucz}}}", f"**{luka_wizualna}**")

        st.info(tekst_wyswietlany)

        # Formularz
        with st.form(key=f"formularz_{wybrany_poziom}_{wybor_tytul}"):
            st.subheader("Wpisz brakujące litery:")
            odpowiedzi_uzytkownika = {}

            for i, (klucz, info) in enumerate(dane_opowiadania["luki"].items()):
                zastepnik = klucz.replace(info["odpowiedz"], "_")
                unikalny_klucz = f"input_{wybrany_poziom}_{wybor_tytul}_{klucz}_{i}"


                wpis = st.text_input(
                    label=f"Uzupełnij słowo: **{zastepnik}**",
                    max_chars=2,
                    key=unikalny_klucz,
                    placeholder="Wpisz brakujące litery..."
                ).strip()

                odpowiedzi_uzytkownika[klucz] = wpis

            wyslane = st.form_submit_button("Sprawdź wynik 🚀", type="primary")

        # Logika sprawdzania wyników
        if wyslane:
            punkty = 0
            max_punktow = len(dane_opowiadania["luki"])

            st.write("---")
            st.subheader("Wyniki:")

            for klucz, info in dane_opowiadania["luki"].items():
                odp = odpowiedzi_uzytkownika[klucz]

                # Pobieramy poprawną odpowiedź z JSON-a
                poprawna_odp = info["odpowiedz"]

                # PORÓWNANIE (Ignoruje wielkość liter)
                if odp.lower() == poprawna_odp.lower():
                    punkty += 1
                    st.success(f"🍏 **{info['pelny']}** — Idealnie!")
                else:
                    wpisano = f"'{odp}'" if odp else "puste pole"
                    st.error(
                        f"🍎 Wpisano {wpisano} w słowie **{klucz.replace(info['odpowiedz'], '_')}**. "
                        f"Poprawna forma to: **{info['pelny']}**. \n\n"
                        f"💡 *Zasada:* {info['zasada']}"
                    )

            # Pasek postępu 
            st.write("---")
            procent = int((punkty / max_punktow) * 100)
            st.progress(punkty / max_punktow, text=f"Twój wynik to {procent}%")

            if punkty == max_punktow:
                st.balloons()
                st.success(
                    f"🏆 Mistrz Ortografii! Zdobywasz {punkty}/{max_punktow} punktów! Przejdź do kolejnego poziomu!")
            elif procent >= 70:
                st.info(f"Brawo! Dobry wynik: {punkty}/{max_punktow}. Oby tak dalej! 🌟")
            else:
                st.warning(
                    f"Trening czyni mistrza! Twój wynik to {punkty}/{max_punktow}. Przeczytaj zasady i spróbuj jeszcze raz! 💪")
else:
    st.warning("Baza opowiadań jest pusta.")
