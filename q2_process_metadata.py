# TODO: Add shebang line: #!/usr/bin/env python3
# Assignment 5, Question 2: Python Data Processing
# Process configuration files for data generation.

#!/usr/bin/env python3

def parse_config(filepath: str) -> dict:
    """
    Parse config file (key=value format) into dictionary.

    Args:
        filepath: Path to q2_config.txt
    
    Returns:
        dict: Configuration as key-value pairs

    Example:
        >>> config = parse_config('q2_config.txt')
        >>> config['sample_data_rows']
        '100'
    """
    config = {}
    with open(filepath, 'r') as file:
        for i in file:
            key, value = i.strip().split('=')
            config[key] = value
    return config



def validate_config(config: dict) -> dict:
    """
    Validate configuration values using if/elif/else logic.

    Rules:
    - sample_data_rows must be an int and > 0
    - sample_data_min must be an int and >= 1
    - sample_data_max must be an int and > sample_data_min

    Args:
        config: Configuration dictionary

    Returns:
        dict: Validation results {key: True/False}

    Example:
        >>> config = {'sample_data_rows': '100', 'sample_data_min': '18', 'sample_data_max': '75'}
        >>> results = validate_config(config)
        >>> results['sample_data_rows']
        True
    """
    results = {}

    #sample_data_rows must be an int and > 0
    if isinstance(config.get("sample_data_rows"), int) and config["sample_data_rows"] > 0:
        results["sample_data_rows"] = True
    else:
        results["sample_data_rows"] = False

    #sample_data_min must be an int and >= 1
    if isinstance(config.get("sample_data_min"), int) and config["sample_data_min"] >= 1:
        results["sample_data_min"] = True
    else:
        results["sample_data_min"] = False

    #sample_data_max must be an int and > sample_data_min
    if not isinstance(config.get("sample_data_max"), int):
        results["sample_data_max"] = False
    elif config["sample_data_max"] <= config.get("sample_data_min", 0):
        results["sample_data_max"] = False
    else:
        results["sample_data_max"] = True

    return results


def generate_sample_data(filename: str, config: dict) -> None:
    """
    Generate a file with random numbers for testing, one number per row with no header.
    Uses config parameters for number of rows and range.

    Args:
        filename: Output filename (e.g., 'sample_data.csv')
        config: Configuration dictionary with sample_data_rows, sample_data_min, sample_data_max

    Returns:
        None: Creates file on disk

    Example:
        >>> config = {'sample_data_rows': '100', 'sample_data_min': '18', 'sample_data_max': '75'}
        >>> generate_sample_data('sample_data.csv', config)
        # Creates file with 100 random numbers between 18-75, one per row
        >>> import random
        >>> random.randint(18, 75)  # Returns random integer between 18-75
    """
    import random

    rows = int(config.get('sample_data_rows'))
    min_val = int(config.get('sample_data_min'))
    max_val = int(config.get('sample_data_max'))

    random_numbers = [random.randint(min_val, max_val) for i in range(rows)]
    
    with open(filename, "w") as file:
        for r in random_numbers:
            file.write(f"{r}\n")
        
    print(f"✅ File '{filename}' created with {rows} random numbers between {min_val} and {max_val}.")



def calculate_statistics(data: list) -> dict:
    """
    Calculate basic statistics.

    Args:
        data: List of numbers

    Returns:
        dict: {mean, median, sum, count}

    Example:
        >>> stats = calculate_statistics([10, 20, 30, 40, 50])
        >>> stats['mean']
        30.0
    """
    statistics = {"mean": 0, "median": 0, "sum": 0, "count": 0}
    n = len(data)
    sorted_data = sorted(data)
    statistics["mean"] = sum(data) / n
    statistics["median"] = sorted_data[n // 2] if n % 2 == 1 else (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2
    statistics["sum"] = sum(data)
    statistics["count"] = n
    return statistics
    



if __name__ == '__main__':
    # TODO: Test your functions with sample data
    # Example:
    # config = parse_config('q2_config.txt')
    # validation = validate_config(config)
    # generate_sample_data('data/sample_data.csv', config)
    # 
    # TODO: Read the generated file and calculate statistics
    # TODO: Save statistics to output/statistics.txt

    config = parse_config("q2_config.txt")
    validation = validate_config(config)
    generate_sample_data("data/sample_data.csv", config)
    with open("data/sample_data.csv", "r") as file:
        data = [int(line.strip()) for line in file.readlines()]

    stats = calculate_statistics(data)
    
    with open("output/statistics.txt", "w") as file:
        for key, value in stats.items():
            file.write(f"{key}: {value}\n")

    print("✅ Statistics saved to output/statistics.txt")
