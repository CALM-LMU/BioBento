from biodetectron.eval import BboxPredictor

import bentoml
from bentoml.adapters import ImageInput
from bentoml.artifact import PytorchModelArtifact

predictor = BboxPredictor('/home/bunk/MitoScanner/boxes.yaml', '/home/bunk/MitoScanner/boxes_final.pth')

@bentoml.env(docker_base_image='davidbunk/biodetectron:latest')
@bentoml.artifacts([PytorchModelArtifact('mitoscanner')])
class MitoScanner(bentoml.BentoService):
    @bentoml.api(input=ImageInput())
    def predict(self, imgs):
        outputs = predictor.detect_one_image(imgs)
        return outputs

svc = MitoScanner()
svc.pack('mitoscanner', predictor.model)

saved_path = svc.save()