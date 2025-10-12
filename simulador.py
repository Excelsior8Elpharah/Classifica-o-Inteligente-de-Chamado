# %% [markdown]
# # 🎯 Simulador de Atendimento de Cobrança - Claro
#
# Este simulador reproduz o ambiente real de trabalho em um call center de cobrança, integrando:
# - **SAAS**: Discador com dados básicos dos clientes
# - **PS8**: Sistema de registro de atendimentos
# - **TOTEM**: Geração de boletos
#
# Todos os dados são salvos automaticamente em arquivos CSV para uso posterior nas análises de Machine Learning.
# %%
import pandas as pd
import numpy as np
import time
import datetime
from datetime import date
import os
from google.colab import files
from faker import Faker
# Criar diretório para os dados se não existir
os.makedirs('/content/dados_simulados', exist_ok=True)
# Caminhos dos arquivos CSV
SAAS_FILE = '/content/dados_simulados/saas_clientes.csv'
PS8_FILE = '/content/dados_simulados/ps8_registros.csv'
TOTEM_FILE = '/content/dados_simulados/totem_boletos.csv'
# %% [markdown]
# ## 🏢 Classe para Simulação do SAAS (Discador)
# %%
class SistemaSAAS:
    def __init__(self, arquivo_saas=SAAS_FILE):
        self.arquivo_saas = arquivo_saas
        self.clientes = self.carregar_clientes()

    def carregar_clientes(self):
        """Carrega clientes do arquivo CSV ou cria dados iniciais"""
        try:
            df = pd.read_csv(self.arquivo_saas)
            print(f"✅ Dados SAAS carregados: {len(df)} clientes")
            return df.to_dict('records')
        except FileNotFoundError:
            print("📝 Arquivo SAAS não encontrado. Iniciando com lista vazia.")
            return []

    def salvar_clientes(self):
        """Salva clientes no arquivo CSV"""
        if self.clientes:
            df = pd.DataFrame(self.clientes)
            df.to_csv(self.arquivo_saas, index=False)
            print(f"💾 SAAS salvo: {len(self.clientes)} clientes")

    def buscar_cliente_por_ban(self, ban):
        """Busca cliente pelo número BAN"""
        for cliente in self.clientes:
            if str(cliente.get('ban')) == str(ban):
                return cliente
        return None

    def adicionar_cliente(self, cliente):
        """Adiciona novo cliente ao SAAS"""
        if not self.buscar_cliente_por_ban(cliente['ban']):
            self.clientes.append(cliente)
            self.salvar_clientes()
            print(f"✅ Cliente {cliente['nome']} adicionado ao SAAS")
            return True
        else:
            print("⚠️ Cliente já existe no SAAS")
            return False
# %% [markdown]
# ## 📋 Classe para Simulação do PS8 (Registro de Atendimentos)
# %%
class SistemaPS8:
    def __init__(self, arquivo_ps8=PS8_FILE):
        self.arquivo_ps8 = arquivo_ps8
        self.registros = self.carregar_registros()

    def carregar_registros(self):
        """Carrega registros do arquivo CSV"""
        try:
            df = pd.read_csv(self.arquivo_ps8)
            print(f"✅ Dados PS8 carregados: {len(df)} registros")
            return df.to_dict('records')
        except FileNotFoundError:
            print("📝 Arquivo PS8 não encontrado. Iniciando com lista vazia.")
            return []

    def salvar_registros(self):
        """Salva registros no arquivo CSV"""
        if self.registros:
            df = pd.DataFrame(self.registros)
            df.to_csv(self.arquivo_ps8, index=False)
            print(f"💾 PS8 salvo: {len(self.registros)} registros")

    def adicionar_registro(self, registro):
        """Adiciona novo registro de atendimento"""
        # Gerar ID automático
        if self.registros:
            ultimo_id = max([r.get('id_registro', 0) for r in self.registros])
            novo_id = ultimo_id + 1
        else:
            novo_id = 1

        registro_completo = {
            'id_registro': novo_id,
            'data_atendimento': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            **registro
        }

        self.registros.append(registro_completo)
        self.salvar_registros()
        print(f"✅ Registro PS8 adicionado: {registro_completo['resultado']}")
        return registro_completo
# %% [markdown]
# ## 🧾 Classe para Simulação do TOTEM (Geração de Boletos)
# %%
class SistemaTOTEM:
    def __init__(self, arquivo_totem=TOTEM_FILE):
        self.arquivo_totem = arquivo_totem
        self.boletos = self.carregar_boletos()

    def carregar_boletos(self):
        """Carrega boletos do arquivo CSV"""
        try:
            df = pd.read_csv(self.arquivo_totem)
            print(f"✅ Dados TOTEM carregados: {len(df)} boletos")
            return df.to_dict('records')
        except FileNotFoundError:
            print("📝 Arquivo TOTEM não encontrado. Iniciando com lista vazia.")
            return []

    def salvar_boletos(self):
        """Salva boletos no arquivo CSV"""
        if self.boletos:
            df = pd.DataFrame(self.boletos)
            df.to_csv(self.arquivo_totem, index=False)
            print(f"💾 TOTEM salvo: {len(self.boletos)} boletos")

    def gerar_boleto(self, ban, valor, dias_vencimento=5):
        """Gera novo boleto"""
        # Gerar ID automático
        if self.boletos:
            ultimo_id = max([b.get('id_boleto', 0) for b in self.boletos])
            novo_id = ultimo_id + 1
        else:
            novo_id = 1

        # Gerar código de barras simulado
        codigo_barras = ''.join([str(np.random.randint(0, 9)) for _ in range(44)])

        novo_boleto = {
            'id_boleto': novo_id,
            'ban': str(ban),
            'valor': float(valor),
            'data_emissao': date.today().strftime("%Y-%m-%d"),
            'data_vencimento': (date.today() + datetime.timedelta(days=dias_vencimento)).strftime("%Y-%m-%d"),
            'codigo_barras': codigo_barras,
            'status': 'emitido'
        }

        self.boletos.append(novo_boleto)
        self.salvar_boletos()
        print(f"✅ Boleto gerado: R$ {valor:.2f} - Vencimento: {novo_boleto['data_vencimento']}")
        return novo_boleto
# %% [markdown]
# ## ✅ Classe para o Checklist Interativo
# %%
class Checklist:
    def __init__(self):
        self.itens = {
            1: {"descricao": "Confirmar nome completo ou CPF.", "concluido": False},
            2: {"descricao": "Informar atraso e valor.", "concluido": False},
            3: {"descricao": "Valorizar desconto e priorizar pagamento imediato.", "concluido": False},
            4: {"descricao": "Confirmar telefone e email.", "concluido": False},
            5: {"descricao": "Ofertar Débito Automático (DCC).", "concluido": False},
            6: {"descricao": "Informar prazo de religação (72h após pagamento).", "concluido": False},
            7: {"descricao": "Pesquisa de inadimplência.", "concluido": False},
            8: {"descricao": "Informar ações de cobrança (juros, multas, etc).", "concluido": False},
            9: {"descricao": "Repassar o acordo (confirmar data e valor).", "concluido": False},
            10: {"descricao": "Perguntar se o cliente tem dúvidas.", "concluido": False}
        }
    def marcar_concluido(self, numero_item):
        if numero_item in self.itens:
            self.itens[numero_item]["concluido"] = True
    def exibir_status(self):
        print("\n✅ CHECKLIST DO ATENDIMENTO - STATUS")
        for num, item in self.itens.items():
            status = "✅ CONCLUÍDO" if item["concluido"] else "❌ PENDENTE"
            print(f"{status}: {num}. {item['descricao']}")
        print("\n---")
# %% [markdown]
# ## 💰 Classe de Negociação do Cliente (Adaptada)
# %%
class NegociacaoCliente:
    def __init__(self, cliente, ps8, totem):
        """
        Inicializa a classe de negociação com dados do cliente.
        """
        self.nome_cliente = cliente['nome']
        self.ban_cliente = cliente['ban']
        self.faturas = cliente['faturas']
        self.faturas_atrasadas = len(self.faturas)
        self.valor_total_divida = sum(fatura['valor'] for fatura in self.faturas)
        self.ps8 = ps8
        self.totem = totem

        self.script_negociacao = {
            "saudacao": f"Olá, {self.nome_cliente}. Meu nome é Cláudia, e estou falando da Claro. O motivo do meu contato é sobre as faturas em atraso do seu serviço.",
            "confirmacao_total": f"Para confirmar, posso falar sobre o pagamento das {self.faturas_atrasadas} faturas vencidas, que totalizam R$ {self.valor_total_divida:.2f}?",
            "opcoes_pagamento": {
                "a_vista": "1. Pagamento à vista (cartão ou boleto)",
                "parcelamento": "2. Parcelamento com entrada",
                "outro": "3. Outra condição/prazo"
            }
        }
    def iniciar_negociacao(self):
        """
        Simula a negociação com o cliente.
        """
        print("--- Negociação Iniciada ---")
        print(self.script_negociacao["saudacao"])
        time.sleep(1)
        print(self.script_negociacao["confirmacao_total"])

        input("\nPressione Enter para simular a resposta do cliente...\n")
        print("Atendente: Vamos às opções de pagamento.")

        return self.negociar_pagamento(self.faturas)

    def negociar_pagamento(self, faturas_para_negociar):
        """
        Lógica central de negociação com opções de pagamento.
        """
        valor_negociacao = sum(fatura['valor'] for fatura in faturas_para_negociar)
        num_faturas = len(faturas_para_negociar)

        print(f"\n--- Negociação de {num_faturas} Fatura(s) - Total: R$ {valor_negociacao:.2f} ---")
        print("Opções disponíveis:")
        for key, value in self.script_negociacao["opcoes_pagamento"].items():
            print(f"  {value}")

        resposta = input("\nEscolha a opção (1/2/3): ").strip()

        if resposta == "1":
            # Pagamento à vista
            boleto = self.totem.gerar_boleto(self.ban_cliente, valor_negociacao)
            registro = {
                'ban': self.ban_cliente,
                'tipo_atendimento': 'cobrança',
                'resultado': 'pagamento_avista',
                'valor_negociado': valor_negociacao,
                'metodo_pagamento': 'boleto',
                'observacoes': 'Cliente optou por pagamento à vista via boleto'
            }
            self.ps8.adicionar_registro(registro)
            return {"resultado": "pagamento_avista", "valor": valor_negociacao}

        elif resposta == "2":
            # Parcelamento
            entrada = max(25.0, float(input("Valor da entrada (mínimo R$ 25,00): R$ ")))
            parcelas = int(input("Número de parcelas: "))

            boleto_entrada = self.totem.gerar_boleto(self.ban_cliente, entrada, 3)
            registro = {
                'ban': self.ban_cliente,
                'tipo_atendimento': 'cobrança',
                'resultado': 'parcelamento',
                'valor_negociado': valor_negociacao,
                'metodo_pagamento': 'parcelado',
                'observacoes': f'Parcelamento em {parcelas}x com entrada de R$ {entrada:.2f}'
            }
            self.ps8.adicionar_registro(registro)
            return {"resultado": "parcelamento", "entrada": entrada, "parcelas": parcelas}

        else:
            # Outra situação
            registro = {
                'ban': self.ban_cliente,
                'tipo_atendimento': 'cobrança',
                'resultado': 'negociacao_pendente',
                'valor_negociado': 0,
                'metodo_pagamento': 'nenhum',
                'observacoes': 'Cliente não aceitou nenhuma opção de pagamento'
            }
            self.ps8.adicionar_registro(registro)
            return {"resultado": "negociacao_pendente"}
# %% [markdown]
# ## 📞 Classe Principal de Atendimento (Adaptada)
# %%
class AtendimentoClaro:
    def __init__(self, cliente):
        self.cliente = cliente
        self.saas = SistemaSAAS()
        self.ps8 = SistemaPS8()
        self.totem = SistemaTOTEM()
        self.checklist = Checklist()

        # Adicionar cliente ao SAAS se não existir
        if not self.saas.buscar_cliente_por_ban(cliente['ban']):
            cliente_saas = {
                'ban': cliente['ban'],
                'nome': cliente['nome'],
                'cpf': cliente['cpf'],
                'telefone': cliente['telefone'],
                'email': cliente['email'],
                'produto': cliente['produto'],
                'status': 'ativo'
            }
            self.saas.adicionar_cliente(cliente_saas)

        self.negociacao = NegociacaoCliente(cliente, self.ps8, self.totem)
    def abertura_atendimento(self):
        """Etapa 1: Abertura e verificação inicial."""
        print("📞 ETAPA 1 - ABERTURA DO ATENDIMENTO")
        print(f"\n[FALA AO CLIENTE] Bom dia! Falo com o(a) Sr(a). {self.cliente['nome']}?")
        print("Meu nome é Cláudia, falo em nome da Claro.")
        print("Para confirmar, poderia me informar seu nome completo ou CPF?")

        input("\nPressione Enter para simular a confirmação do cliente...")
        self.checklist.marcar_concluido(1)

        print("\n[FALA AO CLIENTE] Por favor, aguarde um momento enquanto consulto seus dados...")
        time.sleep(2)

        print(f"\n[AÇÃO NO SISTEMA] Cliente identificado: {self.cliente['nome']}")
        print(f"BAN: {self.cliente['ban']} | CPF: {self.cliente['cpf']}")
        print(f"Faturas em atraso: {len(self.cliente['faturas'])}")
        print(f"Valor total: R$ {self.negociacao.valor_total_divida:.2f}")
    def iniciar_negociacao(self):
        """Etapa 2: Negociação e identificação do motivo."""
        print("\n" + "="*50)
        print("📞 ETAPA 2 - INÍCIO DA NEGOCIAÇÃO")
        print("="*50)

        print(f"\n[FALA AO CLIENTE] Sr(a). {self.cliente['nome']}, estou entrando em contato")
        print(f"referente às {len(self.cliente['faturas'])} faturas em atraso,")
        print(f"totalizando R$ {self.negociacao.valor_total_divida:.2f}.")

        self.checklist.marcar_concluido(2)

        motivo = input("\n[AÇÃO] Motivo do atraso (digite breve descrição): ")
        self.checklist.marcar_concluido(7)

        print("[FALA AO CLIENTE] Entendo sua situação. Vamos encontrar a melhor solução.")

        # Iniciar negociação
        resultado = self.negociacao.iniciar_negociacao()
        self.checklist.marcar_concluido(3)
        self.checklist.marcar_concluido(4)
        self.checklist.marcar_concluido(9)

        return resultado
    def oferecer_dcc(self):
        """Oferta do Débito Automático"""
        print("\n" + "="*50)
        print("📞 ETAPA 3 - OFERTA DE DÉBITO AUTOMÁTICO")
        print("="*50)

        print("\n[FALA AO CLIENTE] Sr(a). {self.cliente['nome']}, a Claro oferece")
        print("débito automático com desconto de R$ 5,00 em todas as faturas.")
        print("Gostaria de conhecer melhor essa opção?")

        resposta = input("\n[AÇÃO] Cliente interessado? (s/n): ").lower()

        if resposta == 's':
            print("\n[FALA AO CLIENTE] Excelente! O débito automático é seguro")
            print("e evita esquecimentos. Posso enviar mais informações?")
            self.checklist.marcar_concluido(5)
        else:
            print("\n[FALA AO CLIENTE] Sem problemas. Continuando com nosso atendimento...")
    def encerrar_atendimento(self):
        """Etapa final do atendimento"""
        print("\n" + "="*50)
        print("📞 ETAPA FINAL - ENCERRAMENTO")
        print("="*50)

        print("\n[FALA AO CLIENTE] Para evitar bloqueios e negativação do seu CPF,")
        print("recomendo que regularize sua situação o mais breve possível.")

        self.checklist.marcar_concluido(8)

        duvidas = input("\n[AÇÃO] Cliente tem dúvidas? (s/n): ").lower()
        if duvidas == 'n':
            self.checklist.marcar_concluido(10)

        print("\n[FALA AO CLIENTE] Obrigada pelo contato. Tenha um ótimo dia!")
        print("Qualquer dúvida, estamos à disposição.")
    def registrar_ps8(self):
        """Registro final no PS8"""
        print("\n" + "="*50)
        print("💻 ETAPA - REGISTRO NO PS8")
        print("="*50)

        print("\n[AÇÃO NO PS8] Registrando atendimento...")
        time.sleep(1)

        registro_final = {
            'ban': self.cliente['ban'],
            'tipo_atendimento': 'cobrança',
            'resultado': 'atendimento_concluido',
            'valor_negociado': self.negociacao.valor_total_divida,
            'metodo_pagamento': 'informar_nos_sistemas',
            'observacoes': 'Atendimento de cobrança concluído com sucesso'
        }

        self.ps8.adicionar_registro(registro_final)
        print("✅ Registro PS8 concluído")
    def executar_atendimento(self):
        """Executa o fluxo completo do atendimento"""
        try:
            self.abertura_atendimento()
            self.iniciar_negociacao()
            self.oferecer_dcc()
            self.encerrar_atendimento()
            self.registrar_ps8()

            # Mostrar checklist final
            print("\n" + "="*50)
            print("✅ CHECKLIST FINAL")
            print("="*50)
            self.checklist.exibir_status()

            print("\n🎉 ATENDIMENTO CONCLUÍDO COM SUCESSO!")
            print("💾 Dados salvos nos sistemas SAAS, PS8 e TOTEM")

        except Exception as e:
            print(f"❌ Erro durante o atendimento: {e}")
# %% [markdown]
# ## 📋 Funções Auxiliares
# %%
def parse_faturas(faturas_input):
    """
    Converte texto de faturas para lista de dicionários.
    Formato: "DATA R$ VALOR"
    Exemplo: "01/01/2024 R$ 99,90"
    """
    faturas = []
    for linha in faturas_input.strip().split('\n'):
        if 'R$' in linha:
            partes = linha.split('R$')
            if len(partes) == 2:
                data = partes[0].strip()
                valor_str = partes[1].strip().replace(',', '.')
                try:
                    valor = float(valor_str)
                    faturas.append({'vencimento': data, 'valor': valor})
                except ValueError:
                    print(f"⚠️ Valor inválido: {valor_str}")
    return faturas
def carregar_dados_exemplo():
    """Carrega dados de exemplo se os arquivos estiverem vazios"""
    saas = SistemaSAAS()
    ps8 = SistemaPS8()
    totem = SistemaTOTEM()

    # Adicionar exemplo se não houver dados
    if not saas.clientes:
        cliente_exemplo = {
            'ban': '100000001',
            'nome': 'João Silva',
            'cpf': '123.456.789-00',
            'telefone': '(11) 99999-9999',
            'email': 'joao.silva@email.com',
            'produto': 'CLARO NET VIRTUA',
            'status': 'ativo'
        }
        saas.adicionar_cliente(cliente_exemplo)

    if not ps8.registros:
        registro_exemplo = {
            'ban': '100000001',
            'tipo_atendimento': 'cobrança',
            'resultado': 'exemplo',
            'valor_negociado': 150.0,
            'metodo_pagamento': 'boleto',
            'observacoes': 'Registro de exemplo'
        }
        ps8.adicionar_registro(registro_exemplo)

    if not totem.boletos:
        totem.gerar_boleto('100000001', 150.0)
# %% [markdown]
# ## 🚀 Execução Principal do Simulador
# %%
# Carregar dados de exemplo se necessário
carregar_dados_exemplo()
print("🎯 SIMULADOR DE ATENDIMENTO - CLARO COBRANÇA")
print("="*55)
# Solicitar dados do cliente
print("\n📝 DIGITE OS DADOS DO CLIENTE:")
ban = input("BAN do cliente: ").strip() or "100000002"
nome = input("Nome do cliente: ").strip() or "Maria Santos"
cpf = input("CPF do cliente: ").strip() or "987.654.321-00"
telefone = input("Telefone: ").strip() or "(11) 98888-8888"
email = input("Email: ").strip() or "maria.santos@email.com"
produto = input("Produto: ").strip() or "CLARO FIXO + INTERNET"
# Solicitar faturas
print("\n💳 DIGITE AS FATURAS EM ATRASO (formato: DD/MM/AAAA R$ VALOR)")
print("Exemplo: 01/01/2024 R$ 99,90")
print("Pressione Enter duas vezes para finalizar:")
faturas_input = ""
while True:
    linha = input()
    if not linha:
        break
    faturas_input += linha + "\n"
# Processar faturas
faturas = parse_faturas(faturas_input)
if not faturas:
    print("⚠️ Nenhuma fatura válida. Usando exemplo...")
    faturas = [{'vencimento': '01/01/2024', 'valor': 99.90}]
# Criar cliente
cliente = {
    "ban": ban,
    "nome": nome,
    "cpf": cpf,
    "telefone": telefone,
    "email": email,
    "produto": produto,
    "faturas": faturas
}
# Executar atendimento
print("\n" + "="*55)
print("🚀 INICIANDO ATENDIMENTO")
print("="*55)
atendimento = AtendimentoClaro(cliente)
atendimento.executar_atendimento()
# %% [markdown]
# ## 📊 Visualização dos Dados Gerados
# %%
# Mostrar dados gerados
print("\n" + "="*55)
print("📊 DADOS GERADOS NOS SISTEMAS")
print("="*55)
# SAAS
saas_df = pd.read_csv(SAAS_FILE) if os.path.exists(SAAS_FILE) else pd.DataFrame()
print(f"\n📋 SAAS - Clientes ({len(saas_df)} registros):")
if not saas_df.empty:
    display(saas_df.tail())
else:
    print("Nenhum dado disponível")
# PS8
ps8_df = pd.read_csv(PS8_FILE) if os.path.exists(PS8_FILE) else pd.DataFrame()
print(f"\n📋 PS8 - Registros ({len(ps8_df)} registros):")
if not ps8_df.empty:
    display(ps8_df.tail())
else:
    print("Nenhum dado disponível")
# TOTEM
totem_df = pd.read_csv(TOTEM_FILE) if os.path.exists(TOTEM_FILE) else pd.DataFrame()
print(f"\n📋 TOTEM - Boletos ({len(totem_df)} registros):")
if not totem_df.empty:
    display(totem_df.tail())
else:
    print("Nenhum dado disponível")
# %% [markdown]
# ## 💾 Download dos Arquivos CSV
# %%
# Download dos arquivos CSV
def download_arquivos():
    arquivos = [SAAS_FILE, PS8_FILE, TOTEM_FILE]
    for arquivo in arquivos:
        if os.path.exists(arquivo):
            files.download(arquivo)
            print(f"📥 Download: {arquivo}")
        else:
            print(f"⚠️ Arquivo não encontrado: {arquivo}")
print("💾 DOWNLOAD DOS ARQUIVOS CSV:")
print("Os arquivos contêm todos os dados simulados para uso no projeto de ML")
download_arquivos()