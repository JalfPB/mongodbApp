import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from bson.objectid import ObjectId
import bcrypt

from pymongo import MongoClient  
uri = "mongodb+srv://iabd:iabdiabd@clusteralfonso.ibue99h.mongodb.net/?retryWrites=true&w=majority&appName=ClusterAlfonso"
client = MongoClient(uri)
db = client.sample_mflix
users = db.users

cursor = users.find()
for u in cursor:
    print(u)

def refresh_user_list():
    tree.delete(*tree.get_children())
    for user in users.find():
        user_id = user.get('_id', 'ID desconocido')
        name = user.get('name', 'Nombre desconocido')
        email = user.get('email', 'Email desconocido')
        password = user.get('password', 'Password desconocido')
        tree.insert('', tk.END, values=(user_id, name, email, password))

def add_user():
    name = simpledialog.askstring("Nombre", "Ingrese el nombre del usuario:")
    email = simpledialog.askstring("Email", "Ingrese el email del usuario:")
    password = simpledialog.askstring("Password", "Ingrese el password del usuario:", show='*')
    if name and email and password:
        password_binaria=password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_binaria, salt)

        users.insert_one({'name': name, 'email': email, 'password': hashed})
        refresh_user_list()

def edit_user():
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)
        user_id = ObjectId(item['values'][0])
        new_name = simpledialog.askstring("Nuevo Nombre", "Ingrese el nuevo nombre del usuario:")
        new_email = simpledialog.askstring("Nuevo Email", "Ingrese el nuevo email del usuario:")
        new_password = simpledialog.askstring("Nueva Contraseña", "Ingrese la nueva contraseña del usuario:", show='*')
        if new_name and new_email and new_password:
            users.update_one({'_id': user_id}, {'$set': {'name': new_name, 'email': new_email, 'password': new_password}})
            refresh_user_list()

def delete_user():
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)
        user_id = ObjectId(item['values'][0])
        result = messagebox.askyesno("Confirmar", "Esta seguro de que desea borrar este usuario?")
        if result:
            users.delete_one({'_id': user_id})
            refresh_user_list()


root = tk.Tk()
root.title("Gestión de usuarios")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

columns = ('user_id', 'name', 'email', 'password')
tree = ttk.Treeview(frame,columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, width=100)
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
scrollbar.pack(side=tk.RIGHT, fill="y")
tree.configure(yscrollcommand=scrollbar.set)

btn_add_user = ttk.Button(root, text="Agregar Usuario", command=add_user, style="C.TButton")
btn_add_user.pack(fill=tk.X, expand=True, padx=10, pady=2)

btn_edit_user = ttk.Button(root, text="Editar Usuario", command=edit_user)
btn_edit_user.pack(fill=tk.X, expand=True, padx=10, pady=2)

btn_delete_user = ttk.Button(root, text="Eliminar Usuario", command=delete_user)
btn_delete_user.pack(fill=tk.X, expand=True, padx=10, pady=2)

refresh_user_list()

root.mainloop()