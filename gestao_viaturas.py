import csv
from decimal import Decimal as dec
from datetime import date, datetime
import subprocess
import sys
from typing import TextIO

CSV_DEFAULT_DELIM = ','
DEFAULT_INDENTATION = 3


class Viatura: 
    def __init__(
        self,
        matricula: str,
        marca: str,
        modelo: str,
        data: date
    ):
        if not matriculaValida(matricula) :
            raise InvalidViatAttribute(f'Matricula {matricula} inválida')
        
        if not modeloValido(modelo):
            raise InvalidViatAttribute(f'Modelo {modelo} inválido')
        
        if not marcaValida(marca):
            raise InvalidViatAttribute(f'Marca {marca} inválida')
        
        if data.year < 1990:
            raise InvalidViatAttribute(f'Data {data} inválida. Deve ser >= 1990')

        self.matricula = matricula
        self.marca = marca
        self.modelo = modelo
        self.data = data


    @classmethod
    def from_csv(cls, linha: str, delim = CSV_DEFAULT_DELIM) -> 'Viatura':
        attrs = linha.split(delim)
        return Viatura(
                matricula= attrs[0],
                marca = attrs[1],
                modelo = attrs[2],
                data = transformStrtoDate(attrs[3])
        )
        
    def __str__(self) -> str:
        cls_name = self.__class__.__name__
        return f'{cls_name}[matricula= {self.matricula} marca = "{self.marca}" modelo = "{self.modelo}"]'
    
    def __repr__(self) -> str:
        cls_name = self.__class__.__name__
        return f'{cls_name}[matricula= {self.matricula} marca = "{self.marca}" modelo = "{self.modelo}", '\
        f'data={self.data.strftime("%Y-%m-%d")})'

    
class InvalidViatAttribute(ValueError):
    pass

class CatalogoViaturas: 
    def __init__(self):
        self._viaturas = {}
    
    def append(self, viatura: Viatura):
        if viatura.matricula in self._viaturas:
            raise DuplicateValue(f'Já existe viatura com matricula {viatura.matricula} no catálogo')
        self._viaturas[viatura.matricula] = viatura

    ###Alterar essa função
    def obtem_por_matricula(self, matricula: str) -> Viatura | None:
        return self._viaturas.get(matricula)
    
    def remove_por_matricula(self, matricula: str) -> Viatura | None:
        viatura = self._viaturas.get(matricula)
        if viatura:
            del self._viaturas[matricula]
        return viatura
    #:
    
    def pesquisa(self, criterio) -> 'CatalogoViaturas':
        encontrados = CatalogoViaturas()
        for viatura in self._viaturas.values():
            if criterio(viatura):
                encontrados.append(viatura)
        return encontrados
    #def Viatura_e_al(prod: Viatura):
    #return prod.modelo =='AL'
    # Viaturas.pesquisa(Viaturas_e_al) - retorna todos os Viaturas com modelo AL
    
    def __str__(self):
        class_name = self.__class__.__name__
        return f'{class_name}[#Viaturas = {len(self._viaturas)}]'

    def __iter__(self):
        for prod in self._viaturas.values():
            yield prod   #append(prod) and return final list
    
    def __len__(self):
        return len(self._viaturas)
    

class DuplicateValue(Exception): 
    pass


###Utils

def transformStrtoDate(data_string: str):
    return datetime.strptime(data_string, '%Y-%m-%d').date()

####Validações

def matriculaValida(matricula: str):
    partes = matricula.split("-")
    if len(partes) != 3:
        return False
    if len(partes[0]) != 2 or not partes[0].isdigit():
        return False
    if len(partes[2]) != 2 or not partes[2].isdigit():
        return False
    if not partes[1].isupper():
        return False
    return True

def marcaValida(marca:str):
    if len(marca) < 3:
        return False
    return marca

def modeloValido(modelo):
    return marcaValida(modelo)

##################
##  leitura dos ficheiros
##################

def le_Viaturas(caminho_fich: str, delim = CSV_DEFAULT_DELIM) -> CatalogoViaturas:
    viaturas = CatalogoViaturas()
    #ler ficheiro e popular catalogo com cada um dos Viaturas
    #uma linha do ficheiro corresponde a um Viatura
    with open(caminho_fich, 'rt') as fich:
        for linha in linhas_relevantes(fich):
            viaturas.append(Viatura.from_csv(linha, delim))
    return viaturas

def linhas_relevantes(fich: TextIO):
    linhas = []
    for linha in fich:
        linha = linha.strip()
        if len(linha)==0 or linha[0]=='#':
            continue
        yield linha

def exibe_msg(*args, indent = DEFAULT_INDENTATION, **kargs):
    print(' ' * (indent - 1), *args, **kargs)

def entrada(msg: str, indent = DEFAULT_INDENTATION) -> str:
    return input(f"{' ' * DEFAULT_INDENTATION}{msg}")


def cls():
    if sys.platform == 'win32':
        subprocess.run(['cls'], shell=True, check=True)
    elif sys.platform in ('darwin', 'linux', 'bsd', 'unix'):
        subprocess.run(['clear'], check=True)

def pause(msg: str="Pressione ENTER para continuar...", indent = DEFAULT_INDENTATION):
    input(f"{' ' * indent}{msg}")

viaturas = CatalogoViaturas()

def save_viaturas_to_csv(viaturas, filename):
    fieldnames = ['Matricula', 'Marca', 'Modelo', 'Data']

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for viatura in viaturas:
            writer.writerow({'Matricula': viatura.matricula,
                             'Marca': viatura.marca,
                             'Modelo': viatura.modelo,
                             'Data': viatura.data.strftime("%Y-%m-%d")})

def exec_menu():
    while True:
        cls()
        exibe_msg("* L - Listar viaturas                   *")
        exibe_msg("* P - Pesquisar Viaturas                *")
        exibe_msg("* A - Adicionar Viatura                 *")
        exibe_msg("* R - Remover Viatura                   *")
        exibe_msg("* G - Guardar catálogo em ficheiro      *")
        exibe_msg("*                                       *")
        exibe_msg("* T - Terminar programa                 *")
        exibe_msg("*****************************************")

        ##as opcoes P, A,E e G ainda tem que ser adicionados 

        print()
        opcao = entrada("OPCAO> ").strip().upper()

        if opcao in('L', 'LISTAR'):
            exec_listar()
        elif opcao in ('P', 'PESQUISAR'):
            exec_pesquisar()
        elif opcao in ('A', 'ADICIONAR'):
            exec_adicionar()
        elif opcao in ('R', 'REMOVER'):
            exec_remover()
        elif opcao in ('G', 'GUARDAR'):
            exec_guardar()
        elif opcao in('T', 'TERMINAR'):
            exec_terminar()
        else:
            exibe_msg(f"Opção {opcao} invalida!")
            pause()

  
def exec_listar():
    cabecalho = f'{"Matricula":^8}|{"Marca":^26}|{"Modelo":^8}|{"Data":^16}|'
    separador = f'{"-" * 8}+{"-" * 26}+{"-" * 8}+{"-" * 16}+{"-" * 16}'
    # separador =  '|'.join(['-' * 16] * 5)
    print()
    exibe_msg(cabecalho)
    exibe_msg(separador)
    for viatura in viaturas:
        linha = f'{viatura.matricula:^8}|{viatura.marca:^26}|{viatura.modelo:^8}|{viatura.data.strftime("%Y-%m-%d"):^16}|'
        exibe_msg(linha)
    #:
    exibe_msg(separador)
    print()
    pause()
#:
    
def exec_adicionar():
    input = 'Introduza a sua viatura com seguinte formato: Matricula, Marca, Modelo, Data'
    exibe_msg(input)
    print()
    nova_matricula = entrada("Matricula (00-AA-00) > ").strip().upper()
    nova_marca = entrada("Marca > ").strip().upper()
    novo_modelo = entrada("Modelo > ").strip().upper()
    nova_data = entrada("Data (YYYY-MM-DD) > ").strip().upper()
    try:
        viaturas.append(Viatura(
                matricula= nova_matricula,
                marca = nova_marca,
                modelo = novo_modelo,
                data = transformStrtoDate(nova_data)))
        exibe_msg(f'A nova viatura com matricula= {nova_matricula} marca = "{nova_marca}" modelo = "{novo_modelo} data="{nova_data} foi adicionada com sucesso!')
        pause()
    except ValueError:
        print("Não foi possível adicionar a viatura. Por favor, tente mais uma vez.")
        pause()

def exec_pesquisar():
    input = 'Introduza a matricula da viatura que pretende pesquisar, no seguinte formato: 00-AA-00'
    exibe_msg(input)
    print()
    nova_matricula = entrada("Matricula (00-AA-00) > ").strip().upper()
    viatura_encontrada = viaturas.obtem_por_matricula(nova_matricula)
    if viatura_encontrada: 
        exibe_msg(f'A viatura encontrada: matricula = {nova_matricula} marca = "{viatura_encontrada.marca}" modelo = "{viatura_encontrada.modelo} data="{viatura_encontrada.data.strftime("%Y-%m-%d")}')
        print()
        pause()
    else: 
        exibe_msg('Não existem viaturas com essa matricula')
        print()
        pause()

def exec_remover():
    input = 'Introduza a matricula da viatura que pretende eliminar, no seguinte formato: 00-AA-00'
    exibe_msg(input)
    print() 
    matricula = entrada("Matricula (00-AA-00) > ").strip().upper()
    viatura_encontrada = viaturas.remove_por_matricula(matricula)
    if viatura_encontrada: 
        exibe_msg(f'A viatura encontrada com seguintes parametros foi eliminada: matricula = {matricula} marca = "{viatura_encontrada.marca}" modelo = "{viatura_encontrada.modelo} data="{viatura_encontrada.data.strftime("%Y-%m-%d")}')
        print()
        pause()
    else: 
        exibe_msg('Não existem viaturas com essa matricula')
        print()
        pause()

def exec_guardar():
    try:
        save_viaturas_to_csv(viaturas,"viaturas_test.csv")
        exibe_msg('As viaturas foram exportadas com sucesso!')
        print()
        pause()
    except Exception as e:
        print("Não foi possível exportar o ficheiro. Tente novamente.", e)

def exec_terminar():
    sys.exit(0)

##################
##  leitura dos ficheiros
##################
        

def main() -> None:
    global viaturas
    viaturas = le_Viaturas('viaturas.csv')
    exec_menu()
    
if __name__=='__main__':
    main()



