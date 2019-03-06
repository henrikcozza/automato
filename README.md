# automato
library para automação de rede
Det
## exemplo de uso
```python
from automato.telnet import IOS

conf = IOS(fileHosts='myswitches', pass_enable='cisco')
conf.set_user(user='admin', password='cisco')
conf.addConfig('vlan 101')
conf.addConfig('name Python_VLAN 101')
conf.configure()

```
