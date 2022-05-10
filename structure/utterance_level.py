# module containing Mentions, which represents an utterance, called Mentions as it contains the AnnotatedMention's
# for the utterance
# Mentions handles calling mention detection functions and determining sentence level information for the
# AnnotatedMentions

import bisect
import pickle
import copy

from mention_detection.span_detection import get_hon_epicene_mentions, \
    get_hon_masculine_mentions, \
    get_hon_feminine_mentions, \
    get_speaker_mentions, \
    get_deputy_speaker_masculine_mentions, \
    get_deputy_speaker_feminine_mentions

from mention_detection.pronominal_mentions import get_pronominal_mentions

from mention_detection.member_for_span_detection import get_member_for_spans

from mention_detection.exact_office_span_detection import get_exact_office_spans

from mention_detection.ministerial_class_span_detection import get_ministerial_class_mentions

from mention_detection.regular_secretary import get_regular_secretary_mentions

from mention_detection.exact_nominal_mentions import get_exact_nominal_mentions

from mention_detection.irregular_office_mention import get_irregular_office_mentions

from mention_detection.mention_type import is_more_precise


# represents an utterance
class Mentions():
    def __init__(self, utt_span):
        self.utt_span = utt_span

        self.annotated_mentions = []

        self.sentence_bounds = None
        self.sentence_starts = None

        self.appositives_processed = False

        self.parent_range = None

    # sort the annotated mentions by start character
    # go through each non-pronominal mention and look at the characters between it and the next non-overlapping mention
    # if the separating characters are of an allowed form, an item of form
    # <mention index>: <next non-overlapping mention index>
    def get_joins(self):
        joins = {}
        for i in range(len(self.annotated_mentions) - 1):
            target = i + 1

            # skip overlapping
            while target < len(self.annotated_mentions) - 1 and self.annotated_mentions[target].start_char <= \
                    self.annotated_mentions[i].end_char:
                target += 1

            separating_span = self.utt_span[
                              self.annotated_mentions[i].end_char:self.annotated_mentions[target].start_char]

            if separating_span in {" ", ", "}:
                joins[i] = target

        return joins

    # transform the joins dictionary into a dictionary containing the groupings of appositives
    def get_appos_chains(self, joins):
        already_added = set()

        # dictionary of lists
        appos_chains = {}
        for i in range(len(self.annotated_mentions)):
            if i in already_added:
                continue

            j = i

            already_added.add(j)
            appos_chains[i] = [i]

            while j in joins:
                j = joins[j]
                appos_chains[i].append(j)
                already_added.add(j)

        return appos_chains

    # take the groupings of appositives and returns a new list of mentions, where appositive chains are a single
    # mention each
    def get_new_list(self, appos_chains):
        new_start_end = {}
        for i in appos_chains:
            first_item_index = appos_chains[i][0]

            new_start = (self.annotated_mentions[first_item_index].start_char,
                         self.annotated_mentions[first_item_index].start_char_in_sentence,
                         self.annotated_mentions[first_item_index].sentence_number)
            new_end = (self.annotated_mentions[first_item_index].end_char,
                       self.annotated_mentions[first_item_index].end_char_in_sentence,
                       self.annotated_mentions[first_item_index].sentence_number)

            for am_index in appos_chains[i]:
                if self.annotated_mentions[am_index].start_char < new_start[0]:
                    new_start = (self.annotated_mentions[am_index].start_char,
                                 self.annotated_mentions[am_index].start_char_in_sentence,
                                 self.annotated_mentions[am_index].sentence_number)
                if self.annotated_mentions[am_index].end_char > new_end[0]:
                    new_end = (
                    self.annotated_mentions[am_index].end_char, self.annotated_mentions[am_index].end_char_in_sentence,
                    self.annotated_mentions[am_index].sentence_number)

            new_start_end[i] = (new_start, new_end)

        return new_start_end

    # returns transformed version of self.annotated_mentions, where appositives are joined
    def get_new_mentions(self, appos_chains, new_start_end):
        new_mentions = []

        for key in appos_chains:
            # go through appos chain to find the most precise mention
            most_precise_index = appos_chains[key][0]
            most_precise = self.annotated_mentions[appos_chains[key][0]]
            for chain_item_index in appos_chains[key]:
                chain_item = self.annotated_mentions[chain_item_index]
                if is_more_precise(chain_item.role, most_precise.role):
                    most_precise = chain_item
                    most_precise_index = chain_item_index

            # now take the properties of the most precise mention in the apposition
            encompassing_mention = copy.deepcopy(most_precise)

            # but set the start and end characters to the start and end of the entire appositive
            encompassing_mention.start_char = new_start_end[key][0][0]
            encompassing_mention.end_char = new_start_end[key][1][0]
            encompassing_mention.start_char_in_sentence = new_start_end[key][0][1]
            encompassing_mention.end_char_in_sentence = new_start_end[key][1][1]
            encompassing_mention.sentence = new_start_end[key][0][2]

            encompassing_mention.appos_chain = []

            if len(appos_chains[key]) > 1:
                encompassing_mention.is_appositive = True


            new_mentions.append(encompassing_mention)

        return new_mentions

    # find all mentions that are adjacent, replace them with a single mention spanning their entirety in
    # self.annotated mentions, add all original mentions to the new mention's appos list
    def join_appositives(self, utt_span=None):
        # sort the AnnotatedMentions by start_char
        self.annotated_mentions.sort(key=lambda x: x.start_char)

        joins = self.get_joins()

        appos_chains = self.get_appos_chains(joins)

        new_start_end = self.get_new_list(appos_chains)

        self.annotated_mentions = self.get_new_mentions(appos_chains, new_start_end)

        self.appositives_processed = True


    # method that for a given utterance span utt_span and its corresponding stanza Document doc, adds mentions of
    # all relevant kinds to self.annotated_mentions, model and datetime_of_utterance provide contextual information
    # that greatly improves mention detection
    def detect_mentions(self, nlp, model, datetime_of_utterance):
        doc = nlp(self.utt_span)

        self.set_sentence_bounds(doc)

        self.sentence_starts = [item[0] for item in self.sentence_bounds]

        sentence_starts = self.sentence_starts

        pronominal_mentions = get_pronominal_mentions(doc, sentence_starts)
        self.add_am_list(pronominal_mentions, sentence_starts)

        hon_epicene_mentions = get_hon_epicene_mentions(self.utt_span, sentence_starts)
        self.add_am_list(hon_epicene_mentions, sentence_starts)

        hon_masculine_mentions = get_hon_masculine_mentions(self.utt_span, sentence_starts)
        self.add_am_list(hon_masculine_mentions, sentence_starts)

        hon_feminine_mentions = get_hon_feminine_mentions(self.utt_span, sentence_starts)
        self.add_am_list(hon_feminine_mentions, sentence_starts)

        speaker_mentions = get_speaker_mentions(self.utt_span)
        self.add_am_list(speaker_mentions, sentence_starts)

        deputy_speaker_masculine_mentions = get_deputy_speaker_masculine_mentions(self.utt_span)
        self.add_am_list(deputy_speaker_masculine_mentions, sentence_starts)

        deputy_speaker_feminine_ranges = get_deputy_speaker_feminine_mentions(self.utt_span)
        self.add_am_list(deputy_speaker_feminine_ranges, sentence_starts)

        member_for_mentions = get_member_for_spans(model, self.utt_span)
        self.add_am_list(member_for_mentions, sentence_starts)

        exact_offices_mentions = get_exact_office_spans(model, self.utt_span, datetime_of_utterance)
        self.add_am_list(exact_offices_mentions, sentence_starts)

        ministerial_class_mentions = get_ministerial_class_mentions(self.utt_span)
        self.add_am_list(ministerial_class_mentions, sentence_starts)

        exact_nominal_mentions = get_exact_nominal_mentions(model, self.utt_span)
        self.add_am_list(exact_nominal_mentions, sentence_starts)

        # do not allow overlap for the following two detected mentions, as these may conflict with earlier, more precise
        # mentions
        regular_secretary_mentions = get_regular_secretary_mentions(self.utt_span)
        self.add_am_list(regular_secretary_mentions, sentence_starts, allow_overlap=False)

        irregular_office_mentions = get_irregular_office_mentions(self.utt_span)
        self.add_am_list(irregular_office_mentions, sentence_starts, allow_overlap=False)

    # returns a tuple [start char index, end char index) for a sentence
    def set_sentence_bounds(self, doc):
        # dictionary containing sentence number as key and tuple of start and end char inclusive
        sentence_list = []

        for sentence in doc.sentences:
            sentence_list.append((sentence.tokens[0].start_char, sentence.tokens[-1].end_char))

        self.sentence_bounds = sentence_list

    # returns a tuple (sentence number, index of start character within sentence, index of end character within
    # sentence)
    def get_sentence_position(self, sentence_starts, start_char, end_char):
        sentence_number = bisect.bisect_right(sentence_starts, start_char) - 1

        start_char_in_sentence = start_char - sentence_starts[sentence_number]
        end_char_in_sentence = end_char - sentence_starts[sentence_number]

        return sentence_number, start_char_in_sentence, end_char_in_sentence

    def is_overlapping_with_existing(self, to_check):
        for item in self.annotated_mentions:
            if item.start_char <= to_check.start_char <= item.end_char \
                    or item.start_char <= to_check.end_char <= item.end_char:
                return True

        return False

    # adds items in mentions to self.annotated_mentions, also calling self.get_sentence_position to add sentence
    # positional data. Items are only added if either allow_overlap is false or they are non-overlapping
    def add_am_list(self, mentions, sentence_starts, allow_overlap=True):
        for mention in mentions:
            if allow_overlap or not self.is_overlapping_with_existing(mention):
                mention.sentence_number, \
                mention.start_char_in_sentence, \
                mention.end_char_in_sentence = self.get_sentence_position(sentence_starts,
                                                                          mention.start_char,
                                                                          mention.end_char)
                self.annotated_mentions.append(mention)



    # returns list of indexes based on self.annotated_mentions, where the ordering is done right to left within
    # sentence and left to right between sentences. Then when this list is iterated backwards in coreference resolution
    # of third person pronouns, the list allows left to right within sentence and right to left between.
    # a b c. d e f. g h. -> indexes for: c b a f e d h g
    def order_mentions(self):
        mentions_ordered = []
        sentence_groups = []
        max_sentence = 0
        for item in self.annotated_mentions:
            if item.sentence_number > max_sentence:
                max_sentence = item.sentence_number

        # add 1 as if the maximum sentence has index 0, we need one sublist to hold its values
        sentence_groups = [[] for item in range(max_sentence+1)]

        for i, item in enumerate(self.annotated_mentions):
            sentence_groups[item.sentence_number].append(i)

        return sentence_groups

    def __repr__(self):
        repr_str = ""
        repr_str += str(self.sentence_bounds) + "\n\n"

        for am in self.annotated_mentions:
            repr_str += f"{am.start_char}, {am.end_char}, {am.sentence_number}, {am.start_char_in_sentence}, " \
                        f"{am.end_char_in_sentence}, {am.gender}\n"

        return repr_str


