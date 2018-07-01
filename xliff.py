import xml.etree.ElementTree as eT
import collections
import re, os


Translation = collections.namedtuple('Translation', 'ident source target')

NSMAP = {'mw': 'urn:oasis:names:tc:xliff:document:1.2'}
eT.register_namespace('', 'urn:oasis:names:tc:xliff:document:1.2')


def get_tree_root(xliff):
    """
    Parses given xliff file and creates a tree and root structure

    :param xliff: path to xliff file
    :return: tree and root objects
    """
    tree = eT.parse(xliff, eT.XMLParser(encoding='utf-8'))
    root = tree.getroot()

    if not root:
        print('Could not successfully parse %s.' % xliff)
    return tree, root


def clean_xliff(xliff):
    """
    Cleans the xliff of unnecessary tags that were inserted as a result of the translation software

    :param xliff: path to xliff file
    :return:
    """
    file = open(xliff, "r", encoding="utf-8")

    removedmrktext = re.sub(r"<[/]{0,1}mrk[\s\S]*?>", "", file.read())
    removedsegsourcetext = re.sub(r"<seg-source>[\s\S]*?</seg-source>", "", removedmrktext)

    file.close()

    file = open(xliff, "w", encoding="utf-8")

    file.write(removedsegsourcetext)
    file.close()


def root_to_array(root):
    """
    Converts a root structure to an array of Translation tuples

    :param root: Xliff root structure generated from get_tree_root()
    :return: array of Translation tuples
    """
    translations = []
    for transunit in root.findall('.//mw:trans-unit', namespaces=NSMAP):
        ident = transunit.get('id')
        sourcestring = transunit.find('.//mw:source', namespaces=NSMAP)
        targetstring = transunit.find('.//mw:target', namespaces=NSMAP)

        if ident is not None and sourcestring is not None and targetstring is not None:
            translations.append(Translation(ident=ident, source=sourcestring.text, target=targetstring.text))

    return translations


def find_missing_translations(translations):
    """
    Creates a list of Translation tuples that are missing translations

    :param translations: Array of Translation tuples
    :return: Array of Translation tuples where item.target is None
    """
    missingtrans = []
    for translation in translations:
        if not translation.target:
            missingtrans.append(translation)

    return missingtrans

# TODO: TEST
def populate_empty_target(xliff):
    """
    Populates the target value if empty to be equal to the source string

    :param xliff: path to xliff file
    :return:
    """
    tree, root = get_tree_root(xliff)

    for transunit in root.findall('.//mw:trans-unit', namespaces=NSMAP):
        sourcestring = transunit.find('.//mw:source', namespaces=NSMAP)
        targetstring = transunit.find('.//mw:target', namespaces=NSMAP)

        if not sourcestring or not sourcestring.text or not targetstring:
            continue
        if not targetstring.text:
            targetstring.text = sourcestring.text

    tree.write(os.path.splitext(xliff)[0] + "_populated.xliff", encoding="utf-8")

# TODO: TEST
def depopulate_empty_target(xliff):
    """
    Removes the target value if the string is equal to the source string

    :param xliff: path to xliff file
    :return:
    """
    tree, root = get_tree_root(xliff)

    for transunit in root.findall('.//mw:trans-unit', namespaces=NSMAP):
        sourcestring = transunit.find('.//mw:source', namespaces=NSMAP)
        targetstring = transunit.find('.//mw:target', namespaces=NSMAP)

        if not sourcestring or not sourcestring.text or not targetstring or not targetstring.text:
            continue
        if targetstring.text == sourcestring.text:
            targetstring.text = ''

    tree.write(os.path.splitext(xliff)[0] + "_depopulated.xliff", encoding="utf-8")


def verify_placeholder(xliff):
    """
    Checks all source strings for existence of placeholders and verifies that the target
    string contains the same place holders.

    :param xliff: path to xliff file
    :return: array of Translation tuples which contain inconsistent placeholders
    """
    regexstring = r"<!--[\s\S]*?-->"
    placeholderregex = re.compile(regexstring)
    tree, root = get_tree_root(xliff)

    transarray = root_to_array(root)

    diffarray = []

    for trans in transarray:
        if not trans.source or not trans.target:
            continue

        sourceplaceholders = placeholderregex.findall(trans.source)
        targetplaceholders = placeholderregex.findall(trans.target)

        diff = list(set(sourceplaceholders) - set(targetplaceholders))

        if diff:
            diffarray.append(trans)

    return diffarray


