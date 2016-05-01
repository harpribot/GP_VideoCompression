import numpy as np
import pandas as pd
import glob
import scipy.io as sio
from sklearn import gaussian_process
from sklearn.externals.joblib import Parallel,delayed
import itertools


class Compressor:
    def __init__(self, frame_dir):
        self.frame_dir = frame_dir
        self.gp_map = {}
        self.gp_map_parallel = {}

    def load_frames(self):
        files = glob.glob(self.frame_dir)
        self.num_frames = len(files)
        self.frames = {}
        for frame in files:
            mat = sio.loadmat(frame)
            frame_id = int(frame.split('.')[0].split('_')[2])
            self.frames[frame_id] = mat['image_gray']
        self.num_rows, self.num_cols = self.frames[1].shape


    def set_compressed_total_frames(self,frame_count=10):
        self.compressed_num_frames = frame_count
        self.__initialize_labelled_frames()

    def __initialize_labelled_frames(self):
        self.full_range = range(1, self.num_frames + 1)
        self.x_trn = range(1,self.num_frames + 1, self.compressed_num_frames)
        self.y_trn = np.array([self.frames[x] for x in self.x_trn])
        self.x_tst = [x for x in self.full_range if x not in self.x_trn]

    def fit(self, parallel = False):
        if parallel: # In progress not working. Due to issues with parallelizing instances
            i_range = range(self.num_rows)
            j_range = range(self.num_cols)
            Parallel(n_jobs=2)(delayed(self.__fit_parallel)(i, j,self.x_trn, self.y_trn, self.gp_map_parallel) for i,j in itertools.product(i_range, j_range))
            assert((1,1) in self.gp_map_parallel, 'gp_map not getting updated')
        else:
            for i in range(self.num_rows):
                print 'Fitting Row : %d of %d rows' %(i,self.num_rows)
                for j in range(self.num_cols):
                    X = np.atleast_2d(self.x_trn).T
                    y = self.y_trn[:,i,j]
                    gp = gaussian_process.GaussianProcess(theta0=1e-2, thetaL=1e-4, thetaU=1e-1)
                    gp.fit(X,y)
                    self.gp_map[(i,j)] = gp

    def __fit_parallel(self, i, j, x_trn, y_trn, gp_map):
        X = np.atleast_2d(x_trn).T
        y = y_trn[:,i,j]
        gp = gaussian_process.GaussianProcess(theta0=1e-2, thetaL=1e-4, thetaU=1e-1)
        gp.fit(X,y)
        gp_map[(i,j)] = gp


    def predict(self):
        for i in range(self.num_rows):
            print 'Predicting Row : %d of %d rows' %(i,self.num_rows)
            for j in range(self.num_cols):
                X = np.atleast_2d(self.x_tst).T
                gp = self.gp_map[(i,j)]
                y_pred, sigma2_pred = gp.predict(X, eval_MSE=True)
                count = 0
                for t in X:
                    self.frames[t[0]][i,j] = y_pred[count]
                    count += 1

    def store_produced_frames(self, outdir):
        for t in self.full_range:
            frame_name = outdir + '/frame_' + str(t) + '.mat'
            sio.savemat(frame_name, {'image_gray':self.frames[t]})
