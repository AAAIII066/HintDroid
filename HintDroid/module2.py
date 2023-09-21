import json
from pprint import pprint
import xmltodict
from utils import *
import uiautomator2 as u2
from loguru import logger



def module2(chat_response: str, editText_list):
    logger.info('asking ChatGPT ...')
    question1 = "Based on the input component context information, the valid input and the corresponding generation basis, please generate test cases for: "
    for i, e in enumerate(editText_list):
        question1 += e["@desc"]
        if (i != len(editText_list) - 1):
            question1 += ", "
    question1 += ", that can trigger an interruption defect, and generate mutation rules based on the above information. "

    print(question1)

    ans2 = askCHATGPT2(question1, chat_response)
    print(ans2)

    question2 = "Based on the test cases you just generated for this component or components that can trigger breakage defects, and the corresponding mutation rules, please write code for these input components:"
    for i, e in enumerate(editText_list):
        question2 += e["@desc"]
        if (i != len(editText_list) - 1):
            question2 += ", "
    question2 += ", that can generate test cases in batch. "

    print(question2)

    ans3 = askCHATGPT3(question2, ans2)
    print(ans3)
    return ans3
