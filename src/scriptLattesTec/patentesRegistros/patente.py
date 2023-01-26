#!/usr/bin/env python 
# encoding: utf-8
#
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
#


from scriptLattesTec.geradorDePaginasWeb import *
from scriptLattesTec.util import similaridade_entre_cadeias


class Patente:
    item = None  # dado bruto
    idMembro = None

    relevante = None
    chave = None

    autores = None
    titulo = None
    ano = ""
    pais = None
    tipoPatente = None
    numeroRegistro = None
    dataDeposito = None
    registro = None
    data_pedido = None
    data_concessao = None

    def __init__(self, idMembro, partesDoItem='', relevante=''):
        # partesDoItem[0]: Numero (NAO USADO)
        # partesDoItem[1]: Descricao (DADO BRUTO)
        self.idMembro = set([])
        self.idMembro.add(idMembro)

        if not partesDoItem == '':
            self.relevante = relevante
            self.item = partesDoItem[1]

            # Dividir o item na suas partes constituintes
            partes = self.item.partition(" . ")
            self.autores = partes[0].strip()

            try:
                partes = partes[2]
                partes = partes.partition(", ")
                self.titulo = partes[0][0: len(partes[0]) - 5]
                self.ano = str(int(partes[0][len(partes[0]) - 4: len(partes[0])]))

                partes = partes[2].split(".");

                self.pais = partes[0];
                self.tipoPatente = partes[1].split(":")[1].strip();
                self.numeroRegistro = partes[2].split(":")[1].split(",")[0].strip();
                self.dataDeposito = partes[2].split(":")[2].split(",")[0].strip();
            except:
                print("Erro no registro ", self.item)

            self.chave = self.autores  # chave de comparação entre os objetos

            print(self.__str__)

    def compararCom(self, objeto):
        if self.idMembro.isdisjoint(objeto.idMembro) and similaridade_entre_cadeias(self.titulo, objeto.titulo):
            # Os IDs dos membros são agrupados. 
            # Essa parte é importante para a criação do GRAFO de colaborações
            self.idMembro.update(objeto.idMembro)

            if len(self.autores) < len(objeto.autores):
                self.autores = objeto.autores

            if len(self.titulo) < len(objeto.titulo):
                self.titulo = objeto.titulo

            return self
        else:  # nao similares
            return None

    def html(self, listaDeMembros):
        try:
            s = self.autores + '. <b>' + self.titulo + '</b>. '
            s += str(self.ano) + '. ' + str(self.pais) + '. '
            s += str(self.numeroRegistro) + '. ' + str(self.dataDeposito) + '.'
            s += menuHTMLdeBuscaPT(self.titulo)
        except:
            s = ""
        return s

    def csv(self):
        s = ''
        s += str(self.ano) + '\t'
        s += str(self.relevante) + '\t'
        s += (self.autores + '\t' if self.autores else '\t')
        s += (self.titulo + '\t' if self.titulo else '\t')
        s += (self.registro + '\t' if self.registro else '\t')
        s += (self.data_pedido + '\t' if self.data_pedido else '\t')
        s += (self.data_concessao + '\t' if self.data_concessao else '\t')

        return s

    def colunas_csv(self):
        return 'ANO' + '\t' + 'RELEVANTE' + '\t' + 'AUTORES' + '\t' + 'TITULO' + '\t' + 'REGISTRO' + '\t' + 'DATA_PEDIDO' + '\t' + 'DATA_CONCESSAO'

    # ------------------------------------------------------------------------ #
    def __str__(self):
        s = "\n[PATENTE E REGISTRO] \n"
        s += "+ID-MEMBRO   : " + str(self.idMembro) + "\n"
        s += "+RELEVANTE   : " + str(self.relevante) + "\n"
        s += "+AUTORES     : " + str(self.autores) + "\n"
        s += "+TITULO      : " + str(self.titulo) + "\n"
        s += "+ANO         : " + str(self.ano) + "\n"
        s += "+item        : " + str(self.item) + "\n"
        return s
