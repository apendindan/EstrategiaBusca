import openai
import os

openai.api_key = os.environ["OPENAI_API_KEY"]  # configure sua chave de API OpenAI


def upload_de_dados():
    # Os dados tem que estar no formato JSONL, salve como for necessário e depois rode a linha abaixo no terminal
    # openai tools fine_tunes.prepare_data -f estrategiaexemplos.csv
    openai.File.create(
        file=open("estrategiaexemplos.jsonl", "rb"),
        purpose='fine-tune'
    )
    file_id = openai.FineTune.list()[-1]["id"]
    print(file_id)
    return file_id


def primeiro_treino(file_id):
    # Treinando o modelo de perguntas e respostas.
    model_base = 'curie'
    openai.FineTune.create(
        training_file=file_id,
        model=model_base
    )

    # Aqui é para salvar o id do modelo para ser usado dps. A função de entrega o id do ultimo modelo treinado.
    model_id = openai.FineTune.list()[-1]["id"]
    print(model_id)


dada_id = upload_de_dados()
primeiro_treino(dada_id)
