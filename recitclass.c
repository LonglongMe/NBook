#include <stdio.h>
#define N 10+10
#define MORE(x) (x+1)
int main(){
    int i=0,j=10;
    int* p=NULL;
    if (i>10){p=&i;}
    //else p=&j;
    if (p==NULL){printf("shit!");p=&j;}
    printf("%d %d %d %d %d",i,&i,*p,&p,p);
}

    /*
    int a=N;
    int b=0;
    MORE(b);
    printf("%d",b);
    //for (int b=0;b<5;MORE(b)){printf("%d",b);}
    //printf("%d",b);
    */