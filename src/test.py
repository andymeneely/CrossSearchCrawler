import unittest
import parse

class maintests(unittest.TestCase):

    def setUp(self):
        # Real header names example taken from an IEEE CSV file
        self.headerNames = ["Document Title", "Authors", "Author Affiliations", "Publication Title", "Date Added To Xplore", "Year", "Volume", "Issue", "Start Page", "End Page", "Abstract", "ISSN", "ISBN", "EISBN", "DOI", "PDF Link", "Author Keywords", "IEEE Terms", "INSPEC Controlled Terms", "INSPEC Non-Controlled Terms", "MeSH Terms", "Article Citation Count", "Patent Citation Count", "Reference Count", "Copyright Year", "Online Date", "Issue Date", "Meeting Date", "Publisher", "Document Identifier"]

    def test_smoke(self):
        self.assertTrue(True)


    """
    Tests both functions main.validateCSVLine and main.parseCSVLine.

    Occasionally, when there are multiple commas within an entry or
    there were originally quotation marks within an entry, the way
    that the IEEE export citations module works inserts quotation marks
    into entries in a way that messes with a normal CSV parser.

    To solve this problem, main.validateCSVLine was implemented to
    remove any inner quoation marks in entries. By removing these
    quotation marks, a normal CSV parser is able to effectively parse
    the lines of CSV data.

    This test ensures that this functionality is in correct working order.
    """
    def test_validateCSVLine1(self):
        # Actual row taken from an IEEE CSV file
        # This particular line has a special case with quotation mark usage
        row = '"Auditing cloud computing migration","Mateescu, G.; Vladescu, M.; Sgarciu, V.","Dept. of Autom. & Comput. Sci., Univ. "Polyteh." of Bucharest, Bucharest, Romania","Applied Computational Intelligence and Informatics (SACI), 2014 IEEE 9th International Symposium on","20140619","2014","","","263","268","This paper presents a tool used to audit the cloud adoption within a company. The first section states the main advantages of the cloud computing environment together with its biggest challenges that can introduce significant risks within a company. In order to assess properly the cloud computing adoption, we developed a web based tool that assists the internal auditor in the pre-migration process. Section II describes in details the Migration Assessment Tool (MAT). Starting with its architecture, we presented the main objects manipulated by our application in order to implement a cloud adoption assessment. In order to compute the impact, we classified the questions in different domains and we defined the dependencies between the questions. At the end of section II, we presented the process implemented in MAT when assessing a cloud migration. The paper ends with conclusions that state the main benefits of our approach and future improvements for MAT.","","","","10.1109/SACI.2014.6840073","http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=6840073","","Best practices;Cloud computing;Companies;Computational modeling;Computer architecture","auditing;business data processing;cloud computing","MAT;Web based tool;cloud adoption assessment;cloud computing migration auditing;company;internal auditor;migration assessment tool;premigration process","","0","","8","","","15-17 May 2014","","IEEE","IEEE Conference Publications"'
        newRow = parse.validateCSVLine(row)

        # Print statements for comparing the difference between the non-validated and validated CSV rows
        # print()
        # print("Row1: " + row)
        # print("Row2: " + newRow)

        # Parse the validated row
        entry = parse.parseCSVLine(newRow, self.headerNames)

        # Assert that values were placed where they should be
        self.assertTrue(entry['Year'] == '2014')
        self.assertTrue(entry['Document Title'] == "Auditing cloud computing migration")
        self.assertTrue(entry['Authors'] == "Mateescu, G.; Vladescu, M.; Sgarciu, V.")
        self.assertTrue(entry['DOI'] == "10.1109/SACI.2014.6840073")

    """
    This test is doing the same thing as test_validateCSVLine1.
    The only difference is the string value being used for the row.
    The one used here represents a different special case that must
    be handled by the CSV validator.
    """
    def test_validateCSVLine2(self):
        # Actual row taken from an IEEE CSV file
        # This particular line has a special case with quotation mark usage
        row = '"A self-routing protocol for distributed consensus on logical information","Fagiolini, A.; Martini, S.; Di Baccio, D.; Bicchi, A.","Interdept. Res. Center "Enrico Piaggio", Univ. of Pisa, Pisa, Italy","Intelligent Robots and Systems (IROS), 2010 IEEE/RSJ International Conference on","20101203","2010","","","5151","5156","In this paper, we address decision making problems, depending on a set of input events, with networks of dynamic agents that have partial visibility of such events. Previous work by the authors proposed so-called logical consensus approach, by which a network of agents, that can exchange binary values representing their local estimates of the events, is able to reach a unique and consistent decision. The approach therein proposed is based on the construction of an iterative map, whose computation is centralized and guaranteed under suitable conditions on the input visibility and graph connectivity. Under the same conditions, we extend the approach in this work by allowing the construction of a logical linear consensus system that is globally stable in a fully distributed way. The effectiveness of the proposed method is showed through the real implementation of a wireless sensor network as a framework for the surveillance of an urban area.","2153-0858","978-1-4244-6674-0","","10.1109/IROS.2010.5650096","http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=5650096","","","decision making;graph theory;multi-agent systems;multi-robot systems;routing protocols;surveillance;wireless sensor networks","decision making problem;dynamic agents network;iterative map;logical consensus approach;logical linear consensus system;self-routing protocol;wireless sensor network","","0","","20","","","18-22 Oct. 2010","","IEEE","IEEE Conference Publications"'
        newRow = parse.validateCSVLine(row)

        # Print statements for comparing the difference between the non-validated and validated CSV rows
        # print()
        # print("Row1: " + row)
        # print("Row2: " + newRow)

        entry = parse.parseCSVLine(newRow, self.headerNames)

        self.assertTrue(entry['Year'] == '2010')
        self.assertTrue(entry['Document Title'] == "A self-routing protocol for distributed consensus on logical information")
        self.assertTrue(entry['Authors'] == "Fagiolini, A.; Martini, S.; Di Baccio, D.; Bicchi, A.")
        self.assertTrue(entry['DOI'] == "10.1109/IROS.2010.5650096")

    """
    This test is doing the same thing as test_validateCSVLine1.
    The only difference is the string value being used for the row.
    The one used here represents a different special case that must
    be handled by the CSV validator.
    """
    def test_validateCSVLine3(self):
        # Actual row taken from an IEEE CSV file
        # This particular line has a special case with quotation mark usage
        row = 'A Weight-Based Symptom Correlation Approach to SQL Injection Attacks,"Ficco, M.; Coppolino, Luigi; Romano, L.","Lab. ITeM C. Savy""", Consorzio Interuniversitario Naz. per l\'\'lnformatica (CINI), Naples," Italy""","Dependable Computing, 2009. LADC \'09. Fourth Latin-American Symposium on",20090911,2009,,,9,16,"Web applications are vulnerable to a variety of new security threats. SQL injection attacks (SQLIAs) are one of the most significant of such threats. Researchers have proposed a wide variety of anomaly detection techniques to address SQLIAs, but all existing solutions have limitations in terms of effectiveness and practicality. %In particular, We claim that the main cause of such limitations is reliance on a single detection model and/or on information generated by a single source. Correlation of information from diverse sources has been proven to be an effective approach for improving detection performance, i.e. reducing both the rate of false positives and the percentage of undetected intrusions. In order to do so, we collect symptoms of attacks against web-based applications at different architectural layers, and correlate them via a systematic approach that applies a number of different anomaly detection models to combine data from multiple feeds, which are located in different locations within the system, and convey information which is diverse in nature. Preliminary experimental results show that, by rearranging alerts based on knowledge about the ability of individual security probes of spotting a specific malicious action, the proposed approach does indeed reduce false positives rates and increase the detection coverage.",,978-1-4244-4678-0,978-0-7695-3760-3,10.1109/LADC.2009.14,http://ieeexplore.ieee.org.ezproxy.rit.edu/stamp/stamp.jsp?arnumber=5234325,Anomaly Detection;Correlation;Information Diversity;Intrusion Detection;SQL Injection Attacks,Cryptography;Data security;Encapsulation;Encoding;Feeds;Information resources;Information security;Intrusion detection;Laboratories;Probes,security of data,Web applications;false positives;individual security probes;security threats;single detection model;specific malicious action;symptom correlation approach;undetected intrusions;weight-based symptom correlation approach,,3,,24,,,1-4 Sept. 2009,,IEEE,IEEE Conference Publications'
        newRow = parse.validateCSVLine(row)

        # Print statements for comparing the difference between the non-validated and validated CSV rows
        # print()
        # print("Row1: " + row)
        # print("Row2: " + newRow)

        entry = parse.parseCSVLine(newRow, self.headerNames)

        self.assertTrue(entry['Year'] == '2009')
        self.assertTrue(entry['Document Title'] == "A Weight-Based Symptom Correlation Approach to SQL Injection Attacks")
        self.assertTrue(entry['Authors'] == "Ficco, M.; Coppolino, Luigi; Romano, L.")
        self.assertTrue(entry['DOI'] == "10.1109/LADC.2009.14")

    """
    This test is doing the same thing as test_validateCSVLine1.
    The only difference is the string value being used for the row.
    The one used here represents a different special case that must
    be handled by the CSV validator.
    """
    def test_validateCSVLine4(self):
        # Actual row taken from an IEEE CSV file
        # This particular line has a special case with quotation mark usage
        row = 'Wireless Intrusion Detection System Using a Lightweight Agent,"Haddadi, F.; Sarram, M.A.","Electr. & Comput. Eng. Dept., Yazd Univ., Yazd, Iran","Computer and Network Technology (ICCNT), 2010 Second International Conference on",20100601,2010,,,84,87,"The exponential growth in wireless network faults, vulnerabilities, and attacks make the Wireless Local Area Network (WLAN) security management a challenging research area. Deficiencies of security methods like cryptography (e.g. WEP) and firewalls, causes the use of more complex security systems, such as Intrusion Detection Systems, to be crucial. In this paper, we present a hybrid wireless intrusion detection system (WIDS). To implement the WIDS, we designed a simple lightweight agent. The proposed agent detect the most destroying and serious attacks; Man-In-The-Middle and Denial-of-Service; with the minimum selected feature set. To evaluate our proposed WIDS and its agent, we collect a complete data-set using open source attack generator softwares. Experimental results show that in comparison with similar systems, in addition of more simplicity, our WIDS provides high performance and precision.",,978-0-7695-4042-9,978-1-4244-6962-8,10.1109/ICCNT.2010.26,http://ieeexplore.ieee.org.ezproxy.rit.edu/stamp/stamp.jsp?arnumber=5474532,Intrusion detection system;Security;Wireless Local Area Network;Wireless network attacks,Communication system security;Computer crime;Computer networks;Computer security;Cryptography;Intrusion detection;Telecommunication traffic;Traffic control;Wireless LAN;Wireless networks,computer network security;cryptography;wireless LAN,cryptography;denial-of-service;firewalls;lightweight agent;man-in-the-middle;open source attack generator softwares;wireless intrusion detection system;wireless local area network security management;wireless network faults,,2,,15,,,23-25 April 2010,,IEEE,IEEE Conference Publications,,,'
        newRow = parse.validateCSVLine(row)

        # Print statements for comparing the difference between the non-validated and validated CSV rows
        # print()
        # print("Row1: " + row)
        # print("Row2: " + newRow)

        entry = parse.parseCSVLine(newRow, self.headerNames)

        self.assertTrue(entry['Year'] == '2010')
        self.assertTrue(entry['Document Title'] == "Wireless Intrusion Detection System Using a Lightweight Agent")
        self.assertTrue(entry['Authors'] == "Haddadi, F.; Sarram, M.A.")
        self.assertTrue(entry['DOI'] == "10.1109/ICCNT.2010.26")
