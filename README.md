# deruuk (progress)

this is a lisp dialect act like programing langue in deutche sprech, Русский язык and Українська мова


### examples
4 ways to do hello
hello word

	(print "hello word")

hello word in german langague

	(drucken "Hallo Welt")


hello word in russian langague

	(печать "привет Мир")

hello word in ukrain langague

	(друк "привіт світ")


**more examples**

great you

	(drucken "hallo" (eingabe "your name\n"))

create a fucntion to sum numbers from 0 to a 

	(леть sum (фн [a] (/ ( * a (+ a 1) ) 2)))
	(sum 100)

sum 2 numbers gived by the user

	 (+ (входнойавтомат) (входнойавтомат))

check if even or odd

	 (wenn (== (% (eingabeautomatik) 2) 0 ) (drucken "even") (drucken "odd") )


Factorial

	(леть fac  (фн [n] (если (== n 1 ) 1 (* n (fac (- n 1))) )) )


Some syntaxis sugar

	(+ 2  3 12 3 412)
	(* 2  3 12 3 412)
	

### References

https://github.com/fluentpython/lispy

https://norvig.com/lispy.html

https://github.com/kanaka/mal
