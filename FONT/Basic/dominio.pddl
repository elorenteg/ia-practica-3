(define (domain tareas-basic)
    (:requirements :adl :typing :strips)
    (:types
        tarea programador - object
    )
    
    (:predicates
        (servida ?t - tarea)
    )
    
    (:functions
        (dtarea ?t - tarea)
        (ttarea ?t - tarea)
        
        (hprog ?p - programador)
        (cprog ?p - programador)
        (tprog ?p - programador)
    )
    
    (:action realiza
        :parameters (?t - tarea ?p - programador)
        :precondition (and (not (servida ?t))
                           (<= (dtarea ?t) (+ (hprog ?p) 1)))
        :effect (and (servida ?t)
                     (increase (tprog ?p) (ttarea ?t))
                     (when (= (dtarea ?t) (+ (hprog ?p) 1)) (increase (tprog ?p) 2)))
    )
)
