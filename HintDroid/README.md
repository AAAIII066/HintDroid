# HintDroid Source code

## How to use
1. Generate Your API Key: Before we start working with the ChatGPT API, we need to login into OpenAI account and generate our API keys.
   `openai.api_key = "XXXXXXX"`
2. Installing the library: To work with the ChatGPT API, first, we have to install the openai library by running the following command.
3. Using “ChatCompletion” gpt-3.5-turbo, which is the same model used by ChatGPT.
   
   `import os` 
   
   `import openai`
   
   `openai.api_key = os.getenv("OPENAI_API_KEY")`

   `completion = openai.ChatCompletion.create(`
   
   `model="gpt-3.5-turbo",`
     
    `)`

    

4. Appending the users role to the previous list and add the input function in order to interact with the API as if we’re working with ChatGPT.
   
   `import os` 
   
   `import openai`
   
   `content = input("User: ")`

   `messages.append({"role": "user", "content": content})`
   
   `completion = openai.ChatCompletion.create(`

   `model="gpt-3.5-turbo",`
   
   `messages=messages`
   
   `)`


### Requirements
* Android emulator
* Ubuntu or Windows
* Appium Desktop Client: [link](https://github.com/appium/appium-desktop/releases/tag/v1.22.3-4)
* Python 3.7
  * apkutils==0.10.2
  * Appium-Python-Client==1.3.0
  * Levenshtein==0.18.1
  * lxml==4.8.0
  * opencv-python==4.5.5.64
  * sentence-transformers==1.0.3
  * torch==1.6.0
  * torchvision==0.7.0

Use the gpt-3.5.

