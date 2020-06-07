import torch
from torchvision import transforms
from PIL import Image

from .model import SSD300
from .definitions import ROOT_DIR, device
from .utils import label_map, rev_label_map

class InferencingModel():

    def __init__(self, **kwargs):
        self.n_classes = len(label_map)
        self.transforms = transforms.Compose([
            transforms.Resize((300, 300)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225]),
            ])

        if 'checkpoint_file' in kwargs.keys():
            self.init_with_checkpoint(kwargs['checkpoint_file'])
        if 'artifact' in kwargs.keys():
            self.init_with_artifact(kwargs['artifact'])

        self.model.to(device)
        self.model.eval()

    def init_with_checkpoint(self, checkpoint_file):
        # load checkpoint
        checkpoint = torch.load(checkpoint_file,
                                map_location=device)

        model = SSD300(self.n_classes)
        self.model = model
        self.model.load_state_dict(checkpoint['model_state'])

    def init_with_artifact(self, artifact):
        self.model = artifact

    def __call__(self, original_img, min_score, top_k, max_overlap):
        img = self.transforms(original_img)

        pred_locs, pred_scores = self.model(img.unsqueeze(0))
        print(pred_locs.shape, pred_scores.shape)

        det_boxes, det_labels, det_scores = self.model.detect_objects(
                                            pred_locs,
                                            pred_scores,
                                            min_score=min_score,
                                            top_k=top_k,
                                            max_overlap=max_overlap,
                                            )
        print(det_boxes, det_labels, det_scores)

        original_dims = torch.FloatTensor([
                                        original_img.width,
                                        original_img.height,
                                        original_img.width,
                                        original_img.height,
                                        ]).unsqueeze(0)
        det_boxes = det_boxes[0] * original_dims

        det_labels = [rev_label_map[l] for l in det_labels[0].tolist()]

        return det_labels, det_boxes.detach().numpy()

if __name__ == '__main__':
    checkpoint = ROOT_DIR/'output/checkpoint_ssd300-150.pth.tar'
    model = InferencingModel(checkpoint_file=checkpoint)

    # load img
    img_path = ROOT_DIR/'data/VOC2007/JPEGImages/000001.jpg'
    orginal_img = Image.open(img_path, mode='r')
    orginal_img = orginal_img.convert('RGB')

    labels, boxes = model(orginal_img, min_score=0.2, top_k=200, max_overlap=0.5)

    print(labels, boxes)
