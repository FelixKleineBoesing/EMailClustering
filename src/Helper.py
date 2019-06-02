from win32com import client
import logging

import re
import codecs

ESCAPE_SEQUENCE_RE = re.compile(r'''
    ( \\U........      # 8-digit hex escapes
    | \\u....          # 4-digit hex escapes
    | \\x..            # 2-digit hex escapes
    | \\[0-7]{1,3}     # Octal escapes
    | \\N\{[^}]+\}     # Unicode characters by name
    | \\[\\'"abfnrtv]  # Single-character escapes
    )''', re.UNICODE | re.VERBOSE)


def get_acc_names():
    '''
    establishes connection to outlook and returns all available account names
    :return: return list of account names
    '''
    try:
        outlook_instance = client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    except Exception as e:
        logging.error("Connection to outlook can´t be established with error msg: {}".format_map(e.args[0]))
        return

    accs = client.Dispatch("Outlook.Application").Session.Accounts
    acc_names = [acc.DeliveryStore.DisplayName for acc in accs]

    return acc_names


def decode_escapes(s):
    def decode_match(match):
        return codecs.decode(match.group(0), 'unicode-escape')

    return ESCAPE_SEQUENCE_RE.sub(decode_match, s)


if __name__=="__main__":
    print(get_acc_names())