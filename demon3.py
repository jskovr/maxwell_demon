# import matplotlib.pyplot as plt
# from scipy.optimize import curve_fit
import numpy as np
import pickle
# import tensorflow as tf
# from tensorflow import keras
from ideal_gas import *
# import pickle
from multiprocessing import cpu_count, Process
import time
# print("Num GPUs Available: {}".format(len(tf.config.experimental.list_physical_devices("GPU"))))
# print(tf.test.is_built_with_cuda())
# print(tf.version.VERSION)



def running(demon_speed_boundaries, physical_boundaries, trials, N_particles, file):
    n = 0
    sims = []
    for x in demon_speed_boundaries:
        for y in physical_boundaries:
            for num in range(trials):
                particles = []
                for _ in range(N_particles-1):
                    particles.append(Particle(RADIUS, (random.uniform(RADIUS, BOX_WIDTH-RADIUS), random.uniform(RADIUS, BOX_HEIGHT-RADIUS)), random.uniform(0, 2*np.pi), 0, m_helium, (0, 0, 255)))
                particles.append(Particle(RADIUS, (random.uniform(RADIUS, BOX_WIDTH-RADIUS), random.uniform(RADIUS, BOX_HEIGHT-RADIUS)), random.uniform(0, 2*np.pi), 20, m_helium, (255, 255, 0)))
                b = Map(particles, 
                        debug=False, 
                        maxwell_demon=x, 
                        non_ideal=True, 
                        display_speeds=False, 
                        sim_num=num, 
                        save_fig=False, 
                        animation=False,
                        max_frames=4500,
                        boundary=y)
                b.run()
                sims.append([b.result, b.speeds])
                n += 1
    with open("demon_data_piece{}.p".format(file), "wb") as f:
        pickle.dump(sims, f)



divisions = 1
divisor = 1
if divisor < 1:
    print("Make divisor > 1")
    raise
WIDTH = BOX_WIDTH
demon_speed_boundaries = [3, 6, 9, 12, 15, 17, 19, 21, 23, 25, 27, 29]
physical_boundaries = [WIDTH*(n/divisor) for n in range(1, divisions+1)]
for boundary in physical_boundaries:
    if boundary >= 2600:
        raise
trials = 250
total_number_of_simulations = len(demon_speed_boundaries)*len(physical_boundaries)*trials
N_particles = 60

def main():
    print(demon_speed_boundaries, physical_boundaries)
    print("Simulations: {}".format(total_number_of_simulations))

    a = Process(target=running, args=(demon_speed_boundaries[0:2], physical_boundaries, trials, N_particles, 0))
    b = Process(target=running, args=(demon_speed_boundaries[2:4], physical_boundaries, trials, N_particles, 1))
    c = Process(target=running, args=(demon_speed_boundaries[4:6], physical_boundaries, trials, N_particles, 2))
    d = Process(target=running, args=(demon_speed_boundaries[6:8], physical_boundaries, trials, N_particles, 3))
    e = Process(target=running, args=(demon_speed_boundaries[8:10], physical_boundaries, trials, N_particles, 4))
    f = Process(target=running, args=(demon_speed_boundaries[10:12], physical_boundaries, trials, N_particles, 5))

    a.start()
    b.start()
    c.start()
    d.start()
    e.start()
    f.start()

    a.join()
    b.join()
    c.join()
    d.join()
    e.join()
    f.join()

    # print("finished in: {} s".format(time.perf_counter()))
    end = time.time()

    print(end-start, "s")
    

if __name__ == "__main__":
    start = time.time()
    main()