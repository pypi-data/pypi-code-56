from StringCalculator.Calculator import MathExpressionClass


def SolveMathProblem(text: str):
    exp = MathExpressionClass(text)
    return exp.Solve()
