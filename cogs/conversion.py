import io
import re
import base64
import codecs
import discord
import binascii

from discord.ext import commands

from utilities import utils
from utilities import decorators


def setup(bot):
    bot.add_cog(Conversion(bot))


class Conversion(commands.Cog):
    """
    Module for unit conversions.
    """

    def __init__(self, bot):
        self.bot = bot
        self.regex = re.compile(
            r"(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?"
        )

        self.to_morse = {
            "a": ".-",
            "b": "-...",
            "c": "-.-.",
            "d": "-..",
            "e": ".",
            "f": "..-.",
            "g": "--.",
            "h": "....",
            "i": "..",
            "j": ".---",
            "k": "-.-",
            "l": ".-..",
            "m": "--",
            "n": "-.",
            "o": "---",
            "p": ".--.",
            "q": "--.-",
            "r": ".-.",
            "s": "...",
            "t": "-",
            "u": "..-",
            "v": "...-",
            "w": ".--",
            "x": "-..-",
            "y": "-.--",
            "z": "--..",
            "1": ".----",
            "2": "..---",
            "3": "...--",
            "4": "....-",
            "5": ".....",
            "6": "-....",
            "7": "--...",
            "8": "---..",
            "9": "----.",
            "0": "-----",
        }

    @decorators.command(
        brief="Convert pounds to kilograms", aliases=["lbs", "pounds", "pound"]
    )
    async def lb(self, ctx, lbs: float):
        """
        Usage: {0}lb <value>
        Aliases: {0}lbs, pounds, pound
        Output: Turn lb into kg (imperial to metric)
        """
        await ctx.send_or_reply(
            content="That is {0:.2f} kg".format(lbs * 0.453592),
        )

    @decorators.command(
        brief="Convert kilograms to pounds.", aliases=["kgs", "kilograms", "kilogram"]
    )
    async def kg(self, ctx, kg: float):
        """
        Usage: {0}kg <value>
        Alias: {0}kgs, kilograms
        Output: Turn kg into lb (metric to imperial)
        """
        await ctx.send_or_reply("That is {0:.2f} lbs".format(kg * 2.20462))

    @decorators.command(brief="Convert feet.inches to centimeters", aliases=["feet"])
    async def ft(self, ctx):
        """
        Usage: {0}ft <value>
        Alias: {0}feet
        Output:
            Turns height ft.inch (Eg: 5.11)
            to cm (imperial to metric)
        """
        value = float(ctx.message.content.split()[1])
        lb = int(value)
        inch = (value - int(value)) * 10
        cm = lb * 30.48 + inch * 2.54
        await ctx.send_or_reply("{0:.2f} cm".format(cm))

    @decorators.command(brief="Convert centimeters to feet and inches.")
    async def cm(self, ctx):
        """
        Usage: {0}cm
        Alias: {0}centimeters
        Output:
            Turns cm (height) to ft + inch
            (metric to imperial) by approximation
        """
        value = float(ctx.message.content.split()[1])
        ft = int(value * 0.0328084)
        inch = round((value * 0.0328084 - ft) * 12)
        await ctx.send_or_reply("That is {}ft {}inches".format(ft, inch))

    # Helper methods
    def _to_bytes(self, in_string):
        return in_string.encode("utf-8")

    def _to_string(self, in_bytes):
        return in_bytes.decode("utf-8")

    # Check hex value
    def _check_hex(self, hex_string):
        # Remove 0x/0X
        hex_string = hex_string.replace("0x", "").replace("0X", "")
        hex_string = re.sub(r"[^0-9A-Fa-f]+", "", hex_string)
        return hex_string

    # To base64 methods
    def _ascii_to_base64(self, ascii_string):
        ascii_bytes = self._to_bytes(ascii_string)
        base_64 = base64.b64encode(ascii_bytes)
        return self._to_string(base_64)

    def _hex_to_base64(self, hex_string):
        hex_string = self._check_hex(hex_string)
        hex_s_bytes = self._to_bytes(hex_string)
        hex_bytes = binascii.unhexlify(hex_s_bytes)
        base64_bytes = base64.b64encode(hex_bytes)
        return self._to_string(base64_bytes)

    # To ascii methods
    def _hex_to_ascii(self, hex_string):
        hex_string = self._check_hex(hex_string)
        hex_bytes = self._to_bytes(hex_string)
        ascii_bytes = binascii.unhexlify(hex_bytes)
        return self._to_string(ascii_bytes)

    def _base64_to_ascii(self, base64_string):
        base64_bytes = self._to_bytes(base64_string)
        ascii_bytes = base64.b64decode(base64_bytes)
        return self._to_string(ascii_bytes)

    # To hex methods
    def _ascii_to_hex(self, ascii_string):
        ascii_bytes = self._to_bytes(ascii_string)
        hex_bytes = binascii.hexlify(ascii_bytes)
        return self._to_string(hex_bytes)

    def _base64_to_hex(self, base64_string):
        b64_string = self._to_bytes(base64_string)
        base64_bytes = base64.b64decode(b64_string)
        hex_bytes = binascii.hexlify(base64_bytes)
        return self._to_string(hex_bytes)

    def _rgb_to_hex(self, r, g, b):
        return "#{:02x}{:02x}{:02x}".format(r, g, b).upper()

    def _hex_to_rgb(self, _hex):
        _hex = _hex.lower().replace("#", "").replace("0x", "")
        l_hex = len(_hex)
        return tuple(
            int(_hex[i : i + l_hex // 3], 16) for i in range(0, l_hex, l_hex // 3)
        )

    def _hex_to_cmyk(self, _hex):
        return self._rgb_to_cmyk(*self._hex_to_rgb(_hex))

    def _cmyk_to_hex(self, c, m, y, k):
        return self._rgb_to_hex(*self._cmyk_to_rgb(c, m, y, k))

    def _cmyk_to_rgb(self, c, m, y, k):
        c, m, y, k = [float(x) / 100.0 for x in tuple([c, m, y, k])]
        return tuple(
            [
                round(255.0 - ((min(1.0, x * (1.0 - k) + k)) * 255.0))
                for x in tuple([c, m, y])
            ]
        )

    def _rgb_to_cmyk(self, r, g, b):
        c, m, y = [1 - x / 255 for x in tuple([r, g, b])]
        min_cmy = min(c, m, y)
        return (
            tuple([0, 0, 0, 100])
            if all(x == 0 for x in [r, g, b])
            else tuple(
                [
                    round(x * 100)
                    for x in [(x - min_cmy) / (1 - min_cmy) for x in tuple([c, m, y])]
                    + [min_cmy]
                ]
            )
        )

    def _hex_int_to_tuple(self, _hex):
        return (_hex >> 16 & 0xFF, _hex >> 8 & 0xFF, _hex & 0xFF)

    @decorators.command(brief="Convert hex to decimal.")
    async def hexdec(self, ctx, *, input_hex=None):
        """
        Usage: {0}hexdec <hex>
        """
        if input_hex == None:
            await ctx.send_or_reply(
                content="Usage: `{}hexdec [input_hex]`".format(ctx.prefix),
            )
            return

        input_hex = self._check_hex(input_hex)
        if not len(input_hex):
            await ctx.fail("Malformed hex - try again.")
            return

        try:
            dec = int(input_hex, 16)
        except Exception:
            await ctx.fail("I couldn't make that conversion!")
            return

        await ctx.send_or_reply(dec)

    @decorators.command(brief="Convert decimal into hex.")
    async def dechex(self, ctx, *, input_dec: int):
        """
        Usage: {0}dechex <hex>
        """
        hex_str = "{:x}".format(input_dec).upper()
        hex_str = "0" * (len(hex_str) % 2) + hex_str
        await ctx.send_or_reply("#" + hex_str)

    @decorators.command(brief="Convert a string to binary.")
    async def strbin(self, ctx, *, input_string: str):
        """
        Usage: {0}strbin <string>
        Output:
            Converts the input string to its binary representation.
        """
        msg = "".join("{:08b}".format(ord(c)) for c in input_string)
        # Format into blocks:
        # - First split into chunks of 8
        msg_list = re.findall("........?", msg)
        # Now we format!
        msg = "```fix\n"
        msg += " ".join(msg_list)
        msg += "```"
        await ctx.send_or_reply(msg)

    @decorators.command(brief="Convert binary to a string")
    async def binstr(self, ctx, *, input_binary: str):
        """
        Usage: {0}binstr <binary>
        Output:
            Converts the input binary to its string representation.
        """
        # Clean the string
        new_bin = ""
        for char in input_binary:
            if char == "0" or char == "1":
                new_bin += char
        if not len(new_bin):
            return await ctx.usage()
        msg = "".join(
            chr(int(new_bin[i : i + 8], 2)) for i in range(0, len(new_bin), 8)
        )
        await ctx.send_or_reply(msg)

    @decorators.command(brief="Convert binary to an integer.")
    async def binint(self, ctx, *, input_binary=None):
        """
        Usage: {0}binint <binary>
        Output:
            Converts the input binary to its integer representation.
        """
        if input_binary == None:
            await ctx.send_or_reply(
                content="Usage: `{}binint [input_binary]`".format(ctx.prefix),
            )
            return
        try:
            msg = int(input_binary, 2)
        except Exception:
            msg = "I couldn't make that conversion!"
        await ctx.send_or_reply(msg)

    @decorators.command(brief="Convert an integer to binary.")
    async def intbin(self, ctx, *, input_int: int):
        """
        Usage: {0}intbin <integer>
        Output:
            Converts the input integer to its binary representation."""
        await ctx.send_or_reply("{:08b}".format(input_int))

    @decorators.group(brief="Encode to: b32, b64, b85, rot13, hex.")
    async def encode(self, ctx):
        """
        Usage: {0}encode <method>
        Methods:
            b32
            b64
            b85
            rot13
            hex
        """
        if ctx.invoked_subcommand is None:
            await ctx.send_help(str(ctx.command))

    @decorators.group(brief="Decode from b32, b64, b85, rot13, hex.")
    async def decode(self, ctx):
        """
        Usage: {0}decode <method>
        Methods:
            b32
            b64
            b85
            rot13
            hex
        """
        if ctx.invoked_subcommand is None:
            await ctx.send_help(str(ctx.command))

    async def detect_file(self, ctx):
        """ Detect if user uploaded a file to convert longer text """
        if ctx.message.attachments:
            file = ctx.message.attachments[0].url

            if not file.endswith(".txt"):
                raise commands.BadArgument(".txt files only")

        try:
            content = await self.bot.get(file, no_cache=True)
        except Exception:
            raise commands.BadArgument("Invalid .txt file")

        if not content:
            raise commands.BadArgument("File you've provided is empty")
        return content

    async def encryptout(self, ctx, convert: str, input):
        """ The main, modular function to control encrypt/decrypt commands """
        if not input:
            return await ctx.usage()

        async with ctx.channel.typing():
            if len(input) > 1900:
                try:
                    data = io.BytesIO(input.encode("utf-8"))
                except AttributeError:
                    data = io.BytesIO(input)

                try:
                    return await ctx.send_or_reply(
                        content=f"{self.bot.emote_dict['log']} **{convert}**",
                        file=discord.File(data, filename=utils.timetext("Encryption")),
                    )
                except discord.HTTPException:
                    return await ctx.send_or_reply(
                        content=f"The file I returned was over 8 MB, sorry {ctx.author.name}...",
                    )

            try:
                await ctx.send_or_reply(
                    content=f"{self.bot.emote_dict['log']} **{convert}**```fix\n{input.decode('UTF-8')}```",
                )
            except AttributeError:
                await ctx.send_or_reply(
                    content=f"{self.bot.emote_dict['log']} **{convert}**```fix\n{input}```",
                )

    @encode.command(name="base32", aliases=["b32"])
    async def encode_base32(self, ctx, *, input: commands.clean_content = None):
        """ Encode in base32 """
        if not input:
            input = await self.detect_file(ctx)

        await self.encryptout(
            ctx, "Text -> base32", base64.b32encode(input.encode("UTF-8"))
        )

    @decode.command(name="base32", aliases=["b32"])
    async def decode_base32(self, ctx, *, input: commands.clean_content = None):
        """ Decode in base32 """
        if not input:
            input = await self.detect_file(ctx)

        try:
            await self.encryptout(
                ctx, "base32 -> Text", base64.b32decode(input.encode("UTF-8"))
            )
        except Exception:
            await ctx.send_or_reply(content="Invalid base32...")

    @encode.command(name="base64", aliases=["b64"])
    async def encode_base64(self, ctx, *, input: commands.clean_content = None):
        """ Encode in base64 """
        if not input:
            input = await self.detect_file(ctx)

        await self.encryptout(
            ctx, "Text -> base64", base64.urlsafe_b64encode(input.encode("UTF-8"))
        )

    @decode.command(name="base64", aliases=["b64"])
    async def decode_base64(self, ctx, *, input: commands.clean_content = None):
        """ Decode in base64 """
        if not input:
            input = await self.detect_file(ctx)

        try:
            await self.encryptout(
                ctx, "base64 -> Text", base64.urlsafe_b64decode(input.encode("UTF-8"))
            )
        except Exception:
            await ctx.fail("Invalid base64.")

    @encode.command(name="rot13", aliases=["r13"])
    async def encode_rot13(self, ctx, *, input: commands.clean_content = None):
        """ Encode in rot13 """
        if not input:
            input = await self.detect_file(ctx)

        await self.encryptout(ctx, "Text -> rot13", codecs.decode(input, "rot_13"))

    @decode.command(name="rot13", aliases=["r13"])
    async def decode_rot13(self, ctx, *, input: commands.clean_content = None):
        """ Decode in rot13 """
        if not input:
            input = await self.detect_file(ctx)

        try:
            await self.encryptout(ctx, "rot13 -> Text", codecs.decode(input, "rot_13"))
        except Exception:
            await ctx.send_or_reply(content="Invalid rot13...")

    @encode.command(name="hex")
    async def encode_hex(self, ctx, *, input: commands.clean_content = None):
        """ Encode in hex """
        if not input:
            input = await self.detect_file(ctx)

        await self.encryptout(
            ctx, "Text -> hex", binascii.hexlify(input.encode("UTF-8"))
        )

    @decode.command(name="hex")
    async def decode_hex(self, ctx, *, input: commands.clean_content = None):
        """ Decode in hex """
        if not input:
            input = await self.detect_file(ctx)

        try:
            await self.encryptout(
                ctx, "hex -> Text", binascii.unhexlify(input.encode("UTF-8"))
            )
        except Exception:
            await ctx.send_or_reply(content="Invalid hex...")

    @encode.command(name="base85", aliases=["b85"])
    async def encode_base85(self, ctx, *, input: commands.clean_content = None):
        """ Encode in base85 """
        if not input:
            input = await self.detect_file(ctx)

        await self.encryptout(
            ctx, "Text -> base85", base64.b85encode(input.encode("UTF-8"))
        )

    @decode.command(name="base85", aliases=["b85"])
    async def decode_base85(self, ctx, *, input: commands.clean_content = None):
        """ Decode in base85 """
        if not input:
            input = await self.detect_file(ctx)

        try:
            await self.encryptout(
                ctx, "base85 -> Text", base64.b85decode(input.encode("UTF-8"))
            )
        except Exception:
            await ctx.send_or_reply(content="Invalid base85...")

    @encode.command(name="ascii85", aliases=["a85"])
    async def encode_ascii85(self, ctx, *, input: commands.clean_content = None):
        """ Encode in ASCII85 """
        if not input:
            input = await self.detect_file(ctx)

        await self.encryptout(
            ctx, "Text -> ASCII85", base64.a85encode(input.encode("UTF-8"))
        )

    @decode.command(name="ascii85", aliases=["a85"])
    async def decode_ascii85(self, ctx, *, input: commands.clean_content = None):
        """ Decode in ASCII85 """
        if not input:
            input = await self.detect_file(ctx)

        try:
            await self.encryptout(
                ctx, "ASCII85 -> Text", base64.a85decode(input.encode("UTF-8"))
            )
        except Exception:
            await ctx.send_or_reply(content="Invalid ASCII85...")

    @decorators.command(brief="Show the morse lookup table")
    async def morsetable(self, ctx, num_per_row=None):
        """
        Usage: {0}morsetable
        Output:
            Prints out the morse code lookup table.
        """
        try:
            num_per_row = int(num_per_row)
        except Exception:
            num_per_row = 5

        msg = "__**Morse Code Lookup Table:**__\n```fix\n"
        max_length = 0
        current_row = 0
        row_list = [[]]
        cur_list = []
        sorted_list = sorted(self.to_morse)
        for key in sorted_list:
            entry = "{} : {}".format(key.upper(), self.to_morse[key])
            if len(entry) > max_length:
                max_length = len(entry)
            row_list[len(row_list) - 1].append(entry)
            if len(row_list[len(row_list) - 1]) >= num_per_row:
                row_list.append([])
                current_row += 1

        for row in row_list:
            for entry in row:
                entry = entry.ljust(max_length)
                msg += entry + "  "
            msg += "\n"

        msg += "```"
        await ctx.send_or_reply(msg)

    @decorators.command(brief="Converts ascii to morse code.")
    async def morse(self, ctx, *, content):
        """
        Usage: {0}morse <content>
        Output: Converts ascii to morse code.
        Notes:
            Accepts a-z and 0-9.
            Each letter is comprised of "-" or "."
            and separated by 1 space.
            Each word is separated by 4 spaces.
        """
        # Only accept alpha numeric stuff and spaces
        word_list = content.split()
        morse_list = []
        for word in word_list:
            # Iterate through words
            letter_list = []
            for letter in word:
                # Iterate through each letter of each word
                if letter.lower() in self.to_morse:
                    # It's in our list - add the morse equivalent
                    letter_list.append(self.to_morse[letter.lower()])
            if len(letter_list):
                # We have letters - join them into morse words
                # each separated by a space
                morse_list.append(" ".join(letter_list))

        if not len(morse_list):
            # We didn't get any valid words
            await ctx.send_or_reply(
                content="There were no valid a-z/0-9 chars in the passed content.",
            )
            return

        # We got *something*
        msg = "    ".join(morse_list)
        msg = "```fix\n" + msg + "```"
        await ctx.send_or_reply(msg)

    @decorators.command(brief="Converts morse code to ascii.")
    async def unmorse(self, ctx, *, content):
        """
        Usage: {0}unmorse <morse>
        Output: Converts morse code to ascii.
        Notes:
            Each letter is comprised of "-" or "."
            and separated by 1 space.
            Each word is separated by 4 spaces.
        """
        # Only accept morse symbols
        content = "".join([x for x in content if x in " .-"])
        word_list = content.split("    ")
        ascii_list = []
        for word in word_list:
            # Split by space for letters
            letter_list = word.split()
            letter_ascii = []
            # Iterate through letters
            for letter in letter_list:
                for key in self.to_morse:
                    if self.to_morse[key] == letter:
                        # Found one
                        letter_ascii.append(key.upper())
            if len(letter_ascii):
                # We have letters - join them into ascii words
                ascii_list.append("".join(letter_ascii))

        if not len(ascii_list):
            # We didn't get any valid words
            await ctx.send_or_reply(
                content="There were no valid morse chars in the passed content.",
            )
            return

        # We got *something* - join separated by a space
        msg = " ".join(ascii_list)
        msg = "```fix\n" + msg + "```"
        await ctx.send_or_reply(msg)

    @decorators.command(
        aliases=["tconvert", "temperature"],
        brief="Convert between units of temperature.",
        implemented="",
        updated="",
        examples="""
                {0}temp 20 Kelvin Fahrenheit
                {0}temperatur 200 Fahrenheit Celsius
                {0}tconvert -40 C K
                """
    )
    async def temp(self, ctx, *, temp_value, from_unit=None, to_unit=None):
        """
        Usage: {0}temp [temp_value] [from unit] [to unit]
        Aliases: {0}temperature, {0}tconvert
        Output: Converts between Fahrenheit, Celsius, and Kelvin.
        Units:
            (F)ahrenheit
            (C)elsius
            (K)elvin
        """
        
        types = [ "Fahrenheit", "Celsius", "Kelvin"]

        args = temp_value.split()
        if not len(args) == 3:
            return await ctx.usage()
        try:
            f = next((x for x in types if x.lower() == args[1].lower() or x.lower()[:1] == args[1][:1].lower()), None)
            t = next((x for x in types if x.lower() == args[2].lower() or x.lower()[:1] == args[2][:1].lower()), None)
            m = int(args[0])
        except Exception:
            return await ctx.usage()
        if not(f) or not(t):
            # No valid types
            await ctx.fail("Temperature units are: {}".format(", ".join(types)))
            return
        if f == t:
            # Same in as out
            await ctx.fail("No change when converting {} ➔ {}.".format(f, t))
            return
        try:
            out_val = None
            if f == "Fahrenheit":
                if t == "Celsius":
                    out_val = self._f_to_c(m)
                else:
                    out_val = self._f_to_k(m)
            elif f == "Celsius":
                if t == "Fahrenheit":
                    out_val = self._c_to_f(m)
                else:
                    out_val = self._c_to_k(m)
            else:
                if t == "Celsius":
                    out_val = self._k_to_c(m)
                else:
                    out_val = self._k_to_f(m)
            output = "{:,} {} {} is {:,} {} {}".format(m, "degree" if (m==1 or m==-1) else "degrees", f, out_val, "degree" if (out_val==1 or out_val==-1) else "degrees", t)
        except Exception:
            return await ctx.fail("Failed to make that conversion")
        await ctx.success(output)

    def _f_to_c(self, f):
        return int((int(f)-32)/1.8)
    def _c_to_f(self, c):
        return int((int(c)*1.8)+32)
    def _c_to_k(self, c):
        return int(int(c)+273)
    def _k_to_c(self, k):
        return int(int(k)-273)
    def _f_to_k(self, f):
        return self._c_to_k(self._f_to_c(int(f)))
    def _k_to_f(self, k):
        return self._c_to_f(self._k_to_c(int(k)))