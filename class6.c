# include <stdio.h>
/*
int add(int *p){
    *p+=1;
}

int main(){
    int i =10;
    int *p=&i;
    add(*p);
    printf("%d %d ",p,&p );
}*/
/*
int main(){
    int a[10]={2,2,3,4,5};
    printf("sizseofa%d\n",sizeof(a));
    printf("%d %d %d %d",a[0],&a[0],&a[0]+1,*a+3);
}*/
int oddselector(int (*a)[5], int *b,int l){
    for (int i=0,l=0;i<5;i++){
        if ( a[0][i] % 2==1){
            b[l++]=a[0][i];
        }
    }
}

int main(){
    int a[1][5]={1,2,3,4,5},b[5],l=0;
    oddselector(a[0],b,l);
    for (int i=0;i<l;i++){printf("%d",b[i]);}
}