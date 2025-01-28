## Author: Victor E Balasoto
## Last Update: 1/23/25
## Purpose: For PGT golfers use

# ----------------------------------------------------------
# > Open CLI
# > cd C:\Users\PC\Desktop\PGT
# > .venv\Scripts\activate
# > streamlit run scorecard_stableford.py
# ----------------------------------------------------------

import streamlit as st
import pandas as pd


def main():
    '''Create scorecard'''
    
    ## Read specific columns by index
    df_names = pd.read_excel('GolfCoursePar.xlsx', usecols=["Knights Play", "Brevofield", "Quaker Creek", "Raleigh Golf", "Zebulon CC"])
    
    kp = pd.read_excel('GolfCoursePar.xlsx', usecols=[0, 1])
    bf = pd.read_excel('GolfCoursePar.xlsx', usecols=[0, 2])
    qc = pd.read_excel('GolfCoursePar.xlsx', usecols=[0, 3])
    rg = pd.read_excel('GolfCoursePar.xlsx', usecols=[0, 4])
    zc = pd.read_excel('GolfCoursePar.xlsx', usecols=[0, 5])
    
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
    course_name = ["Knights Play", "Brevofield", "Quaker Creek", "Raleigh GA", "Zebulon CC", "Custom"]
    golf_course = st.sidebar.selectbox("Golf Course", course_name)

    if golf_course == "Custom":
        custom_input = st.sidebar.text_input("Write the name of Golf Course :")
        if custom_input:
            st.write(f'You are playing :  **_{custom_input} Golf Course_**')
    else:
        st.write(f'You are playing :  **_{golf_course} Golf Course_**')
    
    if golf_course == "Knights Play":
        st.sidebar.write(kp)
    elif golf_course == "Brevofield":
        st.sidebar.write(bf)
    elif golf_course == "Quaker Creek":
        st.sidebar.write(qc)
    elif golf_course == "Raleigh GA":
        st.sidebar.write(rg)
    elif golf_course == "Zebulon CC":
        st.sidebar.write(zc)

    if golf_course == 'Knights Play':
        holes = [f"Hole {i}" for i in range(1, 10)]  # List of holes (1 to 9)
    else:
        holes = [f"Hole {i}" for i in range(1, 19)]  # List of holes (1 to 18)
    
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
            st.write(f"{player}: **{total}**")
        
if __name__ == '__main__':
    main()
