
import os
from src.AKEs import TopicRankExtractor,TextRankExtractor,SingleRankExtractor,YakeExtractor,RakeExtractor

def read_file_content(path):
    with open(path, 'r') as file:
        text = file.read().replace('\n', '')
    return text
def write_list_file(filepath, list, mode='w'):
    with open(filepath, mode) as archivo:
        for element in list:
            archivo.write(str(element) + '\n')

path='datasets/test/docsutf8/'
outputpath='datasets/test/'

n=10

files= os.listdir(path)
print(files)

tpr = TopicRankExtractor()
textr =TextRankExtractor()
singr =SingleRankExtractor()
yakee = YakeExtractor()
rake = RakeExtractor()

os.mkdir(outputpath+'topic')
os.mkdir(outputpath+'rake')
os.mkdir(outputpath+'yake')
os.mkdir(outputpath+'topic/res'+str(n)+'/')

os.mkdir(outputpath+'rake/res'+str(n)+'/')
os.mkdir(outputpath+'yake/res'+str(n)+'/')



for f in files:
    text= read_file_content(path+f)
    keywords= tpr.extract_best(text,n)
    print(keywords,len(keywords))
    write_list_file(outputpath+'topic/res'+str(n)+'/'+f.replace('.txt','.key'),keywords)

    keywords=yakee.extract_n_best(text,n)

    print(keywords,len(keywords))
    write_list_file(outputpath+'yake/res'+str(n)+'/'+f.replace('.txt','.key'),keywords)

    keywords = rake.extract_best(text,n)
    write_list_file(outputpath+'rake/res'+str(n)+'/'+f.replace('.txt','.key'),keywords)

    print(keywords,len(keywords))

    print('----')








