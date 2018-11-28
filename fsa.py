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
        self.num_states = self.get_number_of_states(genome)
        self.new_states_no_food = []
        self.actions_no_food = []
        self.new_states_food = []
        self.actions_food = []
        self.start_state = self.get_start_state(genome)
        self.create_fenotype(genome)
    
    def get_number_of_states(self, genome):
        return int((len(genome) - 4)/12)
    
    def get_start_state(self, genome):
        return bits2int(genome[0:4])
    
    def create_fenotype(self, genome):
        for s in range(0, self.num_states):
            self.new_states_no_food.insert(s, bits2int( genome[(4 + s*12):(8 + s*12)] ) )
            self.actions_no_food.insert(s, bits2int( genome[(8 + s*12):(10 + s*12)] ) )

            self.new_states_food.insert(s, bits2int( genome[(10 + s*12):(14 + s*12)] ) )
            self.actions_food.insert(s, bits2int( genome[(14 + s*12):(16 + s*12)] ) )
