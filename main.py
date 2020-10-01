import torch

import numpy as np
from skimage.measure import regionprops
from skimage.exposure import rescale_intensity

import bentoml
from bentoml.adapters import ImageInput
from bentoml.artifact import PytorchModelArtifact

@bentoml.env(docker_base_image='davidbunk/biodetectron:latest')
@bentoml.artifacts([PytorchModelArtifact('model')])
class YeastMate(bentoml.BentoService):
    @bentoml.api(input=ImageInput())
    def predict(self, imgs):
        image = imgs[0]
        
        if len(image.shape) < 3:
            image = np.expand_dims(image, axis=-1)
        elif image.shape[-1] == 1:
            image = np.repeat(image, 3, axis=-1)

        image = image.astype(np.float32)
        image = rescale_intensity(image)

        height, width = image.shape[0:2]
        image = torch.as_tensor(image.transpose(2,0,1).astype("float32"))  
        image = {"image": image, "height": height, "width": width}

        with torch.no_grad():
            mask, meta = self.artifacts.model([image])[0]["panoptic_seg"]

        things = regionprops(mask.cpu().numpy())

        result = {'boxes': [], 'classes': [], 'scores': []}
        for n, thing in enumerate(things):
            assert meta[n]['id'] == thing.label

            if meta[n]['isthing']:
                result['boxes'].append(thing.bbox)
                result['classes'].append(meta[n]['category_id'])
                result['scores'].append(np.round(meta[n]['score'], decimals=2))

        return result

                



        

