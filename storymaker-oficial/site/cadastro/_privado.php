<?php
// Localiza a pasta privada (fora do public_html). Na Hostinger:
//   .../public_html/cadastro/   ->   .../storymaker-privado/
// Se a pasta ficar em outro lugar, defina a variável de ambiente STORYMAKER_PRIVADO.
declare(strict_types=1);
if (basename($_SERVER['SCRIPT_FILENAME'] ?? '') === '_privado.php') { http_response_code(404); exit; }
$__privado = getenv('STORYMAKER_PRIVADO') ?: dirname(__DIR__, 2) . '/storymaker-privado';
require $__privado . '/lib.php';
