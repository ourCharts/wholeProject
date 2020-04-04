import json
def helloking(arr):
    arr.send(text_data=json.dumps({
                'message': 'hello this is from server kingsley1'
            }))