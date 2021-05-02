import os, glob, json, requests, time
from discord import File
from discord.ext.commands import Cog
from discord.ext.commands import command


class Parser(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @command()
    async def parse(self, ctx):
      await ctx.message.attachments[0].save("in.pdf", seek_begin=True, use_cached=False)
      resume_file  = glob.glob('in.pdf')[0]
      url = 'https://jobs.lever.co/parseResume'
      resume = open(resume_file, 'rb')
      resume_file_path = os.path.splitext(resume_file)[0] + '.json'
      response = requests.post(url, files={'resume': resume}, headers={'referer': 'https://jobs.lever.co/', 'origin': 'https://jobs.lever.co/'}, cookies={'lever-referer': 'https://jobs.lever.co/'})
      parsed_resume = json.loads(response.json(), indent=4)
    
      get_all_values(parsed_resume)
 
    @Cog.listener()
    async def on_ready(self):
        print("parser is ready!")
    
def get_all_values(nested_dictionary):
    str =""
    for key, value in nested_dictionary.items():
        if type(value) is dict:
            get_all_values(value)
        elif key == "names":
            str = str + key, ":", value[0]
        elif type(value) is list:
            print(key, "---:")
            get_all_values(value[0])

        else:
            print(key, ":", value)



def setup(bot):
	bot.add_cog(Parser(bot))
