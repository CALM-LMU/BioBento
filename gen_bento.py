from biodetectron.eval import MaskPredictor

from main import YeastMate

maskpred = MaskPredictor('/home/bunk/BioDetectron/biodetectron/configs/yeastmate_mother.yaml', '/scratch/bunk/logs/osman_mother/121020_181413/model_0046999.pth')

svc = YeastMate()
svc.pack('model', maskpred.model)

saved_path = svc.save()
print('Bento Service Saved in ', saved_path)