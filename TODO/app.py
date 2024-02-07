from flask import Flask, render_template, request, session, send_file
from flask_session import Session
from flask_bootstrap import Bootstrap
from model.item import Item
from model.to_do_list import TO_DO_List
import json
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import base64


app = Flask(__name__)
Bootstrap(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/')
def home():
    if not session.get("to_do_lists", []):
        session.pop("to_do_lists", None)
    return render_template('index.html', title='Home')

@app.route('/display', methods=['GET', 'POST'])
def display():
    if session.get("to_do_lists"):
        return render_template('TO_DO_display.html', content_list=session.get("to_do_lists"))
    else:
        return render_template('index.html', title='Home')

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')

        items = [] 

        to_do_lists = session.get("to_do_lists", [])

        if to_do_lists:
            id = to_do_lists[-1].id + 1
        else:
            id = 0

        new_list = TO_DO_List(id, name, description, items)
        to_do_lists.append(new_list)

        session["to_do_lists"] = to_do_lists
        return render_template('TO_DO_display.html', content_list=session.get("to_do_lists"))
    return render_template('create.html', content_item=session.get("to_do_lists"))

@app.route('/add_item', methods=['POST'])
def add_item():
    item_name = request.form.get('item_name')
    item_description = request.form.get('item_description')
    
    index = int(request.form.get('todoIndex'))
    to_do_lists = session.get("to_do_lists", [])

    list_obj = next((obj for obj in to_do_lists if obj.id == index), None)

    if list_obj:
        to_do_lists.remove(list_obj)
        items = list_obj.items if list_obj.items else []
        if len(items) > 0:
            new_item = Item(items[-1].id +1,item_name, item_description, False)
        else:
            new_item = Item(0,item_name, item_description, False)
        items.append(new_item)
        list_obj.items = items
        to_do_lists.append(list_obj)
        session["to_do_lists"] = to_do_lists

    return render_template('TO_DO_display.html', content_list=session.get("to_do_lists"))


@app.route('/edit_list', methods=['POST'])
def edit_list():
    name = request.form.get('name')
    description = request.form.get('description')
    
    index = int(request.form.get('todoIndex'))
    to_do_lists = session.get("to_do_lists", [])

    list_obj = next((obj for obj in to_do_lists if obj.id == index), None)

    if list_obj:
        to_do_lists.remove(list_obj)
        list_obj.name = name
        list_obj.description = description
        to_do_lists.append(list_obj)
        session["to_do_lists"] = to_do_lists

    return render_template('TO_DO_display.html', content_list=session.get("to_do_lists"))


@app.route('/edit_todo', methods=['POST'])
def edit_todo():
    name = request.form.get('name')
    description = request.form.get('description')
    
    index = int(request.form.get('todoItemParentIndex'))
    toDoIndex = int(request.form.get('todoItemIndex'))
    to_do_lists = session.get("to_do_lists", [])

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


    session["to_do_lists"] = to_do_lists

    return render_template('TO_DO_display.html', content_list=session.get("to_do_lists"))

@app.route('/check_item', methods=['POST'])
def check_item():
    index = int(request.form.get('todoItemParentIndex'))
    toDoIndex = int(request.form.get('todoItemIndex'))
    to_do_lists = session.get("to_do_lists", [])
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
    session["to_do_lists"] = to_do_lists
    return render_template('TO_DO_display.html', content_list=session.get("to_do_lists"))

@app.route('/delete_item', methods=['POST'])
def delete_item():
    index = int(request.form.get('todoItemParentIndex'))
    toDoIndex = int(request.form.get('todoItemIndex'))
    to_do_lists = session.get("to_do_lists", [])
    list_obj = next((obj for obj in to_do_lists if obj.id == index), None)
    if list_obj:
        to_do_lists.remove(list_obj)
        items = list_obj.items if list_obj.items else []    
        list_item = next((obj for obj in items if obj.id == toDoIndex), None)
        if list_item:
            items.remove(list_item)
            list_obj.items = items
            to_do_lists.append(list_obj)
    session["to_do_lists"] = to_do_lists
    return render_template('TO_DO_display.html', content_list=session.get("to_do_lists"))

@app.route('/delete_all', methods=['POST'])
def delete_all():
    session["to_do_lists"] = []
    return render_template('index.html', title='Home')

@app.route('/set_edit_index', methods=['POST'])
def set_edit_index():
    index = int(request.form.get('todoListIndex'))
    session["edit_index"] = index
    return render_template('TO_DO_display.html', content_list=session.get("to_do_lists"), edit_index=index )

@app.route('/delete_list', methods=['POST'])
def delete_list():
    index = int(request.form.get('todoListIndex'))
    to_do_lists = session.get("to_do_lists", [])
    list_obj = next((obj for obj in to_do_lists if obj.id == index), None)
    if list_obj:
        to_do_lists.remove(list_obj)
    session["to_do_lists"] = to_do_lists
    return render_template('TO_DO_display.html', content_list=session.get("to_do_lists"))


@app.route('/download',  methods=['POST'])
def download_to_do():
    password = str(hash(request.form.get('password')))

    content = []
    to_do_lists = session.get("to_do_lists", [])
    for to_do_list in to_do_lists:
        content.append(to_do_list.to_dict())

    json_content = json.dumps(content, indent=2).encode('utf-8')

    salt = b'todo'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=10000,
        salt=salt,
        length=32,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())
    
    encoded_key = base64.urlsafe_b64encode(key)
    
    cipher = Fernet(encoded_key)

    encrypted_data = cipher.encrypt(json_content)

    encrypt = encrypted_data
    temp_file_path = 'temp_file.txt'
    with open(temp_file_path, 'wb') as file:
        file.write(encrypt)

    return send_file(temp_file_path, as_attachment=True, download_name='downloaded_file.txt')



@app.route('/upload', methods=['POST'])
def upload():
    password = str(hash(request.form.get('password')))
    uploaded_file = request.files['file']

    temp_file_path = 'temp_file.txt'
    uploaded_file.save(temp_file_path)

    with open(temp_file_path, 'rb') as file:
        encrypted_data = file.read()

    try :

        salt = b'todo'
        kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=10000,
        salt=salt,
        length=32,
        backend=default_backend()
        )   
        key = kdf.derive(password.encode())
        
        # Encode the key to make it suitable for Fernet
        encoded_key = base64.urlsafe_b64encode(key)
        
        cipher = Fernet(encoded_key)

        decrypted_data = cipher.decrypt(encrypted_data)
        json_content = json.loads(decrypted_data.decode('utf-8'))
        to_do_lists = []
        for item in json_content:
            to_do_list = TO_DO_List(item['id'], item['name'], item['description'], item['items'])
            to_do_lists.append(to_do_list)
        session["to_do_lists"] = to_do_lists
        return render_template('TO_DO_display.html', content_list=session.get("to_do_lists", []))
    except:
        return render_template('error.html', error_message="Incorrect password for TO DO items.")



if __name__ == "__main__":
    app.run(debug=True)
