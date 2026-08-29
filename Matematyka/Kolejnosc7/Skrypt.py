import streamlit as st

# Konfiguracja strony
st.set_page_config(page_title="Trener Kolejności działań - Klasa 7", page_icon="🧮")

st.title("🧮 Mistrz Kolejności Działań - Klasa 7")
st.write("W 7 klasie do tradycyjnych działań dołączają potęgi i pierwiastki. Sprawdź, jak zmieniają one reguły gry.")

# Ściąga
st.header("🔝 Hierarchia działań w klasie 7")

# Formatowanie tabeli dla stabilnego renderowania KaTeX w Streamlit
st.markdown(r"""

| Poziom | Co wykonujemy najpierw? | Przykłady |
| :---: | :--- | :--- |
| **1️⃣** | **Nawiasy** (działania w nich zawarte) | $(5 + 3) \cdot 2$ $\rightarrow$ najpierw $5+3$ |
| **2️⃣** | **Potęgowanie i Pierwiastkowanie** 💥 | $2 \cdot 3^2$ $\rightarrow$ najpierw $3^2 = 9$|
| **3️⃣** | **Mnożenie i dzielenie** (od lewej do prawej) | $12 : 2 \cdot 3$ $\rightarrow$ najpierw $12:2 = 6$|
| **4️⃣** | **Dodawanie i Odejmowanie** (od lewej do prawej) | $10 - 4 + 2$ $\rightarrow$ najpierw $10-4 = 6$ |
""")

st.divider()

# Interaktywny trener
st.header("🧠 Interaktywny Trener Krok Po Krok")
st.write("Wybierz jedno z gotowych, siódmoklasowych zadań, aby zobaczyć jak krok po kroku rozpisać kolejność działań:")

# Lista opcji wyciągnięta do czytelnej listy
opcje_zadan = [
    "Przykład A (Potęga przed mnożeniem)",
    "Przykład B (Pierwiastek w nawiasie)",
    "Przykład C (Od lewej do prawej z potęgą)",
    "Przykład D (Wszystko na raz)"
]

wybor = st.selectbox("Wybierz przykład do analizy:", opcje_zadan)

if wybor == "Przykład A (Potęga przed mnożeniem)":
    st.code("Zadanie: 5 ⋅ 2³", language="text")
    st.info(r"""
    **Jak to rozwiązać krok po kroku?**
    1. Najpierw wykonujemy **potęgowanie**: $2^3 = 2 \cdot 2 \cdot 2 = 8$.
    2. Dopiero teraz robimy **mnożenie**: $5 \cdot 8 = 40$.

    *Częsty błąd siódmoklasisty:* Pomnożenie $5 \cdot 2 = 10$ i podniesienie $10^3 = 1000$. To wielki błąd!
    """)
    st.success("Ostateczny wynik: **40**")

elif wybor == "Przykład B (Pierwiastek w nawiasie)":
    st.code("Zadanie: (12 - √9) ⋅ 2", language="text")
    st.info(r"""
    **Jak to rozwiązać krok po kroku?**
    1. Chcemy obliczyć nawias, ale wewnątrz niego pierwszeństwo ma **pierwiastek**: $\sqrt{9} = 3$.
    2. Kończymy działanie w **nawiasie**: $12 - 3 = 9$.
    3. Na końcu wykonujemy **mnożenie**: $9 \cdot 2 = 18$.
    """)
    st.success("Ostateczny wynik: **18**")

elif wybor == "Przykład C (Od lewej do prawej z potęgą)":
    st.code("Zadanie: 4² : 2 ⋅ 3", language="text")
    st.info(r"""
    **Jak to rozwiązać krok po kroku?**
    1. Absolutny priorytet ma **potęgowanie**: $4^2 = 16$. Wyrażenie ma teraz postać: $16 : 2 \cdot 3$.
    2. Ponieważ mnożenie i dzielenie są równorzędne, wykonujemy je **od lewej do prawej**!
    3. Najpierw dzielenie: $16 : 2 = 8$. Wyrażenie ma postać: $8 \cdot 3$.
    4. Na końcu mnożenie: $8 \cdot 3 = 24$.

    *Uwaga:* Gdybyś najpierw pomnożył $2 \cdot 3 = 6$, wyszedłby zły wynik ($16 : 6$)!
    """)
    st.success("Ostateczny wynik: **24**")

elif wybor == "Przykład D (Wszystko na raz)":
    st.code("Zadanie: 10 + √16 ⋅ 3 - 2²", language="text")
    st.info(r"""
    **Jak to rozwiązać krok po kroku?**
    1. Najpierw **potęgi i pierwiastki** równocześnie: $\sqrt{16} = 4$ oraz $2^2 = 4$. Wyrażenie to teraz: $10 + 4 \cdot 3 - 4$.
    2. Teraz pierwszeństwo ma **mnożenie**: $4 \cdot 3 = 12$. Wyrażenie to teraz: $10 + 12 - 4$.
    3. Dodawanie i odejmowanie robimy **od lewej do prawej**: $10 + 12 = 22$, a potem $22 - 4 = 18$.
    """)
    st.success("Ostateczny wynik: **18**")
