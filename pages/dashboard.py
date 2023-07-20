import streamlit as st
from pycoingecko import CoinGeckoAPI
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


st.set_page_config(page_title='Crypto Dashboard', page_icon=':bar_chart:') 

from datetime import datetime, timedelta

def generate_date(num_days):    
    current_date = datetime.now().date()
    time_durations = current_date - timedelta(days=num_days)
    formatted_date = time_durations.strftime('%d-%m-%Y')
    return formatted_date

@st.cache_data
def get_market_data():
    cg = CoinGeckoAPI()
    return cg.get_global()

market_data = get_market_data()

@st.cache_data
def get_defi_data():
    cg = CoinGeckoAPI()
    defi_data = cg.get_global_decentralized_finance_defi()
    return defi_data

@st.cache_data
def fetch_data (id, date):
    cg = CoinGeckoAPI()
    return cg.get_coin_history_by_id(id=id, date=date)

st.title('Crypto Market Dashboard')

# Market overview section
# Display total market capitalization, trading volume, and DeFi dominance for both 7 days and 30 days.  
# Show the percentage change in these metrics between the two time frames.
st.header('Market Overview')
col1, col2 = st.columns(2)
col1.metric('Total Market Cap', f'{market_data["total_market_cap"]["btc"]:,.0f} BTC')
col2.metric('Trading Volume', f'{market_data["total_volume"]["btc"]:,.0f} BTC')

# Trend analysis charts
# Include separate line charts for market capitalization and trading volume.
# Plot the data for both 7 days and 30 days on the same chart for easy comparison.
# Utilize Streamlit's interactive features to allow users to zoom in and out on the charts.

st.header('Trend Analysis')

day_7 = generate_date(7)
day_30 = generate_date(30)

date = [day_7, day_30]
# st.write(day_7)

hist_seven = fetch_data("bitcoin", day_7)
hist_thirty = fetch_data("bitcoin", day_30)

marketcap_data = {
    # 'date' : [day_7, day_30],
    'market_cap' : [hist_seven["market_data"]["market_cap"]["btc"], hist_thirty["market_data"]["market_cap"]["btc"]],
}  

volume_data = {
    # 'date' : [day_7, day_30],
    'trading_volume' : [hist_seven["market_data"]["total_volume"]["btc"], hist_thirty["market_data"]["total_volume"]["btc"]]
}
market_df = pd.DataFrame(marketcap_data, index = date)
volume_df = pd.DataFrame(volume_data, index = date)

market_col, volume_col = st.columns([1,1])
# st.subheader('Market Capitalisation in Price (BTC) for a week and a month ago')
market_col.area_chart(market_df)
volume_col.area_chart(volume_df)
 
# Trading Volume Comparison:  
# Provide a bar chart or line chart using Streamlit to compare the trading volumes of different cryptocurrencies.
# Display the data for both 7 days and 30 days side by side.
# Highlight any significant differences or patterns between the two time frames.

st.header("Trading Volume")
@st.cache_data
def trading_volume(id):
    cg = CoinGeckoAPI()
    data = cg.get_global()
    volume_data = data["total_volume"]
    
    return volume_data[id]

index = ["btc",
      "eth",
      "ltc",
      "bch",
      "bnb",
      "eos",
      "xrp",
      "xlm",
      "link",
      "dot",
      "yfi",
      "usd",
      "aed",
      "ars",
      "aud",
      "bdt",
      "bhd",
      "bmd"]

value = []
for i in index:
    val = trading_volume(i)
    value.append(val)

# for v in value:
#     value = value/100000

df_volume = pd.DataFrame(value, index=index, columns=["Trading Volume"])


st.bar_chart(df_volume)

# Defi Adoption Tracking:
# Present the total value locked (TVL) in DeFi protocols for both 7 days and 30 days.  
# Use a line chart with Streamlit to show the growth by different chains separately for each time frame.
# Include Streamlit's labels or annotations to highlight notable changes or trends.

# Top Defi Coin:
# Display the top decentralized finance coin by market capitalization for both 7 days and 30 days.
# Show the market dominance percentage for each time frame.
# Utilize Streamlit's table or plot components to compare the performance of different top DeFi coins.


st.header('DeFi Market Overview')
# data_defi = cg.get_global_decentralized_finance_defi()

defi_data = get_defi_data()

defi_market_cap = float(defi_data["defi_market_cap"])
col_DeFi_Market_cap, col_DeFi_dominance = st.columns(2)

col_DeFi_Market_cap.metric('DeFi Market Cap', f'{defi_market_cap:,.0f} USD')
col_DeFi_dominance.metric('Decentralized Finance Dominance', defi_data["defi_dominance"])

col_TopDeFi,col_Top_Dominance = st.columns(2)
col_TopDeFi.metric('Top Decentralized Finance Coin', f'{defi_data["top_coin_name"]}')
col_Top_Dominance.metric('Top Coin DeFi Dominance', f'{defi_data["top_coin_defi_dominance"]:,.0f} %')
    