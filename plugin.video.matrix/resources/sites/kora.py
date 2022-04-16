﻿#-*- coding: utf-8 -*-
#zombi https://github.com/zombiB/zombi-addons/
import base64
import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress ,VSlog, siteManager
from resources.lib.parser import cParser
 
SITE_IDENTIFIER = 'kora'
SITE_NAME = 'kora'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

SPORT_LIVE = ('https://www.s-kora.com/', 'showMovies')

FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Search', 'search.png', oOutputParameterHandler)
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_LIVE[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'بث مباشر', 'sport.png', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText is not False:
        sUrl = ''+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
   
def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
 
# ([^<]+) .+? (.+?)

    sPattern = '<a title="(.+?)" id="match-live" href="(.+?)">'



    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle =  aEntry[0] 
            sThumbnail = ""
            siteUrl = aEntry[1]
            if siteUrl.startswith('//'):
                siteUrl = 'https:' + aEntry[1]
            sInfo = ''
			
			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            oGui.addMisc(SITE_IDENTIFIER, 'showLive', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
    if not sSearch:
        oGui.setEndOfDirectory()
  
def showLive():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    # (.+?) # ([^<]+) .+? 
    sPattern = "setURL([^<]+)'>([^<]+)</button>"
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    VSlog(aResult)

    #print aResult
   
    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
 
            sTitle = aEntry[1]
            siteUrl = aEntry[0].replace('")',"").replace('("',"")
            sInfo = "" 
			
			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler) 
			
    oGui.setEndOfDirectory()
  
def showHosters():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
    

    sPattern = ' var servers(.+?)</script>'
    data = re.findall(sPattern, sHtmlContent)
    VSlog(data)
    # (.+?) # ([^<]+) .+? 
    sPattern = '"(.+?)"'
    aResult = oParser.parse(data, sPattern)
    VSlog(aResult)
    if aResult[0] is True:
       for aEntry in aResult[1]:
           url = aEntry
           oRequestHandler = cRequestHandler(url)
           sHtmlContent = oRequestHandler.request()
           sPattern =  "source: '(.+?)',"
           aResult = oParser.parse(sHtmlContent,sPattern)
           if aResult[0] is True:
               murl = aResult[1][0]
               sHosterUrl = murl+ '|User-Agent=Android' +'&origin=https://serverlivehd7.blogspot.com' 
               oHoster = cHosterGui().checkHoster(sHosterUrl)
               if oHoster != False:
                   oHoster.setDisplayName(sMovieTitle)
                   oHoster.setFileName(sMovieTitle)
                   cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
           sPattern =  'src="(.+?)"'
           aResult = oParser.parse(sHtmlContent,sPattern)
           if aResult[0] is True:
               murl = aResult[1][0]
               sHosterUrl = murl+ '|User-Agent=Android' +'&origin=https://serverlivehd7.blogspot.com' 
               oHoster = cHosterGui().checkHoster(sHosterUrl)
               if oHoster != False:
                   oHoster.setDisplayName(sMovieTitle)
                   oHoster.setFileName(sMovieTitle)
                   cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
    # (.+?) # ([^<]+) .+? 
    sPattern = 'href="([^<]+)">([^<]+)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
       for aEntry in aResult[1]:
           url = aEntry[0]
           oRequestHandler = cRequestHandler(url)
           sHtmlContent = oRequestHandler.request()
           sPattern =  'src="(.+?)"'
           aResult = oParser.parse(sHtmlContent,sPattern)
           if aResult[0] is True:
              url = aResult[1][0]
              oRequestHandler = cRequestHandler(url)
              sHtmlContent = oRequestHandler.request()
              sPattern =  'src="(.+?)"'
              aResult = oParser.parse(sHtmlContent,sPattern)
              if aResult[0] is True:
                 murl = aResult[1][0]
                 sHosterUrl = murl+ '|User-Agent=Android' +'&origin=https://serverlivehd7.blogspot.com' 
                 sMovieTitle = sMovieTitle
                 oHoster = cHosterGui().checkHoster(sHosterUrl)
                 if oHoster != False:
                     oHoster.setDisplayName(sMovieTitle)
                     oHoster.setFileName(sMovieTitle)
                     cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
              sPattern =  "source = '(.+?)'"
              aResult = oParser.parse(sHtmlContent,sPattern)
              if aResult[0] is True:
                 murl = aResult[1][0]
                 sHosterUrl = murl+ '|User-Agent=Android'+'&origin=https://serverlivehd7.blogspot.com'
                 sMovieTitle = sMovieTitle
                 oHoster = cHosterGui().checkHoster(sHosterUrl)
                 if oHoster != False:
                     oHoster.setDisplayName(sMovieTitle)
                     oHoster.setFileName(sMovieTitle)
                     cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

                
    oGui.setEndOfDirectory()