import streamlit as st
import time

running = False
BREAK_TIME_MULTIPLIER = 0.2

st.markdown(
    """
    <style>
        div[data-testid="column"]:nth-of-type(1)
        {
            # border:1px solid red;
        } 

        div[data-testid="column"]:nth-of-type(2)
        {
            # border:1px solid blue;
            text-align: end;
        } 
    </style>
    """,unsafe_allow_html=True
)

def display_formatted_time(time_in_seconds):
    mins, secs = divmod(round(time_in_seconds), 60)
    time_formatted = '{:02d}:{:02d}'.format(mins, secs)
    st.header(f"{time_formatted}")  # TODO: why formatted string?

def display_times(time_in_seconds):
    col1, col2 = st.columns(2)
    with col1:
        display_formatted_time(time_in_seconds)
    with col2:
        display_formatted_time(time_in_seconds*BREAK_TIME_MULTIPLIER)

def count_down(frequency=0.1):
    """
    Counts time down from time_in_seconds to zero.
    """
    global running
    time_in_seconds = st.session_state["time_in_seconds"]
    start_time = time.time()
    end_time = start_time + (time_in_seconds * BREAK_TIME_MULTIPLIER)
    with st.empty():
        while time_in_seconds > 0 and running:  # TODO: think about and check edge cases
            display_times(time_in_seconds / BREAK_TIME_MULTIPLIER)
            time.sleep(frequency)
            time_in_seconds = max(end_time - time.time(), 0)
            st.session_state["time_in_seconds"] = time_in_seconds / BREAK_TIME_MULTIPLIER   # TODO: is it needed?
    # display_time(time_in_seconds)
    # st.write("End of break!")    # TODO: add sound
    st.balloons()


def count_up(frequency=0.1):
    """
    Counts elapsed time. The result is stored in st.session_state["time_in_seconds"]
    """
    global running
    time_in_seconds = st.session_state["time_in_seconds"]
    start_time = time.time() - time_in_seconds
    with st.empty():
        while running:
            display_times(time_in_seconds)
            time.sleep(frequency)
            time_in_seconds = time.time() - start_time
            st.session_state["time_in_seconds"] = time_in_seconds
    # TODO: add max number of seconds


def main():
    st.title("Flowtime technique app")
    global running
    if "time_in_seconds" not in st.session_state:
        st.session_state["time_in_seconds"] = 0

    if st.button("RESET TIMER"):
        st.session_state.time_in_seconds = 0

    selected_action = st.select_slider(
        "Current action:",
        options=["WORK", "STOP", "BREAK"],
        value="STOP"
    )
    if selected_action == "WORK":
        running = True
        count_up()
    elif selected_action == "STOP":
        running = False
        display_times(st.session_state.time_in_seconds)
    elif selected_action == "BREAK":
        running = True
        count_down()
        


if __name__ == '__main__':
    main()
