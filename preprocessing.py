
def convert_BIO(BIO_sents, begin = True, single = False, end = False):
    """
    Conversion of annotated BIO sentences to IO/BIOS/BIOES

    Pre: BIO_sents is the list of annotated data. Begin, single and end are logical: indicate type of coding
    Return: IO code if Begin is False; BIOS if Begin and Single are True; BIOES if Begin, Single and End are True; else returns BIO
    """

    new_sents = list()
    for phrase in BIO_sents:
        new_sent = list()
        phrase.append(None) #Control end-phrase tokens
        prev_BIO = None
        for i, word in enumerate(phrase):
            if word:
                tok, _, label = word
                curr_BIO, entity = label[0], label[1:]
                next_BIO = phrase[i + 1][2] if phrase[i + 1] else None

                #IO
                if not begin:

                    #Outside entities
                    if curr_BIO == 'O':
                        pass
                    #Inside entities
                    else:
                        label = 'I' + entity

                #BIOES
                elif single and end:

                    if curr_BIO == 'O':
                        pass

                    elif curr_BIO == 'B':

                        #Single token entities
                        if (prev_BIO == 'O' or not prev_BIO) and (next_BIO == 'O' or not next_BIO):
                            label = 'S' + entity

                    elif curr_BIO == 'I':

                        #End entity token
                        if (prev_BIO and prev_BIO != 'O') and (next_BIO == 'O' or not next_BIO):
                            label = 'E' + entity

                #BIOS
                elif single:

                    if curr_BIO == 'B':

                        #Single token entities
                        if (prev_BIO == 'O' or not prev_BIO) and (next_BIO == 'O' or not next_BIO):
                            label = 'S' + entity

                    #else -> labels are the same
                    
                new_sent.append((tok, label))
                prev_BIO = curr_BIO
        new_sents.append(new_sent)
    return new_sents
                    

def ne_extractor_txt(sents):
    """
    Extracts the entities of a given IO/BIO/BIOS/BIOES annotated data as tuples (tok, label)
    """
    
    ne = list()
    for phrase in sents:
        phr_ent = list()
        ent_extracted = ('', None)
        phrase.append(None) #Control end-phrase tokens
        prev_BIO = None
        for i, word in enumerate(phrase):
            if word:
                tok, label = word
                curr_BIO, entity = label[0], label[2:]
                next_BIO = phrase[i + 1][1][0] if phrase[i + 1] else None

                if curr_BIO == 'O':
                    if (prev_BIO and prev_BIO != 'O'):
                        phr_ent.append(ent_extracted)
                
                else:
                    #Begin entity
                    if not prev_BIO or prev_BIO == 'O':
                        ent_extracted = (tok, entity)
    
                    else:
                        str, ent = ent_extracted
                        if entity == ent:
                            ent_extracted = (str + ' ' + tok, entity)
                        else:
                            #different entities together
                            phr_ent.append(ent_extracted)
                            ent_extracted = (tok, entity)
                    
                    #Also current word is end entity
                    if not next_BIO:
                        phr_ent.append(ent_extracted)

                prev_BIO = curr_BIO
        ne.append(phr_ent)
    return ne
