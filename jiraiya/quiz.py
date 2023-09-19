import discord
from jiraiya.responses.response_quiz import get_quiz
from jiraiya.utilities.json_utils import read_json



def parameters_quiz(user_message:str) -> tuple[str]:
    """
    Extract and return parameters for the quiz from the user's message.

    :param user_message: The user's message input.
    :return: A tuple containing the anime and message language parameters.
    """

    # Set default parameters
    anime, message_lang = "Naruto", "en"

    parameters = user_message.split("-")
    for parameter in parameters:
        # skip the parameter
        if "!" in parameter:
            continue

        parameter = parameter.strip()

        if len(parameter) == 2:
            message_lang = parameter
        else:
            anime = parameter

    return (anime,message_lang)


class QuizView(discord.ui.View):
    def __init__(self, quiz_answer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.quiz_answer = quiz_answer

        messages_data = read_json()
        language:str = messages_data["jiraiyas_language"]
        messages:list = messages_data["quiz"][language]
        self.message_correct = messages.get("correct")
        self.message_incorrect = messages.get("incorrect")

    @discord.ui.button(label='1')
    async def button1(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.quiz_answer == '1':
            reply_message = self.message_correct
        else:
            reply_message = self.message_incorrect

        await interaction.response.send_message(f"{interaction.user.mention} {reply_message}")

    @discord.ui.button(label='2')
    async def button2(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.quiz_answer == '2':
            reply_message = self.message_correct
        else:
            reply_message = self.message_incorrect

        await interaction.response.send_message(f"{interaction.user.mention} {reply_message}")

    @discord.ui.button(label='3')
    async def button3(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.quiz_answer == '3':
            reply_message = self.message_correct
        else:
            reply_message = self.message_incorrect

        await interaction.response.send_message(f"{interaction.user.mention} {reply_message}")

    @discord.ui.button(label='4')
    async def button4(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.quiz_answer == '4':
            reply_message = self.message_correct
        else:
            reply_message = self.message_incorrect

        await interaction.response.send_message(f"{interaction.user.mention} {reply_message}")


async def send_quiz(message, user_message:str, is_private:bool):
    """
    Send a quiz to the user or channel based on the user's input.

    :param message: The Discord message object.
    :param user_message: The user's input message.
    :param is_private: Boolean indicating whether the quiz should be sent as a private message.
    :return: None
    """

    anime, message_lang = parameters_quiz(user_message)
    quiz, quiz_answer = await get_quiz(anime, message_lang)

    view = QuizView(quiz_answer)

    if is_private:
        await message.author.send(quiz, view=view)
    else:
        await message.channel.send(quiz, view=view)