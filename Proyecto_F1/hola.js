// Entorno Global
let a = 10;
let b = 20;
console.log(a);

console.log(a>b);

if(a>b){
    console.log(a);
    console.log(a>b);
    if(a==10){
    }
}

if(a>b){
    console.log(a);
    console.log(a>b);
    if(a==10){
    }
}else{
    console.log(b);
    console.log(a<b);
}

//  {anterior: none, a:10, b:20, entorno_if: { anterior: 'superior' } }