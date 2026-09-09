import math
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Geometria", layout="wide")
st.title("Interaktywny Pomocnik do Geometrii")

# Menu boczne - rozdzielono elementy w liście
opcja = st.sidebar.radio("Co chcesz robić?", ["Rysowanie figur", "Obliczanie kątów"])

if opcja == "Rysowanie figur":
    figura = st.selectbox("Wybierz figurę", ["Prostokąt", "Kwadrat", "Koło"])

    col1, col2 = st.columns(2)

    with col1:
        if figura == "Prostokąt":
            a = st.number_input("Bok A", min_value=1.0, value=5.0)
            b = st.number_input("Bok B", min_value=1.0, value=3.0)
            pole = a * b
            obwod = 2 * (a + b)

            # Ściągawka ze wzorami dla ucznia
            st.warning(
                "📐 **Ściągawka ze wzorów:**\n* **Pole:** $P = a \\cdot b$\n* **Obwód:** $Obw = 2 \\cdot a + 2 \\cdot b$")

            st.success(f"**Pole:** {pole:.2f}")
            st.success(f"**Obwód:** {obwod:.2f}")

        elif figura == "Kwadrat":
            a = st.number_input("Bok A", min_value=1.0, value=4.0)
            b = a

            st.warning(
                "📐 **Ściągawka ze wzorów:**\n"
                "* **Pole:** $P = a \\cdot a = a^2$\n"
                "* **Obwód:** $Obw = 4 \\cdot a$"
            )

            st.success(f"**Pole:** {a ** 2:.2f}")
            st.success(f"**Obwód:** {4 * a:.2f}")

        elif figura == "Koło":
            a = st.number_input("Promień (r) - to odcinek, który łączy środek koła z jego brzegiem (okręgiem)", min_value=1.0, value=3.0)
            b = a


            st.warning(
                "📐 **Ściągawka ze wzorów:**\n"
                "* **Pole:** $P = \\pi \\cdot r \\cdot r = \\pi \\cdot r^2$\n"
                "* **Obwód:** $Obw = 2 \\cdot \\pi \\cdot r$\n\n"
                "*Przypomnienie dla czwartoklasisty: $\\pi$ to magiczna liczba, która wynosi około 3.14! "
                "Dlatego Twój obwód liczymy tak: $Obw = 2 \\cdot 3.14 \\cdot r$*"
            )

            st.success(f"**Pole:** {3.14 * (a ** 2):.2f}")
            st.success(f"**Obwód:** {2 * 3.14 * a:.2f}")

    with col2:
        fig, ax = plt.subplots()
        if figura in ["Prostokąt", "Kwadrat"]:
            ksztalt = plt.Rectangle(
                (0, 0), a, b, color="skyblue", ec="blue", lw=2
            )
            ax.add_patch(ksztalt)
            ax.set_xlim(-1, max(a, b) + 2)
            ax.set_ylim(-1, max(a, b) + 2)
        elif figura == "Koło":
            # Dedykowane rysowanie koła
            ksztalt = plt.Circle((0, 0), a, color="skyblue", ec="blue", lw=2)
            ax.add_patch(ksztalt)
            ax.set_xlim(-a - 1, a + 1)
            ax.set_ylim(-a - 1, a + 1)

        ax.set_aspect("equal")
        st.pyplot(fig)

elif opcja == "Obliczanie kątów":
    st.subheader("📐 Ekipa Trzech Kątów — Tajemnica 180 Stopni!")

    # Sekcja edukacyjna dla czwartoklasisty
    with st.expander("💡 Kliknij tutaj, aby dowiedzieć się, jak liczymy kąty!", expanded=True):
        st.markdown("""
        ### 🌟 Złota zasada każdego trójkąta:
        Nieważne, czy trójkąt jest malutki, wielki, chudy czy gruby — gdybyśmy odcięli wszystkie jego trzy rogi i ułożyli je obok siebie, **zawsze stworzą idealną linię prostą** (czyli kąt półpełny).

        * **Suma wszystkich trzech kątów to zawsze dokładnie 180°!**
        * Jeśli znasz dwa kąty, to trzeci znajdziesz bardzo łatwo: odejmij te dwa znane kąty od liczby 180.
        * *Przykład:* Jeśli jeden kąt ma 60°, a drugi 40° (razem 100°), to trzeci musi mieć: 180° - 100° = 80°!
        """)

    col1, col2 = st.columns(2)

    with col1:
        st.write("### 📏 Podaj boki trójkąta:")
        a = st.number_input("Bok a", min_value=0.1, value=3.0)
        b = st.number_input("Bok b", min_value=0.1, value=4.0)
        c = st.number_input("Bok c", min_value=0.1, value=5.0)

        if a + b > c and a + c > b and b + c > a:
            alpha_rad = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))
            beta_rad = math.acos((a ** 2 + c ** 2 - b ** 2) / (2 * a * c))
            gamma_rad = math.acos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b))

            alpha = math.degrees(alpha_rad)
            beta = math.degrees(beta_rad)
            gamma = math.degrees(gamma_rad)

            st.write("### 📊 Wyniki pomiarów:")
            st.success(f"**Kąt α (alfa):** {alpha:.0f}°")
            st.success(f"**Kąt β (beta):** {beta:.0f}°")
            st.success(f"**Kąt γ (gamma):** {gamma:.0f}°")

            # Zaokrąglamy do .0f
            st.info(
                f"🔍 **Sprawdźmy:** {alpha:.0f}° + {beta:.0f}° + {gamma:.0f}° = {alpha + beta + gamma:.0f}°! Widzisz? Zawsze wychodzi 180°!")

            x_c = b * math.cos(alpha_rad)
            y_c = b * math.sin(alpha_rad)
        else:
            st.error(
                "❌ Z tych boków nie da się zbudować trójkąta! Pamiętaj: suma dwóch krótszych boków musi być większa niż najdłuższy bok!")
            x_c, y_c = None, None

    with col2:
        if x_c is not None:
            fig, ax = plt.subplots()
            punkty_x = [0, c, x_c, 0]
            punkty_y = [0, 0, y_c, 0]

            ax.plot(punkty_x, punkty_y, color="blue", lw=3)
            ax.fill(punkty_x, punkty_y, color="skyblue", alpha=0.4)

            # Dodanie podpisów kątów na rysunku
            ax.text(0.3, 0.2, f"{alpha:.0f}°", fontsize=12, fontweight='bold')
            ax.text(c - 0.7, 0.2, f"{beta:.0f}°", fontsize=12, fontweight='bold')
            ax.text(x_c, y_c - 0.4, f"{gamma:.0f}°", fontsize=12, fontweight='bold')

            ax.set_xlim(-1, max(c, x_c) + 1)
            ax.set_ylim(-1, max(max(punkty_y), 1) + 1)
            ax.set_aspect("equal")
            ax.axis('off')  # Ukrywamy osie wykresu
            st.pyplot(fig)
