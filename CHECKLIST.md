# 🎮 FaceCraft — Checklist de Desenvolvimento

## 1. 🚀 Estrutura e PWA

* [x] Definir estrutura de pastas e arquivos
* [x] Configurar layout mobile-first
* [x] Configurar PWA
* [x] Configurar manifest
* [x] Criar ícones
* [x] Configurar Service Worker
* [x] Configurar acesso à câmera
* [x] Configurar seleção de fotos da galeria
* [x] Testar câmera e seleção de fotos
* [x] **Teste da estrutura, PWA e recursos de imagem**

---

## 2. 📱 Telas, Fluxo e Configurações

### 🧭 Navegação
- [x] Criar `BottomNav`
- [x] Criar navegação para Início
- [x] Criar navegação para Jogos
- [x] Criar navegação para Configurações
- [x] Definir estado ativo da navegação
- [x] Testar navegação inferior

### 🏠 Início
- [x] Definir layout da tela inicial
- [x] Definir informações exibidas
- [x] Definir ações principais
- [x] Testar tela inicial

### 🎮 Jogos
- [ ] Criar tela de Jogos
- [ ] Criar lista/tabela de jogos
- [ ] Criar pesquisa de jogos
- [ ] Definir informações exibidas para cada jogo
- [ ] Criar modal de informações do jogo
- [ ] Exibir tutorial disponível no modal
- [ ] Criar acesso ao tutorial
- [ ] Definir comportamento quando não houver resultado na pesquisa
- [ ] Testar pesquisa
- [ ] Testar abertura e fechamento do modal
- [ ] Testar acesso aos tutoriais

### ⚙️ Configurações
- [ ] Criar tela de Configurações

#### 🎨 Personalização
- [ ] Criar seção Personalização
- [ ] Configurar Tema
- [ ] Configurar Idioma
- [ ] Configurar Notificações

#### 💾 Dados
- [ ] Criar seção Dados
- [ ] Exibir dados utilizados
- [ ] Exibir armazenamento utilizado
- [ ] Criar opção para limpar análises
- [ ] Criar opção para limpar tutoriais personalizados
- [ ] Criar opção para apagar todos os dados
- [ ] Criar modal de confirmação
- [ ] Criar mensagens de sucesso e erro
- [ ] Atualizar armazenamento após exclusão
- [ ] Definir armazenamento local dos dados
- [ ] Testar exclusão dos dados

#### 📱 Aplicativo
- [ ] Criar seção Aplicativo
- [ ] Exibir Versão
- [ ] Exibir Suporte
- [ ] Exibir Criador

### 🔄 Fluxo do aplicativo
- [ ] Definir fluxo completo de navegação
- [ ] Definir fluxo de captura/seleção da fotografia
- [ ] Definir fluxo da análise facial
- [ ] Definir fluxo da seleção do jogo
- [ ] Definir fluxo da conversão para o jogo
- [ ] Definir fluxo do tutorial personalizado
- [ ] Definir fluxo do resultado
- [ ] Definir estados de carregamento
- [ ] Definir mensagens de erro
- [ ] Testar fluxo completo entre as telas

### 🖥️ Telas
- [ ] Definir todas as telas do aplicativo
- [ ] Definir fluxo de navegação
- [ ] Definir comportamento de cada tela
- [ ] Definir componentes necessários
- [ ] Definir informações exibidas em cada tela
- [ ] Definir ações e botões
- [ ] Definir estados de carregamento
- [ ] Definir mensagens de erro
- [ ] Testar navegação entre telas

### ⚙️ Configurações
- [ ] Criar tela de Configurações
- [ ] Criar seção Personalização
- [ ] Configurar Tema
- [ ] Configurar Idioma
- [ ] Configurar Notificações
- [ ] Criar seção Aplicativo
- [ ] Exibir Versão
- [ ] Exibir Suporte
- [ ] Exibir Criador
- [ ] Testar configurações

### 🔄 Fluxo do aplicativo
- [ ] Definir fluxo completo desde a entrada até o resultado
- [ ] Definir fluxo de seleção do jogo
- [ ] Definir fluxo de seleção/captura da fotografia
- [ ] Definir fluxo da análise facial
- [ ] Definir fluxo da conversão para o jogo
- [ ] Definir fluxo do tutorial
- [ ] Definir fluxo do resultado final

---

## 3. 🎮 Banco de Dados e Configuração dos Jogos

> Cada jogo poderá possuir uma estrutura de criação de personagem completamente diferente.

- [ ] Definir arquitetura dos dados
- [x] Criar tabela `games`
- [x] Configurar RLS da tabela `games`
- [x] Criar Storage `games`
- [ ] Analisar estrutura do primeiro jogo
- [ ] Definir estrutura do JSON do primeiro jogo
- [ ] Criar categorias específicas do jogo
- [ ] Criar opções específicas do jogo
- [ ] Criar parâmetros específicos do jogo
- [ ] Definir valores mínimos e máximos quando existirem
- [ ] Definir regras do jogo
- [ ] Definir limitações do jogo
- [ ] Definir dependências entre parâmetros
- [ ] Definir regras de mapeamento facial
- [ ] Criar primeiro JSON de teste
- [ ] Inserir primeiro jogo no banco
- [ ] Enviar JSON para o Storage
- [ ] Implementar consulta dos jogos
- [ ] Implementar carregamento do JSON do jogo selecionado
- [ ] Garantir que o JSON seja carregado somente quando necessário
- [ ] Testar integração Banco + Storage

---

## 4. 🧠 Análise Facial

- [ ] Pesquisar tecnologias de análise facial
- [ ] Escolher biblioteca/modelo de análise facial
- [ ] Configurar biblioteca/modelo
- [ ] Detectar rosto
- [ ] Validar existência de rosto
- [ ] Detectar múltiplos rostos
- [ ] Identificar pontos faciais
- [ ] Extrair características faciais
- [ ] Processar proporções faciais
- [ ] Normalizar dados da análise
- [ ] Definir estrutura dos dados faciais
- [ ] Testar diferentes formatos de rosto
- [ ] Testar diferentes fotografias
- [ ] Teste da análise facial

---

## 5. 🔀 Conversão da Face para o Jogo

- [ ] Ler configuração do jogo
- [ ] Ler parâmetros disponíveis
- [ ] Ler regras e limitações
- [ ] Relacionar características faciais aos parâmetros do jogo
- [ ] Criar sistema de mapeamento
- [ ] Converter características faciais para os valores do jogo
- [ ] Comparar características com opções disponíveis
- [ ] Aplicar limites dos parâmetros
- [ ] Aplicar regras específicas do jogo
- [ ] Resolver dependências entre parâmetros
- [ ] Definir configurações recomendadas
- [ ] Calcular nível de similaridade
- [ ] Organizar resultado por categoria
- [ ] Estruturar resultado para o tutorial
- [ ] Teste da conversão

---

## 6. 📋 Tutorial de Criação do Personagem

- [ ] Criar estrutura do tutorial
- [ ] Gerar sequência de configuração
- [ ] Organizar etapas
- [ ] Mostrar categoria
- [ ] Mostrar parâmetro
- [ ] Mostrar opção recomendada
- [ ] Mostrar valor recomendado
- [ ] Mostrar instruções
- [ ] Permitir avançar entre etapas
- [ ] Permitir voltar entre etapas
- [ ] Mostrar progresso
- [ ] Criar resumo da configuração
- [ ] Adaptar tutorial à estrutura de cada jogo
- [ ] Testar tutorial

---

## 7. 💾 Resultado

- [ ] Criar tela de resultado
- [ ] Exibir configuração final
- [ ] Exibir fotografia utilizada
- [ ] Exibir jogo selecionado
- [ ] Exibir nível de similaridade
- [ ] Exibir resumo das configurações
- [ ] Permitir revisar tutorial
- [ ] Permitir reiniciar processo
- [ ] Permitir salvar resultado
- [ ] Permitir compartilhar resultado
- [ ] Teste do resultado final

---

## 8. 🧪 Testes

### 📷 Imagens
- [ ] Testar diferentes fotografias
- [ ] Testar diferentes formatos de rosto
- [ ] Testar diferentes iluminações
- [ ] Testar fotografias de diferentes resoluções
- [ ] Testar fotografia sem rosto
- [ ] Testar fotografia com múltiplos rostos
- [ ] Testar fotografia inválida

### 🎮 Jogos
- [ ] Testar primeiro jogo
- [ ] Testar diferentes parâmetros
- [ ] Testar diferentes valores
- [ ] Testar regras específicas
- [ ] Testar limitações
- [ ] Testar jogos com estruturas diferentes

### 📱 Aplicativo
- [ ] Testar câmera
- [ ] Testar galeria
- [ ] Testar permissões
- [ ] Testar navegação
- [ ] Testar configurações
- [ ] Testar diferentes tamanhos de tela
- [ ] Testar dispositivos móveis

---

## 9. ⚡ Performance e Segurança

- [ ] Verificar tempo de carregamento
- [ ] Verificar tempo de análise facial
- [ ] Verificar tempo de processamento
- [ ] Verificar carregamento dos JSONs
- [ ] Evitar carregamento desnecessário de configurações
- [ ] Verificar consumo de memória
- [ ] Verificar desempenho em dispositivos móveis
- [ ] Revisar regras do Supabase
- [ ] Revisar políticas de acesso
- [ ] Garantir que chaves privadas não sejam expostas
- [ ] Revisar tratamento de erros

---

## 10. 🚀 Teste Final e Publicação

- [ ] Testar fluxo completo
- [ ] Testar instalação do PWA
- [ ] Testar câmera
- [ ] Testar seleção de fotografia
- [ ] Testar análise facial
- [ ] Testar seleção do jogo
- [ ] Testar carregamento do JSON
- [ ] Testar conversão
- [ ] Testar geração do tutorial
- [ ] Testar resultado final
- [ ] Testar diferentes dispositivos
- [ ] Corrigir problemas encontrados
- [ ] Revisar projeto
- [ ] Revisar estrutura de arquivos
- [ ] Atualizar README
- [ ] Criar versão final
- [ ] Publicar aplicação