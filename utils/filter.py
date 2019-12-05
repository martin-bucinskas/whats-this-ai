import os
from PIL import Image

count = 0

for filename in os.listdir('data/animal/'):
    if filename.endswith('.jpg'):
        try:
            img = Image.open('data/animal/' + filename)
            img.verify()
            img.save('data/animal/' + filename + '.png')
            os.remove('data/animal/' + filename)
        except(IOError, SyntaxError) as e:
            print('Bad File: ' + filename)
            count = count + 1
            print(count)
            os.remove('data/animal/' + filename)

for filename in os.listdir('data/mineral/'):
    if filename.endswith('.jpg'):
        try:
            img = Image.open('data/mineral/' + filename)
            img.verify()
            img.save('data/mineral/' + filename + '.png')
            os.remove('data/mineral/' + filename)
        except(IOError, SyntaxError) as e:
            print('Bad File: ' + filename)
            count = count + 1
            print(count)
            os.remove('data/mineral/' + filename)

for filename in os.listdir('data/vegetable/'):
    if filename.endswith('.jpg'):
        try:
            img = Image.open('data/vegetable/' + filename)
            img.verify()
            img.save('data/vegetable/' + filename + '.png')
            os.remove('data/vegetable/' + filename)
        except(IOError, SyntaxError) as e:
            print('Bad File: ' + filename)
            count = count + 1
            print(count)
            os.remove('data/vegetable/' + filename)
