Feature: Depósito via PIX
  Como um usuário autenticado
  Quero realizar um depósito via PIX
  Para adicionar saldo à minha conta

  Background:
    Given que estou autenticado no sistema

  Scenario: Gerar QR Code de depósito com sucesso
    When acesso a área de depósitos
    And seleciono o método "PIX"
    And informo um valor válido para depósito
    And clico em "Gerar QR Code"
    Then o sistema deve exibir um QR Code válido
    And a transação deve ser registrada com status "PENDING"

  Scenario: Confirmar depósito após pagamento
    Given que possuo um depósito PIX pendente
    When o PSP envia o callback de confirmação
    Then a transação deve ser atualizada para "SUCCESS"
    And meu saldo deve ser creditado corretamente

  Scenario: Tentar criar depósito com valor inválido
    When tento gerar um depósito PIX com valor abaixo do mínimo permitido
    Then devo ver a mensagem "Valor inválido"
    And o depósito não deve ser criado
