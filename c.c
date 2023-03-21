
    // int i = 8;(((((((((((
int i =9;
// int y = 77;
// int x = 9999;
// while (i > 0){
//     if (i == 4) {
//         int i = i - 1;
//         continue;
//     }
//     while (i > 8){
//         i = i - 1;
//     }
//     printf("%d", i);
//     i = i - 1;
// }
// printf("%d", x);
// for (int i = 0; i < 0, i = i+1){
//     int i = 0;
// }


int x = 1;
int f;
scanf("%d", f);
printf("%d", f);
int a = 0;
int b = 1;
int c = 2;
while (x < f){
    int y = x % 3;
    int z = x % 5;
    if (y == z){
        if (y == 0){
            printf("%d", c);
        }
        else{
            printf("%d", a);
        }
    }
    else if (y == 0){
        printf("%d", b);
    }
    else if (z == 0){
        printf("%d", b);
    }
    else{
        printf("%d", a);
    }
    x = x + 1;

}
// if (y > x){
//     printf("%d", y);
//     while (x < 0){
//         printf("%d", y);
//     }
// }
// else if (y > x) {
//     printf("%d", y);
// }
// int x = 0;
// int y= 0;
// if (y > x){
//     int j = 4;
// }
// else if(y>x){
//     printf("%d", x);
// }
// int x = 5;
// int z = 0;
// while (x > 0) {
//     printf("%d", x);
//     x = x - 1;
//     z = 0;
//     while (z < 5){
//         printf("%d", z);
//         z = z + 1;
//     }
// }
// int y = 111;
// printf("%d", y);
// int num = 0;
// int j = 3;
// while (num < 3 ){
//     // j = j + num;
//     num = num - 1;
//     printf("%d", num);
// }