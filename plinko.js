//using array of size N, where midpoint is 0, find mean and standard deviation

//if n%2=1 slots, midpoint is index floor((plinkoArray.length)/2)
//if n%2=0 slots, no midpoint, -1 is index ((plinkoArray.length/2)-1), +1 is index (plinkoArray.length/2)

var plinkoArray = [0, 2, 2, 2, 2, 2, 0];

//finding mean
function findMean(dataArray){
  var total = 0;
  var count = 0;
  for (var i = 0; i < dataArray.length; i++){
    total += i*dataArray[i];
    count += dataArray[i];
  }
  
  var mean = total/count;
  return mean;
}

//finding (xi - xbar)^2
function standDev(dataArray){
  var sum = 0;
  var m = findMean(dataArray);
  var count = 0;
  for (var i = 0; i < dataArray.length; i++){
    count += dataArray[i];
    for (var j = 0; j < dataArray[i]; j++){
      sum += ((i-m) * (i-m));
    }
  }
  
  var sx = Math.sqrt(sum/(count-1));
  
  return sx;
}

console.log(findMean(plinkoArray));
console.log(standDev(plinkoArray));



//for (var i = 1; i <= ; i++){
//determine where ball ends up (engine)
	var mean = findMean(plinkoArray);
	var sX = standDev(plinkoArray);
	//standDevMean = (sX/Math.sqrt(i));
  console.log("Mean = " + mean + "\nStandard Dev. = " + sX + "\nStandard Dev. of Mean = ");




var amountArray = [0,0,0,0] //index 0 = total, index 1 = 3sX, 2 = 2sX, 3 = 1sX

for (var i = 0; i < plinkoArray.length; i++){
if (i >= (mean - (1*sX)) && i <= (mean + (1*sX))){
amountArray[3] += plinkoArray[i];
}
if (i >= (mean - (2*sX)) && i <= (mean + (2*sX))){
amountArray[2] += plinkoArray[i];
}
if (i >= (mean - (3*sX)) && i <= (mean + (3*sX))){
amountArray[1] += plinkoArray[i];
}
amountArray[0] += plinkoArray[i];
}


//Ideal: 68-95-99.7
//Actual:
s1 = (amountArray[3]/amountArray[0]) * 100;
s2 = (amountArray[2]/amountArray[0]) * 100;
s3 = (amountArray[1]/amountArray[0]) * 100;


console.log(s1 + " " + s2 + " " + s3);

