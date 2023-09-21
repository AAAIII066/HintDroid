import re
import numpy
import hashlib
editc = [
    "android.widget.EditText",
]
textc = [
    "android.widget.TextView",
    "TextInputLayout",
    "android.view.View",
    "android.webkit.WebView"
]



namef = ['cancel']

idf = ['cancel']

thirdk = ['facebook']

couc = ['countrycode']


class EnterNode:
    def __init__(self):
        self.is_explored_in_mutation = False
\

class Node:
    """
    Basic element info get from UI layout xml file
    """

    def __init__(self, tag, classType, packageName, resourceID, contentDesc, text, password, bound, clickable, enable):
        self.__parent = None
        self.__children = None
        self.tag = tag
        self.is_explored_in_mutation = False
        self.attribute = {
            "classType": classType,
            "packageName": packageName,
            "resourceID": resourceID,
            "contentDesc": contentDesc,
            "text": text,
            "password": password,
            "bound": bound,
            "clickable": clickable,
            "location": {'x': bound[0][0], 'y': bound[0][1]},
            "name": None,
            "enable": enable
        }
        if self.attribute['contentDesc']:
            self.attribute['name'] = self.attribute['contentDesc']
        else:
            self.attribute['name'] = self.attribute['text']


    def __eq__(self, other):
        if self.__hash__() == other.__hash__():
            return True
        else:
            return False

    def __hash__(self):
        res = int(hashlib.md5((self.attribute['resourceID'] + self.attribute['classType'] + str(
            self.attribute['bound'])).encode()).hexdigest()[:16], 16)
        return res

    def is_equal(self, other):
        if other is None:
            return False
        if self.attribute['resourceID'] == other.attribute['resourceID'] and self.attribute['classType'] == \
                other.attribute['classType'] and self.attribute['name'] == other.attribute['name'] and self.attribute[
            'bound'] == other.attribute['bound']:
            return True
        else:
            return False

    def is_at_left_top(self):
        center_x = (self.attribute['bound'][0][0] + self.attribute['bound'][1][0]) / 2
        center_y = (self.attribute['bound'][0][1] + self.attribute['bound'][1][1]) / 2
        if center_x < 150 and center_y < 300:
            return True
        else:
            return False

    def is_register(self):
        register_keys = ['register', 'sign up', 'create', 'start', 'continue']
        if get_filter(split_id(self.attribute['resourceID']), register_keys):
            return True
        if get_filter(self.attribute['name'], register_keys):
            return True
        if self.__children is None:
            return False
        for ce in self.__children:
            if not get_filter(ce.attribute['name'], namef):
                if get_filter(ce.attribute['name'], register_keys) or get_filter(
                        split_id(ce.attribute['resourceID']), register_keys):
                    return True
        return False

    def is_login(self):
        login_keys = ['log in', 'sign in', 'login', 'signin']
        if get_filter(self.attribute['name'], login_keys):
            return True
        if self.__children is None:
            return False
        for ce in self.__children:
            if not get_filter(ce.attribute['name'], namef):
                if get_filter(ce.attribute['name'], login_keys):
                    return True
        return False

    def is_back(self):
        back_keywords = ['back', 'navigate up', 'close', 'cancel', 'quit']
        if self.attribute['resourceID'] and 'back' in split_id(self.attribute['resourceID'].lower()):
            return True
        elif get_filter(self.attribute['name'], back_keywords):
            return True
        else:
            return False

    def is_log_out(self):
        log_out_keys = ['logout', 'log_out']
        texts = [self.attribute['resourceID'], self.attribute['name'],
                 self.attribute['contentDesc'], self.attribute['text']]
        for key in log_out_keys:
            for text in texts:
                if key in text.lower():
                    return True
        return False

    def is_bar(self):
        if self.attribute['location']['y'] < 200 or self.attribute['location']['y'] > 2050:
            return True
        else:
            return False

    def success_re(self, restr):
        if type(restr) == str:
            res = re.search(restr, self.attribute['resourceID'])
            if res:
                return True
            else:
                return False
        elif type(restr) == list:
            for sr in restr:
                res = re.search(sr, self.attribute['resourceID'])
                if res:
                    return True
            return False

    def is_third_party(self):
        name_text = self.attribute['name'].lower()
        id_text = split_id(self.attribute['resourceID']).lower()
        text_arr = name_text.split(' ') + name_text.split('_') + id_text.split(' ') + id_text.split('_')
        if get_filter(text_arr, thirdk):
            return True
        elif get_filter(name_text, thirdk) or get_filter(id_text, thirdk):
            return True
        else:
            if self.__children is None:
                return False
            for c in self.__children:
                name_text = c.attribute['name'].lower()
                id_text = split_id(c.attribute['resourceID']).lower()
                text_arr = name_text.split(' ') + name_text.split('_') + id_text.split(' ') + id_text.split('_')
                if get_filter(text_arr, thirdk):
                    return True
                elif get_filter(name_text, thirdk) or get_filter(id_text, thirdk):
                    return True
            return False

    def is_expand(self):
        expand_keys = ['expandable_switch_container']
        if get_filter(split_id(self.attribute['resourceID']), expand_keys):
            return True
        if self.__children is not None:
            for c in self.__children:
                if get_filter(split_id(c.attribute['resourceID']), expand_keys):
                    return True
            return False
        else:
            return False

    def is_country_code(self):
        if get_filter(split_id(self.attribute['resourceID']), couc):
            return True
        else:
            if self.__children is None:
                return False
            for c in self.__children:
                if get_filter((split_id(c.attribute['resourceID'])), couc) or \
                        c.attribute['text'] == '+86':
                    return True
            return False

    def need_filter(self):
        if self.is_expand():
            return True
        if self.get_parent() is not None and self.get_parent().attribute['classType'] == 'android.widget.GridView':
            if self.is_equal(self.__parent.get_children()[0]):
                return False
            else:
                return True
        if get_filter(self.attribute['name'], namef) or get_filter(
                split_id(self.attribute['resourceID']), idf):
            return True
        ccs = self.__children
        if ccs is not None:
            for c in ccs:
                if get_filter(c.attribute['name'], namef):
                    return True
            return False
        return False

    def no_need_deep_explore(self):
        name_no_deep_keys = ['update', 'updates', 'upgrade']
        id_no_deep_keys = ['camera', 'voice_icon', 'search_voice', 'action_share']
        if get_filter(self.attribute['name'], name_no_deep_keys) or get_filter(
                split_id(self.attribute['resourceID']), id_no_deep_keys):
            return True
        if self.__children is not None:
            for c in self.__children:
                if get_filter(c.attribute['name'], name_no_deep_keys) or get_filter(
                        split_id(c.attribute['resourceID']), id_no_deep_keys):
                    return True
            return False
        else:
            return False

    def is_user_image(self):
        image_keys = ['userimage']
        if get_filter(split_id(self.attribute['resourceID']), image_keys):
            return True
        if self.__children is not None:
            for c in self.__children:
                if get_filter(split_id(c.attribute['resourceID']), image_keys):
                    return True
            return False
        else:
            return False

    def is_date_of_sth(self):
        date_keywords = ['day', 'date', 'time']
        if get_filter(self.attribute['name'], date_keywords):
            return True
        if self.__children is not None:
            for c in self.__children:
                if get_filter(c.attribute['name'], date_keywords):
                    return True
            return False
        else:
            return False

    def is_privacy_policy(self):
        privacy_keys = ['privacy', 'policy', 'terms', 'support']
        if get_filter(self.attribute['name'], privacy_keys):
            return True
        else:
            return False

    def is_search_edit_text(self):
        search_keys = ['search']
        if self.attribute['classType'] == 'android.widget.EditText':
            if get_filter(split_id(self.attribute['resourceID']), search_keys) or get_filter(
                    self.attribute['text'], search_keys):
                return True
        return False

    def is_more_option(self):
        more_option_keys = ['more options']
        if equal_filter_key(self.attribute['name'], more_option_keys):
            return True
        else:
            return False

    def compare_id_and_children_id(self, other):
        if self.attribute['resourceID'] or other.attribute['resourceID']:
            if self.attribute['resourceID'] == other.attribute['resourceID']:
                return True
            else:
                return False
        else:
            if self.__children is not None and other.get_children() is not None:
                if len(self.__children) == len(other.get_children()):
                    for i in range(len(self.__children)):
                        if self.__children[i].attribute['resourceID'] != other.get_children()[i].attribute[
                            'resourceID']:
                            return False
                    return True
                else:
                    return False
            else:
                return False

    def is_gender_button(self):
        gender_key_words = ['male', 'female']
        if self.attribute['classType'] == 'android.widget.Button' and self.attribute[
            'text'].lower() in gender_key_words:
            return True
        else:
            return False

    def get_parent(self):
        return self.__parent

    def get_children(self):
        return self.__children

    def BFS(self, func=None):
        sequence = []
        if self.get_children() is None:
            return sequence
        if func:
            for node in self.get_children():
                if func(node):
                    sequence.append(node)
            for node in self.get_children():
                sequence += node.BFS(func)
        else:
            sequence += self.get_children()
            for node in self.get_children():
                sequence += node.BFS()
        return sequence

    def DFS(self, func=None):
        sequence = []
        if self.get_children() is None:
            return sequence
        if func:
            for node in self.get_children():
                if func(self):
                    sequence.append(node)
                sequence += node.DFS(func)
        else:
            for node in self.get_children():
                sequence.append(node)
                sequence += node.DFS()
        return sequence

    def add_child(self, child=None):
        if child is None:
            return 0
        child.set_parent(self)
        if self.__children:
            self.__children.append(child)
        else:
            self.__children = [child]
        return 1

    def is_has_child(self):
        if self.__children is None:
            return False
        return True

    def set_parent(self, Parent=None):
        self.__parent = Parent

    def get_desc(self):
        desc = []
        if self.attribute['text'] != '' and str(self.attribute['text']).isprintable():
            desc.append(str(self.attribute['text']))
        if self.attribute['contentDesc'] != '' and str(self.attribute['contentDesc']).isprintable():
            desc.append((self.attribute['contentDesc']))
        return desc

    def get_closest_node(self, target: list):
        candidate = self.look_down(target, 0)
        result = None
        if candidate:
            pass
        else:
            candidate = self.get_parent().look_up(target, 1)
        if candidate:
            mindist = 99999
            for item in candidate:
                node = item[1]
                dist = self.visual_distance(node)
                if dist < mindist:
                    mindist = dist
                    result = node
        return result

    def look_up(self, target: list, high=0):
        down = self.look_down(target, high)
        if down:
            return down
        else:
            if self.tag == 'root':
                return None
            else:
                return self.get_parent().look_up(target, high + 1)

    def look_down(self, target: list, high=0):
        if self.attribute["classType"] in target:
            return [(high, self)]
        if self.get_children() is None:
            return None
        candidate = []
        mini = 9999
        for node in self.get_children():
            d = node.look_down(target, high + 1)
            if d:
                if d[0][0] < mini:
                    candidate.clear()
                    candidate += d
                    mini = d[0][0]
                elif d[0][0] == mini:
                    candidate += d
        return candidate

    def visual_distance_by_direct(self, node, direct):
        bound1 = self.attribute["bound"]
        bound2 = node.attribute["bound"]
        if direct == 'up':
            return abs((bound1[0][1] + bound1[1][1]) / 2 - (bound2[0][1] + bound2[1][1]) / 2)
        if direct == 'down':
            return abs((bound1[0][1] + bound1[1][1]) / 2 - (bound2[0][1] + bound2[1][1]) / 2)
        if direct == 'right':
            return abs((bound1[0][0] + bound1[1][0]) / 2 - (bound2[0][0] + bound2[1][0]) / 2)
        if direct == 'left':
            return abs((bound1[0][0] + bound1[1][0]) / 2 - (bound2[0][0] + bound2[1][0]) / 2)

    def visual_distance(self, node):
        """
        Distance between two elements
        """
        bound1 = self.attribute["bound"]
        bound2 = node.attribute["bound"]
        if bound1[0][1] < bound2[0][1]:  # y1<y3
            if bound1[1][1] > bound2[1][1]:  # y2>y4
                return 0
            else:
                vec1 = numpy.array((bound1[0][0], bound1[1][1]))
                vec2 = numpy.array(bound2[0])
        elif bound1[0][1] == bound2[0][1]:  # y1=y3
            vec1 = numpy.array(bound1[0])
            vec2 = numpy.array((bound2[1][0], bound2[0][1]))
        elif bound1[0][1] > bound2[0][1]:  # y1>y3
            vec1 = numpy.array(bound1[0])
            vec2 = numpy.array((bound2[0][0], bound2[1][1]))
        else:
            vec1 = numpy.array((float(bound1[0][0] + bound1[1][0]) / 2.0, float(bound1[0][1] + bound1[1][1]) / 2.0))
            vec2 = numpy.array((float(bound2[0][0] + bound2[1][0]) / 2.0, float(bound2[0][1] + bound2[1][1]) / 2.0))
        dist = numpy.sqrt(numpy.sum(numpy.square(vec1 - vec2)))
        return dist

    def visual_direction(self, node):
        bound_base = self.attribute["bound"]
        bound_another = node.attribute["bound"]
        if bound_another[0][1] >= bound_base[1][1]:
            if not bound_another[1][0] <= bound_base[0][0] and not bound_another[0][0] >= bound_base[1][0]:
                return 'up'
        elif bound_another[1][1] <= bound_base[0][1]:
            if not bound_another[1][0] <= bound_base[0][0] and not bound_another[0][0] >= bound_base[1][0]:
                return 'down'
            pass
        elif bound_another[0][0] >= bound_base[1][0]:
            return 'left'
        elif bound_another[1][0] <= bound_base[0][0]:
            return 'right'
        else:
            for i in [0, 1]:
                if not (bound_another[0][i] <= bound_base[0][i] and bound_another[1][i] >= bound_base[1][i]):
                    break
            else:
                return 'inside'
        return 'invalid-position'

    def cal_overlap(self, node):
        bound_base = self.attribute["bound"]
        bound_another = node.attribute["bound"]
        (x11, y11, x12, y12) = bound_base[0][0], bound_base[0][1], bound_base[1][0], bound_base[1][1]
        (x21, y21, x22, y22) = bound_another[0][0], bound_another[0][1], bound_another[1][0], bound_another[1][1]
        start_x = min(x11, x21)
        end_x = max(x12, x22)
        start_y = min(y11, y21)
        end_y = max(y12, y22)
        cur_width = (x12 - x11) + (x22 - x21) - (end_x - start_x)
        cur_height = (y12 - y11) + (y22 - y21) - (end_y - start_y)
        if cur_width <= 0 or cur_height <= 0:
            return 0
        return cur_width * cur_height


class EditNode(Node):
    def __init__(self, tag, classType, packageName, resourceID, contentDesc, text, password, bound, clickable, enable,
                 type="Null"):
        Node.__init__(self, tag, classType, packageName, resourceID, contentDesc, text, password, bound, clickable,
                      enable)
        self.type = type
        self.TotalConstraint = []
        self.hints_record = []
        self.hints = []
        self.mutateCount = 0
        self.mutateState = 'Unknown'
        self.isinMutate = False
        self.hasMutate = False
        self.lastInput = ''
        self.composition = Composition()
        self.relativeIndex = -1

    def __hash__(self):
        res = int(hashlib.md5((str(self.relativeIndex) + self.attribute['resourceID']).encode()).hexdigest()[:16], 16)
        return res

    def get_desc(self):
        desc = []
        if self.attribute['text'] != '' and str(self.attribute['text']).isprintable():
            desc.append(str(self.attribute['text']))
        if self.attribute['contentDesc'] != '' and str(self.attribute['contentDesc']).isprintable():
            desc.append((self.attribute['contentDesc']))
        if self.attribute['resourceID'] != '':
            if self.attribute['resourceID'].find("/") != -1:
                desc.append(str(self.attribute['resourceID'].split("/")[1]))
            else:
                desc.append(str(self.attribute['resourceID']))
        return desc

    def add_hint(self, strings):
        if isinstance(strings, list):
            for s in strings:
                if isinstance(s, list):
                    for sub_s in s:
                        self.hints.append(sub_s)
                else:
                    self.hints.append(s)
            logger.info('Add constraint %s to Node [%s]' % (str(strings), self.attribute['resourceID']))
        else:
            logger.warning('Wrong strings value. Entered %s , list is needed' % type(strings))
            print("Error: wrong value. You have entered %s , list is needed" % type(strings))

    def increase_mutate(self):
        self.mutateCount += 1
        self.hasMutate = True
        if not self.isinMutate:
            self.isinMutate = True

    def clear_mutate(self):
        self.isinMutate = False

    def reset_mutate_his(self):
        logger.info('Node[%s] hasMutate: %s --> False' % (self.attribute['resourceID'], str(self.hasMutate)))
        self.hasMutate = False

    def set_state(self, state):
        if state == 'Success':
            self.mutateState = 'Success'
        elif state == 'Fail':
            self.mutateState = 'Fail'
        else:
            logger.warning('Unknown mutate state: ' + str(state))

    def set_type(self, type):
        if type:
            self.type = type

    def update_constraint(self, flag='walk'):
        for cur_cons in self.hints:
            if cur_cons not in self.hints_record:
                if flag == 'walk':
                    self.hints_record.append(cur_cons)
                    continue
                if not self.isinMutate:
                    self.increase_mutate()
            if cur_cons not in self.TotalConstraint:
                self.TotalConstraint.append(cur_cons)
        if (len(self.hints) == 0 and self.mutateCount == 0) or flag == 'walk':
            self.mutateCount = 1
        else:
            self.hints.clear()


    def get_mutate_info(self):
        node_info = {
            "package_name": self.attribute["packageName"], "edit_type": self.type,
            "edit_id": self.attribute["resourceID"], 'hash': hash(self),
            "mutate_count": self.mutateCount, "isinMutate": self.isinMutate, "hasMutate": self.hasMutate,
            "mutate_state": self.mutateState,
            "location": self.attribute["location"], "restriction": self.TotalConstraint
        }
        return node_info


def equal_filter_key(name, keys):
    if type(name) == str:
        text = name.lower()
        for k in keys:
            if k == text:
                return True
    return False


def get_filter(name, keys):
    if type(name) == str:
        text = name.lower()
        for k in keys:
            if k in text:
                return True
    elif type(name) == list:
        for i in name:
            if i in keys:
                return True
    return False


def split_id(idstring):
    if type(idstring) == str:
        if ":id/" in idstring:
            return idstring[idstring.rfind(':id/') + 4:]
        if ":id" in idstring:
            return idstring[idstring.rfind(':id') + 3:]
        if "/" in idstring:
            return idstring[idstring.rfind('/') + 1:]
        else:
            return idstring
    else:
        return ""


def is_same_bound(arraybound, bound):
    if arraybound[0][0] == bound[0][0] and arraybound[0][1] == bound[0][1] and arraybound[1][0] == bound[1][0] and arraybound[1][1] == bound[1][1]:
        return True
    width_base = bound[1][0] - bound[0][0]
    heigth_base = bound[1][1] - bound[0][1]
    width_er = 5 * (abs(bound[0][0] - arraybound[0][0]) + abs(bound[1][0] - arraybound[1][0]))
    heigth_er = 5 * (abs(bound[0][1] - arraybound[0][1]) + abs(bound[1][1] - arraybound[1][1]))
    if width_er < width_base and heigth_er < heigth_base:
        return True
    return False
