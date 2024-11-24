def normalize_player_name(input_name, name_variations):
    """
    Normalizes a player's name using the name variations dictionary.

    Parameters:
    - input_name (str): The player's name as received from user input.
    - name_variations (Dict[str, str]): The mapping of name variations to standard names.

    Returns:
    - str: The standard player name if found, else the input name.
    """
    normalized_name = name_variations.get(input_name.lower(), input_name)
    return normalized_name
