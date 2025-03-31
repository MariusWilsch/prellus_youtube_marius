def calculate_reading_characters(minutes, reading_speed=250):
    """
    Calculate the number of characters that can be read in a given time.
    
    Parameters:
    minutes (float): Reading time in minutes
    reading_speed (int): Reading speed in words per minute (default: 250 wpm)
    
    Returns:
    int: Number of characters that can be read in the given time
    """
    avg_chars_per_word = 5  # Average English word length including space
    words = reading_speed * minutes
    characters = words * avg_chars_per_word
    
    return int(characters)


if __name__ == "__main__":
    print(calculate_reading_characters(30))