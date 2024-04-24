import re
import unicodedata
import spacy

class Feature_getter:

    def __init__(self, language = "esp", bigram = True, trigram = True, morphology = True, length = True, prefix = True,
                 lemma = True, POS = True, shape = True, gazetteers = False):
        
        # Options initailization
        self.morphology = morphology
        self.length = length
        self.prefix = prefix
        self.lemma = lemma
        self.POS = POS
        self.shape = shape
        self.bigram = bigram
        self.trigram = trigram
        self.gazetteers = gazetteers
        self.language = language

        self.last_doc = None #Store the last doc to avoid reprocessing of whole phrase
        self.current_sentence = 0
        #Model loading
        if language == "esp":
            self.nlp = spacy.load("es_core_news_sm")
        elif language == "ned":
            self.nlp = spacy.load("nl_core_news_sm")
            self.dutch_names = self.get_ned_PER_gazetteer()
        else:
            raise Exception("Language not in the scope of the model") 

    def __call__(self, tokens, idx):
        """
        Extract basic features about this word including
            - Current word
            - is it capitalized?
            - Does it have punctuation?
            - Does it have a number?
            - Suffixes up to length 3

        Note that : we might include feature over previous word, next word etc.

        :return: a list which contains the features
        :rtype: list(str)
        """

        token = tokens[idx]     
        if not token:
            return list()
        if idx == 0:
            self.current_sentence += 1
            #print(f'Processing sentence {self.current_sentence}...',end='\r')
            self.last_doc = list(self.nlp(' '.join(tokens)))

        spacy_token_0 = self.last_doc[idx]
        
        feature_list = self.get_feature(token,spacy_token_0, "")
        if self.bigram:
            if idx - 1 >= 0:
                spacy_token_ant = self.last_doc[idx - 1]
                feature_list.extend(self.get_feature(tokens[idx-1],spacy_token_ant, "-1_"))
            if self.trigram:
                if idx + 1 < len(tokens):
                    spacy_token_post = self.last_doc[idx + 1]
                    feature_list.extend(self.get_feature(tokens[idx+1],spacy_token_post, "+1_"))
        return feature_list
    
    def get_feature(self, token,spacy_token, position):

        feature_list = list()
        correct = (token == spacy_token.text)
        # Morphology
        if self.morphology and correct:
            for gender in spacy_token.morph.get("Gender"):
                feature_list.append(position + "gender_" + gender)
            for number in spacy_token.morph.get("Number"):
                feature_list.append(position + "number_" + number)

        # Length
        if self.length and correct:
            feature_list.append(position + "LEN_" + str(len(token)))

        # Prefix
        if self.prefix  and correct:
            if len(token) > 0:
                feature_list.append(position + "PRE_" + token[:1])
            if len(token) > 1:
                feature_list.append(position + "PRE_" + token[:2])
            if len(token) > 2:
                feature_list.append(position + "PRE_" + token[:3])
        
        # Lemma
        if self.lemma  and correct:
            feature_list.append(position + "LEMMA_" + spacy_token.lemma_)

        # POS
        if self.POS and correct:
            feature_list.append(position + "POS_" + spacy_token.pos_)
        
        # Shape
        if self.shape and correct:
            feature_list.append(position + "SHAPE_" + spacy_token.shape_)
        
        # Capitalization
        if token[0].isupper():
            feature_list.append(position + "CAPITALIZATION")

        # Number
        pattern = r'\d+'
        if re.search(pattern, token) is not None:
            feature_list.append(position + "HAS_NUM")

        # Punctuation
        punc_cat = {"Pc", "Pd", "Ps", "Pe", "Pi", "Pf", "Po"}
        if all(unicodedata.category(x) in punc_cat for x in token):
            feature_list.append(position + "PUNCTUATION")

        # Suffix up to length 3
        if len(token) > 1:
            feature_list.append(position + "SUF_" + token[-1:])
        if len(token) > 2:
            feature_list.append(position + "SUF_" + token[-2:])
        if len(token) > 3:
            feature_list.append(position + "SUF_" + token[-3:])

        #Gazetteers
        if self.gazetteers and self.language == "ned":
            if token in self.dutch_names:
                feature_list.append(position + "IsPERGaz")

        feature_list.append(position + "WORD_" + token)
        return feature_list

    def get_ned_PER_gazetteer(self):

        dutch_names = set(['Christiane', 'Vandenbussche', 'Eric', 'Derycke', 'Walter', 'Sybille', 'Luc', 'Waltniel', 'Delcroix', 'Leo', 'Verberckmoes', 'Marc', 'Rudy',
                            'Willy', 'Norbert', 'De', 'Frans', 'Verwilghen', 'Hilde', 'Marcel', 'Kristian', 'Robert', 'God', 'Cathy', 'Colas', 'Ramotti', 'Karl', 'Laurent', 
                            'Beatrix', 'Albert', 'KDM', 'Kristof', 'Jan', 'Paul', 'Allen', 'Elián', 'Slobodan', 'Djukanovic', 'Goran', 'Bejoui', 'An', 'Negi', 'Steve', 'Frank', 
                            'Casagrande', 'Tonkov', 'Garzelli', 'Stefano', 'Gilberto', 'Ivan', 'Buenahora', 'Di', 'Piepoli', 'Gonzales', 'TL', 'Francesco', 'Dario', 'Marco',
                            'Alvaro', 'Galdeano', 'Tony', 'Simoni', 'Chernow', 'Christo', 'Jeanne-Claude', 'Javacheff', 'Burt', "Christo's", 'Peter-Jan', 'PJB', 'Didier', 'Gosuin',
                            'Magda', 'Zabel', 'Wüst', 'Plaza', 'Leoni', 'Kadlec', 'Frigo', 'Finot', 'Blanco', 'Ullrich', 'Forconi', 'Merckx', 'Verbrugghe', 'Rebellin', 'Bracke', 
                            'Hruska', 'Guidi', 'Bruylandts', 'Pantani', 'Fornaciari', 'Casero', 'McRae', 'Koerts', 'Lanfranchi', 'Beikirch', 'Boscardin', 'Rous', 'Van', 'Petersen', 
                            'Rubiera', 'Pena', 'Savoldelli', 'Hoj', 'Gotti', 'Klöden', 'Gerosa', 'Rittsel', 'Gonzalez', 'Farazijn', 'Usov', 'Baguet', 'Roesems', 'Heppner', 'Liese', 
                            'Vermeersch', 'Blaudzun', 'Lafis', 'Bölts', 'Kristensen', 'Martinello', 'Belli', 'Boogerd', 'Petacchi', 'Baranowski', 'Castelblanco', 'Noè', 'Konyshev', 
                            'Braikia', 'Mattan', 'Elli', 'Mancebo', 'Conte', 'Pieri', 'Honchar', 'Svorada', 'Vandenbroucke', 'Ief', 'Dave', 'Kurt', 'Alberto', 'Sara', 'Bruylants', 
                            'Patrice', 'Marion', 'Marianne', 'Dupont', 'André', 'Vanthilt', 'Jeanine', 'Tom', 'Cahay', 'Georges', 'Sarah', 'Veerle', 'Patricia', 'Kristien', 'Pol', 
                            'Bart', 'Jeroen', 'Carl', 'MR', 'Ouyahia', 'Seyoum', 'Ahmed', 'Maarten', 'Yemane', 'Theo', 'Cortebeeck', 'Rombouts', 'Eddy', 'Max', 'Ceustermans', 
                            'Isabelle', 'Gantman', 'Larmuseau', 'Hendrik', 'Jean-Luc', 'Rosenfeld', 'Dehaene', 'Karel', 'Philippe', 'GT', 'Gary', 'Köhler', 'Chuan', 'John', 'Horst',
                            'Simonet', 'Antoine', 'Jacques', 'James', 'Quaden', 'JVD', 'Guy', 'Tobin', 'Francis', 'Hugo', 'Vermeiren', 'Bob', 'Ruben', 'Schiltz', 'CG', 'Vandamme',
                            'Leen', 'Michael', 'Phil', 'Best', 'Mike', 'Sabonis', "O'Neal", 'Mark', 'Patrick', 'Bird', 'Reggie', 'Larry', 'Scottie', 'Latrell', 'Kobe', 'Travis',
                            'Derrick', 'Pippen', 'Jackson', 'Jeff', 'Ratu', 'Baninimarama', 'Speight', 'George', 'Volavola', 'Nailatikau', 'Adi', 'Chaudhry', 'Eroni', 'Mahendra',
                            'Agassi', 'Els', 'Zvereva', 'Justine', 'Davenport', 'Callens', 'MC', 'Kim', 'Laurence', 'Appelmans', 'Hingis', 'Courtois', 'Casoni', 'Clijsters', 
                            'Sugiyama', 'Christophe', 'Enqvist', 'Gaudio', 'Kournikova', 'Majoli', 'Hrbaty', 'Rios', 'Kiefer', 'Filip', 'Monami-Van', 'Monami', 'Virginia', 'Marta',
                            'Dominique', 'Lindsay', 'Marrero', 'Sidot', 'Kremer', 'Grzybowska', 'Coetzer', 'Garcia', 'Pierce', 'Rittner', 'Razzano', 'Dementieva', 'Huber', 'Morariu',
                            'Martinez', 'Black', 'Carlsson', 'Srebotnik', 'Schett', 'Fusai', 'Williams', 'Tanasugarn', 'Plischke', 'Farina', 'Foretz', 'Zuluaga', 'Mandula', 'Seles',
                            'Gagliardi', 'Hrdlickova', 'Dokic', 'Kuti', 'Foldenyi', 'Mauresmo', 'Montolio', 'Abe', 'Dragomir', 'Shaughnessy', 'Kucera', 'Pioline', 'Rafter', 'Costa',
                            'Gumy', 'El', 'Ignacio', 'Portas', 'Balcells', 'Calleri', 'Medvedev', 'Rosset', 'Grosjean', 'Browne', 'Safin', 'Ilie', 'Chang', 'Johansson', 'Kafelnikov',
                            'Zabaleta', 'Ferrero', 'Dosedel', 'Philippoussis', 'Goldstein', 'Arazi', 'Hipfl', 'Lapentti', 'Ulihrach', 'Federer', 'Gambill', 'Ferreira', 'Coria', 
                            'Henman', 'Vinck', 'Kuerten', 'Charpentier', 'Kratochvil', 'Stanoytchev', 'Vicente', 'Agenor', 'Puerta', 'Clavet', 'Krajicek', 'Eschauer', 'Corretja',
                            'Meligeni', 'Sargsian', 'Schalken', 'Hantschk', 'Prinosil', 'Moya', 'Hewitt', 'Tarango', 'Bruguera', 'Lisnard', 'Squillari', 'Popp', 'Santoro', 
                            'Gustafsson', 'Dupuis', 'Tillstrom', 'Gaudenzi', 'Lottum', 'Savolt', 'Rodriguez', 'Serrano', 'Pavel', 'Stoltenberg', 'Novak', 'Clement', 'Escude', 'Raoux',
                            'Bastl', 'Sanguinetti', 'Chela', 'Martin', 'Vanek', 'Berasategui', 'Massu', 'Diaz', 'Haas', 'C.', 'Ivanisevic', 'Hry', 'Bjorkman', 'Pozzi', 'Norman'])

        return dutch_names