#! python3

import xml.etree.ElementTree as ET
from xml.parsers import expat
import os, sys, re, argparse

# Setup XLIFF name space
NSMAP = {'mw': 'urn:oasis:names:tc:xliff:document:1.2' }
ET.register_namespace('', 'urn:oasis:names:tc:xliff:document:1.2')

# TODO: Define global log file
# TODO: Clean up temp files that get created

class Xliff:
    # TODO: Clean up init function
    def __init__(self, xliffPath):
        # Check if file exists
        if not os.path.exists(xliffPath):
            # TODO: Raise Exception
            return
        if not (xliffPath.lower().endswith('.xliff')):
            print("The given file is not an xliff file")
            # TODO: Raise exceptions
        self.path = xliffPath
        self.tree, self.root = self.getTreeRoot(xliffPath)
        self.transArray = self.xliffToArray()

    def getTreeRoot(self,xliffFile):
        tree = ET.parse(xliffFile, ET.XMLParser(encoding='utf-8'))
        root = tree.getroot()

        if root == None:
            print('Could not successfully parse %s.' % (xliffFile))
        return (tree, root)

    def clean(self):
        print("Opening xliff file...\n\n")
        file = open(self.path, "r+", encoding="utf8")

        removedMrkText = re.sub(r"<[/]{0,1}mrk[\s\S]*?>", "", file.read())
        removedSegSourceText = re.sub(r"<seg-source>[\s\S]*?</seg-source>", "", removedMrkText)

        file.write(removedSegSourceText)

        file.close()

    def xliffToArray(self):
        translations = []
        for transUnit in self.root.findall('.//mw:trans-unit', namespaces=NSMAP):
            ident = transUnit.get('id')
            sourceString = transUnit.find('.//mw:source', namespaces=NSMAP)
            targetString = transUnit.find('.//mw:target', namespaces=NSMAP)

            if (ident!= None and sourceString != None and targetString != None):
                translations.append((ident, sourceString.text, targetString.text))

        return translations

    def xliffToExcel(self, targetPath):
        return




# TODO: Remove old way of doing things

def getXliffTreeRoot(xliffFile):
    tree = ET.parse(xliffFile, ET.XMLParser(encoding='utf-8'))
    root = tree.getroot()

    if root == None:
        print('Could not successfully parse %s.' % (xliffFile))
    return (tree, root)

def cleanXliff(args):
    cleanedXliff = _cleanXliff(args.xliff)
    return cleanedXliff

def _cleanXliff(xliffFile):
    # TODO: Implement cleaning logic
    return

def removeTargetStrings(args):
    _removeTargetStrings(args.xliff)
    return

def _removeTargetStrings(xliffFile):
    print("In _removeTargetStrings")
    xliffFile = xliffFile

    # Create Log file
    logFile = open(os.path.splitext(xliffFile)[0] + "_log.txt", 'w')

    # Check if file exists
    if os.path.exists(xliffFile):

        # Check if file is an xliff
        if not (xliffFile.lower().endswith('.xliff')):
            print("The given file is not an xliff file")
            logFile.write("The given file is not an xliff file: %s\n\n" % xliffFile)
            sys.exit()

        # Open xliff
        logFile.write("Opening xliff file...\n\n")
        file = open(xliffFile, "r", encoding="utf8")

        # Cleanup and create temp
        outputfile = open(os.path.splitext(xliffFile)[0] + "_updated.xliff", "w", encoding="utf8")
        logFile.write("Cleaning up %s and storing the results in %s\n\n" % (xliffFile, outputfile))

        removedMrkText = re.sub(r"<[/]{0,1}mrk[\s\S]*?>", "", file.read())
        removedSegSourceText = re.sub(r"<seg-source>[\s\S]*?</seg-source>", "", removedMrkText)

        outputfile.write(removedSegSourceText)

        file.close()
        outputfile.close()

        # Load and parse xliff
        logFile.write("Loading and parsing temp xliff file\n\n")
        transTree, transRoot = getXliffTreeRoot(os.path.splitext(xliffFile)[0] + "_updated.xliff")
        transLen = len(transRoot.findall('.//mw:trans-unit', namespaces=NSMAP))
        logFile.write('%s translations present in the xliff\n\n' % (transLen))

        # Find all missing translation
        for transUnit in transRoot.findall('.//mw:trans-unit', namespaces=NSMAP):
            ident = transUnit.get('id')
            sourceString = transUnit.find('.//mw:source', namespaces=NSMAP)
            targetString = transUnit.find('.//mw:target', namespaces=NSMAP)

            if sourceString == None:
                logFile.write('Source tag does not exist for trans-unit id: %s\n\n' % (ident))
                continue
            if sourceString.text == None:
                logFile.write('Could not find source string for trans-unit id: %s\n\n' % (ident))
                continue
            if targetString == None:
                logFile.write('Could not find translation tag for trans-unit id: %s\nsource string: %s\n\n' % (
                    ident, sourceString.text))
                continue
            if targetString.text == None:
                logFile.write('Could not find translation string for trans-unit id: %s\n\n' % (
                    ident))
                continue
            if targetString.text == sourceString.text:
                targetString.text = ''

        # Delete the temp file
        logFile.write("Deleting temp file: %s" % (os.path.splitext(xliffFile)[0] + "_updated.xliff"))
        os.unlink(os.path.splitext(xliffFile)[0] + "_updated.xliff")

        # Save the output
        transTree.write(os.path.splitext(xliffFile)[0] + "_updated.xliff", encoding="utf8")
    else:
        print("Given xliff file does not exist")
        logFile.write("The given xliff file does not exist: %s" % xliffFile)

    # Close the log file
    logFile.close()

def addTargetStrings(args):
    _addTargetStrings(args.xliff)
    return

def _addTargetStrings(xliffFile):
    print("In _addTargetStrings")
    xliffFile = xliffFile

    # Create Log file
    logFile = open(os.path.splitext(xliffFile)[0] + "_log.txt", 'w')

    # Check if file exists
    if os.path.exists(xliffFile):

        # Check if file is an xliff
        if not (xliffFile.lower().endswith('.xliff')):
            print("The given file is not an xliff file")
            logFile.write("The given file is not an xliff file: %s\n\n" % xliffFile)
            sys.exit()

        # Open xliff
        logFile.write("Opening xliff file...\n\n")
        file = open(xliffFile, "r", encoding="utf8")

        # Cleanup and create temp
        outputfile = open(os.path.splitext(xliffFile)[0] + "_updated.xliff", "w", encoding="utf8")
        logFile.write("Cleaning up %s and storing the results in %s\n\n" % (xliffFile, outputfile))

        removedMrkText = re.sub(r"<[/]{0,1}mrk[\s\S]*?>", "", file.read())
        removedSegSourceText = re.sub(r"<seg-source>[\s\S]*?</seg-source>", "", removedMrkText)

        outputfile.write(removedSegSourceText)

        file.close()
        outputfile.close()

        # Load and parse xliff
        logFile.write("Loading and parsing temp xliff file\n\n")
        transTree, transRoot = getXliffTreeRoot(os.path.splitext(xliffFile)[0] + "_updated.xliff")
        transLen = len(transRoot.findall('.//mw:trans-unit', namespaces=NSMAP))
        logFile.write('%s translations present in the xliff\n\n' % (transLen))

        # Find all missing translation
        for transUnit in transRoot.findall('.//mw:trans-unit', namespaces=NSMAP):
            ident = transUnit.get('id')
            sourceString = transUnit.find('.//mw:source', namespaces=NSMAP)
            targetString = transUnit.find('.//mw:target', namespaces=NSMAP)

            if sourceString == None:
                logFile.write('Source tag does not exist for trans-unit id: %s\n\n' % (ident))
                continue
            if sourceString.text == None:
                logFile.write('Could not find source string for trans-unit id: %s\n\n' % (ident))
                continue
            if targetString == None:
                logFile.write('Could not find translation tag for trans-unit id: %s\nsource string: %s\n\n' % (
                    ident, sourceString.text))
                continue
            if targetString.text == None:
                targetString.text = sourceString.text

        # Delete the temp file
        logFile.write("Deleting temp file: %s" % (os.path.splitext(xliffFile)[0] + "_updated.xliff"))
        os.unlink(os.path.splitext(xliffFile)[0] + "_updated.xliff")

        # Save the output
        transTree.write(os.path.splitext(xliffFile)[0] + "_updated.xliff", encoding="utf8")
    else:
        print("Given xliff file does not exist")
        logFile.write("The given xliff file does not exist: %s" % xliffFile)

    # Close the log file
    logFile.close()

def findDuplicates(args):
    _findDuplicates(args.xliff)

def _findDuplicates(xliffFile):
    print("in _findDeuplicates")

    # Create Log file
    logFile = open(os.path.splitext(xliffFile)[0] + "_duplicates_log.txt", 'w')




def findMissingTranslations(args):
    print("In findMissingTranslations")
    xliffFile = args.xliff

    # Create Log file
    logFile = open(os.path.splitext(xliffFile)[0] + "_log.txt", 'w')

    # Check if file exists
    if os.path.exists(xliffFile):

        # # Check if file is an xliff
        # if not (xliffFile.lower().endswith('.xliff')):
        #     print("The given file is not an xliff file")
        #     logFile.write("The given file is not an xliff file: %s\n\n" % xliffFile)
        #     sys.exit()

        # Open xliff
        logFile.write("Opening xliff file...\n\n")
        file = open(xliffFile, "r", encoding="utf-8")

        # Cleanup and create temp
        outputfile = open(os.path.splitext(xliffFile)[0] + "_updated.xliff", "w", encoding="utf-8")
        logFile.write("Cleaning up %s and storing the results in %s\n\n" % (xliffFile, outputfile))

        removedMrkText = re.sub(r"<[/]{0,1}mrk[\s\S]*?>", "", file.read())
        removedSegSourceText = re.sub(r"<seg-source>[\s\S]*?</seg-source>", "", removedMrkText)

        outputfile.write(removedSegSourceText)

        file.close()
        outputfile.close()

        # Load and parse xliff
        logFile.write("Loading and parsing temp xliff file\n\n")
        transTree, transRoot = getXliffTreeRoot(os.path.splitext(xliffFile)[0] + "_updated.xliff")
        transLen = len(transRoot.findall('.//mw:trans-unit', namespaces=NSMAP))
        logFile.write('%s translations present in the xliff\n\n' % (transLen))

        translationList = []
        # Find all missing translation
        for transUnit in transRoot.findall('.//mw:trans-unit', namespaces=NSMAP):
            ident = transUnit.get('id')
            sourceString = transUnit.find('.//mw:source', namespaces=NSMAP)
            targetString = transUnit.find('.//mw:target', namespaces=NSMAP)


            if sourceString == None:
                logFile.write('Source tag does not exist for trans-unit id: %s\n\n' % (ident))
                continue
            if sourceString.text == None:
                logFile.write('Could not find source string for trans-unit id: %s\n\n' % (ident))
                continue
            if sourceString.text in translationList:
                print('DUPLICATE SOURCE STRING')
            if targetString == None:
                logFile.write('Could not find translation tag for trans-unit id: %s\nsource string: %s\n\n' % (
                ident, sourceString.text))
                continue
            if targetString.text == None:
                logFile.write('Could not find translation for trans-unit id: %s\nsource string: %s\n\n' % (
                ident, sourceString.text))
                continue

            translationList.append((ident, sourceString.text, targetString.text))

        # Delete the temp file
        logFile.write("Deleting temp file: %s" % (os.path.splitext(xliffFile)[0] + "_updated.xliff"))
        os.unlink(os.path.splitext(xliffFile)[0] + "_updated.xliff")
    else:
        print("Given xliff file does not exist")
        logFile.write("The given xliff file does not exist: %s" % xliffFile)

    # Close the log file
    logFile.close()

def mergeXliffs(args):
    print("In mergeXliffs")
    transSource = args.transSource
    canfieldTarget = args.canfieldTarget
    xliffs = [transSource, canfieldTarget]

    # Create Log file

    logFile = open(os.path.splitext(canfieldTarget)[0] + "_log.txt", 'w')

    # Verify that both files exist and are xliffs
    #
    # for xliff in xliffs:
    #     # Check is file exists
    #     if os.path.exists(xliff):
    #         # Check if file is an xliff
    #         if not ((xliff.lower().endswith('.xliff')) or xliff.lower().endswith('.sdlxliff') or xliff.lower().endwith('.xlf')):
    #             print("The given file is not an xliff file")
    #             logFile.write("The given file is not an xliff file: %s\n\n" % xliff)
    #             sys.exit()
    #     else:
    #         print("Given xliff file does not exist")
    #         logFile.write("The given xliff file does not exist: %s" % xliff)
    #         sys.exit()

    # Clean up and create temp for trans file

    # Open source xliff
    logFile.write("Opening xliff file...\n\n")
    sourceFile = open(transSource, "r", encoding="utf8")

    # cleanup and create temp
    sourceTemp = open(os.path.splitext(transSource)[0] + "_temp.xliff", "w", encoding="utf8")
    logFile.write("Cleaning up %s and storing the results in %s\n\n" % (transSource, sourceTemp))

    removedMrkText = re.sub(r"<[/]{0,1}mrk[\s\S]*?>", "", sourceFile.read())
    removedSegSourceText = re.sub(r"<seg-source>[\s\S]*?</seg-source>", "", removedMrkText)

    sourceTemp.write(removedSegSourceText)

    sourceFile.close()
    sourceTemp.close()

    # Parse xliff files

    logFile.write("Loading and parsing xliff files\n\n")
    transTree, transRoot = getXliffTreeRoot(os.path.splitext(transSource)[0] + "_temp.xliff")
    targetTree, targetRoot = getXliffTreeRoot(os.path.splitext(canfieldTarget)[0] + ".xliff")


    # Get list of translations in the source

    translationList = []
    for transUnit in transRoot.findall('.//mw:trans-unit', namespaces=NSMAP):
        ident = transUnit.get('id')
        sourceString = transUnit.find('.//mw:source', namespaces=NSMAP)
        targetString = transUnit.find('.//mw:target', namespaces=NSMAP)

        if sourceString == None:
            logFile.write('Source tag does not exist for trans-unit id: %s\n\n' % (ident))
            continue
        if sourceString.text == None:
            logFile.write('Could not find source string for trans-unit id: %s\n\n' % (ident))
            continue
        if targetString == None:
            logFile.write('Could not find translation tag for trans-unit id: %s\nsource string: %s\n\n' % (
                ident, sourceString.text))
            continue
        if targetString.text == None:
            logFile.write('Could not find translation for trans-unit id: %s\nsource string: %s\n\n' % (
                ident, sourceString.text))
            continue

        translationList.append([ident, sourceString.text, targetString.text])

    #  Merge files
    #print(translationList)

    for transUnit in targetRoot.findall('.//mw:trans-unit', namespaces=NSMAP):
        ident = transUnit.get('id')
        transNode = [transNode for transNode in translationList if ident in transNode]

        if len(transNode) > 0:
            target = transUnit.find('.//mw:target', namespaces=NSMAP)
            if target != None:
                target.text = transNode[0][2]

    # Save the output
    targetTree.write(os.path.splitext(canfieldTarget)[0] + "_merged.xliff", encoding="utf8")


def createTranslationFile(source, target):
    # TODO: Check if file is an xliff
    # TODO: Open xliff
    # TODO: Cleanup and create temp
    # TODO: Find Missing Translations

    return

def makeStringsFiles(source):
    return

def main():
    # create top level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='Help for subcommands')

    # create the parser for findMissingTranslations command
    parser_fMT = subparsers.add_parser('findMissingTranslations',
                                       help='Finds all nodes where the target child exists and is empty. Outputs to a local log folder')
    parser_fMT.add_argument('--xliff',
                            action="store",
                            dest="xliff",
                            type=str,
                            help="Path to xliff file")
    parser_fMT.set_defaults(func=findMissingTranslations)

    # create the parser for mergeXliffs command
    parser_merge = subparsers.add_parser('mergeXliffs',
                                         help="Merges xliff provided by translators into Canfield xliff file")
    parser_merge.add_argument('--transSource',
                              action="store",
                              dest="transSource",
                              type=str,
                              help="Path to xliff file provided by translators")
    parser_merge.add_argument('--canfieldTarget',
                              action="store",
                              dest="canfieldTarget",
                              type=str,
                              help="Path to Canfield xliff life file that new translations will be merged into")
    parser_merge.set_defaults(func=mergeXliffs)

    # create the parser for cleanXliff command
    parser_clean = subparsers.add_parser('cleanXliff',
                                         help='Clean up unnecessary tags that are created as the result of translation software')
    parser_clean.add_argument('--xliff',
                            action="store",
                            dest="xliff",
                            type=str,
                            help="Path to xliff file")
    parser_clean.set_defaults(func=cleanXliff)

    # create the parser for addTargetStrings
    parser_add = subparsers.add_parser('addTargetStrings',
                                       help='Finds all missing translations and sets the target string to source string')
    parser_add.add_argument('--xliff',
                            action="store",
                            dest="xliff",
                            type=str,
                            help="Path to xliff file")
    parser_add.set_defaults(func=addTargetStrings)

    # create the parser for removeTargetStrings
    parser_remove = subparsers.add_parser('removeTargetStrings',
                                          help = 'Finds all target strings that match its source string and clears out the target string')
    parser_remove.add_argument('--xliff',
                            action="store",
                            dest="xliff",
                            type=str,
                            help="Path to xliff file")
    parser_remove.set_defaults(func=removeTargetStrings)

    # parse arguments
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()