# scriptLattesTec

**scriptLattesTec** é uma extensão da ferramenta scriptLattes (https://scriptlattes.sourceforge.net), que adiciona as seguintes funcionalidades:
* Extração de produções, considerando mais categorias (sobretudo para produções técnicas).
* Geração de datasets no formato CSV.
* Geração de grafos de colaborações endógenas no formato CSV.

O software pode ser utilizado para gerar dados que servirão de entrada para análises sobre as produções de um Programa de Pós-Graduação *Stricto Sensu* e/ou instrumentar a geração de relatórios ou páginas web. Como exemplo, as páginas disponibilizadas em https://teclimpa.ifg.edu.br/producao são geradas a partir dos dados extraídos com scriptLattesTec.

### Execução

	scriptLattesTec.py <nome_arquivo_de_configuracao>


Teste o scriptLattes com o seguinte exemplo (linha de comandos):

	cd <nome_diretorio_scriptLattesTec>
	python scriptLattesTec.py ./config/teclimpa.config

Nesse exemplo consideram-se todas as produções dos docentes do Programa de Pós-Graduação em Tecnologia, Gestão e Sustentabilidade do IFG, cujos arquivos dos currículos Lattes estão na pasta <code>./config/cache</code>. Os IDs Lattes dos membros, assim como o tempo de vínculo ao programa, está listada em: <code>./config/teclimpa.list</code>. O resultado da execução estará disponível em: <code>./config/teclimpa/</code>.

### Idealizador do projeto

Raphael de Aquino Gomes ([raphael.gomes@ifg.edu.br](mailto:raphael.gomes@ifg.edu.br)).

### URL do projeto

	https://github.com/raphaeldeaquino/scriptLattesTec
