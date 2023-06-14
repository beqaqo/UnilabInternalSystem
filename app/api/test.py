options = {
    "Question1": True,
    "Question2": False,
}


for option in options.keys():
    text = option
    is_correct = options[option]
    print(text)
    print(is_correct)