Name: Charles Liu
MIT Email: cliu2014@mit.edu

Q1:How long did the assignment take?:
{A1: 8 hours}

Q2:Potential issues with your solution and explanation of partial completion (for partial credit):
{A2: I couldn't tell whether my log SNR output is correct although it resembles the ones on the lecture slides. Everything else gives reasonable output.}

Q3:Any extra credit you may have implemented:
{A3: None}

Q4:Collaboration acknowledgement (but again, you must write your own code):
{A4: Ryan Lacey}

Q5:What was most unclear/difficult?:
{A5: It was difficult to test some things like log SNR without any examples. Also the offests for Green did not match the same for the others.}

Q6:What was most exciting?:
{A6: The things working}

Q7:What ISO has better SNR?:
{A7: ISO3200. Likely because the 400 image is underexposed, so less signal in the dark areas. With no scale factor (scale=1), log(SNR_400) = 1.233, log(SNR_3200) = 1.711 when averaged over all channels and pixels.}

Q8:Which direction you decided to interpolate along for the edgeBasedGreenChannel?:
{A8: Both, depending on the situation. At each pixel, calculate whether vertical or horizontal difference is smaller and go that way.}