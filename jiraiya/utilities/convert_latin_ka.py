

def convert_latin_ka(text:str) -> str:
    """
    converts Goergian text written in latin to Georgian text written in Georgian
    :param text: text to convert
    :return: converted text    
    """

    dict_ka = {
        "შ":["sh","Sh"],
        "მასტ":["mast","Mast"],
        "ტრ":["tr","Tr"],
        "ტვ":["tv","Tv"],
        "ჭამ":["Cham","cham"],
        "ღ":["gh","Gh"],
        "ჩ":["ch","Ch"],
        "ძ":["dz","Dz"],
        "ა":["a","A"],
        "ბ":["b","B"],
        "გ":["g","G"],
        "დ":["d","D"],
        "ე":["e","E"],
        "ვ":["v","V"],
        "ზ":["z","Z"],
        "თ":["t"],
        "ი":["i","I"],
        "კ":["k","K"],
        "ლ":["l","L"],
        "მ":["m","M"],
        "ნ":["n","N"],
        "ო":["o","O"],
        "პ":["p","P"],
        "რ":["r","R"],
        "ს":["s","S"],
        "უ":["u","U"],
        "ფ":["f","F"],
        "ქ":["q","Q"],
        "ყ":["y","Y"],
        "ც":["c","C"],
        "წ":["w","W"],
        "ხ":["x","X"],
        "ჯ":["j","J"],
        "ჰ":["h","H"],
        #"ჟ":["J"]
    }

    for key, values in dict_ka.items():
        for value in values:
            text = text.replace(value, key)
    return text


if __name__ == '__main__':

    user_message = "raxdeba aba shensken mastero jiraia"

    user_message = convert_latin_ka(user_message)
    print(user_message)

