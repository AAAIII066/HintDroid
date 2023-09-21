import json
from pprint import pprint
import xmltodict
from utils import *
import uiautomator2 as u2
from loguru import logger


def module1():
    logger.info('Scan current page ...')

    d = u2.connect()
    print(d.info)

    page_source = d.dump_hierarchy(compressed=True, pretty=True)
    xml_file = open(save_path + 'hierarchy.xml', 'w', encoding='utf-8')
    xml_file.write(page_source)
    xml_file.close()

    xml_file = open(save_path + 'hierarchy.xml', 'r', encoding='utf-8')
    logger.info('reading hierarchy tree xml file...')
    data_dict = xmltodict.parse(xml_file.read())
    data_str = json.dumps(data_dict)
    json_file = open(save_path + 'hierarchy.json', 'w', encoding='utf-8')
    json_file.write(data_str)
    json_file.close()


    all_components = getAllComponents(data_dict)
    logger.info("There is {} components on current page.".format(str(len(all_components))))

    running_info = get_running_info()
    app_name = running_info['app'].split('.')[-1]
    print("app_name: {}".format(app_name))

    activity_name = running_info['activity'].replace('.', ' ').split(' ')[-1].replace('Activit', '')
    print("activity_name: {}".format(activity_name))

    logger.info('searching for describable components...')

    components_list = []

    for e_component in all_components:
        info = get_common_desc(e_component)
        desc = info['desc']
        if desc != "":
            e_component['@desc'] = desc
            components_list.append(e_component)


    origin_list = [e["@desc"] for e in components_list]
    renamed_list = rename_duplicate(origin_list)

    for i, e in enumerate(renamed_list):
        components_list[i]["@desc"] = e

    editText_list = []

    print("--- There are Input Text components: ---")
    for e in components_list:
        if e['@class'] == 'android.widget.EditText':
            editText_list.append(e)

    print(editText_list)
    print("----------------------------------------")

    if len(editText_list) == 0:
        return "no input text component"

    question = ""

    if len(editText_list) == 1:
        question = "This is a {} app. On its {} page, it has an input text component.\nThe text on this component is {}. ".format(
            app_name, activity_name, editText_list[0]['@desc'])
        (same_horizon_components, same_vertical_components) = chooseFromPos(all_components, editText_list[i]['@bounds'])
        print('same hori: ')
        print(same_horizon_components)
        print('same verti: ')
        print(same_vertical_components)
        if len(same_horizon_components) != 0:
            if len(same_horizon_components) == 1:
                question += "There is a component on the same horizontal line as this input text component. The text on this component is {}.\n".format(
                    same_horizon_components[0]['@desc'])
            else:
                question += "There are {} components on the same horizontal line as this input text component. The text on these components are: ".format(
                    str(len(same_horizon_components)))
                for index, e in enumerate(same_horizon_components):
                    question += e['@desc']
                    if index != len(same_horizon_components) - 1:
                        question += ", "
                question += '.\n'
        if len(same_vertical_components) != 0:
            if len(same_vertical_components) == 1:
                question += "There is a component on the same vertical line as this input text component. The text on this component is {}.\n".format(
                    same_vertical_components[0]['@desc'])
            else:
                question += "There are {} components on the same vertical line as this input text component. The text on these components are: ".format(
                    str(len(same_vertical_components)))
                for index, e in enumerate(same_vertical_components):
                    question += e['@desc']
                    if index != len(same_vertical_components) - 1:
                        question += ", "
                question += '.\n'
    else:
        question = "This is a {} app. On its {} page, it has {} input text components.\n".format(app_name,
                                                                                                 activity_name, str(len(
                editText_list)))
        for i in range(len(editText_list)):
            print(editText_list[i]['@desc'])
            info = "The text on the No.{} input text component is {}. \n".format(str(i + 1), editText_list[i]['@desc'])
            question += info
            (same_horizon_components, same_vertical_components) = chooseFromPos(all_components,
                                                                                editText_list[i]['@bounds'])
            print('same hori: ')
            print(same_horizon_components)
            print('same verti: ')
            print(same_vertical_components)
            if len(same_horizon_components) != 0:
                if len(same_horizon_components) == 1:
                    question += "There is a component on the same horizontal line as this input text component. The text on this component is {}.\n".format(
                        same_horizon_components[0]['@desc'])
                else:
                    question += "There are {} components on the same horizontal line as this input text component. The text on these components are: ".format(
                        str(len(same_horizon_components)))
                    for index, e in enumerate(same_horizon_components):
                        question += e['@desc']
                        if index != len(same_horizon_components) - 1:
                            question += ", "
                    question += '.\n'
            if len(same_vertical_components) != 0:
                if len(same_vertical_components) == 1:
                    question += "There is a component on the same vertical line as this input text component. The text on this component is {}.\n".format(
                        same_vertical_components[0]['@desc'])
                else:
                    question += "There are {} components on the same vertical line as this input text component. The text on these components are: ".format(
                        str(len(same_vertical_components)))
                    for index, e in enumerate(same_vertical_components):
                        question += e['@desc']
                        if index != len(same_vertical_components) - 1:
                            question += ", "
                    question += '.\n'
    if len(editText_list) == 1:
        question += "Please give me a valid input of this input component and the corresponding generation basis (constraint relationship) for this input.\n"
    else:
        question += "Please give me valid inputs of these input components and the corresponding generation bases (constraint relationship) for these inputs.\n"

    print(question)

    logger.info("asking ChatGPT ...")

    output = askCHATGPT1(question)

    # print(output)
    return output, editText_list
