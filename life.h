/*
 * head
 */

int transferStringToArray(char *string, int n, char field[][n]);
int checkLengthOfField(char *string);
int printField(int n, char field[][n], int booleanPrint);
void gameOfLife(char *ruleString, int n, char oldField[][n], char newField[][n],char topology);
int charToInt(char c);
int livingCellsInNeighbourhood(int row, int column, int n, char field[][n],char topology);
int deadOrAlive(int livingCells,int *ruleDead, int deadLength, int *ruleAlive, int aliveLength, char status);
