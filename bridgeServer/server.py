import generateBridgeHands as gbh
from bottle import request, route, run, response
from json import dumps

@route('/get_new_hand', method='POST')
def feedback():
    data = request.json
    result = gbh.steer_deal(data['h_c'], data['ps_c'])
    response.content_type = 'application/json;charset=UTF-8'
    return dumps(result)
run(host='localhost',port=8080)

"""
# client js
criteria = {h_c: {
    'hcp': [[13,13],'x','x','x','x'],
    'suit': [[5,7],'x','x','x']
    },

ps_c: {
    'hcp': [[26,26],'x','x','x','x'],
    'suit': [[9,9],'x','x','x']
    }}

fetch('/get_new_hand', {
	method: 'post',
    headers: new Headers({
		'Content-Type': 'application/json;charset=UTF-8'
	}),
	body: JSON.stringify(criteria)
})
.then(res => {return res.text()})
.then(x => b = JSON.parse(x))
.catch(err => console.log(err))



fetch('/get_new_hand', {
	method: 'post',
    headers: new Headers({
		'Content-Type': 'application/json;charset=UTF-8'
	}),
	body: JSON.stringify(criteria)
})
.then(res => {return res.json()})
.then(x => d = x)
.catch(err => console.log(err))
"""
