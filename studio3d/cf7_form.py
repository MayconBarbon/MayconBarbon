# Define o formulário de briefing do Studio 3D no Contact Form 7 (campos espelham a página /construtoras)
PERFIL=["Construtora","Incorporadora","Engenheiro civil","Arquiteto","Imobiliária","Outro"]
TIPO=["Casa","Apartamento","Condomínio","Edifício residencial","Projeto comercial","Clínica","Escritório","Outro"]
FINAL=["Apresentação ao cliente","Aprovação de conceito","Material comercial","Pré-lançamento","Campanha publicitária","Apresentação para investidores"]
ACAB=["Sim, vou enviar as especificações","Parcialmente","Não, preciso de uma proposta visual conceitual"]
ESTILO=["Contemporâneo","Minimalista","Clássico","Industrial","Escandinavo","Natural / orgânico","Luxo contemporâneo","Outro"]
MOB=["Sem mobiliário","Mobiliário básico para percepção de escala","Ambiente totalmente mobiliado","Decoração completa","Seguir projeto de interiores existente","Criar proposta conceitual sujeita a aprovação"]
VDUR=["15 a 30 segundos","30 a 60 segundos","60 a 90 segundos","Sob consulta"]
VFMT=["Vertical","Horizontal","Ambos"]
VAPL=["Instagram","Anúncios","Site","Estande de vendas","Apresentação comercial"]
VEST=["Cinematográfico","Minimalista","Institucional","Luxo / editorial"]
VEXT=["Lettering","Narração","Trilha","Assinatura da marca"]
FAIXA=["Prefiro não informar","Até R$ 3 mil","R$ 3 mil a R$ 8 mil","R$ 8 mil a R$ 20 mil","Acima de R$ 20 mil"]
q=lambda xs:' '.join('"%s"'%x for x in xs)
FT='filetypes:pdf|jpg|jpeg|png|dwg|dxf|ifc|skp|rvt|fbx|obj|glb|3dm limit:6mb'
SERV=["3D Essencial","3D com Acabamentos","3D Decorado","Imagens renderizadas","Vídeo cinematográfico (Cinematic)"]
def nav(prev=True, nxt=True, submit=False):
    l = '<button type="button" class="btn btn-g" data-go="-1">Voltar</button>' if prev else '<span></span>'
    r = '[submit "Enviar briefing"]' if submit else '<button type="button" class="btn btn-p" data-go="1">Continuar</button>'
    return f'<div class="nav">{l}{r}</div>'
def L(lbl, tag): return f'<div><label>{lbl}</label>{tag}</div>'
FORM = '\n'.join([
 '<div class="st on" data-step="voce"><h3>Você e a empresa</h3><p class="sub">Campos com * são obrigatórios.</p>',
 '<h4>A · Identificação</h4>',
 '<div class="g2">' + L('Nome *','[text* nome autocomplete:name]') + L('Empresa','[text empresa autocomplete:organization]') + '</div>',
 '<div class="g2">' + L('Cargo','[text cargo]') + L('E-mail *','[email* email autocomplete:email]') + '</div>',
 '<div class="g2">' + L('WhatsApp *','[tel* whatsapp autocomplete:tel placeholder "(19) 99999-9999"]') + L('Cidade / UF *','[text* cidade_uf placeholder "Piracicaba / SP"]') + '</div>',
 '<h4>B · Perfil</h4>',
 L('Você é *', f'[select* perfil include_blank {q(PERFIL)}]'),
 nav(prev=False), '</div>',
 '<div class="st" data-step="projeto"><h3>O projeto</h3>',
 '<h4>C · Dados do projeto</h4>',
 L('Tipo de projeto *', f'[select* tipo_projeto include_blank {q(TIPO)}]'),
 '<div class="g2">' + L('Área aproximada (m²)','[text area_m2]') + L('Pavimentos','[text pavimentos]') + '</div>',
 '<div class="g2">' + L('Ambientes a representar','[text ambientes placeholder "ex.: sala, cozinha, 2 dormitórios"]') + L('Cidade do empreendimento','[text cidade_obra]') + '</div>',
 '<h4>D · Finalidade</h4>',
 f'[checkbox finalidade use_label_element {q(FINAL)}]',
 nav(), '</div>',
 '<div class="st" data-step="arquivos"><h3>Arquivos</h3><p class="sub">Até 6 MB por arquivo: PDF, JPG, PNG, DWG, DXF, IFC, SKP, RVT, FBX, OBJ, GLB ou 3DM. Arquivos maiores: use o campo de link.</p>',
 '<h4>E · Envio dos arquivos</h4>',
 L('Planta baixa', f'[file arq_planta {FT}]'),
 L('Cortes, fachadas ou memorial', f'[file arq_complementar {FT}]'),
 L('Referências visuais', f'[file arq_referencias {FT}]'),
 L('Modelo 3D (se houver)', f'[file arq_3d {FT}]'),
 L('Link para arquivos grandes','[text link_arquivos placeholder "Google Drive, WeTransfer, Dropbox"]'),
 nav(), '</div>',
 '<div class="st" data-step="entrega"><h3>O que você precisa</h3>',
 '<h4>F · Serviços *</h4>',
 f'[checkbox* servicos use_label_element {q(SERV)}]',
 L('Observações sobre a entrega','[textarea obs_servicos x3]'),
 '<h4>G · Acabamentos</h4>',
 f'[checkbox acabamentos_definidos exclusive use_label_element {q(ACAB)}]',
 L('Detalhes ou memorial (resumo)','[textarea acabamentos_detalhe x3]'),
 '<h4>H · Estilo e mobiliário</h4>',
 f'[checkbox estilo use_label_element {q(ESTILO)}]',
 L('Descreva o estilo, se quiser','[textarea estilo_descricao x3]'),
 f'[checkbox mobiliario exclusive use_label_element {q(MOB)}]',
 L('Paleta de cores ou referências','[text paleta]'),
 nav(), '</div>',
 '<div class="st" data-step="video"><h3>Vídeo</h3><p class="sub">Só aparece quando o vídeo cinematográfico está marcado.</p>',
 '<h4>I · Vídeo cinematográfico</h4>',
 L('Duração', f'[checkbox video_duracao exclusive use_label_element {q(VDUR)}]'),
 L('Formato', f'[checkbox video_formato exclusive use_label_element {q(VFMT)}]'),
 L('Onde vai ser usado', f'[checkbox video_aplicacao use_label_element {q(VAPL)}]'),
 L('Estilo', f'[checkbox video_estilo exclusive use_label_element {q(VEST)}]'),
 L('Extras', f'[checkbox video_extras use_label_element {q(VEXT)}]'),
 nav(), '</div>',
 '<div class="st" data-step="envio"><h3>Prazo e envio</h3>',
 '<h4>J · Investimento e prazo</h4>',
 '<div class="g2">' + L('Faixa de investimento', f'[select faixa_investimento {q(FAIXA)}]') + L('Prazo desejado','[text prazo_desejado placeholder "ex.: até 30/01"]') + '</div>',
 L('Observações gerais','[textarea observacoes x4]'),
 '<h4>K · Autorizações</h4>',
 '[acceptance aceite_autorizacao] Declaro que tenho autorização para compartilhar estes arquivos e que eles podem ser usados pela Vídeo Imóvel exclusivamente para elaborar a proposta e o projeto. [/acceptance]',
 '[acceptance aceite_conceitual] Estou ciente de que as imagens 3D são ilustrativas, feitas a partir dos arquivos enviados, e não substituem o projeto aprovado. [/acceptance]',
 '[acceptance aceite_privacidade] Li e concordo com a <a href="/politica-de-privacidade/" target="_blank">política de privacidade</a> e com o tratamento dos meus dados para contato sobre esta solicitação. [/acceptance]',
 '[acceptance optin_marketing optional] Aceito receber novidades da Vídeo Imóvel por e-mail ou WhatsApp. (opcional) [/acceptance]',
 '[acceptance optin_portfolio optional] Autorizo o uso do projeto no portfólio da Vídeo Imóvel depois do lançamento. (opcional) [/acceptance]',
 '[hidden protocolo]',
 nav(submit=True), '</div>',
])
BODY='''Novo briefing Studio 3D · Protocolo [protocolo]

IDENTIFICAÇÃO
Nome: [nome] · Empresa: [empresa] · Cargo: [cargo]
E-mail: [email] · WhatsApp: [whatsapp] · Cidade/UF: [cidade_uf] · Perfil: [perfil]

PROJETO
Tipo: [tipo_projeto] · Área: [area_m2] m² · Pavimentos: [pavimentos] · Ambientes: [ambientes]
Cidade do empreendimento: [cidade_obra]
Finalidade: [finalidade]

ARQUIVOS (anexados a este e-mail quando enviados)
Link externo: [link_arquivos]

ENTREGA
Serviços: [servicos]
Observações: [obs_servicos]

ACABAMENTOS
Definidos: [acabamentos_definidos]
[acabamentos_detalhe]

ESTILO
[estilo]
[estilo_descricao]

MOBILIÁRIO
[mobiliario] · Paleta: [paleta]

VÍDEO
Duração: [video_duracao] · Formato: [video_formato] · Aplicação: [video_aplicacao]
Estilo: [video_estilo] · Extras: [video_extras]

ORÇAMENTO E PRAZO
Faixa: [faixa_investimento] · Prazo desejado: [prazo_desejado]
Observações gerais: [observacoes]

AUTORIZAÇÕES
Autorização de uso dos arquivos: [aceite_autorizacao]
Ciência do caráter conceitual: [aceite_conceitual]
Política de privacidade: [aceite_privacidade]
Comunicações de marketing: [optin_marketing]
Uso no portfólio: [optin_portfolio]
'''
CONF='''Olá, [nome]!

Recebemos o seu briefing para o Vídeo Imóvel Studio 3D.
Protocolo: [protocolo]

Nossa equipe vai analisar os arquivos, o escopo e a complexidade do projeto e enviar uma proposta personalizada. Se faltar alguma informação, entraremos em contato pelo WhatsApp [whatsapp] ou por este e-mail.

Resumo
Projeto: [tipo_projeto] · [cidade_obra]
Serviços: [servicos]

Vídeo Imóvel · Studio 3D
videoimovel.com.br/construtoras
'''
ATT='[arq_planta]\n[arq_complementar]\n[arq_referencias]\n[arq_3d]'


if __name__ == '__main__':
    # Salva o formulário pela tela de administração do CF7 (a API REST de criação não grava neste site).
    # O e-mail de confirmação ao solicitante (mail_2) fica DESATIVADO até haver CAPTCHA/Turnstile.
    import pickle, json, re, html
    W = '/tmp/claude-0/-home-user-MayconBarbon/23adc415-3614-5acc-b755-85d3f8a0a095/scratchpad/wp'
    B = 'https://videoimovel.com.br'
    ss = pickle.load(open(W + '/sess.pkl', 'rb')); st = json.load(open(W + '/studio3d.json'))
    fid = st.get('cf7_id') or -1
    pg = ss.get(B + (f'/wp-admin/admin.php?page=wpcf7&post={fid}&action=edit' if fid != -1 else '/wp-admin/admin.php?page=wpcf7-new'), timeout=30).text
    nonce = re.search(r'name="_wpnonce" value="([^"]+)"', pg).group(1)
    msgs = {k: html.unescape(v) for k, v in re.findall(r'name="wpcf7-messages\[(\w+)\]"[^>]*value="([^"]*)"', pg)}
    d = {'_wpnonce': nonce, 'post_ID': str(fid), 'action': 'save', 'active-tab': '0', 'wpcf7-locale': 'pt_BR',
         'post_title': 'Studio 3D · Briefing construtoras', 'wpcf7-form': FORM,
         'wpcf7-mail[active]': '1', 'wpcf7-mail[recipient]': '[_site_admin_email]', 'wpcf7-mail[sender]': '[_site_title] <wordpress@videoimovel.com.br>',
         'wpcf7-mail[subject]': 'Studio 3D · Novo briefing [protocolo] · [empresa] [nome]', 'wpcf7-mail[additional_headers]': 'Reply-To: [email]',
         'wpcf7-mail[body]': BODY, 'wpcf7-mail[attachments]': ATT, 'wpcf7-mail[exclude_blank]': '1',
         'wpcf7-mail-2[recipient]': '[email]', 'wpcf7-mail-2[sender]': '[_site_title] <wordpress@videoimovel.com.br>',
         'wpcf7-mail-2[subject]': 'Recebemos seu briefing · Protocolo [protocolo]', 'wpcf7-mail-2[additional_headers]': 'Reply-To: [_site_admin_email]',
         'wpcf7-mail-2[body]': CONF, 'wpcf7-mail-2[attachments]': '', 'wpcf7-mail-2[exclude_blank]': '1',
         'wpcf7-additional-settings': 'flamingo_email: "[email]"\nflamingo_name: "[nome]"\nflamingo_subject: "Briefing [protocolo] · [empresa] · [tipo_projeto]"', 'wpcf7-save': 'Salvar'}
    for k, v in msgs.items(): d[f'wpcf7-messages[{k}]'] = v
    r = ss.post(B + f'/wp-admin/admin.php?page=wpcf7&post={fid}', data=d, timeout=60)
    m = re.search(r'post=(\d+)', r.url); print(r.status_code, r.url)
    if m: st['cf7_id'] = int(m.group(1)); json.dump(st, open(W + '/studio3d.json', 'w'))
