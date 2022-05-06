from structure.annotated_mention import AnnotatedMention

# todo: incorrectly adds interrogative "what", needs more processing, maybe look at person
def get_pronominal_mentions(doc, sentence_starts):
    annotated_mentions = []
    len_of_person = len("Person=")
    len_of_gender = len("Gender=")

    # add pronouns to annotated_mentions
    for sent_no, sentence in enumerate(doc.sentences):
        for word in sentence.words:

            if word.feats is not None:
                # if the word is a pronoun, look at the feats string to determine if the pronoun is singular
                if word.upos == "PRON":
                    # filter out neuter and epicene pronouns, feats does not contain information to discriminate
                    if word.text.lower() in ["it", "itself", "its", "they", "them", "themselves", "theirs", "their"]:
                        continue

                    # filter out first person plural, feats does not contain info to discriminate this
                    if word.text.lower() in ["we", "us", "ourselves", "ours", "our"]:
                        continue

                    # filter out interrogative non-personal plural, feats does not contain info to discriminate this
                    if word.text.lower() in ["what"]:
                        continue
                    # print(word.text, word.parent.text, word.upos, word.feats)

                    if word.feats.find("Person=") != -1:
                        person = word.feats[word.feats.find("Person=") + len_of_person]
                        person = int(person)
                    else:
                        # stanza outputs no person for some third person pronouns
                        # todo: need better handling of other types
                        person = "other"

                    gender = None

                    # print("word:", word.text, "gender:", word.feats[word.feats.find("Gender=")+len_of_gender : word.feats.find("Gender=")+len_of_gender+4])

                    if word.feats.find("Gender=") != -1:
                        if word.feats[word.feats.find("Gender=") + len_of_gender: word.feats.find(
                                "Gender=") + len_of_gender + 4] == "Masc":
                            gender = "masculine"
                        elif word.feats[word.feats.find("Gender=") + len_of_gender: word.feats.find(
                                "Gender=") + len_of_gender + 3] == "Fem":
                            gender = "feminine"
                        else:
                            gender = "epicene"


                    # store only the features we are interested in
                    # todo: start and end chars are using tokens, which is correct in most cases
                    new_am = AnnotatedMention(start_char=word.parent.start_char,
                                              end_char=word.parent.end_char,
                                              person=person, sentence=sent_no,
                                              gender=gender,
                                              role="pronominal_mention")

                    #self.annotated_mentions.append(new_am)
                    annotated_mentions.append(new_am)

    return annotated_mentions