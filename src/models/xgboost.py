from xgboost import XGBRegressor
from sklearn.model_selection import RandomizedSearchCV, TimeSeriesSplit
import numpy as np


def train_xgboost(X_train, y_train):
    # Define the hyperparameter grid for random search
    param_dist = {
        'n_estimators': np.arange(50, 300, 50),
        'max_depth': np.arange(3, 6),  # Reduce max_depth to avoid overfitting
        'learning_rate': np.linspace(0.01, 0.05, 5),
        'subsample': np.linspace(0.7, 1.0, 3),
        'colsample_bytree': np.linspace(0.6, 0.9, 3),
        'gamma': np.linspace(0, 0.3, 5),
        'min_child_weight': np.arange(1, 6),
        'reg_alpha': np.linspace(0, 1, 3),  # L1 regularization
        'reg_lambda': np.linspace(1, 3, 3),
    }

    # Initialize XGBRegressor
    xgboost_model = XGBRegressor(random_state=42)

    # Define TimeSeriesSplit for sequential data
    tscv = TimeSeriesSplit(n_splits=5)

    # Set up RandomizedSearchCV
    random_search = RandomizedSearchCV(
        estimator=xgboost_model,
        param_distributions=param_dist,
        n_iter=500,           # Number of parameter settings to sample
        scoring='neg_mean_squared_error',  # Performance metric
        cv=tscv,                # Cross-validation folds
        verbose=1,
        n_jobs=-1,           # Use all available CPU cores
        random_state=42
    )

    # Fit the random search model
    random_search.fit(X_train, y_train)
    # Get the best model from random search
    best_model = random_search.best_estimator_

    print("Best Hyperparameters:", random_search.best_params_)
    
    return best_model