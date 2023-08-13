import g4f
from googletranslate import translate
from time import sleep


def get_quiz(anime:str,message_lang:str) -> tuple[str]:

    quiz_prompt = f"""
write quiz with 4 choices about anime {anime}. I want the quiz to be extremely hard difficulty. write only 1 quiz question. Also do not forget to insert the qustions and answers in double bracket tags. provide the quiz in the format as this example:
[question]In the Naruto manga, what is the last name of Tsunade?[question]
[1]Uchiha[1]
[2]Senju[2]
[3]Uzumaki[3]
[4]Hyuga[4]
[correct]Senju[correct]
"""

    # generate Quiz
    try:
        # normal response
        quiz = g4f.ChatCompletion.create(model='gpt-3.5-turbo', provider=g4f.Provider.DeepAi, messages=[
                                     {"role": "user", "content": quiz_prompt}]) # alterative model setting
    except Exception as e:
        print(e)

    # Remove double bracket tags
    question = quiz.split("[question]", 1)[-1].split("[question]", 1)[0]
    a1 = quiz.split("[1]", 1)[-1].split("[1]", 1)[0]
    a2 = quiz.split("[2]", 1)[-1].split("[2]", 1)[0]
    a3 = quiz.split("[3]", 1)[-1].split("[3]", 1)[0]
    a4 = quiz.split("[4]", 1)[-1].split("[4]", 1)[0]
    correct = quiz.split("[correct]", 1)[-1].split("[correct]", 1)[0]

    # Get correct answer
    correct_answer = None
    for idx, answer in enumerate([a1, a2, a3, a4]):
        if answer == correct:
            correct_answer = idx + 1

    # Translate quiz from English to other language
    if message_lang != "en":
        question = translate(question, dest=message_lang, src='en')
        sleep(.2)
        a1 = translate(a1, dest=message_lang, src='en')
        sleep(.2)
        a2 = translate(a2, dest=message_lang, src='en')
        sleep(.2)
        a3 = translate(a3, dest=message_lang, src='en')
        sleep(.2)
        a4 = translate(a4, dest=message_lang, src='en')

    jiraiyas_response = f"{question}\n1. {a1}\n2. {a2}\n3. {a3}\n4. {a4}"

    return jiraiyas_response, str(correct_answer)