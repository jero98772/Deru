(defun check-even-or-odd (n)
  (if (evenp n)
      'even
      'odd))

;; Test the check-even-or-odd function
(write (check-even-or-odd 11))  ; Checks if 10 is even or odd


(defun assess-grade (score)
  (cond ((>= score 90) "A")
        ((>= score 80) "B")
        ((>= score 70) "C")
        ((>= score 60) "D")
        ((>= score 50) "E")
        (t "F")))

(defun determine-fruit-color (fruit)
  (case fruit
    ((apple) 'red)
    ((banana) 'yellow)
    ((cherry) 'red)
    (t 'unknown)))

;; Test the determine-fruit-color function
(write (determine-fruit-color 'banana))  ; Determines the color of a banana

;; Test the assess-grade function
(write (assess-grade 50))  ; Assesses grade based on the score