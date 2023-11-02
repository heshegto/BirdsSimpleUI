import json
from ru.travelfood.simple_ui import NoSQL as noClass
from java import jclass

from android.widget import Toast
from com.chaquo.python import Python

from datetime import datetime

# ------- Обработчики экрана Меню -------
def menu_on_start(hashMap,_files=None,_data=None):   
    return hashMap

def menu_on_input(hashMap,_files=None,_data=None):
    if hashMap.get("listener")=="menu":
        if hashMap.get("menu")=="Список":
            hashMap.put("ShowScreen","Список птиц")        
        elif hashMap.get("menu")=="Создание":
            hashMap.put("ShowScreen","Создание новой птицы")    
    elif  hashMap.get("listener")=='ON_BACK_PRESSED': 
            hashMap.put("FinishProcess","")     
    return hashMap


# ------- Обработчкики экрана Создание новой птицы -------
def create_on_start(hashMap,_files=None,_data=None):
    if not hashMap.containsKey("saved_bird"):
        hashMap.put("saved_bird","")
    return hashMap

def create_on_input(hashMap,_files=None,_data=None):
    noClass = jclass("ru.travelfood.simple_ui.NoSQL")
    ncl = noClass("test_nosql")

    if hashMap.get("listener")=="save_bird":
        if hashMap.containsKey("name_bird") and hashMap.containsKey("color_bird"):

            name, color = hashMap.get("name_bird"), hashMap.get("color_bird")
            j = {
                "name": name,
                "color": color
            }
            if hashMap.containsKey("foto"):
                j["foto"] = hashMap.get("foto")
            jkeys = ncl.getallkeys()
            keys = json.loads(jkeys)
            id = 0
            if len(keys) > 0:
                id = max([int(x) for x in keys]) + 1

            ncl.put(str(id), json.dumps(j,ensure_ascii=False), True)

            hashMap.put("saved_bird", str(id)+' '+ name+' '+color)
           
    if hashMap.get("listener")=='ON_BACK_PRESSED': 
        hashMap.put("ShowScreen","Меню")    
    if hashMap.get("listener")=='del_all':
        ncl.destroy()
        hashMap.put("speak","Attention! All data has been destroyed!")
    return hashMap 


# ------- Обработчики экрана Карточка птицы -------
def card_on_start(hashMap, files=None, data=None):
    noClass = jclass("ru.travelfood.simple_ui.NoSQL")
    ncl = noClass("test_nosql")
    bird = json.loads(ncl.get(hashMap.get("selected_card_key")))

    hashMap.put("bird_name", bird['name'])
    hashMap.put("bird_color", bird['color'])
    if 'foto' in bird.keys():
        hashMap.put("image", bird['foto'])
    else:
        hashMap.put("image", "None")
    if hashMap.get("listener") == 'btn_saw':
        hashMap.put("StartProcess", "Птицы, которых я видел")
    return hashMap

def card_on_input(hashMap, files=None, data=None):
    if hashMap.get("listener")=='ON_BACK_PRESSED': 
        hashMap.put("ShowScreen","Список птиц")
    return hashMap


# ------- Обработчики экрана Список птиц -------
def list_on_start(hashMap,_files=None,_data=None):

    j = { 
        "customcards": {
            "layout": {
                "type": "LinearLayout",
                "orientation": "vertical",
                "height": "match_parent",
                "width": "match_parent",
                "weight": "0",
                "Elements": [
                    {
                        "type": "LinearLayout",
                        "orientation": "horizontal",
                        "height": "wrap_content",
                        "width": "match_parent",
                        "weight": "0",
                        "Elements": [
                            {
                                "type": "Picture",
                                "show_by_condition": "",
                                "Value": "@picture",
                                "NoRefresh": False,
                                "document_type": "",
                                "mask": "",
                                "Variable": "",
                                "TextSize": "16",
                                "TextColor": "#DB7093",
                                "TextBold": True,
                                "TextItalic": False,
                                "BackgroundColor": "",
                                "width": "match_parent",
                                "height": "wrap_content",
                                "weight": 2
                            },
                            {
                                "type": "LinearLayout",
                                "orientation": "vertical",
                                "height": "wrap_content",
                                "width": "match_parent",
                                "weight": "1",
                                "Elements": [
                                    {
                                        "type": "TextView",
                                        "show_by_condition": "",
                                        "Value": "@name",
                                        "NoRefresh": False,
                                        "document_type": "",
                                        "mask": "",
                                        "Variable": ""
                                    },
                                    {
                                        "type": "TextView",
                                        "show_by_condition": "",
                                        "Value": "@color",
                                        "NoRefresh": False,
                                        "document_type": "",
                                        "mask": "",
                                        "Variable": ""
                                    },
                                ]
                            },
                        ]
                    },
                    {
                        "type": "TextView",
                        "show_by_condition": "",
                        "Value": "@pos",
                        "NoRefresh": False,
                        "document_type": "",
                        "mask": "",
                        "Variable": "",
                        "TextSize": "-1",
                        "TextColor": "#6F9393",
                        "TextBold": False,
                        "TextItalic": True,
                        "BackgroundColor": "",
                        "width": "wrap_content",
                        "height": "wrap_content",
                        "weight": 0
                    }
                ]
            }
        }
    }

    noClass = jclass("ru.travelfood.simple_ui.NoSQL")
    ncl = noClass("test_nosql")

    keys = json.loads(ncl.getallkeys())
   
    j["customcards"]["cardsdata"]=[]

    for i in keys:
        bird = json.loads(ncl.get(i))

        c =  {
            "key": i,
            "pos": "Pos. "+i,
            "name": bird['name'],
            "color": bird['color'],
        }
        if 'foto' in bird.keys():
            c["picture"] = bird['foto']

        j["customcards"]["cardsdata"].append(c)

    hashMap.put("cards",json.dumps(j,ensure_ascii=False).encode('utf8').decode())
    return hashMap

def list_on_input(hashMap,_files=None,_data=None):
    if hashMap.get('selected_card_key'):
        hashMap.put("ShowScreen", "Карточка птицы")
    if hashMap.get("listener")=='ON_BACK_PRESSED': 
        hashMap.put("ShowScreen","Меню")
    if hashMap.get("listener")=="create_new":
        hashMap.put("ShowScreen","Создание новой птицы")
    return hashMap


# ------- Обработчики экрана Птицы, которых я видел -------
def i_saw_on_start(hashMap, files=None, data=None):

    j = {
        "customcards": {
            "layout": {
                "type": "LinearLayout",
                "orientation": "vertical",
                "height": "match_parent",
                "width": "match_parent",
                "weight": "0",
                "Elements": [
                    {
                        "type": "LinearLayout",
                        "orientation": "horizontal",
                        "height": "wrap_content",
                        "width": "match_parent",
                        "weight": "0",
                        "Elements": [
                            {
                                "type": "Picture",
                                "show_by_condition": "",
                                "Value": "@picture",
                                "NoRefresh": False,
                                "document_type": "",
                                "mask": "",
                                "Variable": "",
                                "TextSize": "16",
                                "TextColor": "#DB7093",
                                "TextBold": True,
                                "TextItalic": False,
                                "BackgroundColor": "",
                                "width": "match_parent",
                                "height": "wrap_content",
                                "weight": 2
                            },
                            {
                                "type": "LinearLayout",
                                "orientation": "vertical",
                                "height": "wrap_content",
                                "width": "match_parent",
                                "weight": "1",
                                "Elements": [
                                    {
                                        "type": "TextView",
                                        "show_by_condition": "",
                                        "Value": "@string1",
                                        "NoRefresh": False,
                                        "document_type": "",
                                        "mask": "",
                                        "Variable": ""
                                    },
                                    {
                                        "type": "TextView",
                                        "show_by_condition": "",
                                        "Value": "@string2",
                                        "NoRefresh": False,
                                        "document_type": "",
                                        "mask": "",
                                        "Variable": ""
                                    },
                                ]
                            },
                            {
                                "type": "TextView",
                                "show_by_condition": "",
                                "Value": "@val",
                                "NoRefresh": False,
                                "document_type": "",
                                "mask": "",
                                "Variable": "",
                                "TextSize": "16",
                                "TextColor": "#DB7093",
                                "TextBold": True,
                                "TextItalic": False,
                                "BackgroundColor": "",
                                "width": "match_parent",
                                "height": "wrap_content",
                                "weight": 2
                            }
                        ]
                    },
                    {
                        "type": "TextView",
                        "show_by_condition": "",
                        "Value": "@descr",
                        "NoRefresh": False,
                        "document_type": "",
                        "mask": "",
                        "Variable": "",
                        "TextSize": "-1",
                        "TextColor": "#6F9393",
                        "TextBold": False,
                        "TextItalic": True,
                        "BackgroundColor": "",
                        "width": "wrap_content",
                        "height": "wrap_content",
                        "weight": 0
                    }
                ]
            }
        }
    }

    noClass = jclass("ru.travelfood.simple_ui.NoSQL")
    ncl = noClass("list_of_views")

    keys = ncl.getallkeys()
    jkeys = json.loads(keys)
   
    j["customcards"]["cardsdata"]=[]
    for i in jkeys:
        bird = json.loads(ncl.get(i))
        c =  {
        "key": i,
        "descr": "Pos. "+i,
        "string1": bird['datetime'],
        "string2": bird['name'],
        'val': bird['views']
        }
        if 'foto' in bird.keys():
            c["picture"] = bird['foto']
        j["customcards"]["cardsdata"].append(c)

    hashMap.put("seen_birds",json.dumps(j,ensure_ascii=False).encode('utf8').decode())
    
    return hashMap

def i_saw_on_input(hashMap, files=None, data=None):
    id = hashMap.get("selected_card_key")

    noClass = jclass("ru.travelfood.simple_ui.NoSQL")
    ncl = noClass("test_nosql")
    bird = json.loads(ncl.get(id))

    count = noClass("count_views")
    LOviews = noClass("list_of_views")

    if hashMap.get("listener")=="add_to_i_saw":
        j = {
            "datetime": str(datetime.now()),
            "name": bird['name'],
        }
        if 'foto' in bird.keys():
            j["foto"] = bird["foto"]

        keys = count.getallkeys()
        jkeys = json.loads(keys)
        if  id in jkeys:
            count.put(id, str(int(count[id]) + 1), True)
        else:
            count.put(id, '1', True)

        j["views"] = count.get(id)


        keys = LOviews.getallkeys()
        jkeys = json.loads(keys)
        id = 0
        if len(jkeys) > 0:
            id = max([int(x) for x in jkeys]) + 1

        LOviews.put(str(id), json.dumps(j,ensure_ascii=False), True)

    if hashMap.get("listener")=='ON_BACK_PRESSED': 
        hashMap.put("ShowScreen","Меню")
    return hashMap
