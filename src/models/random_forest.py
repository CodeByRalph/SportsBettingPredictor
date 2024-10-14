from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV, TimeSeriesSplit
import numpy as np

def train_random_forest(X_train, y_train):
    """
    Trains a RandomForestRegressor model with hyperparameter tuning using RandomizedSearchCV.
    
    Args:
        X_train: Training features.
        y_train: Training target variable.
    
    Returns:
        model: The trained RandomForestRegressor model.
    """
    # Define the hyperparameter search space
    param_dist = {
        'n_estimators': np.arange(100, 1000, 100),  # Number of trees in the forest
        'max_depth': [None] + list(np.arange(10, 50, 10)),  # Maximum depth of the tree
        'min_samples_split': np.arange(2, 10),  # Minimum number of samples required to split
        'min_samples_leaf': np.arange(1, 10),  # Minimum number of samples required in a leaf
        'max_features': ['auto', 'sqrt', 'log2'],  # Number of features to consider at each split
        'bootstrap': [True, False]  # Whether bootstrap samples are used when building trees
    }

    # Initialize the RandomForestRegressor
    rf = RandomForestRegressor(random_state=42)

    # Initialize RandomizedSearchCV with TimeSeriesSplit
    tscv = TimeSeriesSplit(n_splits=5)
    random_search = RandomizedSearchCV(estimator=rf, param_distributions=param_dist, 
                                       n_iter=50, cv=tscv, scoring='neg_mean_squared_error',
                                       random_state=42, n_jobs=-1, verbose=1)

    # Fit the random search model
    random_search.fit(X_train, y_train)

    # Get the best model from random search
    best_rf_model = random_search.best_estimator_
    print(f"Best Hyperparameters: {random_search.best_params_}")
    
    return best_rf_model
