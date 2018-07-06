import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d
import pandas as pd

class SOM:

    def __init__(self, data, nodes=50, t_max=200):
        self.data = data
        self.t_max = t_max
        self.nodes = nodes
        self.eta = 1
        self.sigma = np.exp(1./t_max)
        self.weight = self.data[np.random.randint(data.shape[0],size=self.nodes),:]

    def topological_distance(self, v_i):
        # length of shortest path with circular topology
        v_i = np.repeat(v_i, self.nodes)
        v_j = np.linspace(0, self.nodes-1, self.nodes)
        length_path1 = abs(v_i-v_j)
        length_path2 = abs(self.nodes+v_j-v_i)
        return np.minimum(length_path1, length_path2)

    def winner_neuron(self, sample):
        sample = np.repeat(sample[np.newaxis,:], self.nodes, axis=0)
        return np.argmin(np.linalg.norm(self.weight - sample, axis=1))   

    def plot_data(self):
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        ax.scatter3D(self.data[:,0],self.data[:,1],self.data[:,2], c='purple', marker='o', s=1)
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')    
        return ax
    
    def save_weights(self, filename='weights.csv'):
        df = pd.DataFrame(self.weight)
        df.to_csv(filename, index=None)

    def som(self):
        ax = self.plot_data()
        plot = None
        # Run a loop for t_max iterations
        for t in range(self.t_max):
            print('Iteration {0:2f}'.format(t))
            print('Learning Rate {0:2f} and sigma {1:2f}'.format(self.eta,self.sigma))
            # Randomly sample a point
            x = self.data[np.random.randint(self.data.shape[0])]
            # Visualize sample point
            sample_point = ax.scatter3D(x[0], x[1], x[2], c='g')
            # Find winner neuron
            v_i = self.winner_neuron(x)
            # Length of shortest path circular topology
            D_ij = self.topological_distance(v_i)

            x = np.repeat(x[np.newaxis,:],self.nodes, axis=0) 
            self.weight += self.eta * np.exp(-0.5 * D_ij / self.sigma)[:,np.newaxis]*(x-self.weight)
            self.eta = 1 - (float(t+1)/float(self.t_max))
            self.sigma = np.exp((float(-t+1)/float(self.t_max)))

            # Visualize weights 
            circular_plot = np.vstack((self.weight, self.weight[0].reshape(-1,self.weight.shape[1])))
            if plot:    ax.lines.pop(0)
            plot = ax.plot(circular_plot[:,0], circular_plot[:,1], circular_plot[:,2], 'r-o')
            sample_point.set_offsets(x[:2])
            sample_point.remove()
            plt.pause(.0001)
        return plt

if __name__ == '__main__':
    data1 = np.loadtxt(open('q3dm1-path1.csv', 'rb'), delimiter=',')
    data2 = np.loadtxt(open('q3dm1-path2.csv', 'rb'), delimiter=',')
    
    nodes = 20
    t_max = 100
    # SOM for trajectory 1
    print('SOM for trajectory 1')
    som_ = SOM(data1, nodes, t_max)
    plt1 = som_.som()
    som_.save_weights('q3dm1_path1_weights.csv')

    # SOM for trajectory 2
    print('SOM for trajectory 2')
    som_ = SOM(data2, nodes, t_max)
    plt2 = som_.som()
    som_.save_weights('q3dm1_path2_weights.csv')

    plt1.show()
    plt2.show()
