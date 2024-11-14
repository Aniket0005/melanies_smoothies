# Import python packages
import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Set up the Snowflake session with error handling
try:
    session = Session.builder.configs(st.secrets["connections.snowflake"]).create()
    
    # Fetch fruit options from Snowflake
    my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).to_pandas()
    
    # Display fruit options in the multiselect input
    ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe['FRUIT_NAME'].tolist(), max_selections=5)
    
    if ingredients_list:
        ingredients_string = ' '.join(ingredients_list)  # Concatenate ingredients with spaces
        st.write("Ingredients selected:", ingredients_string)

        my_insert_stmt = f"""
            INSERT INTO smoothies.public.orders(ingredients, NAME_ON_ORDER)
            VALUES ('{ingredients_string}', '{name_on_order}')
        """

        # Insert the order into the database when button is pressed
        if st.button('Submit Order'):
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")
    
    # Close the session after use
    session.close()

except Exception as e:
    st.error(f"An error occurred: {e}")
