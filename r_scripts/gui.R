pacman::p_load(
    ggplot2,
    tidyverse,
    fgui,
    svDialogs
)

# function to run ls
set_ID_CAM_TAG <- function(
        ID1 = NA,
        ID2 = NA,
        ID3 = NA,
        ID4 = NA,
        ID5 = NA,
        ID6 = NA,
        ID7 = NA,
        ID8 = NA,
        CAM1 = NA,
        CAM2 = NA,
        CAM3 = NA,
        CAM4 = NA,
        CAM5 = NA,
        CAM6 = NA,
        CAM7 = NA,
        CAM8 = NA
        ){
    experimental_settings = tibble(
        ID1 = ID1,
        ID2 = ID2,
        ID3 = ID3,
        ID4 = ID4,
        ID5 = ID5,
        ID6 = ID6,
        ID7 = ID7,
        ID8 = ID8,
        CAM1 = CAM1,
        CAM2 = CAM2,
        CAM3 = CAM3,
        CAM4 = CAM4,
        CAM5 = CAM5,
        CAM6 = CAM6,
        CAM7 = CAM7,
        CAM8 = CAM8
    )
    return(experimental_settings)
}

y <- gui(
    set_ID_CAM_TAG,
    title = "NBO LAB CAM GUI",
    argText = list(
        ID1 = c("ANIMAL 1 ID"),
        ID2 = c("ANIMAL 2 ID"),
        ID3 = c("ANIMAL 3 ID"),
        ID4 = c("ANIMAL 4 ID"),
        ID5 = c("ANIMAL 5 ID"),
        ID6 = c("ANIMAL 6 ID"),
        ID7 = c("ANIMAL 7 ID"),
        ID8 = c("ANIMAL 8 ID")
        ),
    argSlider = list(
        CAM1 = c(1, 8, 1),
        CAM2 = c(1, 8, 1),
        CAM3 = c(1, 8, 1),
        CAM4 = c(1, 8, 1),
        CAM5 = c(1, 8, 1),
        CAM6 = c(1, 8, 1),
        CAM7 = c(1, 8, 1),
        CAM8 = c(1, 8, 1)
        ),
    guiSet("ENTRY_WIDTH", 10),
    guiSet("SLIDER_LENGTH", 200),
    cancelButton = TRUE,
    verbose = TRUE,
    exec = "Set experiment"
    )
