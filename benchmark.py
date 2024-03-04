


from src.evaluation import evaluate_results

path='datasets/test/'


evaluate_results(path+'keys/', path+'topic/',10)
evaluate_results(path+'keys/', path+'rake/',10)
evaluate_results(path+'keys/', path+'yake/',10)