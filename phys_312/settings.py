# Map paramters
WINDOW_WIDTH  = 1300
WINDOW_HEIGHT = 700
BOX_WIDTH     = WINDOW_WIDTH # relative to screen (X)
BOX_HEIGHT    = WINDOW_HEIGHT # relative to screen (Y)
BOX_LENGTH    = 281.9 # in/out of screen (Z)
FPS           = 120  # frames per second
SCALE_SPEED   = 1000 # 1 meter is SCALE_SPEED pixels
RADIUS        = 9
TRIALS        = 1000
# STP is 281.8 pixels each (22.4 L)
# 1 m in length = 1000 pixels
# e.g. 281.8 pixels = 0.2818 m

# Physics numbers
k          = 1.380649e-23 # boltzmann constant
V          = BOX_WIDTH*BOX_HEIGHT*BOX_LENGTH/(SCALE_SPEED**3)
Na         = 6.022e23      # Avogadro's number
N          = 6.022e23      # number of particles
N_display  = 60        # one particle that will be displayed on screen
m_helium   = 6.646e-27     # mass of a helium atom
m_nitrogen = 2.3258671e-26 # mass of a nitrogren atom
m_ideal    = 1
P          = 101325        # initial pressure (N/m^2)
