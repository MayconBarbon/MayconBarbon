# Cadastro de portfólios — Fase 1

25/11/2026. Primeira etapa da rede de Storymakers e Socialmakers: uma página de cadastro com análise interna. **Não é** diretório, área de membros nem marketplace.

## O que existia antes

- Site estático (HTML, CSS e JavaScript puro, sem build). Catálogo e preços em `site/assets/js/config.js`.
- Nenhum formulário, banco de dados ou servidor próprio: o site não armazenava dados de visitantes.
- Hospedagem: Hostinger (endereço temporário `hostingersite.com`), que oferece PHP e MySQL.
- Nenhuma política de privacidade existente.

## O que foi criado

| Caminho | Para quê | Fica onde no servidor |
|---|---|---|
| `site/cadastro/index.html` | Página "Faça parte da rede de Storymakers" + formulário em 4 etapas | `public_html/cadastro/` |
| `site/cadastro/cadastro.css`, `cadastro.js` | Visual (usa o `style.css` do site) e etapas do formulário | `public_html/cadastro/` |
| `site/cadastro/enviar.php` | Recebe, valida e grava o cadastro | `public_html/cadastro/` |
| `site/cadastro/obrigado.html` | Confirmação (para quem envia sem JavaScript) | `public_html/cadastro/` |
| `site/cadastro/privacidade.html` | **Minuta** da política de privacidade do cadastro | `public_html/cadastro/` |
| `site/cadastro/equipe/index.php` | Área da equipe: lista, filtros, status, notas, histórico, revogação e exclusão | `public_html/cadastro/equipe/` |
| `site/cadastro/_privado.php`, `.htaccess` | Liga a parte pública à pasta privada; bloqueia listagem e arquivos sensíveis | `public_html/cadastro/` |
| `storymaker-privado/lib.php`, `config.exemplo.php`, `.htaccess` | Banco, regras, configuração | **Fora** do `public_html` |

Nenhum arquivo existente do site foi alterado. A página não está no menu do site: para divulgá-la, é preciso acrescentar um link (ver "Pendências").

## Como os cadastros são armazenados e quem acessa

- **Banco privado** (SQLite por padrão, ou o MySQL da Hostinger) dentro de `storymaker-privado/dados/`, **fora da pasta pública**: não há endereço web para ele. O arquivo é criado com permissão só do dono (600).
- Acesso apenas pela **área da equipe** (`/cadastro/equipe/`), com senha única da equipe guardada só como *hash* no `config.php` privado. Proteções: sessão expira em 1 h, cookie `HttpOnly`/`Secure`/`SameSite=Strict`, token contra envio forjado (CSRF), bloqueio de 15 min após 5 senhas erradas, páginas com `noindex`, sem cache e sem incorporação em outros sites.
- **O que não é guardado:** IP (só um hash com sal secreto, para limitar abusos, apagado em 24 h), documentos, dados sensíveis, arquivos. Nenhum dado vai para analytics, planilhas, logs ou serviços externos. Em caso de erro, o log registra só o tipo do erro, nunca os dados.
- **Não há envio a terceiros.** O único serviço envolvido é a hospedagem do site. O aviso opcional por e-mail à equipe (`aviso_email`) diz só "novo cadastro #N", sem dados pessoais.

## Campos e autorizações registrados

Cada cadastro guarda: data do envio, status, dados profissionais, contato (e-mail e/ou WhatsApp), observações, as **quatro autorizações separadas** (A obrigatória; B, C e D opcionais, todas desmarcadas por padrão), os campos escolhidos para publicação (se B), o canal de novidades (se D) e a versão da política aceita. Toda mudança de status, nota ou revogação entra no histórico com data e hora.

## Como a equipe revisa

1. Entrar em `/cadastro/equipe/` com a senha da equipe.
2. Filtrar por status, estado, área ou buscar por nome, cidade ou região.
3. Abrir o cadastro, conferir o portfólio e o Instagram (abrem em nova aba).
4. Mudar o status e escrever notas internas (só a equipe vê):
   **Recebido → Em análise → Aprovado para contato / Aprovado para possível publicação / Aguardando informação / Encerrado.**
5. Pedido do titular: botões "Registrar revogação" (B, C ou D) e "Excluir definitivamente" (digitando EXCLUIR).

"Aprovado para possível publicação" **não publica nada**: é só uma marcação interna para a fase 2.

## O que pode ser exibido publicamente (fase 2, só com autorização B)

Somente os campos que a pessoa marcou entre: nome profissional, cidade e estado, regiões em que atende, áreas de atuação, apresentação, Instagram, outra rede ou site e link do portfólio. **E-mail e WhatsApp nunca entram nessa lista.** Compartilhar o contato com um contratante depende da autorização C.

## Nenhum perfil é publicado automaticamente

O envio só grava no banco privado com status "Recebido". Não existe nesta fase nenhuma página que leia o banco para o público.

## Não foi construído nesta fase

Diretório público, busca por cidade/especialidade, cards de perfil, encaminhamento de contratantes, perfil editável, disponibilidade, login de profissionais, área de membros, painel pessoal, aplicativo e upload de arquivos. O banco já guarda o que a fase 2 vai precisar (status de aprovação para publicação, campos autorizados, autorização de contato, UF e áreas para busca) e pode migrar para MySQL sem mudar as páginas.

## Pendências antes de abrir (configuração pela DocMe)

1. **Subir os arquivos** na Hostinger: conteúdo de `site/cadastro/` em `public_html/cadastro/` e a pasta `storymaker-privado/` **ao lado** do `public_html` (nunca dentro). Se o caminho for outro, definir a variável `STORYMAKER_PRIVADO`.
2. **Criar o `config.php`** a partir de `config.exemplo.php`: senha da equipe (hash), sal secreto e, se preferir, os dados do MySQL. Os comandos estão no próprio arquivo.
3. **Revisar a política de privacidade** (`privacidade.html`, marcada como MINUTA): razão social, CNPJ e endereço; provedor de hospedagem e país dos servidores; prazo de guarda (há uma sugestão para revisão); e-mail de privacidade; encarregado (DPO) ou dispensa. Depois de revisada: tirar a faixa "MINUTA", trocar `versao_politica` no config e tirar o `noindex` da página do cadastro.
4. **Abrir as inscrições:** só depois da revisão, mudar `'aberto' => true` no config. Enquanto estiver `false`, o formulário responde "As inscrições ainda não estão abertas".
5. **HTTPS obrigatório** no domínio (a Hostinger oferece SSL grátis). Opcional: proteger também a pasta `cadastro/equipe/` pelo hPanel ("Proteger diretório").
6. **Link para a página:** o site institucional não foi alterado. Para divulgar, acrescentar um link para `cadastro/index.html` (por exemplo no rodapé) quando decidirem.
7. **Backup:** incluir a pasta `storymaker-privado/dados/` no backup da hospedagem e definir quem da equipe tem a senha.

## Testes feitos (servidor PHP local com dados fictícios)

- **Celular (iPhone 13) e computador:** sem rolagem horizontal, sem erros de JavaScript; foco visível e "Pular para o conteúdo" no teclado.
- **Etapas:** cada etapa só avança com os obrigatórios preenchidos e mostra os erros em português; autorizações começam desmarcadas; sem a autorização A o envio é bloqueado; marcar B abre a escolha de campos e D abre a escolha do canal.
- **Envio:** com JavaScript, mostra a confirmação na própria página; sem JavaScript, redireciona para `obrigado.html` (303).
- **Servidor:** dados inválidos são recusados (422) com a lista de erros; campo anti-robô descarta o envio sem gravar; mais de 10 envios por hora do mesmo IP recebe 429; com `aberto => false`, responde 503; GET no `enviar.php` dá 405; `_privado.php` não abre pelo navegador.
- **Banco:** cadastro gravado com data, status "Recebido", autorizações e campos escolhidos; histórico registrado; IP guardado só como hash; nenhum nome, e-mail ou telefone apareceu no log do servidor.
- **Área da equipe:** sem senha não mostra dados; senha errada é recusada; lista, filtro por status, mudança de status, notas, histórico, revogação e exclusão funcionaram; ação sem token CSRF foi recusada (400); sair encerra a sessão; funciona no celular.
- Os testes usaram uma cópia temporária da configuração; nenhum dado de teste ficou no projeto.

Observação: o servidor local não lê `.htaccess`; as regras dele valem na Hostinger (Apache/LiteSpeed). Mesmo sem elas, o banco não fica exposto, porque está fora da pasta pública.
