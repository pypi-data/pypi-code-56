from copy import deepcopy

from doublex import *
from doublex_expects import *
from expects import *
from mamba import *
from sdcclient import SdScanningClient

from sdccli.usecases.scanning import image as use_case

IMAGE_DIGEST = "sha256:6cc44ba161425a205443aba8439052d1d25d6073e24d13efdc2b54a2b3bbb835"
IMAGE_TAG = "docker.io/sysdiglabs/dummy-vuln-app:latest"

with description("Scanning images") as self:
    with before.each:
        self.scanning = Spy(SdScanningClient)
        when(self.scanning).list_images().returns(
            (True, [self.test_scanning_image(), self.test_old_scanning_image()])
        )
        when(self.scanning).query_image_content(ANY_ARG).returns(
            (True, "ImageContent")
        )
        when(self.scanning).query_image_metadata(ANY_ARG).returns(
            (True, "ImageMetadata")
        )
        when(self.scanning).query_image_vuln(ANY_ARG).returns(
            (True, "ImageVulns")
        )


    with it("lists all the images"):
        res = use_case.list_scanning_images(self.scanning, show_all=True)

        expect(res).to(contain(self.test_scanning_image()))
        expect(res).to(contain(self.test_old_scanning_image()))

    with it("lists only the latest the images"):
        res = use_case.list_scanning_images(self.scanning, show_all=False)

        expect(res).to(contain(self.test_scanning_image()))
        expect(res).to_not(contain(self.test_old_scanning_image()))

    with it("is able to query the image content"):
        content = use_case.query_image_content(self.scanning, IMAGE_TAG, "os")

        expect(content).to_not(be_none)

    with it("does not fail to retrieve the image content with the correct content type provided"):
        expect(lambda: use_case.query_image_content(self.scanning, IMAGE_TAG, "os")).to_not(raise_error(Exception))
        expect(lambda: use_case.query_image_content(self.scanning, IMAGE_TAG, "npm")).to_not(raise_error(Exception))
        expect(lambda: use_case.query_image_content(self.scanning, IMAGE_TAG, "gem")).to_not(raise_error(Exception))
        expect(lambda: use_case.query_image_content(self.scanning, IMAGE_TAG, "files")).to_not(raise_error(Exception))

    with it("does not fail to retrieve the image content with the correct content type provided"):
        expect(lambda: use_case.query_image_metadata(self.scanning, IMAGE_TAG, "manifest")).to_not(
            raise_error(Exception))
        expect(lambda: use_case.query_image_metadata(self.scanning, IMAGE_TAG, "dockerfile")).to_not(
            raise_error(Exception))
        expect(lambda: use_case.query_image_metadata(self.scanning, IMAGE_TAG, "docker_history")).to_not(
            raise_error(Exception))

    with it("does not fail to retrieve the vulnerabilities with the correct vulnerability type provided"):
        expect(lambda: use_case.query_image_vuln(self.scanning, IMAGE_TAG, "os")).to_not(
            raise_error(Exception))
        expect(lambda: use_case.query_image_vuln(self.scanning, IMAGE_TAG, "non-os")).to_not(
            raise_error(Exception))
        expect(lambda: use_case.query_image_vuln(self.scanning, IMAGE_TAG, "all")).to_not(
            raise_error(Exception))

    with it("fails when querying the image content with incorrect content type"):
        expect(lambda: use_case.query_image_content(self.scanning, IMAGE_TAG, "foo")).to(
            raise_error(ValueError, "Incorrect content type provided 'foo', must be one of: [os, npm, gem, files]")
        )

    with it("fails when querying the image metadata with incorrect metadata parameter"):
        expect(lambda: use_case.query_image_metadata(self.scanning, IMAGE_TAG, "foo")).to(
            raise_error(ValueError,
                        "Incorrect metadata type provided 'foo', must be one of: [manifest, dockerfile, docker_history]")
        )

    with it("fails when querying the vulnerabilities with incorrect vulnerability type"):
        expect(lambda: use_case.query_image_vuln(self.scanning, IMAGE_TAG, vuln_type="foo")).to(
            raise_error(ValueError, "Incorrect vulnerability type provided, must be one of: [os, non-os, all]")
        )


    def test_scanning_image(self):
        return {
            "analysis_status": "analyzed",
            "analyzed_at": "2020-05-02T12:15:19Z",
            "annotations": {"added-by": "sysdig-cli"},
            "created_at": "2020-05-02T12:12:44Z",
            "imageDigest": IMAGE_DIGEST,
            "image_content": {
                "metadata": {
                    "arch": "amd64",
                    "distro": "debian",
                    "distro_version": "9",
                    "dockerfile_mode": "Guessed",
                    "image_size": 576972800,
                    "layer_count": 4
                }
            },
            "image_detail": [
                {
                    "created_at": "2020-05-02T12:12:44Z",
                    "digest": IMAGE_DIGEST,
                    "dockerfile": "RlJPTSBzY3JhdGNoCkFERCBmaWxlOjk3ODhiNjFkZTM1MzUxNDg5OTU4YzhhYmUxNzU5NjA4NjU3OTAzMTJjZWQ1NjQ1OGNhYTk0Y2NiMGI5YmI3NTcgaW4gLyAKQ01EIFsiYmFzaCJdClJVTiAvYmluL3NoIC1jIGFwdCB1cGRhdGUgJiYgYXB0IGluc3RhbGwgcHl0aG9uLXBpcCBweXRob24tbnVtcHkgb3BlbnNzaC1zZXJ2ZXIgLXkgJiYgcm0gLXJmIC92YXIvbGliL2FwdApSVU4gL2Jpbi9zaCAtYyBwaXAgaW5zdGFsbCBmbGFzawpDT1BZIGZpbGU6OWNiZmFhN2U2YjMzMzg1MTAxNjAwOWVkOTVhNmY3M2NkMGY0ZjljYjQ3NDMzMzA0MDliZDFlZTczZDBmOGUzMSBpbiAvYXBwLnB5IApFWFBPU0UgMjIgNTAwMApFTlRSWVBPSU5UIFsicHl0aG9uIiAiLi9hcHAucHkiXQo=",
                    "fulldigest": "docker.io/sysdiglabs/dummy-vuln-app@sha256:6cc44ba161425a205443aba8439052d1d25d6073e24d13efdc2b54a2b3bbb835",
                    "fulltag": IMAGE_TAG,
                    "imageDigest": IMAGE_DIGEST,
                    "imageId": "8a8bfed71406ff3498bbe71c67d64d827b2ba84498b68a07f78a8a8d798e650b",
                    "last_updated": "2020-05-02T12:15:19Z",
                    "registry": "docker.io",
                    "repo": "sysdiglabs/dummy-vuln-app",
                    "tag": "latest",
                    "tag_detected_at": "2020-05-02T12:12:44Z",
                    "userId": "userID"
                }
            ],
            "image_status": "active",
            "image_type": "docker",
            "last_updated": "2020-05-02T12:15:19Z",
            "parentDigest": IMAGE_DIGEST,
            "userId": "userID"
        }


    def test_old_scanning_image(self):
        image = deepcopy(self.test_scanning_image())
        image["image_detail"][0].update({"created_at": "2019-05-02T12:12:44Z"})
        return image
