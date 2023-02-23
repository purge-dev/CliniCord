import interactions
from interactions import Client, ComponentContext, Button
from interactions.ext.wait_for import setup
import asyncio

bot = Client(token="MTA3Nzk0OTkzMjUyNDI5MDExMA.Gn8ssT.2CEA2ePk2L6T6zBJxJJv9W5ZnZB6rdmPnZ2p9M")

# apply hooks to the class
setup(bot)

@bot.command(
    name="test", description="this is just a test command."
)
async def test(ctx):
    button = Button(style=1, label="testing", custom_id="testing")
    await ctx.send("grabbing a click...", components=button)

    async def check(button_ctx):
        if int(button_ctx.author.user.id) == int(ctx.author.user.id):
            return True
        await ctx.send("I wasn't asking you!", ephemeral=True)
        return False

    try:
        # Like before, this wait_for listens for a certain event, but is made specifically for components.
        # Although, this returns a new Context, independent of the original context.
        button_ctx: ComponentContext = await bot.wait_for_component(
            components=button, check=check, timeout=15
        )
        # With this new Context, you're able to send a new response.
        await button_ctx.send("You clicked it!")
    except asyncio.TimeoutError:
        # When it times out, edit the original message and remove the button(s)
        return await ctx.edit(components=[])


bot.start()