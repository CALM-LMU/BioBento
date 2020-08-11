from biodetectron.eval import BboxPredictor, MaskPredictor

import bentoml
from bentoml.adapters import ImageInput
from bentoml.artifact import PytorchModelArtifact

box_predictor = BboxPredictor('/home/bunk/MitoScanner/boxes.yaml', '/home/bunk/MitoScanner/boxes_final.pth')
mask_predictor = MaskPredictor('/home/bunk/MitoScanner/masks.yaml', '/home/bunk/MitoScanner/masks_final.pth')

@bentoml.env(docker_base_image='davidbunk/biodetectron:latest')
@bentoml.artifacts([PytorchModelArtifact('mitoscanner_box'), PytorchModelArtifact('mitoscanner_mask')])
class MitoScanner(bentoml.BentoService):
    @bentoml.api(input=ImageInput())
    def predict_box(self, imgs):
        outputs = box_predictor.detect_one_image(imgs)
        return outputs

    @bentoml.api(input=ImageInput())
    def predict_mask(self, imgs):
        outputs = mask_predictor.detect_one_image(imgs)
        return outputs

svc = MitoScanner()
svc.pack('mitoscanner_box', box_predictor.model)
svc.pack('mitoscanner_mask', mask_predictor.model)

saved_path = svc.save()