from jnpr.toby.hldcl.juniper.junos import Juniper


class Switch(Juniper):
    def __init__(self, *args, **kwargs):
        super(Switch, self).__init__(**kwargs)
        self.reboot_timeout  = 900
        self.upgrade_timeout = 1500
        self.issu_timeout = 2400
