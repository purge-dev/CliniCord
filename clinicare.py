from interactions import Client, CommandContext, ComponentContext, Embed, SelectOption, SelectMenu, Emoji
from interactions.ext.wait_for import setup
import asyncio

client = Client(token="MTA3Nzk0OTkzMjUyNDI5MDExMA.Gn8ssT.2CEA2ePk2L6T6zBJxJJv9W5ZnZB6rdmPnZ2p9M")
setup(client)

@client.event
async def on_ready():
    print(f"{client.me.name} successfully connected at {round(client.latency)} ms.")

questions  = [
    {"question": "Sadness", "options": ["I do not feel sad.", "I feel sad much of the time.", "I am sad all the time.", "I am so sad or unhappy that I can't stand it."]},
    {"question": "Pessimism", "options": ["I am not discouraged about my future.", "I feel more discouraged about my future than I used to be.", "I do not expect things to work out for me.", "I feel my future is hopeless and will only get worse."]},
    {"question": "Past failure", "options": ["I do not feel like a failure.", "I have failed more than I should have.", "As I look back, I see a lot of failures.", "I feel I am a complete failure as a person."]},
    {"question": "Loss of pleasure", "options": ["I get as much pleasure as I ever did from the things I enjoy.", "I don't enjoy things as much as I used to.", "I get very little pleasure from the things I used to enjoy.", "I can't get any pleasure from the things I used to enjoy."]},
    {"question": "Guilty feelings", "options": ["I don't feel particularly guilty.", "I feel guilty a good part of the time.", "I feel quite guilty most of the time.", "I feel guilty all of the time."]},
    {"question": "Punishment feelings", "options": ["I don't feel I am being punished.", "I feel I may be punished.", "I expect to be punished.", "I feel I am being punished."]},
    {"question": "Self-dislike", "options": ["I don't feel that I am any worse than anybody else.", "I am critical of myself for my weaknesses or mistakes.", "I blame myself all the time for my faults.", "I blame myself for everything bad that happens."]},
    {"question": "Self-criticalness", "options": ["I don't criticize or blame myself more than usual.", "I am more critical of myself than I used to be.", "I criticize myself for all of my faults.", "I blame myself for everything that goes wrong."]},
    {"question": "Suicidal thoughts or wishes", "options": ["I don't have any thoughts of killing myself.", "I have thoughts of killing myself, but I would not carry them out.", "I would like to kill myself.", "I would kill myself if I had the chance."]},
    {"question": "Crying", "options": ["I don't cry any more than usual.", "I cry more now than I used to.", "I cry all the time now.", "I used to be able to cry, but now I can't cry even though I want to."]},
    {"question": "Agitation", "options": ["I am no more restless or wound up than usual.", "I feel more restless or wound up than usual.", "I am so restless or agitated that it's hard to stay still.", "I am so restless or agitated that I have to keep moving or doing something."]},
    {"question": "Loss of interest", "options": ["I have not lost interest in other people.", "I am less interested in other people than I used to be.", "I have lost most of my interest in other people.", "I have lost all of my interest in other people."]},
    {"question": "Indecisiveness", "options": ["I make decisions about as well as ever.", "I put off making decisions more than I used to.", "I have greater difficulty in making decisions more than I used to.", "I can't make decisions at all anymore."]},
    {"question": "Worthlessness", "options": ["I don't feel that I am worthless.", "I don't consider myself as worthwhile and useful as I used to.", "I feel more worthless as compared to others.", "I feel completely worthless."]},
    {"question": "Loss of energy", "options": ["I have as much energy as ever.", "I have less energy than I used to have.", "I don't have enough energy to do much.", "I don't have enough energy to do anything."]},
    {"question": "Changes in sleeping pattern", "options": ["I have not experienced any change in my sleeping pattern.", "I sleep somewhat more than usual.", "I sleep somewhat less than usual.", "I sleep a lot less than usual."]},
    {"question": "Irritability", "options": ["I am no more irritable than usual.", "I am more irritable than usual.", "I am much more irritable than usual.", "I am irritable all the time."]},
    {"question": "Changes in appetite", "options": ["My appetite is no different than usual.", "My appetite is not as good as it used to be.", "My appetite is much worse now.", "I have no appetite at all anymore."]},
    {"question": "Concentration difficulties", "options": ["I can concentrate as well as ever.", "I can't concentrate as well as usual.", "It's hard to keep my mind on anything for very long.", "I find I can't concentrate on anything."]},
    {"question": "Tiredness or fatigue", "options": ["I am no more tired or fatigued than usual.", "I get more tired or fatigued more easily than I used to.", "I am too tired or fatigued to do many of the things I used to do.", "I am too tired or fatigued to do most of the things I used to do."]},
    {"question": "Loss of interest in sex", "options": ["I have not noticed any recent change in my interest in sex.", "I am less interested in sex than I used to be.", "I have lost interest in sex completely.", "I find sex completely unappealing."]}
    ]

@client.command(name="depression", description='Evaluates whether you are suffering from clinical depression using the validated BDI questionnaire.')
async def depression(ctx: CommandContext):
    score = 0

    pic0, pic1, pic2, pic3 = Emoji(), Emoji(), Emoji(), Emoji() # fix this mess
    pic0.name = "🙂" 
    pic1.name = "😕"
    pic2.name = "🙁"
    pic3.name = "😢"

    embed = Embed(title="🧠 CliniCare: Mind", description=f"Hey, <@{ctx.author.id}>, tell me how you currently feel.", color=0xFFFFFF)
    embed.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRNFMDb6nEd906vJEn6xg62TOtwIVHvBDGK2Q&usqp=CAU")

    for i, question in enumerate(questions): # cycle through each question and make a menu for each
        selection = [SelectOption(
            label=question['options'][0], value="0", emoji=pic0),
            SelectOption(
            label=question['options'][1], value="1", emoji=pic1),
            SelectOption(
            label=question['options'][2], value="2", emoji=pic2),
            SelectOption(
            label=question['options'][3], value="3", emoji=pic3)]
        embed.set_footer(f"Question {i+1} of 21.")
        menu = SelectMenu(placeholder="Choose a statement", custom_id=str(i), options=selection)   

        await ctx.send(embeds=embed, components=menu, ephemeral=True)

        async def check(res: ComponentContext):
            if res.author.id == ctx.author.id and res.data.custom_id == menu.custom_id:
                return True

        try:
            res: ComponentContext = await client.wait_for_component(components=menu, check=check, timeout=60)
            await ctx.delete() # remove message so it can display the next one
           # await res.send(f"You chose: {str(res.data.values[0])}", ephemeral=True)
            score += int(res.data.values[0])
    
        except asyncio.TimeoutError:
            await ctx.delete() # remove the message if user takes too long
            await ctx.send(f"You took too long to respond! Please try again.", ephemeral=True)
            return       

    # clean this into a function and add buttons for treatment/SOS/support lines
    if (score <= 10):
        embed.description = "Your responses suggest **normal** levels of stress. Ups and downs happen in life and shape who we are for the better. Keep going strong!"
        embed.set_thumbnail("https://raw.githubusercontent.com/purge-dev/clinicare/main/assets/normal.png")
        embed.color = 0x00FF00
        embed.set_footer("⚠ Consult your doctor if your symptoms worsen.")
        await ctx.send(embeds=embed, ephemeral=True)

    elif (score >= 11 and score <= 16):
        embed.description = "Your responses suggest **mild** levels of mood disturbance."
        embed.set_thumbnail("https://raw.githubusercontent.com/purge-dev/clinicare/main/assets/moody.png")
        embed.color = 0xFFFF00
        embed.set_footer("⚠ Consult your doctor if your symptoms worsen.")
        await ctx.send(embeds=embed, ephemeral=True)

    elif (score >= 17 and score <= 20):
        embed.description = "Your responses suggest **borderline clinical depression**. Consider making an appointment with your doctor to discuss ways going forward."
        embed.set_thumbnail("https://raw.githubusercontent.com/purge-dev/clinicare/main/assets/moody.png")
        embed.color = 0xFFA500
        embed.set_footer("⚠ Consult your doctor if your symptoms worsen.")
        await ctx.send(embeds=embed, ephemeral=True)

    elif (score >= 21 and score <= 30):
        embed.description = "Your responses suggest **moderate clinical depression**. Consult a mental health professional soon to discuss ways going forward."
        embed.set_thumbnail("https://raw.githubusercontent.com/purge-dev/clinicare/main/assets/borderline.png")
        embed.color = 0xFF8C00
        embed.set_footer("⚠ Consult your doctor if your symptoms worsen.")
        await ctx.send(embeds=embed, ephemeral=True)

    elif (score >= 31 and score <= 40):
        embed.description = "Your responses suggest **severe clinical depression**. Consult a doctor or mental health professional soon to discuss ways going forward."
        embed.set_thumbnail("https://raw.githubusercontent.com/purge-dev/clinicare/main/assets/severe.png")
        embed.color = 0xFF0000
        embed.set_footer("⚠ Visit the ER if you are considering self-harm or worse.")
        await ctx.send(embeds=embed, ephemeral=True)

    elif (score > 40):
        embed.description = "Your responses suggest **extreme clinical depression**. Please visit an urgent care mental health clinic as this is likely impacting your overall health."
        embed.set_thumbnail("https://raw.githubusercontent.com/purge-dev/clinicare/main/assets/severe.png")
        embed.color = 0x8B0000
        embed.set_footer("⚠ Visit the ER if you are considering self-harm or worse.")
        await ctx.send(embeds=embed, ephemeral=True)

client.start()

