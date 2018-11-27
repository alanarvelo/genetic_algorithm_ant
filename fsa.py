def bits2int(ls):
    """ Takes a list of binaries, returns integer value 
    multiplies them by 2**(reverse_index).right-most element gets multiplied by 2**0 """
    s=0
    for p,i in enumerate(ls):
        s += i*2**( (len(ls)-1) - p)
    return s


class FSA:
    """ FSA Class. Takes a list of binaries, genomes, and decodes the state and actions to be taken — fenotype. """
    
    def __init__(self, genome):
        self.num_states = int((len(genome)-2)/12)
        self.actions_food = []
        self.new_states_food = []
        self.actions_no_food = []
        self.new_states_no_food = []
        self.start_state = bits2int(genome[0:2])
        self.create_fenotype(genome)
        
    
    def create_fenotype(self, genome):
        for s in range(0, self.num_states):
            self.new_states_no_food.insert(s, bits2int( genome[(2 + s*12):(6 + s*12)] ) )
            self.actions_no_food.insert(s, bits2int( genome[(6 + s*12):(8 + s*12)] ) )

            self.new_states_food.insert(s, bits2int( genome[(8 + s*12):(12 + s*12)] ) )
            self.actions_food.insert(s, bits2int( genome[(12 + s*12):(14 + s*12)] ) )
