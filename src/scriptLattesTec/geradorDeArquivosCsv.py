#!/usr/bin/python
# encoding: utf-8
#
#
# scriptLattesTec
# https://github.com/raphaeldeaquino/scriptLattesTec
#
# Este programa é um software livre; você pode redistribui-lo e/ou
# modifica-lo dentro dos termos da Licença Pública Geral GNU como
# publicada pela Fundação do Software Livre (FSF); na versão 2 da 
# Licença, ou (na sua opinião) qualquer versão.
#
# Este programa é distribuído na esperança que possa ser util, 
# mas SEM NENHUMA GARANTIA; sem uma garantia implicita de ADEQUAÇÂO a qualquer
# MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a
# Licença Pública Geral GNU para maiores detalhes.
#
# Você deve ter recebido uma cópia da Licença Pública Geral GNU
# junto com este programa, se não, escreva para a Fundação do Software
# Livre(FSF) Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
from collections import defaultdict
import datetime
import os
import re
import unicodedata
import logging

import pandas
from pandas.core.indexing import IndexingError
from .charts.graficoDeInternacionalizacao import *
from .highcharts import *  # highcharts
from .membro import *

logger = logging.getLogger('scriptLattes')


class GeradorDeArquivosCsv:
    grupo = None
    dir = None
    version = None
    arquivoRis = None

    def __init__(self, grupo):
        self.grupo = grupo
        self.version = 'V8.11'
        self.dir = self.grupo.obterParametro('global-diretorio_de_saida')

        # self.gerar_pagina_de_metricas()
        self.gerarArquivosDeProducoesBibliograficas()
        self.gerarArquivosDeProducoesTecnicas()
        '''
        if self.grupo.obterParametro('relatorio-mostrar_orientacoes'):
            self.gerarPaginasDeOrientacoes()

        if self.grupo.obterParametro('relatorio-incluir_projeto'):
            self.gerarPaginasDeProjetos()

        if self.grupo.obterParametro('relatorio-incluir_premio'):
            self.gerarPaginasDePremios()

        if self.grupo.obterParametro('relatorio-incluir_participacao_em_evento'):
            self.gerarPaginasDeParticipacaoEmEventos()

        # if self.grupo.obterParametro('relatorio-incluir_organizacao_de_evento'):
        #    self.gerarPaginasDeOrganizacaoDeEventos()

        if self.grupo.obterParametro('grafo-mostrar_grafo_de_colaboracoes'):
            self.gerarPaginaDeGrafosDeColaboracoes()

        if self.grupo.obterParametro('relatorio-incluir_internacionalizacao'):
            self.gerarPaginasDeInternacionalizacao()
        '''

    def gerarArquivosDeProducoesBibliograficas(self):
        self.nPB0 = 0
        self.nPB1 = 0
        self.nPB2 = 0
        self.nPB3 = 0
        self.nPB4 = 0
        self.nPB5 = 0
        self.nPB6 = 0
        self.nPB7 = 0
        self.nPB8 = 0
        self.nPB9 = 0
        self.nPB = 0

        if self.grupo.obterParametro('relatorio-incluir_artigo_em_periodico'):
            self.nPB0 = self.gerar_arquivo_de_producoes(self.grupo.compilador.listaCompletaArtigoEmPeriodico, "PB0")
        if self.grupo.obterParametro('relatorio-incluir_livro_publicado'):
            self.nPB1 = self.gerar_arquivo_de_producoes(self.grupo.compilador.listaCompletaLivroPublicado, "PB1")
        if self.grupo.obterParametro('relatorio-incluir_capitulo_de_livro_publicado'):
            self.nPB2 = self.gerar_arquivo_de_producoes(self.grupo.compilador.listaCompletaCapituloDeLivroPublicado,
                                                        "PB2")
        if self.grupo.obterParametro('relatorio-incluir_texto_em_jornal_de_noticia'):
            self.nPB3 = self.gerar_arquivo_de_producoes(self.grupo.compilador.listaCompletaTextoEmJornalDeNoticia,
                                                        "PB3")
        if self.grupo.obterParametro('relatorio-incluir_trabalho_completo_em_congresso'):
            self.nPB4 = self.gerar_arquivo_de_producoes(self.grupo.compilador.listaCompletaTrabalhoCompletoEmCongresso,
                                                        "PB4")
        if self.grupo.obterParametro('relatorio-incluir_resumo_expandido_em_congresso'):
            self.nPB5 = self.gerar_arquivo_de_producoes(self.grupo.compilador.listaCompletaResumoExpandidoEmCongresso,
                                                        "PB5")
        if self.grupo.obterParametro('relatorio-incluir_resumo_em_congresso'):
            self.nPB6 = self.gerar_arquivo_de_producoes(self.grupo.compilador.listaCompletaResumoEmCongresso,
                                                        "PB6")
        if self.grupo.obterParametro('relatorio-incluir_artigo_aceito_para_publicacao'):
            self.nPB7 = self.gerar_arquivo_de_producoes(self.grupo.compilador.listaCompletaArtigoAceito,
                                                        "PB7")
        if self.grupo.obterParametro('relatorio-incluir_outro_tipo_de_producao_bibliografica'):
            self.nPB9 = self.gerar_arquivo_de_producoes(
                self.grupo.compilador.listaCompletaOutroTipoDeProducaoBibliografica, "PB9")
        # Total de produção bibliográfica
        self.nPB = self.gerar_arquivo_de_producoes(self.grupo.compilador.listaCompletaPB,
                                                   "PB")

    def gerarArquivosDeProducoesTecnicas(self):
        self.nPT0 = 0
        self.nPT1 = 0
        self.nPT2 = 0
        self.nPT3 = 0
        self.nPT4 = 0
        self.nPT5 = 0
        self.nPT6 = 0
        self.nPT7 = 0
        self.nPT8 = 0
        self.nPT9 = 0
        self.nPT10 = 0
        self.nPT11 = 0
        self.nPT12 = 0
        self.nPT13 = 0
        self.nPT = 0

        if self.grupo.obterParametro('relatorio-incluir_software_com_patente'):
            self.nPT0 = self.gerar_arquivo_de_producoes(self.grupo.compilador.listaCompletaSoftwareComPatente,
                                                        "PT0")
        if self.grupo.obterParametro('relatorio-incluir_software_sem_patente'):
            self.nPT1 = self.gerar_arquivo_de_producoes(self.grupo.compilador.listaCompletaSoftwareSemPatente,
                                                        "PT1")
        if self.grupo.obterParametro('relatorio-incluir_produto_tecnologico'):
            self.nPT2 = self.gerar_arquivo_de_producoes(self.grupo.compilador.listaCompletaProdutoTecnologico,
                                                        "PT2")
        if self.grupo.obterParametro('relatorio-incluir_processo_ou_tecnica'):
            self.nPT3 = self.gerar_arquivo_de_producoes(self.grupo.compilador.listaCompletaProcessoOuTecnica,
                                                        "PT3")
        if self.grupo.obterParametro('relatorio-incluir_trabalho_tecnico'):
            self.nPT4 = self.gerar_arquivo_de_producoes(self.grupo.compilador.listaCompletaTrabalhoTecnico,
                                                        "PT4")
        if self.grupo.obterParametro('relatorio-incluir_outro_tipo_de_producao_tecnica'):
            self.nPT5 = self.gerar_arquivo_de_producoes(self.grupo.compilador.listaCompletaOutroTipoDeProducaoTecnica,
                                                        "PT5")
        if self.grupo.obterParametro('relatorio-incluir_apresentacao_de_trabalho'):
            self.nPT6 = self.gerar_arquivo_de_producoes(self.grupo.compilador.listaCompletaApresentacaoDeTrabalho,
                                                        "PT6")
        if self.grupo.obterParametro('relatorio-incluir_curso_de_curta_duracao_ministrado'):
            self.nPT7 = self.gerar_arquivo_de_producoes(
                self.grupo.compilador.listaCompletaCursoDeCurtaDuracaoMinistrado,
                "PT7")
        if self.grupo.obterParametro('relatorio-incluir_desenvolvimento_de_material_didatico_ou_instrucional'):
            self.nPT8 = self.gerar_arquivo_de_producoes(
                self.grupo.compilador.listaCompletaDesenvolvimentoDeMaterialDidaticoOuInstrucional,
                "PT8")
        if self.grupo.obterParametro('relatorio-incluir_organizacao_de_evento'):
            self.nPT9 = self.gerar_arquivo_de_producoes(self.grupo.compilador.listaCompletaOrganizacaoDeEvento,
                                                        "PT9")
        if self.grupo.obterParametro('relatorio-incluir_programa_de_radio_ou_tv'):
            self.nPT10 = self.gerar_arquivo_de_producoes(self.grupo.compilador.listaCompletaProgramaDeRadioOuTv,
                                                         "PT10")
        if self.grupo.obterParametro('relatorio-incluir_relatorio_de_pesquisa'):
            self.nPT11 = self.gerar_arquivo_de_producoes(self.grupo.compilador.listaCompletaRelatorioDePesquisa,
                                                         "PT11")
        if self.grupo.obterParametro('relatorio-incluir_carta-mapa-ou-similar'):
            self.nPT12 = self.gerar_arquivo_de_producoes(self.grupo.compilador.listaCompletaCartaMapaOuSimilar,
                                                         "PT12")
        if self.grupo.obterParametro('relatorio-incluir_patente'):
            self.nPT13 = self.gerar_arquivo_de_producoes(self.grupo.compilador.listaCompletaPatente,
                                                        "PT13")
        # Total de produções técnicas
        self.nPT = self.gerar_arquivo_de_producoes(self.grupo.compilador.listaCompletaPT, "PT")

    def gerarArquivossDeProducoesArtisticas(self):
        self.nPA0 = 0
        self.nPA = 0

        if self.grupo.obterParametro('relatorio-incluir_producao_artistica'):
            self.nPA0 = self.gerar_pagina_de_producoes(self.grupo.compilador.listaCompletaProducaoArtistica,
                                                       "Produção artística/cultural", "PA0")
        # Total de produções técnicas
        self.nPA = self.gerar_pagina_de_producoes(self.grupo.compilador.listaCompletaPA, "Total de produção artística",
                                                  "PA")

    def gerarPaginasDePatentes(self):
        self.nPR0 = 0
        self.nPR1 = 0
        self.nPR2 = 0
        self.nPR = 0

        if self.grupo.obterParametro('relatorio-incluir_patente'):
            self.nPR0 = self.gerar_pagina_de_producoes(self.grupo.compilador.listaCompletaPatente, "Patente", "PR0")
            self.nPR1 = self.gerar_pagina_de_producoes(self.grupo.compilador.listaCompletaProgramaComputador,
                                                       "Programa de computador", "PR1")
            self.nPR2 = self.gerar_pagina_de_producoes(self.grupo.compilador.listaCompletaDesenhoIndustrial,
                                                       "Desenho industrial", "PR2")

            # Total de produções técnicas

            self.nPR = self.gerar_pagina_de_producoes(self.grupo.compilador.listaCompletaPR,
                                                      "Total de patentes e registros", "PR")

    def gerarPaginasDeOrientacoes(self):
        self.nOA0 = 0
        self.nOA1 = 0
        self.nOA2 = 0
        self.nOA3 = 0
        self.nOA4 = 0
        self.nOA5 = 0
        self.nOA6 = 0
        self.nOA = 0

        if self.grupo.obterParametro('relatorio-incluir_orientacao_em_andamento_pos_doutorado'):
            self.nOA0 = self.gerar_pagina_de_producoes(self.grupo.compilador.listaCompletaOASupervisaoDePosDoutorado,
                                                       "Supervisão de pós-doutorado", "OA0")
        if self.grupo.obterParametro('relatorio-incluir_orientacao_em_andamento_doutorado'):
            self.nOA1 = self.gerar_pagina_de_producoes(self.grupo.compilador.listaCompletaOATeseDeDoutorado,
                                                       "Tese de doutorado", "OA1")
        if self.grupo.obterParametro('relatorio-incluir_orientacao_em_andamento_mestrado'):
            self.nOA2 = self.gerar_pagina_de_producoes(self.grupo.compilador.listaCompletaOADissertacaoDeMestrado,
                                                       "Dissertação de mestrado", "OA2")
        if self.grupo.obterParametro('relatorio-incluir_orientacao_em_andamento_monografia_de_especializacao'):
            self.nOA3 = self.gerar_pagina_de_producoes(self.grupo.compilador.listaCompletaOAMonografiaDeEspecializacao,
                                                       "Monografia de conclusão de curso de aperfeiçoamento/especialização",
                                                       "OA3")
        if self.grupo.obterParametro('relatorio-incluir_orientacao_em_andamento_tcc'):
            self.nOA4 = self.gerar_pagina_de_producoes(self.grupo.compilador.listaCompletaOATCC,
                                                       "Trabalho de conclusão de curso de graduação", "OA4")
        if self.grupo.obterParametro('relatorio-incluir_orientacao_em_andamento_iniciacao_cientifica'):
            self.nOA5 = self.gerar_pagina_de_producoes(self.grupo.compilador.listaCompletaOAIniciacaoCientifica,
                                                       "Iniciação científica", "OA5")
        if self.grupo.obterParametro('relatorio-incluir_orientacao_em_andamento_outro_tipo'):
            self.nOA6 = self.gerar_pagina_de_producoes(self.grupo.compilador.listaCompletaOAOutroTipoDeOrientacao,
                                                       "Orientações de outra natureza", "OA6")
        # Total de orientações em andamento
        self.nOA = self.gerar_pagina_de_producoes(self.grupo.compilador.listaCompletaOA,
                                                  "Total de orientações em andamento", "OA")

        self.nOC0 = 0
        self.nOC1 = 0
        self.nOC2 = 0
        self.nOC3 = 0
        self.nOC4 = 0
        self.nOC5 = 0
        self.nOC6 = 0
        self.nOC = 0

        if self.grupo.obterParametro('relatorio-incluir_orientacao_concluida_pos_doutorado'):
            self.nOC0 = self.gerar_pagina_de_producoes(self.grupo.compilador.listaCompletaOCSupervisaoDePosDoutorado,
                                                       "Supervisão de pós-doutorado", "OC0")
        if self.grupo.obterParametro('relatorio-incluir_orientacao_concluida_doutorado'):
            self.nOC1 = self.gerar_pagina_de_producoes(self.grupo.compilador.listaCompletaOCTeseDeDoutorado,
                                                       "Tese de doutorado", "OC1")
        if self.grupo.obterParametro('relatorio-incluir_orientacao_concluida_mestrado'):
            self.nOC2 = self.gerar_pagina_de_producoes(self.grupo.compilador.listaCompletaOCDissertacaoDeMestrado,
                                                       "Dissertação de mestrado", "OC2")
        if self.grupo.obterParametro('relatorio-incluir_orientacao_concluida_monografia_de_especializacao'):
            self.nOC3 = self.gerar_pagina_de_producoes(self.grupo.compilador.listaCompletaOCMonografiaDeEspecializacao,
                                                       "Monografia de conclusão de curso de aperfeiçoamento/especialização",
                                                       "OC3")
        if self.grupo.obterParametro('relatorio-incluir_orientacao_concluida_tcc'):
            self.nOC4 = self.gerar_pagina_de_producoes(self.grupo.compilador.listaCompletaOCTCC,
                                                       "Trabalho de conclusão de curso de graduação", "OC4")
        if self.grupo.obterParametro('relatorio-incluir_orientacao_concluida_iniciacao_cientifica'):
            self.nOC5 = self.gerar_pagina_de_producoes(self.grupo.compilador.listaCompletaOCIniciacaoCientifica,
                                                       "Iniciação científica", "OC5")
        if self.grupo.obterParametro('relatorio-incluir_orientacao_concluida_outro_tipo'):
            self.nOC6 = self.gerar_pagina_de_producoes(self.grupo.compilador.listaCompletaOCOutroTipoDeOrientacao,
                                                       "Orientações de outra natureza", "OC6")
        # Total de orientações concluídas
        self.nOC = self.gerar_pagina_de_producoes(self.grupo.compilador.listaCompletaOC,
                                                  "Total de orientações concluídas", "OC")

    def gerarPaginasDeProjetos(self):
        self.nPj = 0
        self.nPj = self.gerar_pagina_de_producoes(self.grupo.compilador.listaCompletaProjetoDePesquisa,
                                                  "Total de projetos de pesquisa", "Pj")

    def gerarPaginasDePremios(self):
        self.nPm = 0
        self.nPm = self.gerar_pagina_de_producoes(self.grupo.compilador.listaCompletaPremioOuTitulo,
                                                  "Total de prêmios e títulos", "Pm")

    def gerarPaginasDeParticipacaoEmEventos(self):
        self.nEp = 0
        self.nEp = self.gerar_pagina_de_producoes(self.grupo.compilador.listaCompletaParticipacaoEmEvento,
                                                  "Total de participação em eventos", "Ep")

    # def gerarPaginasDeOrganizacaoDeEventos(self):
    #    self.nEo = 0
    #    self.nEo = self.gerar_pagina_de_producoes(self.grupo.compilador.listaCompletaOrganizacaoDeEvento,
    #                                              "Total de organização de eventos", "Eo")

    def gerarPaginasDeInternacionalizacao(self):
        self.nIn0 = 0
        self.nIn0 = self.gerarPaginaDeInternacionalizacao(self.grupo.listaDePublicacoesEinternacionalizacao,
                                                          "Coautoria e internacionalização", "In0")

    @staticmethod
    def arranjar_publicacoes(listaCompleta):
        l = []
        for ano in sorted(listaCompleta.keys(), reverse=True):
            publicacoes = sorted(listaCompleta[ano], key=lambda x: x.chave.lower())
            for indice, publicacao in enumerate(publicacoes):
                l.append((ano, indice, publicacao))
        return l

    @staticmethod
    def chunks(lista, tamanho):
        ''' Retorna sucessivos chunks de 'tamanho' a partir da 'lista'
        '''
        for i in range(0, len(lista), tamanho):
            yield lista[i:i + tamanho]

    @staticmethod
    def template_pagina_de_producoes():
        st = u'''
                {top}
                {grafico}
                <h3>{titulo}</h3> <br>
                    <div id="container" style="min-width: 310px; max-width: 1920px; height: {height}; margin: 0"></div>
                    Número total de itens: {numero_itens}<br>
                    {totais_qualis}
                    {indice_paginas}
                    {producoes}
                    </table>
                {bottom}
              '''
        return st

    def  gerar_arquivo_de_producoes(self, lista_completa, prefixo):
        total_producoes = sum(len(v) for v in lista_completa.values())

        keys = sorted(lista_completa.keys(), reverse=True)

        if keys:  # apenas geramos páginas web para lista com pelo menos 1 elemento
            anos_indices_publicacoes = self.arranjar_publicacoes(lista_completa)

            producoes_csv = ''
            titulos = []

            for ano, indice_no_ano, publicacao in anos_indices_publicacoes:
                if producoes_csv == '':
                    producoes_csv = publicacao.colunas_csv() + '\n'

                existe = False
                for titulo in titulos:
                    if publicacao.titulo == titulo:
                        existe = True
                if not existe:
                    producoes_csv += publicacao.csv() + '\n'
                    titulos.append(publicacao.titulo)

            self.salvarArquivo(prefixo + '.csv', producoes_csv)
        return total_producoes

    def gerarIndiceDePaginas(self, numeroDePaginas, numeroDePaginaAtual, prefixo):
        if numeroDePaginas == 1:
            return ''
        else:
            s = 'Página: '.decode("utf8")
            for i in range(0, numeroDePaginas):
                if i == numeroDePaginaAtual:
                    s += '<b>' + str(i + 1) + '</b> &nbsp;'
                else:
                    s += '<a href="' + prefixo + '-' + str(i) + self.extensaoPagina + '">' + str(i + 1) + '</a> &nbsp;'
            return '<center>' + s + '</center>'

    def gerarPaginaDeInternacionalizacao(self, listaCompleta, tituloPagina, prefixo):
        numeroTotalDeProducoes = 0
        gInternacionalizacao = GraficoDeInternacionalizacao(listaCompleta)
        htmlCharts = gInternacionalizacao.criarGraficoDeBarrasDeOcorrencias()

        keys = listaCompleta.keys()
        keys.sort(reverse=True)
        if len(keys) > 0:  # apenas geramos páginas web para lista com pelo menos 1 elemento
            for ano in keys:
                numeroTotalDeProducoes += len(listaCompleta[ano])

            maxElementos = int(self.grupo.obterParametro('global-itens_por_pagina'))
            numeroDePaginas = int(math.ceil(
                numeroTotalDeProducoes / (maxElementos * 1.0)))  # dividimos os relatórios em grupos (e.g 1000 items)

            numeroDeItem = 1
            numeroDePaginaAtual = 0
            s = ''

            for ano in keys:
                anoRotulo = str(ano) if not ano == 0 else '*itens sem ano'

                s += '<h3 class="year">' + anoRotulo + '</h3> <table>'

                elementos = listaCompleta[ano]
                elementos.sort(
                    key=lambda x: x.chave.lower())  # Ordenamos a lista em forma ascendente (hard to explain!)

                for index in range(0, len(elementos)):
                    pub = elementos[index]
                    s += '<tr valign="top"><td>' + str(index + 1) + '. &nbsp;</td> <td>' + pub.html() + '</td></tr>'

                    if numeroDeItem % maxElementos == 0 or numeroDeItem == numeroTotalDeProducoes:
                        st = self.pagina_top(cabecalho=htmlCharts)
                        st += '\n<h3>' + tituloPagina.decode(
                            "utf8") + '</h3> <br> <center> <table> <tr> <td valign="top"><div id="barchart_div"></div> </td> <td valign="top"><div id="geochart_div"></div> </td> </tr> </table> </center>'
                        st += '<table>'
                        st += '<tr><td>Número total de publicações realizadas SEM parceria com estrangeiros:</td><td>'.decode(
                            "utf8") + str(
                            gInternacionalizacao.numeroDePublicacoesRealizadasSemParceirasComEstrangeiros()) + '</td><td><i>(publicações realizadas só por pesquisadores brasileiros)</i></td></tr>'.decode(
                            "utf8")
                        st += '<tr><td>Número total de publicações realizadas COM parceria com estrangeiros:</td><td>'.decode(
                            "utf8") + str(
                            gInternacionalizacao.numeroDePublicacoesRealizadasComParceirasComEstrangeiros()) + '</td><td></td></tr>'
                        st += '<tr><td>Número total de publicações com parcerias NÂO identificadas:</td><td>'.decode(
                            "utf8") + str(
                            gInternacionalizacao.numeroDePublicacoesComParceriasNaoIdentificadas()) + '</td><td></td></tr>'
                        st += '<tr><td>Número total de publicações com DOI cadastrado:</td><td><b>'.decode(
                            "utf8") + str(numeroTotalDeProducoes) + '</b></td><td></td></tr>'
                        st += '</table>'
                        st += '<br> <font color="red">(*) A estimativa de "coautoria e internacionalização" é baseada na análise automática dos DOIs das publicações cadastradas nos CVs Lattes. A identificação de países, para cada publicação, é feita através de buscas simples de nomes de países.</font><br><p>'.decode(
                            "utf8")

                        st += self.gerarIndiceDePaginas(numeroDePaginas, numeroDePaginaAtual, prefixo)
                        st += s  # .decode("utf8")
                        st += '</table>'
                        st += self.paginaBottom()

                        self.salvarPagina(prefixo + '-' + str(numeroDePaginaAtual) + self.extensaoPagina, st)
                        numeroDePaginaAtual += 1

                        if (index + 1) < len(elementos):
                            s = '<h3 class="year">' + anoRotulo + '</h3> <table>'
                        else:
                            s = ''
                    numeroDeItem += 1

                s += '</table>'
        return numeroTotalDeProducoes

    def gerarPaginaDeGrafosDeColaboracoes(self):
        '''
        lista = ''
        if self.grupo.obterParametro('grafo-incluir_artigo_em_periodico'):
            lista += 'Artigos completos publicados em periódicos, '.decode("utf8")
        if self.grupo.obterParametro('grafo-incluir_livro_publicado'):
            lista += 'Livros publicados/organizados ou edições, '.decode("utf8")
        if self.grupo.obterParametro('grafo-incluir_capitulo_de_livro_publicado'):
            lista += 'Capítulos de livros publicados, '.decode("utf8")
        if self.grupo.obterParametro('grafo-incluir_texto_em_jornal_de_noticia'):
            lista += 'Textos em jornais de notícias/revistas, '.decode("utf8")
        if self.grupo.obterParametro('grafo-incluir_trabalho_completo_em_congresso'):
            lista += 'Trabalhos completos publicados em anais de congressos, '.decode("utf8")
        if self.grupo.obterParametro('grafo-incluir_resumo_expandido_em_congresso'):
            lista += 'Resumos expandidos publicados em anais de congressos, '.decode("utf8")
        if self.grupo.obterParametro('grafo-incluir_resumo_em_congresso'):
            lista += 'Resumos publicados em anais de congressos, '.decode("utf8")
        if self.grupo.obterParametro('grafo-incluir_artigo_aceito_para_publicacao'):
            lista += 'Artigos aceitos para publicação, '.decode("utf8")
        if self.grupo.obterParametro('grafo-incluir_apresentacao_de_trabalho'):
            lista += 'Apresentações de trabalho, '.decode("utf8")
        if self.grupo.obterParametro('grafo-incluir_outro_tipo_de_producao_bibliografica'):
            lista += 'Demais tipos de produção bibliográfica, '.decode("utf8")

        lista = lista.strip().strip(",")

        s = self.pagina_top()
        s += '\n<h3>Grafo de colabora&ccedil;&otilde;es</h3> \
        <a href=membros' + self.extensaoPagina + '>' + str(self.grupo.numeroDeMembros()) + ' curriculos Lattes</a> foram considerados, \
        gerando os seguintes grafos de colabora&ccedil;&otilde;es encontradas com base nas produ&ccedil;&otilde;es: <i>' + lista + '</i>. <br><p>'.decode(
            "utf8")

        prefix = self.grupo.obterParametro('global-prefixo') + '-' if not self.grupo.obterParametro(
            'global-prefixo') == '' else ''
        # s+='Veja <a href="grafoDeColaboracoesInterativo'+self.extensaoPagina+'?entradaScriptLattes=./'+prefix+'matrizDeAdjacencia.xml">na seguinte página</a> uma versão interativa do grafo de colabora&ccedil;&otilde;es.<br><p><br><p>'.decode("utf8")

        s += '\nClique no nome dentro do vértice para visualizar o currículo Lattes. Para cada nó: o valor entre colchetes indica o número \
        de produ&ccedil;&otilde;es feitas em colabora&ccedil;&atilde;o apenas com os outros membros do próprio grupo. <br>'.decode(
            "utf8")

        if self.grupo.obterParametro('grafo-considerar_rotulos_dos_membros_do_grupo'):
            s += 'As cores representam os seguintes rótulos: '.decode("utf8")
            for i in range(0, len(self.grupo.listaDeRotulos)):
                rot = self.grupo.listaDeRotulos[i].decode("utf8", "ignore")
                cor = self.grupo.listaDeRotulosCores[i].decode("utf8")
                if rot == '':
                    rot = '[Sem rótulo]'.decode("utf8")
                s += '<span style="background-color:' + cor + '">&nbsp;&nbsp;&nbsp;&nbsp;</span>' + rot + ' '
        s += '\
        <ul> \
        <li><b>Grafo de colabora&ccedil;&otilde;es sem pesos</b><br> \
            <img src=grafoDeColaboracoesSemPesos.png border=1 ISMAP USEMAP="#grafo1"> <br><p> \
        <li><b>Grafo de colabora&ccedil;&otilde;es com pesos</b><br> \
            <img src=grafoDeColaboracoesComPesos.png border=1 ISMAP USEMAP="#grafo2"> <br><p> \
        </ul>'.decode("utf8")

        cmapx1 = self.grupo.grafosDeColaboracoes.grafoDeCoAutoriaSemPesosCMAPX
        cmapx2 = self.grupo.grafosDeColaboracoes.grafoDeCoAutoriaComPesosCMAPX
        s += '<map id="grafo1" name="grafo1">' + cmapx1.decode("utf8") + '\n</map>\n'
        s += '<map id="grafo2" name="grafo2">' + cmapx2.decode("utf8") + '\n</map>\n'

        if self.grupo.obterParametro('grafo-incluir_grau_de_colaboracao'):
            s += '<br><p><h3>Grau de colaboração</h3> \
                O grau de colaboração (<i>Collaboration Rank</i>) é um valor numérico que indica o impacto de um membro no grafo de colaborações.\
                <br>Esta medida é similar ao <i>PageRank</i> para grafos direcionais (com pesos).<br><p>'.decode("utf8")

            ranks, autores, rotulos = zip(
                *sorted(zip(self.grupo.vectorRank, self.grupo.nomes, self.grupo.rotulos), reverse=True))

            s += '<table border=1><tr> <td><i><b>Collaboration Rank</b></i></td> <td><b>Membro</b></td> </tr>'
            for i in range(0, len(ranks)):
                s += '<tr><td>' + str(round(ranks[i], 2)) + '</td><td>' + autores[i] + '</td></tr>'
            s += '</table> <br><p>'

            if self.grupo.obterParametro('grafo-considerar_rotulos_dos_membros_do_grupo'):
                for i in range(0, len(self.grupo.listaDeRotulos)):
                    somaAuthorRank = 0

                    rot = self.grupo.listaDeRotulos[i].decode("utf8", "ignore")
                    cor = self.grupo.listaDeRotulosCores[i].decode("utf8")
                    s += '<b><span style="background-color:' + cor + '">&nbsp;&nbsp;&nbsp;&nbsp;</span>' + rot + '</b><br>'

                    s += '<table border=1><tr> <td><i><b>AuthorRank</b></i></td> <td><b>Membro</b></td> </tr>'
                    for i in range(0, len(ranks)):
                        if rotulos[i] == rot:
                            s += '<tr><td>' + str(round(ranks[i], 2)) + '</td><td>' + autores[i] + '</td></tr>'
                            somaAuthorRank += ranks[i]
                    s += '</table> <br> Total: ' + str(round(somaAuthorRank, 2)) + '<br><p>'

        s += self.paginaBottom()
        self.salvarPagina("grafoDeColaboracoes" + self.extensaoPagina, s)

        # grafo interativo
        s = self.pagina_top()
        s += '<applet code=MyGraph.class width=1280 height=800 archive="http://www.vision.ime.usp.br/creativision/graphview/graphview.jar,http://www.vision.ime.usp.br/creativision/graphview/prefuse.jar"></applet></body></html>'
        s += self.paginaBottom()
        self.salvarPagina("grafoDeColaboracoesInterativo" + self.extensaoPagina, s)
        '''

    @staticmethod
    def producao_qualis(elemento, membro):
        tabela_template = u"<table style=\"width: 100%; display: block; overflow-x: auto;\"><tbody>" \
                          u"<br><span style=\"font-size:14px;\"><b>Totais de publicações com Qualis:</b></span><br><br>" \
                          u"<div style=\"width:100%; overflow-x:scroll;\">{body}</div>" \
                          u"</tbody></table>"

        first_column_template = u'<div style="float:left; width:200px; height: auto; border: 1px solid black; border-collapse: collapse; margin-left:0px; margin-top:0px;' \
                                ' background:#CCC; vertical-align: middle; padding: 4px 0; {extra_style}"><b>{header}</b></div>'
        header_template = u'<div style="float:left; width:{width}px; height: auto; border-style: solid; border-color: black; border-width: 1 1 1 0; border-collapse: collapse; margin-left:0px; margin-top:0px;' \
                          ' background:#CCC; text-align: center; vertical-align: middle; padding: 4px 0;"><b>{header}</b></div>'
        line_template = u'<div style="float:left; width:{width}px; height: auto; border-style: solid; border-color: black; border-width: 1 1 1 0; border-collapse: collapse; margin-left:0px; margin-top:0px;' \
                        ' background:#EAEAEA; text-align: center; vertical-align: middle; padding: 4px 0;">{value}</div>'  # padding:4px 6px;

        cell_size = 40
        num_estratos = len(membro.tabela_qualis['estrato'].unique())

        header_ano = first_column_template.format(header='Ano', extra_style='text-align: center;')
        header_estrato = first_column_template.format(header=u'Área \\ Estrato', extra_style='text-align: center;')

        for ano in sorted(membro.tabela_qualis['ano'].unique()):
            header_ano += header_template.format(header=ano, width=num_estratos * (cell_size + 1) - 1)
            for estrato in sorted(membro.tabela_qualis['estrato'].unique()):
                header_estrato += header_template.format(header=estrato, width=cell_size)

        if membro.tabela_qualis and not membro.tabela_qualis.empty():
            pt = membro.tabela_qualis.pivot_table(columns=['area', 'ano', 'estrato'], values='freq')
        lines = ''
        for area in sorted(membro.tabela_qualis['area'].unique()):
            lines += first_column_template.format(header=area, extra_style='')
            for ano in sorted(membro.tabela_qualis['ano'].unique()):
                for estrato in sorted(membro.tabela_qualis['estrato'].unique()):
                    try:
                        lines += line_template.format(value=pt.ix[area, ano, estrato], width=cell_size)
                    except IndexingError:
                        lines += line_template.format(value='&nbsp;', width=cell_size)
            lines += '<div style="clear:both"></div>'

        tabela_body = header_ano
        tabela_body += '<div style="clear:both"></div>'
        tabela_body += header_estrato
        tabela_body += '<div style="clear:both"></div>'
        tabela_body += lines

        tabela = tabela_template.format(body=tabela_body)

        # first = True
        # # FIXME: considerar as áreas
        # for ano in sorted(membro.tabela_qualis['ano'].unique()):
        #     if first:
        #         first = False
        #         display = "block"
        #     else:
        #         display = "none"
        #
        #     # esquerda = '<a class="ano_esquerda" rel="{ano}" rev="{rev}" style="cursor:pointer; padding:2px; border:1px solid #C3FDB8;">«</a>'.format(
        #     #     ano=ano, rev=str(elemento))
        #     # direita = '<a class="ano_direita" rel="{ano}" rev="{rev}" style="cursor:pointer; padding:2px; border:1px solid #C3FDB8;">«</a>'.format(
        #     #     ano=ano, rev=str(elemento))
        #     # tabela += '<div id="ano_{ano}_{elemento}" style="display: {display}">{esquerda}<b>{ano}</b>{direita}<br/><br/>'.format(
        #     #           ano=ano, elemento=elemento, display=display, esquerda=esquerda, direita=direita)
        #     chaves = ''
        #     valores = ''
        #
        #     for tipo, frequencia in membro.tabelaQualisDosAnos[ano].items():
        #         # FIXME: terminar de refatorar
        #         if tipo == "Qualis nao identificado":
        #             tipo = '<span title="Qualis nao identificado">QNI</span>'
        #
        #         chaves += '<div style="float:left; width:70px; border:1px solid #000; margin-left:-1px; margin-top:-1px; background:#CCC; padding:4px 6px;"><b>' + str(
        #             tipo) + '</b></div>'
        #         valores += '<div style="float:left; width:70px; border:1px solid #000; margin-left:-1px; margin-top:-1px; background:#EAEAEA; padding:4px 6px;">' + str(
        #             frequencia) + '</div>'
        #
        #     tabela += '<div>' + chaves + '</div>'
        #     tabela += '<div style="clear:both"></div>'
        #     tabela += '<div>' + valores + '</div>'
        #     tabela += '<div style="clear:both"></div>'
        #     tabela += "<br><br></div>"
        # tabTipo += '<div>'
        # chaves = ''
        # valores = ''
        # for chave, valor in membro.tabelaQualisDosTipos.items():
        #
        #     if (chave == "Qualis nao identificado"):
        #         chave = "QNI"
        #
        #     chaves += '<div style="float:left; width:70px; border:1px solid #000; margin-left:-1px; margin-top:-1px; background:#CCC; padding:4px 6px;"><b>' + str(
        #         chave) + '</b></div>'
        #     valores += '<div style="float:left; width:70px; border:1px solid #000; margin-left:-1px; margin-top:-1px; background:#EAEAEA; padding:4px 6px;">' + str(
        #         valor) + '</div>'
        # tabTipo += '<div>' + chaves + '</div>'
        # tabTipo += '<div style="clear:both"></div>'
        # tabTipo += '<div>' + valores + '</div>'
        # tabTipo += '<div style="clear:both"></div>'
        # tabTipo += "<br><br></div><br><br>"
        return tabela

    def gerar_pagina_de_metricas(self):
        s = self.pagina_top()

        s += u'\n<h3>Métricas: Produções bibliográficas, técnicas e artísticas</h3> <table id="metricas" class="sortable" border=1><tr>\
                <th></th>\
                <th></th>\
                <th><b><font size=-1>Rótulo/Grupo</font></b></th>\
                <th><b><font size=-1>Bolsa CNPq</font></b></th>\
                <th><b><font size=-1>Período de<br>análise individual</font></b></th>\
                <th><b><font size=-1>Data de<br>atualização do CV</font><b></th>\
                <th><b><font size=-1>Grande área</font><b></th>\
                <th><b><font size=-1>Área</font><b></th>\
                <th><b><font size=-1>lat</font><b></th>\
                <th><b><font size=-1>lon</font><b></th>\
        <th><b><font size=-1>Produção<br>bibliográfica</font><b></th>\
        <th><b><font size=-1>Periódicos</font><b></th>\
        <th><b><font size=-1>Livros</font><b></th>\
        <th><b><font size=-1>Capítulos</font><b></th>\
        <th><b><font size=-1>Congressos</font><b></th>\
        <th><b><font size=-1>Resumos</font><b></th>\
        <th><b><font size=-1>Aceitos</font><b></th>\
        <th><b><font size=-1>Produção<br>técnica</font><b></th>\
        <th><b><font size=-1>Produção<br>artística</font><b></th>\
        </tr>'

        elemento = 0
        for membro in self.grupo.listaDeMembros:
            elemento += 1
            bolsa = membro.bolsaProdutividade if membro.bolsaProdutividade else ''
            rotulo = membro.rotulo if not membro.rotulo == '[Sem rotulo]' else ''
            rotulo = rotulo.decode('iso-8859-1', 'replace')
            nomeCompleto = unicodedata.normalize('NFKD', membro.nomeCompleto).encode('ASCII', 'ignore')

            quantitativo_publicacoes = [len(membro.listaArtigoEmPeriodico),
                                        len(membro.listaLivroPublicado),
                                        len(membro.listaCapituloDeLivroPublicado),
                                        len(membro.listaTrabalhoCompletoEmCongresso),
                                        len(membro.listaResumoEmCongresso) + len(
                                            membro.listaResumoExpandidoEmCongresso),
                                        len(membro.listaArtigoAceito)]

            quantitativo_tecnica = [len(membro.listaSoftwareComPatente),
                                    len(membro.listaSoftwareSemPatente),
                                    len(membro.listaSoftwareSemPatente),
                                    len(membro.listaProdutoTecnologico),
                                    len(membro.listaProcessoOuTecnica),
                                    len(membro.listaTrabalhoTecnico),
                                    len(membro.listaOutroTipoDeProducaoTecnica),
                                    len(membro.listaCursoDeCurtaDuracaoMinistrado),
                                    len(membro.listaDesenvolvimentoDeMaterialDidaticoOuInstrucional),
                                    len(membro.listaOrganizacaoDeEvento),
                                    len(membro.listaProgramaDeRadioOuTv),
                                    len(membro.listaRelatorioDePesquisa),
                                    len(membro.listaCartaMapaOuSimilar)]

            quantitativo_artistica = [len(membro.listaProducaoArtistica)]

            s += u'\n<tr class="testetabela"> \
                     <td valign="center">{0}.</td> \
                     <td><a href="membro-{1}.html"> {2}</a></td> \
                     <td><font size=-2>{3}</font></td> \
                     <td><font size=-2>{4}</font></td> \
                     <td><font size=-2>{5}</font></td> \
                     <td><font size=-2>{6}</font></td> \
                     <td><font size=-2>{7}</font></td> \
                     <td><font size=-2>{8}</font></td> \
                     <td><font size=-2>{9}</font></td> \
                     <td><font size=-2>{10}</font></td> \
                     <td align="right"><font size=-2>{11}</font></td> \
                     <td align="right"><font size=-2>{12}</font></td> \
                     <td align="right"><font size=-2>{13}</font></td> \
                     <td align="right"><font size=-2>{14}</font></td> \
                     <td align="right"><font size=-2>{15}</font></td> \
                     <td align="right"><font size=-2>{16}</font></td> \
                     <td align="right"><font size=-2>{17}</font></td> \
                     <td align="right"><font size=-2>{18}</font></td> \
                     <td align="right"><font size=-2>{19}</font></td> \
                     </tr>'.format(str(elemento),
                                   membro.idLattes,
                                   nomeCompleto,
                                   rotulo,
                                   bolsa,
                                   membro.periodo,
                                   membro.atualizacaoCV,
                                   membro.nomePrimeiraGrandeArea,
                                   membro.nomePrimeiraArea,
                                   membro.enderecoProfissionalLat,
                                   membro.enderecoProfissionalLon,
                                   sum(quantitativo_publicacoes),
                                   quantitativo_publicacoes[0],
                                   quantitativo_publicacoes[1],
                                   quantitativo_publicacoes[2],
                                   quantitativo_publicacoes[3],
                                   quantitativo_publicacoes[4],
                                   quantitativo_publicacoes[5],
                                   sum(quantitativo_tecnica),
                                   sum(quantitativo_artistica))

        s += '\n</table>'

        s += u'\n<h3>Métricas: Orientações concluídas e em andamento</h3> <table id="metricas" class="sortable" border=1><tr>\
                        <th></th>\
                        <th></th>\
                        <th><b><font size=-1>Rótulo/Grupo</font></b></th>\
                        <th><b><font size=-1>Bolsa CNPq</font></b></th>\
                        <th><b><font size=-1>Período de<br>análise individual</font></b></th>\
                        <th><b><font size=-1>Data de<br>atualização do CV</font><b></th>\
                        <th><b><font size=-1>Grande área</font><b></th>\
                        <th><b><font size=-1>Área</font><b></th>\
        <th><b><font size=-1>Orientações<br>concluídas</font><b></th>\
        <th><b><font size=-1>Posdoc</font><b></th>\
        <th><b><font size=-1>Doutorado</font><b></th>\
        <th><b><font size=-1>Mestrado</font><b></th>\
        <th><b><font size=-1>Especialização</font><b></th>\
        <th><b><font size=-1>TCC</font><b></th>\
        <th><b><font size=-1>IC</font><b></th>\
        <th><b><font size=-1>Orientações<br>em andamento</font><b></th>\
        <th><b><font size=-1>Posdoc</font><b></th>\
        <th><b><font size=-1>Doutorado</font><b></th>\
        <th><b><font size=-1>Mestrado</font><b></th>\
        <th><b><font size=-1>Especialização</font><b></th>\
        <th><b><font size=-1>TCC</font><b></th>\
        <th><b><font size=-1>IC</font><b></th>\
        </tr>'

        elemento = 0
        for membro in self.grupo.listaDeMembros:
            elemento += 1
            bolsa = membro.bolsaProdutividade if membro.bolsaProdutividade else ''
            rotulo = membro.rotulo if not membro.rotulo == '[Sem rotulo]' else ''
            rotulo = rotulo.decode('iso-8859-1', 'replace')
            nomeCompleto = unicodedata.normalize('NFKD', membro.nomeCompleto).encode('ASCII', 'ignore')

            quantitativo_orientacoes_concluidas = [len(membro.listaOCSupervisaoDePosDoutorado),
                                                   len(membro.listaOCTeseDeDoutorado),
                                                   len(membro.listaOCDissertacaoDeMestrado),
                                                   len(membro.listaOCMonografiaDeEspecializacao),
                                                   len(membro.listaOCTCC),
                                                   len(membro.listaOCIniciacaoCientifica)]

            quantitativo_orientacoes_andamento = [len(membro.listaOASupervisaoDePosDoutorado),
                                                  len(membro.listaOATeseDeDoutorado),
                                                  len(membro.listaOADissertacaoDeMestrado),
                                                  len(membro.listaOAMonografiaDeEspecializacao),
                                                  len(membro.listaOATCC),
                                                  len(membro.listaOAIniciacaoCientifica)]

            s += u'\n<tr class="testetabela"> \
                      <td valign="center">{0}.</td> \
                      <td><a href="membro-{1}.html"> {2}</a></td> \
                      <td><font size=-2>{3}</font></td> \
                      <td><font size=-2>{4}</font></td> \
                      <td><font size=-2>{5}</font></td> \
                      <td><font size=-2>{6}</font></td> \
                      <td><font size=-2>{7}</font></td> \
                      <td><font size=-2>{8}</font></td> \
                      <td><font size=-2>{9}</font></td> \
                      <td><font size=-2>{10}</font></td> \
                      <td align="right"><font size=-2>{11}</font></td> \
                      <td align="right"><font size=-2>{12}</font></td> \
                      <td align="right"><font size=-2>{13}</font></td> \
                      <td align="right"><font size=-2>{14}</font></td> \
                      <td align="right"><font size=-2>{15}</font></td> \
                      <td align="right"><font size=-2>{16}</font></td> \
                      <td align="right"><font size=-2>{17}</font></td> \
                      <td align="right"><font size=-2>{18}</font></td> \
                      <td align="right"><font size=-2>{19}</font></td> \
                      <td align="right"><font size=-2>{20}</font></td> \
                      <td align="right"><font size=-2>{21}</font></td> \
                      <td align="right"><font size=-2>{22}</font></td> \
                      </tr>'.format(str(elemento),
                                    membro.idLattes,
                                    nomeCompleto,
                                    rotulo,
                                    bolsa,
                                    membro.periodo,
                                    membro.atualizacaoCV,
                                    membro.nomePrimeiraGrandeArea,
                                    membro.nomePrimeiraArea,
                                    sum(quantitativo_orientacoes_concluidas),
                                    quantitativo_orientacoes_concluidas[0],
                                    quantitativo_orientacoes_concluidas[1],
                                    quantitativo_orientacoes_concluidas[2],
                                    quantitativo_orientacoes_concluidas[3],
                                    quantitativo_orientacoes_concluidas[4],
                                    quantitativo_orientacoes_concluidas[5],
                                    sum(quantitativo_orientacoes_andamento),
                                    quantitativo_orientacoes_andamento[0],
                                    quantitativo_orientacoes_andamento[1],
                                    quantitativo_orientacoes_andamento[2],
                                    quantitativo_orientacoes_andamento[3],
                                    quantitativo_orientacoes_andamento[4],
                                    quantitativo_orientacoes_andamento[5],
                                    )

        s += '\n</table>'

        s += u'\n<h3>Métricas: Projetos, prêmios e eventos</h3> <table id="metricas" class="sortable" border=1><tr>\
                        <th></th>\
                        <th></th>\
                        <th><b><font size=-1>Rótulo/Grupo</font></b></th>\
                        <th><b><font size=-1>Bolsa CNPq</font></b></th>\
                        <th><b><font size=-1>Período de<br>análise individual</font></b></th>\
                        <th><b><font size=-1>Data de<br>atualização do CV</font><b></th>\
                        <th><b><font size=-1>Grande área</font><b></th>\
                        <th><b><font size=-1>Área</font><b></th>\
        <th><b><font size=-1>Projetos</font><b></th>\
        <th><b><font size=-1>Prêmios</font><b></th>\
        <th><b><font size=-1>Participação em eventos</font><b></th>\
        <th><b><font size=-1>Organização de eventos</font><b></th>\
        </tr>'

        elemento = 0
        for membro in self.grupo.listaDeMembros:
            elemento += 1
            bolsa = membro.bolsaProdutividade if membro.bolsaProdutividade else ''
            rotulo = membro.rotulo if not membro.rotulo == '[Sem rotulo]' else ''
            rotulo = rotulo.decode('iso-8859-1', 'replace')
            nomeCompleto = unicodedata.normalize('NFKD', membro.nomeCompleto).encode('ASCII', 'ignore')

            s += u'\n<tr class="testetabela"> \
                      <td valign="center">{0}.</td> \
                      <td><a href="membro-{1}.html"> {2}</a></td> \
                      <td><font size=-2>{3}</font></td> \
                      <td><font size=-2>{4}</font></td> \
                      <td><font size=-2>{5}</font></td> \
                      <td><font size=-2>{6}</font></td> \
                      <td><font size=-2>{7}</font></td> \
                      <td><font size=-2>{8}</font></td> \
                      <td><font size=-2>{9}</font></td> \
                      <td><font size=-2>{10}</font></td> \
                      <td align="right"><font size=-2>{11}</font></td> \
                      <td align="right"><font size=-2>{12}</font></td> \
                      </tr>'.format(str(elemento),
                                    membro.idLattes,
                                    nomeCompleto,
                                    rotulo,
                                    bolsa,
                                    membro.periodo,
                                    membro.atualizacaoCV,
                                    membro.nomePrimeiraGrandeArea,
                                    membro.nomePrimeiraArea,
                                    len(membro.listaProjetoDePesquisa),
                                    len(membro.listaPremioOuTitulo),
                                    len(membro.listaParticipacaoEmEvento),
                                    len(membro.listaOrganizacaoDeEvento)
                                    )

        s += '\n</table>'

        if self.grupo.obterParametro('grafo-mostrar_grafo_de_colaboracoes'):
            s += u'\n<h3>Métricas: Coautoria</h3> <table id="metricas" class="sortable" border=1><tr>\
                            <th></th>\
                            <th></th>\
                            <th><b><font size=-1>Rótulo/Grupo</font></b></th>\
                            <th><b><font size=-1>Bolsa CNPq</font></b></th>\
                            <th><b><font size=-1>Período de<br>análise individual</font></b></th>\
                            <th><b><font size=-1>Data de<br>atualização do CV</font><b></th>\
                            <th><b><font size=-1>Grande área</font><b></th>\
                            <th><b><font size=-1>Área</font><b></th>\
            <th><b><font size=-1>IDs Lattes identificados</font><b></th>\
            <th><b><font size=-1>Número de coautores - endôgeno</font><b></th>\
            <th><b><font size=-1>Número de coautores - Publicações bibliográficas</font><b></th>\
            </tr>'

            elemento = 0
            for membro in self.grupo.listaDeMembros:
                elemento += 1
                bolsa = membro.bolsaProdutividade if membro.bolsaProdutividade else ''
                rotulo = membro.rotulo if not membro.rotulo == '[Sem rotulo]' else ''
                rotulo = rotulo.decode('iso-8859-1', 'replace')
                nomeCompleto = unicodedata.normalize('NFKD', membro.nomeCompleto).encode('ASCII', 'ignore')

                coautores_do_membro = list([])
                alias_do_membro = membro.nomeEmCitacoesBibliograficas.upper().replace(".", "").split(";")
                for i in range(0, len(alias_do_membro)):
                    alias_do_membro[i] = alias_do_membro[i].strip()

                for tipo_de_publicacao in [membro.listaArtigoEmPeriodico,
                                           membro.listaLivroPublicado,
                                           membro.listaCapituloDeLivroPublicado,
                                           membro.listaTrabalhoCompletoEmCongresso,
                                           membro.listaResumoEmCongresso,
                                           membro.listaResumoExpandidoEmCongresso,
                                           membro.listaArtigoAceito]:
                    for pub in tipo_de_publicacao:

                        for coautor in pub.autores.upper().replace(".", "").split(";"):
                            coautor = coautor.strip()
                            if not coautor in alias_do_membro:
                                coautores_do_membro.append(coautor)

                    '''quantitativo_tecnica = [len(membro.listaSoftwareComPatente),
                                            len(membro.listaSoftwareSemPatente),
                                            len(membro.listaProdutoTecnologico),
                                            len(membro.listaProcessoOuTecnica),
                                            len(membro.listaTrabalhoTecnico),
                                            len(membro.listaOutroTipoDeProducaoTecnica)]

                    quantitativo_artistica = [len(membro.listaProducaoArtistica)]
                    '''

                s += u'\n<tr class="testetabela"> \
                          <td valign="center">{0}.</td> \
                          <td><a href="membro-{1}.html"> {2}</a></td> \
                          <td><font size=-2>{3}</font></td> \
                          <td><font size=-2>{4}</font></td> \
                          <td><font size=-2>{5}</font></td> \
                          <td><font size=-2>{6}</font></td> \
                          <td><font size=-2>{7}</font></td> \
                          <td><font size=-2>{8}</font></td> \
                          <td><font size=-2>{9}</font></td> \
                          <td><font size=-2>{10}</font></td> \
                          <td align="right"><font size=-2>{11}</font></td> \
                          </tr>'.format(str(elemento),
                                        membro.idLattes,
                                        nomeCompleto,
                                        rotulo,
                                        bolsa,
                                        membro.periodo,
                                        membro.atualizacaoCV,
                                        membro.nomePrimeiraGrandeArea,
                                        membro.nomePrimeiraArea,
                                        len(membro.listaIDLattesColaboradoresUnica),
                                        len(self.grupo.colaboradores_endogenos[membro.idMembro]),
                                        len(set(coautores_do_membro))
                                        )

            s += '\n</table>'

        # add jquery and plugins
        # s += '<script src="../../js/jexpand/jExpand.js"></script>' \
        #      '<script>' \
        #      '  $(document).ready(function(){' \
        #      '    $(".collapse-box").jExpand();' \
        #      '  });' \
        #      '</script>'

        s += '<script>' \
             '  $(document).ready( function () {' \
             '    $(\'#membros\').DataTable();' \
             '  });' \
             '</script>'

        # $(".ano_esquerda").live("click", function(e){\
        #     var anoAtual = parseInt($(this).attr("rel"));\
        #     var contador = $(this).attr("rev");\
        #     if(anoAtual > ' + str(anoInicio) + '){\
        #         $("#ano_"+anoAtual+"_"+contador).css("display", "none");\
        #         $("#ano_"+(anoAtual-1)+"_"+contador).css("display", "block");\
        #     }\
        # });\
        # $(".ano_direita").live("click", function(e){\
        #     var anoAtual = parseInt($(this).attr("rel"));\
        #     var contador = $(this).attr("rev");\
        #     if(anoAtual < ' + str(anoFim) + '){\
        #         $("#ano_"+anoAtual+"_"+contador).css("display", "none");\
        #         $("#ano_"+(anoAtual+1)+"_"+contador).css("display", "block");\
        #     }\
        # });\

        s += self.paginaBottom()

        self.salvarPagina("metricas" + self.extensaoPagina, s)

    def gerar_lista_de_producoes_de_membro(self, lista, titulo):
        s = '<ol>'
        for publicacao in lista:
            s += '<li>' + publicacao.html(self.grupo.listaDeMembros)
        s += '</ol><br>'
        return (len(lista), s, titulo)

    def gerar_lista_de_colaboracoes(self, membro, titulo):
        s = '<ol>'
        detalhe = '<ul>'

        colaboradores = self.grupo.colaboradores_endogenos[membro.idMembro]

        print('------------------- ok')

        for (idColaborador, quantidade) in sorted(colaboradores, key=lambda x: (-x[1], x[0])):
            colaborador = self.grupo.listaDeMembros[idColaborador]
            s += u'<li><a href="#{0}">{1}</a> ({2})'.format(colaborador.idLattes, colaborador.nomeCompleto, quantidade)
            detalhe += u'<li id="{0}"> <b>{3} &hArr; <a href="membro-{0}{4}">{1}</a></b> ({2}) <ol>'.format(
                colaborador.idLattes, colaborador.nomeCompleto, quantidade, membro.nomeCompleto, self.extensaoPagina)

            for publicacao in self.grupo.listaDeColaboracoes[membro.idMembro][idColaborador]:
                detalhe += '<li>' + publicacao.html(self.grupo.listaDeMembros)

            detalhe += u'</ol><br>'
        s += '</ol><br>'

        detalhe += '</ul><br>'
        return (len(colaboradores), s, titulo, detalhe)

    @staticmethod
    def producao_qualis_por_membro(lista_de_membros):
        # FIXME: ver um local melhor para este método

        producao_por_membro = pandas.DataFrame(columns=list(membro.Membro.tabela_qualis.columns) + ['membro'])

        for m in lista_de_membros:
            nome_membro = unicodedata.normalize('NFKD', m.nomeCompleto).encode('ASCII', 'ignore')
            df = pandas.DataFrame({'membro': [nome_membro] * len(m.tabela_qualis)}, index=m.tabela_qualis.index)
            producao_por_membro = producao_por_membro.append(m.tabela_qualis.join(df), ignore_index=True)

        if producao_por_membro.empty:
            producao_por_membro_pivo = pandas.DataFrame()
        else:
            producao_por_membro_pivo = producao_por_membro.pivot_table(values='freq',
                                                                       columns=['ano', 'estrato'],
                                                                       index=['area', 'membro'],
                                                                       dropna=True, fill_value=0, margins=False,
                                                                       aggfunc=sum)
        return producao_por_membro_pivo

    def pagina_top(self, cabecalho=''):
        nome_grupo = self.grupo.obterParametro('global-nome_do_grupo').decode("utf8")

        s = self.html1
        template = u'<head>' \
                   '<meta http-equiv="Content-Type" content="text/html; charset=utf8">' \
                   '<meta name="Generator" content="scriptLattes">' \
                   '<title>{nome_grupo}</title>' \
                   '<link rel="stylesheet" href="css/scriptLattes.css" type="text/css">' \
                   '<link rel="stylesheet" type="text/css" href="css/jquery.dataTables.css">' \
                   '<link rel="stylesheet" type="text/css" href="css/dataTables.colVis.min.css">' \
                   '<script type="text/javascript" charset="utf8" src="js/jquery.min.js"></script>' \
                   '<script type="text/javascript" charset="utf8" src="js/jquery.dataTables.min.js"></script>' \
                   '<script type="text/javascript" charset="utf8" src="js/dataTables.colVis.min.js"></script>' \
                   '<script src="http://professor.ufabc.edu.br/~jesus.mena/sorttable.js"></script>' \
                   '{cabecalho}' \
                   '</head>' \
                   '<body><div id="header2"> <button onClick="history.go(-1)">Voltar</button>' \
                   '<h2>{nome_grupo}</h2></div>'
        # '<script type="text/javascript" charset="utf8" src="jquery.dataTables.rowGrouping.js"></script>' \
        s += template.format(nome_grupo=nome_grupo, cabecalho=cabecalho)
        return s

    def paginaBottom(self):
        agora = datetime.datetime.now()
        dia = '0' + str(agora.day)
        mes = '0' + str(agora.month)
        ano = str(agora.year)
        hora = '0' + str(agora.hour)
        minuto = '0' + str(agora.minute)
        segundo = '0' + str(agora.second)

        dia = dia[-2:]
        mes = mes[-2:]
        hora = hora[-2:]
        minuto = minuto[-2:]
        segundo = segundo[-2:]
        data = dia + "/" + mes + "/" + ano + " " + hora + ":" + minuto + ":" + segundo

        s = '<br><p>'
        if not self.grupo.obterParametro('global-itens_desde_o_ano') == '' and not self.grupo.obterParametro(
                'global-itens_ate_o_ano') == '':
            s += '<br>(*) Relatório criado com produções desde ' + \
                 self.grupo.obterParametro('global-itens_desde_o_ano') + \
                 ' até ' + \
                 self.grupo.obterParametro('global-itens_ate_o_ano')

        s += '\n<br>Data de processamento: ' + data + '<br> \
        <div id="footer"> \
        Relatório gerado por <a href="http://scriptlattes.sourceforge.net/">scriptLattes ' + self.version + '</a>. \
        Os resultados estão sujeitos a falhas devido a inconsistências no preenchimento dos CVs Lattes. E-mail de contato: <a href="mailto:' + self.grupo.obterParametro(
            'global-email_do_admin') + '">' + self.grupo.obterParametro('global-email_do_admin') + '</a> \
        </div> '

        if self.grupo.obterParametro('global-google_analytics_key'):
            s += '<script type="text/javascript">\
            var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");\
            document.write(unescape("%3Cscript src=\'" + gaJsHost + "google-analytics.com/ga.js\' type=\'text/javascript\'%3E%3C/script%3E"));\
            </script>\
            <script type="text/javascript">\
            try {\
              var pageTracker = _gat._getTracker("' + self.grupo.obterParametro('global-google_analytics_key') + '");\
              pageTracker._trackPageview();\
            } catch(err) {}\
            </script>'
        s += '</body>' + self.html2

        return s.decode("utf8")

    def salvarArquivo(self, nome, conteudo):
        file = open(os.path.join(self.dir, nome), 'w')
        file.write(conteudo)
        file.close()

    def formatarTotaisQualis(self, qtd):
        st = '(<b>A1</b>: ' + str(qtd['A1']) + ', <b>A2</b>: ' + str(qtd['A2']) + ', <b>B1</b>: ' + str(
            qtd['B1']) + ', <b>B2</b>: ' + str(qtd['B2'])
        st += ', <b>B3</b>: ' + str(qtd['B3']) + ', <b>B4</b>: ' + str(qtd['B4']) + ', <b>B5</b>: ' + str(
            qtd['B5']) + ', <b>C</b>: ' + str(qtd['C'])
        st += ', <b>Qualis n&atilde;o identificado</b>: ' + str(qtd['Qualis nao identificado']) + ')'
        st += '<br><p><b>Legenda Qualis:</b><ul>'
        st += '<li> Publica&ccedil;&atilde;o para a qual o nome exato do Qualis foi identificado: <font color="#254117"><b>Qualis &lt;estrato&gt;</b></font>'
        st += '<li> Publica&ccedil;&atilde;o para a qual um nome similar (n&atilde;o exato) do Qualis foi identificado: <font color="#F88017"><b>Qualis &lt;estrato&gt;</b></font> (nome similar)'
        st += '<li> Publica&ccedil;&atilde;o para a qual nenhum nome do Qualis foi identificado: <font color="#FDD7E4"><b>Qualis n&atilde;o identificado</b></font> (nome usado na busca)'
        st += '</ul>'
        return st

        # return 'Sem totais qualis ainda...'


def menuHTMLdeBuscaPB(titulo):
    titulo = re.sub('\s+', '+', titulo)

    s = '<br>\
         <font size=-1> \
         [ <a href="http://scholar.google.com/scholar?hl=en&lr=&q=' + titulo + '&btnG=Search">cita&ccedil;&otilde;es Google Scholar</a> | \
           <a href="http://academic.research.microsoft.com/Search?query=' + titulo + '">cita&ccedil;&otilde;es Microsoft Acad&ecirc;mico</a> | \
           <a href="http://www.google.com/search?btnG=Google+Search&q=' + titulo + '">busca Google</a> ] \
         </font><br>'
    return s


def menuHTMLdeBuscaPT(titulo):
    titulo = re.sub('\s+', '+', titulo)

    s = '<br>\
         <font size=-1> \
         [ <a href="http://www.google.com/search?btnG=Google+Search&q=' + titulo + '">busca Google</a> | \
           <a href="http://www.bing.com/search?q=' + titulo + '">busca Bing</a> ] \
         </font><br>'
    return s


def menuHTMLdeBuscaPA(titulo):
    titulo = re.sub('\s+', '+', titulo)

    s = '<br>\
         <font size=-1> \
         [ <a href="http://www.google.com/search?btnG=Google+Search&q=' + titulo + '">busca Google</a> | \
           <a href="http://www.bing.com/search?q=' + titulo + '">busca Bing</a> ] \
         </font><br>'
    return s


def formata_qualis(qualis, qualissimilar):
    s = ''
    if not qualis == None:
        if qualis == '':
            qualis = 'Qualis nao identificado'

        if qualis == 'Qualis nao identificado':
            # Qualis nao identificado - imprime em vermelho
            s += '<font color="#FDD7E4"><b>Qualis: N&atilde;o identificado</b></font> (' + qualissimilar + ')'
        else:
            if qualissimilar == '':
                # Casamento perfeito - imprime em verde
                s += '<font color="#254117"><b>Qualis: ' + qualis + '</b></font>'
            else:
                # Similar - imprime em laranja
                s += '<font color="#F88017"><b>Qualis: ' + qualis + '</b></font> (' + qualissimilar + ')'
    return s


'''
def formata_qualis(qualis, qualissimilar):
    s = ''

    if not qualis:
        #s += '<font color="#FDD7E4"><b>Qualis: N&atilde;o identificado</b></font>'
        s += ''
    else:
        s += '<font color="#254117"><b>Qualis: </b></font> '
        if type(qualis) is str:
            s += '<font class="area"><b>SEM_AREA</b></font> - <b>' + qualis + '</b>&nbsp'
        else:
            l = ['<font class="area"><b>' + area + '</b></font> - <b>' + q + '</b>' for area, q in
                 sorted(qualis.items(), key=lambda x: x[0])]
            s += '&nbsp|&nbsp'.join(l)
    return s
'''
