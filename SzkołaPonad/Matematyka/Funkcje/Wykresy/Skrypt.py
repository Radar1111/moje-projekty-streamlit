import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

st.title("Asystent Matematyczny - Wykresy Funkcji")

with st.expander("💡 Zobacz jak wpisywać wzory funkcji:"):
    st.write("* `x**2` — x do kwadratu ($x^2$)")
    st.write("* `x**3` — x do sześcianu ($x^3$)")
    st.write("* `3*x` — mnożenie (pamiętaj o gwieździe `*`)")
    st.write("* `3*x + 2` — funkcje liniowe")
    
wzor = st.text_input("Wpisz wzór funkcji f(x):", value="x**2 - 4")

try:
    # 1. Analiza symboliczna (SymPy)
    x_sym = sp.symbols('x')
    wzor_sym = wzor.replace('np.', '').replace('numpy.', '')
    wyrazenie = sp.sympify(wzor_sym)

    # Miejsca zerowe (przecięcie z osią X)
    miejsca_zerowe = sp.solve(wyrazenie, x_sym)
    miejsca_rzeczywiste = []
    for mz in miejsca_zerowe:
        if mz.is_real:
            val = float(mz)
            if val not in miejsca_rzeczywiste:
                miejsca_rzeczywiste.append(round(val, 4))

    # Punkt przecięcia z osią Y
    # Podstawiamy x = 0 do wyrażenia
    y_inter_val = wyrazenie.subs(x_sym, 0)
    punkt_y_istnieje = y_inter_val.is_real
    if punkt_y_istnieje:
        y_intersection = round(float(y_inter_val), 4)

    # 2. Rysowanie wykresu (NumPy + Matplotlib)
    x = np.linspace(-10, 10, 400)
    safe_dict = {"x": x, "np": np, "numpy": np}
    y = eval(wzor, {"__builtins__": None}, safe_dict)

    fig, ax = plt.subplots()
    ax.plot(x, y, label=f"f(x) = {wzor}", color="blue", linewidth=2)

    # Zaznaczanie miejsc zerowych (Oś X)
    for mz in miejsca_rzeczywiste:
        if -10 <= mz <= 10:
            ax.plot(mz, 0, 'ro')
            ax.annotate(f"({mz}, 0)", (mz, 0), textcoords="offset points", xytext=(0, 10), ha='center', color='red',
                        weight='bold')

    # Zaznaczanie punktu przecięcia z osią Y
    if punkt_y_istnieje and -10 <= y_intersection <= 10:
        ax.plot(0, y_intersection, 'go')  # Zielona kropka dla osi Y
        ax.annotate(f"(0, {y_intersection})", (0, y_intersection), textcoords="offset points", xytext=(15, -5),
                    ha='left', color='green', weight='bold')

    ax.axhline(0, color='black', linewidth=0.5, ls='--')
    ax.axvline(0, color='black', linewidth=0.5, ls='--')
    ax.grid(True, linestyle=':')

    # Dynamiczna legenda, żeby opisać kolory kropek
    legenda_elementy = [plt.Line2D([0], [0], color='blue', lw=2, label=f"f(x) = {wzor}")]
    if miejsca_rzeczywiste:
        legenda_elementy.append(plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=8,
                                           label='Miejsce zerowe (X)'))
    if punkt_y_istnieje:
        legenda_elementy.append(plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=8,
                                           label='Przecięcie z osią Y'))
    ax.legend(handles=legenda_elementy)

    st.pyplot(fig)

    # 3. Wyświetlanie wyników w Streamlit
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📍 Miejsca zerowe (Oś X):")
        if miejsca_rzeczywiste:
            for mz in miejsca_rzeczywiste:
                st.success(f"**({mz}, 0)**")
        else:
            st.info("Brak miejsc zerowych.")

    with col2:
        st.subheader("📍 Przecięcie z osią Y:")
        if punkt_y_istnieje:
            st.success(f"**(0, {y_intersection})**")
        else:
            st.info("Funkcja nie przecina osi Y w liczbach rzeczywistych.")

except Exception as e:
    st.warning("Wpisz poprawny wzór funkcji. Zajrzyj do podpowiedzi powyżej, jeśli masz wątpliwości!")

st.divider()
st.caption("Najlepszy portal do matematyki - Szkoła Ponadpodstawowa")
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")
