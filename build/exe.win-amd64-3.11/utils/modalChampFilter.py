import customtkinter
from tkinter import ttk
import os
from PIL import Image

championsList = ["All", "Aatrox", "Ahri", "Akali", "Akshan", "Alistar", "Amumu", "Anivia", "Annie", "Aphelios", "Ashe", "AurelionSol", "Azir", "Bard", "Belveth", "Blitzcrank", "Brand", "Braum", "Caitlyn", "Camille", "Cassiopeia", "Chogath", "Corki", "Darius", "Diana", "Draven", "DrMundo", "Ekko", "Elise", "Evelynn", "Ezreal", "Fiddlesticks", "Fiora", "Fizz", "Galio", "Gangplank", "Garen", "Gnar", "Gragas", "Graves", "Gwen", "Hecarim", "Heimerdinger", "Illaoi", "Irelia", "Ivern", "Janna", "JarvanIV", "Jax", "Jayce", "Jhin", "Jinx", "Kaisa", "Kalista", "Karma", "Karthus", "Kassadin", "Katarina", "Kayle", "Kayn", "Kennen", "Khazix", "Kindred", "Kled", "KogMaw", "KSante", "Leblanc", "LeeSin", "Leona", "Lillia", "Lissandra", "Lucian", "Lulu", "Lux", "Malphite", "Malzahar", "Maokai", "MasterYi", "MissFortune", "MonkeyKing", "Mordekaiser", "Morgana", "Nami", "Nasus", "Nautilus", "Neeko", "Nidalee", "Nilah", "Nocturne", "Nunu", "Olaf", "Orianna", "Ornn", "Pantheon", "Poppy", "Pyke", "Qiyana", "Quinn", "Rakan", "Rammus", "RekSai", "Rell", "Renata", "Renekton", "Rengar", "Riven", "Rumble", "Ryze", "Samira", "Sejuani", "Senna", "Seraphine", "Sett", "Shaco", "Shen", "Shyvana", "Singed", "Sion", "Sivir", "Skarner", "Sona", "Soraka", "Swain", "Sylas", "Syndra", "TahmKench", "Taliyah", "Talon", "Taric", "Teemo", "Thresh", "Tristana", "Trundle", "Tryndamere", "TwistedFate", "Twitch", "Udyr", "Urgot", "Varus", "Vayne", "Veigar", "Velkoz", "Vex", "Vi", "Viego", "Viktor", "Vladimir", "Volibear", "Warwick", "Xayah", "Xerath", "XinZhao", "Yasuo", "Yone", "Yorick", "Yuumi", "Zac", "Zed", "Zeri", "Ziggs", "Zilean", "Zoe", "Zyra"]

class SelectChampionsFilter(customtkinter.CTkToplevel):
    def __init__(self, parent, champForSummoner:list):
        super().__init__(parent)
        # Window parameters
        screenX = int(self.winfo_screenwidth())
        screenY = int(self.winfo_screenheight())
        windowX = 400
        windowY = 400
        posX = (screenX // 2) - (windowX // 2)
        posY = (screenY // 2) - (windowY // 2)
        geometry = "{}x{}+{}+{}".format(windowX, windowY, posX, posY)
        self.geometry(geometry)
        self.title("Champions filter")

        # Store the champions selected
        self.championsForSummoner = champForSummoner
        self.championsButtons = {}
        self.championsCounter = 0
        self.row = 3
        self.column = 0

        self.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        # Button to clear all the champions
        self.removeAllChampionsButton = customtkinter.CTkButton(self, text="Clear all", width=50, command=self.removeAllChampions)
        self.removeAllChampionsButton.grid(row=0, column=0, columnspan=5, padx=10, pady=12, sticky="w")

        # Create a Combobox with the list of LoL champions
        self.championsComboBox = ttk.Combobox(self, value=championsList)
        self.championsComboBox.grid(row=0, column=0, columnspan=5, padx=10, pady=12)
        # Set initial value to "All"
        self.championsComboBox.set("All")
        # Call the function for autocomplete each time we press a key of the keyboard
        self.championsComboBox.bind("<KeyRelease>", self.searchChampionOnKeyRelease)

        # The button that checks, add and show the champion that user wants to filter
        self.addChampionButton = customtkinter.CTkButton(self, text="Add Champion", command=self.addChampion)
        self.addChampionButton.grid(row=1, column=0, columnspan=5, padx=10, pady=12)
        self.bind("<Return>", self.addChampion)

        # Error message if needed
        self.errorMessage = customtkinter.CTkLabel(self, text_color="red", text="", font=("Roboto", 16), wraplength=375)
        self.errorMessage.grid(row=2, column=0, columnspan=5, padx=10, pady=12)

        # Styles for the combo box
        self.option_add('*TCombobox*Listbox*Background', "#333333")
        self.option_add('*TCombobox*Listbox*Foreground', "#FFFFFF")
        self.option_add('*TCombobox*Listbox*selectBackground', "#FFFFFF")
        self.option_add('*TCombobox*Listbox*selectForeground', "#333333")

        # if the array already contains champs
        if (len(self.championsForSummoner)!=0):
          # Path of the images of the champions
          championsPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../media/lol_champions")
          for i in range(len(self.championsForSummoner)):
            # Get the good image
            championImage = customtkinter.CTkImage(Image.open(os.path.join(championsPath, self.championsForSummoner[i] + ".png")), size=(50, 50))
            # Each 5 champions added, go to next row and reset the column counter to 0
            if (self.championsCounter % 5 == 0 and self.championsCounter != 0):
              self.row = self.row + 1
              self.column = 0

            # Show the image and delete on click on it
            self.championsButtons[self.championsCounter] = [customtkinter.CTkButton(self, text="", width=50, fg_color="transparent", image=championImage, command=lambda championName=self.championsForSummoner[i],j=self.championsCounter: self.deleteChampion(championName)), self.championsForSummoner[i]]
            self.championsButtons[self.championsCounter][0].grid(row = self.row, column = self.column)

            self.column = self.column + 1
            self.championsCounter = self.championsCounter + 1

    # Autocompletion of the ComboBox
    def searchChampionOnKeyRelease(self, event):
      inputValue = event.widget.get()
      # If the input is empty, show again all the champions
      if inputValue == '':
          self.championsComboBox['values'] = championsList
      # Otherwise, show the champions corresponding to the input in the Combobox
      else:
          newComboboxData = []
          # Loop through the champions list and check if our input corresponds to what's in the champions list
          for item in championsList:
              # we put every char in lower case + we don't take account of white spaces and ' char
              if inputValue.lower().replace(" ", "").replace("'", "") in item.lower():
                  newComboboxData.append(item)
              if inputValue.lower().replace(" ","").replace("'","")=="wukong":
                if item == "MonkeyKing":
                  newComboboxData.append(item)
              # Update the Combobox to only show results that corresponds
              self.championsComboBox['values'] = newComboboxData

    # Show the image of the champion validated for the filter
    def addChampion(self, event = None):
        # Get the selected value
        selectedChampion = self.championsComboBox.get()
        # we remove white spaces (aurelion sol, tahm kench)
        selectedChampion = selectedChampion.replace(" ", "")
        # in case of void champs with ' chars, we remove '
        selectedChampion = selectedChampion.replace("'", "")

        # to ignore case sensitive cases
        # for e.g : renekton, Renekton, reNEKtoN must strictly match Renekton
        # we loop through the list of champions
        for i in range(len(championsList)):
          # there will be a change of selectedChampion value
          # (to match any of the champion names in list of champions (upper, lower cases etc.)
          # only if string length of selectedChampion is equals to at least one of the champions in list
          if len(championsList[i])==len(selectedChampion):
            # and if correctChamp stays true
            # correctChamp is a boolean initialized at true for each champion (assumption)
            correctChamp=True
            # if boolean stays correct for the entire comparison of each char (each char lowered to compare),
            # then selectedChamp takes the EXACT value of the champion name in championsList
            for j in range(len(championsList[i])):
              # if one of the lowered characters does not match the other, it means that it's not the correct champ
              # so we exit the loop to go to the next champ in championsList
              if(championsList[i][j].lower()!=selectedChampion[j].lower()):
                correctChamp=False
                break
            # each character of the string were checked or premature exit due to an error in the matching of a character
            # so if correctChamp stayed true, then selectedChampion takes the exact value of the champion from championList
            # (every lower, upper cases are applied)
            if correctChamp :
              selectedChampion=championsList[i]
              # no need to go further in championList, so we exit the loop
              break

        if selectedChampion.lower().replace(" ","").replace("'","")=="wukong":
          selectedChampion="MonkeyKing"

        # If nothing is entered
        if (selectedChampion == ""):
          self.errorMessage.configure(text="Error. Please enter a champion to add.", text_color="red")
          return

        # If the value returned isn't a valid champion, stop
        if (not selectedChampion in championsList):
          self.errorMessage.configure(text="Error. " + selectedChampion + " doesn't exist.", text_color="red")
          return
        # If we selected "All" or selected a champion that's already in the array, don't need to show images and add to the array
        if (selectedChampion == "All"):
          self.errorMessage.configure(text="Error. All champions are selected by default, don't need to add All.", text_color="red")
          # Clear the combobox value
          self.championsComboBox.set("")
          return

        # If we selected a champion that's already in the array, don't need to show images and add to the array
        if (selectedChampion in self.championsForSummoner):
          self.errorMessage.configure(text="Error. " + selectedChampion + " is already added.", text_color="red")
          # Clear the combobox value
          self.championsComboBox.set("")
          return

        # Add the champion to the array
        self.championsForSummoner.append(selectedChampion)
        self.errorMessage.configure(text=selectedChampion + " has been added.", text_color="green")
        # Clear the combobox value
        self.championsComboBox.set("")
        # Path of the images of the champions
        championsPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../media/lol_champions")
        # Get the good image
        championImage = customtkinter.CTkImage(Image.open(os.path.join(championsPath, selectedChampion + ".png")), size=(50, 50))

        # Each 5 champions added, go to next row and reset the column counter to 0
        if (self.championsCounter % 5 == 0 and self.championsCounter != 0):
          self.row = self.row + 1
          self.column = 0

        # Show the image and delete on click on it
        self.championsButtons[self.championsCounter] = [customtkinter.CTkButton(self, text="", width=50, fg_color="transparent", image=championImage, command=lambda i=self.championsCounter: self.deleteChampion(selectedChampion)), selectedChampion]
        self.championsButtons[self.championsCounter][0].grid(row = self.row, column = self.column)

        self.column = self.column + 1
        self.championsCounter = self.championsCounter + 1

    # Delete the champion when clicking on the corresponding picture
    def deleteChampion(self, champion):
      # Delete the champion from the array
      self.championsForSummoner.remove(champion)
      self.errorMessage.configure(text=champion + " has been deleted.", text_color="green")

      # Delete every image from the canvas to redraw them in the good order
      for i in range(len(self.championsButtons)):
        self.championsButtons[i][0].destroy()
        self.championsButtons.pop(i)

      # Reset the counters to draw the images
      self.championsCounter = 0
      self.row = 3
      self.column = 0
      # Path of the images of the champions
      championsPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../media/lol_champions")

      # Loop through all champions in the array
      for i in range(len(self.championsForSummoner)):
        # Get the good image
        championImage = customtkinter.CTkImage(Image.open(os.path.join(championsPath, self.championsForSummoner[i] + ".png")), size=(50, 50))
        # Each 5 champions added, go to next row and reset the column counter to 0
        if (self.championsCounter % 5 == 0 and self.championsCounter != 0):
          self.row = self.row + 1
          self.column = 0

        # Show the image and delete on click on it
        self.championsButtons[self.championsCounter] = [customtkinter.CTkButton(self, text="", width=50, fg_color="transparent", image=championImage, command=lambda i=self.championsCounter: self.deleteChampion(self.championsForSummoner[i])), self.championsForSummoner[i]]
        self.championsButtons[self.championsCounter][0].grid(row = self.row, column = self.column)

        self.column = self.column + 1
        self.championsCounter = self.championsCounter + 1


    def removeAllChampions(self):
      # Reset the counters to draw the next images
      self.championsCounter = 0
      self.row = 3
      self.column = 0

      # If we clear at least one champion, show the message to the user
      if len(self.championsButtons) != 0:
        self.errorMessage.configure(text="Champions filter has been cleared.", text_color="green")
      else:
        self.errorMessage.configure(text="")

      # Clear the array
      self.championsForSummoner.clear()
      # Delete every image from the canvas to redraw them in the good order
      for i in range(len(self.championsButtons)):
        self.championsButtons[i][0].destroy()
        self.championsButtons.pop(i)