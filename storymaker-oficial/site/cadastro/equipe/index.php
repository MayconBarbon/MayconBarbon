<?php
/*
 * Área da equipe — revisão dos cadastros de portfólio.
 * Acesso só com a senha da equipe (hash no config.php privado). Não é área de membros: quem se cadastra não tem login.
 */
declare(strict_types=1);
require dirname(__DIR__) . '/_privado.php';
cabecalhos_privados();
header("Content-Security-Policy: default-src 'self'; style-src 'self' 'unsafe-inline'; form-action 'self'; frame-ancestors 'none'; base-uri 'none'");

$https = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off');
session_name('smk_equipe');
session_set_cookie_params(['lifetime' => 0, 'path' => dirname($_SERVER['SCRIPT_NAME']) . '/', 'secure' => $https, 'httponly' => true, 'samesite' => 'Strict']);
session_start();
if (isset($_SESSION['ultimo']) && time() - $_SESSION['ultimo'] > 3600) { $_SESSION = []; session_destroy(); session_start(); }
$_SESSION['ultimo'] = time();
if (empty($_SESSION['csrf'])) { $_SESSION['csrf'] = bin2hex(random_bytes(32)); }
$csrf = $_SESSION['csrf'];
$self = strtok($_SERVER['REQUEST_URI'], '?');

function pagina(string $titulo, string $corpo): void {
    echo '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>' . e($titulo) . ' · Equipe</title><style>
    *{box-sizing:border-box}body{margin:0;font:15px/1.5 system-ui,-apple-system,Segoe UI,sans-serif;color:#2b2a30;background:#f6f5f3}
    header{background:#e7570c;color:#fff;padding:14px 18px;display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}header b{font-size:17px}
    header a,header button{color:#fff}main{max-width:1100px;margin:0 auto;padding:18px}
    .card{background:#fff;border:1px solid #e7e6ea;border-radius:12px;padding:16px;margin-bottom:14px}
    table{width:100%;border-collapse:collapse;background:#fff}th,td{text-align:left;padding:10px;border-bottom:1px solid #eee;vertical-align:top}th{font-size:13px;color:#6c6b72}
    .st{display:inline-block;padding:2px 10px;border-radius:99px;background:#efeef2;font-size:13px;white-space:nowrap}.st.recebido{background:#fff1e8;color:#9a3412}
    input,select,textarea{font:inherit;padding:9px 10px;border:1px solid #cfcdd5;border-radius:8px;max-width:100%}textarea{width:100%}
    button,.btn{font:inherit;background:#2b2a30;color:#fff;border:0;border-radius:8px;padding:9px 16px;cursor:pointer;text-decoration:none;display:inline-block}
    .perigo{background:#b42318}.leve{background:#efeef2;color:#2b2a30}dl{display:grid;grid-template-columns:220px 1fr;gap:6px 14px;margin:0}dt{color:#6c6b72}dd{margin:0;word-break:break-word}
    .ok{background:#ecfdf3;border-color:#abefc6}.erro{background:#fef3f2;border-color:#f4c7c3}.filtros{display:flex;gap:8px;flex-wrap:wrap;align-items:end}
    @media(max-width:700px){dl{grid-template-columns:1fr}td:nth-child(4),th:nth-child(4){display:none}}
    </style></head><body>' . $corpo . '</body></html>';
    exit;
}
function topo(string $csrf, string $self): string {
    return '<header><b>Cadastros de portfólio · Equipe</b><form method="post" action="' . e($self) . '"><input type="hidden" name="csrf" value="' . e($csrf) . '"><input type="hidden" name="acao" value="sair"><button class="leve">Sair</button></form></header>';
}

// ---------- login (senha única da equipe) ----------
$hash = (string)cfg('senha_equipe_hash');
if ($hash === '') { pagina('Configurar', '<main><div class="card erro"><b>Área da equipe ainda não configurada.</b><p>Defina <code>senha_equipe_hash</code> no arquivo <code>storymaker-privado/config.php</code>.</p></div></main>'); }

if (empty($_SESSION['ok'])) {
    $msg = '';
    if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST' && ($_POST['acao'] ?? '') === 'entrar') {
        if (excedeu('login', 5, 900)) { $msg = 'Muitas tentativas. Aguarde 15 minutos.'; }
        elseif (password_verify((string)($_POST['senha'] ?? ''), $hash)) { session_regenerate_id(true); $_SESSION['ok'] = 1; $_SESSION['csrf'] = bin2hex(random_bytes(32)); header('Location: ' . $self, true, 303); exit; }
        else { registrar_tentativa('login'); $msg = 'Senha incorreta.'; }
    }
    pagina('Entrar', '<main style="max-width:420px"><div class="card"><h1 style="font-size:20px;margin-top:0">Área da equipe</h1>' . ($msg ? '<p class="card erro">' . e($msg) . '</p>' : '') .
        '<form method="post" action="' . e($self) . '"><input type="hidden" name="acao" value="entrar"><label>Senha da equipe<br><input type="password" name="senha" autocomplete="current-password" required style="width:100%"></label><p><button>Entrar</button></p></form></div></main>');
}

// ---------- ações (POST com CSRF) ----------
$aviso = '';
if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST') {
    if (!hash_equals($csrf, (string)($_POST['csrf'] ?? ''))) { http_response_code(400); pagina('Erro', '<main><div class="card erro">Sessão expirada. Recarregue a página.</div></main>'); }
    $acao = (string)($_POST['acao'] ?? ''); $id = (int)($_POST['id'] ?? 0);
    if ($acao === 'sair') { $_SESSION = []; session_destroy(); header('Location: ' . $self, true, 303); exit; }
    if ($acao === 'atualizar' && $id) {
        $novo = (string)($_POST['status'] ?? '');
        $q = db()->prepare('SELECT status FROM cadastros WHERE id = ?'); $q->execute([$id]); $ant = $q->fetchColumn();
        if ($ant !== false && isset(STATUS[$novo])) {
            db()->prepare('UPDATE cadastros SET status = ?, notas_internas = ?, atualizado_em = ? WHERE id = ?')->execute([$novo, mb_substr((string)($_POST['notas'] ?? ''), 0, 4000), agora(), $id]);
            if ($ant !== $novo) { historico($id, 'status', STATUS[$ant] . ' → ' . STATUS[$novo]); } else { historico($id, 'notas', 'Notas internas atualizadas'); }
            header('Location: ' . $self . '?ver=' . $id . '&salvo=1', true, 303); exit;
        }
    }
    if ($acao === 'revogar' && $id) {
        $campo = (string)($_POST['campo'] ?? '');
        $mapa = ['consent_publicacao' => 'publicação no diretório', 'consent_compartilhar_contato' => 'compartilhar contato', 'consent_novidades' => 'novidades'];
        if (isset($mapa[$campo])) {
            $extra = $campo === 'consent_publicacao' ? ", campos_publicaveis = '[]'" : ($campo === 'consent_novidades' ? ", canal_novidades = ''" : '');
            db()->prepare("UPDATE cadastros SET $campo = 0$extra, atualizado_em = ? WHERE id = ?")->execute([agora(), $id]);
            historico($id, 'revogacao', 'Autorização revogada a pedido: ' . $mapa[$campo]);
            header('Location: ' . $self . '?ver=' . $id . '&salvo=1', true, 303); exit;
        }
    }
    if ($acao === 'excluir' && $id && ($_POST['confirma'] ?? '') === 'EXCLUIR') {
        db()->prepare('DELETE FROM cadastros WHERE id = ?')->execute([$id]);
        db()->prepare('DELETE FROM historico WHERE cadastro_id = ?')->execute([$id]);
        header('Location: ' . $self . '?excluido=1', true, 303); exit;
    }
    $aviso = 'Nada foi alterado.';
}

$areaNome = fn(string $json) => implode(', ', array_map(fn($a) => AREAS[$a] ?? $a, json_decode($json ?: '[]', true) ?: []));

// ---------- detalhe ----------
if (isset($_GET['ver'])) {
    $id = (int)$_GET['ver'];
    $q = db()->prepare('SELECT * FROM cadastros WHERE id = ?'); $q->execute([$id]); $c = $q->fetch();
    if (!$c) { pagina('Não encontrado', topo($csrf, $self) . '<main><div class="card">Cadastro não encontrado. <a href="' . e($self) . '">Voltar</a></div></main>'); }
    $h = db()->prepare('SELECT * FROM historico WHERE cadastro_id = ? ORDER BY id DESC'); $h->execute([$id]);
    $campos = implode(', ', array_map(fn($k) => CAMPOS_PUBLICAVEIS[$k] ?? $k, json_decode($c['campos_publicaveis'] ?: '[]', true) ?: []));
    $sn = fn($v) => $v ? '<b>Sim</b>' : 'Não';
    $link = fn($u) => $u ? '<a href="' . e($u) . '" target="_blank" rel="noopener noreferrer">' . e($u) . '</a>' : '—';
    $ig = ltrim((string)$c['instagram'], '@');
    $opts = ''; foreach (STATUS as $k => $v) { $opts .= '<option value="' . e($k) . '"' . ($k === $c['status'] ? ' selected' : '') . '>' . e($v) . '</option>'; }
    $rev = function (string $campo, string $rot) use ($c, $csrf, $self) {
        return $c[$campo] ? '<form method="post" action="' . e($self) . '" style="display:inline"><input type="hidden" name="csrf" value="' . e($csrf) . '"><input type="hidden" name="acao" value="revogar"><input type="hidden" name="id" value="' . (int)$c['id'] . '"><input type="hidden" name="campo" value="' . e($campo) . '"><button class="leve">Registrar revogação (' . e($rot) . ')</button></form> ' : '';
    };
    $corpo = topo($csrf, $self) . '<main><p><a href="' . e($self) . '">← Todos os cadastros</a></p>' . (isset($_GET['salvo']) ? '<div class="card ok">Alteração salva.</div>' : '') .
      '<div class="card"><h1 style="margin-top:0;font-size:22px">#' . (int)$c['id'] . ' · ' . e($c['nome_profissional']) . ' <span class="st ' . e($c['status']) . '">' . e(STATUS[$c['status']] ?? $c['status']) . '</span></h1><dl>' .
      '<dt>Recebido em</dt><dd>' . e($c['criado_em']) . '</dd><dt>Última atualização</dt><dd>' . e($c['atualizado_em']) . '</dd>' .
      '<dt>Cidade</dt><dd>' . e($c['cidade']) . ' / ' . e($c['uf']) . '</dd><dt>Regiões em que atende</dt><dd>' . e($c['regioes']) . '</dd>' .
      '<dt>Áreas</dt><dd>' . e($areaNome($c['areas'])) . '</dd><dt>Portfólio</dt><dd>' . $link($c['portfolio']) . '</dd>' .
      '<dt>Instagram</dt><dd>' . $link('https://www.instagram.com/' . rawurlencode($ig) . '/') . '</dd><dt>Outra rede</dt><dd>' . $link($c['outra_rede']) . '</dd>' .
      '<dt>Apresentação</dt><dd>' . nl2br(e($c['apresentacao'])) . '</dd><dt>E-mail</dt><dd>' . e($c['contato_email'] ?: '—') . '</dd><dt>WhatsApp</dt><dd>' . e($c['contato_whatsapp'] ?: '—') . '</dd>' .
      '<dt>Observações</dt><dd>' . nl2br(e($c['observacoes'] ?: '—')) . '</dd></dl></div>' .
      '<div class="card"><h2 style="margin-top:0;font-size:17px">Autorizações (versão da política: ' . e($c['versao_politica']) . ')</h2><dl>' .
      '<dt>A. Análise e contato</dt><dd>' . $sn($c['consent_analise']) . '</dd>' .
      '<dt>B. Publicação futura</dt><dd>' . $sn($c['consent_publicacao']) . ($c['consent_publicacao'] ? ' · campos: ' . e($campos) : '') . '</dd>' .
      '<dt>C. Compartilhar contato</dt><dd>' . $sn($c['consent_compartilhar_contato']) . '</dd>' .
      '<dt>D. Novidades</dt><dd>' . $sn($c['consent_novidades']) . ($c['consent_novidades'] ? ' · ' . e($c['canal_novidades']) : '') . '</dd></dl>' .
      '<p style="margin-bottom:0">' . $rev('consent_publicacao', 'B') . $rev('consent_compartilhar_contato', 'C') . $rev('consent_novidades', 'D') . '</p></div>' .
      '<div class="card"><h2 style="margin-top:0;font-size:17px">Análise interna</h2><form method="post" action="' . e($self) . '"><input type="hidden" name="csrf" value="' . e($csrf) . '"><input type="hidden" name="acao" value="atualizar"><input type="hidden" name="id" value="' . (int)$c['id'] . '">' .
      '<p><label>Status<br><select name="status">' . $opts . '</select></label></p><p><label>Notas internas (só a equipe vê)<br><textarea name="notas" rows="4">' . e($c['notas_internas'] ?? '') . '</textarea></label></p><button>Salvar</button></form>' .
      '<p style="font-size:13px;color:#6c6b72;margin-bottom:0">“Aprovado para possível publicação” não publica nada: a publicação depende da autorização B, dos campos escolhidos e de um convite (fase 2).</p></div>' .
      '<div class="card"><h2 style="margin-top:0;font-size:17px">Histórico</h2><ul>';
    foreach ($h as $r) { $corpo .= '<li>' . e($r['quando']) . ' · ' . e($r['acao']) . ($r['detalhe'] ? ' · ' . e($r['detalhe']) : '') . '</li>'; }
    $corpo .= '</ul></div><div class="card erro"><h2 style="margin-top:0;font-size:17px">Excluir cadastro (pedido do titular)</h2><form method="post" action="' . e($self) . '"><input type="hidden" name="csrf" value="' . e($csrf) . '"><input type="hidden" name="acao" value="excluir"><input type="hidden" name="id" value="' . (int)$c['id'] . '"><p>Apaga definitivamente os dados e o histórico deste cadastro. Digite EXCLUIR para confirmar.</p><input name="confirma" autocomplete="off"> <button class="perigo">Excluir definitivamente</button></form></div></main>';
    pagina('#' . $id, $corpo);
}

// ---------- lista ----------
$st = (string)($_GET['status'] ?? ''); $uf = strtoupper((string)($_GET['uf'] ?? '')); $area = (string)($_GET['area'] ?? ''); $busca = trim((string)($_GET['q'] ?? ''));
$w = []; $a = [];
if (isset(STATUS[$st])) { $w[] = 'status = ?'; $a[] = $st; }
if (in_array($uf, UFS, true)) { $w[] = 'uf = ?'; $a[] = $uf; }
if (isset(AREAS[$area])) { $w[] = 'areas LIKE ?'; $a[] = '%"' . $area . '"%'; }
if ($busca !== '') { $w[] = '(nome_profissional LIKE ? OR cidade LIKE ? OR regioes LIKE ?)'; array_push($a, "%$busca%", "%$busca%", "%$busca%"); }
$q = db()->prepare('SELECT id, criado_em, status, nome_profissional, cidade, uf, areas FROM cadastros' . ($w ? ' WHERE ' . implode(' AND ', $w) : '') . ' ORDER BY id DESC LIMIT 500');
$q->execute($a); $linhas = $q->fetchAll();
$cont = db()->query('SELECT status, COUNT(*) n FROM cadastros GROUP BY status')->fetchAll(PDO::FETCH_KEY_PAIR);

$sel = function (array $op, string $atual, string $nome, string $vazio) { $o = '<select name="' . $nome . '"><option value="">' . e($vazio) . '</option>'; foreach ($op as $k => $v) { $o .= '<option value="' . e($k) . '"' . ((string)$k === $atual ? ' selected' : '') . '>' . e($v) . '</option>'; } return $o . '</select>'; };
$corpo = topo($csrf, $self) . '<main>' . (isset($_GET['excluido']) ? '<div class="card ok">Cadastro excluído definitivamente.</div>' : '') . ($aviso ? '<div class="card">' . e($aviso) . '</div>' : '') .
  '<div class="card"><b>Resumo:</b> ' . implode(' · ', array_map(fn($k) => e(STATUS[$k]) . ': ' . (int)($cont[$k] ?? 0), array_keys(STATUS))) . '</div>' .
  '<form class="card filtros" method="get" action="' . e($self) . '">' . $sel(STATUS, $st, 'status', 'Todos os status') . $sel(array_combine(UFS, UFS), $uf, 'uf', 'UF') . $sel(AREAS, $area, 'area', 'Todas as áreas') .
  '<input name="q" value="' . e($busca) . '" placeholder="Nome, cidade ou região"><button>Filtrar</button> <a class="btn leve" href="' . e($self) . '">Limpar</a></form>' .
  '<table><thead><tr><th>#</th><th>Profissional</th><th>Cidade</th><th>Áreas</th><th>Status</th><th>Recebido</th></tr></thead><tbody>';
foreach ($linhas as $l) {
    $corpo .= '<tr><td>' . (int)$l['id'] . '</td><td><a href="' . e($self) . '?ver=' . (int)$l['id'] . '">' . e($l['nome_profissional']) . '</a></td><td>' . e($l['cidade']) . '/' . e($l['uf']) . '</td><td>' . e($areaNome($l['areas'])) . '</td><td><span class="st ' . e($l['status']) . '">' . e(STATUS[$l['status']] ?? $l['status']) . '</span></td><td>' . e(substr($l['criado_em'], 0, 10)) . '</td></tr>';
}
if (!$linhas) { $corpo .= '<tr><td colspan="6">Nenhum cadastro encontrado.</td></tr>'; }
$corpo .= '</tbody></table></main>';
pagina('Cadastros', $corpo);
