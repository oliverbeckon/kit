
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

        comparison and comparison
            return true if both comparisons return true

        comparison or comparison
            return true if one of the comparisons return true

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


        if booleanExpression {body} 
            executes body if booleanExpression returns True
        

        else if booleanExpression {body}
            executes body if previous if or else if statements booleanExpressions returns false and booleanExpression returns True
        

        else {body}
            executes body if all previous if or else if statements booleanExpressions return false


    Functions
        funcname = f(arg1, arg2) {body}
            creates function with the name 'funcname' that when called using funcname(arg1, arg2) will execute body 
        
        return x
            used in a function to return a variable x
        
         




Examples:
    basic FizzBuzz

        for i ++: 100 {
            if i % 5 == 0 and i % 3 == 0 {
                say("FizzBuzz")
            } else if i % 5 == 0 {
                say("Buzz")
            } else if i % 3 == 0 {
                say("Fizz")
            } else {
                say(i) 
            }
        }



