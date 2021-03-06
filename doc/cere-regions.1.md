cere regions(1) -- List extractible regions
==================================================================

## SYNOPSIS

```
cere regions [-h] [--static] [--dynamic]
```

## DESCRIPTION

**cere regions** list extractible regions. To achieve this all regions are
outlined at compilation time and listed in the file **regions.csv**. this file
contains for each region, informations such as the file and the function from
where the region is outlined, the start line and coverage measures.

By default if no mode is chosen, both modes are enabled.

## OPTIONS

  * `-h`:
    Prints a synopsis and a list of the most commonly used options.

  * `--static`:
    With the **static** flag, all regions are outlined and listed but the binary
    is not executed. So keep in mind that a region may not be extractible as it
    is not necessarily executed. Also coverage informations are not available.

  * `--dynamic`:
    All regions are outlined and the binary is executed. Only executed regions
    are listed with their coverage measures.

## OUTPUT FILES

  * `regions.csv`:
    File containing for each region, the region name, region location, and
    coverage informations.

## COPYRIGHT

cere is Copyright (C) 2014-2015 Université de Versailles St-Quentin-en-Yvelines

## SEE ALSO

cere-capture(1) cere-replay(1) cere-configure(1)
