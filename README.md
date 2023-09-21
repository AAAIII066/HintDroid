# HintDroid

Mobile apps have become indispensable for accessing and participating in various environments, especially for low-vision users. Users with visual impairments can use screen readers to read the content of each screen and understand the content that needs to be operated. Screen readers need to read the hint-text attribute in the text input component to remind visually impaired users what to fill in. Unfortunately, based on our analysis of 4,501 Android apps with text inputs, over 76\% of them are missing hint-text. These issues are mostly caused by developers' lack of awareness when considering visually impaired individuals. To overcome these challenges, we developed an LLM-based hint-text generation model called HintDroid, which analyzes the GUI information of input components and uses in-context learning to generate the hint-text. To ensure the quality of hint-text generation, we further designed a feedback-based inspection mechanism to further adjust hint-text.



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


## structure

![structure](./res/structure.png)

## This example introduces how to use ChatGPT

[a-simple-guide-to-chatgpt-api-with-python](https://medium.com/geekculture/a-simple-guide-to-chatgpt-api-with-python-c147985ae28#id_token=eyJhbGciOiJSUzI1NiIsImtpZCI6ImM5YWZkYTM2ODJlYmYwOWViMzA1NWMxYzRiZDM5Yjc1MWZiZjgxOTUiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJuYmYiOjE2ODMyNjQ1NDksImF1ZCI6IjIxNjI5NjAzNTgzNC1rMWs2cWUwNjBzMnRwMmEyamFtNGxqZGNtczAwc3R0Zy5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsInN1YiI6IjExMTc4NjQ1NDgyMjM3ODU5NTE0NSIsImVtYWlsIjoibWVuZ3podW8uaGFwcHlAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF6cCI6IjIxNjI5NjAzNTgzNC1rMWs2cWUwNjBzMnRwMmEyamFtNGxqZGNtczAwc3R0Zy5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsIm5hbWUiOiJSb2JpbiBDaGVuIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FHTm15eFlwVnBsVVhlY2lOeEMxd0hlQ3l5eGEyYTh0djBRemdLMzdMcVAtPXM5Ni1jIiwiZ2l2ZW5fbmFtZSI6IlJvYmluIiwiZmFtaWx5X25hbWUiOiJDaGVuIiwiaWF0IjoxNjgzMjY0ODQ5LCJleHAiOjE2ODMyNjg0NDksImp0aSI6IjA0YjQ0YzA3NzA2MmNhOGIxZjUxMDY2MjE5ODllZTI5NWQ3ZTQ4NWEifQ.ZSJupHFC6zap9ybM9ThhtDCVmlRB1OEBXwrA1avqnTjCc3oyZOOnKkJbMBT-Jv1TXX7lWHXW9XAqvPClcCePjHH7xwrxYdJpWsbMzMWU1JOU4zI2t3QMmtWGmBwT6qP9Frq31VBVXqAZ3-X_0mJi7OXtjaPSG93eDkLswF7QFyucB9VEsxJhwlcRY3EVF2K5hhLfRsI58BGlHifdbipeueCCYUVKa4hbYCt_33Per27xZmZdcg0LglnPjq4_zN3ciEyP-pzpxu8O2hbrtW7BqvN2F0m115tTddv3hBwp47DHGRwB1XukoTCJe9gkhhLd3nNqLBmHen3AWRLG0ExY_w)

# Motivation

./motivationdata/ This file provides motivation data. Due to GitHub upload restrictions, we have already submitted the complete data to CHI 2024 web system. At the end of the blind review, we will update the connection to Google's online drive.


# Evaluationn

## Usefulness evaluation (./Usefulness evaluation/)


Because the Google Play requires that individuals cannot upload apk without permission. You can download them on Google play through the information in the table.

| **ID** | **App name** | **Category** | **Input** | **accuracy** | **Activity** | **coverage** | **State** | **coverage** | **Filling** | **time** |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
id | App | Category | control | experiment | control | experiment | control | experiment | control | experiment

