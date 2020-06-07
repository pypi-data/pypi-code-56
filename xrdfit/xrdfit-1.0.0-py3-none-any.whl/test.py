from xrdfit.spectrum_fitting import PeakParams, FitExperiment, load_dump
import time

frame_time = 0.1
file_string = '../example_data/example_data_large/adc_065_TI64_NDload_900C_15mms_{:05d}.dat'
first_cake_angle = 90
cakes_to_fit = 1
merge_cakes = False

peak_params = [PeakParams((3.02, 3.27), '(10-10)'),
               PeakParams((3.30, 3.75), ['(0002)', '(110)', '(10-11)'], [(3.4, 3.44), (3.52, 3.56), (3.57, 3.61)]),
               PeakParams((4.54, 4.80), '(10-12)'),
               PeakParams((4.90, 5.10), '(200)'),
               PeakParams((5.35, 5.60), '(11-20)'),
               PeakParams((5.90, 6.15), '(10-13)', [(6.00, 6.05)]),
               PeakParams((6.21, 6.40), '(20-20)'),
               PeakParams((6.37, 6.71), ['(11-22)', '(20-21)'], [(6.43, 6.47), (6.52, 6.56)]),
               PeakParams((6.75, 6.95), '(0004)', [(6.82, 6.87)]),
               PeakParams((6.95, 7.35), ['(220)', '(20-22)'], [(7.05, 7.12), (7.16, 7.20)]),
               PeakParams((7.75, 8.05), '(310)')
              ]


max_frame = 5657
frames_to_fit = range(1, max_frame, 100)

# Multi frame
experiment = FitExperiment(frame_time, file_string,first_cake_angle, cakes_to_fit, peak_params, merge_cakes, frames_to_fit)

experiment.run_analysis(reuse_fits=True)

start = time.time()
experiment.save("a")
mid = time.time()
print(f"{mid - start:4f}s to save")
new_experiment = load_dump("a")
end = time.time()
print(f"{end - mid:4f}s to load")