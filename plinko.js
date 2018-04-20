
  //Allows for calculations to be done on output array of plinko simulator
//Drew Gill and Siyu Chen for NASA Collaboration Project

//using array of size N, where midpoint is 0, find mean and standard deviation


//array is amount of instances of each value (index)
var plinkoArray = [1, 2, 3, 4, 5, 6, 7, 8, 7, 6, 5, 4, 3, 1];
//finding mean
function findMean(dataArray, total){
  let sum = 0;
  for (var i = 0; i < dataArray.length; i++){
    sum += i*dataArray[i];
  }
  var mean = sum/total;
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

  /*CHI SQUARED TESTING
  Can't use individual z-testing
  Use Chi-Squared Goodness of Fit test
  Sum of (o-e)^2/e
  (gaus[0] - 0.68)^2 / 0.68
  (gaus[1] - 0.95)^2 / 0.95
  (gaus[2] - 0.997)^2 / 0.997
  Assume alpha = 0.05
  H0 = distribution follows normal distribution
  Ha = distribution does not follow normal distribution
  df = 2
  if sum >= 5.99, p is low, reject null
  */
  function chiTestStatistic(gaus){
    var chiSquared = 0;
    chiSquared += (Math.pow((gaus[0]*100 - 68), 2))/68;
    chiSquared += (Math.pow((gaus[1]*100 - 95), 2))/95;
    chiSquared += (Math.pow((gaus[2]*100 - 99.7), 2))/99.7;
    var isNormal = (chiSquared < 5.99);
    return [chiSquared, isNormal];
  }
  
  //function per ball
//returns array total[0], mean[1], sx[2], stdmean[3], gaussian%[4]
  function newBall(dataArray, total){
  	var mean = findMean(dataArray, total);
  	var sX = standDev(dataArray, mean);
  	var gaussian = findGaussian(dataArray, mean, sX);
  	var chiSquaredValue = chiTestStatistic(gaussian)[0];
  	var normalTest = chiTestStatistic(gaussian)[1];
  	var standDevMean = (sX/Math.sqrt(total));
  	//key-value pairs
    var dict = {
      "total": total,
      "mean": mean,
      "standDev": sX,
      "standDevMean": standDevMean,
      "gaussian": gaussian,
      "nullHyp": nullHyp,
      "X2value": chiSquaredValue,
      "isNormal": normalTest
    };
	return dict;
  }
console.log(newBall(plinkoArray));
