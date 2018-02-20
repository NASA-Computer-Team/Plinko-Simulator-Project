//Allows for calculations to be done on output array of plinko simulator
//Drew Gill and Siyu Chen for NASA Collaboration Project

//using array of size N, where midpoint is 0, find mean and standard deviation


//array is amount of instances of each value (index)
var plinkoArray = [0, 2, 3, 2, 2, 2, 0, 1, 1, 100];
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
function standDev(dataArray, mean){
  var sum = 0;
  var m = mean;
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


//Returns percent of balls within n standard deviations
function findGaussian(dataArray, inMean, inSx){
	var amountArray = [0,0,0,0]; //index 0 = total, index 1 = 3sX, 2 = 2sX, 3 = 1sX
	for (var i = 0; i < dataArray.length; i++){
		if (i >= (inMean - (1*inSx)) && i <= (inMean + (1*inSx))){
			amountArray[3] += dataArray[i];
		}
		if (i >= (inMean - (2*inSx)) && i <= (inMean + (2*inSx))){
			amountArray[2] += dataArray[i];
		}
		if (i >= (inMean - (3*inSx)) && i <= (inMean + (3*inSx))){
			amountArray[1] += dataArray[i];
		}
		amountArray[0] += dataArray[i];
	}
	
	s1 = (amountArray[3]/amountArray[0]);
	s2 = (amountArray[2]/amountArray[0]);
	s3 = (amountArray[1]/amountArray[0]);
	return [s1,s2,s3];
}

//returns PROPORTIONS
//Ideal: 68-95-99.7
//s1 = proportion within 1 sx, s2 = 2sx, s3 = 3sx



function totalBalls(dataArray){
  var n = 0;
  for (var i = 0; i < dataArray.length; i++){
    n += dataArray[i];
  }
  return n;
}


//function per ball
//returns array total[0], mean[1], sx[2], stdmean[3], gaussian%[4]

function newBall(dataArray){
  var total = totalBalls(dataArray);
	var mean = findMean(dataArray);
	var sX = standDev(dataArray, mean);
	var gaussian = findGaussian(dataArray, mean, sX);
	var nullHyp = nullHypothesis(zStats(gaussian, total));
	
	var standDevMean = (sX/Math.sqrt(total));
	
	return [total, mean, sX, standDevMean, gaussian, nullHyp];
  }
  
  
  
/*H0: p = 0.68
Ha: p != 0.68

z1 = (s1 - p)/sqrt((p(1-p)/total)
z2 = (s2 - p)/sqrt((p(1-p)/total)
z3 = (s3 - p)/sqrt((p(1-p)/total)

|z| < 1.96 , then p-value > 0.05
fail to reject
|z| > 1.96, then p value < 0.05
reject null, conclude Ha, differs from normal curve



*/

//Returns z test statistic of difference from z1 
  function zStats(gaus, tot){
    z1 = (gaus[0] - 0.68)/Math.sqrt(0.2176/tot);
    z2 = (gaus[1] - 0.95)/Math.sqrt(.0475/tot);
    z3 = (gaus[2] - 0.997)/Math.sqrt(.002991/tot);
    
    var curve = [z1, z2, z3];
    
    return curve;
  }
  
  
//if false, fail to reject the null hypothesis (the given sample follows a normal distribution)
//if true, reject the normal hypothesis (the given sample does not follow a normal distribution)
  function nullHypothesis(zStat){
    var rejectNull = [false, false, false];
    
    
    if (Math.abs(zStat[0]) > 1.96)
      rejectNull[0] = true;
    if (Math.abs(zStat[1]) > 1.96)
      rejectNull[1] = true;
    if (Math.abs(zStat[2]) > 1.96)
      rejectNull[2] = true;  
      
    return rejectNull;
  }
  
  console.log(newBall(plinkoArray));
