# -*- coding: utf-8 -*-
import telnetlib


class IOS:
    def __init__(self, fileHosts=None, host=None):
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

        self.__config = [b'enable\n', b'conf t\n']

    def set_user(self, user, password):
        """Define variaveis de usuario"""
        self.__user = {
            'name': user,
            'password': password
        }

    def get_user(self):
        return self.__user

    def login(self, telnet_obj):
        user = self.get_user()
        if user:
            try:
                telnet_obj.read_until(b"Username: ")
                telnet_obj.write(user['name'].encode('ascii') + b"\n")
                if user['password']:
                    telnet_obj.read_until(b"Password: ")
                    telnet_obj.write(user['password'].encode('ascii') + b"\n")
                else:
                    print('Password não pode ter valor nulo')
            except Exception as e:
                print('Falha ao tentar logar com usuario %s'
                      '\n Erro %s' % (user['name'], e))

    def addConfig(self, configLine):
        """Incrementa configurações da instancia para serem
         executadas nos hosts"""
        if not isinstance(configLine, bytes):
            self.__config.append(bytes(configLine))
        else:
            self.__config.append(configLine)

    def getConfig(self):
        """Retorna lista de configureções"""
        return self.__config

    def configure(self):
        """Executa comandos que existem no contexto"""
        config = self.getConfig()
        for host in self.hosts:
            host = host.split()
            if host:
                try:
                    if self.get_user():
                        tn = telnetlib.Telnet(host)
                        self.login(tn)

                        for conf in config:
                            tn.write(conf)
                            # finaliza configuração
                            tn.write(b'end\n')
                            # desconecta telnet deste host
                            tn.write(b'exit\n')

                            assert tn.read_all(), "Algo deu errado."
                    else:
                        print('Erro: Usuário não foi definido')

                except Exception as e:
                    print ('Erro ao tentar conectar'
                           ' no Host %s\n %s' % (host[0], e))

                return 0
