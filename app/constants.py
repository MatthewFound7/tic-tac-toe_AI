# Grid coordinates
in0 = "0.14, 0.19"
in1 = "0.375, 0.19"
in2 = "0.61, 0.19"
in3 = "0.14, 0.5"
in4 = "0.375, 0.5"
in5 = "0.61, 0.5"
in6 = "0.14, 0.81"
in7 = "0.375, 0.81"
in8 = "0.61, 0.81"



# Player Position Tracking
tracking = {
    in0: "", in1: "", in2: "",
    in3: "", in4: "", in5: "",
    in6: "", in7: "", in8: "",
}

# Player Scoring Tracking
scoring = {
    in0: "", in1: "", in2: "",
    in3: "", in4: "", in5: "",
    in6: "", in7: "", in8: "",
}

# Opponent Scoring Tracking
scoring_2 = {
    in0: "", in1: "", in2: "",
    in3: "", in4: "", in5: "",
    in6: "", in7: "", in8: "",
}

# Comp Position tracking
comp_ads = {
    in0: "", in1: "", in2: "",
    in3: "", in4: "", in5: "",
    in6: "", in7: "", in8: "",
}

### POSITIONING FOR BUTTONS ###
grid_x = [0.14, 0.375, 0.61]
grid_y = [0.19, 0.5, 0.81]

### GAME WIN CONDITIONS ###
win_conditions = [
    {
    in0: "hit", in1: "miss", in2: "miss",
    in3: "miss", in4: "hit", in5: "miss",
    in6: "miss", in7: "miss", in8: "hit",    
    },
    {
    in0: "miss", in1: "miss", in2: "hit",
    in3: "miss", in4: "hit", in5: "miss",
    in6: "hit", in7: "miss", in8: "miss",    
    },
    {
    in0: "hit", in1: "hit", in2: "hit",
    in3: "miss", in4: "miss", in5: "miss",
    in6: "miss", in7: "miss", in8: "miss",    
    },
    {
    in0: "miss", in1: "miss", in2: "miss",
    in3: "hit", in4: "hit", in5: "hit",
    in6: "miss", in7: "miss", in8: "miss",    
    },
    {
    in0: "miss", in1: "miss", in2: "miss",
    in3: "miss", in4: "miss", in5: "miss",
    in6: "hit", in7: "hit", in8: "hit",    
    },
    {
    in0: "hit", in1: "miss", in2: "miss",
    in3: "hit", in4: "miss", in5: "miss",
    in6: "hit", in7: "miss", in8: "miss",    
    },
    {
    in0: "miss", in1: "hit", in2: "miss", 
    in3: "miss", in4: "hit", in5: "miss",
    in6: "miss", in7: "hit", in8: "miss",    
    },
    {
    in0: "miss", in1: "miss", in2: "hit",
    in3: "miss", in4: "miss", in5: "hit",
    in6: "miss", in7: "miss", in8: "hit",    
    }
]

### UI COLOUR SELECTION ###
BG_COL = "#DBDBDB"
GREY = "#E6E6E6"
LIGHT_BLUE = "#C5F3FF"
LIGHT_BLUE_HOVER = "#9BEBFF"
MULTI_COL = "#7BB4FF"
MULTI_COL_HOV = "#4495FF"
EASY_COL = "#ACFFAC"
EASY_COL_HOV = "#88FF88"
HARD_COL = "#FFA0A0"
HARD_COL_HOV = "#FF6969"
IMP_COL = "#D894FF"
IMP_COL_HOV = "#C562FF"
SELECT_COL = "#FFED48"