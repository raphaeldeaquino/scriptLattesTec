#!/usr/bin/env python 
# encoding: utf-8
#
#  scriptLattesTec
#  Copyright https://github.com/raphaeldeaquino/scriptLattesTec
#
#  Este programa é um software livre; você pode redistribui-lo e/ou 
#  modifica-lo dentro dos termos da Licença Pública Geral GNU como 
#  publicada pela Fundação do Software Livre (FSF); na versão 2 da 
#  Licença, ou (na sua opinião) qualquer versão.
#
#  Este programa é distribuído na esperança que possa ser util, 
#  mas SEM NENHUMA GARANTIA; sem uma garantia implicita de ADEQUAÇÂO a qualquer
#  MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a
#  Licença Pública Geral GNU para maiores detalhes.
#
#  Você deve ter recebido uma cópia da Licença Pública Geral GNU
#  junto com este programa, se não, escreva para a Fundação do Software
#  Livre(FSF) Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from scriptLattesTec.grupo import *
from scriptLattesTec.util import *
import sys

if 'win' in sys.platform.lower():
    os.environ['PATH'] += ";" + os.path.abspath(os.curdir + '\\Graphviz2.36\\bin')


def executar_scriptlattestec(arquivo_configuracao):
    novoGrupo = Grupo(arquivo_configuracao)
    novoGrupo.imprimirListaDeRotulos()
    novoGrupo.carregar_dados_temporarios_de_geolocalizacao()

    if criarDiretorio(novoGrupo.obterParametro('global-diretorio_de_saida')):
        novoGrupo.carregarDadosCVLattes()  # obrigatorio
        novoGrupo.compilarListasDeItems()  # obrigatorio
        novoGrupo.identificarQualisEmPublicacoes()  # obrigatorio
        novoGrupo.gerarArquivosCsv()  # obrigatorio
        novoGrupo.gerarGrafosCsv()  # obrigatorio

        novoGrupo.salvar_dados_temporarios_de_geolocalizacao()

        # finalizando o processo

        # para incluir a producao com colaboradores é necessário um novo chamado ao scriptLattes
        if novoGrupo.obterParametro('relatorio-incluir_producao_com_colaboradores'):
            executar_scriptlattestec(
                novoGrupo.obterParametro('global-diretorio_de_saida') + "/producao-com-colaboradores.config")


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s - %(levelname)s (%(name)s) - %(message)s')
    logging.root.setLevel(level=logging.DEBUG)
    logger.info("Executando '{}'".format(' '.join(sys.argv)))
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    logging.root.addHandler(handler)

    executar_scriptlattestec(sys.argv[1])
