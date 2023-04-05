import os
import tkinter as tk
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def send_message():
    # Recebe questão e imprime
    global historico
    user_question = user_input.get().strip()  # Recebe a questão
    imprime_fala("User",user_question)                          # Imprime a questão na janela
    user_input.delete(0, tk.END)                                # Apaga o que o usuário escreveu da barra de digitacão
    user_input.insert(tk.END, "... Carregando a resposta ...")  # Escreve na barra de digitação
    window.update()                                             # Atualiza a janela para tudo aparecer para o usuário
    historico += "User:"+user_question+"\n\n"                   # Salva a pergunta que o usuário fez no histórico

    # Formula a resposta e imprime
    response = openai.Completion.create(  # Faz a resposta utilizando a API da OpenAI
        model="curie",                    # Define o modelo a ser usado. Necessário atualizar pós fine-tunning
        prompt=historico+"Bibi:",         # O bot recebe tudo do histórico para continuar a conversa
        max_tokens=200,
        temperature=0
     )
    bibi_response = response["choices"][0]["text"]  # Seleciona apenas a fala que o bot adicinou por último
    historico += "Bibi:"+bibi_response+"\n\n"       # Adiciona essa fala ao histórico
    imprime_fala("Bibi",bibi_response)              # Imprime a fala na janela
    user_input.delete(0, tk.END)                    # Apaga o "carregando" da barra de digitação


def imprime_fala(role, message):
    global speaker, color, numb

    # Descobre se a fala será do assistant ou user, salva o nome e o numero da tag correspondente
    if role == "Bibi":
        speaker = "Bibi: "
        numb = 0                        # Esse é o numero da tag, que será colocado na lista Tags
    elif role == "User":
        speaker = "Você: "
        numb = 2                        # Esse é o numero da tag, que será colocado na lista Tags

    # Inicia
    conversation_history.config(state=tk.NORMAL)
    Tags = ["speaker_assistant", "content_assistant", "speaker_user", "content_user"] # Lista as possíveis formatações

    # Define as configurações para a fala da Bibliotecária (cor azul) com o nome dela em negrito
    conversation_history.tag_config("speaker_assistant", font=("Arial", 12, "bold"),
                                    foreground="#00558C")
    conversation_history.tag_config("content_assistant", font=("Arial", 12),
                                    foreground="#00558C")

    # Define as configurações para a fala do User (cor preto) com o nome dele em negrito
    conversation_history.tag_config("speaker_user", font=("Arial", 12, "bold"),
                                    foreground="#000000")
    conversation_history.tag_config("content_user", font=("Arial", 12),
                                    foreground="#000000")

    # Imprime as falas e os nomes
    conversation_history.insert(tk.END, speaker, Tags[numb])
    conversation_history.insert(tk.END, message + "\n\n", Tags[numb+1])

    # Encerra
    conversation_history.config(state=tk.DISABLED)
    conversation_history.yview(tk.END)    # Desce a janela até o final


def cria_janela():
    # Cria a janela do chat
    global window
    window = tk.Tk()
    window.title("Bibliotecária da BIREME")

    # Cria a área de conversa
    global conversation_history
    conversation_history = tk.Text(window, wrap=tk.WORD, state=tk.DISABLED)
    conversation_history.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    # Cria a área de input do usuário
    global user_input
    user_input = tk.Entry(window, width=100,)
    user_input.pack(side=tk.LEFT, padx=10, pady=5, expand=True, fill=tk.BOTH)
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


cria_janela()

# Define os settings que vamos mandar para o ChatGPT explicando como funcionar no ChatBot
with open(os.getcwd()+'/Texts/settings', 'r') as file:
    settings = file.read()

with open(os.getcwd()+'/Texts/examples', 'r') as file:
    examples = file.read()

# Define a mensagem de apresentação do ChatBot
with open(os.getcwd()+'/Texts/mensagem_inicial', 'r') as file:
    initial_message = file.read()


# Cria o histórico onde vamos salvar a conversa inteira
global historico
historico = settings + "\n\n\n" + examples + "\n\n\n"  # Caso queira adicionar exemplos pro sistema, tirar a #
historico += "Bibi:"+initial_message+"\n\n"
imprime_fala("Bibi", initial_message)

# Começa o loop do chat
window.mainloop()
