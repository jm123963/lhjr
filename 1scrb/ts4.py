

df['%Y-%m'] = df['datetime'].astype("str").str[0: 7]  #截取年-月