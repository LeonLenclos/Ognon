
class Cursor():
    
    def __init__(self, ogn_project):
        self.ogn_project = ogn_project
        self._anim_name = 'master'
        self._layer_idx = 0
        self._frm_idx = 0
        self.playing = False

    def set_anim_name(self, name):
        self._anim_name = name

    def set_layer_idx(self, idx):
        self._layer_idx = idx

    def set_frm_idx(self, idx):
        self._frm_idx = idx

    def set_frm_idx_rel(self, n):
        if self.get_frm_idx() is not None:
            self.set_frm_idx(self.get_frm_idx()+n)

    def get_anim_name(self):
        """Return the anim name. If it does not exists, set it to None."""
        if self._anim_name in self.ogn_project.anims:
            return self._anim_name
        self.set_anim_name(None)
        return None

    def get_layer_idx(self):
        """Return the layer idx. Constrain in layers length.
        Return None if no anim"""
        if self.get_anim_name() is None:
            return None
        self.set_layer_idx(constrain(self._layer_idx, len(self.get_anim().layers)))
        return self._layer_idx

    def get_frm_idx(self):
        """Return the frm idx. Constrain in anim length.
        Return None if no anim"""
        if self.get_anim_name() is None:
            return None
        self.set_frm_idx(constrain(
            self._frm_idx,
            len(self.get_anim()),
            loop = self.ogn_project.get_config('play', 'loop')
        ))
        return self._frm_idx

    def get_anim(self):
        """Return the anim object.
        Return None if no anim"""
        if self.get_anim_name() is None:
            return None
        return self.ogn_project.anims[self.get_anim_name()]

    def get_layer(self):
        """Return the layer object.
        Return None if no layer"""
        if self.get_anim_name() is None or len(self.get_anim().layers) == 0:
            return None
        return self.get_anim().layers[self.get_layer_idx()]

    def get_frm_at(self, i):
        """Return the frm object in the given index.
        Return None if no layer or no frm"""
        if self.get_layer() is None:
            return None
        if i >= len(self.get_layer()):
            return None
        return self.get_layer().frms[i]

    def get_frm(self):
        """Return the frm object.
        Return None if no layer or no frm"""
        return self.get_frm_at(self.get_frm_idx())

    def get_frms(self):
        if self.get_anim_name() is None:
            return []
        return [layer.frms[self.get_frm_idx()] for layer in self.get_anim().layers]

def constrain(value, maxi, loop=False):
    """Retourne une valeur contrainte entre 0 et la longueur de l'anim."""
    if loop:          return value % maxi
    if value <= 0:    return 0
    if value >= maxi: return maxi - 1
    return value
