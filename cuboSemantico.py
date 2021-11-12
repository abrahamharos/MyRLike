# Cubo semantico para MYRLike
# Utilizando logica entera

CS = {
    'int': {
        'int': {
            '=': 'int',
            '+': 'int',
            '-': 'int',
            '*': 'int',
            '/': 'float',
            '<': 'int',
            '<=': 'int',
            '>': 'int',
            '>=': 'int',
            '==': 'int',
            '!=': 'int',
            '||': 'int',
            '&': 'int'
        },
        'float': {
            '+': 'float',
            '-': 'float',
            '*': 'float',
            '/': 'float',
            '<': 'int',
            '<=': 'int',
            '>': 'int',
            '>=': 'int',
            '==': 'int',
            '!=': 'int',
            '||': 'int',
            '&': 'int'
        },
        'char': {
            '=': 'int',
            '+': 'int',
            '-': 'int',
            '*': 'int',
            '/': 'float',
            '<': 'int',
            '<=': 'int',
            '>': 'int',
            '>=': 'int',
            '==': 'int',
            '!=': 'int',
            '||': 'int',
            '&': 'int'
        }
    },
    'float': {
        'int': {
            '=': 'float',
            '+': 'float',
            '-': 'float',
            '*': 'float',
            '/': 'float',
            '<': 'int',
            '<=': 'int',
            '>': 'int',
            '>=': 'int',
            '==': 'int',
            '!=': 'int',
            '||': 'int',
            '&': 'int'
        },
        'float': {
            '=': 'float',
            '+': 'float',
            '-': 'float',
            '*': 'float',
            '/': 'float',
            '<': 'int',
            '<=': 'int',
            '>': 'int',
            '>=': 'int',
            '==': 'int',
            '!=': 'int',
            '||': 'int',
            '&': 'int'
        },
        'char': {
            '=': 'float',
            '+': 'float',
            '-': 'float',
            '*': 'float',
            '/': 'float'
        }
    },
    'char': {
        'int': {
            '=': 'int',
            '+': 'int',
            '-': 'int',
            '*': 'int',
            '/': 'float',
            '<': 'int',
            '<=': 'int',
            '>': 'int',
            '>=': 'int',
            '==': 'int',
            '!=': 'int',
            '||': 'int',
            '&': 'int'
        },
        'float': {
            '+': 'float',
            '-': 'float',
            '*': 'float',
            '/': 'float'
        },
        'char': {
            '=': 'char',
            '+': 'char',
            '-': 'char',
            '*': 'int',
            '<': 'int',
            '<=': 'int',
            '>': 'int',
            '>=': 'int',
            '==': 'int',
            '!=': 'int',
            '||': 'int',
            '&': 'int'
        }
    }
}

def checkValidOperators(rightOperand, rightType, leftOperand, leftType, currentOperator):
    if (leftType in CS.keys()):
        if (rightType in CS[leftType].keys()):
            if (currentOperator in CS[leftType][rightType].keys()):
                resultType = CS[leftType][rightType][currentOperator]
            else:
                print('Type mismatch ' + leftType + ' and ' + rightType + ' can not use the ' + currentOperator + ' operator')
                print('Variables: ' + str(rightOperand) + ' and ' + str(leftOperand))
                exit()
        else:
            print('Type mismatch ' + leftType + ' and ' + rightType + ' can not use the ' + currentOperator + ' operator')
            print('Variables: ' + str(rightOperand) + ' and ' + str(leftOperand))
            exit()
    else:
        print('Type mismatch ' + leftType + ' and ' + rightType + ' can not use the ' + currentOperator + ' operator')
        print('Variables: ' + str(rightOperand) + ' and ' + str(leftOperand))
        exit()
    
    return resultType

if __name__ == "__main__":
    print("Cubo semantico MYRLike:\n")
    for LeftOperator, LOValue in CS.items():
        print(LeftOperator)
        for RightOperator, ROValue in LOValue.items():
            print("\t" + RightOperator)
            for Operator, Value in ROValue.items():
                print("\t\t" + Operator + " : " + Value)