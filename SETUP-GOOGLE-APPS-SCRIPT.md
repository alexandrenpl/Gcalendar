# Configuração do Google Apps Script Web App

## Problema Identificado

O erro que está a receber é porque **todos os Web Apps do Google Apps Script precisam de uma função `doGet()`** como ponto de entrada, mesmo que a aplicação seja principalmente para processar POST requests.

## Solução

### 1. Criar o Projeto no Google Apps Script

1. Vá para [script.google.com](https://script.google.com)
2. Clique em "Novo projeto"
3. Apague o código padrão
4. Cole o código do ficheiro `google-apps-script.gs`
5. Guarde o projeto (Ctrl+S)

### 2. Configurar Permissões

1. No menu, vá a "Executar" → "Executar função" → "testScript"
2. Será pedido para autorizar o script
3. Clique em "Revisar permissões"
4. Escolha a sua conta Google
5. Clique em "Avançado" → "Ir para [nome do projeto] (não seguro)"
6. Clique em "Permitir"

### 3. Publicar como Web App

1. No menu, vá a "Implementar" → "Nova implementação"
2. Clique no ícone de engrenagem → "Web app"
3. Configure:
   - **Descrição**: "Google Calendar Web App"
   - **Executar como**: "Eu"
   - **Quem tem acesso**: "Qualquer pessoa"
4. Clique em "Implementar"
5. **Copie o URL gerado** - este é o URL que deve usar na aplicação Python

### 4. Testar o Web App

#### Teste 1: GET Request (deve funcionar agora)
- Abra o URL do Web App no browser
- Deve ver uma resposta JSON com informações do Web App

#### Teste 2: POST Request
- Use a aplicação Python com o URL copiado
- Configure um token (pode ser qualquer string para teste)
- Teste com o template de evento

### 5. Configurar na Aplicação Python

1. Abra a aplicação Python
2. No campo "Web App URL", cole o URL copiado do Google Apps Script
3. No campo "Token", pode usar qualquer string (ex: "test-token")
4. Clique em "Guardar .env"

## Estrutura do Código

### Função `doGet()`
- **Obrigatória** para todos os Web Apps
- Responde a GET requests (quando acede ao URL no browser)
- Retorna informações sobre o Web App

### Função `doPost()`
- Processa POST requests da aplicação Python
- Cria eventos no Google Calendar
- Valida dados e retorna respostas JSON

### Funções Auxiliares
- `testScript()`: Testa se o script está funcionando
- `listCalendars()`: Lista calendários disponíveis

## Formato JSON Esperado

```json
{
  "title": "Título do Evento",
  "start": "2025-01-15T10:00:00+01:00",
  "end": "2025-01-15T11:00:00+01:00",
  "description": "Descrição do evento",
  "location": "Local do evento (opcional)",
  "calendarId": "primary",
  "timeZone": "Europe/Lisbon",
  "reminders": {
    "popupMinutes": 10,
    "emailMinutes": 60
  }
}
```

## Resolução de Problemas

### Erro: "doGet is not defined"
- **Causa**: Função `doGet()` não existe
- **Solução**: Adicione a função `doGet()` ao código

### Erro: "Script not authorized"
- **Causa**: Script não tem permissões
- **Solução**: Execute `testScript()` e autorize as permissões

### Erro: "Calendar not found"
- **Causa**: Calendar ID incorreto
- **Solução**: Use "primary" ou execute `listCalendars()` para ver IDs disponíveis

### Erro: "Access denied"
- **Causa**: Web App não está público
- **Solução**: Configure como "Qualquer pessoa" na implementação

## Logs e Debug

- Use `console.log()` no Google Apps Script para debug
- Verifique os logs na aplicação Python (ficheiro `gcal_gui.log`)
- Use a função "🔧 Debug" na aplicação Python para informações detalhadas

## Segurança

- O Web App está configurado para aceitar qualquer pessoa
- Para produção, considere implementar autenticação adequada
- O token atual é apenas para identificação, não para autenticação real
