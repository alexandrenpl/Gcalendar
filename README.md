# Google Calendar GUI - Enviar Eventos

Aplicação desktop para Windows que permite enviar eventos para o Google Calendar através de um Web App do Google Apps Script.

## Características

- Interface gráfica simples e intuitiva
- Configuração via ficheiro `.env`
- Editor de JSON com validação e formatação
- Templates pré-definidos para eventos
- Envio seguro via HTTP POST com Bearer Token
- Logging de erros técnicos
- Suporta múltiplos eventos num único JSON

## Requisitos

- Python 3.10 ou superior
- Windows 10/11

## Instalação e Execução

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Executar a aplicação

```bash
python gcal_gui.py
```

## Criação do Executável (.exe)

### 1. Instalar PyInstaller

```bash
pip install pyinstaller
```

### 2. Criar executável

```bash
pyinstaller --onefile --windowed gcal_gui.py
```

O executável será criado em `dist/gcal_gui.exe`.

### Comandos rápidos (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --onefile --windowed --name GoogleCalendarGUI gcal_gui.py
```

Após terminar, encontrará `dist/GoogleCalendarGUI.exe`.

**Nota:** Alguns antivírus podem detectar falsos positivos em executáveis criados com PyInstaller. Isto é normal e pode ser ignorado com segurança.

## Configuração

### Ficheiro .env

A aplicação utiliza um ficheiro `.env` para guardar as configurações:

```
WEB_APP_URL=https://script.google.com/macros/s/SEU_SCRIPT_ID/exec
CALENDAR_ID=primary
```

### Como obter as credenciais

1. **Web App URL**: URL do seu Google Apps Script Web App
2. **Calendar ID**: ID do calendário (opcional - o script usa sempre o calendário padrão)

## Utilização

### 1. Configuração

- Preencha os campos de configuração (URL, Calendar ID)
- Clique em "Guardar .env" para persistir as configurações

### 2. Editor de JSON

- Use "Inserir Template teste" para um exemplo básico
- Carregue ficheiros JSON existentes
- Formate o JSON para melhor legibilidade
- Valide a sintaxe antes de enviar

Suporta:
- Evento único (objeto JSON)
- Múltiplos eventos (objeto com chave `events` contendo uma lista)
- Múltiplos eventos como lista no topo (top-level array)

### 3. Envio

- Clique em "Enviar para Web App"
- A resposta aparecerá na área de resposta
- Verifique o status HTTP e o conteúdo da resposta

## Templates de JSON

### Evento único

```json
{
  "title": "Teste ChatGPT",
  "start": "2025-09-22T09:30:00+01:00",
  "end": "2025-09-22T10:00:00+01:00",
  "description": "Evento de teste criado via Web App (Apps Script).",
  "location": "Local de teste"
}
```

### Múltiplos eventos

```json
{
  "events": [
    {
      "title": "Bloco Produtivo 1",
      "start": "2025-09-22T09:00:00+01:00",
      "end": "2025-09-22T11:00:00+01:00",
      "description": "Decidir tarefa concreta de manhã."
    },
    {
      "title": "Almoço + arrumar cozinha",
      "start": "2025-09-22T13:00:00+01:00",
      "end": "2025-09-22T15:00:00+01:00",
      "description": "Preparar almoço, comer e limpar a cozinha."
    }
  ]
}
```

### Múltiplos eventos (lista no topo)

```json
[
  {
    "title": "Evento A",
    "start": "2025-09-23T09:00:00+01:00",
    "end": "2025-09-23T10:00:00+01:00",
    "description": "Descrição do evento A"
  },
  {
    "title": "Evento B",
    "start": "2025-09-23T11:00:00+01:00",
    "end": "2025-09-23T12:00:00+01:00",
    "location": "Local do evento B"
  }
]
```

Notas:
- A app envia um POST por evento ao seu Web App do Apps Script.
- A área de resposta mostra um resumo com sucesso/falha por evento.
- O script usa sempre o calendário padrão (não precisa de `calendarId`).

## Estrutura de Ficheiros

```
Gcalendar/
├── gcal_gui.py          # Aplicação principal
├── requirements.txt     # Dependências Python
├── README.md           # Este ficheiro
├── .env                # Configurações (criado automaticamente)
└── gcal_gui.log        # Log de erros (criado automaticamente)
```

## Resolução de Problemas

### Erro de ligação

- Verifique se o Web App URL está correto
- Confirme que o Web App está publicado e acessível
- Verifique a ligação à internet

### Erro de ligação ao Web App

- **Use o botão "🔧 Debug"** para verificar a configuração atual
- Confirme que o Web App está publicado como "Anyone"
- Verifique se o Web App tem as permissões necessárias para o Google Calendar
- Teste o Web App URL diretamente no browser
- Verifique o ficheiro `gcal_gui.log` para detalhes técnicos

### JSON inválido

- Use o botão "Formatar JSON" para validar a sintaxe
- Verifique se todas as chaves estão entre aspas
- Confirme que vírgulas e chavetas estão corretas

### Ferramentas de Debug

A aplicação inclui várias ferramentas para ajudar na resolução de problemas:

1. **Botão "🔧 Debug"** - Mostra informações detalhadas da configuração atual
2. **Logs detalhados** - Ficheiro `gcal_gui.log` com informações técnicas
3. **Teste de Web App** - Abre o URL diretamente no browser

## Logs

Os erros técnicos são registados no ficheiro `gcal_gui.log` para facilitar a resolução de problemas.

## Licença

Este projeto é fornecido como está, sem garantias.
