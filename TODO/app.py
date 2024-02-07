from flask import Flask, render_template, request, session, send_file
from flask_session import Session
from flask_bootstrap import Bootstrap
from model.item import Item
from model.to_do_list import TO_DO_List
import utilities

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

    to_do_lists = utilities.edit_todo(index, toDoIndex, to_do_lists, description, name)
    
    session["to_do_lists"] = to_do_lists

    return render_template('TO_DO_display.html', content_list=session.get("to_do_lists"))

@app.route('/check_item', methods=['POST'])
def check_item():
    index = int(request.form.get('todoItemParentIndex'))
    toDoIndex = int(request.form.get('todoItemIndex'))
    to_do_lists = session.get("to_do_lists", [])
    to_do_lists = utilities.mark_as_complete(index, toDoIndex, to_do_lists)
    session["to_do_lists"] = to_do_lists
    return render_template('TO_DO_display.html', content_list=session.get("to_do_lists"))

@app.route('/delete_item', methods=['POST'])
def delete_item():
    index = int(request.form.get('todoItemParentIndex'))
    toDoIndex = int(request.form.get('todoItemIndex'))
    to_do_lists = session.get("to_do_lists", [])
    to_do_lists = utilities.delete_to_do_item(index, toDoIndex, to_do_lists)
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
    to_do_lists = utilities.delete_to_do_list(index, to_do_lists)
    session["to_do_lists"] = to_do_lists
    return render_template('TO_DO_display.html', content_list=session.get("to_do_lists"))


@app.route('/download',  methods=['POST'])
def download_to_do():
    password = str(hash(request.form.get('password')))
    encrypt = utilities.build_file(session.get("to_do_lists", []), password)
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
        to_do_lists = utilities.read_file(encrypted_data, password)
        session["to_do_lists"] = to_do_lists
        return render_template('TO_DO_display.html', content_list=session.get("to_do_lists", []))
    except:
        return render_template('error.html', error_message="Incorrect password for TO DO items.")



if __name__ == "__main__":
    app.run(debug=True)
