# 🎮 FaceCraft

## 📱 Descrição

O **FaceCraft** é um projeto desenvolvido com foco em dispositivos móveis e pensado para funcionar como um aplicativo móvel, mesmo sendo uma aplicação web.

A aplicação utiliza conceitos de **Progressive Web App (PWA)** para fornecer uma experiência próxima a um aplicativo nativo, permitindo instalação no dispositivo e utilização de recursos disponíveis no navegador.

O objetivo principal é analisar uma fotografia do rosto do usuário e utilizar essas informações para auxiliar na criação de personagens em diferentes jogos, considerando as possibilidades de personalização disponíveis em cada jogo.

A aplicação contará com uma base de dados contendo as opções e variáveis de personalização dos personagens, permitindo gerar configurações e tutoriais específicos para cada jogo.

## 📌 Problema

Os sistemas de criação de personagens dos jogos possuem diferentes opções e limitações para personalização facial.

Mesmo quando um jogo oferece diversas possibilidades de alteração do rosto, pode ser difícil identificar quais configurações devem ser utilizadas para criar um personagem visualmente semelhante a uma pessoa real.

Além disso, cada jogo possui seus próprios parâmetros, opções, valores e limitações de personalização.

O **FaceCraft** busca facilitar esse processo utilizando uma fotografia como referência e relacionando as características faciais identificadas com as opções disponíveis no sistema de criação de personagens de cada jogo.

## 🎯 Objetivo

Desenvolver uma aplicação **PWA mobile-first** capaz de:

* Analisar características faciais a partir de uma fotografia;
* Identificar características e proporções do rosto;
* Disponibilizar diferentes jogos para seleção;
* Consultar as possibilidades de personalização disponíveis para cada jogo;
* Relacionar as características faciais identificadas com as opções do jogo;
* Gerar configurações para criação do personagem;
* Criar um tutorial personalizado para reprodução das configurações;
* Considerar as limitações de personalização de cada jogo;
* Auxiliar o usuário na criação de um avatar visualmente semelhante à fotografia utilizada.

O projeto também tem como objetivo explorar conceitos de **visão computacional, processamento de imagens, análise facial, modelagem de dados e desenvolvimento de aplicações PWA**, além de trabalhar com diferentes possibilidades de personalização de personagens.

## 🗄️ Banco de Dados

O **FaceCraft** utilizará uma base de dados responsável por armazenar as informações necessárias para representar o sistema de criação de personagens de cada jogo.

Cada jogo poderá possuir diferentes:

* Categorias de personalização;
* Modelos de rosto;
* Formatos faciais;
* Características dos olhos;
* Características do nariz;
* Características da boca;
* Mandíbula e queixo;
* Sobrancelhas;
* Cabelos e outros elementos;
* Parâmetros ajustáveis;
* Valores mínimos e máximos;
* Opções disponíveis;
* Regras e limitações específicas.

Essas informações serão cadastradas pelo desenvolvedor da aplicação e utilizadas pelo sistema durante a análise e geração das configurações.

Dessa forma, a estrutura da aplicação poderá ser utilizada para diferentes jogos sem que seja necessário desenvolver uma lógica completamente independente para cada um deles.

## 🔨 Desenvolvimento

O desenvolvimento será realizado de forma incremental, começando pela estrutura da aplicação e gerenciamento das entregas e, posteriormente, incorporando recursos como câmera, OCR, GPS, mapas e rotas.

O acompanhamento das tarefas e funcionalidades planejadas está disponível no checklist do projeto:

👉 **[Ver Checklist de Desenvolvimento](./CHECKLIST.md)**

## 👨‍💻 Autor

**Bruno Marques**

🌐 Portfólio: https://bruno-marques.vercel.app/

💼 LinkedIn: https://www.linkedin.com/in/bruno-marques-desenvolvedor/

## 📄 Licença

Este projeto está licenciado sob uma **licença MIT**.

Você pode utilizar, modificar e distribuir o projeto de acordo com os termos estabelecidos pela licença.

Consulte o arquivo [`LICENSE`](https://github.com/brunomarquesdeveloper/facecraft/blob/main/LICENSE) para obter os termos completos da licença.

---

**FaceCraft** — Transforme seu rosto em um personagem. 🎮

