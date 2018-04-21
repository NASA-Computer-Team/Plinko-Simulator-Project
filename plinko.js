
//Allows for calculations to be done on output array of plinko simulator
//Drew Gill and Siyu Chen for NASA Collaboration Project
//Graphically displayed and simulated in program by Pedro Moter


//array is amount of instances of each value (index)
var plinkoArray = [1, 2, 50, 4, 5, 6, 50, 3, 7, 6, 5, 4, 3, 2, 1]; //SAMPLE ARRAY
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
  DETERMINE IF DISTRIBUTION IS NORMAL
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
  
  RETURNS true if is normal (cannot reject null), false if null hyp is rejected
  */
  function chiTestStatistic(gaus){
    var chiSquared = 0;
    chiSquared += (Math.pow((gaus[0]*100 - 68), 2))/68;
    chiSquared += (Math.pow((gaus[1]*100 - 95), 2))/95;
    chiSquared += (Math.pow((gaus[2]*100 - 99.7), 2))/99.7;
    var isNormal = (chiSquared < 5.99);
    return [chiSquared, isNormal];
  }
  
  /*Hypothesis Test for mean
  H0: mean == 0
  HA: mean != 0
  alpha = 0.05
  assume df > 1000
  returns true if H0 is rejected and HA is true, false if H0 cannot be rejected
  
  return[0] = t-test statistic, return[1] = result of test
  */
  function hypTestForMean(dataArray, mean, total, std){
    var t = Math.abs((mean - ((dataArray.length - 1)/2))/(std/Math.sqrt(total))); //t-test statistic
    return [t, (t < 1.96)];
  }
  
  
  //function per ball
//returns array total[0], mean[1], sx[2], stdmean[3], gaussian%[4]
  function newBall(dataArray, total){
  	var mean = findMean(dataArray, total);
  	var sX = standDev(dataArray, mean);
  	var gaussian = findGaussian(dataArray, mean, sX);
  	var chiTestResult = chiTestStatistic(gaussian);
  	var chiSquaredValue = chiTestResult[0];
  	var normalTest = chiTestResult[1];
  	var hypTestResult = hypTestForMean(dataArray, mean, total, sX);
  	var tTestStat = hypTestResult[0];
  	var nullHyp = hypTestResult[1];
  	var standDevMean = (sX/Math.sqrt(total));
  	//key-value pairs
    var dict = {
      "total": total,
      "mean": mean,
      "standDev": sX,
      "standDevMean": standDevMean,
      "gaussian": gaussian,
      "X2value": chiSquaredValue,
      "isNormal": normalTest,
      "tTestStatistic": tTestStat,
      "meanIsZero": nullHyp
    };
	return dict;
  }
console.log(newBall(plinkoArray, 156)); //58 is TESTING VALUE. Replace with TOTAL output.
