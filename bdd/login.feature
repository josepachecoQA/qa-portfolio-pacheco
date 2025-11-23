Feature: Login do usuário
  Como um usuário do sistema
  Quero autenticar com email e senha válidos
  Para acessar minha conta com segurança

  Scenario: Login com sucesso
    Given que estou na página de login
    When informo um email válido
    And informo uma senha válida
    And clico em "Entrar"
    Then devo ser autenticado com sucesso
    And devo visualizar o dashboard

  Scenario: Login com senha incorreta
    Given que estou na página de login
    When informo um email válido
    And informo uma senha inválida
    And clico em "Entrar"
    Then o sistema deve exibir a mensagem "Credenciais inválidas"

  Scenario: Login com email inválido
    Given que estou na página de login
    When informo um email inexistente
    And informo uma senha válida
    And clico em "Entrar"
    Then devo ver o alerta "Usuário não encontrado"
