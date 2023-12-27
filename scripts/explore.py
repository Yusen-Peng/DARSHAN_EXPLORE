"""

a template to integrate Darshan profiling with Python.

"""
import os
import shutil
import numpy as np
from netCDF4 import Dataset
import darshan


filename = 'dummy'
num_datasets = 128 
dimensions = [128]

def generate_array(num_elements):
                                # num_elements: keep track of #elements in each dimension
                                # [a] or [a, b] or [a, b, c]  
    np.random.seed(None)

    if len(num_elements) == 1:
        a = num_elements[0]
        arr = np.random.rand(a).astype(np.float32)
    elif len(num_elements) == 2:
        a, b = tuple(num_elements)
        arr = np.random.rand(a, b).astype(np.float32)
                                # "a*b" random numbers [0,1) 
    else:
        a, b, c = tuple(num_elements)
        arr = np.random.rand(a, b, c).astype(np.float32)
                                # "a*b*c" random numbers [0,1)
    return arr

def copy_file(filename):
    shutil.copy(f'data/files/{filename}.netc', 'data/files_read')
    os.rename(f'data/files_read/{filename}.netc', f'data/files_read/{filename}_copy.netc')
    os.remove(f'data/files/{filename}.netc')
                                                        # copy -> rename -> remove

#HDF5, netCDF4 I/O operation goes here
def perform_io_operations():
    
    #create the file
    file = Dataset(f'data/files/{filename}.netc', 'w', format='NETCDF4')
    if len(dimensions) == 1:
        file.createDimension('x', None)
        axes = ('x',)
    elif len(dimensions) == 2:
        file.createDimension('x', None)
        file.createDimension('y', None)
        axes = ('x', 'y',)
    else:
        file.createDimension('x', None)
        file.createDimension('y', None)
        file.createDimension('z', None) 
        axes = ('x', 'y', 'z') 

    # Create datasets and populate them with data
    for i in range(0, num_datasets):
        
        # generate the random array
        data = generate_array(tuple(dimensions))

        #create datasets                   
        dataset = file.createVariable(f'Dataset_{i}', dimensions=axes, datatype='f')  

        #populate datasets
        if len(dimensions) == 1:
            dataset[:dimensions[0]] = data
        elif len(dimensions) == 2:
            dataset[:dimensions[0], :dimensions[1]] = data
        else:
            dataset[:dimensions[0], :dimensions[1], :dimensions[2]] = data

    #close the file
    file.close()

    # Copy the file to a new directory and rename it to begin the read operations. 
    # This helps avoid any caching effects
    copy_file(filename)


    # Open the copied file
    file_read = Dataset(f'data/files_read/{filename}_copy.netc', 'r')
    

    # Open a dataset within the file and record the time
    for i in range(0, num_datasets):
        dataset = file_read.variables[f'Dataset_{i}']
 
        if len(dimensions) == 1:
            data = dataset[:dimensions[0]]
        elif len(dimensions) == 2:
            data = dataset[:dimensions[0], :dimensions[1]]
        else:
            data = dataset[:dimensions[0], :dimensions[1], :dimensions[2]]

    #close the copied file   
    file_read.close()

    pass



#custom function to collect Darshan metrics
def collect_darshan_metrics():
    
    return 0


#custom function to analyze Darshan logs/metrics
def analyze_darshan_metrics(darshan_metrics):
    
    pass

def main():
    #Set environment variables
    os.environ['DARSHAN_ENABLED'] = '1'

    #perform I/O operations within the Python Script
    perform_io_operations()

    #save darshan logs/metrics related to Python I/O operations
    darshan_metrics = collect_darshan_metrics()

    #analyze darshan logs or metrics 
    analyze_darshan_metrics(darshan_metrics)


if __name__ == '__main__':
    main()