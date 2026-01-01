from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import numpy as np

class TitanicFeatureEngineer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        X_ = X.copy()
        # Smarter Age Imputation: Median by Sex and Pclass
        self.age_medians_ = X_.groupby(['Sex', 'Pclass'])['Age'].median().to_dict()
        self.global_age_median_ = X_['Age'].median()
        
        self.fare_median_ = X_['Fare'].median()
        
        # Learn fare bins
        try:
            _, self.fare_bins_ = pd.qcut(X_['Fare'], 4, retbins=True, duplicates='drop')
        except ValueError:
            self.fare_bins_ = np.array([0, 7.91, 14.45, 31.0, 512.33])

        return self

    def transform(self, X):
        X = X.copy()

        # 1. Age Imputation (Grouped Median)
        if 'Age' in X.columns:
            # Apply grouped median
            X['Age'] = X.apply(
                lambda row: row['Age'] if pd.notnull(row['Age']) 
                else self.age_medians_.get((row['Sex'], row['Pclass']), self.global_age_median_),
                axis=1
            )
        else:
            X['Age'] = self.global_age_median_

        # 2. Fare Handling
        if 'Fare' not in X.columns:
             X['Fare'] = self.fare_median_
        X['Fare'] = X['Fare'].fillna(self.fare_median_)
        
        if len(self.fare_bins_) > 0:
            labels = range(1, len(self.fare_bins_))
            X['FareBand'] = pd.cut(X['Fare'], bins=self.fare_bins_, labels=labels, include_lowest=True)
            X['FareBand'] = X['FareBand'].cat.add_categories([0]).fillna(0).astype(int)
        else:
            X['FareBand'] = 0

        # 3. Child logic
        X['IsChild'] = (X['Age'] <= 16).astype(int)
        
        # Ensure Sex is present for downstream one-hot encoding
        if 'Sex' not in X.columns: X['Sex'] = 'male'
        
        return X
