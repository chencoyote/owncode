#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main( int argc, char *argv[] )
{
    fprintf(stdout, "Memory leak Demo\r\n");

    if ( argc != 4 && argc != 1 )
    {
        fprintf(stdout, "Example: ./mem_leak 泄漏次数 每次多少K 时间间隔(秒)\r\n");
        return 0;
    }

    int count = 0 ;
    int mem_offset = 0;
    int inter = 0;

    if ( argc == 1 )
    { // 默认每次吃 1M，一共 100次
        count = 100;
        mem_offset = 1024;
        inter = 1;
    }
    else 
    {
        int n1 = atoi(argv[1]);
        int n2 = atoi(argv[2]);
        int n3 = atoi(argv[3]);

        count = n1>0 ? n1: 100;
        mem_offset = n2>0 ? n2: 1024;
        inter = n3>0 ? n3: 1;
    }

    int i = 0;
    while ( i++ < count )
    {
        fprintf( stdout, "malloc %d , size:%dk, total:%dk\r\n", i, mem_offset, i*mem_offset );
        char *pdata = (char *)malloc( mem_offset * 1024 );
        if ( pdata == NULL )
        {
            fprintf(stdout, "Progame exit, malloc fail");
            break;
        }
        sleep(inter);
    }

    return 0;
}
