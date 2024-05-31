import graphviz
from tabulate import tabulate
class MealyMachine:
    break_states=[]
    def __init__(self, states, inputs, transitions, initial_state):
        self.states = states
        self.inputs = inputs
        self.transitions = transitions
        self.initial_state = initial_state
    @classmethod
    
    def from_user_input(cls):
        states = input("Enter states separated by commas: ").split(',')
        inputs = input("Enter inputs separated by commas: ").split(',')
        transitions = {}
        initial_state = input("Enter initial state: ")
        rows = 10
        cols = 10
        array_2d = [[] for _ in range(rows)]
        

        for state in states:
            transitions[state] = {}
            for inp in inputs:
                next_state_output = input(f"Enter next state and output for input {inp} and state {state} (comma-separated): ")
                next_state, output = next_state_output.split(',')
                index=ord(next_state)-65
                array_2d[index].append(output)
                transitions[state][inp] = (next_state, output)
        c=0
        k=0

        for row in array_2d:
            if row:  
                first = row[0]
                count = 1
                for number in row[1:]:
                    if number != first:
                        cls.break_states.append(chr(c + 65))
                        break
            c += 1
        print("States to be splitted:")
        print(cls.break_states)
        

        return cls(states, inputs, transitions, initial_state)

    def to_moore(self):
        moore_transitions = {}
        moore_outputs = {}
        moore_states = []

        for state in self.states:
            moore_transitions[state] = {}
            moore_states.append(state)
        for state in self.states:
            for input_symbol, (next_state, output) in self.transitions[state].items():
                if state in MealyMachine.break_states:
                    moore_outputs[state]=""
                    new_state = state+'_' + output
                    moore_states.append(new_state)
                    moore_transitions[new_state] = {}
                    moore_outputs[new_state] = output
                    moore_transitions[state][input_symbol] = next_state+'_'+output
                else:
                    moore_transitions[state][input_symbol] = next_state
                    if next_state not in moore_outputs:
                        moore_outputs[next_state] = output


        for state in self.states:
            # print("State ",state)
            for input_symbol, (next_state, output) in self.transitions[state].items():
                if state in MealyMachine.break_states:
                    state=state
                    
                else:
                    if state==next_state:
                        moore_transitions[state][input_symbol] = next_state
                    else:
                        moore_transitions[state][input_symbol] = next_state+'_'+output
                        if next_state not in moore_outputs:
                            moore_outputs[next_state] = output
        for state in moore_states:
            if '_' in state:
                moore_transitions[state]=moore_transitions[state[0]]
        for s in MealyMachine.break_states:
            moore_states.remove(s)
        

        
        table_data=[]
        for state in moore_states:
            first_key, second_key = moore_transitions[state].keys()
            if state in moore_outputs:
                row=[state,moore_transitions[state][first_key],moore_transitions[state][second_key],moore_outputs[state]]
            else:
                row=[state,moore_transitions[state][first_key],moore_transitions[state][second_key],'']
            table_data.append(row)


        print(tabulate(table_data, headers=["State", f"{first_key}", f"{second_key}", "Output"], tablefmt="github"))
        
        return MooreMachine(moore_states, self.inputs, moore_outputs, moore_transitions, self.initial_state)

    def draw_graph(self, filename):
        dot = graphviz.Digraph()
        dot.attr(rankdir='LR')

        for state in self.states:
            dot.node(state, label=state)

        for state in self.states:
            for input_symbol, (next_state, output) in self.transitions[state].items():
                dot.edge(state, next_state, label=f"{input_symbol}/{output}")

        dot.render(filename, format='png', cleanup=True)
        print(f"Mealy Graph saved as {filename}.png")

class MooreMachine:
    def __init__(self, states, inputs, outputs, transitions, initial_state):
        self.states = states
        self.inputs = inputs
        self.outputs = outputs
        self.transitions = transitions
        self.initial_state = initial_state

    def draw_graph(self, filename):
        dot = graphviz.Digraph()
        dot.attr(rankdir='LR')

        for state in self.states:
            if state in self.outputs:
                dot.node(state, label=f"{state}/{self.outputs[state]}")
            else:
                dot.node(state)

        for state in self.states:
            for input_symbol, next_state in self.transitions[state].items():
                dot.edge(state, next_state, label=input_symbol)

        dot.render(filename, format='png', cleanup=True)
        print(f"Moore Graph saved as {filename}.png")
class FiniteStateMachine:
    def __init__(self, states, inputs, outputs, transitions, initial_state):
        self.states = states
        self.inputs = inputs
        self.outputs = outputs
        self.transitions = transitions
        self.initial_state = initial_state

    def generate_diagram(self):
        dot = graphviz.Digraph()
        dot.attr(rankdir='LR')
        for state in self.states:
            dot.node(state, label=f"{state}/{self.outputs[state]}")
        dot.node('empty', shape='point')
        dot.edge('empty', self.initial_state)
        for transition in self.transitions:
            dot.edge(transition[0], transition[2], label=transition[1])
        return dot

    def convert_to_output_enhanced(self):
        output_enhanced_transitions = []
        for transition in self.transitions:
            output = self.outputs[transition[2]]  # Output associated with the next state A,0,B
            output_enhanced_transitions.append((transition[0], transition[1], transition[2], output))#A,0,B,b
            
        data=[]
        for i in range(0, len(output_enhanced_transitions), 2):
            instance1 = output_enhanced_transitions[i]#A 0 B b
            instance2 = output_enhanced_transitions[i + 1]#A 1 A b
            r=[instance1[0],instance1[2]+","+instance1[3],instance2[2]+","+instance2[3]]#A    B,b    A,b
            first_key=instance1[1]
            second_key=instance2[1]
            data.append(r)
            # print(instance1,instance2)

        
        print(tabulate(data, headers=["State", f"{first_key}", f"{second_key}"], tablefmt="github"))


        return OutputEnhancedStateMachine(self.states, self.inputs, output_enhanced_transitions, self.initial_state)

class OutputEnhancedStateMachine:
    def __init__(self, states, inputs, transitions, initial_state):
        self.states = states
        self.inputs = inputs
        self.transitions = transitions
        self.initial_state = initial_state

    def generate_diagram(self):
        dot = graphviz.Digraph()
        dot.attr(rankdir='LR')
        dot.attr('node', shape='circle')
        for state in self.states:
            dot.node(state)
        dot.node('empty', shape='point')
        dot.edge('empty', self.initial_state)
        for transition in self.transitions:
            dot.edge(transition[0], transition[2], label=f"{transition[1]} / {transition[3]}")
        return dot

# main()
while True:
        conversion_type = input("Enter '1' to convert Moore to Mealy or '2' to convert Mealy to Moore: ")
        if conversion_type=='1':
            states = input("Enter states for Finite State Machine (comma-separated): ").split(',')
            inputs = input("Enter inputs for Finite State Machine (comma-separated): ").split(',')
            outputs = {}
            for state in states:
                outputs[state] = input(f"Enter output for state {state}: ")#outputs[A]=b
            transitions = []
            while True:
                transition = input("Enter transition (from_state,input,to_state) or type 'done' to finish: ")#A,0,B
                if transition == 'done':
                    break
                transitions.append(tuple(transition.split(',')))
            initial_state = input("Enter initial state for Finite State Machine: ")

            
            finite_state_machine = FiniteStateMachine(states, inputs, outputs, transitions, initial_state)

            
            fs_diagram = finite_state_machine.generate_diagram()
            fs_diagram.render('finite_state_machine_diagram', format='png', cleanup=True)

            
            output_enhanced_machine = finite_state_machine.convert_to_output_enhanced()

            
            oe_diagram = output_enhanced_machine.generate_diagram()
            oe_diagram.render('output_enhanced_machine_diagram', format='png', cleanup=True)
        elif conversion_type=='2':
            mealy_machine = MealyMachine.from_user_input()
            moore_machine = mealy_machine.to_moore()

            mealy_machine.draw_graph("mealy_machine")
            moore_machine.draw_graph("moore_machine")
        else:
            print("Invalid input. Please enter either '1' or '2'.")

        continue_execution = input("Do you want to perform another conversion? (yes/no): ")
        if continue_execution.lower() != 'yes':
            break
