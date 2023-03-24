import openai
import os
import json

openai.api_key = os.environ["OPENAI_API_KEY"] # configure sua chave de API OpenAI

# Carregando os dados de treinamento do arquivo JSON
with open('squad_data.json', 'r') as f:
    data = json.load(f)

# Preparando os dados de treinamento para o formato esperado pela API da OpenAI
examples = []
for item in data:
    context = item['context']
    for qa in item['qas']:
        question = qa['question']
        answer = qa['answer']['text']
        examples.append({'text': f'{question} {context}', 'label': answer})

# Treinando o modelo de perguntas e respostas usando o conjunto de dados SQuAD
model_base = 'text-davinci-003'
fine_tune_args = {
    'model': model_base,
    'train_dataset': examples,
    'validation_dataset': examples,
    'epochs': 5,
    'batch_size': 32,
    'learning_rate': 1e-5,
    'max_seq_length': 512,
    'validation_split': 0.2,
    'overwrite': True,
    'model_name': 'Estrategias de Busca',
    'model_tags': ['Estrategias_de_Busca']
}
openai.FineTune.create(**fine_tune_args)

model_id = openai.FineTune.list_models(tag="my_tag")[0]['id']
print(model_id)