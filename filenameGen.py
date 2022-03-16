import os


def getfilenames():
    files = []
    for i in range(20):
        filename = 'mobileshop-ug-list-'+str(i)+'.html'
        files.append(filename)
        if os.path.exists(filename):
            os.remove(filename)
    if os.path.exists('products_list.csv'):
        os.remove('products_list.csv')
    if os.path.exists('products_list.json'):
        os.remove('products_list.json')
    return files


if __name__ == '__main__':
    file = getfilenames()
