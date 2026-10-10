# 🎮 FaceCraft — Checklist de Desenvolvimento

Aplicativo web progressivo (PWA), com foco em dispositivos móveis, que analisa características faciais de uma fotografia e auxilia o usuário a recriar seu rosto na personalização de personagens de diferentes jogos.

**Legenda**
- [x] Implementado ou configurado
- [ ] Pendente de implementação, validação ou teste

---

## 1. 🚀 Estrutura e PWA

- [x] Definir estrutura de pastas e arquivos
- [x] Configurar arquitetura com Vue 3 e TypeScript
- [x] Configurar layout mobile-first
- [x] Configurar Vue Router
- [x] Configurar PWA
- [x] Configurar manifest
- [x] Criar ícones do aplicativo
- [x] Configurar Service Worker
- [x] Configurar atualização automática do PWA
- [x] Configurar acesso à câmera
- [x] Configurar seleção de fotografias da galeria
- [x] Testar estrutura, PWA e recursos de imagem
- [ ] Validar instalação em diferentes dispositivos móveis
- [ ] Validar atualização da aplicação instalada

---

## 2. 📱 Telas, Navegação e Configurações

### 🧭 Navegação

- [x] Criar `BottomNav`
- [x] Criar navegação para Início
- [x] Definir rota para Jogos
- [x] Definir rota para Configurações
- [x] Implementar estado visual da navegação ativa
- [x] Melhorar seleção das telas no `BottomNav`
- [x] Criar header
- [x] Testar navegação básica
- [ ] Validar navegação em diferentes tamanhos de tela

### 🏠 Início

- [x] Definir estrutura inicial da tela
- [x] Definir ações principais
- [x] Implementar seleção de fotografia
- [x] Implementar fluxo inicial de análise facial
- [x] Criar interface de análise facial para testes
- [x] Exibir informações e mensagens de processamento
- [ ] Integrar seleção do jogo ao fluxo principal
- [ ] Integrar análise facial à conversão para o jogo
- [ ] Integrar geração do tutorial personalizado
- [ ] Finalizar o fluxo da tela inicial

### 🎮 Jogos

- [ ] Finalizar tela de Jogos
- [ ] Criar lista de jogos disponíveis
- [ ] Criar pesquisa de jogos
- [ ] Definir informações exibidas para cada jogo
- [ ] Criar modal de informações do jogo
- [ ] Exibir tutoriais disponíveis no modal
- [ ] Criar acesso ao tutorial
- [ ] Definir comportamento quando não houver resultados
- [ ] Integrar lista de jogos ao Supabase
- [ ] Implementar carregamento da configuração do jogo selecionado
- [ ] Testar pesquisa e seleção de jogos
- [ ] Testar abertura e fechamento do modal
- [ ] Testar acesso aos tutoriais

### ⚙️ Configurações

#### 🎨 Personalização

- [ ] Criar tela de Configurações
- [ ] Criar seção Personalização
- [ ] Implementar configuração de tema
- [ ] Implementar configuração de idioma
- [ ] Implementar configuração de notificações, se aplicável
- [ ] Persistir preferências do usuário
- [ ] Testar configurações

#### 💾 Dados e privacidade

- [ ] Criar seção Dados
- [ ] Definir estratégia de armazenamento
- [ ] Definir se análises e resultados serão salvos
- [ ] Exibir informações de armazenamento, quando aplicável
- [ ] Criar opção para limpar análises salvas
- [ ] Criar opção para excluir tutoriais personalizados salvos
- [ ] Criar opção para apagar dados armazenados pelo aplicativo
- [ ] Criar modal de confirmação
- [ ] Exibir mensagens de sucesso e erro
- [ ] Atualizar informações após exclusões
- [ ] Testar exclusão de dados
- [ ] Documentar o tratamento das fotografias e dos dados faciais

#### 📱 Aplicativo

- [ ] Criar seção Aplicativo
- [ ] Exibir versão
- [ ] Exibir informações de suporte
- [ ] Exibir informações do criador
- [ ] Testar apresentação das informações

### 🔄 Fluxo do aplicativo

- [ ] Definir fluxo completo, da entrada ao resultado
- [ ] Definir fluxo de captura ou seleção da fotografia
- [ ] Definir fluxo de validação da imagem
- [ ] Definir fluxo da análise facial
- [ ] Definir fluxo da seleção do jogo
- [ ] Definir fluxo da conversão facial para o jogo
- [ ] Definir fluxo de geração do tutorial
- [ ] Definir fluxo de apresentação do resultado
- [ ] Definir estados de carregamento
- [ ] Definir mensagens de erro e recuperação
- [ ] Testar o fluxo completo entre as telas

---

## 3. 🎮 Banco de Dados e Configuração dos Jogos

> Cada jogo pode possuir uma estrutura de criação de personagens diferente. A análise facial deve ser independente das regras específicas de cada jogo.

### 🗄️ Banco de dados e armazenamento

- [ ] Definir arquitetura dos dados dos jogos
- [x] Criar tabela `games` no Supabase
- [x] Configurar RLS da tabela `games`
- [x] Criar Storage `games`
- [ ] Definir política de acesso aos arquivos do Storage
- [ ] Definir estrutura e versionamento dos arquivos JSON
- [ ] Definir estratégia de atualização das configurações
- [ ] Definir tratamento para jogos inativos ou sem configuração

### 🎮 Primeiro jogo: GTA V

- [x] Escolher GTA V como primeiro jogo de teste
- [ ] Analisar o sistema de criação de personagens do GTA V
- [ ] Documentar as categorias de personalização facial
- [ ] Definir opções categóricas e parâmetros numéricos
- [ ] Definir valores mínimos, máximos e incrementos, quando aplicáveis
- [ ] Identificar presets e opções que não sejam sliders
- [ ] Definir regras e limitações do editor
- [ ] Identificar dependências entre parâmetros
- [ ] Definir regras de mapeamento das características faciais
- [ ] Criar `gtaVCharacterParameters.json`
- [ ] Validar o JSON com dados reais do jogo
- [ ] Inserir ou atualizar o GTA V no banco de dados
- [ ] Enviar o JSON para o Storage
- [ ] Implementar consulta dos jogos
- [ ] Implementar carregamento do JSON do jogo selecionado
- [ ] Carregar configurações somente quando necessárias
- [ ] Tratar erros de consulta e arquivos ausentes
- [ ] Testar integração entre Supabase, Storage e aplicativo

### 🧩 Suporte a outros jogos

- [ ] Definir um formato comum para os perfis dos jogos
- [ ] Permitir categorias específicas por jogo
- [ ] Permitir parâmetros numéricos e opções categóricas
- [ ] Permitir regras e limitações específicas
- [ ] Permitir presets de aparência
- [ ] Testar jogos com estruturas de personalização diferentes

---

## 4. 🧠 Análise Facial

### 🔬 Biblioteca e modelos

- [x] Pesquisar tecnologias de análise facial
- [x] Implementar integração inicial com `@vladmandic/face-api`
- [x] Criar serviço `src/services/faceApi.ts`
- [x] Implementar carregamento dos modelos faciais
- [ ] Disponibilizar os arquivos dos modelos no caminho esperado (`/models`)
- [ ] Validar carregamento dos modelos no ambiente de desenvolvimento
- [ ] Validar carregamento dos modelos na aplicação publicada
- [ ] Confirmar compatibilidade com dispositivos móveis

### 📷 Detecção e processamento

- [x] Implementar detecção facial com Tiny Face Detector
- [x] Implementar detecção de pontos faciais com 68 landmarks
- [x] Implementar conversão de diferentes entradas de imagem para canvas
- [x] Implementar tratamento inicial de erros de entrada
- [x] Implementar seleção do maior rosto detectado
- [x] Implementar cálculo inicial das proporções faciais
- [x] Implementar normalização inicial das características
- [x] Implementar classificação heurística do formato do rosto
- [x] Implementar estimativa da cor da pele por amostragem
- [x] Implementar cálculo inicial da pose facial
- [x] Implementar estrutura de avisos sobre a qualidade da imagem
- [x] Implementar interface para câmera e galeria
- [x] Implementar exibição inicial dos resultados da análise
- [ ] Validar execução completa da análise facial
- [ ] Testar detecção de rosto em fotografias reais
- [ ] Calibrar intervalos de normalização das características
- [ ] Validar a classificação dos formatos faciais
- [ ] Validar o cálculo da pose facial
- [ ] Validar a estimativa de cor da pele
- [ ] Avaliar a precisão das medidas geométricas
- [ ] Diferenciar confiança da detecção e precisão da análise

### 📐 Características faciais

- [x] Implementar medida inicial do comprimento do rosto
- [x] Implementar medida inicial da largura da mandíbula
- [x] Implementar estimativa da forma do queixo
- [x] Implementar medida inicial do espaçamento entre os olhos
- [x] Implementar estimativas do tamanho e abertura dos olhos
- [x] Implementar estimativas da largura e comprimento do nariz
- [x] Implementar estimativa da largura da boca
- [x] Implementar estimativa do volume relativo dos lábios
- [ ] Validar todas as medidas com fotografias de referência
- [ ] Ajustar os cálculos para diferentes proporções faciais
- [ ] Definir tratamento para rostos parcialmente ocultos
- [ ] Definir tratamento para rostos inclinados ou virados
- [ ] Definir tratamento para iluminação inadequada

### 🧪 Testes da análise facial

- [ ] Testar diferentes formatos de rosto
- [ ] Testar fotografias de diferentes resoluções
- [ ] Testar diferentes iluminações
- [ ] Testar diferentes distâncias da câmera
- [ ] Testar fotografias sem rosto
- [ ] Testar fotografias com múltiplos rostos
- [ ] Testar imagens inválidas ou corrompidas
- [ ] Testar entradas de câmera e galeria
- [ ] Testar carregamento e falha dos modelos
- [ ] Testar desempenho em dispositivos móveis

---

## 5. 🔀 Conversão da Face para o Jogo

### 🧩 Mapeamento facial

- [x] Definir estrutura inicial dos dados da análise
- [x] Criar tipos para parâmetros de jogos
- [x] Criar estrutura inicial de perfil de jogo
- [x] Implementar função inicial `mapToGame()`
- [x] Implementar conversão de características normalizadas para sliders
- [x] Implementar suporte inicial a inversão de valores
- [x] Implementar suporte inicial a presets de formato facial
- [x] Implementar seleção de cor por paleta
- [ ] Validar o mapeamento com um perfil real do GTA V
- [ ] Definir mapeamentos específicos para cada característica
- [ ] Diferenciar parâmetros contínuos, discretos e categóricos
- [ ] Aplicar limites e incrementos definidos pelo jogo
- [ ] Aplicar regras específicas de cada jogo
- [ ] Resolver dependências entre parâmetros
- [ ] Definir valores recomendados quando não houver correspondência direta
- [ ] Definir estratégia para características não mensuráveis pela fotografia
- [ ] Calibrar os mapeamentos usando referências visuais

### 📊 Similaridade e resultado

- [ ] Definir método de comparação entre rosto e personagem
- [ ] Definir como será calculado o nível de similaridade
- [ ] Evitar apresentar estimativas como medidas exatas
- [ ] Organizar os resultados por categoria
- [ ] Estruturar os dados para a geração do tutorial
- [ ] Testar conversão com diferentes fotografias
- [ ] Testar conversão com diferentes perfis de jogo

---

## 6. 📋 Tutorial de Criação do Personagem

### 📝 Estrutura e geração

- [ ] Definir estrutura de dados do tutorial
- [ ] Gerar sequência de configuração a partir da conversão
- [ ] Organizar as etapas por categoria
- [ ] Mostrar nome da categoria
- [ ] Mostrar nome do parâmetro
- [ ] Mostrar opção recomendada
- [ ] Mostrar valor recomendado, quando aplicável
- [ ] Mostrar instruções específicas do jogo
- [ ] Adaptar o tutorial às regras de cada jogo
- [ ] Tratar opções indisponíveis no editor
- [ ] Definir comportamento para parâmetros sem correspondência

### 🕹️ Navegação do tutorial

- [ ] Permitir avançar entre etapas
- [ ] Permitir voltar entre etapas
- [ ] Mostrar progresso
- [ ] Criar resumo da configuração
- [ ] Permitir revisar as etapas
- [ ] Testar o tutorial com o perfil do GTA V
- [ ] Testar compatibilidade com outros perfis

---

## 7. 💾 Resultado

- [ ] Finalizar tela de resultado
- [ ] Exibir jogo selecionado
- [ ] Exibir fotografia utilizada, se aplicável
- [ ] Exibir configuração facial recomendada
- [ ] Exibir resumo das configurações
- [ ] Exibir nível de similaridade, quando validado
- [ ] Permitir revisar o tutorial
- [ ] Permitir reiniciar o processo
- [ ] Definir opção para salvar o resultado
- [ ] Definir opção para compartilhar o resultado
- [ ] Definir formato de exportação, se necessário
- [ ] Testar apresentação do resultado final

---

## 8. 🧪 Testes Gerais

### 📷 Imagens e câmera

- [ ] Testar diferentes fotografias
- [ ] Testar diferentes formatos de rosto
- [ ] Testar diferentes condições de iluminação
- [ ] Testar diferentes resoluções e formatos
- [ ] Testar fotografia sem rosto
- [ ] Testar fotografia com múltiplos rostos
- [ ] Testar fotografia inválida
- [ ] Testar permissões da câmera
- [ ] Testar troca entre câmera e galeria
- [ ] Testar erros durante o carregamento dos modelos

### 🎮 Jogos e conversão

- [ ] Testar configuração do GTA V
- [ ] Testar diferentes parâmetros
- [ ] Testar diferentes valores e incrementos
- [ ] Testar regras específicas do jogo
- [ ] Testar parâmetros dependentes
- [ ] Testar opções categóricas e presets
- [ ] Testar jogos com estruturas diferentes
- [ ] Testar ausência ou falha no carregamento do JSON

### 📱 Aplicativo

- [ ] Testar navegação entre telas
- [ ] Testar instalação do PWA
- [ ] Testar câmera e galeria em dispositivos móveis
- [ ] Testar diferentes tamanhos de tela
- [ ] Testar estados de carregamento
- [ ] Testar mensagens de erro
- [ ] Testar recuperação após falhas
- [ ] Testar uso prolongado e liberação de recursos

---

## 9. ⚡ Performance, Segurança e Privacidade

### ⚡ Performance

- [ ] Medir tempo de carregamento da aplicação
- [ ] Medir tempo de carregamento dos modelos
- [ ] Medir tempo da análise facial
- [ ] Medir tempo da conversão para o jogo
- [ ] Avaliar carregamento dos arquivos JSON
- [ ] Evitar carregamento desnecessário de configurações
- [ ] Avaliar consumo de memória
- [ ] Liberar recursos de câmera e imagens quando não forem mais necessários
- [ ] Avaliar desempenho em dispositivos móveis
- [ ] Avaliar tamanho final da aplicação

### 🔐 Segurança e privacidade

- [ ] Revisar regras e políticas do Supabase
- [ ] Revisar políticas de acesso ao Storage
- [ ] Garantir que chaves privadas não sejam expostas
- [ ] Utilizar apenas credenciais públicas apropriadas no cliente
- [ ] Definir o tratamento das fotografias e dos dados faciais
- [ ] Evitar armazenamento de fotografias sem necessidade
- [ ] Revisar tratamento de erros
- [ ] Validar entradas e arquivos recebidos
- [ ] Documentar o processamento local ou remoto dos dados

---

## 10. 🚀 Teste Final e Publicação

### ✅ Validação final

- [ ] Testar fluxo completo da fotografia ao resultado
- [ ] Testar instalação do PWA
- [ ] Testar câmera e seleção de fotografia
- [ ] Testar análise facial
- [ ] Testar seleção do jogo
- [ ] Testar carregamento da configuração do jogo
- [ ] Testar conversão das características faciais
- [ ] Testar geração do tutorial
- [ ] Testar resultado final
- [ ] Testar diferentes dispositivos e navegadores
- [ ] Corrigir problemas encontrados
- [ ] Revisar estrutura dos arquivos
- [ ] Revisar dependências e vulnerabilidades
- [ ] Revisar mensagens de erro e estados de carregamento
- [ ] Atualizar documentação do projeto

### 📦 Publicação

- [ ] Configurar ambiente de produção
- [ ] Configurar variáveis de ambiente
- [ ] Configurar integração com Supabase em produção
- [ ] Configurar hospedagem com HTTPS
- [ ] Gerar build de produção
- [ ] Testar a aplicação publicada
- [ ] Validar instalação do PWA em produção
- [ ] Criar versão inicial estável
- [ ] Publicar aplicação

---

## 📌 Estado atual do projeto

- [x] Estrutura inicial da aplicação Vue 3
- [x] Configuração inicial do PWA
- [x] Navegação inferior e header
- [x] Acesso à câmera e seleção de fotografias
- [x] Tabela `games` e RLS configurados no Supabase
- [x] Storage `games` criado
- [x] Serviço inicial de análise facial com `@vladmandic/face-api`
- [x] Extração inicial de características usando 68 pontos faciais
- [x] Estrutura inicial de conversão para parâmetros de jogos
- [ ] Validar carregamento dos modelos faciais
- [ ] Confirmar execução da análise facial de ponta a ponta
- [ ] Calibrar medidas e normalização facial
- [ ] Criar e validar o perfil de parâmetros do GTA V
- [ ] Integrar banco de dados, análise facial e conversão
- [ ] Gerar tutorial personalizado de criação do personagem
- [ ] Concluir testes e publicação