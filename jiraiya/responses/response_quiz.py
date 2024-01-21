import asyncio
import g4f
from googletranslate import translate



async def generate_quiz(anime:str) -> str:
    """
    Generate a quiz for the specified anime.

    :param anime: The name of the anime for which the quiz is generated.
    :return: A string containing the quiz.
    """

    quiz_prompt = f"""
    Write a quiz with 4 choices about {anime}. The quiz should be of extremely hard difficulty.
    Provide only 1 quiz question. Remember to enclose the question and answers in double bracket tags.
    Follow this format:
    
    [question]In the Naruto manga, what is the last name of Tsunade?[question]
    [1]Uchiha[1]
    [2]Senju[2]
    [3]Uzumaki[3]
    [4]Hyuga[4]
    [correct]Senju[correct]
    """

    try:
        # Generate quiz using GPT model
        quiz = await g4f.ChatCompletion.create_async(model='gpt-3.5-turbo', provider=g4f.Provider.GptGo, messages=[
                                     {"role": "user", "content": quiz_prompt}])
    except Exception as e:
        print(e)
    
    return quiz


async def get_quiz(anime:str, message_lang:str) -> tuple[str]:
    """
    Generate a challenging quiz question related to the specified anime.

    :param anime: The name of the anime for which the quiz question is generated.
    :param message_lang: The language in which the quiz question will be presented.
    
    :return: A tuple containing the quiz question and the correct answer index.
    """

    # Generate quiz using GPT model
    quiz = await generate_quiz(anime)

    # Extract quiz elements from generated response
    question = quiz.split("[question]", 1)[-1].split("[question]", 1)[0]
    a1 = quiz.split("[1]", 1)[-1].split("[1]", 1)[0]
    a2 = quiz.split("[2]", 1)[-1].split("[2]", 1)[0]
    a3 = quiz.split("[3]", 1)[-1].split("[3]", 1)[0]
    a4 = quiz.split("[4]", 1)[-1].split("[4]", 1)[0]
    correct = quiz.split("[correct]", 1)[-1].split("[correct]", 1)[0]

    # Get correct answer index
    correct_answer = None
    for idx, answer in enumerate([a1, a2, a3, a4]):
        if answer == correct:
            correct_answer = idx + 1

    # Translate quiz elements if needed
    if message_lang != "en":
        question = translate(question, dest=message_lang, src='en')
        await asyncio.sleep(.2)
        a1 = translate(a1, dest=message_lang, src='en')
        await asyncio.sleep(.2)
        a2 = translate(a2, dest=message_lang, src='en')
        await asyncio.sleep(.2)
        a3 = translate(a3, dest=message_lang, src='en')
        await asyncio.sleep(.2)
        a4 = translate(a4, dest=message_lang, src='en')

    # Construct final quiz question
    jiraiyas_response = f"{question}\n1. {a1}\n2. {a2}\n3. {a3}\n4. {a4}"

    return (jiraiyas_response, str(correct_answer))



if __name__ == '__main__':

    # Generate quiz for Naruto anime
    quiz = asyncio.run(generate_quiz(anime="Naruto"))
    print(f"quiz: {quiz}")