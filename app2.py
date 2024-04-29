import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from bson.objectid import ObjectId
import bcrypt

from pymongo import MongoClient  
uri = "mongodb+srv://iabd:iabdiabd@clusteralfonso.ibue99h.mongodb.net/?retryWrites=true&w=majority&appName=ClusterAlfonso"
client = MongoClient(uri)
db = client.sample_analytics
customers = db.customers

cursor = customers.find()
for u in cursor:
    print(u)

def refresh_user_list():
    tree.delete(*tree.get_children())
    for user in customers.find():
        user_id = user.get('_id', 'ID desconocido')
        name = user.get('name', 'Nombre desconocido')
        address = user.get('address', 'Direccion desconocida')
        username = user.get('username', 'Nombre de usuario desconocido')
        tree.insert('', tk.END, values=(user_id, name, address, username))

def add_user():
    name = simpledialog.askstring("Nombre", "Ingrese el nombre del usuario:")
    address = simpledialog.askstring("address", "Ingrese la Drireccion del usuario:")
    username = simpledialog.askstring("username", "Ingrese el nombre de Usuario del usuario:")
    if name and address and username:
        #username_binaria=username.encode('utf-8')
        #salt = bcrypt.gensalt()
        #hashed = bcrypt.hashpw(username_binaria, salt)

        customers.insert_one({'name': name, 'address': address, 'username': username})
        refresh_user_list()

def edit_user():
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)
        user_id = ObjectId(item['values'][0])
        new_name = simpledialog.askstring("Nuevo Nombre", "Ingrese el nuevo nombre del usuario:")
        new_address = simpledialog.askstring("Nueva Direccion", "Ingrese la nueva direccion del usuario:")
        new_username = simpledialog.askstring("Nuevo Usuario", "Ingrese el nuevo nombre de usuario del usuario:")
        if new_name and new_address and new_username:
            customers.update_one({'_id': user_id}, {'$set': {'name': new_name, 'address': new_address, 'username': new_username}})
            refresh_user_list()

def delete_user():
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)
        user_id = ObjectId(item['values'][0])
        result = messagebox.askyesno("Confirmar", "Esta seguro de que desea borrar este usuario?")
        if result:
            customers.delete_one({'_id': user_id})
            refresh_user_list()

root = tk.Tk()
root.title("Gestión de usuarios")

style = ttk.Style()

style.configure('W.TButton', font =
               ('calibri', 10, 'bold', 'underline'),
                foreground = 'red')

frame = tk.Frame(root)
frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

columns = ('user_id', 'name', 'address', 'username')
tree = ttk.Treeview(frame,columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, width=100)
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
scrollbar.pack(side=tk.RIGHT, fill="y")
tree.configure(yscrollcommand=scrollbar.set)

btn_add_user = ttk.Button(root, text="Agregar Usuario", command=add_user, 
                style = 'W.TButton')
btn_add_user.pack(fill=tk.X, expand=True, padx=10, pady=2)

btn_edit_user = ttk.Button(root, text="Editar Usuario", command=edit_user, 
                style = 'W.TButton')
btn_edit_user.pack(fill=tk.X, expand=True, padx=10, pady=2)

btn_delete_user = ttk.Button(root, text="Eliminar Usuario", command=delete_user, 
                style = 'W.TButton')
btn_delete_user.pack(fill=tk.X, expand=True, padx=10, pady=2)

refresh_user_list()

root.mainloop()