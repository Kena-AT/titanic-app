from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import numpy as np

class TitanicFeatureEngineer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        X_ = X.copy()
        self.age_median_ = X_['Age'].median()
        self.fare_median_ = X_['Fare'].median()
        
        # Learn fare bins
        try:
            _, self.fare_bins_ = pd.qcut(X_['Fare'], 4, retbins=True, duplicates='drop')
        except ValueError:
            self.fare_bins_ = np.array([0, 7.91, 14.45, 31.0, 512.33])

        return self

    def transform(self, X):
        X = X.copy()

        # 1. Age Imputation (Simple Global Median)
        if 'Age' in X.columns:
            X['Age'] = X['Age'].fillna(self.age_median_)
        else:
            X['Age'] = self.age_median_

        # 2. Fare Handling
        if 'Fare' not in X.columns:
             X['Fare'] = np.nan
        X['Fare'] = X['Fare'].fillna(self.fare_median_)
        
        if len(self.fare_bins_) > 0:
            labels = range(1, len(self.fare_bins_))
            X['FareBand'] = pd.cut(X['Fare'], bins=self.fare_bins_, labels=labels, include_lowest=True)
            X['FareBand'] = X['FareBand'].cat.add_categories([0]).fillna(0).astype(int)
        else:
            X['FareBand'] = 0

        # 3. Child logic (Derived from Age/Sex)
        if 'Sex' not in X.columns: X['Sex'] = 'male'
        X['IsChild'] = (X['Age'] <= 16).astype(int)
        X['MaleChild'] = ((X['Sex'] == 'male') & (X['Age'] <= 16)).astype(int)
        
        # We process ONLY Pclass, Sex, Age, Fare, and the derived FareBand/IsChild/MaleChild
        # The ColumnTransformer will select what it needs.
        
        return X
