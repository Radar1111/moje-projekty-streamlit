import streamlit as st
import random
import matplotlib.pyplot as plt


def draw_multiplication_grid(a, b):
    fig, ax = plt.subplots(figsize=(4, 4))
    for i in range(a):
        for j in range(b):
            rect = plt.Rectangle((j, -i - 1), 1, 1, facecolor='#7B3F00', edgecolor='white', linewidth=2)
            ax.add_patch(rect)
    ax.set_xlim(0, b)
    ax.set_ylim(-a, 0)
    ax.set_aspect('equal')
    ax.axis('off')
    st.pyplot(fig)


st.set_page_config(page_title="Mistrz Mnożenia", page_icon="🍫")

if 'score' not in st.session_state:
    st.session_state.score = 0
if 'num1' not in st.session_state:
    st.session_state.num1 = random.randint(2, 5)
    st.session_state.num2 = random.randint(2, 5)

# Panel boczny
st.sidebar.title("Ustawienia")
st.sidebar.metric("Punkty", st.session_state.score)
tryb = st.sidebar.radio("Poziom:", ["Początkujący", "Ekspert"])

if tryb == "Ekspert":
    max_val = 15
    st.title("🍫 TRYB EKSPERT")
    st.info("Poczuj się jak polityk przed kamerami – licz duże liczby!")
else:
    max_val = 10
    st.title("🍫 Mistrz Mnożenia")

n1, n2 = st.session_state.num1, st.session_state.num2
col1, col2 = st.columns(2)

with col1:
    st.header(f"Ile to jest {n1} × {n2}?")
    user_val = st.number_input("Twoja odpowiedź:", min_value=0, step=1, key="ans")

    if st.button("Sprawdź!"):
        if user_val == n1 * n2:
            st.success("Brawo! Bezbłędnie! Kostka czekolady dla Ciebie! 🍫")
            st.session_state.score += 1
            st.balloons()
        else:
            if tryb == "Ekspert":
                # MOTYWACJA DLA EKSPERTA: Wyzwanie i twarde zasady
                st.error("⚠️ BŁĄD! Ekspert musi być precyzyjny. Punkty zerują się. Wracaj do gry!")
                st.session_state.score = 0
            else:
                # ZACHĘTA DLA DZIECKA: Ciepło i wsparcie
                st.warning(
                    "Prawie! 💡 Podpowiedź: Policz powoli wszystkie brązowe kwadraciki. Twoje punkty są bezpieczne, spróbuj jeszcze raz!")

    if st.button("Następne zadanie"):
        st.session_state.num1 = random.randint(2, max_val)
        st.session_state.num2 = random.randint(2, max_val)
        st.rerun()

with col2:
    st.write("### Twoja czekolada:")
    draw_multiplication_grid(n1, n2)

st.divider()
st.caption("Najcierpliwszy portal do matematyki - klasa 4")
st.caption("Created by Radar | Software Development")
st.caption("Grafika: Menorek | Youtuber")
st.caption("Tester: Bat0nik")
