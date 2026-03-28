import streamlit as st

def link_slider(min_key, max_key, sl_key):
    '''
    Function for updating the slider when the numerical fields are manually updated
    '''
    low_val= st.session_state[min_key]
    high_val= st.session_state[max_key]

    # Check to ensure that min remains <= max
    if low_val> high_val:
        low_val= high_val
        st.session_state[min_key]= low_val

    st.session_state[sl_key]= (low_val, high_val)

def link_nums(min_key, max_key, sl_key):
    '''
    Function for updating the numerical fields when the numerical slider is manually updated
    '''
    st.session_state[min_key], st.session_state[max_key]= st.session_state[sl_key]

def num_slider(label, min_val, max_val, sl_key, default= None):
    '''
    A custom slider that allows a user to select a range via both the actual slider and associated numerical fields.
    '''
    # Initialisation
    min_key= f"{sl_key}_min"
    max_key= f"{sl_key}_max"
    if default== None:
        default= (min_val, max_val)
    if sl_key not in st.session_state:
        st.session_state[sl_key]= default
    if min_key not in st.session_state:
        st.session_state[min_key]= default[0]
    if max_key not in st.session_state:
        st.session_state[max_key]= default[1]
    
    st.write(label)

    # Numerical fields
    min_col, max_col= st.columns(2)
    with min_col:
        st.number_input("Lower bound:", min_value= min_val, max_value= max_val, key= min_key,
                        on_change= link_slider, args=(min_key, max_key, sl_key))
    with max_col:
        st.number_input("Upper bound:", min_value= min_val, max_value= max_val, key= max_key,
                        on_change= link_slider, args=(min_key, max_key, sl_key))
    
    # Slider
    vals= st.slider(label= label, min_value= min_val, max_value= max_val,
                    key= sl_key, on_change= link_nums, args=(min_key, max_key, sl_key), label_visibility= "collapsed")
    
    return vals