import pandas as pd


def column_pct(df, periods):
    df = df.copy()
    df_pct = (df.pct_change(periods=periods) * 100).round(1)
    for col in df.columns:
        if df[col].dtype == 'float':
            df[col] = df[col].map('{:,.2f}'.format) + " (" + df_pct[col].astype(str) + "%)"
        else:
            df[col] = df[col].map('{:,.0f}'.format) + " (" + df_pct[col].astype(str) + "%)"
    return df