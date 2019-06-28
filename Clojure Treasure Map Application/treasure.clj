; COMP6411 Assignment 2 
; Student Name: Prashanthi Ramesh
; Student ID: 40080517

; Treasure Hunt in Clojure
(ns clojure.assignment.comp6411
    (:gen-class))

; read data from text file
(defn read-map []
    (clojure.string/split-lines (slurp "map.txt")))  

; store map data in matrix
(def input-map (atom(to-array-2d (mapv vec (read-map)))))

; store map matrix row size
(def map-row-size (alength @input-map))

; store map matrix column size
(def map-col-size (alength (aget @input-map 0)))

; validation- every row in map matrix has same number of columns
(defn is-valid[row-size col-size]
    (def col-count (atom 0))
    (dotimes [n row-size]
        (if (= (alength(aget @input-map n)) col-size)
            (reset! col-count (inc @col-count))
            )
        )
    @col-count
    )

; print solution map matrix
(defn print-maze[maze, row-size, col-size]
    (dotimes [row row-size]  
        (dotimes [col col-size] (print (aget maze row col))) 
        (newline))
    )

; check if row and column values are with in matrix dimensions
(defn is-map-safe[maze,row-size, col-size, row,col]
    (def cond1 (>= row 0))
    (def cond2 (< row row-size))
    (def cond3 (>= col 0))
    (def cond4 (< col col-size))
    (def cond5 (= (aget maze row col) \-))
    (def cond6 (= (aget maze row col) \@))

    (and(and(and(and cond1 cond2)cond3)cond4)(or cond5 cond6))
    )


; find the path to the treasure
(defn find-path[row-size, col-size, row, col] 

    (if (and (is-map-safe @input-map row-size col-size row col) (= (aget @input-map row col) \@))
        (do
            (aset @input-map row col \@)
            (reset! input-map @input-map)
            true
            )
        (do
            (if (is-map-safe @input-map row-size col-size row col)
                (do
                    (aset @input-map row col \+)
                    (reset! input-map @input-map)

                    (if (and(and (< (inc col) col-size) (not= (aget @input-map row (inc col)) \#)) (find-path row-size col-size row (inc col)))
                        true
                        (do
                            (if (and(and (< (inc row) row-size) (not= (aget @input-map (inc row) col) \#)) (find-path row-size col-size (inc row) col))
                                true 
                                (do  
                                    (if (and(and (>= (dec row) 0) (not= (aget @input-map (dec row) col) \#)) (find-path row-size col-size (dec row) col))
                                        true
                                        (do
                                            (if (and(and (>= (dec col) 0) (not= (aget @input-map row (dec col)) \#)) (find-path row-size col-size row (dec col)))
                                                true
                                                (do
                                                    (aset @input-map row col \!)
                                                    (reset! input-map @input-map) 
                                                    false
                                                    )

                                                )
                                            )    
                                        )
                                    )
                                )
                            )
                        )
                    )
                false
                )

            )
        )
    )


; Game Starts here

; validation- check if every row in map matrix has same number of columns
(if (= (is-valid map-row-size map-col-size) map-row-size)
    (do
        (newline)
        (println "The given treasure map format is valid!")
        (newline)
        (println "This is my challenge:")
        (newline)

        ; print input map matrix
        (print-maze @input-map map-row-size map-col-size)
        (newline)
        (println "Result-")
        (newline)

        ; print result
        (if(find-path map-row-size map-col-size 0 0) (println "Woo hoo, I found the treasure :)") (println "Uh oh, I could not find the treasure :("))

        (newline)

        ; print solution map matrix
        (print-maze @input-map map-row-size map-col-size)
        (newline)

        )
    (do
        (newline)
        (println "Uh oh, the given treasure map format is invalid! Try again later ! Exiting....")
        (newline)
        )

    )


