# establish an ordering of specificity of mention types

def is_more_precise(first_type, second_type):
    order = [
        # there is exactly one MP for a given constituency, irrefular office or speaker mention
        "member_for_mention",
        "irregular_office_mention",
        "speaker_mention",
        # there is likely only one MP for a given name or office
        "exact_nominal_mention",
        "exact_office_mention",
        "secretary_regular_mention",
        # these narrow the possible referents to a small class
        "minister_class_mention",
        "deputy_speaker_mention",
        # hon mentions usually refer to prefious utterer, but if in apposition probably not
        "hon_mention",
        # least precise
        "pronominal_mention"
    ]
    if first_type not in order or second_type not in order:
        raise Exception("mention type not in ordering")

    # a lower index is more precise
    if order.index(first_type) < order.index(second_type):
        return True
    else:
        return False