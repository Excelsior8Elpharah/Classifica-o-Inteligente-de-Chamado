# %%
!pip install faker
import pandas as pd
import numpy as np
from faker import Faker
import os
from google.colab import files
import random

print("🚀 Gerando dados de chamados mais realistas para o projeto de ML...")

# Configurações
NUM_RECORDS = 1000
OUTPUT_FILE = 'dados_chamados.csv'
Faker.seed(42)
fake = Faker('pt_BR')

# Padrões de urgência
URGENCIA_PATTERNS = {
    'Alta': [
        "Não consigo pagar desde {dias} dias, perdi meu emprego.",
        "Minha situação financeira está complicada, estou devendo {valor} reais.",
        "O serviço foi cortado, preciso resolver imediatamente!",
        "Estou com dívidas acumuladas há {dias} dias, preciso de ajuda."
    ],
    'Média': [
        "Gostaria de negociar o valor de {valor} reais em atraso.",
        "Tenho uma proposta de pagamento parcelado.",
        "Preciso de condições melhores para quitar minha dívida.",
        "Quero entender as opções para regularizar meu débito."
    ],
    'Baixa': [
        "Solicito a segunda via do boleto referente a {valor} reais.",
        "Tenho dúvida sobre a fatura, o valor não confere.",
        "Preciso de um extrato de pagamentos atualizado.",
        "Qual é o meu débito atual?"
    ]
}

# Atributos adicionais
CANAIS = ["telefone", "e-mail", "chat", "whatsapp", "app"]
TIPO_CLIENTE = ["PF", "PJ"]

# Função para criar texto dinâmico
def gerar_texto(urgencia, dias, valor):
    base = random.choice(URGENCIA_PATTERNS[urgencia])
    texto = base.format(dias=dias, valor=valor)
    complemento = random.choice([
        "Por favor, me ajudem.",
        "Aguardo retorno.",
        "Muito obrigado.",
        "Estou aguardando uma resposta.",
        ""
    ])
    return f"{texto} {complemento}".strip()

# Gerar dados
data = []
for i in range(NUM_RECORDS):
    dias_atraso = min(np.random.exponential(scale=20), 365)  # atraso até 1 ano
    dias_atraso = int(dias_atraso)

    valor_total_divida = max(20, round(np.random.normal(200, 120), 2))  # dívida mínima de 20
    historico_pagamento = np.random.choice(['bom', 'regular', 'ruim'], p=[0.45, 0.35, 0.20])

    # Definir urgência
    if dias_atraso > 90 or (valor_total_divida > 500 and historico_pagamento == 'ruim'):
        urgencia = 'Alta'
    elif dias_atraso > 30 or valor_total_divida > 250:
        urgencia = 'Média'
    else:
        urgencia = 'Baixa'

    texto_chamado = gerar_texto(urgencia, dias_atraso, valor_total_divida)

    data.append({
        'id_chamado': i + 1,
        'cliente': fake.name(),
        'cpf_cnpj': fake.cpf() if np.random.rand() < 0.85 else fake.cnpj(),
        'tipo_cliente': np.random.choice(TIPO_CLIENTE, p=[0.8, 0.2]),
        'estado': fake.estado_sigla(),
        'canal_contato': random.choice(CANAIS),
        'tentativas_contato': np.random.randint(1, 6),
        'dias_atraso': dias_atraso,
        'valor_total_divida': valor_total_divida,
        'historico_pagamento': historico_pagamento,
        'urgencia': urgencia,
        'texto': texto_chamado
    })

# Criar DataFrame
df = pd.DataFrame(data)

# Salvar CSV
df.to_csv(OUTPUT_FILE, index=False)
print(f"✅ Arquivo '{OUTPUT_FILE}' criado com sucesso! ({len(df)} registros)")

# Mostrar amostra
print("\n📊 Primeiras entradas:")
display(df.head(10))

# Download automático
files.download(OUTPUT_FILE)
print("✅ Download concluído!")
