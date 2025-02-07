from utilities import utils

config = utils.config()
try:
    admins = config["admins"]
    bitly = config["bitly"]
    embed = config["embed"]
    gtoken = config["gtoken"]
    owners = config["owners"]
    postgres = config["postgres"]
    prefix = config["prefix"]
    support = config["support"]
    tester = config["tester"]
    timezonedb = config["timezonedb"]
    token = config["token"]
except KeyError as e:
    print(
        f"""
          Warning! The key {e} is missing from your ./config.json file.
          Add this key or the bot might not function properly.
          """
    )
avatars = {
    "red": "https://cdn.discordapp.com/attachments/846597178918436885/847339918216658984/red.png",
    "orange": "https://cdn.discordapp.com/attachments/846597178918436885/847342151238811648/orange.png",
    "yellow": "https://cdn.discordapp.com/attachments/846597178918436885/847341423945711637/yellow.png",
    "green": "https://cdn.discordapp.com/attachments/846597178918436885/847528287739314176/green.png",
    "blue": "https://cdn.discordapp.com/attachments/846597178918436885/847339750042239007/blue.png",
    "purple": "https://cdn.discordapp.com/attachments/846597178918436885/847340695823450117/purple.png",
    "black": "https://cdn.discordapp.com/attachments/846597178918436885/847339605555675176/black.png",
}
emotes = {
    "loading": "<a:loading:819280509007560756>",
    "success": "<:checkmark:816534984676081705>",
    "failed": "<:failed:816521503554273320>",
    "warn": "<:warn:816456396735905844>",
    "error": "<:error:836325837871382638>",
    "announce": "<:announce:834495346058067998>",
    "1234button": "<:1234:816460247777411092>",
    "info": "<:info:827428282001260544>",
    "exclamation": "<:exclamation:827753511395000351>",
    "trash": "<:trash:816463111958560819>",
    "forward": "<:forward:816458167835820093>",
    "forward2": "<:forward2:816457685905440850>",
    "backward": "<:backward:816458218145579049>",
    "backward2": "<:backward2:816457785167314987>",
    "desktop": "<:desktop:817160032391135262>",
    "mobile": "<:mobile:817160232248672256>",
    "search": "<:web:817163202877194301>",
    "online": "<:online:849961397654650930>",
    "offline": "<:offline:849961094989873192>",
    "dnd": "<:dnd:849960757943861248>",
    "idle": "<:idle:849960995458777138>",
    "owner": "<:owner:850175556866932787>",
    "emoji": "<:emoji:810678717482532874>",
    "members": "<:members:810677596453863444>",
    "categories": "<:categories:810671569440473119>",
    "textchannel": "<:textchannel:810659118045331517>",
    "voicechannel": "<:voicechannel:810659257296879684>",
    "messages": "<:messages:816696500314701874>",
    "commands": "<:command:816693906951372870>",
    "role": "<:role:816699853685522442>",
    "invite": "<:invite:816700067632513054>",
    "bot": "<:bot:816692223566544946>",
    "question": "<:question:817545998506393601>",
    "lock": "<:lock:817168229712527360>",
    "unlock": "<:unlock:817168258825846815>",
    "letter": "<:letter:816520981396193280>",
    "num0": "<:num0:827219939583721513>",
    "num1": "<:num1:827219939961602098>",
    "num2": "<:num2:827219940045226075>",
    "num3": "<:num3:827219940541071360>",
    "num4": "<:num4:827219940556931093>",
    "num5": "<:num5:827219941253709835>",
    "num6": "<:num6:827219941790580766>",
    "num7": "<:num7:827219942343442502>",
    "num8": "<:num8:827219942444236810>",
    "num9": "<:num9:827219942758809610>",
    "stop": "<:stop:827257105420910652>",
    "stopsign": "<:stopsign:841848010690658335>",
    "clock": "<:clock:839640961755643915>",
    "alarm": "<:alarm:839640804246683648>",
    "stopwatch": "<:stopwatch:827075158967189544>",
    "log": "<:log:835203679388303400>",
    "db": "<:database:839574200506646608>",
    "privacy": "<:privacy:839574405541134346>",
    "delete": "<:deletedata:839587782091735040>",
    "heart": "<:heart:839354647546298399>",
    "graph": "<:graph:840046538340040765>",
    "upload": "<:upload:840086768497983498>",
    "download": "<:download:840086726209961984>",
    "right": "<:right:840289355057725520>",
    "kick": "<:kick:840490315893702667>",  # So its a she 💞
    "ban": "<:ban:840474680547606548>",
    "robot": "<:robot:840482243218767892>",
    "plus": "<:plus:840485455333294080>",
    "minus": "<:minus:840485608555020308>",
    "undo": "<:undo:840486528110166056>",
    "redo": "<:redo:840486303354322962>",
    "audioadd": "<:audioadd:840491464928002048>",
    "audioremove": "<:audioremove:840491410720948235>",
    "pin": "<:pin:840492943226961941>",
    "pass": "<:pass:840817730277867541>",
    "fail": "<:fail:840817815148953600>",
    "snowflake": "<:snowflake:841848061412376596>",
    "dev": "<:botdev:850169506310389820>",
    "user": "<:user:850173056140050442>",
    "join": "<:join:850175242009313342>",
    "leave": "<:leave:850175275316019220>",
    "nitro": "<:nitro:850175331197124618>",
    "staff": "<:staff:850175717131681842>",
    "partner": "<:partner:850175829182251058>",
    "boost": "<:boost:850175958505357343>",
    "balance": "<:balance:850176108099665920>",
    "brilliance": "<:brilliance:850176212537835530>",
    "bravery": "<:bravery:850176483136766013>",
    "moderator": "<:moderator:850176521154330637>",
    "bughuntergold": "<:bughuntergold:850176871751614514>",
    "bughunter": "<:bughunter:850176820976549899>",
    "supporter": "<:supporter:850177686193438720>",
    "hypesquad": "<:hypesquad:850181797555208212>",
    "like": "<:like:854215293048193034>",
    "dislike": "<:dislike:854215235005841418>",
    "youtube": "<:youtube:854214998770057226>",
    "pause": "<:pause:854214661481431080>",
    "play": "<:play:854216311014031360>",
    "music": "<:music:854216986719813634>",
    "volume": "<:volume:854216882567905302>",
    "skip": "<:skip:854216673803763732>",
    "wave": "<:wave:854218904033296414>",
    "loop": "<:loop:854254549488107561>",
    "clarinet": "<:clarinet:854217207248977930>",  # For me :)
}
