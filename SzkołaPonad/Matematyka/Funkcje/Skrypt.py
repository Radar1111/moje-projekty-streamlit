import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt  # Dodany import do zaawansowanych wykresów

# Konfiguracja strony
st.set_page_config(page_title="Analizator Punktów Wspólnych Funkcji")

st.title("Analizator Miejsc Zerowych i Osi OY")
st.write("Aplikacja bada punkty przecięcia z osiami, krotności pierwiastków, znaki funkcji oraz równanie stycznej.")

# Panel boczny
st.sidebar.header("Ustawienia funkcji")
user_input = st.sidebar.text_input("Wpisz funkcję f(x):", value="sqrt(x - 1)")

st.sidebar.markdown("""
**Ściągawka ze składni:**
* Potęgowanie: `x**2`
* **Pierwiastek kwadratowy:** `sqrt(x-1)` lub `(x-1)**(0.5)`
* Mnożenie: `2*x` (zawsze używaj `*`)
* Nawiasy: `(x - 2)*(x + 1)`
""")

if user_input:
    try:
        x = sp.symbols('x')
        f = sp.sympify(user_input)

        # Wyświetlenie wzoru głównego
        st.latex(f"f(x) = {sp.latex(f)}")

        st.markdown("---")

        # 1. Przecięcie z osią OY i styczna
        st.subheader("1. Przecięcie z osią OY i Styczna")
        y_cross = f.subs(x, 0)
        pochodna = sp.diff(f, x)
        wsp_kierunkowy = pochodna.subs(x, 0)
        styczna = wsp_kierunkowy * x + y_cross

        if y_cross.is_real is False or 'I' in str(y_cross):
            st.info("**Punkt przecięcia z osią OY:** Brak (funkcja nie istnieje dla x = 0)")
            st.info("**Równanie prostej stycznej w punkcie (0, f(0)):** Brak stycznej w tym punkcie")
        else:
            st.info(f"**Punkt przecięcia z osią OY:** $(0, {y_cross})$")
            st.info(f"**Równanie prostej stycznej w punkcie (0, f(0)):** $y = {sp.latex(styczna)}$")

        # 2. Miejsca zerowe (Oś OX) i krotności
        st.subheader("2. Miejsca zerowe (Przecięcie z osią OX)")
        try:
            miejsca_zerowe = sp.roots(f, x)
            if miejsca_zerowe:
                for mz, krotnosc in miejsca_zerowe.items():
                    zachowanie = "odbija się od osi OX" if krotnosc % 2 == 0 else "przebija oś OX"
                    st.success(
                        f"* **$x = {mz}$** (krotność: {krotnosc}) $\\rightarrow$ wykres w tym punkcie **{zachowanie}**")
            else:
                mz_lista = sp.solve(f, x)
                if mz_lista:
                    mz_real = [res for res in mz_lista if res.is_real]
                    if mz_real:
                        st.success(f"Miejsca zerowe: $x = {mz_real}$")
                    else:
                        st.warning("Brak miejsc zerowych w zbiorze liczb rzeczywistych.")
                else:
                    st.warning("Brak miejsc zerowych w zbiorze liczb rzeczywistych.")
        except Exception:
            st.warning("Nie udało się automatycznie wyznaczyć miejsc zerowych.")

        # 3. Znak funkcji
        st.subheader("3. Znak funkcji")
        try:
            dodatnia = sp.solve(f > 0, x)
            ujemna = sp.solve(f < 0, x)
            st.write(f"* **Funkcja jest dodatnia ($f(x) > 0$):** ${sp.latex(dodatnia)}$")
            st.write(f"* **Funkcja jest ujemna ($f(x) < 0$):** ${sp.latex(ujemna)}$")
        except Exception:
            st.error("Równanie jest zbyt skomplikowane lub dziedzina ogranicza automatyczne wyznaczenie znaków.")

        # 4. Parzystość i nieparzystość
        st.subheader("4. Symetria wykresu")
        f_minus_x = f.subs(x, -x)
        if sp.simplify(f - f_minus_x) == 0:
            st.markdown("⭐ Funkcja jest **PARZYSTA** (wykres jest symetryczny względem osi OY).")
        elif sp.simplify(f + f_minus_x) == 0:
            st.markdown(
                "⭐ Funkcja jest **NIEPARZYSTA** (wykres jest symetryczny względem początku układu współrzędnych $(0,0)$).")
        else:
            st.markdown("Funkcja nie jest ani parzysta, ani nieparzysta (brak prostej symetrii).")

        # 5. Pełny układ współrzędnych (4 ćwiartki)
        st.markdown("---")
        st.subheader("5. Wizualizacja w układzie współrzędnych")

        f_num = sp.lambdify(x, f, "numpy")
        styczna_num = sp.lambdify(x, styczna, "numpy")

        # Zakres X obejmujący ćwiartki ujemne i dodatnie (od -7 do 7)
        x_vals = np.linspace(-7, 7, 500)

        try:
            # Obliczanie wartości dla f(x) z obsługą liczb zespolonych
            y_vals_f_complex = f_num(x_vals + 0j)
            y_vals_f = np.where(np.abs(np.imag(y_vals_f_complex)) > 1e-9, np.nan, np.real(y_vals_f_complex))

            # Tworzenie rysunku Matplotlib
            fig, ax = plt.subplots(figsize=(8, 6))

            # Rysowanie funkcji f(x)
            ax.plot(x_vals, y_vals_f, label="f(x)", color="blue", linewidth=2.5)

            # Rysowanie stycznej (jeśli istnieje)
            if y_cross.is_real and 'I' not in str(y_cross):
                y_vals_styczna = styczna_num(x_vals)
                if isinstance(y_vals_styczna, (int, float)):
                    y_vals_styczna = np.full_like(x_vals, y_vals_styczna)
                ax.plot(x_vals, y_vals_styczna, label="Styczna", color="orange", linestyle="--", linewidth=1.5)

            # USTAWIENIE OSI W CENTRUM (krzyż na punkcie 0,0)
            ax.spines['left'].set_position('zero')
            ax.spines['bottom'].set_position('zero')
            ax.spines['right'].set_color('none')
            ax.spines['top'].set_color('none')

            # Wykres zawsze pokazuje wszystkie ćwiartki
            ax.set_xlim([-6, 6])
            ax.set_ylim([-6, 6])


            ax.grid(True, which='both', linestyle=':', alpha=0.6)
            ax.legend(loc="upper left")

            # Wykres do Streamlita
            st.pyplot(fig)

        except Exception as plot_error:
            st.error(f"Nie udało się wygenerować wykresu. Błąd: {plot_error}")

    except Exception as e:
        st.error(f"Nie można przetworzyć funkcji. Sprawdź poprawność zapisu. Szczegóły: {e}")

st.divider()
st.caption("Najlepszy portal do matematyki - Szkoła Ponadpodstawowa")
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")
