# Cubo semantico para MYRLike
# Utilizando logica entera

CS = {
    'int': {
        'int': {
            'PLUS': 'int',
            'MINUS': 'int',
            'TIMES': 'int',
            'DIVIDE': 'float',
            'LT': 'int',
            'LTE': 'int',
            'GT': 'int',
            'GTE': 'int',
            'EQ': 'int',
            'NE': 'int',
            'OR': 'int',
            'AND': 'int'
        },
        'float': {
            'PLUS': 'float',
            'MINUS': 'float',
            'TIMES': 'float',
            'DIVIDE': 'float',
            'LT': 'int',
            'LTE': 'int',
            'GT': 'int',
            'GTE': 'int',
            'EQ': 'int',
            'NE': 'int',
            'OR': 'int',
            'AND': 'int'
        },
        'char': {
            'PLUS': 'int',
            'MINUS': 'int',
            'TIMES': 'int',
            'DIVIDE': 'float',
            'LT': 'int',
            'LTE': 'int',
            'GT': 'int',
            'GTE': 'int',
            'EQ': 'int',
            'NE': 'int',
            'OR': 'int',
            'AND': 'int'
        }
    },
    'float': {
        'int': {
            'PLUS': 'float',
            'MINUS': 'float',
            'TIMES': 'float',
            'DIVIDE': 'float',
            'LT': 'int',
            'LTE': 'int',
            'GT': 'int',
            'GTE': 'int',
            'EQ': 'int',
            'NE': 'int',
            'OR': 'int',
            'AND': 'int'
        },
        'float': {
            'PLUS': 'float',
            'MINUS': 'float',
            'TIMES': 'float',
            'DIVIDE': 'float',
            'LT': 'int',
            'LTE': 'int',
            'GT': 'int',
            'GTE': 'int',
            'EQ': 'int',
            'NE': 'int',
            'OR': 'int',
            'AND': 'int'
        },
        'char': {
            'PLUS': 'float',
            'MINUS': 'float',
            'TIMES': 'float',
            'DIVIDE': 'float'
        }
    },
    'char': {
        'int': {
            'PLUS': 'int',
            'MINUS': 'int',
            'TIMES': 'int',
            'DIVIDE': 'float',
            'LT': 'int',
            'LTE': 'int',
            'GT': 'int',
            'GTE': 'int',
            'EQ': 'int',
            'NE': 'int',
            'OR': 'int',
            'AND': 'int'
        },
        'float': {
            'PLUS': 'float',
            'MINUS': 'float',
            'TIMES': 'float',
            'DIVIDE': 'float'
        },
        'char': {
            'PLUS': 'char',
            'MINUS': 'char',
            'TIMES': 'int',
            'LT': 'int',
            'LTE': 'int',
            'GT': 'int',
            'GTE': 'int',
            'EQ': 'int',
            'NE': 'int',
            'OR': 'int',
            'AND': 'int'
        }
    }
}

if __name__ == "__main__":
    print("Cubo semantico MYRLike:\n")
    for LeftOperator, LOValue in CS.items():
        print(LeftOperator)
        for RightOperator, ROValue in LOValue.items():
            print("\t" + RightOperator)
            for Operator, Value in ROValue.items():
                print("\t\t" + Operator + " : " + Value)