#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

void cere_markerInit(char* tool) {{
    {cere_init}
}}

void cere_markerClose(char* tool) {{
    {cere_close}
}}

void cere_markerStartRegion(char* tool, char* regName, bool trace, bool global) {{
    {cere_start}
}}

void cere_markerStopRegion(char* tool, char* regName, bool trace, bool global) {{
    {cere_stop}
}}
