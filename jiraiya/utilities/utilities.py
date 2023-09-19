import random



def write_file(path:str, message:str):
    with open(path, "w", encoding="utf-8") as f:
        f.write(message)


def split_text(text:str, chunk_size:int) -> list[str]:
    """
    Splits text into a list of chunks of specified size.
    """
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]


def shorten_text_line_length(text:str, max_chars:int) -> str:
    """
    Shortens the text line length to a maximum of specified characters.
    """
    lines = text.split("\n")
    new_lines = []

    for line in lines:
        words = line.split()  # Split the line into words
        if not words:
            new_lines.append("")  # Append an empty line if the original line was empty
            continue

        current_line = words[0]

        for word in words[1:]:
            if len(current_line) + len(word) + 1 <= max_chars:  # Check if adding the word fits
                current_line += " " + word
            else:
                new_lines.append(current_line)
                current_line = word

        new_lines.append(current_line)  # Append the last line

    return "\n".join(new_lines)


def generate_nude_emojis() -> str:
    """
    Generates a random string of nude-themed emojis.

    This function randomly selects a sequence of nude-themed emojis and returns them as a single string.

    Returns:
        str: A string containing a random sequence of nude-themed emojis.
    """
    EMOJI = ["😀","😃","😄","😁","😆","😅","😂","🤣","😊","😇","🙂","🙃","😉","😌","😍","🥰", "😘", 
            "😗", "😙", "😚","😋","😛","😝","😜","🤪","🤨","🧐","😏","😣", "😖","😫", "😩","😳","🥵",
            "🥶","😱","😨","😰","😓","🤗","🤔","🤭","🤫","😶","😑","😬","😲","🥱","😴","🤤","😵","🤒",
            "😌","💀","😈","👀","👅","👉👌","🍑👏","👗🤏","🍆","💦","💥","🔥","👙","🍌"]

    random_emoji_count = random.randrange(1, 4)
    selected_emojis = random.choices(EMOJI, k=random_emoji_count)
    emoji_sequence = "".join(selected_emojis)

    return emoji_sequence