from tabpy.tabpy_tools.client import Client
import tensorflow as tf
import pandas as pd
import numpy as np
from sklearn import preprocessing
from datetime import timedelta

def prepocessing(data):
    numeric_feat = ['TENURE_IN_DAYS', 'FOB_RACING_TURNOVER', 'FOB_SPORT_TURNOVER', 'PARI_RACING_TURNOVER', 'PARI_RACING_TURNOVER', 'DIVIDENDS_PAID', 'TICKETS']
    categorical_feat = ['AGE_BAND', 'RESIDENTIAL_STATE', 'DAY_OF_WEEK_FULL', 'GENDER_FULL']
    for col in numeric_feat:
        data[col] = data[col].astype('float')
    for feature in categorical_feat:
        label_encoder = preprocessing.LabelEncoder() # intitalizing label encoder object
        label_encoder.fit(list(data[feature].values.astype('str'))) # fit with list of variables in that feature
        data[feature] = label_encoder.transform(list(data[feature].values.astype('str'))) # transforming that feature
    return data
    
def group_data_by_account(data, start_date):

    test_frame_k_mindate = pd.to_datetime(start_date)
    test_frame_k_maxdate = test_frame_k_mindate + timedelta(days=92)
    
    test_frame_k_1 = data.groupby('BET_ACCOUNT_NUM_HASH').agg({
      'DAY_OF_WEEK_FULL': 'max',
      'AGE_BAND': 'max',
      'GENDER_FULL': 'max',
      'TENURE_IN_DAYS': 'max',
      'RESIDENTIAL_STATE': 'max',
      'FOB_RACING_TURNOVER': 'sum',
      'FOB_SPORT_TURNOVER': 'sum',
      'PARI_RACING_TURNOVER': 'sum',
      'PARI_SPORT_TURNOVER': 'sum',
      'DIVIDENDS_PAID': 'sum',
      'GROSS_MARGIN': 'sum',
      'TICKETS': 'sum',
    })

    test_frame_k_2 = data.groupby('BET_ACCOUNT_NUM_HASH').agg({
      'DATE_DIM':  [('first_ses_from_the_period_start' , lambda x: x.min() - test_frame_k_mindate), #first betting session for customer after the period end date for current frame.
                ('last_ses_from_the_period_end', lambda x: test_frame_k_maxdate - x.max()), #Last betting session for customer before the period end date for current frame.
                ('interval_dates' , lambda x: x.max() - x.min()),  #interval calculated as the latest date on which customer visited - oldest date on which they visited.
                ('unqiue_date_num' , lambda x: len(set(x)))] , # Unique number of dates customer visited.
    })

    # Drop the parent level of features. for e.g. drop geoNetwork.networkDomain and keep only 'networkDomain' which stores max value from the group.
    test_frame_k_2.columns = test_frame_k_2.columns.droplevel()
    test_frame_k = pd.merge(test_frame_k_1,
                             test_frame_k_2 ,
                             left_on='BET_ACCOUNT_NUM_HASH',
                             right_on='BET_ACCOUNT_NUM_HASH').reset_index()
    # test_true = pd.merge(test_frame_k,
    #                          test_data_turnover,
    #                          left_on='BET_ACCOUNT_NUM_HASH',
    #                          right_on='BET_ACCOUNT_NUM_HASH')

    return test_frame_k

def prediction_turnover_df(df, start_date):
    
    df= df.loc[df.DATE_DIM >= start_date]
    df = prepocessing(df)
    df = group_data_by_account(df, start_date)
    
    target_columns=['BET_ACCOUNT_NUM_HASH']
    classification_model = tf.keras.models.load_model('E:\\Data Got Talent\\notebooks\\saved_model\\model_classification')
    regression_model = tf.keras.models.load_model('E:\\Data Got Talent\\notebooks\\saved_model\\model_regression')
    
    classification_predictions=classification_model.predict(df.drop(columns=target_columns))
    regression_predictions = regression_model.predict(df.drop(columns=target_columns))
    regression_predictions[regression_predictions<0] = 0
    
    predictions = classification_predictions*regression_predictions
    pred_df = pd.DataFrame({"BET_ACCOUNT_NUM_HASH":df["BET_ACCOUNT_NUM_HASH"].values})
    pred_df["PredictedLogRevenue"] = predictions
    pred_df["PredictedTurnover"] = pred_df["PredictedLogRevenue"].apply(np.expm1)
    
    return pred_df[["BET_ACCOUNT_NUM_HASH", "PredictedTurnover"]].values.tolist()

def prediction_turnover(_arg1, _arg2, _arg3, _arg4, _arg5, _arg6,\
    _arg7, _arg8, _arg9, _arg10, _arg11, _arg12, _arg13, _arg14, _arg15):
    
    df = pd.DataFrame({'BET_ACCOUNT_NUM_HASH':_arg1, 'DATE_DIM':_arg2, 'DAY_OF_WEEK_FULL': _arg3, \
        'AGE_BAND': _arg4, 'GENDER_FULL': _arg5, 'TENURE_IN_DAYS':_arg6, 'RESIDENTIAL_STATE': _arg7, \
            'FOB_RACING_TURNOVER': _arg8, 'FOB_SPORT_TURNOVER': _arg9, 'PARI_RACING_TURNOVER': _arg10, \
                'PARI_SPORT_TURNOVER':_arg11, 'DIVIDENDS_PAID': _arg12, 'GROSS_MARGIN': _arg13, 'TICKETS': _arg14})
    start_date = _arg15
    df= df.loc[df.DATE_DIM >= start_date]
    df = prepocessing(df)
    df = group_data_by_account(df, start_date)
    
    target_columns=['BET_ACCOUNT_NUM_HASH']
    classification_model = tf.keras.models.load_model('E:\\Data Got Talent\\notebooks\\saved_model\\model_classification')
    regression_model = tf.keras.models.load_model('E:\\Data Got Talent\\notebooks\\saved_model\\model_regression')
    
    classification_predictions=classification_model.predict(df.drop(columns=target_columns))
    regression_predictions = regression_model.predict(df.drop(columns=target_columns))
    regression_predictions[regression_predictions<0] = 0
    
    predictions = classification_predictions*regression_predictions
    pred_df = pd.DataFrame({"BET_ACCOUNT_NUM_HASH":df["BET_ACCOUNT_NUM_HASH"].values})
    pred_df["PredictedLogRevenue"] = predictions
    pred_df["PredictedTurnover"] = pred_df["PredictedLogRevenue"].apply(np.expm1)
    
    return pred_df[["BET_ACCOUNT_NUM_HASH", "PredictedTurnover"]].values.tolist()

client = Client('http://localhost:9004/')
client.deploy('Predicted Turnover',
              prediction_turnover,
              'Returns prediction turnover of customer.', override = True)