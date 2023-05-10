// #include <iostream>
#include <stdio.h>
#include <string.h>

// using namespace std;

#define	MAX_STRING_SIZE         500
#define M                       3

struct Parameters {
    
    /* ����� ��� ���������� ������� ������� */

    int cells_number;           /* ����� ����� */
       
    /* ����� ������ */
    
    double stop_time;           /* ������ �������, ��� �������� �������� ������ ������� */

    /* ��������� ������� */

   double left_params[M];   /* ������ ����������� ���������� ����� �� ������� */
   double right_params[M];  /* ������ ����������� ���������� ������ �� ������� */
    
    /* ��������� ��������� */
    
    double g;                   /* ���������� ������� */

};

int main()
{
    struct Parameters *params;
    FILE *parameters;
    char string[MAX_STRING_SIZE];   /* ��� ���������� ��������� ���������� �� ����� */
        
    /* ��� ��������� ������ ��������� � ����� parameters.txt */
    strcpy( string, "C://My_Progs//nvp//Accurate_solution//Accurate_solution//test.dat" );

    printf("%d", 1);
    fscanf( parameters, "%s %d", string, MAX_STRING_SIZE, &(params->cells_number) );

    printf("%d", params->cells_number);

    return 0;
}