import xml.etree.cElementTree as ET
import os
from widget_information import Node, EditNode, split_id, get_filter, editc, EnterNode
import re

OUTPUT_MODE = None

ADDITIONAL_CLASS = ['android.widget.EditText', 'android.widget.Spinner', 'android.widget.RadioButton',
                    'android.widget.CheckBox', 'android.widget.CalendarView', 'android.widget.CheckedTextView',
                    'android.widget.Switch']

VERIFY_CODE_FILTER_KEYS = ['verify', 'code']



class XmlTree:
    def __init__(self, file="", xml_string=None):
        self.__root = None
        self.TextNodes = []
        self.WebViewNodes = []
        self.TextInputLayoutNodes = []
        self.ViewNodes = []
        self.TextViewNodes = []
        self.EditNodes = []
        self.AllNodes = []
        self.ButtonNodes = []
        self.ImageButtonNodes = []
        self.ImageViewNodes = []
        self.CalendarNodes = []
        self.RadioButtonNodes = []
        self.CheckBoxNodes = []
        self.CheckTextViewNodes = []
        self.SpinnerNodes = []
        self.IdentifyEditNodes = []
        self.OtherNodes = []
        self.RawClickNodes = []
        self.PendingClickNodes = []
        self.ClickableNodes = []
        self.NoEnabledClickNodes = []
        self.AllClickableElements = []
        self.VerifyCodeNodes = []
        self.CountryCodeNodes = []
        self.ThirdPartyNode = []
        self.GenderNodes = []
        self.BackNodes = []
        self.ClassDict = {}
        self.DrawerLayoutNode = []
        self.WebviewFlag = False
        self.SearchEditFlag = False
        self.AlreadyClickNodes = []
        self.textInput = {}
        self.parentUI = 0
        self.MineIdx = -1
        self.nextClick = None
        self.noNeedClick = False
        self.sidebarFlag = False
        self.EnterNode = EnterNode()
        # init
        flag = 0
        if file:
            flag = self.__parse_xml(file)
        elif isinstance(xml_string, str):
            if len(xml_string) != 0:
                flag = self.__parse_xml_string(xml_string)
            else:
                flag = -1
        elif isinstance(xml_string, list):
            flag = self.__parse_xml_list(xml_string)
        else:
            flag = -1
        if flag == -1:
            return
        self.parse_nodes()
        if self.DrawerLayoutNode:
            if len(self.DrawerLayoutNode) == 1:
                DNChilds = self.DrawerLayoutNode[0].get_children()
                if DNChilds is not None:
                    if len(DNChilds) > 1:
                        self.clear_state()
                        self.sidebarFlag = True
                        self.__root = DNChilds[1]
                        self.parse_nodes()
                        if len(DNChilds) > 2:
                            pass
                    else:
                        pass
            else:
                pass

    def clear_state(self):
        self.__root = None
        self.TextNodes = []
        self.WebViewNodes = []
        self.TextInputLayoutNodes = []
        self.ViewNodes = []
        self.TextViewNodes = []
        self.EditNodes = []
        self.AllNodes = []
        self.ButtonNodes = []
        self.ImageButtonNodes = []
        self.ImageViewNodes = []
        self.CalendarNodes = []
        self.RadioButtonNodes = []
        self.CheckBoxNodes = []
        self.CheckTextViewNodes = []
        self.SpinnerNodes = []
        self.IdentifyEditNodes = []
        self.OtherNodes = []
        self.RawClickNodes = []
        self.ClickableNodes = []
        self.NoEnabledClickNodes = []
        self.VerifyCodeNodes = []
        self.CountryCodeNodes = []
        self.ThirdPartyNode = []
        self.GenderNodes = []
        self.BackNodes = []
        self.ClassDict = {}
        self.DrawerLayoutNode = []
        self.WebviewFlag = False
        self.AlreadyClickNodes = []
        self.textInput = {}
        self.parentUI = -1
        self.nextClick = None

    def parse_nodes(self):
        self.AllNodes = self.__root.DFS()
        tmpidx = 0
        for n in self.AllNodes:
            if n.attribute["classType"] in editc:
                n.relativeIndex = tmpidx
                tmpidx += 1
        loginNode = None
        for node in self.AllNodes:
            if node.attribute['packageName'] == "com.android.systemui":
                continue
            if node.attribute['clickable'] == 'true' and node not in self.AllClickableElements:
                self.AllClickableElements.append(node)
            className = node.attribute['classType']
            if className not in self.ClassDict:
                self.ClassDict[className] = 0
            if className == 'android.support.v4.widget.DrawerLayout':
                if node not in self.DrawerLayoutNode:
                    self.DrawerLayoutNode.append(node)
            elif className == 'android.webkit.WebView':
                if not self.WebviewFlag:
                    self.WebviewFlag = True
                if node not in self.WebViewNodes:
                    self.ClassDict[className] += 1
                    self.WebViewNodes.append(node)
                    self.TextNodes.append(node)
            elif className == 'TextInputLayout':
                if node not in self.TextInputLayoutNodes and node.is_has_child():
                    self.ClassDict[className] += 1
                    self.TextInputLayoutNodes.append(node)
                    self.TextNodes.append(node)
            elif className == 'android.view.View':
                if node.attribute['resourceID'] == 'android:id/insertion_handle':
                    continue
                if node not in self.ViewNodes:
                    self.ClassDict[className] += 1
                    self.ViewNodes.append(node)
                    self.TextNodes.append(node)
            elif className == 'android.widget.TextView':
                if node not in self.TextViewNodes:
                    self.ClassDict[className] += 1
                    self.TextViewNodes.append(node)
                    self.TextNodes.append(node)
            elif className == 'android.widget.EditText':
                if node not in self.EditNodes:
                    self.ClassDict[className] += 1
                    self.EditNodes.append(node)
                    self.textInput[hash(node)] = node.attribute['text']
                if node not in self.IdentifyEditNodes:
                    self.IdentifyEditNodes.append(node)
            elif className == "android.widget.LinearLayout" and node.attribute[
                'clickable'] == 'true' and split_id(node.attribute['resourceID']) == 'container':
                if node not in self.IdentifyEditNodes:
                    self.IdentifyEditNodes.append(node)
            elif className == 'android.widget.Button':
                if node not in self.ButtonNodes:
                    self.ClassDict[className] += 1
                    self.ButtonNodes.append(node)
            elif className == 'android.widget.ImageButton':
                if node not in self.ImageButtonNodes:
                    self.ClassDict[className] += 1
                    self.ImageButtonNodes.append(node)
            elif className == 'android.widget.ImageView':
                if node not in self.ImageViewNodes:
                    self.ClassDict[className] += 1
                    self.ImageViewNodes.append(node)
            elif className == 'android.widget.CalendarView':
                if node not in self.CalendarNodes:
                    self.ClassDict[className] += 1
                    self.CalendarNodes.append(node)
            elif className == 'android.widget.RadioButton':
                if node not in self.RadioButtonNodes:
                    self.ClassDict[className] += 1
                    self.RadioButtonNodes.append(node)
            elif className == 'android.widget.CheckBox':
                if node not in self.CheckBoxNodes:
                    self.ClassDict[className] += 1
                    self.CheckBoxNodes.append(node)
            elif className == 'android.widget.CheckedTextViewList':
                if node not in self.CheckTextViewNodes:
                    self.ClassDict[className] += 1
                    self.CheckTextViewNodes.append(node)
            elif className == 'android.widget.Spinner':
                if node not in self.SpinnerNodes:
                    self.ClassDict[className] += 1
                    self.SpinnerNodes.append(node)
            else:
                if node.attribute['classType'] == 'android.widget.FrameLayout':
                    continue
                if node not in self.OtherNodes:
                    self.ClassDict[className] += 1
                    self.OtherNodes.append(node)
            if node.attribute['clickable'] == 'true' and node.attribute['enable'] == 'false':
                if node not in self.NoEnabledClickNodes:
                    self.NoEnabledClickNodes.append(node)
            elif node.attribute['clickable'] == 'true' and node.attribute['enable'] == 'true':
                if node not in self.RawClickNodes:
                    self.RawClickNodes.append(node)
                else:
                    continue
                if node in self.IdentifyEditNodes:
                    continue
                if not node.is_bar():
                    self.PendingClickNodes.append(node)
                if node.is_back(): 
                    self.BackNodes.append(node)
                elif node.is_gender_button():
                    self.GenderNodes.append(node)
                elif className not in ADDITIONAL_CLASS and node.is_country_code():
                    self.CountryCodeNodes.append(node)
                elif className not in ADDITIONAL_CLASS and get_filter(
                        split_id(node.attribute['resourceID']),
                        VERIFY_CODE_FILTER_KEYS):
                    self.VerifyCodeNodes.append(node)
                elif className not in ADDITIONAL_CLASS and not node.need_filter():
                    if node.is_register():
                        self.ClickableNodes.insert(0, node)
                    elif node.is_third_party():
                        self.ThirdPartyNode.append(node)
                    elif node.is_login() and loginNode is None:
                        if loginNode is None:
                            loginNode = node
                    elif not self.same_id_in_clickable_nodes(node):
                        self.ClickableNodes.append(node)
        if len(self.BackNodes) > 1:
            tmpNodes = []
            bn = self.BackNodes[0]
            for i in range(1, len(self.BackNodes)):
                if bn.attribute['location']['x'] <= self.BackNodes[i].attribute['location']['x']:
                    tmpNodes.append(self.BackNodes[i])
                else:
                    tmpNodes.append(bn)
                    bn = self.BackNodes[i]
            self.BackNodes = [bn]
            self.ClickableNodes += tmpNodes
        if self.ClickableNodes and loginNode is not None:
            if self.ClickableNodes[0].is_register():
                self.ClickableNodes.insert(0, loginNode)
            else:
                self.ClickableNodes.insert(0, loginNode)
        if self.ThirdPartyNode:
            self.ClickableNodes = self.ThirdPartyNode + self.ClickableNodes
        if len(self.ButtonNodes) == 1 and len(self.VerifyCodeNodes) == 1 and self.ButtonNodes[0] == \
                self.VerifyCodeNodes[0]:
            self.ClickableNodes.insert(0, self.VerifyCodeNodes[0])
            self.VerifyCodeNodes.pop()
        self.ClassDict = {name: num for name, num in self.ClassDict.items() if num != 0}

    def process_clickable_nodes_by_ig(self, ui_type):
        if type(ui_type) != str:
            return
        if ui_type == 'Other' or ui_type == 'Login':
            return
        elif ui_type == "Signup":
            tmpNodes = self.ClickableNodes
            self.ClickableNodes = []
            signupNodes = []
            tpNodes = []
            for n in tmpNodes:
                if n.is_third_party():
                    tpNodes.append(n)
                elif n.is_login():
                    self.ClickableNodes.append(n)
                elif n.is_register():
                    signupNodes.append(n)
                else:
                    self.ClickableNodes.append(n)
            # discard thirdParty when sign up
            self.ClickableNodes = signupNodes + tpNodes + self.ClickableNodes
        else:
            print("xmlBuilder:processClickableNodesByIG No Recognize:" + ui_type)

    def same_id_in_clickable_nodes(self, node):
        if node.attribute['resourceID']:
            for i in self.ClickableNodes:
                if i.attribute['resourceID'] == node.attribute['resourceID']:
                    return True
                else:
                    return False
        return False

    def set_text_input(self, inputDict):
        self.textInput = inputDict

    def update_widgets_by_device(self, pageSource):
        after_input_node = XmlTree('', pageSource)
        self.update_widgets_by_node(after_input_node)

    def update_widgets_by_node(self, afterInputNode):
        self.__root = afterInputNode.get_root()
        self.TextNodes = afterInputNode.TextNodes
        self.WebViewNodes = afterInputNode.WebViewNodes
        self.TextInputLayoutNodes = afterInputNode.TextInputLayoutNodes
        self.ViewNodes = afterInputNode.ViewNodes
        self.TextViewNodes = afterInputNode.TextViewNodes
        self.EditNodes = afterInputNode.EditNodes
        self.AllNodes = afterInputNode.AllNodes
        self.ButtonNodes = afterInputNode.ButtonNodes
        self.ImageButtonNodes = afterInputNode.ImageButtonNodes
        self.ImageViewNodes = afterInputNode.ImageViewNodes
        self.CalendarNodes = afterInputNode.CalendarNodes
        self.RadioButtonNodes = afterInputNode.RadioButtonNodes
        self.CheckBoxNodes = afterInputNode.CheckBoxNodes
        self.CheckTextViewNodes = afterInputNode.CheckTextViewNodes
        self.SpinnerNodes = afterInputNode.SpinnerNodes
        self.IdentifyEditNodes = afterInputNode.IdentifyEditNodes
        self.OtherNodes = afterInputNode.OtherNodes
        self.RawClickNodes = afterInputNode.RawClickNodes
        self.ClickableNodes = afterInputNode.ClickableNodes
        self.VerifyCodeNodes = afterInputNode.VerifyCodeNodes
        self.CountryCodeNodes = afterInputNode.CountryCodeNodes
        self.BackNodes = afterInputNode.BackNodes
        self.ClassDict = afterInputNode.ClassDict
        self.ThirdPartyNode = afterInputNode.ThirdPartyNode
        self.WebviewFlag = afterInputNode.WebviewFlag
        self.SearchEditFlag = afterInputNode.SearchEditFlag
        self.sidebarFlag = afterInputNode.sidebarFlag

    def compare_edit_node_id(self, other):
        if len(self.EditNodes) != len(other.EditNodes):
            return False
        for s, o in zip(self.EditNodes, other.EditNodes):
            if hash(s) != hash(o):
                return False
        if self.ButtonNodes and other.ButtonNodes:
            for i in range(len(self.ButtonNodes)):
                btnID = self.ButtonNodes[i].attribute["resourceID"]
                if btnID:
                    if i < len(other.ButtonNodes) and btnID == other.ButtonNodes[i].attribute["resourceID"]:
                        return True
                    else:
                        return False
        return True

    def compare_button_node_id(self, other):
        if len(self.ButtonNodes) != len(other.ButtonNodes):
            return False
        for s, o in zip(self.ButtonNodes, other.ButtonNodes):
            if s.attribute['resourceID'] != o.attribute['resourceID']:
                return False
        return True

    def compare_all_nodes_content(self, other):
        for s, o in zip(self.AllNodes, other.AllNodes):
            if s.attribute['name'] != o.attribute['name'] or s.attribute['resourceID'] != o.attribute['resourceID'] or \
                    s.attribute['classType'] != o.attribute['classType'] or s.attribute['bound'] != o.attribute[
                'bound']:
                return False
        return True

    def is_alert(self, app_package=""):
        alert_classes = ['android.widget.TextView', 'android.view.View', 'android.widget.Button',
                         'android.widget.ImageButton', 'android.widget.ScrollView', 'android.widget.ImageView']
        if self.IdentifyEditNodes or len(self.ClickableNodes) > 5 or len(self.ButtonNodes) > 2:
            return False
        for node in self.AllNodes:
            if app_package and app_package != node.attribute['packageName']:
                continue
            if node.attribute['classType'] is None or 'layout' in node.attribute[
                'classType'].lower() or "android.support.v" in node.attribute['classType'].lower():
                continue
            if node.attribute['classType'] not in alert_classes:
                return False
        return True

    def cal_similarity_by_edit_node_id(self, IDList):
        if len(self.EditNodes) != len(IDList):
            return 0
        for e in self.EditNodes:
            if e.attribute['resourceID'] not in IDList:
                return 0
        return 1

    def cal_similarity(self, other):
        if self.EditNodes:
            if not other.EditNodes:
                return 0
            if self.compare_edit_node_id(other):
                return 1
            else:
                return 0
        else:
            if other.EditNodes:
                return 0
            if not self.compare_button_node_id(other):
                return 0
            if self.is_alert():
                if self.compare_all_nodes_content(other):
                    return 1
                else:
                    return 0
            else:
                if self.ClassDict == other.ClassDict:
                    return 1
                if len(self.TextViewNodes) == len(other.TextViewNodes) and len(self.ImageViewNodes) == len(
                        other.ImageViewNodes) and len(self.CheckTextViewNodes) == len(other.CheckTextViewNodes):
                    return 1
                else:
                    return 0

    def in_pages(self, page_list):
        for page in page_list:
            if self.cal_similarity(page) == 1:
                return True
        return False

    def no_need_input(self):
        if not self.EditNodes:
            return True
        if len(self.EditNodes) == 1:
            if 'picker' in split_id(self.EditNodes[0].attribute['resourceID']) and self.EditNodes[0].attribute[
                'text']:
                return True
            tt = self.EditNodes[0].attribute['text'].lower()
            if tt == 'male' or tt == 'female':
                return True
            else:
                return False
        return False

    def get_root(self):
        return self.__root

    def __node_walker(self, parent, parentNode):
        for node in list(parent):
            packageName, resourceID, contentDesc, text, password, classinfo, bound, clickable, enable = self.__extractInfo(
                node)
            if packageName == "":
                continue
            if classinfo in editc:
                currentNode = EditNode("child", classinfo, packageName, resourceID, contentDesc, text, password, bound,
                                       clickable, enable)
            else:
                currentNode = Node("child", classinfo, packageName, resourceID, contentDesc, text, password, bound,
                                   clickable, enable)
            parentNode.add_child(currentNode)
            self.__node_walker(node, currentNode)

    def __parse_xml(self, file):
        self.__uni_file(file)
        try:
            root = ET.parse(file).getroot()
        except Exception as e:
            print("Error : wrong xml file [%s]" % file)
            print(e)
            return -1
        rootNode = Node("root", None, None, None, None, None, None, [(-1, -1), (-1, -1)], None, None)
        self.__root = rootNode
        self.__node_walker(root, rootNode)
        return 1

    def __parse_xml_string(self, xmlstring):
        xmlstring = re.sub(r'&', '&amp;', xmlstring)
        try:
            root = ET.fromstring(xmlstring)
        except Exception as e:
            print("Error : wrong xmlstring: [%s]" % xmlstring)
            print(e)
            return -1
        rootNode = Node("root", None, None, None, None, None, None, [(-1, -1), (-1, -1)], None, None)
        self.__root = rootNode
        self.__node_walker(root, rootNode)
        return 1

    def __uni_file(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f1, open("%s.bak" % file_path, "w", encoding="utf-8") as f2:
            for line in f1:
                string = re.sub(r'&', '&amp;', line)
                f2.write(string)
        os.remove(file_path)
        os.rename("%s.bak" % file_path, file_path)

    def __parse_xml_list(self, xmlstring: list):
        NodeList = []
        for node in xmlstring:
            if not isinstance(node, dict):
                print('Warning: node is not a dic')
                NodeList.append(Node('emty', None, None, None, None, None, None, [(-1, -1), (-1, -1)], None, None))
                continue
            packageName, resourceID, contentDesc, text, password, classinfo, bound, clickable, enable = self.__DroidInfo(
                node)
            if packageName == "":
                continue
            if classinfo in editc:
                currentNode = EditNode("child", classinfo, packageName, resourceID, contentDesc, text, password, bound,
                                       clickable, enable)
            else:
                currentNode = Node("child", classinfo, packageName, resourceID, contentDesc, text, password, bound,
                                   clickable, enable)
            NodeList.append(currentNode)
        if len(NodeList) == 0:
            return -1
        self.__walkDroid(NodeList, xmlstring)
        return 1

    def __DroidInfo(self, node: dict):
        packageName = resourceID = contentDesc = text = klass = ""
        enable = 'false'
        clickable = 'false'
        password = 'false'
        bound = []
        if "package" in node.keys() and node["package"]:
            packageName = node["package"]
        if "text" in node.keys() and node["text"]:
            text = node["text"]
        if "resource_id" in node.keys() and node["resource_id"]:
            resourceID = node["resource_id"]
        if "content_description" in node.keys() and node["content_description"]:
            contentDesc = node["content_description"]
        if "is_password" in node.keys() and node["is_password"]:
            password = str(node["is_password"]).lower()
        if "bounds" in node.keys() and node["bounds"]:
            b = node['bounds']
            bound = [(b[0][0], b[0][1]), (b[1][0], b[1][1])]
        if "clickable" in node.keys() and node["clickable"]:
            clickable = str(node['clickable']).lower()
        if "enabled" in node.keys() and node['enabled']:
            enable = str(node['enabled']).lower()
        if "class" in node.keys() and node['class']:
            klass = node['class']
        return packageName, resourceID, contentDesc, text, password, klass, bound, clickable, enable

    def __walkDroid(self, NodeList: list, xmlstring: list):
        rootNode = Node("root", None, None, None, None, None, None, [(-1, -1), (-1, -1)], None, None)
        self.__root = rootNode
        if len(NodeList) != len(xmlstring):
            print('Error: NodeList not equal xmlstring')
            return -1
        for i in range(len(NodeList)):
            current = xmlstring[i]
            currentNode = NodeList[i]
            if len(current['children']) == 0:
                continue
            for j in current['children']:
                currentNode.add_child(NodeList[j])
            if current['parent'] == -1:
                rootNode.add_child(currentNode)

    def __extractInfo(self, node):
        enable = clickable = packageName = resourceID = contentDesc = text = password = ""
        bound = []
        if "resource-id" not in node.attrib:
            node.attrib["resource-id"] = ""
        if "content-desc" not in node.attrib:
            node.attrib["content-desc"] = ""
        if node.attrib["package"]:
            # get package name
            packageName = node.attrib["package"]
        if node.attrib["text"]:
            # get text inside
            text = node.attrib["text"]
        if node.attrib["resource-id"]:
            # get resoure identification
            resourceID = node.attrib["resource-id"]
        if node.attrib["content-desc"]:
            # get content description
            contentDesc = node.attrib["content-desc"]
        if node.attrib["password"]:
            # get password status
            password = node.attrib["password"]
        if node.attrib["bounds"]:
            # get bound string
            s = node.attrib["bounds"]
            bound = self.__string2bound(s)
        if node.attrib["clickable"]:
            clickable = node.attrib['clickable']
        if node.attrib['enabled']:
            enable = node.attrib['enabled']
        return packageName, resourceID, contentDesc, text, password, node.attrib["class"], bound, clickable, enable

    def __string2bound(self, s):
        result = re.split(r'[\[\]]', s)
        while '' in result:
            result.remove('')
        bound = []
        bound.append((int(result[0].split(",")[0]), int(result[0].split(",")[1])))
        bound.append((int(result[1].split(",")[0]), int(result[1].split(",")[1])))
        return bound


def clean_encode(text):
    while "&#" in text:
        i = text.find("&#")
        length = text[i:].find(";")
        if length == -1:
            return text
        text = text[:i] + text[i + length + 1:]
    return text
