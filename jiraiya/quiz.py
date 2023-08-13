import discord
from jiraiya.responses.response_quiz import get_quiz
from jiraiya.utilities.json_utils import read_json


def parameters_quiz(message:str) -> tuple[str]:

    #set default parameters
    anime, message_lang = "Naruto", "en"

    parameters = message.split("-")
    for parameter in parameters:
        # skip the command
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
            await interaction.response.send_message(self.message_correct)
        else:
            await interaction.response.send_message(self.message_incorrect)

    @discord.ui.button(label='2')
    async def button2(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.quiz_answer == '2':
            await interaction.response.send_message(self.message_correct)
        else:
            await interaction.response.send_message(self.message_incorrect)

    @discord.ui.button(label='3')
    async def button3(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.quiz_answer == '3':
            await interaction.response.send_message(self.message_correct)
        else:
            await interaction.response.send_message(self.message_incorrect)

    @discord.ui.button(label='4')
    async def button4(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.quiz_answer == '4':
            await interaction.response.send_message(self.message_correct)
        else:
            await interaction.response.send_message(self.message_incorrect)


async def send_quiz(message, user_message:str, is_private:bool):

    anime,message_lang = parameters_quiz(user_message)
    quiz,quiz_answer = get_quiz(anime,message_lang)

    view = QuizView(quiz_answer)
    await message.author.send(quiz,view=view) if is_private else await message.channel.send(quiz,view=view)



