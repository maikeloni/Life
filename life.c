#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <life.h>

// execute: life "rule" -n/t/k/p string
// rule: [1234567890]/[1234567890]
// (n)ormal, (t)orus, (k)lein bottle or (p)rojective plane topology
// string is like 010/n101/n000 and gives the field of game of life (0 dead, 1 alive)

int main(int argc, char **argv)
{    
    //printf("%d\n",(50+50)%50);
    //check for (n)ormal, (t)orus, (k)lein bottle or (p)rojective plane topology
    char topology = 'n';
    char *rule="23/3";
    for (int k=1;k<argc-1;k++)
    {
        if (argv[k][0] == '-')
        {
            topology = argv[k][1];
        } else
        {
            rule=argv[k];
        }
    }
    
    //check if one string or more strings in the argument
    char *string = *(argv+argc-1);    
    int length = checkLengthOfField(string);
    char field[length][length];
    
    if (length == argc-1)
    {
        //printf("multiple strings\n");
        for (int k=1; k<length+1;k++)
        {
            for (int l=0; l<length;l++)
            {
                field[k-1][l]=argv[k][l];
            }
        }
    } else
    {
        //printf("one string\n");
        transferStringToArray(*(argv+argc-1), length, field);
    }
    
    if (printField(length,field,1))
    {
        printf("\nERROR: Field needs to consist only from zeros and ones!\n");
        return 1;
    }
    
    // Game Of Life
    char newField[length][length];
    gameOfLife(rule,length,field,newField,topology);
    printField(length,newField,0);
    return 0;
}
