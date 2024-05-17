;; Define a function to calculate the average of two numbers
(defun average (num1 num2)
  (/ (+ num1 num2) 2))

;; Call the function with two arguments and store the result in a variable
(setq result (average 10 20))

;; Print the result
(print result)  ; This will print the average of 10 and 20, which is 15

(write (* 1 2 3 4 5 6 7 ))
(print "  ")
;;(defun hello-world ()
;;  (format t "Hello, world!~%"))

;;(hello-world)
(print "  ")
(defun sum (&rest numbers)
  (apply #'+ numbers))

;; Test the sum function with different numbers of arguments
(sum 1 2 3)  ; Returns 6
(write (sum 1 2 3 4 5))  ; Returns 15
