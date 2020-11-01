import os
import script.data as data

data.merge_data()

for folder in ['bs', 'is', 'isq']:
    for f in os.listdir('data/' + folder):
        if f.endswith('.csv'):
            print("remove: " + f)
            os.remove(os.path.join('data', folder, f))
