"""
Class for SRC Devices
"""
from jnpr.toby.hldcl.juniper.junos import Juniper
from jnpr.toby.exception.toby_exception import TobyException

class Src(Juniper):
    """
    Base class for SRC devices
    """
    def __init__(self, *args, **kwargs):
        super(Src, self).__init__(*args, **kwargs)

    def execute(self, **kwargs):
        """
        Executes commands on text channel

        device_object.execute(command = 'show version detail | no-more')

        :param command:
            **REQUIRED** CLI command to execute
        :param timeout:
            *OPTIONAL* Time by which response should be received. Default is
            60 seconds
        :param pattern: Pattern to match.
        :return: Dictionary with the following keys
            'response': Response from the CLI command(text/xml)
        """
        command = ''
        if 'command' in kwargs and kwargs['command'] is not None:
            command = kwargs['command']
        else:
            self.log(level="ERROR", message="Mandatory argument 'command' "
                                            "is missing!")

        timeout = kwargs.get('timeout', 60)
        pattern = kwargs.get('pattern')
        no_response = kwargs.get('no_response', False)
        raw_output = kwargs.get('raw_output', False)

        if pattern is None:
            pattern = self.prompt

        if 'text' not in self.channels.keys():
            self.log(level='error', message="'text' channel does not exist")
            raise Exception("'text' channel does not exist")

        response = self.channels['text'].execute(
            cmd=command, pattern=pattern, device=self, no_response=no_response,
            timeout=timeout, raw_output=raw_output)

        if response == -1:
            self.log(level="DEBUG",
                     message="Timeout seen while retrieving output")
            raise Exception('Timeout seen while retrieving output')
        else:
            return self.response

    # Mode Shift
    def _switch_mode(self, mode='CLI', config_mode=''):
        """
        switch to desired mode and set default cli options
        """
        curr_mode = self.mode.upper()
        mode = mode.upper()
        if mode == 'CONFIG':
            curr_config_mode = self.config_mode.upper()
        else:
            curr_config_mode = ''
        curr_prompt = self.prompt
        curr_prompt = curr_prompt[:-1]

        self.log(level='DEBUG', message='curr config mode = %s, mode = %s, '
                 'curr_mode = %s, config_mode = %s'
                 % (curr_config_mode, mode, curr_mode, config_mode.upper()))
        if mode == curr_mode and config_mode.upper() == curr_config_mode:
            return True

        self.log(level='DEBUG', message='Mode switch required')
        if isinstance(curr_prompt, list):
            curr_prompt = ''.join(curr_prompt)
        elif isinstance(curr_prompt, str):
            curr_prompt = curr_prompt
        cli_prompt = curr_prompt+'>'
        shell_prompt = curr_prompt+'%'
        config_prompt = curr_prompt+'#'

        try:
            if mode == 'CLI':
                if curr_mode == 'SHELL':
                    output = (
                        self.execute(command='cli', pattern='> ') +
                        self.execute(
                            command='set cli prompt ' + cli_prompt,
                            pattern=cli_prompt) +
                        self.execute(
                            command='set cli terminal dumb',
                            pattern=cli_prompt) +
                        self.execute(
                            command='set cli complete-on-space off',
                            pattern=cli_prompt) +
                        self.execute(
                            command='set cli screen-length 50000',
                            pattern=cli_prompt) +
                        self.execute(
                            command='set cli screen-width 500',
                            pattern=cli_prompt))
                elif curr_mode == 'CONFIG':
                    output = self.execute(
                        command='exit configuration-mode', pattern=cli_prompt)
                setattr(self, 'prompt', cli_prompt)
                setattr(self, 'mode', mode)
            elif mode == 'CONFIG':
                config_cmd = 'configure ' + config_mode
                if curr_mode == 'CONFIG' and \
                        config_mode.upper() != curr_config_mode:
                    output = (
                        self.execute(command='exit', pattern=cli_prompt) +
                        self.execute(command=config_cmd, pattern=config_prompt))
                elif curr_mode == 'SHELL':
                    output = (
                        self.execute(command='cli', pattern='> ') +
                        self.execute(command='set cli prompt '+cli_prompt,
                                     pattern=cli_prompt) +
                        self.execute(command='set cli terminal dumb',\
                            pattern=cli_prompt) +
                        self.execute(command='set cli complete-on-space off',\
                            pattern=cli_prompt) +
                        self.execute(command='set cli screen-length 50000',\
                            pattern=cli_prompt) +
                        self.execute(command='set cli screen-width 500',\
			    pattern=cli_prompt) +
                        self.execute(command=config_cmd,\
                            pattern=config_prompt))
                elif curr_mode == 'CLI':
                    output = self.execute(command=config_cmd,
                                          pattern=config_prompt)
                setattr(self, 'prompt', config_prompt)
                setattr(self, 'mode', mode)
                setattr(self, 'config_mode', config_mode)
            elif mode == 'SHELL':
                if curr_mode == 'CLI':
                    output = self.execute(command='exit', pattern=shell_prompt)
                elif curr_mode == 'CONFIG':
                    output = (
                        self.execute(command='exit configuration-mode',
                                     pattern=cli_prompt) +
                        self.execute(command='exit', pattern=shell_prompt))
                setattr(self, 'prompt', shell_prompt)
                setattr(self, 'mode', mode)
            else:
                raise TobyException('Mode:' + mode + ' does not exist.', host_obj=self)

        except:
            raise TobyException('Cannot switch to ' + mode + ' mode.', host_obj=self)

        return True

    def set_prompt_cli(self, prompt):
        """
        Example: device_object.set_prompt_cli(prompt='cli > ')

        Method called by Unix new or user to set device prompt
        :param prompt: prompt to set on the device
        :return: True if set prompt is successful.
                 In all other cases Exception is raised
        """
        self.prompt = prompt
        res = self.channels['text'].execute(
            cmd='set cli prompt {0} '.format(prompt),
            pattern=self.prompt,
            device=self
        )
        if res == -1:
            raise TobyException('Error setting Device prompt', host_obj=self)
        self.mode = 'cli'

        res = self.channels['text'].execute(
            cmd='set cli terminal dumb',
            pattern=self.prompt,
            device=self
        )
        if res == -1:
            self.log(level='ERROR', message="Error setting 'set cli terminal dumb'")

        res = self.channels['text'].execute(
            cmd='set cli complete-on-space off',
            pattern=self.prompt,
            device=self
        )
        if res == -1:
            self.log(level='ERROR', message="Error setting 'set cli complete-on-space off'")

        res = self.channels['text'].execute(
            cmd='set cli screen-length 50000',
            pattern=self.prompt,
            device=self
        )
        if res == -1:
            self.log(level='ERROR', message='set cli screen-length 50000')

        res = self.channels['text'].execute(
            cmd='set cli screen-width 500',
            pattern=self.prompt,
            device=self
        )
        if res == -1:
            self.log(level='ERROR', message="Error setting set cli 'screen-width 500'")
