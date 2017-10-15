#include <stdio.h>
#include <math.h>

int convertBinaryToDecimal(long long n)
{
    int decimalNumber = 0, i = 0, remainder;
    while (n!=0)
    {
        remainder = n%10;
        n /= 10;
        decimalNumber += remainder*pow(2,i);
        ++i;
    }
    return decimalNumber;
}

int main(void)
{
	char* s = "\u00d1"; /* Ñ */
  	printf("%d\n", convertBinaryToDecimal(10000000 & 10000000));

	return 1;
}