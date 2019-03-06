# -*- coding: utf-8 -*-
import telnetlib


class IOS:
    def __init__(self, fileHosts=None, host=None, pass_enable=''):
        """Incializa construtor armazenando hosts que seram
        configurados"""
        if not fileHosts:
            assert host, "É necessário informar o parametro host ou um " + \
                    "arquivo\ncontendo todos os hosts utilizados na " + \
                    "configuração."
            self.hosts = [host]
        else:
            with open(fileHosts) as file:
                self.hosts = file.read().splitlines()

        self.__config = [b'enable\n', pass_enable.encode('ascii')+b'\n', b'conf t\n']

    def set_user(self, user, password):
        """Define variaveis de usuario"""
        self.__user = {
            'name': user,
            'password': password
        }

    def get_user(self):
        return self.__user

    def login(self, host):
        user = self.get_user()
        tn = None

        if user:
            try:
                print("Configurando Switch %s" % (host))

                try:
                    tn = telnetlib.Telnet(host)
                except Exception as e:
                    print('host - %s : erro - %s'%(host,e))

                tn.read_until(b"Username: ")
                tn.write(user['name'].encode('ascii') + b"\n")
                if user['password']:
                    tn.read_until(b"Password: ")
                    tn.write(user['password'].encode('ascii') + b"\n")
                else:
                    print('Password não pode ter valor nulo')
            except Exception as e:
                print('Falha ao tentar logar com usuario %s'
                      '\n Erro %s' % (user['name'], e))

        return tn

    def addConfig(self, configLine):
        """Incrementa configurações da instancia para serem
         executadas nos hosts"""

        if not isinstance(configLine, bytes):
            if '\n' not in configLine:
                configLine += '\n'
            self.__config.append(bytes(configLine, 'utf-8'))
        else:
            if b'\n' not in configLine:
                configLine += b'\n'
            self.__config.append(configLine)

    def loadConfigFile(self, file):
        """Carrega configurações aplicadas nos dispositivos atraves
            de um arquivo de texto simples"""
        with open(file) as f:
            # concatena os 3 primeiros elementos da configuração definidos no
            # com as configurações carregasdas do arquivo.
            self.__config = self.__config[:3] + [x.encode('ascii') for x in f.read().splitlines()]

    def getConfig(self):
        """Retorna lista de configureções"""
        return self.__config

    def configure(self):
        """Executa comandos que existem no contexto"""
        config = self.getConfig()
        config += [b'end\n', b'exit\n']
        for host in self.hosts:
            if host:
                try:
                    if self.get_user():
                        tn = self.login(host)
                        for conf in config:
                            tn.write(conf)
                        print(tn.read_all().decode('ascii'))
                    else:
                        print('Erro: Usuário não foi definido')

                except Exception as e:
                    print ('Erro ao tentar conectar'
                           ' no Host %s\n %s' % (host, e))
                print('host %s configurado' % host)
        return 0
