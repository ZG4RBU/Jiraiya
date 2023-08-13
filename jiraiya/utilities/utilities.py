

def write_file(path:str, message:str):
	with open(path, "w", encoding="utf-8") as f:
		f.write(message)


def split_text(text, chunk_size):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]


def shorten_text_line_length(text: str, max_chars: int) -> str:
    """
    Shortens the text line length to a maximum of specified characters.
    """
    lines = text.split("\n")
    new_lines = []

    for line in lines:
        while len(line) > max_chars:
            new_lines.append(line[:max_chars])
            line = line[max_chars:].strip()

        new_lines.append(line)

    return "\n".join(new_lines)


def get_emojis():
    import random

    emoji = ["😀","😃","😄","😁","😆","😅","😂","🤣","😊","😇","🙂","🙃","😉","😌","😍","🥰", "😘", 
            "😗", "😙", "😚","😋","😛","😝","😜","🤪","🤨","🧐","😏","😣", "😖","😫", "😩","😳","🥵",
            "🥶","😱","😨","😰","😓","🤗","🤔","🤭","🤫","😶","😑","😬","😲","🥱","😴","🤤","😵","🤒",
            "😌","💀","😈","👀","👅","👉👌","🍑👏","👗🤏","🍆","💦","💥","🔥","👙","🍌"]
    
    emoji = random.choices(emoji, k=random.randrange(1,4))
    emoji = "".join(emoji)

    return emoji