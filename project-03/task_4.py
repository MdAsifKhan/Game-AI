import numpy as np
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import pdb

class ImitationLearning:

	def __init__(self, data, weights, nm_clusters=20, t_max=100):
		self.x = data
		self.samples = data.shape[0]
		self.som_weights = weights
		self.k = nm_clusters
		self.t_max = t_max
		self.a = np.zeros((data.shape[0],data.shape[1])) # Activity states at 't'
		self.a_tm1 = np.zeros((data.shape[0],data.shape[1])) # Activity states at 't-1'

		self.s = np.zeros(self.samples) # Location states
		#self.r_j = 
		self.joint_prob_s_r = np.zeros((self.som_weights.shape[0], self.k), dtype='float32')

	def clustering(self):
		# Cluster location data into 'l' states using SOM Weights
		# l: number of nodes in SOM Graph
		self.s = np.array([np.argmin([np.linalg.norm(w - x) for w in self.som_weights]) for x in self.x])		
		# Compute player's activity at time t
		for t in range(1,self.samples-1):
			# Action at time t
			self.a[t] = self.x[t+1]-self.x[t]
			# Action at time t-1
			self.a_tm1[t] = self.x[t] - self.x[t-1]
		model = KMeans(n_clusters=self.k, init='random')
		# Cluster player's activity in 'k' clusters
		model.fit(self.a)
		r = model.predict(self.a)
		
		return r, model

	def learning1(self):

		# Calculate Joint Probability
		r, KMeans_model = self.clustering()
		for s_i, r_j in zip(self.s, r):
			self.joint_prob_s_r[s_i,r_j] += 1
		
		self.joint_prob_s_r = self.joint_prob_s_r/(self.joint_prob_s_r.sum().sum())

		x_t = self.x[np.random.randint(self.x.shape[0])]
		trajectory = [x_t]
		for t in range(self.t_max):
			# Nearest state	of a sample point		
			s_i = np.argmin([np.linalg.norm(w - x_t) for w in self.som_weights])
			C = self.joint_prob_s_r[s_i,:].sum()
			if C != 0: self.joint_prob_s_r[s_i,:]/C
			
			a_t = KMeans_model.cluster_centers_[np.argmax(self.joint_prob_s_r[s_i,:])]			
			x_t += a_t
			if x_t[2]<np.amin(self.x, axis=1)[2]: x_t[2] = np.amin(self.x, axis=1)[2]
			if x_t[2]>np.amax(self.x, axis=1)[2]: x_t[2] = np.amax(self.x, axis=1)[2]
			#KMeans_model.cluster_centers_[a_t]
			trajectory.append(np.copy(x_t))

		self.trajectory = np.array(trajectory)

	# Solution to problem in previous stage
	def learning2(self):

		# Calculate Joint Probability
		r, KMeans_model = self.clustering()
		r_tm1 = KMeans_model.predict(self.a_tm1)
		# Probability of executing 'r_t' as a successor of 'r_t-1'
		joint_prob_p_i_j = np.zeros((self.k, self.k), dtype='float32')

		for s_i, r_j,r_t1 in zip(self.s, r, r_tm1):
			self.joint_prob_s_r[s_i,r_j] += 1
			joint_prob_p_i_j[r_t1, r_j] += 1

		cond_prob_s_r = self.joint_prob_s_r/(self.joint_prob_s_r.sum())
		cond_prob_p_i_j = joint_prob_p_i_j/joint_prob_p_i_j.sum()

		x_idx = np.random.randint(self.x.shape[0])
		x_t = self.x[x_idx]
		trajectory = [x_t]
		for t in range(self.t_max):
			# Nearest state	of a sample point		
			s_i = np.argmin([np.linalg.norm(w - x_t) for w in self.som_weights])
			if t<=1:
				prior_action = np.array(trajectory[t]) - self.x[x_idx-1]
			else:
				prior_action = np.array(trajectory[t]) - np.array(trajectory[t-1])				
			
			r_prior = KMeans_model.predict([prior_action])[0]
			
			cond_prob_sr_i_j = np.zeros(self.k)
			for s_j in range(self.k):
				C = np.sum(cond_prob_s_r[s_i,:]*cond_prob_p_i_j[r_prior,:])
				if C != 0: 
					cond_prob_sr_i_j[s_j] = (cond_prob_s_r[s_i,s_j]*cond_prob_p_i_j[r_prior,s_j])/C
				else:
					if np.sum(cond_prob_s_r[s_i,:]) != 0:
						cond_prob_sr_i_j[s_j] = cond_prob_s_r[s_i,s_j]/cond_prob_s_r[s_i,:].sum()

			# If all conditional probabilities are zero just use the joint probability of s and r
			if np.all(cond_prob_sr_i_j==0.):		
				C = self.joint_prob_s_r[s_i,:].sum()
				if C != 0: self.joint_prob_s_r[s_i,:]/C
				a_t = KMeans_model.cluster_centers_[np.argmax(self.joint_prob_s_r[s_i,:])]	
			else:
				dist = cond_prob_sr_i_j/cond_prob_sr_i_j.sum()
				a_t = KMeans_model.cluster_centers_[np.argmax(np.random.multinomial(1,dist))]
			
			x_t += a_t
			if x_t[2]<np.amin(self.x, axis=1)[2]: x_t[2] = np.amin(self.x, axis=1)[2]
			if x_t[2]>np.amax(self.x, axis=1)[2]: x_t[2] = np.amax(self.x, axis=1)[2]
			#KMeans_model.cluster_centers_[a_t]
			trajectory.append(np.copy(x_t))

		self.trajectory = np.array(trajectory)

	def plot_trajectory(self,filename='image.png'):
		fig = plt.figure()
		ax = p3.Axes3D(fig)
		ax.view_init(elev=50, azim=-45)
		ax.plot(self.x[:,0], self.x[:,1], self.x[:,2], 'b-*', alpha=0.2)
		ax.scatter(self.trajectory[0,0], self.trajectory[0,1], self.trajectory[0,2], 'g', alpha=1)		
		ax.plot(self.trajectory[:,0], self.trajectory[:,1], self.trajectory[:,2], 'g-')
		fig.savefig(filename)
		plt.show()


if __name__ == '__main__':
    data1 = np.loadtxt(open('q3dm1-path1.csv', 'rb'), delimiter=',')
    weight1 = np.loadtxt(open('q3dm1_path1_weights.csv', 'rb'), delimiter=',')
    
    iml = ImitationLearning(data1, weight1, nm_clusters=20, t_max=100)
    iml.learning1()
    iml.plot_trajectory('path1_trajectory.png')

    data2 = np.loadtxt(open('q3dm1-path2.csv', 'rb'), delimiter=',')
    weight2 = np.loadtxt(open('q3dm1_path2_weights.csv', 'rb'), delimiter=',')

    iml = ImitationLearning(data2, weight2, nm_clusters=20, t_max=100)
    iml.learning1()
    iml.plot_trajectory('path2_trajectory_1.png')

    iml = ImitationLearning(data2, weight2, nm_clusters=20, t_max=100)
    iml.learning2()
    iml.plot_trajectory('path2_trajectory_2.png')
