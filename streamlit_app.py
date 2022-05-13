import streamlit  

streamlit.title('My Mom\'s New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas

#have pandas read CSV file from S3 bucket. We use a pandas called function called read_csv to pull data into a dataframe 
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

#After pulling the data into a pandas darafram called my_fruit_list, we will ask the streamlit library to display it on the page
streamlit.dataframe(my_fruit_list)

#add a user interactive widget called multi-select that will allow users to pick the fruits they want in their smoothies
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
#ask app to put the list of selected fruits into a variable fruit select (as seen in previous line) then we'll ask our app to use the fruits in our fruits_select list
#to pull rows from the full data set. 
fruits_to_show = my_fruit_list.loc[fruits_selected]

#display the table on the page
streamlit.dataframe(fruits_to_show)

#new section to display fruitvice api response
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
streamlit.text(fruityvice_response)
