import utilities
from model.item import Item
from model.to_do_list import TO_DO_List
import json

def get_item(list_index, item_index, to_do_list):
    list_obj = next((obj for obj in to_do_list if obj.id == list_index), None)
    if list_obj:
        items = list_obj.items if list_obj.items else []    
        list_item = next((obj for obj in items if obj.id == item_index), None)
        if list_item:
            return list_item

test_item1 = Item(0, "test", False)
test_item2 = Item(1, "test", True)

test_list = [TO_DO_List(0, "test_list", "test_list", [test_item1, test_item2] ),
             TO_DO_List(1, "test_list", "test_list", [test_item1] ),
             TO_DO_List(2, "test_list", "test_list", [test_item2] )]


# Test mark_as_complete to True

to_do_list = utilities.mark_as_complete(0, 0, test_list)
testItem = get_item(0, 0, to_do_list)
if testItem.completed:
    print("Mark as complete to True: Passed")
else:
    print("Mark as complete to True: Failed")        

# Test mark_as_complete to False
    
to_do_list = utilities.mark_as_complete(0, 1, test_list)
testItem = get_item(0, 1, to_do_list)
if not testItem.completed:
    print("Mark as complete to False: Passed")
else:
    print("Mark as complete to False: Failed")

# Test delete_to_do_item 
to_do_list = utilities.delete_to_do_item(0, 0, test_list)
if len(to_do_list[0].items) == 1:
    print("Delete item: Passed")
else:
    print("Delete item: Failed")

# Test delete_to_do_list 
to_do_list = utilities.delete_to_do_list(0, test_list)
if len(to_do_list) == 2:
    print("Delete list: Passed")
else:
    print("Delete list: Failed")


# Test build_file 
encrypted_content = utilities.build_file(to_do_list, "password")
content = []
for to_do_list in to_do_list:
    content.append(to_do_list.to_dict())

json_encrypted_content = json.dumps(content, indent=2).encode('utf-8')

if encrypted_content != json_encrypted_content:
    print("Encrypted file: Passed")
else:
    print("Encrypted file: Failed")


decrypted_content = utilities.read_file(encrypted_content, "password")

content = []
for to_do_list in decrypted_content:
    content.append(to_do_list.to_dict())

json_decrypted_content = json.dumps(content, indent=2).encode('utf-8')



if json_encrypted_content == json_decrypted_content:
    print("Full flow encryption and decryption: Passed")
else:
    print("Full flow encryption and decryption: Failed")
