# -*- coding: utf-8 -*-
#!/usr/bin/python
#
# Copyright (C) 2012 eEcho.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""

Command to find urls op vacatures sites


"""

__author__ = 'sergej[A]dergatsjev[D]be (Sergej Dergatsjev)'

from django.db import models, IntegrityError, DatabaseError
from django.core.management.base import BaseCommand

from permanentjob.models import Category
import sys, traceback


class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        Entery point
        """
        cats = {"18002000": "Brandweer", "15002003": "Schoonmaakpersoneel", "12006000": "Andere: juridisch", "3005003": "Project Management", "3005002": "Onroerend goed & facility management", "3005001": "Andere: Banken, financi\u00eble diensten en verzekeringen", "9001000": "Schilderwerk, stukadoorswerk", "5007003": "Uitzendconsulent/e", "5007002": "HR consultancy", "5007001": "Andere: HR", "1015000": "IT-training", "1003000": "Application Development & Programming", "14005000": "Sociaal, jeugd en gemeenschapswerk", "7001000": "Secretariaat", "18003000": "Leger", "14001000": "Arts, tandheelkunde, farmacie", "16001000": "Landbouw, visserij en tuinbouw", "14004000": "Medisch onderzoek en laboratoriumwetenschappen", "10011000": "CAD Construction / Visualizing", "6010000": "Trade marketing", "2004000": "Klantendienst", "4000000": "Financi\u00ebn, administratie & accounting", "11005000": "Business Consulting", "8005000": "Andere: transport en logistiek", "6008000": "Media planning & Purchasing", "10007000": "Chemie", "6005000": "Marktonderzoek & -analyse", "1007000": "Helpdesk & Technical Support", "11001000": "Directie en raad van bestuur", "19004000": "Andere: media en informatie", "4001000": "Auditing", "21002004": "Binnenhuisarchitectuur", "22001000": "Kleuteronderwijs", "21002001": "Illustratie en grafisch ontwerp", "21002003": "Mode en kledingontwerp", "21002002": "Industrieel ontwerp", "20001001": "Museum en galerij", "22002000": "Lager onderwijs", "15003000": "Reizen & toerisme", "11006001": "Andere: general management", "10001000": "Procestechniek", "6006000": "Public- & investor relations", "3000000": "Banken, financi\u00eble diensten en verzekeringen", "20001003": "Muziek, dans en theater", "9006000": "Voedselbereiding", "20001002": "Geschiedenis en archeologie", "2000000": "Verkoop en inkoop", "5004000": "HR management", "14000000": "Gezondheidszorg, sociale- en medische diensten", "20002001": "Fotografie", "20002002": "Kunst", "17000000": "Overheidsdiensten", "13001002": "Biotechnologie", "1004000": "Applications Administration", "20003000": "Andere: cultuur en kunst", "7004000": "Management assistentie", "12001000": "Advocatuur", "6002000": "Product management", "2006000": "Sales support en -administratie", "1012000": "IT-Consulting", "8003004": "Haven, zeetransport en binnenvaart", "8003002": "Baantransport", "8003003": "Spoortransport", "8003001": "Luchttransport", "1002000": "Application Analysis", "16004000": "Andere: land, zee, milieu en natuurbehoud", "6009000": "Sales Support", "16003001": "Leefmilieu en natuurbehoud", "16003002": "Afvalmanagement", "8002000": "Transport-, logistiek management", "5000000": "HR", "13001001": "Chemie, fysica en biologie", "21001002": "Landschaps- en tuinarchitectuur", "7000000": "Administratieve ondersteuning & secretariaat", "4006000": "Belastingadvies", "11006002": "Partner", "17005000": "Belastingdienst", "20001004": "Bibliotheek", "12003000": "Assistentie notaris/gerechtshof", "9005000": "Arbeider/bouw", "10003000": "Elektronica", "1018000": "IT-Architecture", "6012000": "Marketing Assistent", "5006000": "Aanwerving & selectie", "3003001": "Makelarij", "12000000": "Juridisch", "3003002": "Beurshandel", "2005002": "Winkel bediening", "16000000": "Land, zee, milieu en natuurbehoud", "14007000": "Andere: gezondheidszorg, sociale- en medische diensten", "2005001": "Retail management, Filiaalhouding", "1006001": "Network Operations & Maintenance", "1006002": "Network Administration & Security", "4008000": "Andere: Financi\u00ebn, administratie & accounting", "9011000": "Quality assurance/Milieu co\u00f6rdinator/Preventieadviseur", "8006000": "Supply Chain Management", "15000000": "Horeca, toerisme", "9003004": "Materieel", "9003003": "Mechaniek", "9003002": "Laswerk", "9003001": "Loodgieterij", "2002000": "Sales Management", "1013000": "Andere: IT & Telecommunicatie", "18001000": "Politie, gevangenis en aanverwant werk", "19000000": "Media en informatie", "17001000": "Ambassades en diplomatencorps", "5003000": "HR administratie", "2008000": "Andere: Verkoop en inkoop", "13002000": "Wiskunde, statistiek en informatica", "14003000": "Verpleging, medische hulp en -hulpdiensten", "10000000": "Engineering & techniek", "18005000": "Andere: veiligheid en beveiliging", "7006000": "Klerk", "4004000": "Controlling", "2003003": "Commerci\u00eble vertegenwoordiging", "2001000": "Callcenter & telefonische verkoop", "6011000": "Andere: marketing, reclame & communicatie", "21001001": "Architectuur", "4007000": "Financial consultancy", "3004000": "Verzekeringen en schadebeheer", "6000000": "Marketing, reclame & communicatie", "12005000": "Notariaat", "1006003": "Telecommunication & Mobile Systems", "21000000": "Ontwerp en architectuur", "7007000": "Vertalingen", "6003000": "Database- & direct marketing", "1009000": "IT-Project Management", "10005000": "Materiaalkunde", "9000000": "Productie, constructie en handvaardigheid", "1016000": "Systeemadministratie / Management", "22003000": "Middelbaar onderwijs", "5005000": "Training & development", "13000000": "R&D, wetenschap en wetenschappelijk onderzoek", "1001000": "Hardware Design & Engineering", "9007000": "Persoonlijke verzorging", "19002000": "Uitgeverij", "16002000": "Veterinaire wetenschap, dierenwelzijn", "10010002": "Biotechnologie", "10010003": "Productie & operationeel management", "7002000": "Office management", "10010001": "Andere: engineering & techniek", "6004000": "Event marketing", "10010004": "Onderhoud & productie", "10010005": "Project Management", "7003000": "Receptie, telefonie", "1010000": "Webdesign & Webmaster", "10009000": "Techniek", "17006000": "Douane", "17004000": "Lokale overheid", "10008000": "Technisch consultancy", "4002000": "Accountancy, boekhouding", "11004000": "Operations Management", "6007000": "Advertising/Communication management", "10006000": "Bouwkunde, werktuigbouwkunde", "11002000": "General Management", "18000000": "Politie, Veiligheid en Beveiliging", "19001000": "Journalistiek", "13003003": "Laboratoriumwerk", "8000000": "Transport en logistiek", "2003001": "(Key) account Management", "2003002": "Buitendienst", "1014000": "Informatica", "4005000": "Financieel management", "17007000": "Andere: overheidsdiensten", "15004002": "Andere: Horeca & Toerisme", "15004001": "Receptie", "14002000": "Optiek & akoestiek", "9008000": "Industri\u00eble fabricage & productie", "5002000": "Payroll", "17002000": "Ambtenarij buitenlandse zaken", "13003001": "Research en development", "11000000": "General Management", "13003002": "Quality Assurance", "9002001": "Schrijnwerk", "9002002": "Timmerman", "22004000": "Hoger en universitair onderwijs", "8004000": "Postbezorging & koerierdiensten", "13004000": "Andere: R&D, wetenschap en wetenschappelijk onderzoek", "3001000": "Analyse, compliance & consultancy", "9009001": "Andere: productie, constructie en handvaardigheid", "15002001": "Zaalpersoneel", "9009003": "Calculator", "9009002": "Werfsupervisie & projectleider", "12004000": "Gerechtelijke administratie", "1000000": "IT en Telecommunicatie", "17003000": "Ambtenarij federale zaken", "14006000": "Sport & fitness, paramedisch", "1017000": "Redactietechnieken", "20000000": "Cultuur en kunst", "18004000": "Beveiliging en bescherming", "22005000": "Gespecialiseerde opleidingen", "2007001": "Purchasing Management", "2007002": "Purchaser", "11003000": "Business Development", "21003000": "Andere: ontwerp en architectuur", "12002000": "Bedrijfsjuridische dienst", "6001000": "Marketing management", "22000000": "Opleiding en training", "22006000": "Andere: opleiding en training", "1011000": "IT-Quality Assurance & Inspection", "1008000": "IT Management", "19003000": "Film, TV, radio & multimedia", "10004002": "Elektromechanica", "10004001": "Mechanica", "7008000": "Andere: administratieve ondersteuning & secretariaat", "4003000": "Cash management & treasury", "1005001": "Database Administration", "8001000": "Magazijnbeheer", "5001000": "Compensation & benefits", "3002000": "Banking", "10002000": "Elektrotechniek", "15001000": "Horeca management", "9004000": "Elektricien", "1005002": "Data Processing", "1019000": "Product Manager/ Functional of Business Analyst", "15002002": "Keukenpersoneel", "1005003": "Data Warehousing", "7005000": "Archief"
                }
        for id, cat in cats.items():
            newcat = Category()
            newcat.name = cat
            newcat.stepstone_id = id
            newcat.save()
            
        
