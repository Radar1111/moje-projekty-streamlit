import streamlit as st

st.set_page_config(page_title="Dzielenie pod kreską", page_icon="🧮")
st.title("🧮 Dzielenie pod kreską krok po kroku")
st.write("Wpisz dzielną i dzielnik")

# Pobieranie danych
dzielna = st.number_input("Wpisz dzielną (liczba dzielona, np. 735):", min_value=1, max_value=999, value=735, step=1)
dzielnik = st.number_input("Wpisz dzielnik (przez ile dzielisz, np. 5):", min_value=1, max_value=99, value=5, step=1)

if st.button("Pokaż etapy dzielenia", type="primary"):
    str_dzielna = str(dzielna)
    str_dzielnik = str(dzielnik)
    wynik_caly = dzielna // dzielnik
    reszta_cala = dzielna % dzielnik

    st.subheader("Wizualizacja graficzna:")

    len_dzielna = len(str_dzielna)

    # Nagłówek działania
    linie_wizualizacji = [
        f" {wynik_caly:>{len_dzielna}}",  # Wynik nad kreską
        f" " + "_" * len_dzielna,  # Kreska nad dzielną
        f" {str_dzielna} : {str_dzielnik}"  # Główne działanie
    ]

    kroki_tekst = []
    aktualna_reszta = 0

    # Przechodzimy krok po kroku przez każdą cyfrę dzielnej
    for i, cyfra in enumerate(str_dzielna):
        poprzednia_reszta = aktualna_reszta
        aktualna_reszta = aktualna_reszta * 10 + int(cyfra)
        ile_razy = aktualna_reszta // dzielnik
        iloczyn = ile_razy * dzielnik
        nowa_reszta = aktualna_reszta - iloczyn

        # Opisy kroków
        kroki_tekst.append(f"**Krok {i + 1}:** Spisujemy cyfrę **{cyfra}**. Mamy teraz liczbę **{aktualna_reszta}**.")
        kroki_tekst.append(
            f"⋅ Ile razy {dzielnik} mieści się w {aktualna_reszta}? Mieści się **{ile_razy}** razy (zapisujemy {ile_razy} nad kreską).")
        kroki_tekst.append(f"⋅ Mnożymy: {ile_razy} ⋅ {dzielnik} = **{iloczyn}**.")
        kroki_tekst.append(f"⋅ Odejmujemy: {aktualna_reszta} - {iloczyn} = **{nowa_reszta}**.")
        kroki_tekst.append("---")




        # 1. Wiersz z odejmowaniem (np. -5) - teraz schoowany o 1 pozycję w lewo
        len_ilo = len(str(iloczyn))
        len_akt = len(str(aktualna_reszta))
        wciecie_odejmowania = " " * (i - (len_ilo - 1))
        linie_wizualizacji.append(f"{wciecie_odejmowania}-{iloczyn}")

        # 2. Kreska pozioma pod odejmowaniem
        dlugosc_kreski = max(len_akt, len_ilo) + 1
        wciecie_kreski = " " * (i - (dlugosc_kreski - len_ilo - 1))
        linie_wizualizacji.append(f"{wciecie_kreski}" + "-" * dlugosc_kreski)

        # 3. Spisanie kolejnej cyfry na dół
        if i < len_dzielna - 1:
            nastepna_cyfra = str_dzielna[i + 1]
            wciecie_wyniku = " " * (i + 1 - (len(str(nowa_reszta)) - 1))
            linie_wizualizacji.append(f"{wciecie_wyniku}{nowa_reszta}{nastepna_cyfra}")
        else:
            # Koniec działania - reszta
            wciecie_wyniku = " " * (i + 1 - (len(str(nowa_reszta)) - 1))
            linie_wizualizacji.append(f"{wciecie_wyniku}{nowa_reszta} (reszta)")

        aktualna_reszta = nowa_reszta


    html_content = "<br>".join([line.replace(" ", "&nbsp;") for line in linie_wizualizacji])

    # Wyświetlenie kodu
    st.markdown(
        f"""
        <div style="
            background-color: #f8f9fa;
            padding: 25px;
            border-radius: 12px;
            border: 2px solid #e9ecef;
            font-family: 'Courier New', Courier, monospace;
            font-size: 24px;
            font-weight: bold;
            line-height: 1.5;
            letter-spacing: 2px;
            white-space: nowrap;">
            {html_content}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Wynik końcowy
    st.write("")
    if reszta_cala == 0:
        st.success(f"Brawo! Wynik końcowy to dokładnie: **{wynik_caly}**")
    else:
        st.warning(f"Wynik końcowy to: **{wynik_caly}** oraz **{reszta_cala}** reszty.")

    # Opisy słowne
    st.subheader("💡 Szczegółowy opis działań:")
    for krok in kroki_tekst:
        if "Krok" in krok:
            st.markdown(krok)
        elif krok == "---":
            st.markdown("---")
        else:
            st.info(krok)

# STOPKA
st.divider()
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")
