# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Street Feast - Online Order App")
st.write("Please enter your name to place order online ")

title = st.text_input("Name")
if title:
    st.write("Welcome ", title," !")



cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("foodtruck.business.menu").select(col('Item'),col('ItemId'),col('price'))


pd_df = my_dataframe.to_pandas()                                                                      

st.write("Please select your food from below menu list")
order_list =st.multiselect('Maximum of 5 items are allowed per order', my_dataframe, max_selections = 5)
but = st.button('Submit')


if but:
    if order_list:

        items = ''
        totalPrice =0
        
        orderDetails = ""
        orderTitle = "**You Order details**"
        id=0
        for order in order_list:
            items +=order +' ' 
            matched = pd_df.loc[pd_df['ITEM'] == order, 'PRICE'].iloc[0]
            id = pd_df.loc[pd_df['ITEM'] == order, 'ITEMID'].iloc[0]
            totalPrice+=matched
            orderDetails +="\n"+order +" price = "+str(matched)

            
        
        if(totalPrice > 0):
            
            total ="**Total Amount = "+str(totalPrice) +"**"
            my_insert_stmt = """ insert into foodtruck.business.orders(Items,CustomerName,TotalPrice)
            values ('""" + items + """', '"""+ title +"""', '"""+ str(totalPrice) +"""')"""

            

            if items:
                session.sql(my_insert_stmt).collect()
                st.success('Your Order is placed. Thank you!', icon="✅")
                
                #st.markdown(orderDetails)
                #st.write(orderDetails)
                st.write(orderTitle)
                st.text(orderDetails)
                st.write(total)


            
