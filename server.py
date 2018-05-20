from bottle import get, post, run, response
from pwdmgr import PwdMgr
from utils import Const
import copy

RESP_OBJ = {
    'status': 'success',
    'description': '',
    'data': dict()
}

PwdMgr.init()


@get('/tags')
def list_tags():
    response.set_header('Content-Type', 'application/json; charset=UTF-8')

    resp = copy.deepcopy(RESP_OBJ)
    resp['data'] = []
    tags = PwdMgr.list_tags()
    for tag in tags:
        resp['data'].append(tag)
    return resp


@get('/tags/<tag_name>')
def list_tags(tag_name):
    response.set_header('Content-Type', 'application/json; charset=UTF-8')

    account_tokens = PwdMgr.get_account(tag_name)
    resp = copy.deepcopy(RESP_OBJ)
    if account_tokens:
        user_id = account_tokens[1].decode(Const.UTF8_ENC)
        pwd = account_tokens[2].decode(Const.UTF8_ENC)
        resp['data']['id'] = user_id
        resp['data']['pwd'] = pwd
    else:
        resp['description'] = 'No record found'
    return resp


# @post('/account')
# def create_account():
#     response.set_header('Content-Type', 'application/json; charset=UTF-8')
#
#     PwdMgr.set_account()
#     resp = copy.deepcopy(RESP_OBJ)
#     resp['data'] = 'Created new account'
#     return resp


run(host='localhost', port=8090, debug=True, reloader=True)
