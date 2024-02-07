from model.item import Item
from model.to_do_list import TO_DO_List
import json
import file_encrypt

def mark_as_complete(index, toDoIndex, to_do_lists):
    list_obj = next((obj for obj in to_do_lists if obj.id == index), None)
    if list_obj:
        to_do_lists.remove(list_obj)
        items = list_obj.items if list_obj.items else []    
        list_item = next((obj for obj in items if obj.id == toDoIndex), None)
        if list_item:
            items.remove(list_item)
            list_item.completed = not list_item.completed
            items.append(list_item)
            list_obj.items = items
            to_do_lists.append(list_obj)
            
    return to_do_lists

def edit_todo(index, toDoIndex, to_do_lists, description, name):
    list_obj = next((obj for obj in to_do_lists if obj.id == index), None)
    if list_obj:
        to_do_lists.remove(list_obj)
        items = list_obj.items if list_obj.items else []    
        list_item = next((obj for obj in items if obj.id == toDoIndex), None)
        if list_item:
            items.remove(list_item)
            list_item.description = description
            list_item.name = name
            items.append(list_item)
            list_obj.items = items
            to_do_lists.append(list_obj)
            
    return to_do_lists


def delete_to_do_item(index, toDoIndex, to_do_lists):
    list_obj = next((obj for obj in to_do_lists if obj.id == index), None)
    if list_obj:
        to_do_lists.remove(list_obj)
        items = list_obj.items if list_obj.items else []    
        list_item = next((obj for obj in items if obj.id == toDoIndex), None)
        if list_item:
            items.remove(list_item)
            list_obj.items = items
            to_do_lists.append(list_obj)
    return to_do_lists


def delete_to_do_list(index, to_do_lists):
    list_obj = next((obj for obj in to_do_lists if obj.id == index), None)
    if list_obj:
        to_do_lists.remove(list_obj)
    return to_do_lists

def build_file(to_do_lists, password):
    content = []
    for to_do_list in to_do_lists:
        content.append(to_do_list.to_dict())

    json_content = json.dumps(content, indent=2).encode('utf-8')

    return file_encrypt.encrypt_file(json_content, password)


def read_file(encrypted_data, password):
    decrypted_content = file_encrypt.decrypt_file(encrypted_data, password)
    json_content = json.loads(decrypted_content.decode('utf-8'))
    to_do_lists = []
    for item in json_content:
        to_do_list = TO_DO_List(item['id'], item['name'], item['description'], item['items'])
        to_do_lists.append(to_do_list)

    return to_do_lists