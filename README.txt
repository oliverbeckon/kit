
Kit Syntax:
    variable assignment statement is like this
        x = 3
        y = "String"
        z = True

    Expressions
        a + b == a plus b
        a - b == a minus b
        a * b == a times b
        a / b == a divided by b
        a ** b == a to the power of b
        a // b == bth root of a
        a % b == a modulos b
     

    Comparisons
        x == b
            returns true if x equals b 

        x != b
            returns true if x doesnt equal b

        x > b
            returns true if x is greater then b

        x < b 
            returns true if x is less then b

        x >= b 
            returns true if x is greater then or equal to b

        x <= b
            return true if x is less then or equal to b

    print
        say(x) 

    comments
        #none of this will be interpreted
        this will
    
    Structures
        for x {body} 
            executes body x times inclusively


        for i ++: x {body} 
            executes body x times inclusively while incrementing i by 1 starting as 1 each time


        while booleanExpression {body} 
            executes body repeatedly until booleanExpression returns false


        ? booleanExpression {body} 
            executes body if booleanExpression returns True
        

        else? booleanExpression {body}
            executes body if previous ? or else? statements booleanExpressions returns false and booleanExpression returns True
        
        else {body}
            executes body if all previous ? or else? statements booleanExpressions return false
         


Examples:
    basic FizzBuzz

        for i ++: 100 {
            z = i % 5 + i % 3
            ? z == 0 {
                say("FizzBuzz")
            } else? i % 5 == 0 {
                say("Buzz")
            } else? i % 3 == 0 {
                say("Fizz")
            } else {
                say(i) 
            }
        }