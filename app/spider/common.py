"""
author songjie
"""
from config import settings


class GenerateUrl(object):
    def generate_url(self, domian="", suffix="", params=None, is_generate=True, module=1):
        """
        :param is_generate:
        :param domian:
        :param suffix:
        :param params: a dict, key is keyword, value is a value which will be send
        :return:
        """
        if not is_generate:
            return domian
        if domian == "":
            url = settings.DOMAIN
        else:
            url = domian
        url = url + suffix
        if not params:
            return url
        url = self.__spell_param(url, params, module)
        return url

    def __spell_param(self, url, params, module):
        """
        spell param
        :param url:
        :param params:
        :param module:
        :return:
        """
        param = ""
        flag = 0
        for k, v in params:
            param, flag = self.__generate_url(param, k, v, flag, module=module)
        url = url + param
        return url

    @classmethod
    def __generate_url(cls, param, k, v, flag=0, module=1):
        if module == 1:
            if flag == 0:
                param = param + "?" + k + "=" + str(v)
                flag = flag + 1
            else:
                param = param + "&" + k + "=" + str(v)
        else:
            param = param + "/" + str(v)
        return param, flag
