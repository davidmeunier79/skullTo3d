#!/usr/bin/bash

#script written by Adam SGHARI, David MEUNIER & Julien SEIN for the registration/resampling of the brain_mask into the skull_extraction (macaque subjects only / MRI PETRA only)

########### Variables #############
subject=Galileo
data_path="/envau/work/nit/users/sghari.a/Analysis/segmentation_petra_galileo/23_03_23_masking_with_brains_mask"
#k_dil_ero_headmask=5
#thr_head=125
#uthr_skull=120
#k_dil_ero_final=7
#min_size=100


#1111111 IMAGE_CROP for Ebdo ##############
xmin=85-42(why?i dont remeber), xmax=248, xsize=163
ymin=54, ymax=237, ysize=183
zmin=188, zmax=322, zsize=134
#1111111 IMAGE_CROP for Galileo ##############
#xmin=108, xmax=328, xsize=220
#ymin=78, ymax=318, ysize=240
#zmin=240, zmax=408, zsize=168

fslroi ${data_path}/sub-${subject}_ses-01_rec-mean_petra.nii.gz ${data_path}/sub-${subject}_ses-01_rec-mean_petra_roi5.nii.gz ${xmin} ${xsize} ${ymin} ${ysize} ${zmin} ${zsize}

#!!!!!# POUR GALILEO L'ETAPE DU CROP N'EST PAS NECESSAIRE LE RESAMPLING SUFFIT A RECALER LE BRAIN_MASK SUR L'EXTRACTION DU CRANE FINAL POUR GALILEO

#fslroi sub-Ebdo_ses-01_space-native_desc-brain_mask.nii.gz sub-Ebdo_ses-01_space-native_desc-brain_mask_roi5.nii.gz 43 163 54 183 188 134

#reg_resample -ref new_100_sub-Ebdo_ses-01_rec-mean_petra_roi5_bias_restore_masked_uthr120_dilD7_fillh_ero7.nii.gz -flo sub-Ebdo_ses-01_space-native_desc-brain_mask_roi5.nii.gz -inter 0 -res sub-Ebdo_ses-01_space-native_desc-brain_mask_roi5_res.nii.gz

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

Parameters
Reference image name: new_100_sub-Ebdo_ses-01_rec-mean_petra_roi5_bias_restore_masked_uthr120_dilD7_fillh_ero7.nii.gz
	163x183x134 voxels, 1 volumes
	0.5x0.5x0.5 mm
Floating image name: sub-Ebdo_ses-01_space-native_desc-brain_mask_roi5.nii.gz
	163x183x134 voxels, 1 volumes
	0.5x0.5x0.5 mm
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

[NiftyReg] Resampled image has been saved: sub-Ebdo_ses-01_space-native_desc-brain_mask_roi5_res.nii.gz

#fslmaths sub-Ebdo_ses-01_space-native_desc-brain_mask_roi5_res.nii.gz -kernel boxv 9 (plutot 15 d'apres les derniers traitement Ebdo) -dilD sub-Ebdo_ses-01_space-native_desc-brain_mask_roi5_res_dilD9.nii.gz

#fslmaths new_100_sub-Ebdo_ses-01_rec-mean_petra_roi5_bias_restore_masked_uthr120_dilD7_fillh_ero7.nii.gz -mas sub-Ebdo_ses-01_space-native_desc-brain_mask_roi5_res_dilD9.nii.gz new_100_sub-Ebdo_ses-01_rec-mean_petra_roi5_bias_restore_masked_uthr120_dilD7_fillh_ero7_brainmasked.nii.gz

