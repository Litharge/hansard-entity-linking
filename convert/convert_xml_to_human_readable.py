# generate a human readable form of the xml allowing human annotators, as well as a description of how to map it back
# to xml, so that the human annotations can be compared with the system output
# start and end tags specify range [start, end] to be annotated as the entire day would be too great a task
import bisect
import bisect

from lxml import etree


class IDRanges():
    def __init__(self):
        # dictionary containing the lower character position bound of each id, utterer and separator
        self.mapping = {}

    # method to return the id associated with a given character position
    def get_id(self, index):
        sorted_mapping_keys = sorted(self.mapping)

        key_index = bisect.bisect_right(sorted_mapping_keys, index) - 1
        return self.mapping[sorted_mapping_keys[key_index]]




# start: id attribute value of speech tag to start at, inclusive. Set to None to specify first tag.
# end: id attribute of speech tag to end at, inclusive. Set to None to specify last tag.
# returns: string consisting of utterances in range [start, end]
def get_human_readable(location, start, end):
    tree = etree.parse(location)

    root = tree.getroot()

    selected_text = ""

    seen_start = False

    # dictionary to map character index in output to pid of xml
    pid = IDRanges()

    for ch in root.getchildren():
        # skip the loop until the start pid is found
        if not seen_start and ch.get("id") != start:
            continue
        else:
            seen_start = True

        if ch.tag == "speech" and not ch.get("nospeaker") == "true":
            pid.mapping[len(selected_text)] = "utterer_" + ch.get("speakername")
            selected_text += ch.get("speakername") + "\n"

            for p in ch.getchildren():
                pid.mapping[len(selected_text)] = p.get("pid")
                selected_text += "".join(p.itertext()) + "\n"

            pid.mapping[len(selected_text)] = "separator"
            selected_text += "\n"


        # end the loop when the end pid is found
        if ch.get("id") == end:
            break

    return selected_text, pid
