#-*- coding: utf-8 -*- 

from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.packer import cPacker
from resources.lib.comaddon import dialog, VSlog

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vod540', 'Vod540')

    def setUrl(self, url):
        self._url = str(url)

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        sReferer = ""
        url = self._url
        sReferer = self._url.split('dl')[0]
        
        oRequest = cRequestHandler(url)
        oRequest.addHeaderEntry('user-agent',UA)
        oRequest.addHeaderEntry('Referer',sReferer)
        sHtmlContent = oRequest.request()

        
        oParser = cParser()
        
        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        if aResult[0]:
            sHtmlContent = cPacker().unpack(aResult[1][0])
        
            # (.+?) .+?
        sPattern = 'file:"(.+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        api_call = False

        if aResult[0]:
            api_call = aResult[1][0]
 
            if api_call:
                return True, api_call + '|User-Agent=' + UA + '&Referer=' + sReferer

        sPattern = '<source src="(.+?)" type='
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        api_call = False

        if aResult[0]:
            api_call = aResult[1][0]
 
            if api_call:
                return True, api_call + '|User-Agent=' + UA + '&Referer=' + sReferer


        sPattern = 'file:.+?"(.+?)",.+?label: "(.+?)",'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        api_call = False

        if aResult[0]:
            
            #initialisation des tableaux
            url=[]
            qua=[]
            
            #Replissage des tableaux
            for i in aResult[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))
            api_call = dialog().VSselectqual(qua, url)
 
            if api_call:
                return True, api_call  + '|User-Agent=' + UA + '&Referer=' + sReferer

        return False, False