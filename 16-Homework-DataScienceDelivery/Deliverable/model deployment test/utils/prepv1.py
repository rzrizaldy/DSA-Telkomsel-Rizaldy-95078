import pandas as pd

from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import OneHotEncoder
from pandas.api.types import CategoricalDtype


class FeatureProcessor:
    def __init__(self):
        self.monetary_scaler = RobustScaler()
        #         self.available_money_scaler = RobustScaler()
        #         self.transaction_amount_scaler = RobustScaler()
        #         self.current_balance_scaler = RobustScaler()
        self.acq_country_categories = []
        self.merchant_country_code_categories = []
        self.transaction_type_categories = []
        self.pos_entry_mode_categories = []
        self.pos_condition_code_categories = []
        self.merchant_category_code_categories = []

    def fit(self, data):
        self.monetary_scaler.fit(data[['creditLimit', 'availableMoney', 'transactionAmount', 'currentBalance']])
        #         self.available_money_scaler.fit(data['availableMoney'])
        #         self.transaction_amount_scaler.fit(data['transactionAmount'])
        #         self.current_balance_scaler.fit(data['currentBalance'])
        self.acq_country_categories = CategoricalDtype(categories=data['acqCountry'].dropna().unique().tolist(),
                                                       ordered=True)
        self.merchant_country_code_categories = CategoricalDtype(categories=data['merchantCountryCode'].
                                                                 dropna().unique().tolist(), ordered=True)
        self.transaction_type_categories = CategoricalDtype(categories=data['transactionType'].
                                                            dropna().unique().tolist(), ordered=True)
        self.pos_entry_mode_categories = CategoricalDtype(categories=data['posEntryMode'].
                                                          dropna().astype('str').unique().tolist(), ordered=True)
        self.pos_condition_code_categories = CategoricalDtype(categories=data['posConditionCode'].
                                                              dropna().astype('str').unique().tolist(), ordered=True)
        self.merchant_category_code_categories = CategoricalDtype(categories=data['merchantCategoryCode'].
                                                                  dropna().unique().tolist(), ordered=True)

    def transform(self, data, pred=True):
        # drop missing data
        column_dropped = ['merchantCity', 'merchantState', 'merchantZip', 'echoBuffer',
                          'posOnPremises', 'recurringAuthInd']
        new_data = data.drop(columns=column_dropped)
        # dates features
        new_data['transactionDateTime'] = pd.to_datetime(new_data['transactionDateTime'], format="%Y-%m-%dT%H:%M:%S")
        new_data['currentExpDate'] = pd.to_datetime(new_data['currentExpDate'], format="%m/%Y")
        new_data['accountOpenDate'] = pd.to_datetime(new_data['accountOpenDate'], format="%Y-%m-%d")
        new_data['dateOfLastAddressChange'] = pd.to_datetime(new_data['dateOfLastAddressChange'], format="%Y-%m-%d")
        new_data['transactionMonth'] = new_data['transactionDateTime'].dt.strftime("%m").astype('int')
        new_data['transactionDayssOfWeek'] = new_data['transactionDateTime'].dt.strftime("%w").astype('int')
        new_data['transactionHour'] = new_data['transactionDateTime'].dt.strftime("%H").astype('int')
        new_data['expiryFromTransactionDays'] = (new_data['currentExpDate'] - new_data['transactionDateTime']).dt.days
        new_data['expiryFromOpenDays'] = (new_data['currentExpDate'] - new_data['accountOpenDate']).dt.days
        new_data['transactionFromOpenDays'] = (new_data['transactionDateTime'] - new_data['accountOpenDate']).dt.days
        new_data['transactionFromAddressChangeDays'] = (new_data['transactionDateTime']
                                                        - new_data['dateOfLastAddressChange']).dt.days
        new_data['addressChangeFromOpenDays'] = (new_data['dateOfLastAddressChange']
                                                 - new_data['accountOpenDate']).dt.days
        # monetary features
        new_data[['creditLimit', 'availableMoney', 'transactionAmount', 'currentBalance']] = \
            self.monetary_scaler.transform(new_data[['creditLimit', 'availableMoney',
                                                     'transactionAmount', 'currentBalance']])
        # new_data['availableMoney'] = self.available_money_scaler.transform(new_data['availableMonet'])
        # new_data['transactionAmount'] = self.transaction_amount_scaler.transform(new_data['transactionAmount'])
        # new_data['currentBalance'] = self.current_balance_scaler.transform(new_data['currentBalance'])
        # card features
        new_data['matchedCVV'] = new_data['cardCVV'] == new_data['enteredCVV']
        # country features
        new_data['countryMatch'] = data['acqCountry'] == data['merchantCountryCode']
        new_data['acqCountry'] = new_data['acqCountry'].astype(self.acq_country_categories)
        new_data = pd.concat([new_data,
                              pd.get_dummies(new_data['acqCountry'],
                                             prefix='acqCountry', dummy_na=True)], axis=1).drop(['acqCountry'], axis=1)
        new_data['merchantCountryCode'] = new_data['merchantCountryCode'].\
            astype(self.merchant_country_code_categories)
        new_data = pd.concat([new_data,
                              pd.get_dummies(new_data['merchantCountryCode'],
                                             prefix='merchantCountryCode', dummy_na=True)], axis=1).\
            drop(['merchantCountryCode'], axis=1)
        # transaction type features
        new_data['transactionType'] = new_data['transactionType'].astype(self.transaction_type_categories)
        new_data = pd.concat([new_data,
                              pd.get_dummies(new_data['transactionType'],
                                             prefix='transactionType',
                                             dummy_na=True)], axis=1).drop(['transactionType'], axis=1)
        # pos code features
        new_data['posEntryMode'] = new_data['posEntryMode'].astype('str').\
            astype(self.pos_entry_mode_categories)
        new_data = pd.concat([new_data,
                              pd.get_dummies(new_data['posEntryMode'],
                                             prefix='posEntryMode',
                                             dummy_na=True)], axis=1).drop(['posEntryMode'], axis=1)
        new_data['posConditionCode'] = new_data['posConditionCode'].astype('str').\
            astype(self.pos_condition_code_categories)
        new_data = pd.concat([new_data,
                              pd.get_dummies(new_data['posConditionCode'],
                                             prefix='posConditionCode',
                                             dummy_na=True)], axis=1).drop(['posConditionCode'], axis=1)
        # merchant features
        new_data['merchantCategoryCode'] = new_data['merchantCategoryCode'].\
            astype(self.merchant_category_code_categories)
        new_data = pd.concat([new_data,
                              pd.get_dummies(new_data['merchantCategoryCode'],
                                             prefix='merchantCategoryCode',
                                             dummy_na=True)], axis=1).drop(['merchantCategoryCode'], axis=1)

        # label encode
        if not(pred):
            new_data['isFraud'] = new_data['isFraud'] + 0

        # drop unused variable
        new_data = new_data.drop(columns=['accountNumber', 'customerId', 'transactionDateTime', 'currentExpDate',
                                          'accountOpenDate', 'dateOfLastAddressChange', 'merchantName'])

        # return processed data
        if not(pred):
            return (new_data, new_data.drop(columns=['isFraud']), new_data['isFraud'])
        else:
            return new_data

