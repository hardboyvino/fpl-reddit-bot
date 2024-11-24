import praw
import config

from data_loader import load_predictions, load_name_variations
from name_normalizer import normalize_player_name
from nlp_processor import extract_player_names, determine_query_type

input_filename = 'raw_2_day_comments_sample.txt'
output_filename = 'comments_with_responses.txt'

with open(output_filename, 'w', encoding='utf-8') as file:
        # Just opening in 'w' mode clears the contents
        pass

def main():
    """
    Main function to interact with Reddit API.
    """
    # Load data files
    predictions = load_predictions('predictions.csv')
    name_variations = load_name_variations('name_variations.json')

    # Load comments from the text file
    comments = load_comments_from_file(input_filename)

    # Output the total number of comments fetched
    print(f"Total Comments Fetched: {len(comments)}\n")

    # Iterate through comments and print author and comment body
    for comment in comments:
        input_text = comment.strip()

        # Determine the query type
        query_type = determine_query_type(input_text)

        # Extract player names
        extracted_players = extract_player_names(input_text, name_variations)

        # Process based on query type
        if query_type == 'Comparison' and len(extracted_players) == 2:
            # Handle player comparison
            response = handle_player_comparison(extracted_players, predictions)
        elif query_type == 'Transfer' and len(extracted_players) >= 1:
            # Handle transfer advice
            response = handle_transfer_advice(extracted_players, predictions)
        elif query_type == 'RMT':
            # Handle Rate My Team (RMT)
            response = handle_rmt(extracted_players, predictions)
        else:
            # Unable to process the comment
            response = "I'm sorry, I couldn't understand your query."

        # Output the response as txt
        with open(output_filename, mode='a', encoding='utf-8') as file:
            file.write(f"Query Type: {query_type}\n")
            file.write(f"Extracted Players: {extracted_players}\n")
            file.write(f"Comment: {input_text}\n")
            file.write(f"Response: {response}\n")
            file.write('-' * 40 + '\n')

def load_comments_from_file(file_path):
    """
    Loads comments from a text file.

    Parameters:
    - file_path (str): The path to the text file containing comments.

    Returns:
    - List[str]: A list of comments.
    """
    comments = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            # Split comments based on separator lines
            comments = content.split('----------------------------------------')
            # Remove any empty strings and strip whitespace
            comments = [comment.strip() for comment in comments if comment.strip()]
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred while loading comments: {e}")
    return comments

def fetch_top_level_comments(thread_url):
    """
    Fetches top-level comments from Reddit thread
    """
    # Initialize Reddit instance
    reddit = praw.Reddit(
        client_id=config.REDDIT_CLIENT_ID,
        client_secret=config.REDDIT_CLIENT_SECRET,
        username=config.REDDIT_USERNAME,
        password=config.REDDIT_PASSWORD,
        user_agent=config.REDDIT_USER_AGENT
    )

    # Fetch the submission using the URL
    submission = reddit.submission(url=thread_url)

    # Fetch only top-level comments
    submission.comments.replace_more(limit=0)
    comments = list(submission.comments)

    return submission.title, comments

def handle_player_comparison(players, predictions):
    """
    Generates a response for player comparisons.

    Parameters:
    - players (List[str]): List of player names.
    - predictions (Dict[Tuple[str, str], float]): Predicted points.

    Returns:
    - str: Response text.
    """
    player_points = []
    for player_name in players:
        normalized_name = player_name
        # Find all matching players
        matching_players = [
            ((name, team), points)
            for ((name, team), points) in predictions.items()
            if name == normalized_name.lower()
        ]

        if matching_players:
            # For simplicity, pick the first matching player
            (name_team_key, predicted_points) = matching_players[0]
            standard_name, team_name = name_team_key
            player_points.append((standard_name, team_name.title(), predicted_points))
        else:
            # Default to 1 point if not found
            player_points.append((normalized_name, 'Unknown Team', 1.0))

    # Compare the two players
    player1, player2 = player_points
    if player1[2] > player2[2]:
        better_player = f"{player1[0]} ({player1[1]})"
    else:
        better_player = f"{player2[0]} ({player2[1]})"

    response = f"Based on predicted points, {better_player} is the better choice."
    return response

def handle_transfer_advice(players, predictions):
    """
    Generates a response for transfer advice.

    Parameters:
    - players (List[str]): List of player names.
    - predictions (Dict[Tuple[str, str], float]): Predicted points.

    Returns:
    - str: Response text.
    """
    responses = []
    for player_name in players:
        normalized_name = player_name
        matching_players = [
            ((name, team), points)
            for ((name, team), points) in predictions.items()
            if name == normalized_name.lower()
        ]
        if matching_players:
            (name_team_key, predicted_points) = matching_players[0]
            standard_name, team_name = name_team_key
            responses.append(f"{standard_name} ({team_name.title()}): {predicted_points:.2f} points")
        else:
            responses.append(f"{normalized_name}: 1.00 point (default)")

    response = "Here are the predicted points for the players:\n" + "\n".join(responses)
    return response

def handle_rmt(players, predictions):
    """
    Generates a response for Rate My Team (RMT) queries.

    Parameters:
    - players (List[str]): List of player names.
    - predictions (Dict[Tuple[str, str], float]): Predicted points.

    Returns:
    - str: Response text.
    """
    total_points = 0.0
    for player_name in players:
        normalized_name = player_name
        matching_players = [
            ((name, team), points)
            for ((name, team), points) in predictions.items()
            if name == normalized_name.lower()
        ]
        if matching_players:
            (_, _), predicted_points = matching_players[0]
            total_points += predicted_points
        else:
            total_points += 1.0  # Default point

    response = f"Your team's total predicted points are approximately {total_points:.2f}."
    return response

if __name__ == "__main__":
    main()