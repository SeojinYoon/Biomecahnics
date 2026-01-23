
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from ipywidgets import interact, IntSlider

def plot_arm(ax,
             shoulder_position: np.ndarray,
             elbow_position: np.ndarray,
             wrist_position: np.ndarray,
             xlabel = "X",
             ylabel = "Y",
             zlabel = "Z"):
    """
    Plot arm links
    
    :param ax: matplotlib 3d axis
    :param shoulder_position: 3d position of shoulder joint (x,y,z)
    :param elbow_position: 3d position of elbow joint (x,y,z)
    :param wrist_position: 3d position of wrist joint (x,y,z)
    """
    pos = np.row_stack((shoulder_position, elbow_position, wrist_position))
    
    # Plot
    ax.plot(pos[:, 0], pos[:, 1], pos[:, 2], color = "black")
    scatter = ax.scatter(pos[:, 0], pos[:, 1], pos[:, 2], c = np.arange(len(pos)), cmap = "rainbow", s=100)
    handles, labels = scatter.legend_elements(prop="colors")
    ax.legend(handles, ["Shoulder", "Elbow", "Hand"], loc="upper right", title="Joint label")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)

def visualize_dynamic_arm(shoulder_positions: np.ndarray,
                          elbow_positions: np.ndarray,
                          wrist_positions: np.ndarray,
                          joint_angles: np.ndarray,
                          joint_angle_labels: np.ndarray,
                          xlabel = "X",
                          ylabel = "Y",
                          zlabel = "Z",
                          x_range = None,
                          y_range = None,
                          z_range = None,
                          camera_info = {}):
    """
    Visualize arm position per step with interactive slider
    
    :param shoulder_positions(shape - #step, xyz): shoulder position per step
    :param elbow_positions(shape - #step, xyz): elbow position per step
    :param wrist_positions(shape - #step, xyz): wrist position per step
    :param joint_angles(shape - #joint, #step): joint angles per step
    :param joint_angle_labels(shape - #joint): joint angle labels
    """
    n_step = shoulder_positions.shape[0]
    cmap = plt.get_cmap("rainbow")

    if x_range is None:
        min_x = min(np.min(shoulder_positions[:,0]), np.min(elbow_positions[:,0]), np.min(wrist_positions[:,0]))
        max_x = max(np.max(shoulder_positions[:,0]), np.max(elbow_positions[:,0]), np.max(wrist_positions[:,0]))
    else:
        min_x, max_x = x_range

    if y_range is None:
        min_y = min(np.min(shoulder_positions[:,1]), np.min(elbow_positions[:,1]), np.min(wrist_positions[:,1]))
        max_y = max(np.max(shoulder_positions[:,1]), np.max(elbow_positions[:,1]), np.max(wrist_positions[:,1]))
    else:
        min_y, max_y = y_range

    if z_range is None:
        min_z = min(np.min(shoulder_positions[:,2]), np.min(elbow_positions[:,2]), np.min(wrist_positions[:,2]))
        max_z = max(np.max(shoulder_positions[:,2]), np.max(elbow_positions[:,2]), np.max(wrist_positions[:,2]))
    else:
        min_z, max_z = z_range
    
    # Setting slider
    slider = IntSlider(min=0, max=n_step - 1, step=1, layout={'width': '600px'})

    @interact(step_i=slider)
    def plot_frame(step_i):
        # Data
        s = shoulder_positions[step_i]
        e = elbow_positions[step_i]
        w = wrist_positions[step_i]
        
        link_pos = np.row_stack((s, e, w)) 
        joint_names = ['Shoulder', 'Elbow', 'Hand']

        # Setting for figure
        fig = plt.figure(figsize=(12, 6))
        
        ## GridSpec
        gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1]) 
        gs_right = gridspec.GridSpecFromSubplotSpec(
            2, 2, 
            subplot_spec=gs[0, 1],
            hspace=0.4,
            wspace=0.6,
        )
        
        # Main 3D arm plot
        ax_big = fig.add_subplot(gs[0, 0], projection='3d')
        plot_arm(ax_big, shoulder_positions[step_i], elbow_positions[step_i], wrist_positions[step_i])
        ax_big.scatter(wrist_positions[:step_i, 0], wrist_positions[:step_i, 1], wrist_positions[:step_i, 2], color='gray', alpha=0.5)
        ax_big.set_title(f"Arm (Step {step_i})")
        ax_big.set_xlim(min_x, max_x)
        ax_big.set_ylim(min_y, max_y)
        ax_big.set_zlim(min_z, max_z)
        ax_big.set_xlabel(xlabel)
        ax_big.set_ylabel(ylabel)
        ax_big.set_zlabel(zlabel)
        ax_big.view_init(elev=camera_info.get("elev", 40), azim=camera_info.get("azim", -145))
        
        # Joint angles
        for joint_i in range(len(joint_angles)):
            ax = fig.add_subplot(gs_right[joint_i])
            ax.plot(joint_angles[joint_i, :step_i])
            ax.set_xlim(0, n_step)
            ax.set_ylim(np.min(joint_angles[joint_i]), np.max(joint_angles[joint_i]))
            ax.set_title(joint_angle_labels[joint_i])
        plt.tight_layout()
        plt.show()
        
if __name__ == "__main__":
    upperarm_length, forearm_length = 33, 26
    origin = np.array([0, 0, 0]) # Shoulder (Global origin)
    elbow = np.array([0, -upperarm_length, 0]) # Elbow position relative to Shoulder
    hand = np.array([0, -forearm_length, 0]) # Hand position relative to Elbow
    initial_pos = np.column_stack((origin, elbow, hand + elbow))
    
    fig = plt.figure(figsize=[5, 5])
    ax = fig.add_subplot(111, projection='3d')
    plot_arm(ax, initial_pos[:, 0], initial_pos[:, 1], initial_pos[:, 2])
    ax.set_xlabel("X (LR)")
    ax.set_ylabel("Y (AP)")
    ax.set_zlabel("Z (IS)")
    