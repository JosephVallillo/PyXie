#! python3

import argparse
import xliff
import os
from gooey import Gooey


def log_string(logfile, s):
    print(s)
    log = open(logfile, 'a', encoding="utf-8")
    log.write(s + '\n')
    log.close()


def find_missing_translations(args):
    _find_missing_translations(args.xliff)


def _find_missing_translations(path):
    if not os.path.isdir(path) and not os.path.isfile(path):
        logfile = path + "_find_missing_translatations_log.txt"
        log_string(logfile, "{} does not exist or could not be found".format(path))
        return

    if os.path.isdir(path):
        for file in os.listdir(path):
            if file.endswith('.xliff'):
                file = os.path.join(path, file)
                logfile = os.path.splitext(file)[0] + "_find_missing_translations_log.txt"
                log_string(logfile, 'Cleaning xliff file...')
                xliff.clean_xliff(file)

                _, root = xliff.get_tree_root(file)
                transarray = xliff.root_to_array(root)

                log_string(logfile, '{} translations found in xliff'.format(len(transarray)))

                missingtrans = xliff.find_missing_translations(transarray)

                log_string(logfile, '{} missing translations found in xliff'.format(len(missingtrans)))
                for trans in missingtrans:
                    log_string(logfile, str(trans))

    elif os.path.isfile(path):
        file = path

        logfile = os.path.splitext(file)[0] + "_find_missing_translations_log.txt"

        if not file.lower().endswith('.xliff'):
            log_string(logfile, '{} is not an xliff file'.format(file))
            return

        log_string(logfile, 'Cleaning xliff file...')
        xliff.clean_xliff(file)

        _, root = xliff.get_tree_root(file)
        transarray = xliff.root_to_array(root)

        log_string(logfile, '{} translations found in xliff'.format(len(transarray)))

        missingtrans = xliff.find_missing_translations(transarray)

        log_string(logfile, '{} missing translations found in xliff'.format(len(missingtrans)))
        for trans in missingtrans:
            log_string(logfile, str(trans))


def clean_xliff(args):
    _clean_xliff(args.xliff)


def _clean_xliff(file):
    logfile = os.path.splitext(file)[0] + "_clean_xliff_log.txt"

    if not os.path.isfile(file):
        log_string(logfile, '{} does not exist or could not be found'.format(file))
        return
    if not file.lower().endswith('.xliff'):
        log_string(logfile, '{} is not an xliff file'.format(file))
        return

    log_string(logfile, 'Attempting to clean {}...'.format(file))
    xliff.clean_xliff(file)


def populate(args):
    _populate(args.xliff)


def _populate(file):
    xliff.clean_xliff(file)
    xliff.populate_empty_target(file)


def depopulate(args):
    _depopulate(args.xliff)


def _depopulate(file):
    xliff.clean_xliff(file)
    xliff.depopulate_empty_target(file)


def verify_placeholders(args):
    _verify_placeholders(args.xliff)


def _verify_placeholders(file):
    logfile = os.path.splitext(file)[0] + "_verify_placeholders_log.txt"

    if not os.path.isfile(file):
        log_string(logfile, '{} does not exist or could not be found'.format(file))
        return
    if not file.lower().endswith('.xliff'):
        log_string(logfile, '{} is not an xliff file'.format(file))
        return

    log_string(logfile, 'Verify placeholders in {}'.format(file))
    diffarray = xliff.verify_placeholder(file)
    if not diffarray:
        log_string(logfile, 'All placeholders in {} match!'.format(file))
        return

    log_string(logfile, 'Inconsistent placeholders in the following idents: ')
    for diff in diffarray:
        log_string(logfile, str(diff))


@Gooey
def main():
    # create top level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='Help for subcommands')

    # create the parser for findMissingTranslations command
    parser_fmt = subparsers.add_parser('findMissingTranslations',
                                       help='Finds all nodes where the target child exists and is empty.'
                                            ' Outputs to a local log folder')
    parser_fmt.add_argument('--xliff',
                            action="store",
                            dest="xliff",
                            type=str,
                            help="Path to xliff file")
    parser_fmt.set_defaults(func=find_missing_translations)

    # create the parser for cleanXliff command
    parser_clean = subparsers.add_parser('cleanXliff',
                                         help='Clean up unnecessary tags that are created as '
                                              'the result of translation software')
    parser_clean.add_argument('--xliff',
                              action="store",
                              dest="xliff",
                              type=str,
                              help="Path to xliff file")
    parser_clean.set_defaults(func=clean_xliff)

    # create the parser for addTargetStrings
    parser_add = subparsers.add_parser('addTargetStrings',
                                       help='Finds all missing translations '
                                            'and sets the target string to source string')
    parser_add.add_argument('--xliff',
                            action="store",
                            dest="xliff",
                            type=str,
                            help="Path to xliff file")
    parser_add.set_defaults(func=populate)

    # create the parser for removeTargetStrings
    parser_remove = subparsers.add_parser('removeTargetStrings',
                                          help='Finds all target strings that match its source string '
                                               'and clears out the target string')
    parser_remove.add_argument('--xliff',
                               action="store",
                               dest="xliff",
                               type=str,
                               help="Path to xliff file")
    parser_remove.set_defaults(func=depopulate)

    # create the parse for verifyPlaceholders
    parser_verify = subparsers.add_parser('verifyPlaceholders',
                                          help='Verifies the placeholder strings')
    parser_verify.add_argument('--xliff',
                               action="store",
                               dest="xliff",
                               type=str,
                               help="Path to xliff file")
    parser_verify.set_defaults(func=verify_placeholders)

    # parse arguments
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
