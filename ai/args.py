from utils import dotdict

args = dotdict({
    'numIters': 3,#20, #    niii VAŽNOO, TO MORŠ V EVAL.SH
    'numEps': 4,#100,              # Number of complete self-play games to simulate during a new iteration.
    'tempThreshold': 15,        #
    'updateThreshold': 0.6,     # During arena playoff, new neural net will be accepted if threshold or more of games are won.
    'maxlenOfQueue': 90000, #200000,    # Number of game examples to train the neural networks.
    'numMCTSSims': 10, #25,          # Number of games moves for MCTS to simulate.
    'arenaCompare': 4, #40,         # Number of games to play during arena play to determine if new net will be accepted.
    'cpuct': 3,
    'timeLimit' :4.9, 

    'checkpoint': './eval/test_2/',
    'load_model': False,
    'load_folder_file': ('/dev/models/8x100x50','best.pth.tar'),
    'numItersForTrainExamplesHistory': 20,

})