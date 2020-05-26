import re
class Response(object):
    def __init__(self, **kwargs):
        """
        Creates response object
        """
        self.resp = kwargs.get('response')
        self.stat = kwargs.get('status')

    def response(self):
        """
        returns command resonse
        """
        return self.resp

    def status(self):
        """
        returns command status
        """
        return self.stat

    def __bool__(self):
        return self.stat

    def __nonzero__(self):
        return self.__bool__()

    def __eq__(self, other):
        """
        Over write __eq__ method
        """
        if isinstance(other, bool):
            return other == self.stat
        elif isinstance(other, str):
            return other == self.resp
        return None

def response_check(self, response, mode):
    """
    DESCRIPTION:
       'response_check' is to parse device response for set of patterns
       based on junos mode passed and returs command status.
    ARGUMENTS:
        :param OBJECT device:
            *MANDATORY* Device handle on which the commands are executed
        :param STR response:
            *MANDATORY* command response to parase
        :param STR mode:
            *MANDATORY* junos mode where the command executed
        Returns:
           Returns True/False
    """
    command_status = True
    if hasattr(self, 'response_instructions'):
        status = self.response_instructions['junos'][mode]['status']
        instruct_patterns = self.response_instructions['junos'][mode]['patterns']
        if not status:
            reg_lst = []
            for raw_regex in instruct_patterns:
                reg_lst.append(re.compile(raw_regex))
            for regex in reg_lst:
                if regex.search(response):
                    command_status = False
                    self.log(level="INFO", message="Device response matched instruction patterns: %s" % str(instruct_patterns))
    return command_status
