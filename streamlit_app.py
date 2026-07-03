# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests    
import pandas as pd

# Write directly to the app
st.title(f"Example Streamlit App :icecream: {st.__version__}")
st.write(
  """Choose fruits you want in your smoothie  """
)

cnx = st.connection("snowflake")
session = cnx.session()
# session = get_active_session()

name_on_order = st.text_input("Name On Smoothie")
st.write("The name on smoothie will be ", name_on_order)

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
pd_df = my_datafram.to_pandas()
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()

ingredients = st.multiselect('Select upto 5 fruits', my_dataframe)
# if len(ingredients<=5):
#     st.text(ingredients)

if ingredients:
    # st.write(ingredients)
    # st.text(ingredients)
    ingredients_string = ''

    for fruit_choosen in ingredients:
      ingredients_string = ingredients_string + ' ' + fruit_choosen

      search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
      st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

      st.subheader(fruit_choosen + 'Nutrition Information')
      url = "https://my.smoothiefroot.com/api/fruit/watermelon"
      smoothiefroot_response = requests.get(url)  
      st_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = True)
      
    # st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

    # st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")





    
