<?php
/*
 * Cadastro de portfólios — biblioteca privada.
 * ESTA PASTA (storymaker-privado/) FICA FORA DA PASTA PÚBLICA DO SITE (public_html).
 * Ela guarda a configuração e o banco de dados; nada aqui pode ser acessado pelo navegador.
 */
declare(strict_types=1);

const STATUS = [
    'recebido'            => 'Recebido',
    'em_analise'          => 'Em análise',
    'aprovado_contato'    => 'Aprovado para contato',
    'aprovado_publicacao' => 'Aprovado para possível publicação',
    'aguardando_info'     => 'Aguardando informação',
    'encerrado'           => 'Encerrado',
];

const AREAS = [
    'corporativos'   => 'Eventos corporativos',
    'casamentos'     => 'Casamentos',
    'festas'         => 'Festas e eventos sociais',
    'pequenos'       => 'Pequenos negócios',
    'marcas'         => 'Conteúdo para marcas',
    'tempo_real'     => 'Cobertura mobile em tempo real',
    'edicao'         => 'Edição de vídeos curtos',
];

// Campos que a pessoa pode autorizar para um futuro diretório público (fase 2). Contato direto NUNCA entra aqui.
const CAMPOS_PUBLICAVEIS = [
    'nome_profissional' => 'Nome profissional',
    'cidade'            => 'Cidade e estado',
    'regioes'           => 'Regiões em que atende',
    'areas'             => 'Áreas de atuação',
    'apresentacao'      => 'Apresentação profissional',
    'instagram'         => 'Instagram profissional',
    'outra_rede'        => 'LinkedIn, site ou outra rede',
    'portfolio'         => 'Link do portfólio',
];

const UFS = ['AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO'];

function cfg(?string $chave = null) {
    static $c = null;
    if ($c === null) {
        $arq = __DIR__ . '/config.php';
        if (!is_file($arq)) { throw new RuntimeException('config.php ausente'); }
        $c = require $arq;
    }
    return $chave === null ? $c : ($c[$chave] ?? null);
}

function db(): PDO {
    static $pdo = null;
    if ($pdo) { return $pdo; }
    $d = cfg('db');
    if (($d['tipo'] ?? 'sqlite') === 'mysql') {
        $pdo = new PDO($d['dsn'], $d['usuario'], $d['senha'], [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
        $auto = 'INT AUTO_INCREMENT PRIMARY KEY'; $txt = 'TEXT';
    } else {
        $arq = $d['arquivo'];
        if (!is_dir(dirname($arq))) { mkdir(dirname($arq), 0700, true); }
        $novo = !is_file($arq);
        $pdo = new PDO('sqlite:' . $arq, null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
        if ($novo) { @chmod($arq, 0600); }
        $pdo->exec('PRAGMA foreign_keys = ON');
        $auto = 'INTEGER PRIMARY KEY AUTOINCREMENT'; $txt = 'TEXT';
    }
    $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
    $pdo->exec("CREATE TABLE IF NOT EXISTS cadastros (
        id $auto,
        criado_em VARCHAR(25) NOT NULL,
        atualizado_em VARCHAR(25) NOT NULL,
        status VARCHAR(30) NOT NULL DEFAULT 'recebido',
        nome_profissional VARCHAR(120) NOT NULL,
        cidade VARCHAR(80) NOT NULL,
        uf CHAR(2) NOT NULL,
        regioes VARCHAR(300) NOT NULL,
        instagram VARCHAR(200) NOT NULL,
        outra_rede VARCHAR(300) NOT NULL DEFAULT '',
        portfolio VARCHAR(300) NOT NULL,
        areas $txt NOT NULL,
        apresentacao $txt NOT NULL,
        contato_email VARCHAR(160) NOT NULL DEFAULT '',
        contato_whatsapp VARCHAR(20) NOT NULL DEFAULT '',
        observacoes $txt,
        consent_analise SMALLINT NOT NULL,
        consent_publicacao SMALLINT NOT NULL DEFAULT 0,
        campos_publicaveis $txt,
        consent_compartilhar_contato SMALLINT NOT NULL DEFAULT 0,
        consent_novidades SMALLINT NOT NULL DEFAULT 0,
        canal_novidades VARCHAR(20) NOT NULL DEFAULT '',
        versao_politica VARCHAR(40) NOT NULL,
        notas_internas $txt
    )");
    $pdo->exec("CREATE TABLE IF NOT EXISTS historico (
        id $auto,
        cadastro_id INTEGER NOT NULL,
        quando VARCHAR(25) NOT NULL,
        acao VARCHAR(40) NOT NULL,
        detalhe VARCHAR(200) NOT NULL DEFAULT ''
    )");
    $pdo->exec("CREATE TABLE IF NOT EXISTS tentativas (
        id $auto,
        tipo VARCHAR(10) NOT NULL,
        chave CHAR(64) NOT NULL,
        quando INTEGER NOT NULL
    )");
    return $pdo;
}

function agora(): string { return (new DateTimeImmutable('now', new DateTimeZone('America/Sao_Paulo')))->format('Y-m-d H:i:s'); }

function e($s): string { return htmlspecialchars((string)$s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8'); }

/* Controle de abuso: guarda só um hash do IP (com sal secreto), nunca o IP, e apaga depois de 24 h. */
function chave_ip(): string {
    $ip = $_SERVER['REMOTE_ADDR'] ?? '0';
    return hash('sha256', (string)cfg('sal') . '|' . $ip);
}
function excedeu(string $tipo, int $max, int $janela): bool {
    $p = db();
    $p->prepare('DELETE FROM tentativas WHERE quando < ?')->execute([time() - 86400]);
    $q = $p->prepare('SELECT COUNT(*) FROM tentativas WHERE tipo = ? AND chave = ? AND quando > ?');
    $q->execute([$tipo, chave_ip(), time() - $janela]);
    return (int)$q->fetchColumn() >= $max;
}
function registrar_tentativa(string $tipo): void {
    db()->prepare('INSERT INTO tentativas (tipo, chave, quando) VALUES (?, ?, ?)')->execute([$tipo, chave_ip(), time()]);
}

function historico(int $id, string $acao, string $detalhe = ''): void {
    db()->prepare('INSERT INTO historico (cadastro_id, quando, acao, detalhe) VALUES (?, ?, ?, ?)')
        ->execute([$id, agora(), $acao, mb_substr($detalhe, 0, 200)]);
}

function cabecalhos_privados(): void {
    header('Cache-Control: no-store, max-age=0');
    header('X-Robots-Tag: noindex, nofollow');
    header('X-Content-Type-Options: nosniff');
    header('X-Frame-Options: DENY');
    header('Referrer-Policy: no-referrer');
}
