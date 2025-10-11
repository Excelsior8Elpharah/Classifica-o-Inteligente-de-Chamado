🧠 Classificação Inteligente de Chamados
Pipeline de Machine Learning para Priorização Automática no Atendimento ao Cliente

📘 1. INTRODUÇÃO

Este projeto apresenta a implementação de um pipeline completo de Machine Learning (ML) voltado à classificação e priorização automatizada de chamados de clientes.

O objetivo é prever a urgência de cada chamado, com base em atributos como dias_atraso, valor_total_divida e texto_chamado, simulando um cenário real de atendimento ao cliente.

O target (variável urgencia) é definido conforme regras de negócio simuladas, onde altos valores de atraso e dívida indicam Alta Urgência.

O pipeline combina dados tabulares e textuais, aplicando técnicas de Processamento de Linguagem Natural (NLP) e aprendizado supervisionado.
Devido ao desbalanceamento natural das classes, a métrica principal escolhida é o F1-Score Ponderado, mais robusta que a acurácia em cenários assimétricos.

⚙️ 2. CONFIGURAÇÃO E GERAÇÃO DE DADOS
2.1 Configuração do Ambiente e Dependências

A etapa inicial (bootstrap) compreende a instalação automatizada de dependências essenciais:

Simulação de dados: faker

Modelos avançados: xgboost, torch, tensorflow

Balanceamento de classes: imbalanced-learn

Manipulação e visualização: pandas, numpy, seaborn

Pré-processamento: TfidfVectorizer, LabelEncoder, StandardScaler

Modelagem: RandomForestClassifier, SVC, XGBClassifier, Keras Sequential

2.2 Estratégia de Carregamento e Dados Sintéticos

A função upload_data() realiza a tentativa de upload de um dataset.
Se não houver arquivo disponível, o script criar_dados_simulados() gera um dataset sintético com 1.000 registros coerentes com a lógica de negócio.

A variável texto_chamado é diretamente correlacionada à urgência, permitindo aplicar NLP supervisionado sobre o texto.

📸 [CÉLULA 1] Visualização do head() do DataFrame e formato (shape).

🔍 3. ANÁLISE EXPLORATÓRIA DE DADOS E PRÉ-PROCESSAMENTO
3.1 Análise de Correlação e Estatísticas

Variáveis categóricas, como urgencia e historico_pagamento, foram codificadas ordinalmente:
Baixa = 0, Média = 1, Alta = 2.

A matriz de correlação evidencia a relação direta entre dias_atraso, valor_total_divida e urgencia_encoded_corr.

📊 [CÉLULA 2.1.1] Heatmap da matriz de correlação.

📈 [CÉLULA 2.1.2] Estatísticas descritivas agrupadas por nível de urgência.

3.2 Pré-processamento de Dados Textuais (NLP)

A função preprocess_text() aplica etapas de normalização:

Conversão para minúsculas;

Remoção de pontuação e símbolos;

Exclusão de stopwords em português.

Os textos são vetorizados por TF-IDF, gerando uma matriz numérica representativa dos chamados.

3.3 Codificação do Target e Análise de Desbalanceamento

A variável urgencia é codificada com LabelEncoder.
Um gráfico de barras mostra o desbalanceamento entre as classes.

⚖️ [CÉLULA 4] Distribuição de amostras por nível de urgência.

3.4 Validação do Sinal Preditivo

A EDA visual confirma o relacionamento entre risco financeiro e urgência, sustentando a coerência do modelo.

💲 [CÉLULA 5] Boxplot de dias_atraso e valor_total_divida por urgencia.

🧩 4. ENGENHARIA DE FEATURES E COMBINAÇÃO HÍBRIDA
4.1 Vetorização TF-IDF

O TfidfVectorizer é configurado com:
ngram_range=(1,2), max_features=500, min_df=2, max_df=0.8.

🗣️ [CÉLULA 6] Gráfico das 15 principais palavras (Top Features) no TF-IDF.

4.2 Fusão e Normalização

As variáveis contínuas são normalizadas com StandardScaler, e as categóricas mantêm hierarquia ordinal.

📊 [CÉLULA 7] Histogramas antes e depois da normalização.

4.3 Divisão Estratificada

A função train_test_split() é utilizada com stratify=y, garantindo a mesma proporção de classes nos conjuntos de treino e teste.

✅ [CÉLULA 8] Comparativo de proporções entre treino e teste.

🤖 5. MODELAGEM E AVALIAÇÃO DE DESEMPENHO
5.1 Modelos Clássicos

Modelos testados:

Random Forest

XGBoost

SVM

O desbalanceamento foi mitigado por class_weight='balanced'.

🎯 [CÉLULA 9] Matrizes de confusão e relatórios de classificação.

5.2 Rede Neural (Deep Learning)

Implementação de rede Sequential (Keras) com:

Camadas densas com ReLU;

Regularização via Dropout(0.5);

Otimizador Adam;

Função de perda categorical_crossentropy.

🧠 [CÉLULA 14] Curvas de Loss e Acurácia.
🎯 [CÉLULA 10] Matriz de confusão da rede neural.

5.3 Análise de Erros e Interpretabilidade

O DataFrame erros_df isola falsos negativos para análise.
Também é avaliado o comportamento dos vetores de suporte (SVM).

🚨 [CÉLULA 11] Erros e falsos negativos.
🔎 [CÉLULA 12–13] Análise dos vetores de suporte e perfis preditivos.

5.4 Comparação de Desempenho

O desempenho foi avaliado com base no F1-Score ponderado.

🏆 [CÉLULA 15] Comparativo de desempenho entre modelos.
📈 [CÉLULA 16] Curvas de aprendizado do modelo vencedor.

🚀 6. DEPLOYMENT E SIMULAÇÃO OPERACIONAL
6.1 Persistência de Artefatos

Os artefatos são salvos em formato .pkl via joblib:

modelo_priorizacao.pkl

tfidf_vectorizer.pkl

scaler.pkl

label_encoder.pkl

Esses arquivos garantem reprodutibilidade e ausência de data leakage.

6.2 Teste de Unidade e Simulação

A função priorizar_chamado() simula a classificação de um novo chamado.

🧪 [CÉLULA 19] Saída de testes unitários com previsões Alta/Média/Baixa.

A simulação batch adiciona a coluna urgencia_prevista ao dataset.

🥇 [CÉLULA 21] Visualização do DataFrame final com predições.

📊 7. BUSINESS INTELLIGENCE (BI) E ANÁLISES ESTRATÉGICAS
7.1 Dashboard de Monitoramento

Painel 2x2 exibindo:

Real vs Previsto;

Precisão por Classe;

Valor Médio de Dívida;

Matriz de Confusão Final.

🖼️ [CÉLULA 22] Dashboard consolidado de desempenho.

7.2 Análises de Segmentação
7.2.1 Segmentação Geográfica

🗺️ [CÉLULA 23] Urgência Prevista por Estado.
♨️ [CÉLULA 26] Mapa Coroplético – Urgência Prevista.
🌎 [CÉLULA 27] Mapa Coroplético – Volume Total de Chamados.

7.2.2 Segmentação Operacional

📞 [CÉLULA 24] Urgência por Tipo de Cliente e Canal de Contato.
⚙️ [CÉLULA 25] Correlação entre Tentativas de Contato e Risco.

🧾 8. CONCLUSÃO

O projeto implementa um pipeline completo de Machine Learning, cobrindo desde o tratamento de dados até o deployment e geração de insights estratégicos.

As variáveis dias_atraso e valor_total_divida se mostraram altamente correlacionadas com a urgência, comprovando a relevância do modelo.

O Random Forest obteve o melhor desempenho, sendo o modelo vencedor.
Todos os artefatos foram salvos para reutilização e integração futura com sistemas de atendimento.

O resultado é uma solução automatizada para priorização de chamados, que proporciona:

Redução de falsos negativos;

Otimização da triagem de tickets;

Apoio à tomada de decisão estratégica.

👨‍💻 Autor: Raphael Henrique

📅 Ano: 2025
🏛️ Instituição: Projeto Acadêmico – Gestão da Tecnologia da Informação/Machine Learning & Deep Learning
🎓 Tema: Inteligência Artificial e Ciência de Dados Aplicada ao Atendimento
