<div align="center">

# 🚀 SAT RPA 1.0.1

### Automação Inteligente para Exportação de NF-e e NFC-e
**Portal SAT • Secretaria da Fazenda de Santa Catarina**

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-Automation-2EAD33?style=for-the-badge&logo=playwright&logoColor=white)
![Windows](https://img.shields.io/badge/Windows-10/11-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![Status](https://img.shields.io/badge/Status-Em%20Produção-success?style=for-the-badge)

---

Automação desenvolvida para realizar consultas, solicitações de exportação e download de **NF-e** e **NFC-e** diretamente do Portal SAT da Secretaria da Fazenda de Santa Catarina.

</div>

---

# 📌 Funcionalidades

✅ Login automático no Portal SAT

✅ Consulta de NF-e

✅ Consulta de NFC-e

✅ Solicitação automática de exportação

✅ Monitoramento do processamento

✅ Download automático dos arquivos

✅ Organização automática das pastas por competência

✅ Processamento em lote de empresas

✅ Geração de relatório final

---

# 📂 Estrutura do Projeto

```text
SAT_RPA/
│
├── main.py
├── config.json
├── requirements.txt
├── empresas.xlsx
│
├── modules/
│   ├── navegador.py
│   ├── login.py
│   ├── consulta.py
│   ├── exportacao.py
│   ├── download.py
│   ├── empresas.py
│   ├── datas.py
│   ├── relatorio.py
│   └── logger.py
│
├── ChromeProfile/
│
├── screenshots/
│
└── README.md
```

---

# ⚙️ Requisitos

- Python 3.11 ou superior
- Google Chrome
- Playwright
- Microsoft Excel
- Acesso ao Portal SAT

---

# 📦 Instalação

Clone o projeto

```bash
git clone https://github.com/seuusuario/SAT_RPA.git
```

Instale as dependências

```bash
pip install -r requirements.txt
```

Instale os navegadores do Playwright

```bash
playwright install
```

---

# 🔧 Configuração

Configure o arquivo:

```text
config.json
```

Exemplo:

```json
{
    "usuario": "SEU_USUARIO",
    "senha": "SUA_SENHA"
}
```

---

# 📄 Empresas

As empresas são carregadas automaticamente pelo arquivo

```text
empresas.xlsx
```

Modelo:

| Empresa | Nome | CNPJ |
|---------:|:-------------|----------------|
| 1001 | Empresa Alpha | 00000000000000 |
| 1002 | Empresa Beta | 11111111111111 |

---

# 🚀 Fluxo da Automação

```text
┌────────────────────────────┐
│ Início                     │
└──────────────┬─────────────┘
               │
               ▼
      Login no Portal SAT
               │
               ▼
      Leitura das Empresas
               │
               ▼
      Consulta de NF-e
               │
               ▼
     Solicita Exportação
               │
               ▼
 Aguarda Processamento SAT
               │
               ▼
      Download do Arquivo
               │
               ▼
      Consulta de NFC-e
               │
               ▼
     Solicita Exportação
               │
               ▼
 Aguarda Processamento SAT
               │
               ▼
      Download do Arquivo
               │
               ▼
      Geração do Relatório
               │
               ▼
             Fim
```

---

# 📁 Organização dos Downloads

Os arquivos são salvos automaticamente na seguinte estrutura:

```text
Z:\SAT\downloads
│
├── 1001 - Empresa Alpha
│   ├── 2026-06
│   │      NFE.xlsx
│   │      NFCE.xlsx
│   │
│   ├── 2026-07
│   │      NFE.xlsx
│   │      NFCE.xlsx
```

> A competência da pasta corresponde ao período exportado no Portal SAT.

---

# 📊 Relatório

Ao término da execução é gerado um relatório contendo:

- Empresa
- Nome
- CNPJ
- Status da NF-e
- Status da NFC-e
- Resultado Final
- Observações
- Data/Hora da execução

---

# 🛠 Tecnologias

- 🐍 Python
- 🎭 Playwright
- 📊 OpenPyXL
- 📄 Pandas
- 🌐 Chrome Remote Debugging

---

# 📈 Características

- ✔ Código modular
- ✔ Fácil manutenção
- ✔ Processamento em lote
- ✔ Organização automática dos downloads
- ✔ Reutilização da sessão do Chrome
- ✔ Tratamento de erros
- ✔ Relatório automático

---

# 📜 Licença

Projeto desenvolvido para automação interna do Portal SAT da Secretaria da Fazenda de Santa Catarina.

---

<div align="center">

## 🚀 SAT RPA 1.0.1

**Automatizando processos fiscais com rapidez, organização e confiabilidade.**

</div>
