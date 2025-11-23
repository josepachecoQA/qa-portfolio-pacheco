Feature: Saque via PIX
  Como um usuário autenticado
  Quero solicitar um saque via PIX
  Para retirar meu saldo com segurança

  Background:
    Given que estou autenticado no sistema

  Scenario: Solicitar saque com sucesso
    When acesso a área de saques
    And informo uma chave PIX válida
    And informo um valor disponível para saque
    And clico em "Solicitar Saque"
    Then o sistema deve registrar a solicitação com status "PROCESSING"
    And devo visualizar a confirmação de envio

  Scenario: Saque confirmado pelo PSP
    Given que tenho um saque em processamento
    When o PSP envia o callback de confirmação
    Then o status deve ser atualizado para "SUCCESS"
    And meu saldo deve ser atualizado corretamente

  Scenario: Tentar sacar valor maior que o saldo
    When tento realizar um saque com valor superior ao meu saldo
    Then o sistema deve exibir "Saldo insuficiente"
    And a solicitação de saque não deve ser criada

  Scenario: Tentar sacar com chave PIX inválida
    When informo uma chave PIX inválida
    And clico em "Solicitar Saque"
    Then devo ver a mensagem "Chave PIX inválida"
    And o saque deve ser bloqueado
