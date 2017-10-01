(define lelse (lambda (size level) (ldragon size (- level 1)) (tleft 90) (rdragon size (- level 1))))
(define relse (lambda (size level) (ldragon size (- level 1)) (tright 90) (rdragon size (- level 1))))
(define ldragon (lambda (size level) (if (= level 0) (tforward size) (lelse size level))))
(define rdragon (lambda (size level) (if (= level 0) (tforward size) (relse size level))))
(tinit 800 600)
(tspeed 0)
(ldragon 4 11)