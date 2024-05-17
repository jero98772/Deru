 ;; Define a function for addition
(defun add (a b)
  (+ a b))

;; Define a function for subtraction
(defun subtract (a b)
  (- a b))

;; Define a function for multiplication
(defun multiply (a b)
  (* a b))

;; Define a function for division
(defun divide (a b)
  (if (zerop b)
      (error "Division by zero")
      (/ a b)))

;; Function to perform calculations based on user input
(defun calculator ()
  (format t "Enter operation (+, -, *, /): ")
  (let ((operator (read-line)))
    (format t "Enter first number: ")
    (let ((num1 (read)))
      (format t "Enter second number: ")
      (let ((num2 (read)))
        (cond
          ((string= operator "+") (format t "Result: ~a~%" (add num1 num2)))
          ((string= operator "-") (format t "Result: ~a~%" (subtract num1 num2)))
          ((string= operator "*") (format t "Result: ~a~%" (multiply num1 num2)))
          ((string= operator "/") (format t "Result: ~a~%" (divide num1 num2)))
          (t (format t "Invalid operator.~%")))))))

;; Test the calculator function
(calculator)
