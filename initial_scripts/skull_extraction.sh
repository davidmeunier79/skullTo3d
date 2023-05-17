#!/usr/bin/bash

#script written by Julien SEIN, David MEUNIER & Adam SGHARI for skull_extraction from MRI PETRA Images
 
data_path="/envau/work/nit/users/sghari.a/Analysis/10_03_23/"
k_dil_ero=5
thr_head=125
thr_skull=120


fast -o ${data_path}/sub-Ebdo_ses-01_rec-mean_petra_roi5_bias.nii.gz -l 3 -b -B ${data_path}/sub-Ebdo_ses-01_rec-mean_petra_roi5.nii.gz

fslmaths ${data_path}/sub-Ebdo_ses-01_rec-mean_petra_roi5_bias_restore.nii.gz -thr ${thr_head} -bin ${data_path}/sub-Ebdo_ses-01_restore_head_125.nii.gz

fslmaths ${data_path}/sub-Ebdo_ses-01_restore_head_125.nii.gz -kernel boxv 5 -dilD ${data_path}/sub-Ebdo_ses-01_restore_head_125_dilD5.nii.gz

fslmaths ${data_path}/sub-Ebdo_ses-01_restore_head_125_dilD5.nii.gz -kernel boxv 5 -ero ${data_path}/sub-Ebdo_ses-01_restore_head_125_dilD5_ero5.nii.gz

#fslmaths sub-Ebdo_ses-01_rec-mean_petra_roi5_bias_restore.nii.gz -recip -log sub-Ebdo_ses-01_rec-mean_petra_roi5_bias_restore_recip_log.nii.gz

#fslmaths sub-Ebdo_ses-01_rec-mean_petra_roi5_bias_restore_recip_log.nii.gz -mas sub-Ebdo_ses-01_restore_head_125_dilD5_ero5.nii.gz sub-Ebdo_ses-01_rec-mean_petra_roi5_bias_restore_recip_log_masked.nii.gz

fslmaths ${data_path}/sub-Ebdo_ses-01_rec-mean_petra_roi5_bias_restore.nii.gz -mas ${data_path}/${data_path}/sub-Ebdo_ses-01_restore_head_125_dilD5_ero5.nii.gz sub-Ebdo_ses-01_rec-mean_petra_roi5_bias_restore_masked.nii.gz

fslmaths ${data_path}/sub-Ebdo_ses-01_rec-mean_petra_roi5_bias_restore_masked.nii.gz -uthr 120 ${data_path}/sub-Ebdo_ses-01_rec-mean_petra_roi5_bias_restore_masked_uthr120.nii.gz



