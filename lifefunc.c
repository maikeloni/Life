#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <life.h>

void gameOfLife(char *ruleString, int n, char oldField[][n], char newField[][n], char topology)
{
    // check if ruleString is correct
    int aliveLength = 0, deadLength = 0, afterSlash = 0;
    while (*ruleString != '\0')
    {
        if (*ruleString != '/')
        {
            if (afterSlash)
            {
                deadLength++;
            } else
            {
                aliveLength++;
            }
        } else
        {
            afterSlash++;
        }
        ruleString++;
    }  
    
    if (afterSlash != 1 || aliveLength > 9 || deadLength > 9)
    {   // ERROR-Exception
        printf("ERROR: Rule-input should be of the form \"xxx/yyy.\n");
        return;
    } else
    {        
        ruleString -= aliveLength+deadLength+1;

        // find rule, e.g. "23/2" means:
        // living cell with 2 or 3 neighbours stays alive, otherwise dies
        // dead cell with 3 neighbours becomes alive, otherwise stays dead
        int ruleAlive[aliveLength], ruleDead[deadLength];
        int alive = 0, dead = 0; afterSlash = 0;
        for (int m=0; m<aliveLength+deadLength+1; m++)
        {   
            if (ruleString[m] != '/')
            {
                if (afterSlash)
                {
                    ruleDead[dead] = charToInt(ruleString[m]);
                    dead++;
                } else
                {
                    ruleAlive[alive] = charToInt(ruleString[m]);
                    alive++;
                }
            } else
            {
                afterSlash++;
            }
        }
        // e.g.: ruleAlive = [2 3], ruleDead = [3]; aliveLength = 2, deadLength = 1 (length of the rules)
        
        // conpute newField
        int livingCells;
        for (int row=0; row<n; row++)
        {
            for (int column=0; column<n; column++)
            {
                livingCells = livingCellsInNeighbourhood(row,column,n,oldField,topology);
                //printf("living cells in [%d,%d]: %d\n",row,column,livingCells);
                if (deadOrAlive(livingCells, ruleDead, deadLength, ruleAlive, aliveLength, oldField[row][column]))
                {
                    newField[row][column] = '1';
                } else
                {
                    newField[row][column] = '0';
                }            
            }
        }    
    } // } closes the else-part
    return;
}

int deadOrAlive(int livingCells,int *ruleDead, int deadLength, int *ruleAlive, int aliveLength, char status)
{   // return 0 for dead, 1 for alive
    // e.g.: ruleAlive = [2 3], ruleDead = [3]; aliveLength = 2, deadLength = 1 (length of the rules)
    // living cell with 2 or 3 neighbours stays alive, otherwise dies
    // dead cell with 3 neighbours becomes alive, otherwise stays dead
    //printf("living cells: %d\nruleAlive = [%d,%d]\nruleDead = [%d]\ncell is alive: %c\n",livingCells,ruleAlive[0],ruleAlive[1],ruleDead[0],status);
    
    int alive;
    if (status == '1')
    {   //alive
        alive = 0;
        for (int k=0; k<aliveLength; k++)
        {
            if (livingCells == ruleAlive[k])
            {
                alive = 1;
            }
        }
    } else if (status == '0')
    {   //dead
        alive = 0;
        for (int k=0; k<deadLength; k++)
        {
            if (livingCells == ruleDead[k])
            {
                alive = 1;
            }
        }
    }
    //printf("outcome: %d\n\n",alive);
    return alive;
}

int livingCellsInNeighbourhood(int row, int column, int n, char field[][n], char topology)
{
    int numberOfLivingCells = 0;
    for (int k=-1; k<2; k++)
    {
        for (int l=-1; l<2; l++)//
        {
            if (k == 0 && l == 0)
                continue;
            
            if (k+row > -1 && k+row < n && l+column > -1 && l+column < n)
            {   // no outburst; every topology
                if (field[k+row][l+column] == '1')
                {
                    numberOfLivingCells++;
                }
            } else if ((k+row == -1 || k+row == n) && l+column > -1 && l+column < n && topology != 'n')
            {   // top/down outburst
                if ((field[(k+row+n)%n][(l+column)] == '1' && topology == 't') || (field[(k+row+n)%n][(n-1-(l+column))] == '1' && topology == 'k') || (field[(k+row+n)%n][(n-1-(l+column))] == '1' && topology == 'p'))
                {
                    numberOfLivingCells++;
                }
            } else if (k+row > -1 && k+row < n && (l+column == -1 || l+column == n) && topology != 'n')
            {   // left/right outburst
                if ((field[(k+row)][(l+column+n)%n] == '1' && topology == 't') || (field[(k+row)][(l+column+n)%n] == '1' && topology == 'k') || (field[(n-1-(k+row))][(l+column+n)%n] == '1' && topology == 'p'))
                {
                    numberOfLivingCells++;
                }
            } else if (topology != 'n')
            {   // corner outburst
                if (field[(k+row+n)%n][(l+column+n)%n] == '1')
                {
                    numberOfLivingCells++;
                }
            }    
        }
    }
    return numberOfLivingCells;
}

int charToInt(char c)
{
    int i=0;
    switch(c)
    {
        case '0': i=0; break;
        case '1': i=1; break;
        case '2': i=2; break;
        case '3': i=3; break;
        case '4': i=4; break;
        case '5': i=5; break;
        case '6': i=6; break;
        case '7': i=7; break;
        case '8': i=8; break;
        case '9': i=9; break;
        default: break;
    }
    return i;
}

int printField(int length, char field[][length], int booleanPrint)
{   // boleanPrint == 0: print, else: don't print
    for (int k=0; k<length; k++)
    {
        for (int l=0; l<length; l++)
        {
            if (field[k][l] == '0' || field[k][l] == '1')
            {
                if (booleanPrint == 0) {printf("%c",field[k][l]);}
            } else
            {
                return 1;
            }
        }
        if (booleanPrint == 0) {printf("\n");}
    }
    //if (booleanPrint == 0) {printf("\n");}
    return 0;
}

int transferStringToArray(char *string, int length, char field[][length])
{
    int column = 0;
    int row = 0;
    
    while (*string != '\0')
    {
        if ((*string == '\\' && *(string+1) == 'n') || *string == ' ' || *string == '\n')
        //jump zu next row
        {
            row++;
            column = 0;
            
        } else if (*(string-1) != '\\' || *string != 'n')//(strcmp(string[k],"\\") != 0 || strcmp(string[k+1],"n") != 0)
        {
            field[row][column] = *string;
            //printf("%c in [row,column]: [%d,%d]\n",field[row][column],row,column);
            column++;
        }
        string++;
    }

    return 0;
}

int checkLengthOfField(char *string)
{
    int length=0;
    while ((*string != '\0') && ((*string != '\\') && *(string+1) != 'n') && (*string != ' ') && (*string != '\n'))
    {
        length++;
        string++;
    }
    return length;
}
