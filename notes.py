
def top_emojis(artist_twitter_df):
    '''
    Returns top 10 positive emojis.
    If positive=False, return top 10 negative emojis.
    '''
    def shorthand_sentiment_value(shorthand_text):
        try:
            row_emoji = emoji.demojize(shorthand_text)
            sentiment_val = emoji_sentiment_dict[row_emoji]
        except:
            sentiment_val = np.nan
        return sentiment_val

    emojis_list = []

    for idx, row in artist_twitter_df.iterrows():
        text = row['Description']

        emo_series = pd.DataFrame(emoji.emoji_list(text))
        emojis_list.extend(emo_series['emoji'])

        df = pd.DataFrame.from_dict(Counter(emojis_list), orient='index')
        df.reset_index(inplace=True)
        df.rename(columns={'index':'emoji',0:'count'},
        inplace=True)

        df['shorthand'] = df['emoji'].apply(emoji.demojize)
        # apply FN above
        df['sentiment_val'] = df['shorthand'].apply(shorthand_sentiment_value)

        df = df.dropna()
        df = df.sort_values('count',ascending=False)
        df.reset_index(drop=True, inplace=True)

    return df
