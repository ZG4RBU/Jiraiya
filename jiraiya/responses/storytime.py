import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import random
import os
import asyncio
from jiraiya.utilities.json_utils import read_json



def chrome_setup(implicit_wait:int,profile:str,headless:bool=False) -> uc.Chrome:
    options = uc.ChromeOptions()
    #options.add_argument("--window-size=1920x1080")
    options.add_argument('--start-maximized')
    options.add_argument('--disable-notifications')
    options.add_argument("--mute-audio")
    options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
    pc_user = os.getlogin()
    options.add_argument(rf'--user-data-dir=C:\Users\{pc_user}\AppData\Local\Google\Chrome\User Data')
    options.add_argument(f'--profile-directory={profile}')
    program_files = "Program Files" if "Google" in os.listdir("C:\\Program Files") else "Program Files (x86)"
    options.binary_location = f"C:\\{program_files}\\Google\\Chrome\\Application\\chrome.exe"

    if headless == True:
        options.add_argument("--headless")
        options.add_argument('--disable-gpu')

    driver = uc.Chrome(options=options)
    driver.implicitly_wait(implicit_wait)

    return driver


def get_sidekicks(character:dict,character_sex:str) -> list[str]:

    partner = character.get("partner")
    male_sidekick = character.get("male_sidekick")
    female_sidekick = character.get("female_sidekick")

    if character_sex == "Male":
        partner = random.choice(partner)
        female_sidekick = random.choice([i for i in female_sidekick if i != partner])
        male_sidekick = random.choices(male_sidekick,k=2)

        sidekicks = [partner,male_sidekick[0],female_sidekick,male_sidekick[1]]

    elif character_sex == "Female":
        partner = random.choice(partner)
        male_sidekick = random.choice([i for i in male_sidekick if i != partner])
        female_sidekick = random.choices(female_sidekick,k=2)

        sidekicks = [female_sidekick[0],partner,female_sidekick[1],male_sidekick]

    return sidekicks


async def generate_story(preset:str,character_name:str) -> tuple[str]:

    driver:uc.Chrome = chrome_setup(implicit_wait=10,profile="Default")

    try:
        driver.get("https://fanficmaker.com/")
        #agree
        driver.find_element(By.XPATH, '//button[@class="gwt-Button"]').click()

        #choose preset
        driver.find_element(By.XPATH, '//button[@class="gwt-Button FakeListArrow"]').click()
        driver.find_element(By.XPATH, f'.//div[contains(text(),"{preset}")]').click()

        #load character
        characters:dict = read_json("data/scroll_characters.json")
        character:dict = characters[character_name][0]

        #select sex
        character_sex = character.get('sex')
        driver.find_element(By.XPATH, f"//option[@value='{character_sex}']").click()

        characters_inputs = driver.find_elements(By.XPATH, '//input[@class="gwt-TextBox"]')
        sidekicks = get_sidekicks(character,character_sex)

        for index,character_input in enumerate(characters_inputs):
            if index == 0:
                input = character_name
            elif index == 1:
                input = character.get("superpower")
            elif index == 2:
                input = character.get("hobby")
            elif index == 3:
                input = character.get("hometown")
            elif index == 5:
                input = sidekicks[0]
            elif index == 6:
                input = sidekicks[1]
            elif index == 7:
                input = sidekicks[2]
            elif index == 8:
                input = sidekicks[3]
            elif index == 10:
                input = character.get("MacGuffin")
            else: continue

            character_input.clear()
            character_input.send_keys(input)

        #change villain name/sex
        villains = character.get("villains")
        villain = random.choice(villains)

        villain_input = driver.find_elements(By.XPATH, '//input[@class="gwt-TextBox"]')[9] #name
        villain_input.clear()
        villain_input.send_keys(villain)

        villain_sex = "Male" if villain != "Kaguya" else "Female"
        driver.find_elements(By.XPATH, f"//option[@value='{villain_sex}']")[1].click() #sex

        #increase sex
        driver.find_elements(By.XPATH, './/div[@class="gwt-SliderBar-shell"]')[2].send_keys(Keys.ARROW_RIGHT * 15)

        #change relationship
        driver.find_element(By.XPATH, "//option[@value='Hero']").click()
        partner_sex = 'FSide1' if character_sex == 'Male' else 'MSide1'
        driver.find_elements(By.XPATH, f"//option[@value='{partner_sex}']")[1].click()

        #change authors name/sex
        authors_name = driver.find_elements(By.XPATH, '//input[@class="gwt-TextBox"]')[11] #name
        authors_name.clear()
        authors_name.send_keys("Jiraiya")
        driver.find_elements(By.XPATH, "//option[@value='Male']")[2].click() #sex

        #make story
        driver.find_element(By.XPATH, './/button[@class="MakeStory glowlink"]').click()
        await asyncio.sleep(10)

        title = driver.find_element(By.XPATH, './/div[@class="titlestyle"]').text
        story = driver.find_element(By.XPATH, './/div[@class="TextAreaAsLabel DefaultFanficFont"]').text

    except Exception as e:
        print(e)

    driver.quit()

    return (title,story)


if __name__ == '__main__':

    title,story = generate_story(preset="Naruto",character="Sakura")
    print(title)
    print(story)