# Import python packages
import streamlit as st

# Line below is commented because its NOT needed in Streamlit OG
#from snowflake.snowpark.context import get_active_session

from snowflake.snowpark.functions import col

# Lines below are NEEDED for Streamlit OG
cnx = st.connection("snowflake")
session = cnx.session()

# Write title of app directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """)

# Label and Textbox for Smoothie name
name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be", name_on_order)

# Build a dataframe from database table using column FRUIT_NAME
# session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

# ingredients_list is a list variable.  Multi-selct list uses dataframe as source
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:", 
    my_dataframe,
    max_selections=5
)

# below means if ingredients_list is not null: then do everything below this line that is indented. 
if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)

    # defines/initializes variable as a string
    ingredients_string = ''

    # below means for each fruit_chosen in ingredients_list multiselect box: do everything below this line that is indented. 
    for fruit_chosen in ingredients_list:
        # below means  "add fruit to what is already in the variable"
        ingredients_string += fruit_chosen + ' '

    # output the variable
    #st.write(ingredients_string)

    # built SQL Insert statement as a string variable
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')
            """

    # output the variable
    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")
