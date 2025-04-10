import pandas as pd
import numpy as np
import random
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn as sns
# Estilo visual bonito
sns.set(style="whitegrid")

from datetime import datetime, timedelta

# Definir número de clientes e transações
num_clientes = 20
num_transacoes = 300

# Criar listas de dados base
ids_clientes = [f"C{id:03d}" for id in range(1, num_clientes + 1)]
cidades = ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Salvador', 'Curitiba']

# Função para gerar datas aleatórias
def gerar_data_aleatoria():
    data_inicial = datetime(2023, 1, 1)
    dias = random.randint(0, 60)
    return data_inicial + timedelta(days=dias)

# Gerar transações
dados = []
for _ in range(num_transacoes):
    cliente = random.choice(ids_clientes)
    data = gerar_data_aleatoria()
    valor = round(np.random.exponential(scale=1000), 2)  # Gera valores positivos, com maioria baixos e alguns altos
    cidade = random.choice(cidades)
    dados.append([cliente, data.date(), valor, cidade])

# Criar DataFrame
df = pd.DataFrame(dados, columns=['id_cliente', 'data_transacao', 'valor_transacao', 'cidade'])


# Regra 1: Transações com valor maior que 500
df['suspeita_valor'] = df['valor_transacao'] > 5000
# Visualizar os primeiros dados

# Contar quantas transações cada cliente fez por dia
transacoes_por_dia = df.groupby(['id_cliente', 'data_transacao']).size().reset_index(name='quantidade_transacoes')

# Juntar essa informação de volta no DataFrame principal
df = df.merge(transacoes_por_dia, on=['id_cliente', 'data_transacao'])

# Regra 2: Mais de 3 transações no mesmo dia
df['suspeita_frequencia'] = df['quantidade_transacoes'] > 3

df['suspeita_geral'] = df['suspeita_valor'] | df['suspeita_frequencia']

df_suspeitas = df[df['suspeita_geral'] == True]
pd.set_option('display.max_columns', None)
print(df_suspeitas.head())
print(f"Total de transações suspeitas: {len(df_suspeitas)}")
sns.set(style="whitegrid")

plt.figure(figsize=(10, 5))
sns.histplot(df['valor_transacao'], bins=50, kde=True)
plt.title('Transaction Amount Distribution')
plt.xlabel('Transaction Amount (R$)')
plt.ylabel('Frequency')
plt.savefig('C:\\Users\\55319\\Documents\\antifraude-projeto\\imagens\\distribuicao_valores.png')
plt.show()


# Contar quantas transações suspeitas por regra
tipos_suspeita = {
    'High Value': df['suspeita_valor'].sum(),
    'Many Transactions in a Day': df['suspeita_frequencia'].sum()
}

plt.figure(figsize=(7, 5))
sns.barplot(x=list(tipos_suspeita.keys()), y=list(tipos_suspeita.values()))
plt.title('Suspicious Transactions by Rule Type')
plt.ylabel('Number of transactions')
plt.xlabel('Suspicion type')
plt.savefig('C:\\Users\\55319\\Documents\\antifraude-projeto\\imagens\\transacoes.png')
plt.show()


# Filtrar apenas as transações suspeitas
df_suspeitas = df[df['suspeita_geral']]

# Contar por cliente
top_clientes = df_suspeitas['id_cliente'].value_counts().head(5)

plt.figure(figsize=(7, 5))
sns.barplot(x=top_clientes.index, y=top_clientes.values)
plt.title('Top 5 Customers with the Most Suspicious Transactions')
plt.ylabel('Number of Suspicious Transactions')
plt.xlabel('Customer ID')
plt.savefig('C:\\Users\\55319\\Documents\\antifraude-projeto\\imagens\\top.png')
plt.show()

