from . import model

class Cursor():
    
    def __init__(self, proj=None):
        self.proj = proj
        self._pos = {
            'anim':'master',
            'layer':0,
            'frm':0,
        }
        self.playing = False
        self.loop = True

    # Setter and getter for the cursor position.

    def get_pos(self, key=None):
        self.set_pos()
        if key:
            return self._pos[key]
        return self._pos

    def set_pos(self, anim=None, layer=None, frm=None):
        # Set position
        if anim is not None:
            self._pos['anim'] = anim
            self._pos['layer'] = 0
            self._pos['frm'] = 0
        if layer is not None:
            self._pos['layer'] = layer
        if frm is not None:
            self._pos['frm'] = frm
        # Constain anim and layer.
        if self._pos['anim'] not in self.proj.anims:
            self._pos['anim'] = 'master'
        if self._pos['layer'] >= len(self.proj.anims[self._pos['anim']].layers) \
        or self._pos['layer']  < 0:
            self._pos['layer'] = 0   
        # Constrain frm.
        self._pos['frm'] = self.constrain_frm(self._pos['frm'])

    def constrain_frm(self, frm):
        if self.loop:
            return frm % self.anim_len()
        if frm <= 0:
            return 0
        if frm >= self.anim_len():
            return self.anim_len() - 1
        return frm

    # Getter for project's object.

    def get_anim(self, anim=None):
        anim = anim or self.get_pos('anim')
        return self.proj.anims[anim]

    def get_layer(self, anim=None, layer=None):
        layer = layer if layer is not None else self.get_pos('layer')
        return self.get_anim(anim).layers[layer]

    def get_element_pos(self, anim=None, layer=None, frm=None):
        """Return a tuple with the index of the element in the layer, the
        element object and the position of the cursor inside the element
        Return None if no element"""
        layer = self.get_layer(anim, layer)
        frm = frm if frm is not None else self.get_pos('frm')
        frm_ = 0
        for i, e in enumerate(layer.elements):
            frm_ += self.element_len(e)
            if frm_ > frm:
                return i, e, frm_ - frm - 1


    def get_element(self, anim=None, layer=None, frm=None):
        return self.get_element_pos(anim, layer, frm)[1]

    # Method for objects' length

    def anim_len(self, anim=None):
        anim = anim if anim else self._pos['anim']
        layer_len = lambda layer : sum(map(self.element_len, layer.elements))
        return layer_len(max(self.proj.anims[anim].layers, key=layer_len))

    def element_len(self, elmt):
        """return the length of the element"""
        if isinstance(elmt, model.Cell):
            return 1
        elif isinstance(elmt, model.AnimRef):
            return self.anim_len(elmt.name)
        else:
            raise TypeError('Unknow element type')