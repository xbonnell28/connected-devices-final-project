#!/usr/bin/env python
import shelve

character_data = shelve.open('character.db')
try:
    character_data['health'] = '100'
    character_data['attack'] = '10'
    character_data['gold'] = '1000'
finally:
    character_data.close()

shop_data= shelve.open('shop.db', writeback=True)
try:
    shop_data['Greatsword'] = '100'
    shop_data['Fire Staff'] = '50'
    shop_data['Steel Armor'] = '200'
finally:
    shop_data.close()
