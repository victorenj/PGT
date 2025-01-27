## Author: Victor E Balasoto
## Last Update: 1/23/25
## Purpose: For PGT golfers use

# ----------------------------------------------------------
# > Open CLI
# > cd C:\Users\PC\Desktop\Golf
# > Scripts\activate
# > streamlit run scorecard_stableford.py
# ----------------------------------------------------------

import streamlit as st
import pandas as pd


## Read specific columns by name
df_names = pd.read_excel('GolfCoursePar.xlsx', usecols=["Brevofield", "Quaker Creek", "Knights Play"])
#bf = df_names["Brevofield"]
#qc = df_names["Quaker Creek"]
#kp = df_names["Knights Play"]

## Read specific columns by index
bf = pd.read_excel('GolfCoursePar.xlsx', usecols=[0, 1])
qc = pd.read_excel('GolfCoursePar.xlsx', usecols=[0, 2])
kp = pd.read_excel('GolfCoursePar.xlsx', usecols=[0, 3])

# Title of the app
st.logo("assets/pgt_logo2_blk.jpg", size="large")
st.title("PGT Stableford Scorecard")
st.subheader("*Pinoy Golf Tour*")

# Sidebar for player input
st.sidebar.header("Player Information")
num_players = st.sidebar.number_input("Number of Players", min_value=1, max_value=4, value=1)
player_names = []

for i in range(num_players):
    player_name = st.sidebar.text_input(f"Enter name for Player {i + 1}", value=f"Player {i + 1}")
    player_names.append(player_name)

# Sidebar for course input
golf_course = st.sidebar.selectbox(
        "Golf Course",
        ("Brevofield", "Quaker Creek", "Knights Play")
)

nine_holes = st.sidebar.radio("Number of holes :", ['18 holes', '9 holes'], horizontal=True)

if golf_course == "Brevofield":
    st.sidebar.write(bf)
elif golf_course == "Quaker Creek":
    st.sidebar.write(qc)
elif golf_course == "Knights Play":
    st.sidebar.write(kp)

if nine_holes == '18 holes':
    holes = [f"Hole {i}" for i in range(1, 19)]  # List of holes (1 to 18)
if nine_holes == '9 holes':
    holes = [f"Hole {i}" for i in range(1, 10)]  # List of holes (1 to 9)

# Initialize a DataFrame to store scores and points
score_value = pd.DataFrame(index=holes, columns=player_names)

# Input scores for each hole and player
columns = st.columns(4, gap="small", vertical_alignment="center")

options = {
    'Zero': 0,
    'Bogey': 1,
    'Par': 2,
    'Birdie': 3,
    'Eagle': 4
}

for player, column in zip(player_names, columns):
    with column:
        st.subheader(f'{player}')
        for hole in holes:
            score_key = st.selectbox(f"{hole} ({player})", options.keys())
            score_value.loc[hole, player] = options[score_key]

scol1, scol2 = st.columns(2, gap='large')
with scol1:
    # Display the scorecard table
    st.subheader("Scorecard Table")
    st.dataframe(score_value)
with scol2:
    # Display total scores for players
    st.subheader("Total Scores")
    total_scores = score_value.sum(axis=0)
    for player, total in total_scores.items():
        #st.subheader(f"Score for {player}")
        st.write(f"{player}: **{total}**")