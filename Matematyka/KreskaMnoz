import streamlit as st

st.set_page_config(page_title="Mnożenie pod kreską", page_icon="🧮")
st.title("🧮 Mnożenie pod kreską ze 'schodkiem'")
st.write("Wpisz liczby i zobacz, jak działa szkolny mechanizm przesunięcia pozycji, czyli 'schodek'.")

# Pobieranie danych
l1 = st.number_input("Pierwsza liczba:", min_value=0, max_value=999, value=123, step=1)
l2 = st.number_input("Druga liczba:", min_value=0, max_value=999, value=45, step=1)


if st.button("Pokaż etapy mnożenia", type="primary"):
    str_l2 = str(l2)
    cyfry_l2 = [int(c) for c in reversed(str_l2)]
    szerokosc = 12

    st.subheader("Tradycyjny zapis szkolny:")


    linie_html = []

    linie_html.append(f"{l1:>{szerokosc}}")
    linie_html.append(f"×{l2:>{szerokosc - 1}}")
    linie_html.append("-" * szerokosc)

    # Generowanie etapów pośrednich
    for i, cyfra in enumerate(cyfry_l2):
        iloczyn_czesciowy = l1 * cyfra

        if i == 0:

            linia = f"{iloczyn_czesciowy:>{szerokosc}}"
            linia = linia.replace(" ", "&nbsp;")
        else:
            zera_schodka = "0" * i
            czerwone_zera = f"<span style='color: #FF4B4B; font-weight: bold;'>{zera_schodka}</span>"
            szerokosc_dla_liczb = szerokosc - i
            czesc_liczbowa = f"{iloczyn_czesciowy:>{szerokosc_dla_liczb}}"
            czesc_liczbowa_html = czesc_liczbowa.replace(" ", "&nbsp;")
            linia = f"{czesc_liczbowa_html}{czerwone_zera}"

        linie_html.append(linia)

        # Zabezpieczenie przed liczbami 4-cyfrowymi (na wypadek zmiany max_value)
        nazwy_pozycji = ["jedności", "dziesiątek", "setek"]
        nazwa_pozycji = nazwy_pozycji[i] if i < len(nazwy_pozycji) else f"pozycji {i + 1}"

        st.info(f"**Krok {i + 1}:** Mnożymy {l1} x {cyfra} ({nazwa_pozycji}). " +
                (f"Dopisujemy **{i} czerwone zero** jako schodek." if i > 0 else ""))




    wynik_koncowy = l1 * l2
    linie_html.append("-" * szerokosc)

    wynik_str = f"{wynik_koncowy:>{szerokosc}}"
    linie_html.append(wynik_str.replace(" ", "&nbsp;"))


    html_content = "<br>".join(
        [line if "<span" in line or "&nbsp;" in line else line.replace(" ", "&nbsp;") for line in linie_html])

    # Tablica matematyczna
    st.markdown(
        f"""
        <div style="
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        font-family: 'Courier New', Courier, monospace;
        font-size: 24px;
        line-height: 1.2;
        letter-spacing: 2px;
        white-space: nowrap;">
        {html_content}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.success(f"Wynik końcowy: **{wynik_koncowy}**")

    # Sekcja edukacyjna
    st.markdown("---")
    st.markdown("### 💡 Jak czytać ten zapis? Instrukcja dla ucznia:")
    st.markdown("""
    *   **Dlaczego ostatnia cyfra jest czerwona?** 🔴
        To jest nasz **szkolny schodek**! Kiedy mnożysz przez drugą cyfrę (dziesiątki), zaczynasz pisać wyniki pod dziesiątkami. Czerwone zero pilnuje, aby żadna cyfra nie wskoczyła na złe miejsce.

    *   **Jak powstały linie pomocnicze?**
        * Pierwsza linia to wynik mnożenia pierwszej liczby przez **jedności** (ostatnią cyfrę z dołu).
        * Druga linia to mnożenie przez **dziesiątki** (środkową cyfrę) + dopisane czerwone zero.
        * Trzecia linia (jeśli mnożysz przez liczbę 3-cyfrową) to mnożenie przez **setki** + dwa czerwone zera.

    *   **Co robisz na końcu?**
        Dodajemy do siebie wszystkie linie pomocnicze w pionowych kolumnach i otrzymujemy wynik końcowy!
    """)

# STOPKA
st.divider()
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")
