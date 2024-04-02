


from src.evaluation import evaluate_results

path='datasets/target/SemEval2017_GPT3/'

n= 5
print('N: '+str(n))
print('topic_rank')
evaluate_results(path+'keys/', path+'topic/',n)
print('rake')

evaluate_results(path+'keys/', path+'rake/',n)
print('yake')
evaluate_results(path+'keys/', path+'yake/',n)