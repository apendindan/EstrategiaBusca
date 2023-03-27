import os
import json
import tkinter as tk
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def send_message():
    user_question = json.loads(json.dumps({"role": "user", "content": user_input.get().strip()}))  # Recebe a questão
    imprime_fala(user_question)    # Imprime a questão na janela
    user_input.delete(0, tk.END)   # Apaga o texto que o usuário escreveu da barra de digitacão
    history.append(user_question)  # Salva a pergunta que o usuário fez no histórico de mensagens
    response = openai.ChatCompletion.create(  # Faz a resposta utilizando a API da OpenAI
        model="gpt-3.5-turbo",                # Define o modelo a ser usado. Necessário atualizar pós fine-tunning
        messages=history                      # O bot recebe tudo do histórico para continuar a conversa
    )
    bibi_response = response["choices"][0]["message"]  # Seleciona apenas a fala que o bot adicinou por último
    history.append(bibi_response)                      # Adiciona essa fala ao histórico
    imprime_fala(bibi_response)                        # Imprime a fala na janela


def imprime_fala(message):
    if message["role"] == "assistant":  # Define o nome e a cor do "assistant"
        speaker = "Bibliotecária: "
        color = "#00558C"  # azul
    elif message["role"] == "user":    # Define o nome e a cor do "user"
        speaker = "Você: "
        color = "#FF0000"  # preto
    else:                              # Caso de algum problema
        speaker = "PROBLEMA: "
        color = "#FF0000"  # vermelho
    conversation_history.config(state=tk.NORMAL)
    conversation_history.insert(tk.END, speaker, "speaker")                                   # Imprime o nome
    conversation_history.insert(tk.END, message["content"] + "\n\n", "content")               # Imprime a fala
    conversation_history.tag_config("speaker", font=("Arial", 12, "bold"), foreground=color)  # Configuracoes do nome
    conversation_history.tag_config("content", font=("Arial", 12), foreground=color)          # Configuracoes da fala
    conversation_history.config(state=tk.DISABLED)


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
    # Adiciona o logo da BIREME
    global logo


cria_janela()
settings = json.loads( """
    {"role": "system", 
    "content": "Você é a Bibliotecária da BIREME. Apenas responda o que for relacionado a estratégias de busca, e, se algo fugir do tema, responda \\"Desculpe, não sou capacitada para responder nada além de questões sobre estratégias de busca\\".\\n\\nExemplo:\\nUsuário:exercicios aerobicos na insuficiencia cardiaca em idosos\\n\\nBibi:Para os temas abaixo recomendamos usar termos livres em diferentes idiomas; pesquisar os descritores de assunto mais adequados para cada um.\\nexercicio aeróbico, Aerobic Exercise\\ninsuficiencia cardíaca, Heart Failure\\nExemplo de busca:\\n(\\"exercicio aeróbico\\" OR \\"Aerobic Exercise\\") AND (\\"insuficiencia cardíaca\\" OR \\"Heart Failure\\")\\nPara idosos - use o filtro LIMITE disponível na interface de resultado, essa faixa etária está disponível na opção Mais filtros, clique e inclua para selecionar a faixa etária.\\n    *os termos da busca são recuperados no título, resumo e descritor de assunto (quando aplicável) dos documentos"}
""")
initial_message = json.loads("""
    {"role": "assistant", 
    "content": "Olá, sou a Bibliotecária virtual da BIREME. Meu objetivo aqui é ajudar você a formular estratégias de busca para conseguir achar os artigos que precisa! Me diga, o que está querendo buscar?"}
""")
history = json.loads('[]')
history.append(settings)
history.append(initial_message)
imprime_fala(initial_message)
window.mainloop()
