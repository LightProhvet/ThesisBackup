enabled_axes = None

class Axis:
    def __init__(self, axis, lock, id):
        self.axis = axis
        self.lock = lock
        self.id = id

# Enable only a subset of axes of the form [(1234567890, 0), ...]
def enable_only_axes(odrv_ids_and_axes):
    print('Enabling only the following pairs of ODrives and their axes: {}'.format(odrv_ids_and_axes))
    global enabled_axes
    enabled_axes = odrv_ids_and_axes

def is_odrv_enabled(odrv_id):
    return enabled_axes is None or odrv_id in [x[0] for x in enabled_axes]

def is_axis_enabled_iter(odrv):
    for o in odrv:
        yield enabled_axes is None or (o.id, 0) in enabled_axes
        yield enabled_axes is None or (o.id, 1) in enabled_axes

def axes_of(odrv):
    axis_filter = is_axis_enabled_iter(odrv)
    for o in odrv:
        if next(axis_filter):
            yield Axis(o.odrv.axis0, o.lock, (o.id, 0))
        if next(axis_filter):
            yield Axis(o.odrv.axis1, o.lock, (o.id, 1))

