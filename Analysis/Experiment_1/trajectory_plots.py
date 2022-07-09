import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from ast import literal_eval
import os
from glob import glob


def reformat_condition_data(dat, anim_trajFiles, phys_trajFiles, cf_trajFiles):
    vid_dat = dat.groupby(['vid_num', 'agent']).mean()
    vid_dat[['p0', 'p1']] = ''
    vid_dat['closeness'] = 0
    top_pocket = np.array([54.40703582763672, 25.04831886291504])  # got this values from blender file 1_p_in_out.blend
    bottom_pocket = np.array([54.350181579589844, 2.945833206176758])  # got this values from blender file 12a_in_in_rev.blend

    for i in range(len(phys_trajFiles)):
        path = phys_trajFiles[i]
        cond = path.split('/')[-1].split('.')[0].split('_')
        phys_traj = get_trajectory(phys_trajFiles[i])
        cf_traj = get_trajectory(cf_trajFiles[i])

        if (cond[2] == 'in') and (cond[3] == 'out'):
            p0 = np.array(phys_traj.iloc[-1].B[:2])  # just use XY, so 2D
            bb = cf_traj.B.apply(pd.Series)
            maxX = bb.loc[bb[0] == max(bb[0])].index[0]
            p1 = np.array(cf_traj.iloc[maxX].B[:2])
        if (cond[2] == 'in') and (cond[3] == 'in'):
            p0 = np.array(phys_traj.iloc[-1].B[:2])
            if i == 9:  # this is because I screwed up the counterfactual for vid 10
                p1 = np.array(phys_traj.iloc[-1].B[:2])
            else:
                p1 = np.array(cf_traj.iloc[-1].B[:2])
        if (cond[2] == 'out') and (cond[3] == 'out'):
            bb = cf_traj.B.apply(pd.Series)
            maxX = bb.loc[bb[0] == max(bb[0])].index[0]
            p1 = np.array(cf_traj.iloc[maxX].B[:2])
            possibpocket = [np.linalg.norm(top_pocket - p1), np.linalg.norm(bottom_pocket - p1)]
            p0 = np.array([top_pocket, bottom_pocket])[possibpocket == min(possibpocket)][0]
        if (cond[2] == 'out') and (cond[3] == 'in'):
            p0 = np.array(cf_traj.iloc[-1].B[:2])
            bb = cf_traj.B.apply(pd.Series)
            maxX = bb.loc[bb[0] == max(bb[0])].index[0]
            p1 = np.array(cf_traj.iloc[maxX].B[:2])

        dist = np.linalg.norm(p0 - p1)
        vid_dat.at[(i + 1, 'animate'), 'p0'] = tuple(p0)
        vid_dat.at[(i + 1, 'inanimate'), 'p0'] = tuple(p0)
        vid_dat.at[(i + 1, 'animate'), 'p1'] = tuple(p1)
        vid_dat.at[(i + 1, 'inanimate'), 'p1'] = tuple(p1)
        vid_dat.loc[(i + 1,), 'closeness'] = dist

    vid_dat.reset_index(inplace=True)
    return vid_dat


def trajectory_difference(traj1, traj2, ball, plot=False, cf=False, verbose=False):
    """
    Function to compute the distance between a given ball in two trajectories.

    :param traj1: pandas Dataframe with columns 'A' & 'B' where each index is a frame and values are the xyz coordinates of each ball.
    :param traj2: pandas Dataframe with columns 'A' & 'B' where each index is a frame and values are the xyz coordinates of each ball.
    :param ball: str: the ball you're interest
    :param plot: Bool: whether or not you want to visuali
    :param verbose: Bool: whether to print sum of the distance between 'ball' in trajectories.
    :return: list: the of the distance between 'ball' in traj1 and traj 2 for each frame.
    """
    t_diffs = []
    for t in range(len(traj1)):
        t_diffs.append(np.linalg.norm(np.asarray(traj1.loc[t, ball]) - np.asarray(traj2.loc[t, ball])))
    if ball == 'A': # compute difference only after the collision
        traj1['distance']= [np.linalg.norm(np.asarray(traj1.loc[t, 'A']) - np.asarray(traj1.loc[t, 'B'])) for t in range(250)]
        t_collision = traj1['distance'].idxmin()  #becuase python starts w 0
        t_diffs = t_diffs[t_collision:]

    if plot:
        plt.plot(t_diffs)
    total_diff = sum(t_diffs)
    if verbose:
        print(f'total difference between ball trajectories: {total_diff}')
    if cf:
        x = np.array(t_diffs)
        return np.mean(x[x>0])

    return total_diff


def get_trajectory(path):
    traj = pd.read_csv(path,  names=['A', 'B'])
    for ball in ['A', 'B']:
        traj[ball] =  traj[ball].apply(literal_eval)
    return traj


def get_velocity(traj, at_collision=False, pre_collision=False):
    traj.loc[1:249, 'A_fwd'] = [np.linalg.norm(np.array(traj.A[t-1]) - np.array(traj.A[t])) for t in range(1, len(traj))]
    #vel = np.gradient(traj.A_fwd.cumsum())
    #vel = traj.A_fwd.cumsum()
    vel = traj.A_fwd
    if at_collision:
        dist = pd.Series([np.linalg.norm(np.asarray(traj.loc[t, 'A']) - np.asarray(traj.loc[t, 'B'])) for t in range(len(traj))])
        t_collision = dist.iloc[30:].idxmin() #looking from frame 30 on because in vid 9/10, balls overlap before the animation, so the .minidx() is artificially early.
        return vel[t_collision]
    if pre_collision:
        dist = pd.Series([np.linalg.norm(np.asarray(traj.loc[t, 'A']) - np.asarray(traj.loc[t, 'B'])) for t in range(len(traj))])
        t_collision = dist.iloc[30:].idxmin()
        return vel[:t_collision]

    return vel


def plot_stimTrajectory(stim1, stim2,stim3, filename=None):
    f, a = plt.subplots(figsize=(15, 5), ncols=3, sharey=True)

    a[0].scatter(*zip(*stim1.B))
    a[0].scatter(*zip(*stim1.A), color='r')
    a[0].set_title("INANIMATE")
    a[0].set_aspect(2)
    a[1].scatter(*zip(*stim2.B))
    a[1].scatter(*zip(*stim2.A), color='r')
    a[1].set_title("ANIMATE")
    a[1].set_aspect(2)
    a[2].scatter(*zip(*stim3.B))
    a[2].set_title("COUNTERFACTUAL")
    a[2].set_aspect(2)
    if filename:
        plt.savefig(filename, dpi=80)


def plot_trajectory(stimulus, plot_labels, filename=None):
    """

    :param stimulus: pd.Dataframe or list of pd.Dataframes with columns 'A' and 'B'
    :param filename: str, path and filename to save
    :param plot_labels: list, list of strings denoting stimulus types (inanimate, animate, cf) in stimulus arg. MUST be in the same order as stimulus list
    :return:
    """
    if type(stimulus) != list:
        stimulus = [stimulus]
    f, a = plt.subplots(figsize=((5*len(stimulus)), 5), ncols=3, nrows=int(len(stimulus)/3),  sharey=True)
    for i, stim in enumerate(stimulus):
        a[i].scatter(*zip(*stim.B))
        if plot_labels[i] != 'Counterfactual':
            a[i].scatter(*zip(*stim.A), color='r')
        a[i].set_title(plot_labels[i])
        a[i].set_aspect(2)
    if filename:
        plt.savefig(filename, dpi=80)


def plotAllTrajectories(f, ax, anim_trajFiles, phys_trajFiles, cf_trajFiles, vid_dat=None, filename=None):

    plt.rcParams["figure.autolayout"] = True
    im = plt.imread('/Users/bryangonzalez/BilliardsApp/Analysis/Experiment_1/table.png')
    im[:, :, -1] = .3

    #f, ax = plt.subplots(figsize=(15, (5*len(phys_trajFiles))), ncols=3, nrows=len(phys_trajFiles),  sharey=True)
    for row, (anim, phys, cf) in enumerate(zip(anim_trajFiles, phys_trajFiles, cf_trajFiles)):
        traj_a = get_trajectory(anim)
        traj_p = get_trajectory(phys)
        traj_cf = get_trajectory(cf)
        if vid_dat is not None:
            ax[row, 2].scatter(*vid_dat.loc[vid_dat.vid_num == int(row+1)].p0.values[0], color='y', zorder=2)
            ax[row, 2].scatter(*vid_dat.loc[vid_dat.vid_num == int(row+1)].p1.values[0], color='y', zorder=2)

        for col, (stim, label, cond) in enumerate(zip([traj_p, traj_a, traj_cf], ['inanimate','animate', 'Counterfactual'], (anim, phys, cf))):
            ax[row, col].imshow(im, zorder=1, extent=[0, 61.5, -1, 31])
            ax[row, col].scatter(*zip(*stim.B), zorder=2)
            condition = cond.split('/')[-1].split('.')[0].split('_')

            if label != 'Counterfactual':
                ax[row, col].scatter(*zip(*stim.A), color='r', zorder=2)
                if vid_dat is not None:
                    caus_mean = round(vid_dat.loc[(vid_dat.vid_num == int(condition[0])) & (vid_dat['agent'] == label), 'causal_rating'].values[0], 2)

                    #ax[row, col].text(5, 25, f"M = {caus_mean}", fontsize=18, color='w' )
            ax[row, col].set_title('stim'+str(row+1)+' '+label+' outcome: '+condition[2]+' cf: '+condition[3])
            ax[row,col].set_ylim(ymin=0.0)
            ax[row, col].xaxis.set_visible(False)
            ax[row, col].yaxis.set_visible(False)

    plt.show()
    if filename:
        plt.savefig(filename, dpi=80)
    return f
