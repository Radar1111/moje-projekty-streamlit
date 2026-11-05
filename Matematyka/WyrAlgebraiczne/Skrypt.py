import streamlit as st
import random

st.set_page_config(page_title="Wyrażenia Algebraiczne - Klasa 7", page_icon="🧮", layout="wide")

# Tytuł 
st.title("🧮 Wyrażenia Algebraiczne – Klasa 7")
st.markdown("Witaj w aplikacji, która pomoże Ci zrozumieć podstawy algebry!")

# Panel boczny 
menu = st.sidebar.radio(
    "Wybierz sekcję:",
    ["📖 Teoria i Przykłady", "✏️ Ćwiczenia Interaktywne", "📝 Quiz Sprawdzający"]
)

# TEORIA 
if menu == "📖 Teoria i Przykłady":
    st.header("Co to są wyrażenia algebraiczne?")
    st.write(
        "**Wyrażenie algebraiczne** to zapis matematyczny, w którym obok liczb i znaków działań "
        "(oraz nawiasów) pojawiają się **litery** (zmienne). Znak mnożenia między liczbą a literą zazwyczaj pomijamy (np. zamiast $3 \\cdot x$ piszemy $3x$)."
    )

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Słowniczek pojęć klasa 7:")
        st.markdown("""
        * **Jednomian:** Liczba, litera lub ich iloczyn (np. $7$, $x$, $-2ab^2$).
        * **Suma algebraiczna:** Wyrażenie powstałe z dodania lub odjęcia jednomianów (np. $2x + 3y - 5$).
        * **Wyrazy podobne:** Jednomiany, które mają identyczną część literową (np. $3ab$ oraz $-5ab$).
        * **Redukcja wyrazów podobnych:** Upraszczanie sumy poprzez dodawanie/odejmowanie wyrazów podobnych.
        """)

    with col2:
        st.subheader("Zapisywanie słowne na matematyczne:")
        st.markdown("""
        * *Liczba o 5 większa od x:* $x + 5$
        * *Liczba 3 razy mniejsza od y:* $\\frac{y}{3}$ lub $\\frac{1}{3}y$
        * *Kwadrat liczby a:* $a^2$
        * *Iloczyn liczb a i b:* $ab$
        """)

# ĆWICZENIA INTERAKTYWNE 
elif menu == "✏️ Ćwiczenia Interaktywne":
    st.header("Ucz się przez praktykę (Generator zadań)")
    st.markdown("Generuj losowe zadania, rozwiązuj je w zeszycie, a potem sprawdzaj swoje odpowiedzi!")

    st.subheader("1. Redukcja wyrazów podobnych")

    # Inicjalizacja zmiennych losowych w session_state, aby nie zmieniały się przy każdym kliknięciu
    if "rand_a" not in st.session_state:
        st.session_state.rand_a = random.randint(2, 9)
        st.session_state.rand_b = random.randint(2, 9)
        st.session_state.rand_c = random.randint(1, st.session_state.rand_a - 1)  # aby wynik z x był dodatni
        st.session_state.rand_d = random.randint(1, 5)

    # Przypisanie dla łatwiejszego czytania kodu
    a = st.session_state.rand_a
    b = st.session_state.rand_b
    c = st.session_state.rand_c
    d = st.session_state.rand_d

    # Wyświetlenie wygenerowanego wyrażenia
    st.write(f"Spróbuj zredukować wyrażenie: ${a}x + {b}y - {c}x + {d}y$")

    # Obliczenie poprawnego wyniku
    wynik_x = a - c
    wynik_y = b + d

    col_button1, col_button2 = st.columns([1, 4])
    with col_button1:
        pokaz_krok = st.button("Pokaż krok po kroku")
    with col_button2:
        # Przycisk do losowania nowego zadania (czyści stan sesji dla tych zmiennych)
        if st.button("🔄 Wylosuj nowe zadanie", key="nowe_redukcja"):
            del st.session_state.rand_a
            del st.session_state.rand_b
            del st.session_state.rand_c
            del st.session_state.rand_d
            st.rerun()

    if pokaz_krok:
        st.info(
            f"Pogrupujmy wyrazy podobne:\n"
            f"* Iksy: ${a}x - {c}x = {wynik_x}x$\n"
            f"* Igreki: ${b}y + {d}y = {wynik_y}y$\n\n"
            f"Wynik końcowy: **${wynik_x}x + {wynik_y}y$**"
        )

    st.write("---")

    st.subheader("2. Obliczanie wartości liczbowej")

    # Inicjalizacja zmiennych dla drugiego zadania
    if "rand_m" not in st.session_state:
        st.session_state.rand_m = random.randint(2, 6)
        st.session_state.rand_n = random.randint(2, 6)
        st.session_state.val_a = random.randint(-5, 5)
        st.session_state.val_b = random.randint(-5, 5)

    m = st.session_state.rand_m
    n = st.session_state.rand_n

    st.write(f"Oblicz wartość wyrażenia ${m}a + {n}b$ dla wylosowanych lub własnych wartości:")

    # Pola wejściowe dostają domyślnie wartości wylosowane, ale uczeń może je zmienić
    val_a = st.number_input("Podaj wartość za 'a':", value=st.session_state.val_a, key="input_a")
    val_b = st.number_input("Podaj wartość za 'b':", value=st.session_state.val_b, key="input_b")

    wynik_wartosci = m * val_a + n * val_b

    # Tworzymy napisy dla 'a' i 'b' - dają nawias TYLKO dla liczb ujemnych
    str_a = f"({val_a})" if val_a < 0 else f"{val_a}"
    str_b = f"({val_b})" if val_b < 0 else f"{val_b}"

    # Obliczamy iloczyny
    iloczyn_a = m * val_a
    iloczyn_b = n * val_b

    # Tworzymy napisy dla wyników mnożenia (też dają nawias tylko dla ujemnych)
    str_iloczyn_a = f"({iloczyn_a})" if iloczyn_a < 0 else f"{iloczyn_a}"
    str_iloczyn_b = f"({iloczyn_b})" if iloczyn_b < 0 else f"{iloczyn_b}"

    # Wyświetlamy gotowy komunikat z inteligentnymi nawiasami
    st.success(
        f"Dla a = {val_a} oraz b = {val_b}, wartość wyrażenia ${m}a + {n}b$ wynosi: **{wynik_wartosci}**\n\n"
        f"*(bo ${m} \\cdot {str_a} + {n} \\cdot {str_b} = {str_iloczyn_a} + {str_iloczyn_b} = {wynik_wartosci}$)*"
    )

    if st.button("🔄 Wylosuj inne liczby startowe", key="nowe_wartosc"):
        del st.session_state.rand_m
        del st.session_state.rand_n
        del st.session_state.val_a
        del st.session_state.val_b
        st.rerun()

# QUIZ 
elif menu == "📝 Quiz Sprawdzający":
    st.header("Sprawdź swoją wiedzę!")
    st.markdown(
        "Za każdym razem losujemy dla Ciebie **5 pytań** z naszej bazy. Odpowiedz na nie, a na końcu kliknij przycisk podsumowania.")

    # BAZA PYTAŃ 
    baza_pytan = [
        {
            "pytanie": "Jak zapiszesz wyrażenie: 'Liczba o 4 mniejsza od dwukrotności liczby x'?",
            "opcje": ["$4 - 2x$", "$2x - 4$", "$2(x - 4)$", "$\\frac{x}{2} - 4$"],
            "poprawna": 1,
            "wyjasnienie": "Dwukrotność liczby x to $2x$. Liczba o 4 mniejsza oznacza, że odejmujemy 4. Zatem: $2x - 4$."
        },
        {
            "pytanie": "Które z podanych jednomianów są wyrazami podobnymi?",
            "opcje": ["$2x$ i $2y$", "$3ab$ i $-ab$", "$x^2$ i $x^3$", "$5a$ i $5a^2$"],
            "poprawna": 1,
            "wyjasnienie": "Wyrazy podobne muszą mieć identyczne litery w tych samych potęgach. $3ab$ i $-ab$ spełniają ten warunek."
        },
        {
            "pytanie": "Zredukuj wyrażenie: $4a - 5 + 2a + 7$",
            "opcje": ["$6a + 2$", "$6a - 12$", "$2a + 2$", "$8a + 2$"],
            "poprawna": 0,
            "wyjasnienie": "Dodajemy wyrazy z literą: $4a + 2a = 6a$, a potem liczby: $-5 + 7 = 2$. Wynik to $6a + 2$."
        },
        {
            "pytanie": "Zapisz w jak najprostszej postaci wyrażenie: $3(2x - 4y)$",
            "opcje": ["$6x - 4y$", "$5x - y$", "$6x - 12y$", "$6x + 12y$"],
            "poprawna": 2,
            "wyjasnienie": "Mnożymy liczbę stojącą przed nawiasem przez każdy wyraz w nawiasie: $3 \\cdot 2x = 6x$ oraz $3 \\cdot (-4y) = -12y$. Otrzymujemy $6x - 12y$."
        },
        {
            "pytanie": "Opuść nawiasy i zredukuj wyrażenie: $5a - (2a - 3)$",
            "opcje": ["$3a - 3$", "$3a + 3$", "$7a - 3$", "$7a + 3$"],
            "poprawna": 1,
            "wyjasnienie": "Minus przed nawiasem zmienia znak każdego wyrazu w nawiasie na przeciwny: $5a - 2a + 3$. Po redukcji $5a - 2a$ otrzymujemy $3a + 3$."
        },
        {
            "pytanie": "Zeszyt kosztuje $x$ złotych, a długopis jest od niego o 3 złote tańszy. Jak zapisać koszt zakupu 2 zeszytów i 1 długopisu?",
            "opcje": ["$2x + x - 3$", "$2x + 3$", "$2x + (x + 3)$", "$3x + 3$"],
            "poprawna": 0,
            "wyjasnienie": "Cena zeszytu to $x$, więc 2 zeszyty kosztują $2x$. Długopis jest tańszy o 3 zł, czyli kosztuje $x - 3$. Łącznie: $2x + x - 3$."
        },
        {
            "pytanie": "Jaka jest wartość liczbowa wyrażenia $x^2 - 2x$ dla $x = -3$?",
            "opcje": ["$3$", "$-3$", "$15$", "$9$"],
            "poprawna": 2,
            "wyjasnienie": "Podstawiamy $-3$ w miejsce $x$: $(-3)^2 - 2 \\cdot (-3) = 9 - (-6) = 9 + 6 = 15$."
        },
        {
            "pytanie": "Które z poniższych wyrażeń NIE jest jednomianem?",
            "opcje": ["$-5x^2y$", "$\\frac{a}{4}$", "$2x + y$", "$xyz$"],
            "poprawna": 2,
            "wyjasnienie": "Jednomian to liczba, litera lub ich iloczyn. Wyrażenie $2x + y$ to suma algebraiczna."
        },
        {
            "pytanie": "Jak uprościsz wyrażenie $-2x \\cdot 4y$?",
            "opcje": ["$2xy$", "$-8xy$", "$-6xy$", "$8xy$"],
            "poprawna": 1,
            "wyjasnienie": "Mnożymy liczby przez siebie: $-2 \\cdot 4 = -8$, a litery dopisujemy: $-8xy$."
        },
        {
            "pytanie": "Wskaż jednomian stopnia trzeciego (suma wykładników potęg przy literach wynosi 3):",
            "opcje": ["$3x$", "$x^3$", "$3x^3$", "Zarówno $x^3$ jak i $3x^3$"],
            "poprawna": 3,
            "wyjasnienie": "Współczynnik liczbowy z przodu nie ma znaczenia. Liczy się tylko potęga zmiennej. Oba wyrażenia mają literę w trzeciej potędze."
        },
        {
            "pytanie": "Połowa liczby o 6 większej od $a$ to:",
            "opcje": ["$\\frac{a+6}{2}$", "$\\frac{a}{2} + 6$", "$2(a+6)$", "$a + 3$"],
            "poprawna": 0,
            "wyjasnienie": "Najpierw tworzymy liczbę o 6 większą od $a$, czyli $(a+6)$, a potem dzielimy ją przez 2."
        },
        {
            "pytanie": "Wyrażenie $a \\cdot a \\cdot a \\cdot b \\cdot b$ po uproszczeniu to:",
            "opcje": ["$3a + 2b$", "$a^3b^2$", "$3a^2b$", "$6ab$"],
            "poprawna": 1,
            "wyjasnienie": "Mnożenie tych samych liter zamieniamy na potęgowanie. Trzy litery $a$ to $a^3$, dwie litery $b$ to $b^2$. Wynik: $a^3b^2$."
        },
        {
            "pytanie": "Opuść nawias i zredukuj wyrażenie: $4(x - 2) + 3x$",
            "opcje": ["$7x - 2$", "$7x - 8$", "$4x - 8$", "$1x - 8$"],
            "poprawna": 1,
            "wyjasnienie": "Mnożymy nawias przez 4: $4 \\cdot x - 4 \\cdot 2 = 4x - 8$. Następnie dodajemy $3x$: $4x - 8 + 3x = 7x - 8$."
        },
        {
            "pytanie": "Tomek ma $x$ lat, a jego siostra Ania jest od niego o 4 lata starsza. Ile lat będą mieli łącznie za 3 lata?",
            "opcje": ["$2x + 4$", "$2x + 7$", "$2x + 10$", "$x + 7$"],
            "poprawna": 2,
            "wyjasnienie": "Obecny wiek Tomka to $x$, a Ani to $x + 4$. Za 3 lata Tomek będzie miał $x + 3$ lat, a Ania $(x + 4) + 3 = x + 7$ lat. Razem: $(x + 3) + (x + 7) = 2x + 10$."
        },
        {
            "pytanie": "Po uproszczeniu wyrażenia $\\frac{6x - 9}{3}$ otrzymamy:",
            "opcje": ["$2x - 9$", "$6x - 3$", "$2x - 3$", "$2x + 3$"],
            "poprawna": 2,
            "wyjasnienie": "Dzielimy każdy składnik licznika przez mianownik: $\\frac{6x}{3} = 2x$ oraz $\\frac{-9}{3} = -3$. Wynik to $2x - 3$."
        },
        {
            "pytanie": "W klasie jest $n$ chłopców, a dziewcząt jest o 15% więcej niż chłopców. Jak zapisać liczbę dziewcząt?",
            "opcje": ["$n + 15$", "$0{,}15n$", "$1{,}15n$", "$15n$"],
            "poprawna": 2,
            "wyjasnienie": "Dziewcząt jest 100% + 15% = 115% liczby chłopców. Zamieniając procent na ułamek, otrzymujemy $1{,}15n$."
        },
        {
            "pytanie": "Jak zapiszesz obwód prostokąta o bokach długości $2a$ oraz $a + 3$?",
            "opcje": ["$3a + 3$", "$6a + 6$", "$4a + 6$", "$2a(a + 3)$"],
            "poprawna": 1,
            "wyjasnienie": "Prostokąt ma dwa pary takich samych boków. Obwód to $2 \\cdot (2a) + 2 \\cdot (a + 3) = 4a + 2a + 6 = 6a + 6$."
        },
        {
            "pytanie": "Zredukuj wyrażenie: $x^2 - 3x + 2x^2 + 5x$",
            "opcje": ["$3x^2 + 2x$", "$3x^2 - 2x$", "$2x^2 + 2x$", "$5x^2$"],
            "poprawna": 0,
            "wyjasnienie": "Łączymy wyrazy podobne tego samego stopnia. Dla $x^2$: $1x^2 + 2x^2 = 3x^2$. Dla $x$: $-3x + 5x = 2x$. Wynik to $3x^2 + 2x$."
        },
        {
            "pytanie": "Jak zapisać: 'Iloraz kwadratu liczby $x$ przez liczbę 5'?",
            "opcje": ["$(5x)^2$", "$\\frac{x^2}{5}$", "$\\frac{2x}{5}$", "$x^2 - 5$"],
            "poprawna": 1,
            "wyjasnienie": "Kwadrat liczby $x$ to $x^2$. Iloraz oznacza dzielenie (kreskę ułamkową). Zatem dzielimy $x^2$ przez 5, co daje $\\frac{x^2}{5}$."
        },
        {
            "pytanie": "Opuść nawiasy i uprość wyrażenie: $-(x - 3y) + (2x - y)$",
            "opcje": ["$3x + 2y$", "$x + 2y$", "$x - 4y$", "$-3x - 4y$"],
            "poprawna": 1,
            "wyjasnienie": "Minus przed pierwszym nawiasem zmienia znaki: $-x + 3y$. Plus przed drugim zostawia znaki bez zmian: $+ 2x - y$. Łączymy: $(-x + 2x) + (3y - y) = x + 2y$."
        }
    ]

    # LOSOWANIE DO SESSION_STATE
    # Losujemy zestaw pytań TYLKO RAZ, gdy uczeń wchodzi do quizu.
    if "wylosowane_pytania" not in st.session_state:
        # random.sample pobiera 5 UNIKALNYCH losowych elementów z bazy
        st.session_state.wylosowane_pytania = random.sample(baza_pytan, 5)

    pytania = st.session_state.wylosowane_pytania

    # Przycisk u góry, jeśli uczeń chce zresetować i wylosować inne pytania
    if st.button("🔄 Wylosuj inny zestaw pytań"):
        del st.session_state.wylosowane_pytania
        st.rerun()

    st.write("---")

    # FORMULARZ QUIZU 
    with st.form("quiz_form"):
        odpowiedzi_uzytkownika = {}

        for i, p in enumerate(pytania):
            st.markdown(f"#### Pytanie {i + 1}: {p['pytanie']}")
            wybor = st.radio(
                f"Wybierz odpowiedź do pytania {i + 1}:",
                p["opcje"],
                key=f"q_{i}",
                index=None,
                label_visibility="collapsed"
            )
            if wybor is not None:
                odpowiedzi_uzytkownika[i] = p["opcje"].index(wybor)
            st.write("---")

        submitted = st.form_submit_button("Podsumuj mój wynik", type="primary")

    # SPRAWDZANIE WYNIKÓW
    if submitted:
        uaktualnione_punkty = 0
        bledne_pytania = []

        st.write("### 📊 Wyniki szczegółowe:")
        for i, p in enumerate(pytania):
            user_ans = odpowiedzi_uzytkownika.get(i, None)

            if user_ans == p["poprawna"]:
                uaktualnione_punkty += 1
                st.success(f"**Pytanie {i + 1}:** Poprawnie! 🎉")
            else:
                bledne_pytania.append(i + 1)
                wybrana_odp = p["opcje"][user_ans] if user_ans is not None else "Brak odpowiedzi"
                st.error(f"**Pytanie {i + 1}:** Błąd. Twoja odpowiedź: {wybrana_odp}")
                st.info(f"💡 **Wyjaśnienie:** {p['wyjasnienie']}")

        st.balloons()
        st.metric(label="Twój całkowity wynik", value=f"{uaktualnione_punkty} / {len(pytania)}")

        if uaktualnione_punkty == len(pytania):
            st.success("Genialnie! Wzorowy wynik! 🏆 Wszystkie odpowiedzi są poprawne.")
        elif uaktualnione_punkty >= len(pytania) / 2:
            st.info(f"Dobry wynik! Przejrzyj jeszcze raz pytania, w których pojawił się błąd: {bledne_pytania}")
        else:
            st.warning(f"Warto jeszcze poćwiczyć teorię. Błędy pojawiły się w pytaniach: {bledne_pytania}")

# --- STOPKA ---
st.divider()
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")
