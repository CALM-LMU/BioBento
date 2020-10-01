from biodetectron.eval import MaskPredictor

from main import YeastMate

maskpred = MaskPredictor('/home/bunk/BioDetectron/biodetectron/configs/yeastmate.yaml', '/scratch/bunk/logs/yeastmate/092820_170831/model_0045999.pth')

svc = YeastMate()
svc.pack('model', maskpred.model)

saved_path = svc.save()
print('Bento Service Saved in ', saved_path)