def get_datatypes(df):

    result = {}

    for column in df.columns:

        result[column] = str(df[column].dtype)

    return result