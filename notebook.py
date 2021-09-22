import json
import os

TEMPLATE = os.path.join('notebook', '模版.ipynb')

def update(template, filepath): 
    ticker = os.path.basename(filepath).split(".")[0]
    template['cells'][0]['source'] = ["### {}".format(os.path.basename(os.path.dirname(filepath)))]
    template['cells'][1]['source'] = ["ticker = '{}'".format(ticker)]
    # with open(filepath) as r:
    #     rj = json.load(r)
    #     template['cells'][0] = rj['cells'][0]
    #     template['cells'][1] = rj['cells'][1]
    with open(filepath, 'w') as w:
        json.dump(template, w)


if __name__ == '__main__':
    with open(TEMPLATE) as tf:
        tj = json.load(tf)
    
    for root, dirs, files in os.walk('notebook'):
        for name in files:
            if name.endswith('.ipynb') and not name == '模版.ipynb':
                p = os.path.join(root, name)
                update(tj, p)
