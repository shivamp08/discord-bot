import os, shutil
from docx import Document
from discord import File
from discord.ext.commands import Cog
from discord.ext.commands import command


class Clgen(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @command()
    async def generate(self, ctx, *, message):
      await ctx.message.attachments[0].save("./src/cogs/in/in.docx", seek_begin=True, use_cached=False)
      tags = message.split("\n")

      folder = './src/cogs/out'
      for filename in os.listdir(folder):
          file_path = os.path.join(folder, filename)
          try:
              if os.path.isfile(file_path) or os.path.islink(file_path):
                  os.unlink(file_path)
              elif os.path.isdir(file_path):
                  shutil.rmtree(file_path)
          except Exception as e:
              print('Failed to delete %s. Reason: %s' % (file_path, e))

      document = Document('./src/cogs/in/in.docx')
      
      for i in document.paragraphs:
        for tag in tags[1:]:
          pair = tag.split("=")
          if pair[0] in i.text:
            inline = i.runs
            for x in range(len(inline)):
                if pair[0] in inline[x].text:
                        inline[x].text = inline[x].text.replace(pair[0], pair[1])

      document.save("./src/cogs/out/edited.docx")
      await ctx.send(file= File(r'./src/cogs/out/edited.docx'))


    @Cog.listener()
    async def on_ready(self):
        print("Clgen is ready!")
    

def setup(bot):
	bot.add_cog(Clgen(bot))
