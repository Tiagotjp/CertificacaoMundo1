import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# Código do usuário e senha para login
USUARIO_LOGIN = "fullestacio"
SENHA_LOGIN = "fullstack"

# Dados simulados das tabelas
usuarios = [
    {"nome": "João da Silva", "cpf": "05486210564", "funcao": "Analista de Vendas"},
    {"nome": "Maria Santos", "cpf": "02544856823", "funcao": "Gerente Financeiro"},
    {"nome": "Carlos Oliveira", "cpf": "03645892340", "funcao": "Desenvolvedor"},
    {"nome": "Ana Rodrigues", "cpf": "01574862354", "funcao": "Administrador de Banco de Dados"}
]

perfis_acesso = [
    {"codigo_sistema": 1, "nome_perfil": "Administrador", "descricao": "Acesso total ao sistema de RH"},
    {"codigo_sistema": 2, "nome_perfil": "Vendedor", "descricao": "Acesso somente às funcionalidades de vendas"},
    {"codigo_sistema": 3, "nome_perfil": "Financeiro", "descricao": "Acesso às funções financeiras do sistema"},
    {"codigo_sistema": 4, "nome_perfil": "Desenvolvedor", "descricao": "Acesso total ao sistema de desenvolvimento"}
]

sistemas = [
    {"codigo_sistema": 1, "nome_sistema": "Sistema de Recursos Humanos"},
    {"codigo_sistema": 2, "nome_sistema": "Sistema de Vendas"},
    {"codigo_sistema": 3, "nome_sistema": "Sistema Financeiro"},
    {"codigo_sistema": 4, "nome_sistema": "Sistema de Desenvolvimento"}
]

conflito_interesse = [
    {"cpf_1": "11111111111", "cpf_2": "22222222222", "conflito": "Sim"},
    {"cpf_1": "11111111111", "cpf_2": "44444444444", "conflito": "Sim"},
    {"cpf_1": "22222222222", "cpf_2": "33333333333", "conflito": "Não"}
]


# Função para fazer login


def fazer_login():
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    if usuario == USUARIO_LOGIN and senha == SENHA_LOGIN:
        frame_login.pack_forget()
        frame_principal.pack()
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos.")

# Função para exibir informações de nomes e matrículas na página de login


def exibir_info():
    info = "\n".join([
        "ALEX BARROSO PAZ  202306151781",
        "BRUNO SAMPAIO BASTOS  202304594821",
        "CRISTIAN DA SILVA DE MACENA  202305246398",
        "LUKAS CAUÃ OLIVEIRA XAVIER  202305450556",
        "MARILENE GOMES DUARTE  202304554749",
        "TIAGO DE JESUS PEREIRA FURTADO  202306189045"
    ])
    messagebox.showinfo("Dev Team 2", info)

# Função para adicionar novo usuário


def adicionar_usuario():
    novo_usuario = entry_novo_usuario.get()
    novo_cpf = entry_nova_cpf.get()
    nova_funcao = entry_novo_funcao.get()

    # Verifique se o CPF já existe em algum usuário existente
    cpf_existente = next((usuario for usuario in usuarios if usuario["cpf"] == novo_cpf), None)

    if novo_usuario and novo_cpf and nova_funcao:
        if cpf_existente:
            messagebox.showerror("Erro", f"CPF '{novo_cpf}' já está cadastrado.")
        else:
            usuarios.append({"nome": novo_usuario, "cpf": novo_cpf, "funcao": nova_funcao})

            # Verifique os conflitos entre o novo usuário e os usuários existentes
            for usuario in usuarios:
                if usuario["cpf"] != novo_cpf:
                    adicionar_conflito_auto(novo_cpf, usuario["cpf"])  # Fornecendo ambos os CPFs

            # Atualiza as tabelas
            update_tables()

            messagebox.showinfo("Informação", f"Novo usuário '{novo_usuario}' adicionado com sucesso.")
    else:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")


# Função para excluir usuário selecionado


def excluir_usuario():
    selection = tree_usuarios.selection()
    if selection:
        cpf_selecionado = tree_usuarios.item(selection[0])["values"][0]

        # Procura o usuário a ser removido na lista de usuários
        usuario_para_remover = None
        for usuario in usuarios:
            if usuario["cpf"] == cpf_selecionado:
                usuario_para_remover = usuario
                break

        # Remove o usuário da lista de usuários
        if usuario_para_remover:
            usuarios.remove(usuario_para_remover)

        # Remove o item selecionado da Treeview
        tree_usuarios.delete(selection)

        messagebox.showinfo("Informação", "Usuário excluído com sucesso.")
    else:
        messagebox.showerror("Erro", "Por favor, selecione um usuário para excluir.")


# Função para adicionar novo perfil de acesso

def adicionar_perfil():
    novo_perfil = entry_novo_perfil.get()

    if novo_perfil:
        novo_codigo_sistema = len(perfis_acesso) + 1
        perfis_acesso.append({"codigo_sistema": novo_codigo_sistema,
                             "nome_perfil": novo_perfil, "descricao": ""})

        # Atualiza as tabelas
        update_tables()

        messagebox.showinfo("Informação", f"Novo perfil de acesso '{novo_perfil}' adicionado com sucesso.")
    else:
        messagebox.showerror("Erro", "Por favor, insira o nome do novo perfil de acesso.")

# Função para excluir perfil de acesso selecionado


def excluir_perfil():
    selection = tree_perfis.selection()
    if selection:
        codigo_perfil_selecionado = tree_perfis.item(selection[0])["values"][0]

        # Remove o perfil de acesso da lista de perfis
        for perfil in perfis_acesso:
            if perfil["codigo_sistema"] == codigo_perfil_selecionado:
                perfis_acesso.remove(perfil)
                break

        # Atualiza as tabelas
        update_tables()

        messagebox.showinfo("Informação", "Perfil de acesso excluído com sucesso.")
    else:
        messagebox.showerror("Erro", "Por favor, selecione um perfil de acesso para excluir.")

# Função para adicionar novo sistema


def adicionar_sistema():
    novo_sistema = entry_novo_sistema.get()

    if novo_sistema:
        novo_codigo_sistema = len(sistemas) + 1
        sistemas.append({"codigo_sistema": novo_codigo_sistema,
                        "nome_sistema": novo_sistema})

        # Atualiza as tabelas
        update_tables()

        messagebox.showinfo("Informação", f"Novo sistema '{novo_sistema}' adicionado com sucesso.")
    else:
        messagebox.showerror("Erro", "Por favor, insira o nome do novo sistema.")

# Função para excluir sistema selecionado


def excluir_sistema():
    selection = tree_sistemas.selection()
    if selection:
        codigo_sistema_selecionado = tree_sistemas.item(selection[0])["values"][0]

        # Remove o sistema da lista de sistemas
        for sistema in sistemas:
            if sistema["codigo_sistema"] == codigo_sistema_selecionado:
                sistemas.remove(sistema)
                break

        # Atualiza as tabelas
        update_tables()

        messagebox.showinfo("Informação", "Sistema excluído com sucesso.")
    else:
        messagebox.showerror("Erro", "Por favor, selecione um sistema para excluir.")


# Função para verificar conflitos automaticamente
def verificar_conflitos():
    for sod in conflito_interesse:
        cpf_1 = sod["cpf_1"]
        cpf_2 = sod["cpf_2"]

        # Lógica de verificação de conflitos (exemplo: se duas pessoas têm a mesma função)
        usuario_1 = next((user for user in usuarios if user["cpf"] == cpf_1), None)
        usuario_2 = next((user for user in usuarios if user["cpf"] == cpf_2), None)

        if usuario_1 and usuario_2:
            if usuario_1["funcao"] == usuario_2["funcao"]:
                sod["conflito"] = "Sim"
            else:
                sod["conflito"] = "Não"




# Função para excluir conflito selecionado


def excluir_conflito():
    selection = tree_sod.selection()
    if selection:
        cpf_1 = tree_sod.item(selection[0])["values"][0]
        cpf_2 = tree_sod.item(selection[0])["values"][1]

        # Remove o conflito da lista de conflitos
        for conflito in conflito_interesse:
            if (
                conflito["cpf_1"] == cpf_1
                and conflito["cpf_2"] == cpf_2
            ):
                conflito_interesse.remove(conflito)
                break

        # Remove o item selecionado da Treeview
        tree_sod.delete(selection)

        messagebox.showinfo("Informação", "Conflito excluído com sucesso.")
    else:
        messagebox.showerror("Erro", "Por favor, selecione um conflito para excluir.")


# Função para remover conflitos relacionados a um usuário excluído


def remover_conflitos_usuario(cpf):
    global conflito_interesse

    # Crie uma cópia da lista de conflitos para evitar problemas ao iterar e remover
    conflitos_a_remover = []

    # Encontre e adicione conflitos relacionados ao CPF especificado na lista
    for conflito in conflito_interesse:
        if conflito["cpf_1"] == cpf or conflito["cpf_2"] == cpf:
            conflitos_a_remover.append(conflito)

    # Remova os conflitos relacionados ao CPF da lista de conflitos
    for conflito in conflitos_a_remover:
        conflito_interesse.remove(conflito)

    # Atualize a tabela SoD
    update_table_sod()


# Função para adicionar novo conflito automaticamente
def adicionar_conflito_auto(cpf_1, cpf_2):
    global conflito_interesse

    # Lógica para verificar conflitos automaticamente
    usuario_1 = next((user for user in usuarios if user["cpf"] == cpf_1), None)
    usuario_2 = next((user for user in usuarios if user["cpf"] == cpf_2), None)

    if usuario_1 and usuario_2:
        if usuario_1["funcao"] == usuario_2["funcao"]:
            conflito = "Sim"
        else:
            conflito = "Não"

        # Adiciona o conflito à lista de conflitos
        conflito_interesse.append({
            "cpf_1": cpf_1,
            "cpf_2": cpf_2,
            "conflito": conflito
        })

        # Atualiza a tabela SoD
        update_table_sod()


# Função para atualizar todas as tabelas


def update_tables():
    update_table_usuarios()
    update_table_perfis()
    update_table_sistemas()
    update_table_sod()

# Função para atualizar a tabela de usuários


def update_table_usuarios():
    tree_usuarios.delete(*tree_usuarios.get_children())
    for usuario in usuarios:
        tree_usuarios.insert("", "end", values=(
            usuario["nome"], usuario["cpf"], usuario["funcao"]))

# Função para atualizar a tabela de perfis de acesso


def update_table_perfis():
    tree_perfis.delete(*tree_perfis.get_children())
    for perfil in perfis_acesso:
        tree_perfis.insert("", "end", values=(
            perfil["codigo_sistema"], perfil["nome_perfil"], perfil["descricao"]))

# Função para atualizar a tabela de sistemas


def update_table_sistemas():
    tree_sistemas.delete(*tree_sistemas.get_children())
    for sistema in sistemas:
        tree_sistemas.insert("", "end", values=(
            sistema["codigo_sistema"], sistema["nome_sistema"]))

# Função para atualizar a tabela SoD


def update_table_sod():
    tree_sod.delete(*tree_sod.get_children())
    for sod in conflito_interesse:
        tree_sod.insert("", "end", values=(
            sod["cpf_1"], sod["cpf_2"], sod["conflito"]))


# Criar janela principal


root = ctk.CTk()
root.title("Matriz SoD")
root.resizable(False, False)

# Carregar a imagem de fundo
imagem_fundo = Image.open("EstacioIMG.png")
imagem_fundo = imagem_fundo.resize((100, 100), Image.LANCZOS)
imagem_fundo = ImageTk.PhotoImage(imagem_fundo)

# Colocar a imagem de fundo em um Label
label_fundo = tk.Label(master=root, image=imagem_fundo)
label_fundo.place(x=-130, y=-30, relwidth=1, relheight=1)

# Página de login


frame_login = ctk.CTkFrame(master=root)
frame_login.pack(padx=100, pady=20)


entry_usuario = ctk.CTkEntry(master=frame_login, placeholder_text="Usuário")
entry_usuario.grid(row=0, column=1, padx=10, pady=5)


entry_senha = ctk.CTkEntry(master=frame_login, placeholder_text="Senha", show="*")
entry_senha.grid(row=1, column=1, padx=10, pady=5)

btn_login = ctk.CTkButton(master=frame_login, text="Login", command=fazer_login)
btn_login.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

btn_info = ctk.CTkButton(frame_login, text="Info", command=exibir_info)
btn_info.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

# Página principal
frame_principal = ctk.CTkFrame(root)

# Cria o widget Notebook para as abas
notebook = ttk.Notebook(frame_principal)
notebook.pack(padx=10, pady=5)

# Aba Tabela Cadastro de Usuários
tab_usuarios = ctk.CTkFrame(notebook)
notebook.add(tab_usuarios, text="Cadastro de Usuários")

tree_usuarios = ttk.Treeview(tab_usuarios, columns=(
    "nome", "cpf", "funcao"), show="headings")
tree_usuarios.heading("nome", text="Nome do Usuário")
tree_usuarios.heading("cpf", text="CPF do Usuário")
tree_usuarios.heading("funcao", text="Função")
tree_usuarios.pack(padx=10, pady=5, expand=True, fill="both")

# Entradas de texto e rótulos para adicionar novo usuário

entry_novo_usuario = ctk.CTkEntry(tab_usuarios, placeholder_text="Nome do Usuário")
entry_novo_usuario.pack(padx=10, pady=5)

entry_nova_cpf = ctk.CTkEntry(tab_usuarios, placeholder_text="CPF do Usuário")
entry_nova_cpf.pack(padx=10, pady=5)

entry_novo_funcao = ctk.CTkEntry(tab_usuarios, placeholder_text="Função")
entry_novo_funcao.pack(padx=10, pady=5)

btn_adicionar_usuario = ctk.CTkButton(
    tab_usuarios, text="Adicionar Usuário", command=adicionar_usuario)
btn_adicionar_usuario.pack(padx=10, pady=5)

btn_excluir_usuario = ctk.CTkButton(
    tab_usuarios, text="Excluir Usuário", command=excluir_usuario)
btn_excluir_usuario.pack(padx=10, pady=5)

# Aba Tabela Cadastro de Perfis de Acesso
tab_perfis = ctk.CTkFrame(notebook)
notebook.add(tab_perfis, text="Cadastro de Perfis de Acesso")

tree_perfis = ttk.Treeview(tab_perfis, columns=(
    "codigo_sistema", "nome_perfil", "descricao"), show="headings")
tree_perfis.heading("codigo_sistema", text="Código do Sistema")
tree_perfis.heading("nome_perfil", text="Nome do Perfil")
tree_perfis.heading("descricao", text="Descrição do Perfil")
tree_perfis.pack(padx=10, pady=5, expand=True, fill="both")

# Entrada de texto para adicionar novo perfil
entry_novo_perfil = ctk.CTkEntry(tab_perfis, placeholder_text="Cadastre o Perfil")
entry_novo_perfil.pack(padx=10, pady=5)

btn_adicionar_perfil = ctk.CTkButton(
    tab_perfis, text="Adicionar Perfil", command=adicionar_perfil)
btn_adicionar_perfil.pack(padx=10, pady=5)

btn_excluir_perfil = ctk.CTkButton(
    tab_perfis, text="Excluir Perfil", command=excluir_perfil)
btn_excluir_perfil.pack(padx=10, pady=5)

# Aba Tabela Cadastro de Sistemas
tab_sistemas = ctk.CTkFrame(notebook)
notebook.add(tab_sistemas, text="Cadastro de Sistemas")

tree_sistemas = ttk.Treeview(tab_sistemas, columns=(
    "codigo_sistema", "nome_sistema"), show="headings")
tree_sistemas.heading("codigo_sistema", text="Código do Sistema")
tree_sistemas.heading("nome_sistema", text="Nome do Sistema")
tree_sistemas.pack(padx=10, pady=5, expand=True, fill="both")

# Entrada de texto para adicionar novo sistema
entry_novo_sistema = ctk.CTkEntry(tab_sistemas, placeholder_text="Cadastre o Sistema")
entry_novo_sistema.pack(padx=10, pady=5)

btn_adicionar_sistema = ctk.CTkButton(
    tab_sistemas, text="Adicionar Sistema", command=adicionar_sistema)
btn_adicionar_sistema.pack(padx=10, pady=5)

btn_excluir_sistema = ctk.CTkButton(
    tab_sistemas, text="Excluir Sistema", command=excluir_sistema)
btn_excluir_sistema.pack(padx=10, pady=5)

# Aba Tabela Matriz de Conflitos (SoD)
tab_sod = ctk.CTkFrame(notebook)
notebook.add(tab_sod, text="Matriz de Conflitos (SoD)")

# Criar botão para excluir conflito selecionado
btn_excluir_conflito = ctk.CTkButton(
    tab_sod, text="Excluir Conflito", command=excluir_conflito)
btn_excluir_conflito.pack(padx=10, pady=5)

# Tabela Matriz de Conflitos (SoD)
tree_sod = ttk.Treeview(tab_sod, columns=(
    "cpf_1", "cpf_2", "conflito"), show="headings")
tree_sod.heading("cpf_1", text="CPF 1")
tree_sod.heading("cpf_2", text="CPF 2")
tree_sod.heading("conflito", text="Conflito")
tree_sod.pack(padx=10, pady=5, expand=True, fill="both")

def exibir_matriz_de_conflitos():
    # ... Seu código para exibir a aba ...

    # Chama a função para verificar conflitos automaticamente
    verificar_conflitos()


# Atualiza as tabelas na página principal
update_tables()

# Exibir página de login
frame_login.pack()

# Iniciar loop da aplicação
root.mainloop()
