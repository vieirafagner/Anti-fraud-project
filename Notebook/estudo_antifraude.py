import pandas as pd
import numpy as np
import random
import seaborn as sns
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
plt.title('Distribuição dos valores das transações')
plt.xlabel('Valor da transação (R$)')
plt.ylabel('Frequência')
plt.show()


# Contar quantas transações suspeitas por regra
tipos_suspeita = {
    'Valor alto': df['suspeita_valor'].sum(),
    'Muitas transações no dia': df['suspeita_frequencia'].sum()
}

plt.figure(figsize=(7, 5))
sns.barplot(x=list(tipos_suspeita.keys()), y=list(tipos_suspeita.values()))
plt.title('Transações suspeitas por tipo de regra')
plt.ylabel('Quantidade de transações')
plt.xlabel('Tipo de suspeita')
plt.show()


# Filtrar apenas as transações suspeitas
df_suspeitas = df[df['suspeita_geral']]

# Contar por cliente
top_clientes = df_suspeitas['id_cliente'].value_counts().head(5)

plt.figure(figsize=(7, 5))
sns.barplot(x=top_clientes.index, y=top_clientes.values)
plt.title('Top 5 clientes com mais transações suspeitas')
plt.ylabel('Quantidade de transações suspeitas')
plt.xlabel('ID do cliente')
plt.show()
