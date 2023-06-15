/*----HEADER----*/
package main;

import(
        "fmt"
);

var t0, t1 float64;
var P, H float64;
var stack [30101999]float64;
var heap [30101999]float64;

func main(){
        t0 = 5 * 6;
        t1 = 4 + t0;
        fmt.Printf("%d", int(t1));
};