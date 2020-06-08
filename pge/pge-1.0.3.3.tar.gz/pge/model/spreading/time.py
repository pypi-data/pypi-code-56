import numpy as np


class Spreading:
    @staticmethod
    def get_modeling_spreading_time_full_min(timer, model, num_iter):
        times = model.iteration_bunch(num_iter)
        df_times = [timer.get_times(int(mx)) for mx in np.max(times, axis=1)]

        for i in np.arange(times.shape[0]):
            for j in np.arange(times.shape[1]):
                times[i, j] = np.sum(df_times[i][: int(times[i, j])])
        return {
            model.ids[i]: np.min(times[:, i]) for i in np.arange(model.graph.size())
        }

    @staticmethod
    def get_modeling_spreading_time_complex(timer, model, num_iter, comm, prnt=False):
        times = []
        comm_times = []

        for _ in np.arange(num_iter):
            k, n = model.iteration_bunch_complex(comm)
            df_times = timer.get_times(n)
            times.append(np.sum(df_times))
            comm_times.append(np.sum(df_times[:k]))
            if prnt:
                print("iteration", _)
        return comm_times, times

    @staticmethod
    def get_modeling_spreading_time_min(timer, model, num_iter, prnt=False):
        times = []

        mx = None
        for _ in np.arange(num_iter):
            n = model.iteration_bunch_speed(mx)
            if mx is None:
                mx = n
            elif mx > n:
                mx = n
            times.append(np.sum(timer.get_times(n)))

            if prnt:
                print("iteration", _)
        return np.min(times)
