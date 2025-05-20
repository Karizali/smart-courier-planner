import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import os

class DeliveryTimePredictor:
    def __init__(self, data_path=None):
        self.model = None
        self.preprocessor = None
        self.model_path = './models/delivery_time_model.joblib'
        self.preprocessor_path = './models/delivery_time_preprocessor.joblib'
        
        if os.path.exists(self.model_path) and os.path.exists(self.preprocessor_path):
            self.load_model()
        elif data_path:
            self.train_model(data_path)
    
    def load_model(self):
        """Load trained model and preprocessor from disk"""
        self.model = joblib.load(self.model_path)
        self.preprocessor = joblib.load(self.preprocessor_path)
    
    def save_model(self):
        """Save trained model and preprocessor to disk"""
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.preprocessor, self.preprocessor_path)
    
    def transform_data(self, df, delivery_type):
        weight_ranges = ['1-5 kg', '5-10 kg', '10-20 kg', '20-50 kg', '50+ kg']
        melted_df = pd.melt(
            df,
            id_vars=['Source', 'Destination', 'Special Service'],
            value_vars=weight_ranges,
            var_name='weight_category',
            value_name='delivery_time'
        )
        melted_df.columns = ['source_city', 'destination_city', 'courier_type', 'weight_category', 'delivery_time']
        melted_df['delivery_type'] = delivery_type  # Add the type (city_to_city or within_city)
        return melted_df
    
    def preprocess_data(self, df):
        df['route'] = df['source_city'] + " to " + df['destination_city']
        
        categorical_cols = ['courier_type', 'route', 'weight_category', 'delivery_type']
        for col in categorical_cols:
            df[col] = df[col].astype('category')
        
        return df
    
    def train_model(self, city_to_city_path, within_city_path):
        city_df = pd.read_csv(city_to_city_path)
        within_df = pd.read_csv(within_city_path)

        # Transform and label each
        city_df = self.transform_data(city_df, 'city_to_city')
        within_df = self.transform_data(within_df, 'within_city')

        # Combine both datasets
        df = pd.concat([city_df, within_df], ignore_index=True)
        df = self.preprocess_data(df)

        X = df[['courier_type', 'route', 'weight_category', 'delivery_type']]
        y = df['delivery_time']

        categorical_features = ['courier_type', 'route', 'weight_category', 'delivery_type']
        categorical_transformer = Pipeline(steps=[
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])

        self.preprocessor = ColumnTransformer(
            transformers=[
                ('cat', categorical_transformer, categorical_features)
            ])

        X_processed = self.preprocessor.fit_transform(X)

        self.model = LinearRegression()
        self.model.fit(X_processed, y)

        self.save_model()
    
    def predict_delivery_time(self, input_data):
        if not self.model or not self.preprocessor:
            raise Exception("Model not trained or loaded")

        input_data['route'] = input_data['source_city'] + " to " + input_data['destination_city']

        input_df = pd.DataFrame({
            'courier_type': [input_data['courier_type']],
            'route': [input_data['route']],
            'weight_category': [input_data['weight_category']],
            'delivery_type': [input_data['delivery_type']]  # Must be 'city_to_city' or 'within_city'
        })

        processed_input = self.preprocessor.transform(input_df)
        prediction = self.model.predict(processed_input)

        return max(1, round(prediction[0], 1))







