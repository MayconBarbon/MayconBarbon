<?php
/*
 * Recebe o formulário "Cadastre seu portfólio".
 * - Grava somente no banco privado (fora do site público). Nada é publicado.
 * - Não grava IP, não registra os dados em log, não envia nada a terceiros.
 */
declare(strict_types=1);
require __DIR__ . '/_privado.php';
cabecalhos_privados();

$querJson = str_contains($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json');
function responder(bool $ok, string $msg, array $erros = []): void {
    global $querJson;
    if (!$ok && http_response_code() === 200) { http_response_code($erros ? 422 : 400); }
    if ($querJson) {
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode(['ok' => $ok, 'mensagem' => $msg, 'erros' => $erros], JSON_UNESCAPED_UNICODE);
    } elseif ($ok) {
        header('Location: obrigado.html', true, 303);
    } else {
        header('Content-Type: text/html; charset=utf-8');
        echo '<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Cadastro</title>'
           . '<body style="font-family:system-ui;max-width:640px;margin:40px auto;padding:0 16px;color:#2b2a30"><h1>Não foi possível enviar</h1><p>' . e($msg) . '</p>'
           . ($erros ? '<ul><li>' . implode('</li><li>', array_map('e', $erros)) . '</li></ul>' : '')
           . '<p><a href="javascript:history.back()">Voltar e corrigir</a></p></body>';
    }
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') { http_response_code(405); header('Allow: POST'); exit; }

try {
    if (!cfg('aberto')) { http_response_code(503); responder(false, 'As inscrições para a rede ainda não estão abertas. Tente novamente em breve.'); }

    // Anti-robô: campo invisível precisa ficar vazio e o envio não pode acontecer em menos de 3 s.
    if (trim($_POST['site'] ?? '') !== '') { responder(true, 'ok'); }
    $t = (int)($_POST['t'] ?? 0);
    if ($t > 0 && (time() * 1000 - $t) < 3000) { responder(false, 'Envio muito rápido. Confira os dados e tente de novo.'); }
    if (excedeu('envio', 10, 3600)) { http_response_code(429); responder(false, 'Muitos envios em pouco tempo. Tente de novo mais tarde.'); }

    $txt = fn(string $k, int $max) => mb_substr(trim(preg_replace('/\s+/u', ' ', (string)($_POST[$k] ?? ''))), 0, $max);
    $longo = fn(string $k, int $max) => mb_substr(trim(str_replace("\r", '', (string)($_POST[$k] ?? ''))), 0, $max);
    $url = function (string $v): string {
        if ($v === '') { return ''; }
        if (!preg_match('~^https?://~i', $v)) { $v = 'https://' . $v; }
        return filter_var($v, FILTER_VALIDATE_URL) && preg_match('~^https?://[^\s/]+\.[^\s]+~i', $v) ? $v : '!';
    };

    $d = [
        'nome_profissional' => $txt('nome_profissional', 120),
        'cidade'            => $txt('cidade', 80),
        'uf'                => strtoupper($txt('uf', 2)),
        'regioes'           => $txt('regioes', 300),
        'instagram'         => $txt('instagram', 200),
        'outra_rede'        => $url($txt('outra_rede', 300)),
        'portfolio'         => $url($txt('portfolio', 300)),
        'apresentacao'      => $longo('apresentacao', 800),
        'contato_email'     => $txt('contato_email', 160),
        'contato_whatsapp'  => preg_replace('/\D+/', '', (string)($_POST['contato_whatsapp'] ?? '')),
        'observacoes'       => $longo('observacoes', 800),
    ];
    $areas = array_values(array_intersect(array_keys(AREAS), (array)($_POST['areas'] ?? [])));

    $erros = [];
    if (mb_strlen($d['nome_profissional']) < 2) { $erros[] = 'Informe seu nome profissional.'; }
    if (mb_strlen($d['cidade']) < 2) { $erros[] = 'Informe sua cidade.'; }
    if (!in_array($d['uf'], UFS, true)) { $erros[] = 'Escolha o estado.'; }
    if (mb_strlen($d['regioes']) < 2) { $erros[] = 'Conte em quais regiões ou cidades você aceita trabalhar.'; }
    $ig = preg_replace('~^(https?://)?(www\.)?instagram\.com/~i', '', $d['instagram']);
    $ig = trim($ig, " /@");
    if (!preg_match('/^[A-Za-z0-9._]{1,30}$/', $ig)) { $erros[] = 'Informe o @ do seu Instagram profissional.'; } else { $d['instagram'] = '@' . $ig; }
    if ($d['outra_rede'] === '!') { $erros[] = 'O link da outra rede não parece um endereço válido.'; }
    if ($d['portfolio'] === '' || $d['portfolio'] === '!') { $erros[] = 'Informe um link válido para o seu portfólio.'; }
    if (!$areas) { $erros[] = 'Escolha pelo menos uma área de atuação.'; }
    if (mb_strlen($d['apresentacao']) < 20) { $erros[] = 'Escreva uma breve apresentação (pelo menos uma frase).'; }
    if ($d['contato_email'] !== '' && !filter_var($d['contato_email'], FILTER_VALIDATE_EMAIL)) { $erros[] = 'O e-mail não parece válido.'; }
    if ($d['contato_whatsapp'] !== '' && !preg_match('/^\d{10,13}$/', $d['contato_whatsapp'])) { $erros[] = 'O WhatsApp precisa ter DDD e número.'; }
    if ($d['contato_email'] === '' && $d['contato_whatsapp'] === '') { $erros[] = 'Informe um e-mail ou WhatsApp para contato.'; }

    $cA = ($_POST['consent_analise'] ?? '') === 'sim';
    $cB = ($_POST['consent_publicacao'] ?? '') === 'sim';
    $cC = ($_POST['consent_compartilhar_contato'] ?? '') === 'sim';
    $cD = ($_POST['consent_novidades'] ?? '') === 'sim';
    $campos = $cB ? array_values(array_intersect(array_keys(CAMPOS_PUBLICAVEIS), (array)($_POST['campos_publicaveis'] ?? []))) : [];
    $canal = $cD ? (string)($_POST['canal_novidades'] ?? '') : '';
    if (!$cA) { $erros[] = 'Para analisarmos o cadastro, marque a autorização de uso das informações para análise e contato.'; }
    if ($cB && !$campos) { $erros[] = 'Escolha quais campos podem aparecer no diretório, ou desmarque essa autorização.'; }
    if ($cD && !in_array($canal, ['email', 'whatsapp'], true)) { $erros[] = 'Escolha por onde quer receber novidades.'; }
    if ($cD && $canal === 'email' && $d['contato_email'] === '') { $erros[] = 'Para receber novidades por e-mail, informe seu e-mail.'; }
    if ($cD && $canal === 'whatsapp' && $d['contato_whatsapp'] === '') { $erros[] = 'Para receber novidades por WhatsApp, informe seu WhatsApp.'; }

    registrar_tentativa('envio');
    if ($erros) { responder(false, 'Confira os campos abaixo.', $erros); }

    $p = db();
    $agora = agora();
    $p->prepare('INSERT INTO cadastros (criado_em, atualizado_em, status, nome_profissional, cidade, uf, regioes, instagram, outra_rede, portfolio, areas, apresentacao,
        contato_email, contato_whatsapp, observacoes, consent_analise, consent_publicacao, campos_publicaveis, consent_compartilhar_contato, consent_novidades, canal_novidades, versao_politica)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)')
      ->execute([$agora, $agora, 'recebido', $d['nome_profissional'], $d['cidade'], $d['uf'], $d['regioes'], $d['instagram'], $d['outra_rede'], $d['portfolio'],
        json_encode($areas), $d['apresentacao'], $d['contato_email'], $d['contato_whatsapp'], $d['observacoes'], 1, (int)$cB, json_encode($campos), (int)$cC, (int)$cD, $canal,
        (string)cfg('versao_politica')]);
    $id = (int)$p->lastInsertId();
    historico($id, 'recebido', 'Autorizações: análise=sim, publicação=' . ($cB ? 'sim' : 'não') . ', compartilhar contato=' . ($cC ? 'sim' : 'não') . ', novidades=' . ($cD ? $canal : 'não'));

    // Aviso opcional à equipe, SEM dados pessoais.
    $aviso = (string)cfg('aviso_email');
    if ($aviso !== '' && function_exists('mail')) {
        @mail($aviso, 'Novo cadastro de portfólio #' . $id, "Um novo cadastro foi recebido (#$id). Acesse a área da equipe para analisar.\n", 'Content-Type: text/plain; charset=utf-8');
    }
    responder(true, 'Recebemos seu portfólio.');
} catch (Throwable $ex) {
    error_log('cadastro: falha ao gravar (' . get_class($ex) . ')'); // sem dados pessoais
    http_response_code(500);
    responder(false, 'Não conseguimos salvar seu cadastro agora. Tente novamente em alguns minutos.');
}
