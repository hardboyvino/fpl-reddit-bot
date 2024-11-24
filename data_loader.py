import csv
import json

def load_predictions(csv_file_path):
    """
    Loads the weekly points predictions from a CSV file.

    Parameters:
    - csv_file_path (str): The file path to the predictions CSV.

    Returns:
    - Dict[Tuple[str, str], float]: A dictionary mapping (player name, team) tuples to their predicted points.
    """
    predictions = {}
    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                player_name = row['Name'].strip()
                team_name = row['Team'].strip()
                predicted_points = float(row['Points'])
                key = (player_name.lower(), team_name.lower())
                predictions[key] = predicted_points
    except FileNotFoundError:
        print(f"Error: The file {csv_file_path} was not found.")
    except Exception as e:
        print(f"An error occurred while loading predictions: {e}")
    return predictions


# data_loader.py (continued)

def load_name_variations(json_file_path):
    """
    Loads the player name variations from a JSON file.

    Parameters:
    - json_file_path (str): The file path to the name variations JSON.

    Returns:
    - Dict[str, str]: A dictionary mapping variation names to standard player names.

    Note: Since team names are not included in the name variations, we will handle
    potential ambiguities during name normalization.
    """
    name_variations = {}
    try:
        with open(json_file_path, mode='r', encoding='utf-8') as jsonfile:
            data = json.load(jsonfile)
            for standard_name, variations in data.items():
                for variation in variations:
                    name_variations[variation.lower()] = standard_name
                # Also map the standard name to itself
                name_variations[standard_name.lower()] = standard_name
    except FileNotFoundError:
        print(f"Error: The file {json_file_path} was not found.")
    except Exception as e:
        print(f"An error occurred while loading name variations: {e}")
    return name_variations
