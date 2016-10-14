#include <stdio.h>
#include <stdlib.h>

int main()
{
    int gb;
    char *command;

    printf("Enter the number of gigabytes to upload to Google Drive: ");
    scanf("%d", &gb);
	
	command = (char *) malloc (50 * sizeof(char)); 
    sprintf(command, "fallocate -l %dG fallocate%d.txt", gb, gb);
	system(command);
	free(command); 
	
	command = (char *) malloc (50 * sizeof(char)); 
	sprintf(command, "gdrive upload fallocate%d.txt", gb);
	system(command);
	free(command);

    return 0;
}
