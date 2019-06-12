import json
import sys 
import traceback

def main():
    try:
        json_input = open(sys.argv[1]).read()
        data = json.loads(json_input) 
    except:
        print("Please enter a valid file")
        return -1

    fix(data)
    print(json.dumps(data, indent=4, sort_keys=True))
    return 0

def fix(data):
    for feature in data:
        translate_feature(feature)
        for scenario in feature['elements']:
            if type(scenario) == dict:
                translate_scenario(scenario)
                scenario['id'] = feature['id'] + ";" + scenario['id']
            for step in scenario['steps']:
                step['line'] = step['location'].split(':')[1]
                step['match'] = {'location':step['location']}          
                
 

def fix_tags(feature):
    if type(feature) == dict:
        if 'tags' in feature.keys():
            for tag in feature['tags']:
                tmp = {}
                tmp['name'] = '@' + tag
                tmp['line'] = 'todo'
                feature['tags'].append(tmp)
                feature['tags'].remove(tag)           
        for i in feature:
            fix_tags(feature[i])
    elif type(feature) == list:
        for i in feature:
            fix_tags(i)
   
def translate_feature(json):
    parts = json['location'].split(':')
    json['uri'] = parts[0]
    json['line'] = parts[1]
    json.pop('location')
    json.pop('status')
    if json['tags'] == []:
        json.pop('tags')    
    json['id'] = '-'.join(json['name'].lower().split())
    if 'description' not in json.keys():
        json['description'] = ''    
    remove_not_run(json)
    return 0

def translate_scenario(json):
    parts = json['location'].split(':')
    json['uri'] = parts[0]
    json['line'] = parts[1]
    json.pop('location')
    if 'description' not in json.keys():
        json['description'] = ''
    #json.pop('status')
    if json['tags'] == []:
        json.pop('tags')    
    for i in json['steps']:
        if 'match' in i.keys() and i['match']['arguments'] == []:
            i['match'].pop('arguments')
        if 'result' in i.keys() and 'duration' in i['result'].keys():
            i['result']['duration'] = translate_time(i['result']['duration'])
    json['id'] = '-'.join(json['name'].lower().split())
    for i in range(len(json['tags'])):
        tmp = {'name':('@'+json['tags'][i]), 'line':'TODO'}
        json['tags'][i] = tmp
    return 0

def translate_time(result):
    return result*(10**9)

def remove_not_run(feature):
    for scenario in feature['elements']:
        if 'result' not in scenario['steps'][0].keys():
            feature['elements'].remove(scenario)     
                    
if __name__ == "__main__":
    main()
