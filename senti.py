# -*- coding: utf-8 -*-
import csv


class SentimentAnalysisService():
    rating=10
    NEGATIONS_WORDS = ["aint", "arent", "cannot", "cant", "couldnt", "darent", "didnt", "doesnt",
                     "ain't", "aren't", "can't", "couldn't", "daren't", "didn't", "doesn't",
                     "dont", "hadnt", "hasnt", "havent", "isnt", "mightnt", "mustnt", "neither",
                     "don't", "hadn't", "hasn't", "haven't", "isn't", "mightn't", "mustn't",
                     "neednt", "needn't", "never", "none", "nope", "nor", "not", "nothing", "nowhere",
                     "oughtnt", "shant", "shouldnt", "uhuh", "wasnt", "werent",
                     "oughtn't", "shan't", "shouldn't", "wasn't", "weren't",
                     "without", "wont", "wouldnt", "won't", "wouldn't", "rarely", "seldom", "despite"]

    def __init__(self):
        with open('stopWords.csv', 'r') as f:
            reader = csv.reader(f)
            inp2 = list(reader)
            self.StopWord = inp2[0] #index is number of row

        self.WordsDict = {} #dictionary word - score
        with open('Positive.csv', 'r') as f:
            reader = csv.reader(f)
            WordList = list(reader)

        for a in WordList: #iterate in list and add positive words
            self.WordsDict[str(a[0]).lower()] = (1.0,)

        with open('Negative.csv', 'r') as f:
            reader = csv.reader(f)
            WordList = list(reader)

        for row in WordList: #add negative words to dict
            self.WordsDict[str(row[0]).lower()] = (-1.0,)

        with open('nouns.csv', 'r') as f:
            reader = csv.reader(f)
            inp = list(reader)
        self.Nouns = inp[0]

    def solve(self, rev):
        FeatureDict = {}
        avg = 0
        cnt = 0
        # Fptr : Feature detected with index
        # Adjptr: Adjective detected with polarity and index

        for sentence in rev.split('.'): #get sentences from text
            Fptr = []
            AdjPtr = []
            if sentence == '':
                continue
            arr = sentence.split(' ') #get word from sentence
            i = 0
            direction = +1
            for cstr in arr: #for every word
                i += 1
                p = str(cstr).lower()
                if p in self.NEGATIONS_WORDS:
                    direction = -direction
                    continue
                if p in self.StopWord:
                    continue
                if p == "but":
                    direction = +1
                    continue
                elif p in self.Nouns:
                    Fptr.append((p, i))
                    if p not in FeatureDict.keys():
                        FeatureDict[p] = 0.0
                        if p in self.WordsDict.keys():
                            FeatureDict[p] = self.WordsDict[p][0] * 0.1
                elif p in self.WordsDict.keys():
                    x = self.WordsDict[p][0]
                    if x > 0.125 or x < -0.125:
                        AdjPtr.append((p, direction * self.WordsDict[p][0], i))
                        # print AdjPtr

                        # Pairing Adjectives and Nouns by computing distance.
                        # The adjective and noun with minimum distance between them will be paired.

            for i in range(len(AdjPtr)):
                dist = 1000000007
                feat = ""
                for j in range(len(Fptr)):
                    if abs(AdjPtr[i][2] - Fptr[j][1]) < dist:
                        dist = abs(AdjPtr[i][2] - Fptr[j][1])
                        feat = Fptr[j][0]
                if feat != '':
                    FeatureDict[feat] += AdjPtr[i][1]
                avg += AdjPtr[i][1]
                cnt += 1
                # test.append(AdjPtr[i][1])
                # print feat + " - " + AdjPtr[i][0] + " || " ,(AdjPtr[i][1])


                # print FeatureDict

                # Computing the Score

        avg /= max(cnt, 1)

        # nscore = (x - minscore)/(maxscore - minscore)
        # handle rating part( thats left for computing the score)
        # If score > 2.5 , sentiment = Positive else sentiment = Negative

        normalizedscore = ((avg + 1) / 2) * 5

        # Taking 30% rating and 70% Score computed
        if self.rating >= 0:
            fscore = normalizedscore * 0.7 + 0.3 * self.rating
        else:
            fscore = normalizedscore * 1.0


        FinanceList = []
        LogisticsList = []
        QualityList = []

        LogisticsDept = ["slow", "behind", "belated", "blown", "delayed", "dilatory", "eleventh-hour", "gone", "jammed",
                         "lagging", "overdue", "postponed", "remiss", "stayed", "tardy", "late", "unpunctual",
                         "aboriginal", "antecedent", "antediluvian", "antiquated", "preceding", "premier", "prevenient",
                         "primal", "prime", "primitive", "primordial", "prior", "pristine", "proleptical", "raw",
                         "undeveloped", "gradual", "heavy", "lackadaisical", "leisurely", "lethargic", "moderate",
                         "passive", "quiet", "reluctant", "sluggish", "stagnant", "crawling", "creeping", "dawdling",
                         "delaying", "deliberate", "disinclined", "idle", "lagging", "loitering", "measured",
                         "plodding", "postponing", "procrastinating", "slack", "apathetic", "dilatory", "dreamy",
                         "drowsy", "imperceptible", "inactive", "indolent", "leaden", "negligent", "slow-moving",
                         "snaillike", "torpid", "tortoiselike"]

        FinanceDept = ["costly", "extravagant", "high", "lavish", "overpriced", "pricey", "valuable", "excessive",
                       "exorbitant", "immoderate", "inordinate", "invaluable", "posh", "rich", "swank", "uneconomical",
                       "unreasonable", "economical", "reasonable", "worthless", "cheap", "inexpensive", "moderate",
                       "agile", "nimble", "accelerated", "electric", "flashing", "flying", "snap", "winged",
                       "breakneck", "highprice", "price", "priced", "cost"]

        QualityDept = ["complicated", "confusing", "flawed", "imprecise", "inaccurate", "incomplete", "incorrect",
                       "useful", "not ", "pointless", "ugly", "unfinished", "unreliable", "useless", "appropriate",
                       "attractive", "convenient", "faultless", "flawless", "free of error", "handy", "helpful ",
                       "practical", "precise", "quality", "useful ", "acceptable", "bad", "excellent", "exceptional",
                       "favorable", "great", "marvelous", "positive", "satisfactory", "satisfying", "superb",
                       "valuable", "wonderful", "ace", "boss", "bully", "capital", "choice", "crack", "nice",
                       "pleasing", "prime", "rad", "sound", "spanking", "sterling", "super", "superior", "welcome",
                       "worthy", "admirable", "agreeable", "commendable", "congenial", "deluxe", "first-class",
                       "first-rate", "gratifying", "honorable", "neat", "precious", "reputable", "select", "shipshape",
                       "splendid", "stupendous", "poor", "dreadful", "atrocious", "cheap", "unacceptable", "sad",
                       "lousy", "crummy", "awful", "rough", "synthetic", "gross", "imperfect", "bummer", "garbage",
                       "blah", "diddly", "inferior", "downer", "abominable", "amiss", "bad news", "beastly", "careless",
                       "cheesy", "crappy", "defective", "deficient", "satisfactory", "erroneous", "fallacious",
                       "faulty", "grungy", "icky", "inadequate", "incorrect", "off", "raunchy", "slipshod", "stinking",
                       "substandard", "unsatisfactory", "junky", "bottom out", "not good"]

        # Initializing the Lists
        FinanceList.append(0)
        LogisticsList.append(0)
        QualityList.append(0)

        a = rev
        v = a.split('.')
        # print "V " ,v
        S = 0
        for sentence in v:
            S = S + 1
            z = sentence.split(' ')
            # print z,S
            for c in z:
                c = c.lower()
                if c in FinanceDept and S not in FinanceList:
                    FinanceList.append(S)
                if c in LogisticsDept and S not in LogisticsList:
                    LogisticsList.append(S)
                if c in QualityDept and S not in QualityList:
                    QualityList.append(S)

        return fscore
print (SentimentAnalysisService().solve(''' There is so much hype about alt-coins lately that there are now reports of people even taking out second mortgages and home equity lines to buy them. The volatility is so great that the Chicago Board Options Exchange (CBOE) halted bitcoin trading twice on Dec. 10 and once again on Dec. 13, and Coinbase halted litecoin and ethereum trading on Dec. 12.

For years, financial analysts have warned people away from cryptocurrency by arguing that it was too volatile to be a safe investment. However, with prices going sky-high, it's hard for investors and entrepreneurs to sit on the sidelines while a major new asset class emerges.

However, before people take the plunge, they need to understand the risks. The cryptocurrency markets aren't just volatile, they are also extremely murky and riddled with fraud. Since the launch of bitcoin in 2009, these markets have been plagued with cyber attacks and scams that have cost investors millions of dollars. To make matters worse, cryptocurrency isn't protected by the FDIC, so losses due to theft may not be covered.

Related: 5 Essential Podcasts for Entrepreneurs Serious About Cryptocurrency

There are two main ways cryptocurrency investors can lose their shirts to scammers.

The first is when hackers attack the infrastructure underpinning these coin markets (ex: exchanges, digital wallets, mining companies, web host services, etc.). Reuters estimates that 980,000 bitcoins have been stolen from cryptocurrency exchanges since 2011, the equivalent of $15 billion to $18 billion at current prices. Recent examples of this include the NiceHash hack in December, which lost $64 million in investors' money; also, in November, Tether was hacked for $30 million; and someone exploited a software bug in Parity to freeze $160 million in investors' accounts. And let's not forget the massive Mt. Gox hack in 2014 -- $460 million was lost as a result.

The second is when criminals target investors directly. There are a variety of these online scams, which often use "social engineering" tactics, but the primary ones to worry about are initial coin offering (ICO) fraud, phone-porting, fake wallets and malware.

While there is not much investors can do to protect themselves against attacks on the cryptocurrency system, they can take measures to lower their own risk of falling for a targeted attack.

Related: 6 Cryptocurrencies You Should Know About (and None of Them Are Bitcoin)

Here is a breakdown of these four attacks and ways to reduce the threat:

Initial Coin Offering (ICO) fraud
An ICO is when a newly invented cryptocurrency is launched to investors. Needless to say, this is an unregulated and risky activity all by itself, but it is also plagued by scammers.

There are two ways ICO fraud happens. The first is when criminals create a fake ICO and steal any money that investors give them. This is what happened in December, when the SEC shut down the PlexCoin ICO, which it alleges was a $15 million fraud.

The second type of ICO fraud is when hackers "spoof," or impersonate, a legitimate ICO and trick investors into paying them instead of the real company. This happened recently with messaging giant Kik's ICO, which goes to show it can affect even well-established companies. Typically, cybercriminals will create a fake website or social media account and use phishing emails to promote a phony "pre-sale" offer or other trick. Chainalysis recently estimated that ICO spoofing has victimized 30,000 investors this year alone, to the tune of $225 million.

Related: Why You Can't Afford to Ignore Cryptocurrencies and Blockchain Anymore

Security tip: Do sufficient research on an ICO before buying in. Check industry sites like CoinDesk to verify the legitimacy of a claimed ICO. Don't fall for hard sell tactics or too-good-to-be-true offers, especially when received over email or social media messaging, as these are likely phishing attempts. See the SEC's tips on ICO investments.

Phone-porting
Cell phone identity theft, also known as "phone-porting," is when criminals commandeer a person's phone number by tricking the mobile provider into giving them control of the account. Once they have the phone number, they can reset the password to a digital wallet and drain the account. Since these cryptocurrency transactions can't be reversed, the investor can lose everything. According to Federal Trade Commission statistics, phone-porting attacks in general rose by 256 percent between 2013 and 2016.

Security tip: Mobile providers usually recommend adding a unique PIN and verification question to the account to improve security. However, a better solution is to switch two-factor authentication from SMS to a third-party service like Google Authenticator.

Related: How Digital Wallets and Mobile Payments Are Evolving and What It Means for You

Fake digital wallets
Cryptocurrency has to be stored somewhere, and investors often use virtual wallets. The problem is that fake wallets occasionally appear online or in mobile app stores, and they may steal investors' savings. This happened recently with the bitcoin gold wallet scam, which reportedly stole $3 million. On Dec. 10, the popular service MyEtherWallet warned customers about a fake MyEtherWallet digital wallet app, which had risen to No. 3 in the iOS App Store's finance category.

Security tip: Before selecting a digital wallet provider, do your homework. Only use services that have a solid track record. Another option is to use an offline hardware wallet.

Bitcoin-stealing malware
It's estimated that nearly one-third of all home computers are infected with some type of malware. Recently, a new category of malware has emerged that specializes in one activity -- stealing bitcoins. It can do this in a few different ways, such as stealing log-in credentials or the wallet itself, or getting in the middle of a transaction. Dell SecureWorks estimates this malware increased 11-fold between 2012 and 2014.

Security tip: Use a robust antivirus program and an inbound/outbound firewall to protect your computer. Use two-factor authentication and a password manager to protect the log-in.

Cryptocurrency investors face a lot of risks, not the least of which is scamming. Since this market is largely unregulated and unprotected, it is up to individual investors to account for their own security. Follow the above tips, and also take additional measures, such as encrypting the internet connection with a VPN (virtual private network). It's also not a bad idea to consider using a dedicated computer (i.e., it does nothing else but log in to your bitcoin account) to be safer when performing these transactions.

Related Video: The Risks of Starting a Bitcoin-Based Business'''))
