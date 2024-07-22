"""
Script by: Tom Sadeh.
If you have any questions, send an email to dtsj89@gmail.com

This script is part of the Expenditure Decile Calculator Project.
This script sets up a Streamlit web application to calculate the expenditure decile for households based on their monthly expenditures. 
It uses the pandas, numpy, streamlit, and pathlib libraries, and incorporates social media icons via st_social_media_links.

Script Overview

Library Imports:
Imports the necessary libraries for data manipulation (pandas), numerical operations (numpy), web application framework (streamlit), and path management (pathlib).
Imports SocialMediaIcons for displaying social media links in the app.

Page Configuration:
Sets the Streamlit page layout to wide.

Function Definitions:
nefesh_btl(nefesh): Calculates the standardized number of persons in the household based on definitions from the National Security Institute and the Central Bureau of Statistics.
find_nearest(array, value): Finds the closest value in an array to the given value.
load_data(file, p, i=None): Loads data from a CSV file, leveraging Streamlit's caching mechanism for efficiency.

Data Loading:
Sets the path to the data directory and loads the decile limits data from a CSV file.

Custom CSS for RTL Alignment:
Adds custom CSS to ensure the text in the app is right-aligned, suitable for languages that use right-to-left scripts.

Main Title:
Displays the main title of the app in the center of the page.

Expenditure Categories:
Provides a dictionary mapping expenditure category codes to their descriptions in Hebrew.

Tabs Creation:
Creates two tabs: "הסברים" (Explanations) and "מחשבון עשירוני הוצאה" (Expenditure Decile Calculator).
Expenditure Decile Calculator Tab:

Prompts the user to input the number of persons in the household.
Allows the user to select between total expenditure and expenditure by category.
Depending on the selection, prompts the user to input their monthly expenditures.
Calculates the expenditure per person and determines the corresponding decile.
Displays the decile result.

Explanations Tab:
Provides detailed explanations about which expenditures to consider and how the decile is defined.
Social Media Links:

Adds social media links and icons at the bottom of the app for user interaction.
"""

# Importing the required libraries.
import pandas as pd
import numpy as np
import streamlit as st
from pathlib import Path
from st_social_media_links import SocialMediaIcons

# Set the Streamlit page configuration to wide layout.
st.set_page_config(layout="wide")

def nefesh_btl(nefesh):
    """
    Calculates the standardized number of persons in the household.

    Parameters
    ----------
    nefesh : int
        The number of persons the household has.

    Returns
    -------
    Float
        The standardized number of persons in the household, 
        according to National Security Institute and the Central Bureau of Statistics definition.
    """
    l = [1.25, 2, 2.65, 3.2, 3.75, 4.25, 4.75, 5.2]
    if nefesh <= len(l) - 1:
        return l[int(nefesh - 1)]
    else:
        return 5.6 + (nefesh - 9) * 0.4

def find_nearest(array, value):
    """
    Finds the closest value in the array to the given value.

    Parameters
    ----------
    array : numpy array
        The array to be searched.
    value : float or int
        A number to be searched in the array.

    Returns
    -------
    int or float
        Returns the closest value in the array to the value searched, from the bottom.
    """
    array = np.asarray(array)
    if value < array[0]:
        return array[0]
    elif value >= array[-1]:
        return array[-1]
    array = array[array > value]
    idx = (np.abs(array - value)).argmin()
    return array[idx]

@st.cache_data
def load_data(file, p, i=None):
    """
    Loads data from a CSV file.

    Parameters
    ----------
    file : str
        The file name.
    p : Path object
        The path to the file.
    i : str, optional
        The column to read as the index of the dataframe. The default is None.

    Returns
    -------
    DataFrame
        The loaded dataframe.
    """
    return pd.read_csv(p / (file + ".csv"), index_col=i)

# Set the path to the data directory and load the decile limits data.
path = Path(".\data")
data = load_data('limits', path, i='p')

# Creating custom HTML to make the text in the app right-aligned.
st.markdown("""<style> 
                div.row-widget.stSelectbox > div {
                    direction:rtl;
                    text_align:right !important;
                    } </style>""", unsafe_allow_html=True)
st.markdown("""<style>
                li {
                    text-align:right;
                } </style>""", unsafe_allow_html=True)
st.markdown("""<style> 
                div.row-widget.stMultiSelect > div {
                 direction:rtl; 
                 text_align:right !important;
                 } </style>""", unsafe_allow_html=True)                
st.markdown("""<style> 
                input {
                 direction:rtl; 
                 text-align:center !important;
                 } 
                </style>""", unsafe_allow_html=True)
st.markdown("""<style>
                .stTabs > div {
                    direction: rtl;
                    text_align: right;
                    }
                </style>""", unsafe_allow_html=True)
st.markdown("""<style> 
                div.row-widget.stRadio > div {
                 direction:rtl; 
                 text_align:right !important;
                 } 
                </style>""", unsafe_allow_html=True)

# Display the main title of the app.
st.markdown("<h1 style='text-align: center;'>?באיזה עשירון הוצאה אתם</h1>", unsafe_allow_html=True)

# Dictionary of expenditure categories in Hebrew.
c_option_dict = {
                 'c30' : 'מזון ללא ירקות ופירות',
                 'c31' : 'ירקות ופירות',
                 'c32' : 'שכר דירה',
                 'c33' : 'אחזקת הדירה (חשמל, מים, ארנונה, ניקיון וכו\')',
                 'c34' : 'ריהוט וציוד לבית',
                 'c35' : 'הלבשה והנעלה',
                 'c36' : 'בריאות',
                 'c37' : 'חינוך, תרבות ובידור',
                 'c38' : 'תחבורה ותקשורת',
                 'c39' : 'אחר (תכשיטים, סיגריות, תרומות וכו\')'}

# Create tabs for the app: explanations and expenditure decile calculator.
tabs = ['הסברים', 'מחשבון עשירוני הוצאה']
tab2, tab1 = st.tabs(tabs)

# Expenditure decile calculator tab.
with tab1:
    # Prompt the user to input the number of persons in the household.
    st.markdown("<div style='text-align: center;'>הכניסו את מספר הנפשות במשק הבית (כולל ילדים)</div>", unsafe_allow_html=True)
    persons = st.number_input("הכנס את מספר הנפשות במשק הבית (כולל ילדים)", 
                              step=1, 
                              min_value=1, 
                              max_value=20,
                              label_visibility='collapsed')
    
    # Radio button to select total expenditure or expenditure by category.
    radio_options = {'all' : 'הוצאה כוללת',
                     'specific' : 'הוצאה לפי קטגוריה'}
    radio = st.radio('הוצאה כוללת או הוצאה לפי קטגוריה',
                     options = radio_options.keys(),
                     label_visibility='collapsed',
                     format_func=lambda x: '{}'.format(radio_options.get(x)))

    if radio == 'all':
        # If total expenditure is selected, prompt for the total monthly expenditure.
        inp = 'c3'
        text = "הכניסו את כלל ההוצאות החודשיות של משק הבית שלכם " 
        st.markdown(f"<div style='text-align: center;'>{text}</h1>", unsafe_allow_html=True)
        exp_input = st.number_input('placeholder_long' + str(inp), 
                                         min_value=0, 
                                         max_value=100000,
                                         step=100,
                                         label_visibility='collapsed')
        # Calculate expenditure per person and find the corresponding decile.
        exp_pp = exp_input / persons
        decile = data.index[data[inp] == find_nearest(data[inp], exp_pp)]
        text_decile = "עשירון הוצאה כוללת"
        # Display the decile result.
        st.markdown(f"<div style='text-align: center;'>{text_decile}</div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center; font-weight: bold;'>{}</div>".format(int(decile[0] * 10)), unsafe_allow_html=True)
        
    else:
        # If expenditure by category is selected, prompt for the expenditure categories.
        st.markdown("<div style='text-align: center;'>בחרו קטגוריית הוצאה</div>", unsafe_allow_html=True)
        expenditure_type = st.multiselect(label='קטגוריית הוצאה',
                                          options=c_option_dict.keys(),
                                          key='decile_radio',
                                          label_visibility='collapsed',
                                          format_func=lambda x: '{}'.format(c_option_dict.get(x)),
                                          placeholder='בחרו קטגוריית הוצאה אחת או יותר')
        inp = 0    
        if len(expenditure_type) >= 1:
            exp_input = {}
            decile = {}
            for inp in enumerate(expenditure_type):
                # Prompt for the monthly expenditure in each selected category.
                text = "הכניסו את ההוצאות החודשיות של משק הבית שלכם בקטגוריית " + "{}".format(c_option_dict.get(inp[1]))
                st.markdown(f"<div style='text-align: center;'>{text}</h1>", unsafe_allow_html=True)
                exp_input[inp[1]] = st.number_input('placeholder_long' + str(inp[0]), 
                                                 min_value=0, 
                                                 max_value=100000,
                                                 step=10,
                                                 label_visibility='collapsed')
                # Calculate expenditure per person and find the corresponding decile for each category.
                exp_pp = exp_input[inp[1]] / persons
                decile[inp[1]] = data.index[data[inp[1]] == find_nearest(data[inp[1]], exp_pp)]
        
        if isinstance(inp, tuple):
            # Display the decile result for each selected category.
            exp_cols = st.columns(11)
            for loc, exp in zip([5,4,6,3,7,2,8,1,9,0], enumerate(expenditure_type)):
                with exp_cols[loc]:
                    text_decile = "עשירון " + "{}".format(c_option_dict.get(expenditure_type[exp[0]]))
                    st.markdown(f"<div style='text-align: center;'>{text_decile}</div>", unsafe_allow_html=True)
                    st.markdown("<div style='text-align: center; font-weight: bold;'>{}</div>".format(int(decile[exp[1]][0] * 10)), unsafe_allow_html=True)

# Explanations tab.
with tab2:
    # Provide explanations and instructions about the expenditures to consider and how the deciles are defined.
    st.markdown("<div style='text-align: right;'>אילו הוצאות להחשיב?</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: right;'>החשיבו את כל הוצאות משק הבית שלכם, ללא חיסכון, הלוואות או משכנתה.</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: right;'>במקום המשתכנתה הניחו שהייתם משלמים שכר דירה על הדירה בבעלותכם למישהו אחר.</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: right;'>באותו האופן, החשיבו הוצאה שאחר משלם עליכם באופן קבוע כאילו זו הוצאה שלכם, כמו למשל רכב חברה, סיבוס וכו'.</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: right;'></div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: right;'>הגדרת העשירונים:</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: right;'>עשירון בקטגוריית הוצאה מוגדר לפי ההוצאה בקטגורייה הזו של משק הבית, חלקי הנפשות התקניות שבו.</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: right;'></div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: right;'>יאללה, לדרך. בחרו בלשונית 'מחשבון עשירוני הוצאה' כדי להתחיל.</div>", unsafe_allow_html=True)
    
# Add some spacing and display social media links.
st.markdown(" ") 
st.markdown("<div style='text-align: center;'>מצאו אותי כאן</div>", unsafe_allow_html=True)
st.markdown(" ") 

# Define social media links and render the icons.
social_media_links = [
"https://twitter.com/tom_sadeh",
"https://www.facebook.com/DTSJ52"
]

social_media_icons = SocialMediaIcons(social_media_links)
social_media_icons.render()
