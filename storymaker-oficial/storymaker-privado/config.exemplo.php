<?php
/*
 * MODELO de configuração do cadastro de portfólios.
 * 1. Copie este arquivo para "config.php" (na mesma pasta storymaker-privado/, FORA do public_html).
 * 2. Preencha os campos abaixo. O config.php nunca vai para o GitHub (.gitignore).
 */
return [
    // Só aceita cadastros com true. Deixe false até a DocMe revisar a política de privacidade.
    'aberto' => false,

    // Banco de dados. Padrão: SQLite num arquivo dentro de storymaker-privado/dados/ (fora do site público).
    'db' => [
        'tipo' => 'sqlite',
        'arquivo' => __DIR__ . '/dados/cadastros.sqlite',
        // Para usar o MySQL da Hostinger, troque por:
        // 'tipo' => 'mysql', 'dsn' => 'mysql:host=localhost;dbname=NOME_DO_BANCO;charset=utf8mb4',
        // 'usuario' => 'USUARIO', 'senha' => 'SENHA',
    ],

    // Senha da área da equipe (/cadastro/equipe/). Guarde só o HASH, nunca a senha.
    // Gere no terminal:  php -r 'echo password_hash("SUA-SENHA-FORTE", PASSWORD_DEFAULT), PHP_EOL;'
    'senha_equipe_hash' => '',

    // Texto aleatório longo, usado para embaralhar o IP no controle de abuso (o IP nunca é salvo).
    // Gere com:  php -r 'echo bin2hex(random_bytes(32)), PHP_EOL;'
    'sal' => '',

    // Versão da política aceita, gravada em cada cadastro. Troque quando publicar a versão final.
    'versao_politica' => 'minuta-2026-11-25',

    // Opcional: e-mail da equipe para receber um aviso de "novo cadastro" (o aviso NÃO leva dados pessoais).
    // Deixe vazio para não enviar nada.
    'aviso_email' => '',
];
