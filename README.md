# 📊 Isert_dados - Manual de Uso

**Repositório para inserção de dados em banco de dados SQL via CVS**

---

## 📋 Descrição

Este repositório contém scripts Python para facilitar a importação e inserção de dados em bancos de dados SQL através de arquivos CVS (Comma Separated Values). O projeto automatiza o processo de leitura, validação e inserção de dados.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.x** - Linguagem principal
- **SQL** - Banco de dados
- **CVS** - Formato de dados

---

## 📁 Estrutura do Projeto

```
Isert_dados/
├── insert_Log.py          # Script para registrar logs das operações
├── insert_dados_gov.py    # Script para inserir dados governamentais
├── README.md              # Este arquivo
└── .github/               # Configurações do GitHub
```

---

## 🚀 Como Usar

### Pré-requisitos

- Python 3.x instalado
- Acesso ao banco de dados SQL
- Arquivo CVS com os dados a serem importados

### Instalação

1. **Clone o repositório**
   ```bash
   git clone https://github.com/yungGenos/Isert_dados.git
   cd Isert_dados
   ```

2. **Instale as dependências** (se houver arquivo `requirements.txt`)
   ```bash
   pip install -r requirements.txt
   ```

### Execução dos Scripts

#### 1. **insert_dados_gov.py** - Inserir Dados Governamentais

Este script é responsável pela inserção de dados governamentais no banco de dados.

```bash
python insert_dados_gov.py
```

**O que faz:**
- Lê arquivo CVS com dados governamentais
- Valida os dados
- Insere os registros no banco de dados SQL

#### 2. **insert_Log.py** - Registrar Logs

Este script gerencia e registra logs de todas as operações realizadas.

```bash
python insert_Log.py
```

**O que faz:**
- Registra operações bem-sucedidas
- Documenta erros e exceções
- Mantém histórico das inserções

---

## ⚙️ Configuração

Antes de usar, configure:

1. **Credenciais do Banco de Dados**
   - Abra os scripts Python
   - Configure o host, usuário, senha e nome do banco de dados

2. **Caminho dos Arquivos CVS**
   - Especifique o caminho correto do arquivo CVS a ser importado

3. **Configurações de Log**
   - Defina o local onde os logs serão salvos

---

## 📝 Exemplos de Uso

### Exemplo 1: Inserir dados de um arquivo CVS

```bash
python insert_dados_gov.py --arquivo dados.csv --banco producao
```

### Exemplo 2: Executar com log detalhado

```bash
python insert_Log.py --verbose
```

---

## ⚠️ Observações Importantes

- **Backup**: Sempre faça backup do banco de dados antes de inserir dados
- **Validação**: Os scripts validam os dados automaticamente
- **Logs**: Verifique os logs para monitorar o progresso das operações
- **Formato CVS**: Certifique-se de que o arquivo segue o padrão esperado

---

## 🐛 Troubleshooting

### Erro: Conexão recusada ao banco de dados
- Verifique se o servidor SQL está ativo
- Confirme as credenciais de acesso
- Verifique o host e porta configurados

### Erro: Arquivo CVS não encontrado
- Verifique o caminho completo do arquivo
- Certifique-se de que o arquivo tem permissão de leitura

### Erro: Dados inválidos
- Revise o formato dos dados no arquivo CVS
- Consulte os logs para identificar a linha com erro

---

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique os logs gerados pelo script
2. Abra uma issue no repositório
3. Entre em contato com o desenvolvedor

---

## 📄 Licença

Este projeto é fornecido como está. Use por sua conta e risco.

---

## 👨‍💻 Autor

**yungGenos**  
GitHub: https://github.com/yungGenos

---

## 📅 Última Atualização

10 de Fevereiro de 2026
