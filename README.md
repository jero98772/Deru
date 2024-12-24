# Deru 🚀

Deru is a Lisp dialect designed to support programming in German (Deutsche Sprache), Russian (Русский язык).

## Introduction to Lisp 🧠
Lisp (LISt Processing) is one of the oldest programming languages, known for its simple syntax and powerful macro system. It's particularly well-suited for symbolic computation and artificial intelligence applications. Deru aims to bring this powerful language into a multilingual context.

This programing language is a example to learn how to make a programming language in a easy way 

## Examples 📚

### Hello World in Four Languages 🌍

**English:**
```lisp
(print "hello world")
```

**German:**
```lisp
(drucken "Hallo Welt")
```

**Russian:**
```lisp
(печать "привет Мир")
```

### More Examples ✨

**Greet the user:**
```lisp
(drucken "hallo" (eingabe "your name\n"))
```

**Create a function to sum numbers from 0 to a:**
```lisp
(леть sum (фн [a] (/ ( * a (+ a 1) ) 2)))
(sum 100)
```

**Sum two numbers given by the user:**
```lisp
(+ (входнойавтомат) (входнойавтомат))
```

**Check if a number is even or odd:**
```lisp
(wenn (== (% (eingabeautomatik) 2) 0 ) (drucken "even") (drucken "odd"))
```

**Factorial:**
```lisp
(леть fac (фн [n] (если (== n 1 ) 1 (* n (fac (- n 1))) )))
```

**Fibonacci:**
```lisp
(let fibonacci (fn [n] (если (<= n 1) n (+ (fibonacci (- n 1)) (fibonacci (- n 2))))))
```

**Syntax Sugar:**
```lisp
(+ 2 3 12 3 412)
(* 2 3 12 3 412)
```

## How to Run 🏃‍♂️

1. Clone the repository:
    ```bash
    git clone https://github.com/jero98772/deruuk.git
    cd deruuk
    ```

2. Run the main script:
    ```bash
    python main.py
    ```

## Future Plans 🌟
We are working on integrating Rust to add Tail Call Optimization (TCO) to improve performance. The related code is currently commented out.

## References 🔗

- [Lispy by Fluent Python](https://github.com/fluentpython/lispy)
- [Norvig's Lispy](https://norvig.com/lispy.html)
- [Make a Lisp (mal) by Kanaka](https://github.com/kanaka/mal) <- give a star to this code i get most of this code from here
