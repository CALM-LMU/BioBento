import torch
import logging

import numpy as np
from skimage.measure import regionprops
from skimage.exposure import rescale_intensity

import base64
from PIL import Image
from io import BytesIO

import bentoml
from bentoml.adapters import ImageInput
from bentoml.artifact import PytorchModelArtifact

@bentoml.env(docker_base_image='davidbunk/biodetectron:latest')
@bentoml.artifacts([PytorchModelArtifact('model')])
class YeastMate(bentoml.BentoService):
    @bentoml.api(input=ImageInput())
    def predict(self, image):
        logging.disable(logging.CRITICAL)

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
            pred = self.artifacts.model([image])[0]

        boxes = list(pred['instances'].pred_boxes)
        boxes = [tuple(box.cpu().numpy()) for box in boxes]

        masks = list(pred['instances'].pred_masks)
        masks = [mask.cpu().numpy() for mask in masks]

        scores = list(pred['instances'].scores)
        scores = [score.cpu().numpy() for score in scores]

        classes = list(pred['instances'].pred_classes)
        classes = [cls.cpu().numpy() for cls in classes]

        new_mask = np.zeros((height, width, 4), dtype=np.uint16)

        res = []
        for n, mask in enumerate(masks):
            mask = mask.astype(np.uint16)

            tmp = new_mask[:,:,classes[n]]
            tmp[mask > 0] = n + 1
            new_mask[:,:,classes[n]] = tmp

            x1, y1, x2, y2 = map(int, boxes[n])

            obj = {'id': n+1, 'class': int(classes[n]), 'box': [x1, y1, x2, y2], 'score': float(np.round(scores[n], decimals=2))}
            res.append(obj)

        return {"things": res, "mask": new_mask.flatten(), 'height': height, 'width': width, "channel": 4}

    @bentoml.api(input=ImageInput())
    def predict_fiji(self, image):
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

        result = {'things': []}
        for t, thing in enumerate(things):
            assert meta[t]['id'] == thing.label

            if meta[t]['isthing']:
                y1, x1, y2, x2 = map(int, thing.bbox)

                crop = thing.image.astype(np.uint8)
                crop[crop > 0] = 255
                crop = Image.fromarray(crop)
                
                buff = BytesIO()
                crop.save(buff, format='PNG')
                base64_string = base64.b64encode(buff.getvalue())

                obj = {'id': meta[t]['id'], 'class': meta[t]['category_id'], 'box': [x1, y1, x2, y2], 'mask': base64_string, 'score': np.round(meta[t]['score'], decimals=2)}
                result['things'].append(obj)

        return result
                



        

