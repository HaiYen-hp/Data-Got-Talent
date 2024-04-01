import pandas as pd
# Preposcessing Data
def clean_data(df):
# df = pd.read_csv('../dataset/TAB_Betting_Data.csv')

     # print(df.head())

     # print(df.shape)

     # df.BET_ACCOUNT_NUM_HASH.nunique()

     # print(df.isnull().sum())

     list_cate_turnover = ['FOB_RACING_TURNOVER', 'FOB_SPORT_TURNOVER', 'PARI_RACING_TURNOVER', 'PARI_SPORT_TURNOVER']
     for mis_col in list_cate_turnover:
          df.fillna({mis_col:0}, inplace=True)
          
     # print(df.isnull().sum())

     df = df.drop_duplicates()

     df['DATE_DIM']=pd.to_datetime(df['DATE_DIM'])

     dict_nameofday = {'Mon':'Monday', 'Tue':'Tuesday', 'Wed':'Wednesday', 'Thu': 'Thursday', 'Fri':'Friday', 'Sat':'Saturday', 'Sun':'Sunday'}
     dict_gender = {'M':'Male', 'F':'Female', 'U':'Undefined'}

     df['DAY_OF_WEEK_FULL']=df['DAY_OF_WEEK'].apply(lambda x:dict_nameofday[x])
     df['GENDER_FULL']=df['GENDER'].apply(lambda x:dict_gender[x])

     # print(df.shape)
     return df