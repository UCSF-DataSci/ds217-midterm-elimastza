# TODO: Add shebang line: #!/usr/bin/env python3
# Assignment 5, Question 2: Python Data Processing
# Process configuration files for data generation.

#!/usr/bin/env python3

filename = "q2_config.txt"
if filename.endswith(".txt"):
    print("Processing txt file")

def config(dict) -> None:
    with open('q2_config.txt', 'r') as file:
        for line in file:
            content = file.read()
    print(f"File content: {content}")
    return config
    
sample_data_rows = 100
sample_data_min = 18
sample_data_max = 75

def parse_config(filepath: str) -> dict:
    with open(filepath, 'r') as file:
        lines = file.readlines()
    for line in lines:
        config == {sample_data_rows == '100', sample_data_min == '18',sample_data_max == '75'}
    return parse_config
    


    # TODO: Read file, split on '=', create dict
pass
# TODO:Validate config values with if/elif/else logic, sample_data_rows must be an int and > 0, sample_data_min must be an int and >= 1, sample_data_max must be an int and > sample_data_min

def validate_config(config: dict) -> dict:
    """ 
    sample_data_rows = int 
    sample_data_rows > 0 else: 
    sample_data_rows = "Invalid"
    sample_data_min = int
    sample_data_min >= 1 else:
    sample_data_min = "Invalid"
    sample_data_max = int
    sample_data_max > sample_data_min else:
    sample_data_max = "Invalid" """

        
    for sample_data_rows in config.get('sample_data_rows'):
        if not isinstance(sample_data_rows > 0, (int, float)):
            raise ValueError(f"Invalid sample_data_rows type: {type(sample_data_rows)}")

    for sample_data_min in config.get('sample_data_min'):
        if not isinstance(sample_data_min >= 1, (int, float)):
            raise ValueError(f"Invalid sample_data_min type: {type(sample_data_min)}")

    for sample_data_max in config.get('sample_data_max'):
        if not isinstance(sample_data_max > sample_data_min, (int, float)):
            raise ValueError(f"Invalid sample_data_max type: {type(sample_data_max)}")

    return validate_config 

    # TODO: Implement with if/elif/else

 

def generate_sample_data(filename: str, config: dict) -> None:
    
    # TODO: Parse config values (convert strings to int)
    # TODO: Generate random numbers and save to file
    # TODO: Use random module with config-specified range
    pass


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
    # TODO: Calculate stats
    pass


if __name__ == '__main__':
    # TODO: Test your functions with sample data
    # Example:
    # config = parse_config('q2_config.txt')
    # validation = validate_config(config)
    # generate_sample_data('data/sample_data.csv', config)
    # 
    # TODO: Read the generated file and calculate statistics
    # TODO: Save statistics to output/statistics.txt
    pass
