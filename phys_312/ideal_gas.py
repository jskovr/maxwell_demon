from settings import *
from classes import Particle
from formulas import maxwell_boltzmann
from scipy.optimize import curve_fit
from scipy.spatial import distance
import pygame
# import tensorflow as tf
import numpy as np
# import tensorflow.experimental.numpy as np
# print(tensorflow.experimenta.numpy)
import matplotlib.pyplot as plt
import random

class Map:
    def __init__(self, 
                 particles, 
                 debug=False, 
                 maxwell_demon=False, 
                 non_ideal=False, 
                 display_speeds=False, 
                 sim_num=None, 
                 save_fig=False,
                 animation=False,
                 max_frames=10,
                 boundary=BOX_WIDTH/2):
        # Toggle demon and other flags
        self.maxwell_demon = maxwell_demon
        self.non_ideal     = non_ideal
        self.display_speeds = display_speeds
        self.save_fig = save_fig
        self.animation = animation
        self.boundary = boundary

        if self.animation:
            pygame.init()
            self.font      = pygame.font.Font(pygame.font.get_default_font(), 20) # font for text
            self.font2     = pygame.font.Font(pygame.font.get_default_font(), 15) # font for text
            self.screen    = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
            self.clock     = pygame.time.Clock()
            print(pygame.version.ver)
        self.sim_num   = sim_num
        self.max_frames = max_frames
        self.playing   = True
        self.debug     = debug


        # Particles and physics
        self.particles = particles
        self.vrms      = 0
        self.N         = N_display
        self.P         = P
        self.V         = V
        self.T         = self.P*self.V/self.N/k
        self.f         = 0
        self.speeds    = []

        # Print statements
        if self.debug:
            print("Number of particles: {} ({} mol)".format(N, N/Na))
            print("Volume of the box: {} m^3 ({} L)".format(self.V, self.V*1000))
            print("Initial pressure of the box: {} N/m^2 ({} atm)".format(self.P, self.P/101325))
            print("Initial temperature of the box: {} K ({} C)".format(self.T, self.T-273.15))

        # Map
        self.plane1  = pygame.transform.scale(pygame.image.load("border.png"), (BOX_WIDTH, BOX_HEIGHT))
        self.buttons = pygame.sprite.Group()

    def run(self):
        # print("sim no. {} started. total_frames={}".format(self.sim_num, self.f))
        while self.playing:
            self.f += 1

            if not self.animation:
                for particle1 in self.particles:
                    particle1.update(self.boundary, maxwell_demon=self.maxwell_demon)
                    if self.non_ideal:
                        self.handle_collisions(particle1)

                if self.f == self.max_frames:
                    self.playing = False
                    # self.maxwell_boltzmann_distribution()
                    L_tot, R_tot = self.document_result()
                    self.result = [len(L_tot), len(R_tot)]
                    self.speeds = np.array([particle.speed for particle in self.particles])

            else:
                # Tick the pygame clock (FPS / second), update the sprites
                self.clock.tick(FPS)
                self.screen.fill("black")
                for particle1 in self.particles:
                    particle1.update(maxwell_demon=self.maxwell_demon)
                    if self.non_ideal:
                        self.handle_collisions(particle1)
                    self.draw(particle1)
                L_tot, R_tot = self.document_result()

                if self.f/FPS == 10:
                    self.playing = False
                    # self.maxwell_boltzmann_distribution()

                    self.result = [len(L_tot), len(R_tot)]

                # Check the pygame events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.playing = False
                        self.maxwell_boltzmann_distribution()
                    # if event.type == pygame.MOUSEBUTTONDOWN:

                # Animate the simulation
                self.screen.blit(
                    self.font.render(f"N visible: {len(self.particles)}", True, (255, 255, 255)), dest=(WINDOW_WIDTH-300, 30))
                if self.display_speeds:
                    for particle in self.particles:
                        self.screen.blit(
                            self.font2.render("{:.3f}".format(particle.speed), True, (255, 255, 255)), dest=(particle.position[0]-particle.radius, particle.position[1]-2*particle.radius))
                self.screen.blit(
                    self.font.render("rms speed: {:.3f} m/s".format(self.vrms), True, (255, 255, 255)), dest=(WINDOW_WIDTH-300, 100))
                self.screen.blit(
                    self.font.render("N_left: {}".format(len(L_tot)), True, (255, 255, 255)), dest=(WINDOW_WIDTH-300, 140))
                self.screen.blit(
                    self.font.render("N_right: {}".format(len(R_tot)), True, (255, 255, 255)), dest=(WINDOW_WIDTH-300, 180))

                if self.maxwell_demon:
                    self.screen.blit(
                        self.font.render("Condition: v < {}".format(self.maxwell_demon), True, (255, 255, 255)), dest=(WINDOW_WIDTH-300, 160))
                    self.screen.blit(
                        self.font.render("Condition: v >= {}".format(self.maxwell_demon), True, (255, 255, 255)), dest=(WINDOW_WIDTH-300, 200))
                
                if self.debug:
                    particle = self.particles[-1]
                    # print(particle.position[0])
                    self.screen.blit(
                        self.font.render("v_left: {} v_right: {}".format(particle.sorted_v_left, particle.sorted_v_right), 
                            True, (255, 255, 255)), dest=(WINDOW_WIDTH-300, 220))
                    self.screen.blit(
                        self.font.render("pos_left: {} pos_right: {}".format(particle.sorted_left, particle.sorted_right), 
                            True, (255, 255, 255)), dest=(WINDOW_WIDTH-300, 240))


                # HUD Metrics
                self.screen.blit(
                    self.font.render('{:e} K'.format(self.T), True, (255, 255, 255)), dest=(WINDOW_WIDTH-300, 410))
                self.screen.blit(
                    self.font.render('{:.3f} atm'.format(self.P/101325), True, (255, 255, 255)), dest=(WINDOW_WIDTH-300, 430))
                self.screen.blit(
                    self.font.render('{} s'.format(int(self.f/FPS)), True, (255, 255, 255)), dest=(WINDOW_WIDTH-300, 450))
                self.screen.blit(
                    self.font.render('Sim No. {}'.format(self.sim_num), True, (255, 255, 255)), dest=(WINDOW_WIDTH-300, 470))              
                
                # Update the display
                self.calculate_v_rms()
                pygame.display.update()

    def document_result(self):
        L_tot = []
        R_tot = []
        for particle in self.particles:
            if particle.position[0] <= self.boundary:
                L_tot.append(particle)
            elif particle.position[0] > self.boundary:
                R_tot.append(particle)
        return L_tot, R_tot

    def draw(self, particle1):
        # draw the particles on the screen
        pygame.draw.circle(self.screen, particle1.color, (particle1.position[0], particle1.position[1]), particle1.radius)
        pygame.draw.line(self.screen, "white", 
            (particle1.position[0], particle1.position[1]), 
            (particle1.position[0]+particle1.velocity[0]*5, particle1.position[1]+particle1.velocity[1]*5), 
            2)

    def handle_collisions(self, particle1):
        for particle2 in self.particles:
            if particle1 != particle2:
                # particle2.update(self)
                d = distance.euclidean(particle1.position, particle2.position)
                if d <= (particle1.radius+particle2.radius):
                    m1 = particle1.mass
                    m2 = particle2.mass
                    v1 = particle1.velocity 
                    v2 = particle2.velocity
                    x1 = particle1.position
                    x2 = particle2.position 
                    particle1.velocity = v1 - ((2*m2/(m1+m2)))*((np.dot(v1-v2, x1-x2))/(np.linalg.norm(x1-x2)**2))*(x1-x2)
                    particle2.velocity = v2 - ((2*m1)/(m1+m2))*((np.dot(v2-v1, x2-x1))/(np.linalg.norm(x2-x1)**2))*(x2-x1)

    def calculate_v_rms(self):
        self.vrms = np.sqrt(np.sum(np.array([particle.speed for particle in self.particles])**2)/N_display)

    def maxwell_boltzmann_distribution(self):
        speeds = np.array([particle.speed for particle in self.particles])
        plt.figure()
        plt.hist(speeds, bins=35)
        if self.save_fig:
            plt.savefig("simulation_{}.png".format(self.sim_number))
        plt.show()