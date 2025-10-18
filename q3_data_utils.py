# TODO: Add shebang line: #!/usr/bin/env python3
# Assignment 5, Question 3: Data Utilities Library
# Core reusable functions for data loading, cleaning, and transformation.
#
# These utilities will be imported and used in Q4-Q7 notebooks.

#!/usr/bin/env python3

import pandas as pd
import numpy as np




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
    data = pd.read_csv(filepath)
    return data

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
    cleaned_data = df.copy()
    cleaned_data = cleaned_data.replace(sentinel_value, np.nan)
    if remove_duplicates:
        cleaned_data = cleaned_data.drop_duplicates()

    return cleaned_data


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
    missing_counts = df.isnull().sum()
    return missing_counts

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
    copy = df.copy()
    if strategy == "mean":
        copy[column] = copy[column].fillna(copy[column].mean())
    elif strategy == "median":
        copy[column] = copy[column].fillna(copy[column].median())
    elif strategy == "ffill":
        copy[column] = copy[column].fillna(method='ffill')
    return copy


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
    filtered_df = df.copy()
    for f in filters:
        col = f["column"]
        cond = f["condition"]
        val = f["value"]
        
        if cond == "equals:":
            filtered_df = filtered_df[filtered_df[col] == val]
        elif cond == "greater_than":
            filtered_df = filtered_df[filtered_df[col] > val]
        elif cond == "less_than":
            filtered_df = filtered_df[filtered_df[col] < val]
        elif cond == "in_range":
            filtered_df = filtered_df[(filtered_df[col] >= val[0]) & (filtered_df[col] <= val[1])]
        elif cond == "in_list":
            filtered_df = filtered_df[filtered_df[col].isin(val)]   
    return filtered_df
    


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
    transformed_df = df.copy()
    for col, type in type_map.items():
        if type == "datetime":
            transformed_df[col] = pd.to_datetime(transformed_df[col], errors= "coerce")
        elif type == "numeric":
            transformed_df[col] = pd.to_numeric(transformed_df[col], errors= "coerce")
        elif type == "category":
            transformed_df[col] = transformed_df[col].astype("category")
        elif type == "string":
            transformed_df[col] = transformed_df[col].astype("string")
    return transformed_df

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
    binned_df = df.copy()
    if new_column is None:
        new_column = f"{column}_binned"
    binned_df[new_column] = pd.cut(binned_df[column], bins=bins, labels=labels, include_lowest=True)
    return binned_df


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
        summary_df = df.groupby(group_col).describe()
    else:
        summary_df = df.groupby(group_col).agg(agg_dict)
    return summary_df




if __name__ == '__main__':
    # Optional: Test your utilities here
    print("Data utilities loaded successfully!")
    print("Available functions:")
    print("  - load_data()")
    print("  - clean_data()")
    print("  - detect_missing()")
    print("  - fill_missing()")
    print("  - filter_data()")
    print("  - transform_types()")
    print("  - create_bins()")
    print("  - summarize_by_group()")
    

    test_df = pd.DataFrame({"age": [25, 25, -999, 3], "bmi": [22, 22, 28, None]})
    print(test_df.dtypes)
    print("Test DataFrame created:", test_df.shape)
    print("Test clean_data:", clean_data(test_df))
    print("Test detect_missing:", detect_missing(test_df))
    print("Test fill_missing:", fill_missing(test_df, "bmi", "mean"))
    print("Test filter_data:", filter_data(test_df, [{"column": "age", "condition": "greater_than", "value": 20}]))
    print("Test transform_types:", transform_types(test_df, {"age": "numeric"}))
    print("Test create_bins:", create_bins(test_df, "age", bins=[0, 18, 30, 100], labels=["<18", "18-29", "30+"]))
    print("Test summarize_by_group:", summarize_by_group(test_df, "age", {"bmi": "mean"}))  

    print(test_df.dtypes)
