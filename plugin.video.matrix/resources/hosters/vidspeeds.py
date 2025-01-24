﻿#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import VSlog
from resources.hosters.hoster import iHoster
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidspeeds', 'vidspeeds')

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        sReferer = self._url
        
        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('user-agent',UA)
        oRequest.addHeaderEntry('Referer',sReferer)
        sHtmlContent = oRequest.request()
        
        oParser = cParser()
        
            # (.+?) .+?
        sPattern = 'file:"(.+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        api_call = False

        if (aResult[0] == True):
            api_call = aResult[1][0]
            VSlog(api_call)

            if (api_call):
                return True, api_call + '|User-Agent=' + UA
        return False, False
        
