#conectando ao MySql 
import mysql.connector 
import os

from mysql.connector.utils import read_int #modulo para limpar tela
from conector import Banco #importando arquivo externo para pegar informações do banco
import getpass #modulo para esconder a senha no prompt (a senha nao aparecerá)
conexao = mysql.connector.connect(host=Banco.dados['host'],database=Banco.dados['database'],user=Banco.dados['user'],password=Banco.dados['password'])
if conexao.is_connected(): #verificando se conexao foi realizada, se sim:
        db_info = conexao.get_server_info() #busca versao do server
        print("Conexão realizada com sucesso! Servidor versão: ",db_info)
        mycursor = conexao.cursor(buffered=True) #criando variavel "mycursor" para executar comandos sql
        mycursor1 = conexao.cursor(buffered=True) #criando variavel "mycursor1" para executar comandos sql
else:
    print("Problemas em conectar")

#encerrar conexao
def pararConexao():
    conexao.close()
    print("Conexão encerrada com sucesso!") 

#limpar tela
def limparTela():
    os.system('cls')

#   FUNÇÕES 
# TELA DE BOAS VINDAS
def bemVindo():
    limparTela()
    print('')
    print('-- SISTEMA CONSULTÓRIO MÉDICO --')
    print('versão: 1.0')
    print('SEJA BEM VINDO(a)')

# LOGIN
def login():
    escolha()
    F = input('Informe sua posição: ')
    # Login (Paciente,Médico,Gestor,Administrador)
    if(F == '1'):
        loginPaciente()
    elif(F == '2'):
        loginMedico()
    elif(F == '3'):
        loginGestor()
    elif(F == '4'):
        loginAdm()
    else:
        limparTela()
        print('Opção invalida!')
        login()

# Cadastrar paciente,medico,gestor
def cadastrar():
    escolhaAdm()
    arm = input("Escolha o usuário a cadastrar: ")
    #cadastro Paciente
    if arm == '1':
        nomeUsu = input("Digite um nome para o usuário: ")
        senha = input("Digite uma senha para o usuário: ")
        nomeCompleto = input("Digite o nome completo do Paciente: ")

        sql = ("INSERT INTO tbl_Paciente(nm_Usuario,ds_Senha,nm_Completo) VALUES(%s,%s,%s)") #inserindo credenciais no banco de dados
        val = (nomeUsu,senha,nomeCompleto) 
        mycursor.execute(sql, val)
        conexao.commit()
        print("Cadastro realizado com sucesso!")                
        continuarOUsair()
            
    #cadastro Médico
    elif arm == '2':
        nomeUsu = input("Digite um nome para o usuário: ")
        senha = input("Digite uma senha para o usuário: ")
        nomeCompleto = input("Digite o nome completo do Médico: ")
        especialidade = input("Digite a especialidade do médico: ")

        sql = ("INSERT INTO tbl_Medico(nm_Usuario,ds_Senha,nm_Completo,ds_Especialidade) VALUES(%s,%s,%s,%s)") #inserindo credenciais no banco de dados
        val = (nomeUsu,senha,nomeCompleto,especialidade) 
        mycursor.execute(sql, val)
        conexao.commit()
        print("Cadastro realizado com sucesso!")            
        continuarOUsair()

    #cadastro Gestor
    elif arm == '3':
        nomeUsu = input("Digite um nome para o usuário: ")
        senha = input("Digite uma senha para o usuário: ")
        nomeCompleto = input("Digite o nome completo do Gestor: ")

        sql = ("INSERT INTO tbl_Gestor(nm_Usuario,ds_Senha,nm_Completo) VALUES(%s,%s,%s)") #inserindo credenciais no banco de dados
        val = (nomeUsu,senha,nomeCompleto) 
        mycursor.execute(sql, val)
        conexao.commit()
        print("Cadastro realizado com sucesso!")              
        continuarOUsair()
             
    else:
        print('escolha uma opção válida!')
        cadastrar()

# continuar ou sair
def continuarOUsair():
    arm2=int(input("Digite 1 para continuar cadastrando ou 2 para sair: "))
    if arm2== 1:
        cadastrar()
    elif arm2== 2:
        limparTela()
        login()
    else:
        print('Escolha a opção 1 ou 2!!!')
        continuarOUsair()

def continuarOUsairMedico():
    sair=int(input("Digite 1 para continuar a sessão ou 2 para encerrar: "))
    if sair==1:
            programaMedico()
    else:
            print("Sessão encerrada!")

def continuarOUsairPaciente():
    sair=int(input("Digite 1 para continuar a sessão ou 2 para encerrar: "))
    if sair==1:
            programaPaciente()
    else:
            print("Sessão encerrada!")

def continuarOUsairGestor():
    sair=int(input("Digite 1 para continuar a sessão ou 2 para encerrar: "))
    if sair==1:
            programaGestor()
    else:
            print("Sessão encerrada!")

# PROGRAMAS DE CADA USUARIO
def programaMedico():
    limparTela()
    print('--- BEM VINDO(a)!!! ---')
    escolha=int(input("Digite 1 para exibir as consultas marcadas em seu nome; 2 para marcar uma agenda; 3 para apagar uma agenda: "))
    if escolha==1: #visualizar consultas marcadas em seu nome
        print('--- CONSULTAS MARCADAS ---')
        mycursor.execute("select * FROM tbl_Consulta WHERE sg_Disponibilidade = 'A' AND cd_Medico='%s' " % (cod1)) #exibindo as consultas confirmadas
        myresult = mycursor.fetchall()

        for x in myresult:
            print(x)
        
        continuarOUsairMedico()
    
    elif escolha==2: #marcar uma agenda
        dataDisponivel = str(input("Digite uma data para disponibilizar horários: "))
        horaEntrada = str(input("Digite seu horário de entrada para este dia: "))
        horaSaida = str(input("Digite seu horário de saída para este dia: "))

        confirmar=int(input("Se deseja confirmar a agenda digite 1 senão digite 2: "))
        if confirmar==1:
            sql = ("INSERT INTO tbl_agendaMedico(cd_Medico, ds_Data, hr_Entrada, hr_Saida) VALUES (%s,%s,%s,%s)")
            val = (cod1, dataDisponivel, horaEntrada, horaSaida) 
            mycursor.execute(sql, val)
            conexao.commit()
            print("Agenda cadastrada com sucesso!")
            continuarOUsairMedico()
        else:
            print("Agenda não foi marcada")
            continuarOUsairMedico()
    
    elif escolha ==3: #desmarcar uma agenda
        print('--- AGENDA MEDICO ---')
        mycursor.execute("select * FROM tbl_agendaMedico WHERE cd_Medico='%s' " % (cod1)) 
        myresult = mycursor.fetchall()

        for x in myresult:
            print(x)
        
        print('')
        apagar=input("Digite a data da consulta a apagar: ")
        confirmar=int(input("Se deseja confirmar digite 1 senão digite 2: "))
        if confirmar==1:
            mycursor.execute("DELETE FROM tbl_agendaMedico WHERE ds_Data='%s' AND cd_Medico='%s' " % (apagar,cod1)) #futuramente fazer WHERE ds_Data='%s' AND cd_Medico='%s'
            conexao.commit()
            print("Agenda apagada com sucesso!")
            continuarOUsairMedico()
        else:
            print("Agenda não foi apagada")
            continuarOUsairMedico()

    else:
        print("Digite uma opção válida!!!")
        programaMedico()
    # em escolha==1 exibir com WHERE cd_Medico='%s' para aparecerem apenas consultas do medico de login atual
    # atualizar a tabela consulta

def programaPaciente():
    limparTela()
    print("--- AGENDA DE MÉDICOS DISPONÍVEIS ---")
    mycursor.execute("select * from vw_mostrarAgendaMedico") #exibindo a agenda dos medicos
    myresult = mycursor.fetchall()

    for x in myresult:
        print(x)

    entrar=int(input("Digite 1 para solicitar uma consulta ou 2 para encerrar: "))
    if entrar==1:
        print("")
        medico = str(input("digite o nome do medico que deseja marcar consulta: "))
        especialidade = str(input("digite a especialidade do medico: "))
        data = str(input("digite a data desejada para consulta: "))
        hora = str(input("digite a hora desejada para consulta (*a consulta terá tempo máximo de 50min): "))

        sql = ("INSERT INTO tbl_Consulta(nm_Medico,ds_Especialidade,ds_Data,hr_Consulta) VALUES (%s,%s,%s,%s)") #inserindo credenciais no banco de dados
        val = (medico,especialidade,data,hora)
        mycursor.execute(sql, val)
        conexao.commit()
        print("Solicitação de consulta concluída!")
        continuarOUsairPaciente()
        # inserir codigo do paciente que solicitou automaticamente na tbl_Consulta
    else:
        print("Programa encerrado!")

def programaGestor():
    limparTela()
    print("--- BEM VINDO(a)!!! ---")
    print("-- AGENDA DOS MÉDICOS --")
    mycursor.execute("select * from vw_mostrarAgendaMedico") #exibindo a agenda dos medicos
    myresult = mycursor.fetchall()

    for x in myresult:
        print(x)

    print("")
    print("-- CONSULTAS SOLICITADAS -- ")
    mycursor1.execute("select * from vw_mostrarSolicitacoesConsulta") #exibindo consultas solicitadas
    myresult1 = mycursor1.fetchall()

    for x in myresult1:
        print(x)

    #gestor deverá escolher o código da consulta a se alterar o status
    print("")
    cod=int(input("Digite o codigo da consulta a alterar o status: "))
    alterarStatus=int(input("Digite 1 para confirmar a consulta; 2 para desmarcar a consulta; 3 para manter inativa: "))
    if alterarStatus == 1: #confirmar consulta
        #solicitar codigo do gestor
        # sql=("INSERT INTO tbl_Consulta(cd_Gestor) WHERE cd_Gestor='%s' ") 
        # acima devo inserir na tabela consulta o codigo do gestor que alterou o status da consulta
        confirmar=int(input("Digite 1 para confirmar a escolha ou 2 para cancelar: "))
        if confirmar==1:
            mycursor.execute("UPDATE tbl_Consulta SET sg_Disponibilidade = 'A' WHERE cd_Consulta='%s' " % (cod))
            conexao.commit()
            print("Consulta marcada com sucesso!") 
        else:
            print("Nenhuma alteração foi feita")
        continuarOUsairGestor()

    elif alterarStatus == 2: #desmarcar consulta
        confirmar=int(input("Digite 1 para confirmar a escolha ou 2 para cancelar: "))
        if confirmar==1:
            mycursor.execute("UPDATE tbl_Consulta SET sg_Disponibilidade = 'I' WHERE cd_Consulta='%s' " % (cod))
            conexao.commit()
            print("Consulta desmarcada com sucesso!") 
        else:
            print("Nenhuma alteração foi feita")
        continuarOUsairGestor()

    else: #manter status
        print("Consulta não teve seu status alterado")
        continuarOUsairGestor()

# Login de cada usuário
def loginPaciente():
    x = input('Usuário: ')
    y = getpass.getpass('Senha: ')
    mycursor.execute("select nm_Usuario, ds_Senha FROM tbl_Paciente WHERE nm_Usuario = '%s' and ds_Senha = '%s'" % (x,y)) #validando login
    verificacao = mycursor.fetchall()

    if verificacao:
        print('Bem vindo(a)!')
        programaPaciente()
    else:
        print("Usuário ou senha incorretos!")
        login()

def loginMedico():
    x = input('Usuário: ')
    y = getpass.getpass('Senha: ')
    mycursor.execute("select nm_Usuario, ds_Senha FROM tbl_Medico WHERE nm_Usuario = '%s' and ds_Senha = '%s'" % (x,y))
    verificacao = mycursor.fetchall()

    if verificacao:
        mycursor1.execute("select cd_Medico FROM tbl_Medico WHERE nm_Usuario = '%s'" % (x)) 
        cod=mycursor1.fetchone() #inserindo cod do medico na variavel (será retornada uma lista)
        global cod1 #criando variavel global para nao precisar ficar passando como parâmetro nas funções
        cod1=cod[0] #passando para a variável 'cod1' a primeira posição da lista que contém o cod do medico que acabou de fazer login
        print('Bem vindo(a)!')
        programaMedico() #passando como parâmetro ao programaMedico o cod do medico guardado em 'cod1'
    else:
        print("Usuário ou senha incorretos!")
        login()

def loginGestor():
    x = input('Usuário: ')
    y = getpass.getpass('Senha: ')
    mycursor.execute("select nm_Usuario, ds_Senha FROM tbl_Gestor WHERE nm_Usuario = '%s' and ds_Senha = '%s'" % (x,y))
    verificacao = mycursor.fetchall()

    if verificacao:
        print('Bem vindo(a)!')
        programaGestor()
    else:
        print("Usuário ou senha incorretos!")
        login()

def loginAdm():
    x = input('Usuário: ')
    y = getpass.getpass('Senha: ')
    mycursor.execute("select nm_Usuario, ds_Senha FROM tbl_Administrador WHERE nm_Usuario = '%s' and ds_Senha = '%s'" % (x,y))
    verificacao = mycursor.fetchall()

    if verificacao:
        print('Bem vindo(a)!')
        cadastrar()
    else:
        print("Usuário ou senha incorretos!")
        login()

# exibir opções de Login
def escolha():
    print('')
    print('      * Login *    ')
    print('   -- Paciente 1 --  ')
    print('    -- Médico 2 --   ')
    print('    -- Gestor 3 --   ')
    print(' -- Administrador 4 --')
    print('')

def escolhaAdm():
    limparTela()
    print('')
    print('    * Cadastro *    ')
    print('   -- Paciente 1 --  ')
    print('    -- Médico 2 --   ')
    print('    -- Gestor 3 --   ')
    print('')
#   FIM FUNÇÕES 

# INICIO PROGRAMA #
bemVindo()
login()

               # DESENVOLVIMENTO
#Programa Medico
    #disponibiliza sua agenda (horario entrada/saida e data) -
    #visualiza consultas marcadas em seu nome


#Programa Paciente
    #pode ver a agenda dos médicos disponiveis
    #faz a solicitação de consulta (confirmada pelo gestor) com os dados:
    #                               data,hora,medico,especialidade


#Programa Gestor
    #exibir agenda dos medicos e solicitações dos pacientes
    #confirma ou mantém inativa a solicitação de consulta. 
    # Se confirmar,a consulta passará a aparcer p/o respectivo medico