import pandas as pd
import plotly.graph_objects as go
import talib


INCREASING_COLOR = '#FF0033'
DECREASING_COLOR = '#00CC66'


def draw(df, period, price_period, volume_period):
    """
    df: DataFrame has colunms: date, open, high, low, close, volume
    """    
    df['price_sma'] = talib.SMA(df.close, price_period)
    df['volume_sma'] = talib.SMA(df.volume, volume_period)
    if len(df) > period:
        df = df.iloc[-period:]

    # build complete timepline from start date to end date
    dt_all = pd.date_range(start=df['date'].iloc[0],end=df['date'].iloc[-1])    
    # retrieve the dates that ARE in the original datset
    dt_obs = [d.strftime("%Y-%m-%d") for d in pd.to_datetime(df['date'])]    
    # define dates with missing values
    dt_breaks = [d for d in dt_all.strftime("%Y-%m-%d").tolist() if not d in dt_obs]

    data = []
    price_candlestick = {
        'type': 'candlestick',
        'x': df.date,
        'open': df.open, 'high': df.high, 'low': df.low, 'close': df.close,
        'yaxis': 'y2',
        'increasing': {'line': {'color': INCREASING_COLOR}},
        'decreasing': {'line': {'color': DECREASING_COLOR}}
    }
    data.append(price_candlestick)
    
    colors = [DECREASING_COLOR]
    for i in range(1, len(df.close)):
        if df.close.iloc[i] >= df.close.iloc[i-1]:
            colors.append(INCREASING_COLOR)
        else:
            colors.append(DECREASING_COLOR)
    volume_bar = {
        'type': 'bar',
        'x': df.date, 'y': df.volume, 
        'yaxis': 'y',
        'marker': {'color': colors}
    }
    data.append(volume_bar)

    price_sma_line = {
        'type': 'scatter',
        'x': df.date, 'y': df.price_sma, 
        'yaxis': 'y2',
        'line': {'width': 1},
        'marker': {'color': '#666'},
        'hoverinfo': 'none'
    }
    data.append(price_sma_line)
    
    volume_sma_line = {
        'type': 'scatter',
        'x': df.date, 'y': df.volume_sma, 
        'yaxis': 'y',
        'line': {'width': 1},
        'marker': {'color': '#666'},
        'hoverinfo': 'none'
    }
    data.append(volume_sma_line)

    fig = {
        'data': data,
        'layout': {
            'plot_bgcolor': 'rgb(250, 250, 250)',
            'yaxis': {'domain': [0, 0.2], 'showticklabels': False},
            'yaxis2': {'domain': [0.2, 1.0]},
            'margin': {'t': 40, 'b': 40, 'l': 40, 'r': 40},
            'height': 600
        }
    }
    
    fig = go.Figure(fig)
    fig.update_xaxes(rangebreaks=[dict(values=dt_breaks)])
    fig.update(layout_xaxis_rangeslider_visible=False)
    fig.update_layout(showlegend=False)
    fig.show()
