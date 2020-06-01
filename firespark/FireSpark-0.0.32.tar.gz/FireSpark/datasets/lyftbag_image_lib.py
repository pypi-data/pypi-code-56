# FireSpark -- the Data Work
# Copyright 2020 The FireSpark Author. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""FireSpark lyftbag dataset utility library

Methods for packing information from level5 camera lyftbag data to MAS protobuf.
Note: there is no annotation information for data parsed from lyftbags.

"""

import os
import tqdm
import ntpath
import tempfile
import shutil
import base64

from ..core.proto_utils import ProtoDataset
from ..core.lyftbag_utils import LyftbagParser
from ..protos.mas import image_data_pb2 as image_proto


class LyftbagDataset(ProtoDataset):
    """ Level5 Lmdb dataset class """
    topics = ['/cam0/image_compressed',
              '/cam1/image_compressed',
              '/cam2/image_compressed',
              '/cam3/image_compressed',
              '/cam4/image_compressed',
              '/cam5/image_compressed',
              '/cam6/image_compressed',
              '/cam7/image_compressed',
              '/cam8/image_compressed'
              ]

    def __init__(self, **job):
        super().__init__(**job)
    
    def _record_provider(self):
        """ provide raw lyftbag files from the source dataset directory """
        if not os.path.isdir(self._datasrc): return
        records = []
        for r, _, f in os.walk(self._datasrc):
            local_files = [os.path.join(r, file) for file in f if file.endswith('.lyftbag')]
            records.extend(local_files)
        self._n_records = len(records)
        for r in records:
            yield r
    
    def get_data_from_files(self, record:str) -> dict:
        """ Method for extracting lyftbag camera image data from a local record.

            Args:
                record: lyftbag file or key to lyftbag file
        
            Returns: a dict object containing frame data
        """
        if self._bucket_name:
            workspace_ = tempfile.mkdtemp()
            lyftbag = os.path.join(workspace_, ntpath.basename(record))
            self.aws.download_file(self._bucket_name, record, lyftbag)
            record = lyftbag
        cam_data = {}
        bag_parser = LyftbagParser(record, topics=self.topics)
        for frame in bag_parser.frames:
            if frame['payload'] is not None:
                camera_id = frame['metadata']['topic'].split("/")[1]
                if not camera_id in cam_data.keys():
                    cam_data[camera_id] = {}
                if not 'trigger_time' in frame['payload']['metadata'].keys():
                    meta_data_ts = frame['metadata']['message_header']['lct_timestamp']
                else:
                    meta_data_ts = frame['payload']['metadata']['trigger_time']                
                timestamp_ns = int(meta_data_ts['boot_time_ns']) \
                    + int(meta_data_ts['time_since_boot_ns'])
                cam_data[camera_id].update({timestamp_ns: frame['payload']})
        if self._bucket_name: shutil.rmtree(workspace_)
        return cam_data

    def _add_to_proto(self, record: dict) -> dict:
        """ Method for processing level5 lyftbag cam frame to protobuf message

            Args:
                record: a level5 lyftbag cam frame data dictionary

            Returns:
                dict of new MAS protobuf messages for cameras
        """
        protos__ = {}
        for cam in record.keys():
            pd = image_proto.VideoDataProto()
            pd.host.host_type = 1
            pd.device.camera_id = cam

            ts_list = sorted(list(record[cam].keys()))
            for ts in ts_list:
                im = image_proto.ImageTopicProto()
                im.host_state.timestamp_ns = ts
                im.image.depth = 3
                payload = record[cam][ts]
                if payload['compression_format'] == 'COMPRESSION_FORMAT_JPEG':
                    im.image.format = 1
                elif payload['compression_format'] == 'COMPRESSION_FORMAT_HEVC_IFRAME':
                    im.image.format = 4
                im.image.data = base64.b64decode(payload['data'])
                pd.image_data.append(im)
            
            protos__[cam] = {}
            protos__[cam]['proto'] = pd
            if len(ts_list)>0:
                protos__[cam]['ts'] = [ts_list[0], ts_list[-1]]
            else:
                protos__[cam]['ts'] = []

        return protos__
    
    def _proto_file(self):
        """ get the filename of a proto batch """
        return "{}_batch_{}.proto".format(self._dataset_name, self._batch_id)
    
    def _gen_proto_record(self, package: dict):
        """ write video proto message to a .proto file """
        for cam in package.keys():
            if not package[cam]['ts']: continue
            proto_key = "{}_{}_{}.proto".format(
                cam, package[cam]['ts'][0], package[cam]['ts'][1])
            proto_file = os.path.join(self._workspace, proto_key)
            with open(proto_file, "wb") as f:
                bytesAsString = package[cam]['proto'].SerializeToString()
                f.write(bytesAsString)
            if self._bucket_dst:
                target_key = os.path.join(self._s3_key, proto_key)
                self.aws.upload_file(self._bucket_dst, proto_file, target_key)
                os.remove(proto_file)
            else:
                shutil.move(proto_file, os.path.join(self._datadst, proto_key))

    def pack_protos(self):
        """ Process mas data examples into proto format in batches
            For child classes implemented for different raw datasets,
            this method shall be overridden.
        """
        self._workspace = tempfile.mkdtemp()
        pbar = tqdm.tqdm(total=1000)
        for rec in self._record_list:
            self._gen_proto_record(
                self._add_to_proto(self.get_data_from_files(rec))
            )
            pbar.update(int(1.0/self._n_records*1000))
        shutil.rmtree(self._workspace)
        print("///: Totally {} lyftbags converted to {}".format(
            self._n_records, self._datadst)
        )

    def read_one_proto(self, proto_file):
        """ Display one proto contents

            Args:
            proto_file: protobuf record filename or url
        """
        import cv2
        import numpy as np
        workspace_ = None
        if self.aws.S3_BUCKET_BASE in proto_file:
            workspace_ = tempfile.mkdtemp()
            bucket_name, s3_key = self.aws.url_to_bnk(proto_file, False)
            proto_file = os.path.join(workspace_, ntpath.basename(s3_key))
            self.aws.download_file(bucket_name, s3_key, proto_file)
        if not os.path.isfile(proto_file):
            print("///: protobuf reocord DO NOT exist!")
            return
        with open(proto_file, "rb") as f:
            proto_data = image_proto.VideoDataProto().FromString(f.read())

        print("///: Data from {} device-{}".format(
            proto_data.host.host_type, proto_data.device.camera_id))

        n_frames = 0
        for frame in proto_data.image_data:
            n_frames += 1
            im = cv2.imdecode(np.frombuffer(frame.image.data, dtype=np.uint8), -1)
            print("///: Frame {} timestamp@-{}".format(
                n_frames, frame.host_state.timestamp_ns))
            print("///: Format-({}) and shape: {}".format(
                frame.image.format, im.shape))
            cv2.imshow("frame", im)
            key = cv2.waitKey(100)
            if key==27: break

        print("///: loading successfully")
        if workspace_: shutil.rmtree(workspace_)
