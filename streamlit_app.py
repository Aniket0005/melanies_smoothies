import streamlit as st
from snowflake.snowpark.session import Session  # Assuming you have a Snowflake session object

# Title and description
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie"""
)

# User input
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be: ', name_on_order)

# Get fruits list (assuming you have a session object)
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))

# Select ingredients
ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections=5)

if ingredients_list:

    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    st.write(ingredients_string)

    my_insert_stmt = f"""insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
                        values ('{ingredients_string}','{name_on_order}')"""  # Using f-strings for string formatting

    try:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
    except Exception as e:
        st.error(f"Error inserting order: {e}")  # Basic error handling
