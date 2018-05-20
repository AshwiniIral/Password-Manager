from account import Account
from utils import Utils, Const, Globals
from pathlib import Path


class PwdMgr:

    @staticmethod
    def init(key):

        # key_hash = Utils.get_hash(key)
        # Globals.db_file = '{0}/.{1}'.format(user_home, key_hash)

        Globals.db_file = PwdMgr.db_file(key)
        Utils.init_cipher(key)

        if Path.is_file(Path(Globals.db_file)):
            PwdMgr.read_db()

    @staticmethod
    def db_file(key):
        user_home = str(Path.home())
        key_hash = Utils.get_hash(key)
        return '{0}/.{1}'.format(user_home, key_hash)

    @staticmethod
    def create(tag, access_rec):
        account = Account(tag, access_rec)
        Globals.db_data[tag] = account.get_access_rec()
        PwdMgr.save_db()

    @staticmethod
    def get(tag):
        if tag in Globals.db_data.keys():
            return Utils.decrypt(Globals.db_data[tag])
        return None

    @staticmethod
    def list():
        return Globals.db_data.keys()

    @staticmethod
    def save_db():
        with open(Globals.db_file, 'wb') as f:
            db_out = b''
            for tag in Globals.db_data.keys():
                db_out = b''.join([db_out, Globals.db_data[tag], Const.END_OF_REC])
            f.write(db_out)

    @staticmethod
    def read_db():
        with open(Globals.db_file, 'rb') as f:
            db_raw_data = f.read()
            db_raw_rec_data = db_raw_data.split(Const.END_OF_REC)
            for account_cipher_rec in db_raw_rec_data:
                if len(account_cipher_rec) != 0:
                    access_rec = Utils.decrypt(account_cipher_rec)
                    account_tag = access_rec.split(Const.B_REC_TOKENS_SEP)[0].decode(Const.UTF8_ENC)
                    Globals.db_data[account_tag] = account_cipher_rec
                    access_rec = None  # this will have decrypted access_rec

    @staticmethod
    def set_account(tag, user_id, pwd):
        access_rec = Utils.encrypt(
            '{0}{1}{2}{3}{4}'.format(tag, Const.REC_TOKENS_SEP, user_id, Const.REC_TOKENS_SEP, pwd))
        PwdMgr.create(tag, access_rec)

    @staticmethod
    def get_account(tag):
        access_rec = PwdMgr.get(tag)
        if access_rec:
            access_rec = access_rec.strip(b'\x03')  # remove padding characters
            access_rec_tokens = access_rec.split(Const.B_REC_TOKENS_SEP)
            return access_rec_tokens
        return None

    @staticmethod
    def list_tags():
        return PwdMgr.list()
