from markov_chain import MarkovChain

mc = MarkovChain()
mc.read_file("./sample.txt")
#mc.print_dict()
mc.generate_text(7)
