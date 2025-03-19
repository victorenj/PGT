## Author: Victor E Balasoto
## Last Update: 3/10/25
## Purpose: For PGT golfers use

import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="PGT Modified Stableford",
    page_icon=":golfer:",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("PGT Modified Stableford")
    st.logo("assets/pgt_logo2_blk.jpg", size="large")

    # --- Sidebar for player input ---
    st.sidebar.header("Player Information")
    num_players = st.sidebar.number_input("Number of Players", min_value=1, max_value=4, value=1)
    player_names = []
    
    for i in range(num_players):
        player_name = st.sidebar.text_input(f"Enter name for Player {i + 1}", value=f"Player {i + 1}")
        player_names.append(player_name)

    # --- Sidebar for course input ---
    st.sidebar.header("Course Information")
    course_name = ["Knights Play", "Brevofield", "Quaker Creek", "Raleigh GA", "Zebulon CC", "Custom"]
    selected_course = st.sidebar.selectbox("Golf Course", course_name)

    if selected_course == "Custom":
        custom_input = st.sidebar.text_input("Write the name of Golf Course :")
        if custom_input:
            st.subheader(f'**_{custom_input} Golf Course_**')
    else:
        st.subheader(f'**_{selected_course} Golf Course_**')

    try:
        df_all = pd.read_excel('GolfCoursePar.xlsx')
        course_mapping = {
        'Knights Play': [0, 1],
        'Brevofield': [0, 2],
        'Quaker Creek': [0, 3],
        'Raleigh GA': [0, 4],
        'Zebulon CC': [0, 5]
        }

        if selected_course in course_mapping:
            cols = course_mapping[selected_course]
            df = df_all.iloc[:, cols].T  # Transpose the DataFrame for display
            df.iloc[1:, :] = df.iloc[1:, :].fillna(0).astype(int)
        else:
            pass
            df = pd.DataFrame()  # Empty DataFrame if no match
        
    except Exception as e:
        st.error(f"An error occurred while loading the file: {e}")

    if selected_course != "Custom":
        st.dataframe(df)

    # --- Hole & total scores ---
    holes = [f"Hole {i}" for i in range(1, 19)]  # List of holes (1 to 18)
    score_value = pd.DataFrame(index=player_names, columns=holes)
    columns = st.columns(18, gap="small", vertical_alignment="top")
    
    options = {
        'Zero': 0,
        'Bogey': 1,
        'Par': 3,
        'Birdie': 6,
        'Eagle': 10
    }
    
    for hole, column in zip(holes, columns):
        with column:
            for player in player_names:
                score_key = st.selectbox(f"{player} ({hole})", options.keys())
                score_value.loc[player, hole] = options[score_key]
    
    scol1, scol2, scol3 = st.columns([2,1.25,.75], gap='small')

    with scol1:
        st.subheader("Player Scorecard")
        st.dataframe(score_value)

    with scol2:
        total_scores = score_value.sum(axis=1).astype(int)
        total_scores_df = total_scores.to_frame(name='Total Score')

        if not total_scores.empty:
            max_score = total_scores.max()
            winner_df = pd.DataFrame({
                'Player': total_scores.index,
                'Total Score': total_scores.values
            })
            st.subheader("Leaderboard")
            st.dataframe(
                winner_df.style.highlight_max(axis=0, color='green'),
                use_container_width=True
            )

    with scol3:
        csv = total_scores_df.to_csv(index=False)
        st.download_button(
            label="Download Total Scores as CSV",
            data=csv,
            file_name="golf_scorecard.csv",
            mime="text/csv"
        )    

if __name__ == '__main__':
    main()
