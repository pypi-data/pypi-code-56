from typing import List
import time
import os
import csv

class Timer:
    def __init__(self):
        """
        For creating a timer object. Example initialization timer = Timer().
        """
        # start and end time
        self.t:List[float, float] = [0., 0.]
        
        # storing time
        self.t_store = []        
    
    def __store(self):
        """
        Store the result of tic and toc into the t_store list.
        """
        self.t_store.append([self.t[0], self.t[1], self.t[1] - self.t[0]])
        self.t:List[float, float] = [0., 0.]    
        
    def tic(self):
        """
        Begin the timer.
        """
        self.t[0] = time.time()
    
    def toc(self) -> float:
        """
        End the timer and store the time.

        Returns:
            float: the run time (time elapsed).
        """
        time_end = time.time()
        self.t[1] = time_end
        self.__store()

        return self.t_store[-1][1] - self.t_store[-1][0]

    def dump(self, filename:str, mode:str = 'a'):        
        """
        Store all recorded run times in a file.

        Args:
            filename (str): saving file name.
            mode (str, optional): File write mode. Either 'a' for append or
                'w' for write. Defaults to 'a'.
        """
        
        # make sure we got the correct output mode            
        assert(mode == 'a' or mode == 'w')
        
        # output to the saving file
        save_output:str = ''             
             
        for time_list in self.t_store:
            runtime = time_list[1] - time_list[0]
            save_output += f'{time_list[0]},{time_list[1]},{runtime}\n'
        
        # write the output
        f = open(filename, f'{mode}+')
        f.write(save_output)
        f.close()
    
    def load(self, filename:str) -> List:
        """
        Read all recorded run times into t_store list. Note that when this is
        done, the t_store list is reset. Make sure to dump() before load()!        

        Args:
            filename (str): file to read.

        Returns:
            List: the loaded t_store list.
        """

        data = csv.reader(open(filename), delimiter=',')
        self.t_store = list(data)[1:]
        return self.t_store
    
    def plot(self, plot_start_time:bool = True,
             plot_avg:bool = False):
        """
        For plotting the runtimes. Needs matplotlib.

        [extended_summary]

        Args:
            plot_start_time (bool, optional): Second x-axis for labeling the 
                local start time. Defaults to True.
            plot_avg (bool, optional): Plot the average time as a dashed line. 
                Defaults to False.

        Returns:
            fig, ax: Figure and axes objects from matplotlib.
        """
        
        # import matplotlib for plotting
        import matplotlib.pyplot as plt
        
        # unzip the data structure
        start_t, _, runtime = zip(*self.t_store)
        
        # cast to make sure the runtimes are float
        runtime = list(map(float, runtime))
        # how many times we ran this
        run_number = list(range(len(runtime)))
        
        # set up for plotting
        fig = plt.figure(figsize=(8,6))
        ax = fig.add_subplot(111)
        
        # plotting
        ax.plot(run_number, runtime, 'k.-', label='Run time')
        ax.set_ylabel('Run time (s)')
        ax.set_xlabel('Run number')
        
        if plot_start_time:
            # prepare the start time
            # convert from time.time() seconds --> date time format
            start_local = []
            for i, t in enumerate(start_t):
                t = float(t)
                # convert time to local time structure
                local_t = time.localtime(t)
                # format the time showing DD/MM HH:MM:SS
                formatted_t = time.strftime("%d/%m %H:%M:%S", local_t)
                # if this is the first label, we are okay
                # else this is too much information (don't need DD/MM)
                if i > 0:
                    # check the previous time
                    prev_t = time.localtime(float(start_t[i-1]))
                    # if the current time and previous time share DD/MM
                    if (prev_t.tm_mon == local_t.tm_mon and 
                        prev_t.tm_mday == local_t.tm_mday):
                        # then don't show DD/MM
                        formatted_t = time.strftime("%H:%M:%S", local_t)
                start_local.append(formatted_t)        
            
            # plotting
            ax2 = ax.twiny()
            l2, = ax2.plot(start_local, runtime, 'k.-', label='Run time')
            ax2.set_xlabel('Start time (DD/MM HH:MM:SS)')
            ax2.set_xticklabels(start_local, rotation=90)
            l2.remove()
            
        if plot_avg:
            from statistics import mean
            ax.axhline(mean(runtime),color='k',linestyle='--', label='Average')
            ax.legend()
        
        # turn on grid
        ax.grid()
        # make sure everything fits
        fig.tight_layout()
        
        return fig, ax
    
    def summarize(self) -> str:
        output:str = ''
        output += '\nDatetime format: DD/MM HH:MM:SS\n'
        # formatting to a table form
        fmt = '{: >15}  {: >15} {: >15}\n'
        output += fmt.format('Start', 'End','Time (s)')
        # unzip the data structure
        start_t, end_t, runtime = zip(*self.t_store)
        
        for i, t in enumerate(start_t):
            # convert time to local time for start_t
            t = float(t)
            local_t = time.localtime(t)
            t1 = time.strftime("%d/%m %H:%M:%S", local_t)
            # convert time to local time for end_t
            t = float(end_t[i])
            local_t = time.localtime(t)
            t2 = time.strftime("%d/%m %H:%M:%S", local_t)
            # output
            output +=  fmt.format(t1, t2, 
                                  round(float(runtime[i]),6))

        return output
    def __repr__(self):
        return self.summarize()
