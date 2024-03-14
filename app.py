import streamlit as st
import pandas as pd

st.set_page_config(page_title="Historical UFC Rax", page_icon="🥊", layout="wide", initial_sidebar_state="collapsed")

hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
    </style>
'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

st.title("Historical UFC Rax")
st.write("Click on 'more data' for RAX calculation. Displays top 30 but data exists for 2405 fighters.")
st.write("Made by @yangsl")
st.markdown("""<br><br>""", unsafe_allow_html=True)

df = pd.read_csv("final_values.csv")


left_column, right_column = st.columns([2, 2])

with left_column:

    search_query = st.text_input("Search by fighter name:", "")

    num_rows_to_display = st.selectbox("Number of rows to display:", options=[10, 20, 30, 40, 50, 100], index=2)

with right_column :
        
    mode = st.selectbox("Viewing Options", options=["Rankings", "Compare Fighters"], index=0) 

st.markdown("""<br><br>""", unsafe_allow_html=True)

reset_button = st.button("Reset All Multipliers")



def reset_multipliers():
    for key in st.session_state.keys():
        if key.startswith("multiplier_"):
            st.session_state[key] = 1.2
        if key.startswith("value_"):
            fighter_name = key.replace("value_", "").replace("_", " ")
            original_value = df.loc[df['name'] == fighter_name, 'Value'].values[0]
            st.session_state[key] = round(original_value * 1.2)

if reset_button:
    reset_multipliers()

st.markdown("""<br><br>""", unsafe_allow_html=True)
st.markdown("""<br><br>""", unsafe_allow_html=True)

if search_query:
    df_filtered = df[df['name'].str.contains(search_query, case=False)]
else:
    df_filtered = df.head(num_rows_to_display)

multipliers = [1.2, 1.4, 1.6, 2.0, 2.5, 4.0, 6.0]
multiplier_colors = {
    1.2: '#6591B2',  # common
    1.4: '#689F6D',  # uncommon
    1.6: '#BA8057',  # rare
    2.0: '#AE5353',  # epic
    2.5: '#7258A9',  # legendary
    4.0: '#B9985A',  # mystic
    6.0: '#AB6FB0',  # iconic
}


def load_data(search_query, num_rows_to_display):
    df = pd.read_csv("final_values.csv")
    if search_query:
        df_filtered = df[df['name'].str.contains(search_query, case=False)]
    else:
        df_filtered = df.head(num_rows_to_display)
    return df_filtered

def load_search_data(search_query, num_rows_to_display):
    df = pd.read_csv("final_values.csv")
    if search_query:
        df_filtered = df[df['name'].str.contains(search_query, case=False)]
    else :
        df_filtered = df.head(num_rows_to_display)
    return df_filtered

def render_row(row, column_id):
    value_key = f"value_{row['name'].replace(' ', '_')}"
    multiplier_key = f"multiplier_{row['name'].replace(' ', '_')}"

    if value_key not in st.session_state:
        st.session_state[value_key] = round(row['Value'] * 1.2)
    
    if multiplier_key not in st.session_state:
        st.session_state[multiplier_key] = 1.2
    
    col1, col2, *button_cols = st.columns([2, 1] + [0.6 for _ in multipliers])

    with col1:
        st.markdown(f"## {row['name']}")

    with col2:
        color = multiplier_colors[st.session_state[multiplier_key]]
        value_placeholder = st.markdown(f"<h2 style='color: {color};'>{st.session_state[value_key]}</h2>", unsafe_allow_html=True)

    for i, multiplier in enumerate(multipliers):
        with button_cols[i]:
            st.markdown(f"<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
            button_key = f'{multiplier}_{row["name"].replace(" ", "_")}_{column_id}' # Correct key format
            if st.button(f'{multiplier}x', key=button_key):
                new_value = round(row['Value'] * multiplier)
                st.session_state[value_key] = new_value
                st.session_state[multiplier_key] = multiplier
                color = multiplier_colors[multiplier]
                value_placeholder.markdown(f"<h2 style='color: {color};'>{st.session_state[value_key]}</h2>", unsafe_allow_html=True)

    with st.expander("More Data"):
        data_for_chart = row.drop(labels=['name', 'Value'])
        chart_data = pd.DataFrame(data_for_chart)
        chart_data = chart_data.rename(columns={row.name: 'Value'}).reset_index()
        chart_data.columns = ['Category', 'Value']
        st.bar_chart(chart_data.set_index('Category'))

def render_row_compare(row, column_id):
    value_key = f"value_{row['name'].replace(' ', '_')}"
    multiplier_key = f"multiplier_{row['name'].replace(' ', '_')}"

    if value_key not in st.session_state:
        st.session_state[value_key] = round(row['Value'] * 1.2)
    
    if multiplier_key not in st.session_state:
        st.session_state[multiplier_key] = 1.2

    col1, col2 = st.columns([3, 5])

    with col1:
        st.markdown(f"## {row['name']}")

    with col2:
        color = multiplier_colors[st.session_state[multiplier_key]]
        value_placeholder = st.markdown(f"<h2 style='color: {color};'>{st.session_state[value_key]}</h2>", unsafe_allow_html=True)

    button_cols = st.columns(len(multipliers))

    for i, multiplier in enumerate(multipliers):
        with button_cols[i]:  # This selects each column one by one
            st.markdown(f"<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
            button_key = f'{multiplier}_{row["name"].replace(" ", "_")}_{column_id}' # Correct key format
            if st.button(f'{multiplier}x', key=button_key):
                new_value = round(row['Value'] * multiplier)
                st.session_state[value_key] = new_value
                st.session_state[multiplier_key] = multiplier
                color = multiplier_colors[multiplier]
                value_placeholder.markdown(f"<h2 style='color: {color};'>{st.session_state[value_key]}</h2>", unsafe_allow_html=True)

    with st.expander("More Data"):
        data_for_chart = row.drop(labels=['name', 'Value'])
        chart_data = pd.DataFrame(data_for_chart)
        chart_data = chart_data.rename(columns={row.name: 'Value'}).reset_index()
        chart_data.columns = ['Category', 'Value']
        st.bar_chart(chart_data.set_index('Category'))

def load_all_fighter_names():
    df = pd.read_csv("final_values.csv")
    return df['name']

fighter_names = load_all_fighter_names()

if mode == "Rankings" :
    df_filtered = load_data(search_query, num_rows_to_display)
    for _, row in df_filtered.iterrows():
        render_row(row, "none")

elif mode == "Compare Fighters" :

    left_column, right_column = st.columns([2, 2])

    with left_column:
        fighter1 = st.selectbox("Select Fighter 1", options=fighter_names, index=1, format_func=lambda x: x if x else "Type to search...")

        if not fighter1 == "" :
            df_filtered = load_search_data(fighter1, num_rows_to_display)
            for _, row in df_filtered.iterrows():
                render_row_compare(row, "left")

    
    with right_column:
        fighter2 = st.selectbox("Select Fighter 2", options=fighter_names, index=2, format_func=lambda x: x if x else "Type to search...")

        if not fighter2 == "" :
            df_filtered = load_search_data(fighter2, num_rows_to_display)
            for _, row in df_filtered.iterrows():
                render_row_compare(row, "right")



