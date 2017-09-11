from __future__ import absolute_import, division, print_function, with_statement

import config

from maintain import db
db = db.db

def clear_pn_records(pn):
    db.deal_pn_user_history(pn)

def clear_ac_online_records(acs=[]):
    '''
        ac : list
    '''
    if not acs:
        return
    db.clear_ac_online_records(acs)


if __name__ == '__main__':
    db.setup(config['database'])
    # clear pynx user's history
    clear_pn_records(15914)
    # clear online records 
    # clear_ac_online_records(['172.201.2.251', '172.201.2.252'])

    print('clear successfully')
