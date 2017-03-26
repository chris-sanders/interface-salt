from charms.reactive import RelationBase
from charms.reactive import scopes
from charms.reactive import hook
from charms.reactive import when
#from charms.reactive import remove_state

class SaltRequires(RelationBase):
    scope = scopes.UNIT

    @hook('{requires:salt}-relation-{joined,changed}')
    def changed(self):
        conv = self.conversation()
        print("Requires relation joined/changed called")
        if conv.get_remote('hostname'):
            conv.set_state('{relation_name}.available')
            conv.set_state('{relation_name}.changed')

    @hook('{requires:salt}-relation-{departed}')
    def departed(self):
        conv = self.conversation()
        conv.remove_state('{relation_name}.available')

    @property
    def hostname(self):
        conv = self.conversation()
        return conv.get_remote('hostname')

    def configure_me(self):
        print("salt-minion is asking to be configured")
        self.set_remote(key="unconfigured",value=True)
        self.set_state('salt.minion.configure')
