'''
Created on May 15, 2014

@author: daniel
'''

if __name__ == '__main__':
    """
    input: Config file, dataset
    output: stores model in modelfile 
    """
    load config
    load dataset
    init_model(config)
    load model params/preprocessing options
    
    cross validation loop (option)
        model.fit()
        evaluate model
        
    fit model on complete dataset (option)
    eval model on complete dataset (option)
    save model (option)
    
    pass