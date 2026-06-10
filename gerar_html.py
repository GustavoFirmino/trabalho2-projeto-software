# -*- coding: utf-8 -*-
"""Gera documentacao-projeto.html com os diagramas embutidos em base64."""
import base64
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
DIAG = os.path.join(BASE, "diagramas")

HTML = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Documentação de Projeto — AutoFix</title>
<style>
  :root { --vermelho: #FF0000; }
  * { box-sizing: border-box; }
  html { background: #808080; }
  body {
    font-family: 'Times New Roman', Times, serif;
    font-size: 12pt;
    color: #000000;
    margin: 0;
    padding: 24px 0;
  }
  .pagina {
    background: #ffffff;
    width: 8.5in;
    min-height: 11in;
    margin: 0 auto 24px auto;
    padding: 1in;
    box-shadow: 0 2px 8px rgba(0,0,0,.35);
  }
  p { text-align: justify; line-height: 1.25; margin: 0 0 10pt 0; }
  .dir { text-align: right; }
  .centro { text-align: center; }
  .vermelho { color: var(--vermelho); }
  .arial { font-family: Arial, Helvetica, sans-serif; }

  /* Capa — mesma formatação do template (Arial, negrito, alinhado à direita) */
  .capa-titulo   { font-family: Arial, Helvetica, sans-serif; font-size: 32pt; font-weight: bold; text-align: right; margin: 0 0 6pt 0; }
  .capa-sub     { font-family: Arial, Helvetica, sans-serif; font-size: 20pt; font-weight: bold; text-align: right; margin: 0 0 6pt 0; }
  .capa-versao  { font-family: Arial, Helvetica, sans-serif; font-size: 14pt; font-weight: bold; text-align: right; margin: 18pt 0 24pt 0; }
  .capa-aluno   { font-family: Arial, Helvetica, sans-serif; font-size: 12pt; text-align: right; margin: 0 0 4pt 0; }
  .capa-data    { font-family: Arial, Helvetica, sans-serif; font-size: 14pt; font-weight: bold; text-align: right; margin: 36pt 0 0 0; }

  /* Títulos de seção — Times, negrito, preto (como no template) */
  h1 { font-family: 'Times New Roman', Times, serif; font-size: 18pt; font-weight: bold; color: #000; margin: 24pt 0 12pt 0; }
  h2 { font-family: 'Times New Roman', Times, serif; font-size: 14pt; font-weight: bold; color: #000; margin: 14pt 0 14pt 0; }
  .titulo-bloco { font-family: 'Times New Roman', Times, serif; font-size: 18pt; font-weight: bold; margin: 24pt 0 12pt 0; }

  table { border-collapse: collapse; width: 100%; margin: 0 0 12pt 0; font-size: 11pt; }
  th, td { border: 1px solid #000; padding: 4pt 6pt; vertical-align: top; text-align: left; }
  th { font-weight: bold; }

  .toc { list-style: none; padding-left: 0; font-size: 12pt; }
  .toc li { margin: 2pt 0; }
  .toc .n1 { font-weight: bold; }
  .toc .n2 { padding-left: 24pt; }
  .toc a { color: #000; text-decoration: none; }
  .toc .pontos { float: right; }

  figure { margin: 12pt 0; text-align: center; page-break-inside: avoid; }
  figure img { max-width: 100%; height: auto; border: 0; }
  figcaption { font-size: 10pt; font-style: italic; margin-top: 6pt; text-align: center; }

  ul.atores { margin: 0 0 10pt 0; }
  ul.atores li { margin-bottom: 6pt; text-align: justify; }

  @media print {
    html { background: #fff; }
    .pagina { box-shadow: none; margin: 0 auto; width: auto; min-height: 0; padding: 0.6in; }
  }
</style>
</head>
<body>

<!-- ===================== CAPA ===================== -->
<div class="pagina">
  <div style="height: 2.2in"></div>
  <p class="capa-titulo">Documentação de Projeto</p>
  <p class="capa-sub">para o sistema</p>
  <p class="capa-titulo"><span class="vermelho">AutoFix — Gestão de Oficina Mecânica</span></p>
  <p class="capa-versao">Versão 1.0</p>
  <p class="capa-aluno">Projeto de sistema elaborado pelo(s) aluno(s) Gustavo Pessoa Firmino Duarte</p>
  <p class="capa-aluno">como parte da disciplina <b>Projeto de Software</b>.</p>
  <p class="capa-data"><span class="vermelho">10 de junho de 2026</span></p>
</div>

<!-- ===================== TABELA DE CONTEÚDO ===================== -->
<div class="pagina">
  <p class="titulo-bloco">Tabela de Conteúdo</p>
  <ul class="toc">
    <li class="n1"><a href="#s1">1. Introdução</a></li>
    <li class="n1"><a href="#s2">2. Modelos de Usuário e Requisitos</a></li>
    <li class="n2"><a href="#s21">2.1. Descrição de Atores</a></li>
    <li class="n2"><a href="#s22">2.2. Modelo de Casos de Uso</a></li>
    <li class="n2"><a href="#s23">2.3. Diagrama de Sequência do Sistema</a></li>
    <li class="n2"><a href="#s24">2.4. Contratos de Operação</a></li>
    <li class="n1"><a href="#s3">3. Modelos de Projeto</a></li>
    <li class="n2"><a href="#s31">3.1. Arquitetura</a></li>
    <li class="n2"><a href="#s32">3.2. Diagrama de Componentes e Implantação</a></li>
    <li class="n2"><a href="#s33">3.3. Diagrama de Classes</a></li>
    <li class="n2"><a href="#s34">3.4. Diagramas de Sequência</a></li>
    <li class="n2"><a href="#s35">3.5. Diagramas de Comunicação</a></li>
    <li class="n2"><a href="#s36">3.6. Diagramas de Estados</a></li>
    <li class="n1"><a href="#s4">4. Modelos de Dados</a></li>
  </ul>

  <p class="titulo-bloco">Histórico de Revisões</p>
  <table>
    <tr><th>Nome</th><th>Data</th><th>Razões para Mudança</th><th>Versão</th></tr>
    <tr>
      <td>Gustavo Pessoa Firmino Duarte</td>
      <td>10/06/2026</td>
      <td>Elaboração inicial do documento: modelos de usuário e requisitos, modelos de projeto e modelos de dados.</td>
      <td>1.0</td>
    </tr>
    <tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
    <tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
  </table>
</div>

<!-- ===================== 1. INTRODUÇÃO ===================== -->
<div class="pagina">
  <h1 id="s1">1. Introdução</h1>
  <p>Este documento agrega: 1) a elaboração e revisão de modelos de domínio e 2) modelos de
  projeto para o sistema <span class="vermelho">AutoFix — Gestão de Oficina Mecânica</span>.
  A referência principal para a descrição geral do problema, domínio e requisitos do sistema é o
  documento de especificação que descreve a visão de domínio do sistema.</p>

  <p>O <b>AutoFix</b> é um sistema de gestão para oficinas mecânicas de pequeno e médio porte.
  Ele informatiza o ciclo completo de atendimento da oficina: o cliente agenda um atendimento
  para o seu veículo; o atendente abre uma <b>Ordem de Serviço (OS)</b>; o mecânico registra o
  diagnóstico e emite um orçamento com serviços e peças; o cliente aprova (ou recusa) o
  orçamento; o mecânico executa os serviços aprovados, registrando as peças utilizadas (com
  baixa automática de estoque); e, por fim, o atendente finaliza a OS recebendo o pagamento —
  em dinheiro ou de forma eletrônica via gateway de pagamento. Em todas as etapas relevantes o
  cliente é notificado por e-mail. O gerente acompanha a operação por meio de relatórios
  gerenciais de faturamento, produtividade e estoque.</p>

  <p>Toda a diagramação deste documento foi produzida com <b>PlantUML</b>, e os arquivos-fonte
  (<i>.puml</i>) acompanham este documento na pasta <i>diagramas/</i>.</p>
</div>

<!-- ===================== 2. MODELOS DE USUÁRIO E REQUISITOS ===================== -->
<div class="pagina">
  <h1 id="s2">2. Modelos de Usuário e Requisitos</h1>

  <h2 id="s21">2.1. Descrição de Atores</h2>
  <p>Nesta subseção é apresentado descrição de cada um dos atores que interagem com o sistema.</p>
  <table>
    <tr><th style="width:18%">Ator</th><th>Descrição</th></tr>
    <tr><td><b>Cliente</b></td><td>Proprietário do veículo. Agenda atendimentos, acompanha o andamento da Ordem de Serviço, aprova ou recusa orçamentos e consulta o histórico de manutenções do seu veículo.</td></tr>
    <tr><td><b>Atendente</b></td><td>Funcionário responsável pela recepção. Cadastra clientes e veículos, abre Ordens de Serviço, gerencia agendamentos e registra o pagamento na entrega do veículo.</td></tr>
    <tr><td><b>Mecânico</b></td><td>Funcionário técnico. Realiza o diagnóstico do veículo, emite o orçamento (serviços e peças), executa os serviços aprovados e registra as peças utilizadas.</td></tr>
    <tr><td><b>Gerente</b></td><td>Responsável pela administração da oficina. Mantém o catálogo de serviços e o estoque de peças e gera relatórios gerenciais (faturamento, produtividade, estoque).</td></tr>
    <tr><td><b>Gateway de Pagamento</b></td><td><i>Sistema externo</i> que autoriza transações eletrônicas (cartão de crédito, débito e PIX).</td></tr>
    <tr><td><b>Servidor de E-mail</b></td><td><i>Sistema externo</i> (SMTP) utilizado para notificar o cliente sobre orçamentos emitidos, conclusão de serviços e emissão da nota de pagamento.</td></tr>
  </table>

  <h2 id="s22">2.2. Modelo de Casos de Uso</h2>
  <p>Nesta subseção é apresentado o diagrama de casos de uso do sistema. Para cada um deles,
  utiliza-se um ID que serve de referência no restante do documento (por exemplo, UC-01 para o
  Caso de Uso 01).</p>
  {{img:casos-de-uso|Figura 1 — Diagrama de Casos de Uso do sistema AutoFix (PlantUML).}}
  <table>
    <tr><th style="width:12%">ID</th><th style="width:32%">Caso de Uso</th><th>Descrição resumida</th></tr>
    <tr><td>UC-01</td><td>Agendar Atendimento</td><td>Cliente (ou atendente, por telefone) reserva data e hora para levar o veículo à oficina.</td></tr>
    <tr><td>UC-02</td><td>Cadastrar Cliente e Veículo</td><td>Atendente registra os dados do cliente e de seus veículos.</td></tr>
    <tr><td>UC-03</td><td>Abrir Ordem de Serviço</td><td>Atendente abre a OS vinculada ao veículo, com a queixa relatada pelo cliente.</td></tr>
    <tr><td>UC-04</td><td>Registrar Diagnóstico e Orçamento</td><td>Mecânico registra o diagnóstico e emite orçamento com serviços e peças; o cliente é notificado por e-mail.</td></tr>
    <tr><td>UC-05</td><td>Aprovar Orçamento</td><td>Cliente aprova ou recusa o orçamento emitido para a sua OS.</td></tr>
    <tr><td>UC-06</td><td>Executar Serviço</td><td>Mecânico executa os itens de serviço aprovados e marca cada item como concluído.</td></tr>
    <tr><td>UC-07</td><td>Registrar Peças Utilizadas</td><td>Mecânico registra as peças aplicadas na OS, com baixa automática no estoque.</td></tr>
    <tr><td>UC-08</td><td>Finalizar OS e Receber Pagamento</td><td>Atendente encerra a OS e registra o pagamento (dinheiro ou eletrônico via gateway); a nota é enviada por e-mail.</td></tr>
    <tr><td>UC-09</td><td>Consultar Histórico do Veículo</td><td>Cliente ou atendente consulta todas as manutenções já realizadas no veículo.</td></tr>
    <tr><td>UC-10</td><td>Gerar Relatórios Gerenciais</td><td>Gerente emite relatórios de faturamento, produtividade dos mecânicos e posição de estoque.</td></tr>
  </table>
</div>

<!-- ===================== 2.3 DSS ===================== -->
<div class="pagina">
  <h2 id="s23">2.3. Diagrama de Sequência do Sistema</h2>
  <p>Nesta subseção é apresentado o diagrama de sequência do sistema (DSS) de três Casos de Uso
  descritos na Seção 2.2: <b>UC-01 — Agendar Atendimento</b>, <b>UC-05 — Aprovar Orçamento</b> e
  <b>UC-08 — Finalizar OS e Receber Pagamento</b>. Em cada DSS o sistema é tratado como uma
  caixa-preta, evidenciando apenas os eventos trocados entre os atores e o sistema.</p>
  {{img:dss-uc01-agendar-atendimento|Figura 2 — DSS do UC-01 Agendar Atendimento.}}
  {{img:dss-uc05-aprovar-orcamento|Figura 3 — DSS do UC-05 Aprovar Orçamento.}}
  {{img:dss-uc08-finalizar-os|Figura 4 — DSS do UC-08 Finalizar OS e Receber Pagamento.}}
</div>

<!-- ===================== 2.4 CONTRATOS ===================== -->
<div class="pagina">
  <h2 id="s24">2.4. Contratos de Operação</h2>
  <p>Formato para cada contrato de operação:</p>

  <table>
    <tr><th style="width:24%">Contrato</th><td><b>CO-01 — agendarAtendimento</b></td></tr>
    <tr><th>Operação</th><td>agendarAtendimento(veiculoId, dataHora, descricaoProblema)</td></tr>
    <tr><th>Referências cruzadas</th><td>UC-01 — Agendar Atendimento</td></tr>
    <tr><th>Pré-condições</th><td>O cliente e o veículo estão cadastrados no sistema; o horário informado está dentro do expediente da oficina e disponível.</td></tr>
    <tr><th>Pós-condições</th><td>Uma instância de <i>Agendamento</i> foi criada com status AGENDADO; o agendamento foi associado ao cliente e ao veículo; o cliente foi notificado por e-mail com o código do agendamento.</td></tr>
  </table>

  <table>
    <tr><th style="width:24%">Contrato</th><td><b>CO-02 — aprovarOrcamento</b></td></tr>
    <tr><th>Operação</th><td>aprovarOrcamento(numeroOS)</td></tr>
    <tr><th>Referências cruzadas</th><td>UC-05 — Aprovar Orçamento</td></tr>
    <tr><th>Pré-condições</th><td>A OS existe e possui orçamento emitido com status AGUARDANDO_APROVACAO; o solicitante é o cliente proprietário do veículo da OS.</td></tr>
    <tr><th>Pós-condições</th><td>O atributo <i>aprovado</i> do <i>Orcamento</i> foi definido como verdadeiro; o status da <i>OrdemServico</i> foi alterado para APROVADA; o mecânico responsável foi notificado para iniciar a execução.</td></tr>
  </table>

  <table>
    <tr><th style="width:24%">Contrato</th><td><b>CO-03 — registrarPagamento</b></td></tr>
    <tr><th>Operação</th><td>registrarPagamento(numeroOS, formaPagamento, valor)</td></tr>
    <tr><th>Referências cruzadas</th><td>UC-08 — Finalizar OS e Receber Pagamento</td></tr>
    <tr><th>Pré-condições</th><td>A OS está com status FINALIZADA; o valor informado corresponde ao valor total calculado da OS; em pagamento eletrônico, o gateway autorizou a transação.</td></tr>
    <tr><th>Pós-condições</th><td>Uma instância de <i>Pagamento</i> foi criada e associada à OS (com NSU, quando eletrônico); o status da <i>OrdemServico</i> foi alterado para PAGA; a nota foi enviada por e-mail ao cliente; o veículo foi liberado para entrega.</td></tr>
  </table>
</div>

<!-- ===================== 3. MODELOS DE PROJETO ===================== -->
<div class="pagina">
  <h1 id="s3">3. Modelos de Projeto</h1>

  <h2 id="s31">3.1. Arquitetura</h2>
  <p>A arquitetura do AutoFix é descrita com um diagrama apropriado da UML. Adotou-se o estilo
  <b>arquitetura em camadas (MVC)</b>: uma SPA em React consome uma API REST construída em
  Spring Boot, organizada em camadas de apresentação (<i>controllers</i>), negócio
  (<i>services</i>), persistência (<i>repositories</i>) e domínio (entidades JPA), sobre um banco
  PostgreSQL. As integrações externas (gateway de pagamento e servidor SMTP) são acessadas
  exclusivamente pela camada de negócio.</p>
  {{img:arquitetura|Figura 5 — Arquitetura em camadas do sistema AutoFix.}}
</div>

<div class="pagina">
  <h2 id="s32">3.2. Diagrama de Componentes e Implantação</h2>
  <p>Diagramas de componentes do sistema e diagrama de implantação mostrando onde os componentes
  estarão alocados para a execução. O back-end é modularizado por área de negócio (agendamento,
  OS, orçamento, pagamento, estoque, notificação e relatórios); em produção, a aplicação roda em
  contêineres Docker (Nginx como proxy reverso, API Spring Boot e PostgreSQL) hospedados em um
  servidor cloud.</p>
  {{img:componentes|Figura 6 — Diagrama de Componentes do AutoFix.}}
  {{img:implantacao|Figura 7 — Diagrama de Implantação do AutoFix.}}
</div>

<div class="pagina">
  <h2 id="s33">3.3. Diagrama de Classes</h2>
  <p>Diagrama de classes do sistema. As classes centrais do domínio são <i>OrdemServico</i> (com
  seus itens de serviço e de peça), <i>Orcamento</i>, <i>Agendamento</i> e <i>Pagamento</i>.
  Utiliza-se herança para <i>Pessoa</i> → <i>Cliente</i>/<i>Funcionario</i> e
  <i>Funcionario</i> → <i>Atendente</i>/<i>Mecanico</i>, além de enumerações para os estados e
  formas de pagamento.</p>
  {{img:classes|Figura 8 — Diagrama de Classes do AutoFix.}}
</div>

<div class="pagina">
  <h2 id="s34">3.4. Diagramas de Sequência</h2>
  <p>Diagramas de sequência para realização de casos de uso. São detalhadas as realizações de
  <b>UC-05 — Aprovar Orçamento</b> e <b>UC-08 — Finalizar OS e Receber Pagamento</b>, mostrando a
  colaboração entre controladores, serviços, repositórios e sistemas externos.</p>
  {{img:seq-uc05-aprovar-orcamento|Figura 9 — Diagrama de Sequência da realização do UC-05.}}
  {{img:seq-uc08-finalizar-os|Figura 10 — Diagrama de Sequência da realização do UC-08.}}
</div>

<div class="pagina">
  <h2 id="s35">3.5. Diagramas de Comunicação</h2>
  <p>Diagramas de comunicação para realização de casos de uso. As mesmas colaborações são
  apresentadas sob a perspectiva estrutural, com a numeração das mensagens indicando a ordem das
  interações.</p>
  {{img:comunicacao-uc01|Figura 11 — Diagrama de Comunicação da realização do UC-01.}}
  {{img:comunicacao-uc05|Figura 12 — Diagrama de Comunicação da realização do UC-05.}}
</div>

<div class="pagina">
  <h2 id="s36">3.6. Diagramas de Estados</h2>
  <p>Diagramas de estados do sistema. O ciclo de vida da <i>Ordem de Serviço</i> é o mais rico do
  domínio: da abertura ao diagnóstico, passando pela aprovação (ou recusa) do orçamento, execução,
  finalização e pagamento — com possibilidade de cancelamento nas fases iniciais.</p>
  {{img:estados-ordem-servico|Figura 13 — Diagrama de Estados da Ordem de Serviço.}}
</div>

<!-- ===================== 4. MODELOS DE DADOS ===================== -->
<div class="pagina">
  <h1 id="s4">4. Modelos de Dados</h1>
  <p>Apresentam-se a seguir os esquemas de banco de dados e as estratégias de mapeamento entre as
  representações de objetos e não-objetos.</p>
  {{img:modelo-er|Figura 14 — Modelo de Dados (ER) do AutoFix.}}
  <p><b>Estratégia de mapeamento objeto-relacional (ORM):</b> o mapeamento entre objetos e
  tabelas é realizado com <b>JPA/Hibernate</b>, segundo as decisões abaixo:</p>
  <table>
    <tr><th style="width:34%">Decisão de mapeamento</th><th>Estratégia adotada</th></tr>
    <tr><td>Herança <i>Pessoa</i> → <i>Cliente</i>/<i>Funcionario</i></td><td>Uma tabela por classe concreta (TABLE_PER_CLASS achatada em <i>clientes</i> e <i>funcionarios</i>), pois os subtipos têm atributos e relacionamentos distintos e não há consultas polimórficas relevantes.</td></tr>
    <tr><td>Herança <i>Atendente</i>/<i>Mecanico</i></td><td>Discriminador <i>cargo</i> na tabela única <i>funcionarios</i> (SINGLE_TABLE), pois os campos específicos são poucos.</td></tr>
    <tr><td>Enumerações (<i>StatusOS</i>, <i>FormaPagamento</i>, ...)</td><td>Persistidas como <i>VARCHAR</i> (EnumType.STRING), privilegiando legibilidade do esquema.</td></tr>
    <tr><td>Associações 1:N (ex.: OS → itens)</td><td>Chave estrangeira no lado N, com carregamento LAZY e cascata na agregação composta (itens pertencem à OS).</td></tr>
    <tr><td>Associações 1:1 (OS → Orçamento, OS → Pagamento)</td><td>Chave estrangeira com restrição UNIQUE na tabela dependente.</td></tr>
    <tr><td>Valores monetários</td><td><i>NUMERIC(10,2)</i> mapeado para <i>BigDecimal</i>, evitando erros de ponto flutuante.</td></tr>
  </table>
</div>

</body>
</html>
"""

def embed(match):
    name, caption = match.group(1), match.group(2)
    path = os.path.join(DIAG, name + ".png")
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return (f'<figure><img src="data:image/png;base64,{b64}" alt="{caption}">'
            f'<figcaption>{caption}</figcaption></figure>')

out = re.sub(r"\{\{img:([a-z0-9\-]+)\|([^}]+)\}\}", embed, HTML)
dest = os.path.join(BASE, "documentacao-projeto.html")
with open(dest, "w", encoding="utf-8") as f:
    f.write(out)
print("OK", dest, len(out), "bytes")
