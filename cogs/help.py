import discord
import asyncio
from utilities import default
from discord.ext import commands
from lib.bot import owners


COG_EXCEPTIONS = ['OWNER','HELP','CONFIG']
COMMAND_EXCEPTIONS = ['EYES']


def setup(bot):
    bot.remove_command("help")
    bot.add_cog(Help(bot))


class Help(commands.Cog):
    """
    Help command cog
    """
    def __init__(self, bot):
        self.bot = bot


      ############################
     ## Get Commands From Cogs ##
    ############################

    async def send_help(self, ctx, embed, pm, delete_after):
        if pm is True:
            if not ctx.guild: 
                msg = await ctx.send(embed=embed)
                return
            try:
                msg = await ctx.author.send(embed=embed)
                try:
                    await ctx.message.add_reaction("<:mailbox1:811303021492305990>")
                except: return
            except:
                msg = await ctx.send(embed=embed, delete_after=delete_after)
        else:
            msg = await ctx.send(embed=embed, delete_after=delete_after)

        def reaction_check(m):
            if m.message_id == msg.id and m.user_id == ctx.author.id and str(m.emoji) == "<:trashcan:805643072896892949>":
                return True
            return False

        try:
            await msg.add_reaction("<:trashcan:805643072896892949>")
            await self.bot.wait_for('raw_reaction_add', timeout=120.0, check=reaction_check)
            await msg.delete()
        except asyncio.TimeoutError:
            await msg.delete()
        except discord.Forbidden:
            return

    async def helper_func(self, ctx, cog, name, pm, delete_after):
        the_cog = sorted(cog.get_commands(), key=lambda x:x.name)
        cog_commands = []
        for c in the_cog:
            if c.hidden and ctx.author.id not in owners: continue
            if str(c.name).upper() in COMMAND_EXCEPTIONS and ctx.author.id not in owners: continue
            cog_commands.append(c)
        if cog_commands:
            await self.category_embed(ctx, cog=cog.qualified_name, list=cog_commands, pm=pm, delete_after=delete_after)
        else:
            return await ctx.send(f":warning: No command named `{name}` found.")


      ##########################
     ## Build Category Embed ##
    ##########################
    

    async def category_embed(self, ctx, cog, list, pm, delete_after):
        embed = discord.Embed(title=f"Category: `{cog}`",
        description=f"**Bot Invite Link:** [https://ngc.discord.bot](https://discord.com/oauth2/authorize?client_id=810377376269205546&scope=bot&permissions=8)\n"
                    f"**Support Server:**  [https://discord.gg/ngc](https://discord.gg/947ramn)\n", color=default.config()["embed_color"])
        embed.set_footer(text=f"Use \"{ctx.prefix}help command\" for information and usage examples on a command.\n")

        msg = ""
        for i in list:
            if i.brief is None:
                i.brief = "No description"
            line = f"\n`{i.name}` {i.brief}\n"
            msg += line
        embed.add_field(name=f"**{cog} Commands**", value=f"** **{msg}")
        
        await self.send_help(ctx, embed, pm, delete_after)


    @commands.command(name="help", brief="NGC0000's Help Command")
    async def _help(self, ctx, invokercommand:str = None, pm = False, delete_after=None):
        """
        Usage:  -help [command/category] [pm = true]
        Output: HELP!
        """
        if str(invokercommand).upper() in ["YES","TRUE"]:
            trigger = None
            pm = True

        elif invokercommand and str(pm).upper() in ["YES","TRUE"]:
            trigger = True
            pm = True

        else:
            if invokercommand:
                trigger = True
                pm = False
            else:
                trigger = None
                pm = False

        if trigger is None:

              ##########################
             ## Manages General Help ##
            ##########################

            embed = discord.Embed(title=f"{self.bot.user.name}'s Help Command", url="https://discord.gg/947ramn",
            description=f"**Bot Invite Link:** [https://ngc.discord.bot](https://discord.com/oauth2/authorize?client_id=810377376269205546&scope=bot&permissions=8)\n"
                        f"**Support Server:**  [https://discord.gg/ngc](https://discord.gg/947ramn)", color=default.config()["embed_color"])

            embed.set_footer(text=f"Use \"{ctx.prefix}help category\" for specific information on a category.")

            valid_cogs = []
            msg = ""
            for cog in sorted(self.bot.cogs):
                c = self.bot.get_cog(cog)
                if c.qualified_name.upper() in COG_EXCEPTIONS: continue
                valid_cogs.append(c)
            for c in valid_cogs:
                line = f"\n`{c.qualified_name}` {c.description}\n"
                msg += line

            embed.add_field(name=f"**Current Categories**", value=f"** **{msg}")

            await self.send_help(ctx, embed, pm, delete_after)

        elif trigger is True:

              ######################
             ## Manages Cog Help ##
            ######################

            if invokercommand.lower() in ["auto","automod","automoderation"]:
                cog = self.bot.get_cog("Automoderation")
                return await self.helper_func(ctx, cog=cog, name=invokercommand, pm = pm, delete_after=delete_after)

            if invokercommand.lower() in ["channel","channels","channeling","channelling"]:
                cog = self.bot.get_cog("Channels")
                return await self.helper_func(ctx, cog=cog, name=invokercommand, pm = pm, delete_after=delete_after)

            if invokercommand.lower() in ["config","conf"]:
                cog = self.bot.get_cog("Config")
                return await self.helper_func(ctx, cog=cog, name=invokercommand, pm = pm, delete_after=delete_after)

            if invokercommand.lower() in ["info","general","information"]:
                cog = self.bot.get_cog("General")
                return await self.helper_func(ctx, cog=cog, name=invokercommand, pm = pm, delete_after=delete_after)

            if invokercommand.lower() in ["message","messages","cleanup","msg","msgs"]:
                cog = self.bot.get_cog("Messages")
                return await self.helper_func(ctx, cog=cog, name=invokercommand, pm = pm, delete_after=delete_after)

            if invokercommand.lower() in ["logging","logger","logs"]:
                cog = self.bot.get_cog("Logging")
                return await self.helper_func(ctx, cog=cog, name=invokercommand, pm = pm, delete_after=delete_after)

            if invokercommand.lower() in ["mod","moderator","punishment","moderation"]:
                cog = self.bot.get_cog("Moderation")
                return await self.helper_func(ctx, cog=cog, name=invokercommand, pm = pm, delete_after=delete_after)

            if invokercommand.lower() in ["owner","master","creator","owners","hidden","own"]:
                cog = self.bot.get_cog("Owner")
                return await self.helper_func(ctx, cog=cog, name=invokercommand, pm = pm, delete_after=delete_after)
                
            if invokercommand.lower() in ["roles","role","serverroles"]:
                cog = self.bot.get_cog("Roles")
                return await self.helper_func(ctx, cog=cog, name=invokercommand, pm = pm, delete_after=delete_after)

            if invokercommand.lower() in ["admin","administration","administrator","settings","setup","configuration"]:
                cog = self.bot.get_cog("Settings")
                return await self.helper_func(ctx, cog=cog, name=invokercommand, pm = pm, delete_after=delete_after)

            if invokercommand.lower() in ["stats","statistics","track","tracking"]:
                cog = self.bot.get_cog("Statistics")
                return await self.helper_func(ctx, cog=cog, name=invokercommand, pm = pm, delete_after=delete_after)

            if invokercommand.lower() in ["warner","warning","warnings"]:
                cog = self.bot.get_cog("Warnings")
                return await self.helper_func(ctx, cog=cog, name=invokercommand, pm = pm, delete_after=delete_after)
    
            else:

                  ##########################
                 ## Manages Command Help ##
                ##########################

                valid_cog = ""
                valid_commands = ""
                valid_help = ""
                valid_brief = ""
                for cog in sorted(self.bot.cogs):
                    cog_commands = sorted(self.bot.get_cog(cog).get_commands(), key=lambda x:x.name)
                    for command in cog_commands:
                        if str(command.name) == invokercommand.lower() or invokercommand.lower() in command.aliases:
                            if command.hidden and ctx.author.id not in owners: continue
                            valid_commands += (command.name)
                            valid_help += (command.help)
                            if not command.brief:
                                command.brief = "None"
                            valid_brief += (command.brief)
                            valid_cog += (str(command.cog.qualified_name))

                if valid_commands != "":
                    help_embed = discord.Embed(title=f"Category: `{valid_cog.title()}`", 
                    description=f"**Bot Invite Link:** [https://ngc.discord.bot](https://discord.com/oauth2/authorize?client_id=810377376269205546&scope=bot&permissions=8)\n"
                                f"**Support Server:**  [https://discord.gg/ngc](https://discord.gg/947ramn)", 
                    color=default.config()["embed_color"])
                    help_embed.set_footer(text=f"Use \"{ctx.prefix}help command\" for information and usage examples on a command.")
                    help_embed.add_field(name=f"**Command Name:** `{valid_commands.title()}`", 
                    value=f"\n**Description:** `{valid_brief}`\n"
                          f"```yaml\n{valid_help}```")
                    await self.send_help(ctx, help_embed, pm, delete_after)
                else: 
                    await ctx.send(f":warning: No command named `{invokercommand}` found.")


            



        

            
