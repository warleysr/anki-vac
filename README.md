# Anki-VAC

<img src="https://i.imgur.com/jxPSxue.png" width="250px" align="right"/>

VAC stands for Vocabulary Acquisition. The main purpose of this software is to automate the creation of Anki Flashcards for constant vocabulary acquisition.

### Features
- Get word definition and example phrases
- Generate TTS audio
- Get related image

### How it works
Anki-VAC uses WiktionaryParser to get the definition and example phrases from <a href="https://wiktionary.org">wiktionary.org</a> and add this into your cards. You don't need an API key for that.

But you will need some if you want to enhance your cards with audio or images, for that it uses Azure Services. You can create an free account by clicking <a href="https://azure.microsoft.com/en-in/free/">here</a>.

To get your keys login into Azure portal and create a **Speech service** if you want TTS audios and a **Bing Resource** if you want to add images. You will get also the endpoints URL's on the same place.

You will need to install <a href="https://ankiweb.net/shared/info/2055492159">AnkiConnect</a> addon into your Anki. This addon creates an local API for managing flashcards.

Having everything properly configured you can input a list of words that you don't know and one flashcard will be created for each. It can take some time depending on how much words you want to add in a row as much data need to be collected.

### How to use
Anki-VAC have a very straightforward graphical interface. You can configure the deck, model and flashcard layout that you want, for that some variables are available.

**Flashcard Variables:**
- `[WORD]`: your unknown word
- `[MEANING]`: the definition of this word
- `[PHRASE]`: an example phrase with the word
- `[AUDIO]`: a TTS audio with the selected voice
- `[PICTURE]`: a picture related to the word 

After configuration, to use the Anki-VAC you need to open your Anki and paste a list of unknown words to you, one per line and then click the button in main window to start the proccess.

### Images
<img src="https://i.imgur.com/N1UQDOf.png" width="300px"/><br>
<img src="https://i.imgur.com/jJ8n4LC.png" width="300px"/><br>
<img src="https://i.imgur.com/q49PdNv.png" width="250px"/>


