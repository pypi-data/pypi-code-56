from enum import Enum

from django.db import models

from .session import Session
from .stimulus import Stimulus


class DataAcquisitionMethod(models.Model):
    class TYPE(Enum):
        behavioral = ('behav', 'Behavioral')
        biological = ('bio', 'Biological samples')
        eeg = ('eeg', 'Electroencephalography')
        meg = ('meg', 'Magnetoencephalography')
        microscopy = ('micro', 'Microscopy data')
        mri = ('mri', 'Magnetic resonance imaging')
        nirs = ('nirs', 'Near-Infrared Spectroscopy')
        pause = ('pause', 'Pause')
        pet = ('pet', 'Positron-emission tomography')
        physiological = ('phys', 'Physiological measures')
        questionnaire = ('quest', 'Questionnaire')
        screening = ('screen', 'Screening')

        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]

    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField()

    stimulus = models.ForeignKey(Stimulus, on_delete=models.SET_NULL, null=True)

    type = models.CharField(max_length=16, choices=[x.value for x in TYPE])

    location = models.CharField(max_length=126)


class Behavioral(models.Model):
    method = models.ForeignKey(DataAcquisitionMethod, on_delete=models.CASCADE,
                               related_name='behaviorals')


class Biological(models.Model):
    method = models.ForeignKey(DataAcquisitionMethod, on_delete=models.CASCADE,
                               related_name='biologicals')


class EEG(models.Model):
    method = models.ForeignKey(DataAcquisitionMethod, on_delete=models.CASCADE, related_name='eeg')


class MEG(models.Model):
    method = models.ForeignKey(DataAcquisitionMethod, on_delete=models.CASCADE, related_name='meg')


class Microscopy(models.Model):
    method = models.ForeignKey(DataAcquisitionMethod, on_delete=models.CASCADE,
                               related_name='microscopys')


class MRI(models.Model):
    method = models.ForeignKey(DataAcquisitionMethod, on_delete=models.CASCADE, related_name='mri')


class NIRS(models.Model):
    method = models.ForeignKey(DataAcquisitionMethod, on_delete=models.CASCADE, related_name='nirs')


class Pause(models.Model):
    method = models.ForeignKey(DataAcquisitionMethod, on_delete=models.CASCADE,
                               related_name='pause')


class PET(models.Model):
    method = models.ForeignKey(DataAcquisitionMethod, on_delete=models.CASCADE, related_name='pet')


class Physiological(models.Model):
    method = models.ForeignKey(DataAcquisitionMethod, on_delete=models.CASCADE,
                               related_name='physiologicals')


class Questionnaire(models.Model):
    method = models.ForeignKey(DataAcquisitionMethod, on_delete=models.CASCADE,
                               related_name='questionnaires')


class Screening(models.Model):
    method = models.ForeignKey(DataAcquisitionMethod, on_delete=models.CASCADE,
                               related_name='screenings')
