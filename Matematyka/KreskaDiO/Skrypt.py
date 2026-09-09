import streamlit as st


# Funkcja do sumowania
def licz_dodawanie(a, b):
    gora, dol = str(a), str(b)
    dlugosc = max(len(gora), len(dol))
    gora, dol = gora.zfill(dlugosc), dol.zfill(dlugosc)

    pamiec = 0
    kroki = []
    wynik_str = ""
    nad_liczba = [""] * dlugosc

    kolumny = ["jedności", "dziesiątek", "setek", "tysięcy", "dziesięciu tysięcy"]

    for i in range(dlugosc - 1, -1, -1):
        cyfra1, cyfra2 = int(gora[i]), int(dol[i])
        suma = cyfra1 + cyfra2 + pamiec

        zapisz = suma % 10
        stara_pamiec = pamiec
        pamiec = suma // 10
        wynik_str = str(zapisz) + wynik_str

        if pamiec > 0 and i > 0:
            nad_liczba[i - 1] = str(pamiec)

        nazwa = kolumny[dlugosc - 1 - i] if (dlugosc - 1 - i) < len(kolumny) else f"kolumna {dlugosc - i}"

        txt = f"W rzędzie **{nazwa}** dodajemy {cyfra1} + {cyfra2}"
        if stara_pamiec > 0:
            txt += f" i dorzucamy {stara_pamiec} z pamięci"
        txt += f". Wychodzi **{suma}**."

        if suma >= 10:
            txt += f" Na dole ląduje **{zapisz}**, a jedynka ucieka do góry do następnej kolumny."
        else:
            txt += f" Zapisujemy **{zapisz}** i gotowe."
        kroki.append(txt)

    if pamiec > 0:
        wynik_str = str(pamiec) + wynik_str
        kroki.append(f"Zostało nam jeszcze {pamiec} z pamięci, więc dopisujemy na samym początku.")

    # BUDOWANIE MACIERZY LATEX (Wszystkie wiersze mają długość: dlugosc + 1)
    wiersz_nad = [""] + nad_liczba
    wiersz_gora = [""] + list(gora)
    wiersz_dol = ["+"] + list(dol)

    # Dopasowanie wiersza wyniku do odpowiedniej długości
    wiersz_wynik = list(wynik_str)
    while len(wiersz_wynik) < (dlugosc + 1):
        wiersz_wynik = [""] + wiersz_wynik

    latex_nad = " & ".join([f"\\color{{red}}{{{c}}}" if c else "" for c in wiersz_nad])
    latex_gora = " & ".join(wiersz_gora)
    latex_dol = " & ".join(wiersz_dol)
    latex_wynik = " & ".join(wiersz_wynik)

    format_kolumn = "r" * (dlugosc + 1)

    latex_code = rf'''
    \begin{{array}}{{{format_kolumn}}}
        {latex_nad} \\
        {latex_gora} \\
        {latex_dol} \\
        \hline
        {latex_wynik}
    \end{{array}}
    '''
    return latex_code, kroki


def licz_odejmowanie(a, b):
    # Obsługa przypadku ujemnego
    zamiana = False
    if b > a:
        a, b = b, a
        zamiana = True


    g, d = str(a), str(b)
    L = len(g)
    d = d.zfill(L)

    cyfry_g = [int(c) for c in g]
    kroki, res = [], ""
    gora_fix = [""] * L
    miejsca = ["jedności", "dziesiątek", "setek", "tysięcy", "dziesięciu tysięcy"]

    for i in range(L - 1, -1, -1):
        c1 = cyfry_g[i]
        c2 = int(d[i])
        nazwa = miejsca[L - 1 - i] if (L - 1 - i) < len(miejsca) else f" rząd {L - i}"

        if c1 < c2:
            idx = i - 1
            # Pożyczanie przez zera
            while idx >= 0 and cyfry_g[idx] == 0:
                cyfry_g[idx] = 9
                gora_fix[idx] = "9"
                idx -= 1
            # Pomniejszenie pierwszej niezerowej cyfry
            if idx >= 0:
                cyfry_g[idx] -= 1
                gora_fix[idx] = str(cyfry_g[idx])

            nowe_c1 = c1 + 10
            kroki.append(
                f"W rzędzie **{nazwa}** mamy {c1} - {c2}. Za mało! Pożyczamy od sąsiada. Mamy teraz **{nowe_c1} - {c2} = {nowe_c1 - c2}**."
            )
            wynik_kolumny = nowe_c1 - c2
        else:
            kroki.append(f"W rzędzie **{nazwa}** odejmujemy {c1} - {c2}. Wynik to **{c1 - c2}**.")
            wynik_kolumny = c1 - c2

        res = str(wynik_kolumny) + res

    wynik_str = res.lstrip('0') or "0"

    if zamiana:
        kroki.append("⚠️ Uwaga: Odjemna była mniejsza od odjemnika. Wynik końcowy jest ujemny.")

    # SPÓJNE BUDOWANIE MACIERZY LATEX
    wiersz_nad = [""] + gora_fix
    wiersz_gora = [""] + list(g)
    wiersz_dol = ["-"] + list(d)

    # Budujemy wiersz wyniku. Jeśli wynik jest ujemny, dodamy znak minus na samym początku wiersza
    wiersz_wynik = list(wynik_str)
    while len(wiersz_wynik) < L:
        wiersz_wynik = [""] + wiersz_wynik

    if zamiana:
        wiersz_wynik = ["-"] + wiersz_wynik
    else:
        wiersz_wynik = [""] + wiersz_wynik

    latex_nad = " & ".join([f"\\color{{red}}{{{c}}}" if c else "" for c in wiersz_nad])
    latex_gora = " & ".join(wiersz_gora)
    latex_dol = " & ".join(wiersz_dol)
    latex_wynik = " & ".join(wiersz_wynik)

    format_kolumn = "r" * (L + 1)

    latex_code = rf'''
    \begin{{array}}{{{format_kolumn}}}
        {latex_nad} \\
        {latex_gora} \\
        {latex_dol} \\
        \hline
        {latex_wynik}
    \end{{array}}
    '''
    return latex_code, kroki


# Interfejs Użytkownika
st.set_page_config(page_title="Zadania domowe")
st.title("Liczenie pisemne - pomocnik")

wybor = st.selectbox("Co liczysz?", ["Dodawanie", "Odejmowanie"])

c1, c2 = st.columns(2)
num1 = c1.number_input("Liczba u góry", value=148, min_value=0)
num2 = c2.number_input("Liczba na dole", value=75, min_value=0)

if "Dodawanie" in wybor:
    latex_słupek, info = licz_dodawanie(num1, num2)
else:
    latex_słupek, info = licz_odejmowanie(num1, num2)

st.write("### Twój słupek:")
st.latex(latex_słupek)

st.write("### Jak do tego dojść?")
for i, k in enumerate(info):
    st.info(f"{i + 1}. {k}")
