import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go

#page congiguration
st.set_page_config(
    page_title="Car Price Prediction",
    page_icon="",
    layout="wide"
)
#custom css
st.markdown(
    """
     <style>
     .main{padding: Orem,lrem; }
     h1{color='red';padding-bottom:lrem;}
     </style>

""",unsafe_allow_html=True)
#loading model
@st.cache_resource
def load_model():
    try:
        model=joblib.load("car_prediction_model.pkl")
        return model
    except FileNotFoundError:
        return None
#header
st.title("car price prediction System")
st.markdown('### Get Instant valuation for your used car')

#Load model
model=load_model()
if model is None:
    st.error(" Model file not found")
    st.info(""" Please run the folllwing command first:
            "python car_price_prediction.py"
            THis will train and save the model
            """)
#side bar inputs
st.sidebar.title("car Details")
st.sidebar.subheader("Basic Information")
year=st.sidebar.slider('Manufacturing year',2000,2034,2015)
present_price=st.sidebar.number_input("Current Ex'showrrom price(lakhs)",0.0,50.0,0.1)
kms_driven=st.sidebar.number_input("kilometers_Driven",0,50000,50000,1000)

st.sidebar.subheader("car Specifications")
fuel_type=st.sidebar.selectbox('fuel type',['Petrol','Diesel','CNG'])
seller_type=st.sidebar.selectbox('Seller Type',['Dealer','Individual'])
trnasmission=st.sidebar.selectbox('Transmission',['Manual','Automatic'])
owner=st.sidebar.selectbox('Number of previous owners',[0,1,2,3])

#Calauclate car age
current_year=2024
car_age=current_year-year

#predict button
st.sidebar.markdown(".....")
predict_btn=st.sidebar.button("Get price Estimate",type="primary",use_container_width=True)

#Main content
if predict_btn:
    #Encode Categorical varaibles
    fuel_encoded={'Petrol':0,'Diesel':1,'CNG':2}[fuel_type]
    seller_encoded={'Dealer':0,'Individual':1}[seller_type]
    trnasmission_encoded={'Manual':0,'Automatic':1}[trnasmission]

    #prepare input
    input_data=pd.DataFrame({
        'Year':[year],
        'Present_Price':[present_price],
        'Kms_Driven':[kms_driven],
        'Fuel_Type':[fuel_encoded],
        'Seller_Type':[seller_encoded],
        'Transmission':[trnasmission_encoded],
        'Owner':[owner]


    })
    predicted_price=model.predict(input_data)[0]
    # calcualte the depreciation
    deprecation=present_price-predicted_price
    depreciation_percent=(deprecation/present_price)*100 if present_price>0 else 0

    #Display Results
    st.markdown(".......")
    st.header("price Estimation Results")

    #Main metrics
    col1,col2,col3=st.columns(3)
    with col1:
        st.metric(
            "Estimated Selling pirce",
            f"{predicted_price:2f}Lakhs",
            delta =None

        
        )
    with col2:
        st.metric(
            "current  showroom price",
            f"{present_price:2f} Lakhs",
            delta=None


        )

    with col3:
        st.metric(
            "Total Depreciation",
            f"{deprecation:2f} Lakhs",
            delta=f"-{depreciation_percent:2f}%"



        )
    #gauge chart for price range
    st.markdown("...")
    st.subheader("Price Analaysis")

    col1,col2,=st.columns([2,1])
    with col1:
        lower_estimate=predicted_price=0.9
        upper_estimate=predicted_price=1.1

        st.success(f"""
                **Expected price range:** {lower_estimate:2f}L-{upper_estimate:2f}L
                    This is the typical market range for similar vehicles """)
        st.write("**price Factors:**")
        factors=[]
        if car_age<=2:
            factors.append("Very new car-minimal depreication")
        elif car_age<=5:
            factors.append("Relatively new-good reslale value")
        elif car_age<=10:
            factors.append("Moderate age-average market value")
        else:
            factors.append("older car-higher deprecation")
        
        if kms_driven < 30000:
            factors.append("Low mileage-adds value")
        elif kms_driven < 80000:
            factors.append("Average mileage")
        else:
            factors.append("high mileage-reduces value")
        if trnasmission == "Automatic":
            factors.append("Automatic transmission- premium pricing")
        if fuel_type=="Diesel":
            factors.append("Diesel- prefeered for higher prices")
        elif fuel_type=="Petrol":
            factors.append("Petrol- standard option")
        if seller_type=="Dealer":
            factors.append("ealer-may offer better warranty")
        for factor in factors:
            st.markdown(f"-{factor}")
    with col2:
        max_price=present_price*1.2
        
        fig=go.Figure(go.Indicator(
            mode="gauge+number",
            value=predicted_price,
            title={'text':"Estimated price"},
            number={'prefix':"$",'suffix':"m"},
            gauge={
                'axis':{'range':[None,max_price]},
                'bar':{'color':"red"},
                'steps':[{
                    'range':[0,present_price *0.3],'color':"lightgray"},
                    {'range':[present_price * 0.3,present_price * 0.7], 'color':'lightyellow'},
                    {'range':[present_price * 0.7, max_price], 'color':'lightgreen'}
                ],
                'threshold':{
                    'line':{'color':"blue",'width':4},
                    'thickness':0.75,
                    'value':present_price
                }

            }



        ))

        fig.update_layout(height=300,margin=dict(l=20,r=20,t=50,b=20))
        st.plotly_chart(fig,use_container_width=True)

    #car details summary:
    st.markdown("...")
    st.subheader("your car Details")

    details_col1,details_col2=st.columns(2)

    with details_col1:
        st.write(f"**Manufacturing year:** {year}")
        st.write(f"**car age:** {car_age} years")
        st.write(f"** kilometers Driven:**{kms_driven:,} km")
        st.write(f"** fuel type:**{fuel_type}")

    with details_col2:
        st.write(f"** Transmission:**{trnasmission}")
        st.write(f"**Seller Type:** {seller_type}")
        st.write(f"**Previous Owners:**{owner}")
        st.write(f"** Current Showroom price:** ${present_price}million")
    #Tips for selling:
    st.markdown(".....")
    st.subheader("Tips to get Better price")

else:
    #Initial page
    st.markdown("...")
    st.info("Enter your car details in the side bar and click **Get price Estimate**")

    #show example cars
    st.subheader("Example valuations")

    col1,col2,col3=st.columns(3)

    with col1:
        st.write("** Recent_car**")
        st.write("Year:2020")
        st.write("price:$6.0M")
        st.write("kms:20000")
        st.write("Est: $6.5-7.5M")
        
    with col2:
        st.write("**Mid_Range Car**")
        st.write("year:2015")
        st.write("price:$6.0M")
        st.write("kms:50000")
        st.write("Est:$3.5-4.5M")
    with col3:
        st.write("**    Older Car   **")
        st.write("year:2010")
        st.write("price:$5.0M")
        st.write("kms:200000")
        st.write("Est:$1.5-2.5M")
    st.markdown("....")
    
    #model info
    st.subheader("Model information")
    col1,col2,col3=st.columns(3)
    col1.metric("Algorithm","ML Regression")
    col2.metric("Accuracy","85%")
    col3.metric("Dataset","300+cars")





   


