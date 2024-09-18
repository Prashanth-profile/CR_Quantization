import matplotlib.pyplot as plt

# Sample plot
fig, ax = plt.subplots()
lines = ax.plot([0, 1, 2], [0, 1, 0], label='Line')
legend = ax.legend()

# Variables to store the dragging state and initial position
dragging = False
legend_position = None

def on_pick(event):
    global dragging, legend_position
    if event.artist == legend:
        dragging = True
        # Get the initial position of the legend
        bbox = legend.get_window_extent()
        legend_position = (event.mouseevent.x, event.mouseevent.y)

def on_motion(event):
    global dragging, legend_position
    if dragging:
        dx = event.x - legend_position[0]
        dy = event.y - legend_position[1]
        # Update the legend position
        bbox = legend.get_window_extent()
        fig_x = bbox.x0 + dx
        fig_y = bbox.y0 + dy
        legend_position = (event.x, event.y)
        # Convert pixel coordinates to axes coordinates
        inv = ax.transAxes.inverted()
        new_pos = inv.transform((fig_x, fig_y))
        legend.set_bbox_to_anchor(new_pos, transform=ax.transAxes)
        fig.canvas.draw()

def on_release(event):
    global dragging
    dragging = False

# Connect the event handlers
fig.canvas.mpl_connect('pick_event', on_pick)
fig.canvas.mpl_connect('motion_notify_event', on_motion)
fig.canvas.mpl_connect('button_release_event', on_release)

# Enable picking on the legend
legend.set_picker(True)

plt.show()
