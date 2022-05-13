import streamlit  
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Mom\'s New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


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
streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    #take the json version of the response and normalize it
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    #output it the screen as a table
    streamlit.dataframe(fruityvice_normalized)

 except URLError as e:
    streamlit.error()

    #adding stop command. dont' run anything past here while we trouble shoot
streamlit.stop()

#check to see if snowflake connector pulls snowflake info
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

#add a second input entry
add_my_fruit = streamlit.text_input('What fruit would you like to add?', 'jackfruit')
streamlit.write('Thanks for adding', add_my_fruit)

#testing add even though it will not work
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
