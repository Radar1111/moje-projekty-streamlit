import streamlit as st
import random

# Konfiguracja strony
st.set_page_config(page_title="Nauka Potęg i Pierwiastków - Klasa 7", layout="centered")


def wyswietl_sekcje_wsparcia():

    if "parent_verified" not in st.session_state:
        st.session_state.parent_verified = False
    if "num1" not in st.session_state:
        st.session_state.num1 = random.randint(5, 15)
    if "num2" not in st.session_state:
        st.session_state.num2 = random.randint(5, 15)

    LINK_DO_KAWY = "https://buycoffee.to/gigawiedza"


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

# Tytuł aplikacji
st.title("🔢 Mistrz Potęg i Pierwiastków - Klasa 7")
st.write("Witaj! Ta aplikacja pomoże Ci opanować potęgi, pierwiastki oraz notację wykładniczą.")

st.sidebar.header("Nawigacja")
opcja = st.sidebar.radio(
    "Wybierz tryb:",
    ["Teoria i Wzory", "Quiz - Sprawdź się"]
)

#  📝 MULTI-BRUDNOPIS W SIDEBARZE (TEKST + RYSOWANIE)
st.sidebar.markdown("---")
st.sidebar.header("📝 Brudnopis Ucznia")

# Tworzymy dwie niezależne zakładki w pasku bocznym
zakladka_rysuj, zakladka_pisz = st.sidebar.tabs(["🎨 Rysuj", "✍️ Pisz"])

with zakladka_rysuj:
    st.caption("Rysuj myszką lub palcem. Kliknij ikonę kosza pod tablicą, aby wyczyścić.")
    from streamlit_drawable_canvas import st_canvas

    # Rysownica w sidebarze działa stabilnie, bo nie blokuje jej główny formularz
    st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=3,
        stroke_color="#000000",
        background_color="#ffffff",
        update_streamlit=False,
        height=250,
        drawing_mode="freedraw",
        key="globalny_canvas_brudnopis",
    )

with zakladka_pisz:
    if "brudnopis_globalny" not in st.session_state:
        st.session_state["brudnopis_globalny"] = ""


    def czysc_notatnik():
        st.session_state["brudnopis_globalny"] = ""


    st.text_area(
        label="Miejsce na Twoje obliczenia:",
        placeholder="Np. wspólny mianownik to 12...",
        key="brudnopis_globalny",
        height=180
    )
    st.button("Wyczyść notatnik 🧹", on_click=czysc_notatnik)
with st.sidebar:
    wyswietl_sekcje_wsparcia()


# TEORIA
if opcja == "Teoria i Wzory":
    st.header("📚 Podstawowe Wzory i Teoria")
    st.write("Wybierz temat z listy, aby zobaczyć wzór i przykład:")

    dzialanie = st.selectbox(
        "Wybierz temat:",
        [
            "Mnożenie i dzielenie potęg o tych samych podstawach",
            "Potęgowanie potęgi, iloczynu i ilorazu",
            "Pierwiastki - definicja i własności",
            "Wyłączanie czynnika przed znak pierwiastka",
            "Notacja wykładnicza (zapis dużych liczb)",
            "Notacja wykładnicza (zapis małych liczb)"
        ]
    )

    if dzialanie == "Mnożenie i dzielenie potęg o tych samych podstawach":
        st.info("$$a^m \\cdot a^n = a^{m+n}$$  \n  $$a^m : a^n = a^{m-n}$$")
        st.write("**Mnożenie:** Podstawę przepisujesz, a wykładniki **dodajesz**.")
        st.write("**Dzielenie:** Podstawę przepisujesz, a wykładniki **odejmujesz**.")
        st.success("**Przykłady:**  \n$2^3 \\cdot 2^4 = 2^{3+4} = 2^7$  \n$5^6 : 5^2 = 5^{6-2} = 5^4$")

    elif dzialanie == "Potęgowanie potęgi, iloczynu i ilorazu":
        st.info("$$(a^m)^n = a^{m \\cdot n}$$  \n  $$(a \\cdot b)^n = a^n \\cdot b^n$$")
        st.write("**Potęga potęgi:** Podstawę przepisujesz, wykładniki **mnożysz**.")
        st.write("**Iloczyn do potęgi:** Każdy czynnik w nawiasie podnosisz do tej potęgi.")
        st.success("**Przykłady:**  \n$(3^2)^4 = 3^{2 \\cdot 4} = 3^8$  \n$(2 \\cdot 3)^4 = 2^4 \\cdot 3^4$")

    elif dzialanie == "Pierwiastki - definicja i własności":
        st.info("$$\\sqrt{a} = b \\iff b^2 = a$$  \n  $$\\sqrt[3]{a} = b \\iff b^3 = a$$")
        st.write(
            "**Pierwiastek kwadratowy ($\\sqrt{}$):** Szukasz liczby, która pomnożona przez samą siebie daje liczbę pod pierwiastkiem.")
        st.write(
            "**Pierwiastek sześcienny ($\\sqrt[3]{}$):** Szukasz liczby, która podniesiona do potęgi 3 daje liczbę pod pierwiastkiem.")
        st.success("**Przykłady:**  \n$\\sqrt{49} = 7$, bo $7^2 = 49$  \n$\\sqrt[3]{27} = 3$, bo $3^3 = 27$")

    elif dzialanie == "Wyłączanie czynnika przed znak pierwiastka":
        st.info("$$\\sqrt{a \\cdot b} = \\sqrt{a} \\cdot \\sqrt{b}$$")
        st.write(
            "**Zasada:** Rozbijasz liczbę pod pierwiastkiem na iloczyn dwóch liczb, z których jedna daje się łatwo zpierwiastkować.")
        st.success("**Przykład:** $\\sqrt{12} = \\sqrt{4 \\cdot 3} = \\sqrt{4} \\cdot \\sqrt{3} = 2\\sqrt{3}$")

    elif dzialanie == "Notacja wykładnicza (zapis dużych liczb)":
        st.info("$$a \\cdot 10^n$$ gdzie $$1 \\le a < 10$$ oraz $$n$$ jest liczbą całkowitą")
        st.write(
            "**Zasada:** Przesuwasz przecinek tak, aby przed nim stała tylko jedna cyfra (różna od zera). Wykładnik $n$ to liczba miejsc, o które przesunięto przecinek w lewo.")
        st.success("**Przykład:** $350\\ 000 = 3,5 \\cdot 10^5$")

    elif dzialanie == "Notacja wykładnicza (zapis małych liczb)":
        st.info("$$a \\cdot 10^{-n}$$ gdzie $$1 \\le a < 10$$")
        st.write(
            "**Zasada:** W przypadku ułamków dziesiętnych przesunięcie przecinka w prawo daje ujemny wykładnik potęgi liczby 10.")
        st.success("**Przykład:** $0,00042 = 4,2 \\cdot 10^{-4}$")

#  QUIZ
elif opcja == "Quiz - Sprawdź się":
    st.header("📝 Szybki Test")
    st.write("Rozwiąż wylosowane zadania. Łącznie masz 12 pytań ze wszystkich działów.")


    def generuj_nowy_quiz():
        pytania = []


        lista_dzialow = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6]


        for typ in lista_dzialow:
            p = random.randint(2, 9)
            w1 = random.randint(2, 6)
            w2 = random.randint(2, 6)

            # POTĘGI
            if typ == 1:
                wyb = random.choice(["mnozenie", "dzielenie"])
                if wyb == "mnozenie":

                    tekst = r"Uprość wyrażenie: $" + f"{p}^{{{w1}}} \\cdot {p}^{{{w2}}}" + r"$"
                    poprawna = f"${p}^{{{w1 + w2}}}$"
                    niepoprawne = [f"${p}^{{{w1 * w2}}}$", f"${p * 2}^{{{w1 + w2}}}$", f"${p}^{{{abs(w1 - w2)}}}$"]
                else:
                    w1_dzial = max(w1, w2) + 1
                    w2_dzial = min(w1, w2)
                    tekst = f"Uprość wyrażenie: ${p}^{{{w1_dzial}}} : {p}^{{{w2_dzial}}}$"
                    poprawna = f"${p}^{{{w1_dzial - w2_dzial}}}$"
                    niepoprawne = [f"${p}^{{{w1_dzial + w2_dzial}}}$", f"${p}^{{{w1_dzial * w2_dzial}}}$",
                                   f"$1^{{{w1_dzial - w2_dzial}}}$"]

            elif typ == 2:
                tekst = f"Uprość wyrażenie: $({p}^{{{w1}}})^{{{w2}}}$"
                poprawna = f"${p}^{{{w1 * w2}}}$"
                niepoprawne = [f"${p}^{{{w1 + w2}}}$", f"${p * p}^{{{w1 * w2}}}$", f"${p}^{{{abs(w1 - w2)}}}$"]

            # PIERWIASTKI
            elif typ == 3:
                rodzaj = random.choice(["kwadrat", "szescian"])
                if rodzaj == "kwadrat":
                    liczba = random.choice([16, 25, 36, 49, 64, 81, 100])
                    wynik = int(liczba ** 0.5)

                    tekst = r"Oblicz wartość pierwiastka: $\sqrt{" + str(liczba) + r"}$"
                    poprawna = f"${wynik}$"
                    niepoprawne = [f"${wynik - 1}$", f"${wynik + 2}$", f"${liczba * 2}$"]
                else:
                    liczba = random.choice([8, 27, 64, 125])
                    wynik = int(round(liczba ** (1 / 3)))
                    tekst = r"Oblicz wartość pierwiastka: $\sqrt[3]{" + str(liczba) + r"}$"
                    poprawna = f"${wynik}$"
                    niepoprawne = [f"${wynik + 1}$", f"${wynik - 1}$", f"${int(liczba / 3)}$"]

            elif typ == 4:

                zestawy = [(12, r"2\sqrt{3}", [r"3\sqrt{2}", r"4\sqrt{3}", r"2\sqrt{6}"]),
                           (18, r"3\sqrt{2}", [r"2\sqrt{3}", r"9\sqrt{2}", r"3\sqrt{6}"]),
                           (20, r"2\sqrt{5}", [r"5\sqrt{2}", r"4\sqrt{5}", r"2\sqrt{10}"]),
                           (32, r"4\sqrt{2}", [r"2\sqrt{8}", r"2\sqrt{4}", r"8\sqrt{2}"])]
                wybrane = random.choice(zestawy)
                tekst = r"Wyłącz czynnik przed znak pierwiastka: $\sqrt{" + str(wybrane[0]) + r"}$"
                poprawna = f"${wybrane[1]}$"
                niepoprawne = [f"${x}$" for x in wybrane[2]]

            # NOTACJA WYKŁADNICZA
            elif typ == 5:
                mnoznik = round(random.uniform(1.1, 9.9), 1)
                zera = random.randint(4, 7)
                liczba_int = int(mnoznik * (10 ** zera))
                tekst = f"Zapisz liczbę {liczba_int:,} w notacji wykładniczej:"
                poprawna = r"$" + f"{str(mnoznik).replace('.', ',')} \\cdot 10^{{{zera}}}" + r"$"
                niepoprawne = [
                    r"$" + f"{str(mnoznik).replace('.', ',')} \\cdot 10^{{{zera - 1}}}" + r"$",
                    r"$" + f"{str(mnoznik * 10).replace('.', ',')} \\cdot 10^{{{zera}}}" + r"$",
                    r"$" + f"{str(mnoznik).replace('.', ',')} \\cdot 10^{{{zera + 1}}}" + r"$"
                ]

            else:
                mnoznik = random.randint(1, 9)
                miejsca = random.randint(3, 6)
                ułamek = mnoznik / (10 ** miejsca)
                tekst = f"Zapisz liczbę {ułamek:.6f} w notacji wykładniczej:"
                poprawna = r"$" + f"{mnoznik} \\cdot 10^{{-{miejsca}}}" + r"$"
                niepoprawne = [
                    r"$" + f"{mnoznik} \\cdot 10^{{-{miejsca - 1}}}" + r"$",
                    r"$" + f"{mnoznik} \\cdot 10^{{{miejsca}}}" + r"$",
                    r"$" + f"{mnoznik * 10} \\cdot 10^{{-{miejsca}}}" + r"$"
                ]


            warianty = niepoprawne + [poprawna]
            random.shuffle(warianty)


            pytania.append({
                "tekst": tekst,
                "poprawna": poprawna,
                "warianty": warianty
            })



    def generuj_nowy_quiz():
        pytania = []

        # 12 Zadań
        for typ in range(1, 13):
            p = random.randint(2, 9)
            w1 = random.randint(2, 6)
            w2 = random.randint(2, 6)

            if typ == 1:
                wyb = random.choice(["mnozenie", "dzielenie"])
                if wyb == "mnozenie":
                    tekst = f"Uprość wyrażenie: ${p}^{{{w1}}} \\cdot {p}^{{{w2}}}$"
                    poprawna = f"${p}^{{{w1 + w2}}}$"
                    niepoprawne = [f"${p}^{{{w1 * w2}}}$", f"${p * 2}^{{{w1 + w2}}}$", f"${p}^{{{abs(w1 - w2)}}}$"]
                else:
                    w1_dzial = max(w1, w2) + 1
                    w2_dzial = min(w1, w2)
                    tekst = f"Uprość wyrażenie: ${p}^{{{w1_dzial}}} : {p}^{{{w2_dzial}}}$"
                    poprawna = f"${p}^{{{w1_dzial - w2_dzial}}}$"
                    niepoprawne = [f"${p}^{{{w1_dzial + w2_dzial}}}$", f"${p}^{{{w1_dzial * w2_dzial}}}$",
                                   f"$1^{{{w1_dzial - w2_dzial}}}$"]

            elif typ == 2:
                tekst = f"Uprość wyrażenie: $({p}^{{{w1}}})^{{{w2}}}$"
                poprawna = f"${p}^{{{w1 * w2}}}$"
                niepoprawne = [f"${p}^{{{w1 + w2}}}$", f"${p * p}^{{{w1 * w2}}}$", f"${p}^{{{abs(w1 - w2)}}}$"]

            elif typ == 3:
                rodzaj = random.choice(["kwadrat", "szescian"])
                if rodzaj == "kwadrat":
                    liczba = random.choice([16, 25, 36, 49, 64, 81, 100])
                    wynik = int(liczba ** (0.5))  # Poprawione z liczba(0.5) na potęgowanie
                    tekst = f"Oblicz wartość pierwiastka: $\\sqrt{{{liczba}}}$"
                    poprawna = f"${wynik}$"
                    niepoprawne = [f"${wynik - 1}$", f"${wynik + 2}$", f"${liczba * 2}$"]
                else:
                    liczba = random.choice([8, 27, 64, 125])
                    wynik = int(round(liczba ** (1 / 3)))  # Poprawione z liczba(1/3) na potęgowanie
                    tekst = f"Oblicz wartość pierwiastka: $\\sqrt[3]{{{liczba}}}$"
                    poprawna = f"${wynik}$"
                    niepoprawne = [f"${wynik + 1}$", f"${wynik - 1}$", f"${int(liczba / 3)}$"]

            elif typ == 4:
                zestawy = [
                    (12, "2\\sqrt{3}", ["3\\sqrt{2}", "4\\sqrt{3}", "2\\sqrt{6}"]),
                    (18, "3\\sqrt{2}", ["2\\sqrt{3}", "9\\sqrt{2}", "3\\sqrt{6}"]),
                    (20, "2\\sqrt{5}", ["5\\sqrt{2}", "4\\sqrt{5}", "2\\sqrt{10}"]),
                    (32, "4\\sqrt{2}", ["2\\sqrt{8}", "2\\sqrt{4}", "8\\sqrt{2}"])
                ]
                wybrane = random.choice(zestawy)
                tekst = f"Wyłącz czynnik przed znak pierwiastka: $\\sqrt{{{wybrane[0]}}}$"
                poprawna = f"${wybrane[1]}$"
                niepoprawne = [f"${x}$" for x in wybrane[2]]

            elif typ == 5:
                mnoznik = round(random.uniform(1.1, 9.9), 1)
                zera = random.randint(4, 7)
                liczba_int = int(mnoznik * (10 ** zera))
                tekst = f"Zapisz liczbę {liczba_int} w notacji wykładniczej:"
                poprawna = f"${str(mnoznik).replace('.', ',')} \\cdot 10^{{{zera}}}$"
                niepoprawne = [
                    f"${str(mnoznik).replace('.', ',')} \\cdot 10^{{{zera - 1}}}$",
                    f"${str(round(mnoznik * 10, 1)).replace('.', ',')} \\cdot 10^{{{zera}}}$",
                    f"${str(mnoznik).replace('.', ',')} \\cdot 10^{{{zera + 1}}}$"
                ]

            else:
                mnoznik = random.randint(1, 9)
                miejsca = random.randint(3, 6)
                ułamek = mnoznik / (10 ** miejsca)
                tekst = f"Zapisz liczbę {ułamek:.{miejsca}f} w notacji wykładniczej:"
                poprawna = f"${mnoznik} \\cdot 10^{{-{miejsca}}}$"
                niepoprawne = [
                    f"${mnoznik} \\cdot 10^{{-{miejsca - 1}}}$",
                    f"${mnoznik} \\cdot 10^{{{miejsca}}}$",
                    f"${mnoznik * 10} \\cdot 10^{{-{miejsca}}}$"
                ]


            warianty = niepoprawne + [poprawna]
            random.shuffle(warianty)
            pytania.append({"tekst": tekst, "poprawna": poprawna, "warianty": warianty})

        return pytania


    # Inicjalizacja sesji Streamlit
    if "zestaw_pytan" not in st.session_state:
        st.session_state.zestaw_pytan = generuj_nowy_quiz()

    # Wyświetlanie pytań w Streamlit
    for i, q in enumerate(st.session_state.zestaw_pytan):
        st.subheader(f"Zadanie {i + 1}")
        st.write(q["tekst"])

        odp = st.radio("Wybierz poprawną odpowiedź:", q["warianty"], index=None, key=f"rand_q_{i}")

        if odp:
            if odp == q["poprawna"]:
                st.success("🎉 Doskonale! To poprawna odpowiedź.")
            else:
                st.error("❌ Spróbuj ponownie. Zastanów się nad regułą matematyczną.")

        if i < len(st.session_state.zestaw_pytan) - 1:
            st.divider()
            st.write("")

    # Przycisk generowania nowego quizu
    if st.button("🔄 Generuj nowe zadania", type="primary"):
        st.session_state.zestaw_pytan = generuj_nowy_quiz()
        st.rerun()

# STOPKA 
st.divider()
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")
