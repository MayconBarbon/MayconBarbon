# Define o formulário de briefing do Studio 3D no Contact Form 7 (campos espelham a página /construtoras)
PERFIL=["Construtora","Incorporadora","Engenheiro civil","Arquiteto","Imobiliária","Outro"]
TIPO=["Casa","Apartamento","Condomínio","Edifício residencial","Projeto comercial","Clínica","Escritório","Outro"]
FINAL=["Apresentação ao cliente","Aprovação de conceito","Material comercial","Pré-lançamento","Campanha publicitária","Apresentação para investidores"]
SERV=["3D essencial","3D com acabamentos","3D decorado","Imagens renderizadas","Vídeo cinematográfico"]
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
FORM=f'''[text* nome] [text empresa] [text cargo] [email* email] [tel* whatsapp] [text* cidade_uf]
[select* perfil {q(PERFIL)}]
[select* tipo_projeto {q(TIPO)}] [text area_m2] [text pavimentos] [text ambientes] [text cidade_obra]
[checkbox finalidade {q(FINAL)}]
[file arq_planta {FT}] [file arq_complementar {FT}] [file arq_referencias {FT}] [file arq_3d {FT}] [text link_arquivos]
[checkbox* servicos {q(SERV)}] [textarea obs_servicos]
[radio acabamentos_definidos {q(ACAB)}] [textarea acabamentos_detalhe]
[checkbox estilo {q(ESTILO)}] [textarea estilo_descricao]
[radio mobiliario {q(MOB)}] [text paleta]
[radio video_duracao {q(VDUR)}] [radio video_formato {q(VFMT)}] [checkbox video_aplicacao {q(VAPL)}] [radio video_estilo {q(VEST)}] [checkbox video_extras {q(VEXT)}]
[select faixa_investimento {q(FAIXA)}] [text prazo_desejado] [textarea observacoes]
[acceptance aceite_autorizacao] Autorizo [/acceptance]
[acceptance aceite_conceitual] Ciência [/acceptance]
[acceptance aceite_privacidade] Privacidade [/acceptance]
[acceptance optin_marketing optional] Marketing [/acceptance]
[acceptance optin_portfolio optional] Portfólio [/acceptance]
[text protocolo]
[submit "Enviar"]'''
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
