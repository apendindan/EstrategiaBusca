import os
import json
import tkinter as tk
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def send_message():
    # Recebe a questão que o usuário precisa de ajuda
    user_question = json.loads(json.dumps({"role": "user", "content": user_input.get().strip()}))
    Imprime_Fala(user_question)
    user_input.delete(0, tk.END)
    history.append(user_question)
    # Faz a resposta. Necessário colocar o comando da OpenAI API aqui
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=history
    )
    bibi_response = response["choices"][0]["message"]
    history.append(bibi_response)
    Imprime_Fala(bibi_response)

def Imprime_Fala(message):
    if message["role"] == "assistant":
        speaker = "Bibliotecária: "
        color = "#00558C"  # azul
    elif message["role"] == "user":
        speaker = "Você: "
        color = "#FF0000"  # preto
    else:
        speaker = "PROBLEMA: "
        color = "#FF0000"  # vermelho
    conversation_history.config(state=tk.NORMAL)
    conversation_history.insert(tk.END, speaker, "speaker")
    conversation_history.insert(tk.END, message["content"] + "\n\n", "content")
    conversation_history.tag_config("speaker", font=("Arial", 12, "bold"), foreground=color)
    conversation_history.tag_config("content", font=("Arial", 12), foreground=color)
    conversation_history.config(state=tk.DISABLED)


def Cria_Janela():
    # Cria a janela do chat
    global window
    window = tk.Tk()
    window.title("Bibliotecária da BIREME")
    # Cria a área de conversa
    global conversation_history
    conversation_history = tk.Text(window, wrap=tk.WORD, state=tk.DISABLED)
    conversation_history.pack(expand=True, fill=tk.BOTH)
    # Cria a área de input do usuário
    global user_input
    user_input = tk.Entry(window, width=100)
    user_input.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.BOTH)
    user_input.bind('<Return>', lambda event: send_message())
    # Cria o botão de sair
    global quit_button
    quit_button = tk.Button(window, text="Sair", command=window.quit)
    quit_button.pack(side=tk.RIGHT, padx=5, pady=5)
    # Cria o botão de envio
    global send_button
    send_button = tk.Button(window, text="Enviar", command=send_message)
    send_button.pack(side=tk.RIGHT, padx=5, pady=5)
    # Define as cores de fundo
    window.configure(background="#00558C")
    conversation_history.configure(background="#FFFFFF")
    user_input.configure(background="#FFFFFF", fg="#000000", font=("Arial", 12))
    # Adiciona o logo da BIREME
    global logo
    logo = tk.PhotoImage(file="Imagens/bireme_logo.png")
    logo_label = tk.Label(window, image=logo)
    logo_label.pack(side=tk.TOP, pady=1)


Cria_Janela()
settings = json.loads(
    '{"role": "system", "content": "Você é a Bibliotecária da BIREME. Apenas responda o que for relacionado a estratégias de busca, e, se algo fugir do tema, responda \\"Desculpe, não sou capacitada para responder nada além de questões sobre estratégias de busca\\"."}')
initial_message = json.loads(
    '{"role": "assistant", "content": "Olá, sou a Bibliotecária virtual da BIREME. Meu objetivo aqui é ajudar você a formular estratégias de busca para conseguir achar os artigos que precisa! Me diga, o que está querendo buscar?"}')
history = json.loads('[]')
history.append(settings)
history.append(initial_message)
Imprime_Fala(initial_message)
window.mainloop()
