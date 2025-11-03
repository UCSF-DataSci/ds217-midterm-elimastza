# TODO: Add shebang line: #!/usr/bin/env python3
# Assignment 5, Question 3: Data Utilities Library
# Core reusable functions for data loading, cleaning, and transformation.
#
# These utilities will be imported and used in Q4-Q7 notebooks.

#!/usr/bin/env python3
from hashlib import new
from IPython.display import display
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def load_data(filepath: str) -> pd.DataFrame:
    """
    Load CSV file into DataFrame.

    Args:
        filepath: Path to CSV file

    Returns:
        pd.DataFrame: Loaded data

    Example:
        >>> df = load_data('data/clinical_trial_raw.csv')
        >>> df.shape
        (10000, 18)
    """
    df = pd.read_csv('data/clinical_trial_raw.csv')
    display(f"Data shape: {df.shape}")
    return df


def clean_data(df: pd.DataFrame, remove_duplicates: bool = True,
               sentinel_value: float = -999) -> pd.DataFrame:
    """
    Basic data cleaning: remove duplicates and replace sentinel values with NaN.

    Args:
        df: Input DataFrame
        remove_duplicates: Whether to drop duplicate rows
        sentinel_value: Value to replace with NaN (e.g., -999, -1)

    Returns:
        pd.DataFrame: Cleaned data

    Example:
        >>> df_clean = clean_data(df, sentinel_value=-999)
    """
    df = df.copy()
    if remove_duplicates:
        df = df.drop_duplicates()
    df = df.replace(sentinel_value, np.nan)
    return df



def detect_missing(df: pd.DataFrame) -> pd.Series:
    """
    Return count of missing values per column.

    Args:
        df: Input DataFrame

    Returns:
        pd.Series: Count of missing values for each column

    Example:
        >>> missing = detect_missing(df)
        >>> missing['age']
        15
    """
    return df.isnull().sum()


def fill_missing(df: pd.DataFrame, column: str, strategy: str = 'mean') -> pd.DataFrame:
    """
    Fill missing values in a column using specified strategy.

    Args:
        df: Input DataFrame
        column: Column name to fill
        strategy: Fill strategy - 'mean', 'median', or 'ffill'

    Returns:
        pd.DataFrame: DataFrame with filled values

    Example:
        >>> df_filled = fill_missing(df, 'age', strategy='median')
    """
    df_ffill = df.ffill()
    print(df_ffill)  # Missing values replaced with previous value
    return df_ffill

filters = [
        {'column': 'age', 'condition': 'greater_than', 'value': 65},
        {'column': 'bmi', 'condition': 'less_than', 'value': 18.5},
        {'column': 'sex', 'condition': 'in_list', 'value': ['Female', 'Male']},
        {'column': 'systolic_bp', 'condition': 'greater than', 'value': 140}, 
        {'column': 'diastolic_bp', 'condition': 'in_range', 'value': [80, 90]},
        {'column': 'cholesterol_total', 'condition': 'in_range', 'value': [200, 240]},
        {'column': 'cholesterol_hdl', 'condition': 'greater_than', 'value': 40},
        {'column': 'cholesterol_ldl', 'condition': 'less_than', 'value': 160},
        {'column': 'glucose_fasting', 'condition': 'less_than', 'value': 100},
        {'column': 'site', 'condition': 'in_list', 'value': ['Site A', 'Site B', 'Site C']},
        {'column': 'intervention_group', 'condition': 'in_list', 'value': ['Control', 'Treatment']},
        {'column': 'follow_up_months', 'condition': 'greater_than', 'value': 12},
        {'column': 'adverse_events', 'condition': 'equals', 'value': 0},
        {'column': 'outcome_cvd', 'condition': 'equals', 'value': 0},
        {'column': 'adherence_pct', 'condition': 'greater_than', 'value': 80},
        {'column': 'dropout', 'condition': 'equals', 'value': 0}
                 
    ]
    

def filter_data(df: pd.DataFrame, filters: list) -> pd.DataFrame:
    """
    Apply a list of filters to DataFrame in sequence.

    Args:
        df: Input DataFrame
        filters: List of filter dictionaries, each with keys:
                'column', 'condition', 'value'
                Conditions: 'equals', 'greater_than', 'less_than', 'in_range', 'in_list'

    Returns:
        pd.DataFrame: Filtered data

    Examples:
        >>> # Single filter
        >>> filters = [{'column': 'site', 'condition': 'equals', 'value': 'Site A'}]
        >>> df_filtered = filter_data(df, filters)
        >>>
        >>> # Multiple filters applied in order
        >>> filters = [
        ...     {'column': 'age', 'condition': 'greater_than', 'value': 18},
        ...     {'column': 'age', 'condition': 'less_than', 'value': 65},
        ...     {'column': 'site', 'condition': 'in_list', 'value': ['Site A', 'Site B']}
        ... ]
        >>> df_filtered = filter_data(df, filters)
        >>>
        >>> # Range filter example
        >>> filters = [{'column': 'age', 'condition': 'in_range', 'value': [18, 65]}]
        >>> df_filtered = filter_data(df, filters)
    """
    for f in filters:
        column = f['column']
        condition = f['condition']
        value = f['value']

        if condition == 'equals':
            df = df[df[column] == value]
        elif condition == 'greater_than':
            df = df[df[column] > value]
        elif condition == 'less_than':
            df = df[df[column] < value]
        elif condition == 'in_range':
            df = df[(df[column] >= value[0]) & (df[column] <= value[1])]
        elif condition == 'in_list':
            df = df[df[column].isin(value)]
    return df


type_map = {
        'patient_id': 'string',
        'age': 'numeric',
        'bmi': 'numeric',
        'sex': 'category',
        'enrollment_date': 'datetime',
        'site': 'category',
        'systolic_bp': 'numeric',
        'diastolic_bp': 'numeric',
        'cholesterol_total': 'numeric',
        'cholesterol_hdl': 'numeric',
        'cholesterol_ldl': 'numeric',
        'glucose_fasting': 'numeric',
        'site': 'category',
        'intervention_group': 'category',
        'follow_up_months': 'numeric',
        'adverse_events': 'numeric',
        'outcome_cvd': 'string',
        'adherence_pct': 'numeric',
        'dropout': 'category'
    }

def transform_types(df: pd.DataFrame, type_map: dict) -> pd.DataFrame:
    """
    Convert column data types based on mapping.

    Args:
        df: Input DataFrame
        type_map: Dict mapping column names to target types
                  Supported types: 'datetime', 'numeric', 'category', 'string'

    Returns:
        pd.DataFrame: DataFrame with converted types

    Example:
        >>> type_map = {
        ...     'enrollment_date': 'datetime',
        ...     'age': 'numeric',
        ...     'site': 'category'
        ... }
        >>> df_typed = transform_types(df, type_map)
    """
    for column in type_map:
        if type_map[column] == 'numeric':
            df[column] = pd.to_numeric(df[column], errors='coerce')
        if type_map[column] == 'datetime':
            df[column] = pd.to_datetime(df[column], errors='coerce')
        if type_map[column] == 'category':
            df[column] = df[column].astype('category')
        if type_map[column] == 'string':
            df[column] = df[column].astype('string')

    return df


def create_bins(df: pd.DataFrame, column: str, bins: list,
                labels: list, new_column: str = None) -> pd.DataFrame:
    """
    Create categorical bins from continuous data using pd.cut().

    Args:
        df: Input DataFrame
        column: Column to bin
        bins: List of bin edges
        labels: List of bin labels
        new_column: Name for new binned column (default: '{column}_binned')

    Returns:
        pd.DataFrame: DataFrame with new binned column

    Example:
        >>> df_binned = create_bins(
        ...     df,
        ...     column='age',
        ...     bins=[0, 18, 35, 50, 65, 100],
        ...     labels=['<18', '18-34', '35-49', '50-64', '65+']
        ... )
    """
    df = df.copy()
    if new_column is None:
        new_column = f"{column}_binned"
    df[new_column] = pd.cut(df[column], bins=bins, labels=labels)
    return df
    

def summarize_by_group(df: pd.DataFrame, group_col: str,
                       agg_dict: dict = None) -> pd.DataFrame:
    """
    Group data and apply aggregations.

    Args:
        df: Input DataFrame
        group_col: Column to group by
        agg_dict: Dict of {column: aggregation_function(s)}
                  If None, uses .describe() on numeric columns

    Returns:
        pd.DataFrame: Grouped and aggregated data

    Examples:
        >>> # Simple summary
        >>> summary = summarize_by_group(df, 'site')
        >>>
        >>> # Custom aggregations
        >>> summary = summarize_by_group(
        ...     df,
        ...     'site',
        ...     {'age': ['mean', 'std'], 'bmi': 'mean'}
        ... )
    """
    if agg_dict is None:
        # Default: describe numeric columns by group
        return df.groupby(group_col).describe()
    else:
        return df.groupby(group_col).agg(agg_dict)



if __name__ == '__main__':
    # Optional: Test your utilities here
    print("Data utilities loaded successfully!")
    print("Available functions:")
    
    # Load data first
    df = load_data('data/clinical_trial_raw.csv')
    
    print(clean_data(df))
    print(detect_missing(df))
    print(fill_missing(df, 'age', strategy='ffill'))
    print(fill_missing(df, 'sex', strategy='ffill'))
    print(fill_missing(df, 'bmi', strategy='ffill'))
    print(fill_missing(df, 'enrollment_date', strategy='ffill'))
    print(fill_missing(df, 'systolic_bp', strategy='ffill'))
    print(fill_missing(df, 'diastolic_bp', strategy='ffill'))
    print(fill_missing(df, 'cholesterol_total', strategy='ffill'))
    print(fill_missing(df, 'cholesterol_hdl', strategy='ffill'))
    print(fill_missing(df, 'cholesterol_ldl', strategy='ffill'))
    print(fill_missing(df, 'glucose_fasting', strategy='ffill'))
    print(fill_missing(df, 'follow_up_months', strategy='ffill'))
    print(fill_missing(df, 'adverse_events', strategy='ffill'))
    print(fill_missing(df, 'outcome_cvd', strategy='ffill'))
    print(fill_missing(df, 'adherence_pct', strategy='ffill'))
    print(fill_missing(df, 'dropout', strategy='ffill'))
    print(fill_missing(df, 'site', strategy='ffill'))
    print(fill_missing(df, 'intervention_group', strategy='ffill'))
    
    # Test filter_data with proper filter list
    test_filters = [{'column': 'age', 'condition': 'greater_than', 'value': 75}]
    print(filter_data(df, test_filters))
    
    print(transform_types(df, type_map))
    
    # Apply binning
    df = create_bins(df, 'age', bins=[0, 18, 35, 50, 65, 100], labels=['<18', '18-34', '35-49', '50-64', '65+'], new_column='age_binned')
    print(df['age_binned'].value_counts())
    
    df = create_bins(df, 'bmi', bins=[0, 18.5, 25, 30, 35, 40, 100], labels=['<18.5', '18.5-24.9', '25-29.9', '30-34.9', '35-39.9', '40+'], new_column='bmi_groups')
    print(df['bmi_groups'].value_counts())

    df = create_bins(df, 'systolic_bp', bins=[0, 120, 130, 140, 160, 180, 200], labels=['<120', '120-129', '130-139', '140-159', '160-179', '180+'], new_column='sbp_groups')
    print(df['sbp_groups'].value_counts())

    df = create_bins(df, 'diastolic_bp', bins=[0, 80, 85, 90, 100, 110, 120], labels=['<80', '80-84', '85-89', '90-99', '100-109', '110+'], new_column='dbp_groups')
    print(df['dbp_groups'].value_counts())

    df = create_bins(df, 'cholesterol_total', bins=[0, 200, 240, 280, 320, 360], labels=['<200', '200-239', '240-279', '280-319', '320+'], new_column='cholesterol_total_groups')
    print(df['cholesterol_total_groups'].value_counts())

    df = create_bins(df, 'cholesterol_hdl', bins=[0, 40, 60, 80, 100], labels=['<40', '40-59', '60-79', '80+'], new_column='cholesterol_hdl_groups')
    print(df['cholesterol_hdl_groups'].value_counts())
    df = create_bins(df, 'cholesterol_ldl', bins=[0, 100, 130, 160, 190, 220], labels=['<100', '100-129', '130-159', '160-189', '190+'], new_column='cholesterol_ldl_groups')
    print(df['cholesterol_ldl_groups'].value_counts())
    df = create_bins(df, 'glucose_fasting', bins=[0, 100, 125, 150, 200], labels=['<100', '100-124', '125-149', '150+'], new_column='glucose_fasting_groups')
    print(df['glucose_fasting_groups'].value_counts())
    df = create_bins(df, 'follow_up_months', bins=[0, 6, 12, 18, 24, 36, 50], labels=['<6', '6-11', '12-17', '18-23', '24-35', '36+'], new_column='follow_up_months_groups')
    print(df['follow_up_months_groups'].value_counts())
    df = create_bins(df, 'adherence_pct', bins=[0, 50, 80, 90, 100], labels=['<50', '50-79', '80-89', '90-100'], new_column='adherence_pct_groups')
    print(df['adherence_pct_groups'].value_counts())
    print(summarize_by_group(df, 'site'))

    
    # TODO: Add simple test example here
    # Example:
    # test_df = pd.DataFrame({'age': [25, 30, 35], 'bmi': [22, 25, 28]})
    # print("Test DataFrame created:", test_df.shape)
    # print("Test detect_missing:", detect_missing(test_df))