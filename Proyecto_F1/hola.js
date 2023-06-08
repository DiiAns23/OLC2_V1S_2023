// Entorno Global
let a = 10;

// Entorno de Local
if(true) {
    a = 30;
    console.log(a);
}

console.log(a);