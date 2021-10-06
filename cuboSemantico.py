# Cubo semantico para MYRLike
# Utilizando logica entera

CS = {
    'INT': {
        'INT': {
            'PLUS': 'INT',
            'MINUS': 'INT',
            'TIMES': 'INT',
            'DIVIDE': 'FLOAT',
            'LT': 'INT',
            'LTE': 'INT',
            'GT': 'INT',
            'GTE': 'INT',
            'EQ': 'INT',
            'NE': 'INT',
            'OR': 'INT',
            'AND': 'INT'
        },
        'FLOAT': {
            'PLUS': 'FLOAT',
            'MINUS': 'FLOAT',
            'TIMES': 'FLOAT',
            'DIVIDE': 'FLOAT',
            'LT': 'INT',
            'LTE': 'INT',
            'GT': 'INT',
            'GTE': 'INT',
            'EQ': 'INT',
            'NE': 'INT',
            'OR': 'INT',
            'AND': 'INT'
        },
        'CHAR': {
            'PLUS': 'INT',
            'MINUS': 'INT',
            'TIMES': 'INT',
            'DIVIDE': 'FLOAT',
            'LT': 'INT',
            'LTE': 'INT',
            'GT': 'INT',
            'GTE': 'INT',
            'EQ': 'INT',
            'NE': 'INT',
            'OR': 'INT',
            'AND': 'INT'
        }
    },
    'FLOAT': {
        'INT': {
            'PLUS': 'FLOAT',
            'MINUS': 'FLOAT',
            'TIMES': 'FLOAT',
            'DIVIDE': 'FLOAT',
            'LT': 'INT',
            'LTE': 'INT',
            'GT': 'INT',
            'GTE': 'INT',
            'EQ': 'INT',
            'NE': 'INT',
            'OR': 'INT',
            'AND': 'INT'
        },
        'FLOAT': {
            'PLUS': 'FLOAT',
            'MINUS': 'FLOAT',
            'TIMES': 'FLOAT',
            'DIVIDE': 'FLOAT',
            'LT': 'INT',
            'LTE': 'INT',
            'GT': 'INT',
            'GTE': 'INT',
            'EQ': 'INT',
            'NE': 'INT',
            'OR': 'INT',
            'AND': 'INT'
        },
        'CHAR': {
            'PLUS': 'FLOAT',
            'MINUS': 'FLOAT',
            'TIMES': 'FLOAT',
            'DIVIDE': 'FLOAT'
        }
    },
    'CHAR': {
        'INT': {
            'PLUS': 'INT',
            'MINUS': 'INT',
            'TIMES': 'INT',
            'DIVIDE': 'FLOAT',
            'LT': 'INT',
            'LTE': 'INT',
            'GT': 'INT',
            'GTE': 'INT',
            'EQ': 'INT',
            'NE': 'INT',
            'OR': 'INT',
            'AND': 'INT'
        },
        'FLOAT': {
            'PLUS': 'FLOAT',
            'MINUS': 'FLOAT',
            'TIMES': 'FLOAT',
            'DIVIDE': 'FLOAT'
        },
        'CHAR': {
            'PLUS': 'CHAR',
            'MINUS': 'CHAR',
            'TIMES': 'INT',
            'LT': 'INT',
            'LTE': 'INT',
            'GT': 'INT',
            'GTE': 'INT',
            'EQ': 'INT',
            'NE': 'INT',
            'OR': 'INT',
            'AND': 'INT'
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