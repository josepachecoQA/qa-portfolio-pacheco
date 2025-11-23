🚀 Testes de API — Portfólio QA Pleno
Autor: José Pacheco da Silva Neto

Aqui estão exemplos reais de testes de API utilizados para validação de integrações, fluxos financeiros e endpoints críticos.

📌 Conteúdo desta pasta

Coleções Postman
→ Testes organizados por módulo (login, usuários, pagamentos, PIX etc.)

Scripts automatizados
→ Testes usando Postman + JavaScript
→ Exemplo de execução via Newman

JSON de testes
→ Exemplos de payloads reais usados para validação

Chamadas reais de API
→ Requests e responses documentados
→ Logs e cenários de teste

🛠️ Ferramentas utilizadas

Postman

Newman (CLI)

Node.js

Swagger / OpenAPI

OpenSearch (validação de logs)

▶️ Como executar automatizado (Newman)
newman run Collection.postman_collection.json -e ambiente.postman_environment.json --reporters cli,html

📁 Arquivos incluídos (ou a incluir)

Collection.postman_collection.json ← (vou gerar para você no próximo passo)

ambiente.postman_environment.json

Scripts JS para pré-execução e testes

Exemplos de payloads:

pix-payload.json

login-payload.json

saque-payload.json

🔥 Exemplos de scripts Postman
🔹 Script de Teste — Validar status 200
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

🔹 Script de Teste — Validar campo obrigatório
pm.test("Valida campo 'transactionID'", function () {
    var json = pm.response.json();
    pm.expect(json).to.have.property("transactionID");
});

🌐 Exemplos de endpoints incluídos

POST /auth/login

POST /payments/payment/checkout

GET /payments/transaction/verify

POST /pix/deposit

POST /pix/withdraw
