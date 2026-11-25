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
 f'[radio acabamentos_definidos use_label_element {q(ACAB)}]',
 L('Detalhes ou memorial (resumo)','[textarea acabamentos_detalhe x3]'),
 '<h4>H · Estilo e mobiliário</h4>',
 f'[checkbox estilo use_label_element {q(ESTILO)}]',
 L('Descreva o estilo, se quiser','[textarea estilo_descricao x3]'),
 f'[radio mobiliario use_label_element {q(MOB)}]',
 L('Paleta de cores ou referências','[text paleta]'),
 nav(), '</div>',
 '<div class="st" data-step="video"><h3>Vídeo</h3><p class="sub">Só aparece quando o vídeo cinematográfico está marcado.</p>',
 '<h4>I · Vídeo cinematográfico</h4>',
 L('Duração', f'[radio video_duracao use_label_element {q(VDUR)}]'),
 L('Formato', f'[radio video_formato use_label_element {q(VFMT)}]'),
 L('Onde vai ser usado', f'[checkbox video_aplicacao use_label_element {q(VAPL)}]'),
 L('Estilo', f'[radio video_estilo use_label_element {q(VEST)}]'),
 L('Extras', f'[checkbox video_extras use_label_element {q(VEXT)}]'),
 nav(), '</div>',
 '<div class="st" data-step="envio"><h3>Prazo e envio</h3>',
 '<h4>J · Investimento e prazo</h4>',
 '<div class="g2">' + L('Faixa de investimento', f'[select faixa_investimento {q(FAIXA)}]') + L('Prazo desejado','[text prazo_desejado placeholder "ex.: até 30/01"]') + '</div>',
 L('Observações gerais','[textarea observacoes x4]'),
 '<h4>K · Autorizações</h4>',
 '[acceptance aceite_autorizacao] Declaro que tenho autorização para compartilhar estes arquivos e que eles podem ser usados pela Vídeo Imóvel exclusivamente para elaborar a proposta e o projeto. [/acceptance]',
 '[acceptance aceite_conceitual] Estou ciente de que as imagens 3D são ilustrativas, feitas a partir dos arquivos enviados, e não substituem o projeto aprovado. [/acceptance]',
 '[acceptance aceite_privacidade] Li e concordo com o tratamento dos meus dados para contato sobre esta solicitação, conforme a LGPD. [/acceptance]',
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
    # cria (ou atualiza) o formulário no WordPress; segunda mensagem (confirmação ao solicitante) fica DESATIVADA até haver CAPTCHA/Turnstile
    import pickle, json, os, sys
    W = '/tmp/claude-0/-home-user-MayconBarbon/23adc415-3614-5acc-b755-85d3f8a0a095/scratchpad/wp'
    B = 'https://videoimovel.com.br'
    ss = pickle.load(open(W + '/sess.pkl', 'rb'))
    st = json.load(open(W + '/studio3d.json'))
    data = {
        'title': 'Studio 3D · Briefing construtoras',
        'locale': 'pt_BR',
        'form': FORM,
        'mail': {'active': True, 'recipient': '[_site_admin_email]', 'sender': '[_site_title] <wordpress@videoimovel.com.br>',
                 'subject': 'Studio 3D · Novo briefing [protocolo] · [empresa] [nome]', 'body': BODY, 'additional_headers': 'Reply-To: [email]',
                 'attachments': ATT, 'use_html': False, 'exclude_blank': True},
        'mail_2': {'active': False, 'recipient': '[email]', 'sender': '[_site_title] <wordpress@videoimovel.com.br>',
                   'subject': 'Recebemos seu briefing · Protocolo [protocolo]', 'body': CONF, 'additional_headers': 'Reply-To: [_site_admin_email]',
                   'attachments': '', 'use_html': False, 'exclude_blank': True},
        'messages': {
            'mail_sent_ok': 'Briefing enviado. Confira o número da solicitação abaixo.',
            'mail_sent_ng': 'Não conseguimos enviar o briefing agora. Tente de novo em alguns minutos ou fale com a gente pelo WhatsApp (19) 99861-2626.',
            'validation_error': 'Há campos com erro. Confira as etapas destacadas.',
            'spam': 'Não conseguimos enviar o briefing agora. Fale com a gente pelo WhatsApp (19) 99861-2626.',
            'accept_terms': 'Para enviar, marque as autorizações obrigatórias.',
            'invalid_required': 'Campo obrigatório.',
            'invalid_too_long': 'Texto longo demais.', 'invalid_too_short': 'Texto curto demais.',
            'upload_failed': 'Falha no envio do arquivo. Tente de novo ou use o campo de link.',
            'upload_file_type_invalid': 'Tipo de arquivo não aceito. Use o campo de link.',
            'upload_file_too_large': 'Arquivo acima de 6 MB. Envie pelo campo de link.',
            'upload_failed_php_error': 'Falha no envio do arquivo. Tente de novo ou use o campo de link.',
            'invalid_email': 'E-mail inválido.', 'invalid_tel': 'Telefone inválido.',
        },
        'additional_settings': '',
    }
    fid = st.get('cf7_id')
    url = B + '/wp-json/contact-form-7/v1/contact-forms' + (f'/{fid}' if fid else '')
    r = ss.post(url, json=data, timeout=60); j = r.json()
    print(r.status_code, j.get('id'), j.get('config_errors'))
    if j.get('id'):
        st['cf7_id'] = j['id']; json.dump(st, open(W + '/studio3d.json', 'w'))
