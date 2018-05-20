import getpass
import sys
from pathlib import Path

from utils import Const
from pwdmgr import PwdMgr

import pyperclip


def run():
    # passkey should be of at least 32 characters
    while True:
        print('** Use UUID from https://www.uuidgenerator.net/ for passwords')
        db_key1 = getpass.getpass('> Enter passkey (at least 32 characters): ')
        if len(db_key1) < 32:
            print('Password length is < 32 characters')
            continue

        if Path.is_file(Path(PwdMgr.db_file(db_key1))):
            PwdMgr.init(db_key1)
            break

        while True:
            db_key2 = getpass.getpass('> Re enter passkey (at least 32 characters): ')
            if len(db_key2) < 32:
                print('Password length is < 32 characters')
                continue
            break

        if db_key1 == db_key2:
            PwdMgr.init(db_key1)
            break

        print('Passwords did not match. Retry')

    while True:
        print('[1] New account')
        print('[2] Find account')
        print('[3] List all tags')
        print('[4] Exit')

        try:
            action = int(input('Select: '))
        except ValueError:
            print('!!! Error - Incorrect selection')
            continue

        if action == 1:
            tag = input('> Tag: ')
            user_id = input('> Id: ')
            while True:
                pwd1 = getpass.getpass('> Password: ')
                pwd2 = getpass.getpass('> Re-enter Password: ')
                if pwd1 == pwd2:
                    break
                else:
                    print('Passwords did not match. Try again')
            PwdMgr.set_account(tag, user_id, pwd1)
        elif action == 2:
            tag = input('> Tag: ')
            account_tokens = PwdMgr.get_account(tag)
            if account_tokens:
                print('Id - ' + account_tokens[1].decode(Const.UTF8_ENC))
                pyperclip.copy(account_tokens[2].decode(Const.UTF8_ENC))
                print('Password copied to clipboard')
            else:
                print('No record found')
        elif action == 3:
            tags = PwdMgr.list_tags()
            for tag in tags:
                print(tag)

        elif action == 4:
            sys.exit(0)
        else:
            print('!!! Error - Incorrect selection')


if __name__ == '__main__':
    run()
