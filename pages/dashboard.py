import streamlit as st
from pycoingecko import CoinGeckoAPI
import plotly.express as px
import pandas as pd

st.set_page_config(page_title='Crypto Dashboard', page_icon=':bar_chart:') 

@st.cache_data
def get_market_data():
    cg = CoinGeckoAPI()
    return cg.get_global()

market_data = get_market_data()

def get_history_data(id, date):
    cg = CoinGeckoAPI()
    return cg.get_coin_history_by_id(id=id, date=date)

history_data = get_history_data("bitcoin", "10-7-2023")
    

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
# df = pd.DataFrame(history_data["btc"])
# fig = px.line(df, x="date", y="lifeExp", color='country')
# fig.show()

st.write(history_data["market_data"]["total_volume"]["btc"])
# st.line_chart(chart_data)

# Defi Market Capitalization:
# Display the market capitalization of top DeFi tokens for both 7 days and 30 days.
# Present the growth rates and percentage change in market caps between the two time frames.  
# Use Streamlit's table or plot components to showcase the comparative data.

def plot_defi_marketcap(cg, top_n=10):

  # Get current market cap
  current = cg.get_coins_markets(vs_currency='usd', category='decentralized_finance_defi', per_page=50)
  current_df = pd.DataFrame([x['market_cap'] for x in current], columns=['market_cap'])

  # Get previous market cap
  prev = cg.get_coins_markets(vs_currency='usd', category='decentralized_finance_defi', order='market_cap_desc', per_page=50, page=1, sparkline=False, price_change_percentage='24h')
  prev_df = pd.DataFrame([x['market_cap'] for x in prev], columns=['prev_market_cap'])

  # Join and calculate % change
  df = current_df.join(prev_df) 
  df['pct_change'] = (df['market_cap'] - df['prev_market_cap']) / df['prev_market_cap'] * 100

  # Filter top tokens
  top_tokens = df.nlargest(top_n, 'market_cap')   

  # Create chart
  fig = px.bar(top_tokens, x=top_tokens.index, y='market_cap', 
               color='pct_change', color_continuous_scale='RdYlGn',
              title=f'Top {top_n} DeFi Tokens by Market Cap')

  return fig

# Example usage:

cg = CoinGeckoAPI() 
chart = plot_defi_marketcap(cg, top_n=10)
st.plotly_chart(chart)

# Defi Dominance:
# Plot a line chart using Streamlit to visualize the ratio of DeFi market capitalization to total market capitalization.
# Show the trends for both 7 days and 30 days on the same chart.
# Utilize Streamlit's labeling or annotation capabilities to indicate any significant changes in DeFi dominance.

# Trading Volume Comparison:  
# Provide a bar chart or line chart using Streamlit to compare the trading volumes of different cryptocurrencies.
# Display the data for both 7 days and 30 days side by side.
# Highlight any significant differences or patterns between the two time frames.

# Defi Adoption Tracking:
# Present the total value locked (TVL) in DeFi protocols for both 7 days and 30 days.  
# Use a line chart with Streamlit to show the growth by different chains separately for each time frame.
# Include Streamlit's labels or annotations to highlight notable changes or trends.

# Top Defi Coin:
# Display the top decentralized finance coin by market capitalization for both 7 days and 30 days.
# Show the market dominance percentage for each time frame.
# Utilize Streamlit's table or plot components to compare the performance of different top DeFi coins.

st.header('Top Defi Coins') 
df = pd.DataFrame(market_data['defi_tokens'])
st.table(df)