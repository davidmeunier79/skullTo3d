#!/usr/bin/bash

fast -o avg_sub-Riesling_ses-2020_run-01_T1w_res_ROI_corrected_bias.nii.gz -l 3 -b -B avg_sub-Riesling_ses-2020_run-01_T1w_res_ROI_corrected.nii.gz

fast -o avg_sub-Riesling_ses-2020_run-01_T1w_res_ROI_corrected_bias_restore_bias.nii.gz -l 3 -b -B avg_sub-Riesling_ses-2020_run-01_T1w_res_ROI_corrected_bias_restore.nii.gz

#rename the output above sub-Riesling_T1w_restore2fois.nii.gz

#then pad it (Dilate & Erode reasons)
python resize_mri_riesling_t1.py sub-Riesling_T1w_restore2fois.nii.gz

#create head_mask
fslmaths padded_sub-Riesling_T1w_restore2fois.nii.gz -thr 60 -bin padded_sub-Riesling_T1w_restore2fois_thr60bin.nii.gz

#
python skull_filter2_T1.py padded_sub-Riesling_T1w_restore2fois_thr60bin.nii.gz

###
fslmaths new_GCC_padded_sub-Riesling_T1w_restore2fois_thr60bin.nii.gz -kernel boxv 3 -dilD -fillh -ero sub-Riesling_T1w_headmask.nii.gz
#!!!!! il faut dil et ero a plus que 9 voire plus que 15
#à 9 c'est bon pour l'instant
#à 5 ça marche aussi

#headmaskin'
fslmaths padded_sub-Riesling_T1w_restore2fois.nii.gz -mas sub-Riesling_T1w_headmask9.nii.gz padded_sub-Riesling_T1w_restore2fois_hmasked9.nii.gz

#recip log mul-1
fslmaths padded_sub-Riesling_T1w_restore2fois_hmasked9.nii.gz -recip -log -mul -1 padded_sub-Riesling_T1w_restore2fois_hmasked9_recip_log_mul-1.nii.gz

#uthr 4, pour riesling 3.7

#filter

#dil fill ero

#BIN & filter
fslmaths padded_sub-Riesling_T1w_restore2fois_hmasked9_recip_log_mul-1_-uthr4_dil5ero.nii.gz -bin padded_sub-Riesling_T1w_restore2fois_hmasked9_recip_log_mul-1_-uthr4_dil5ero_bin.nii.gz ; python skull_filter2_T1.py padded_sub-Riesling_T1w_restore2fois_hmasked9_recip_log_mul-1_-uthr4_dil5ero_bin.nii.gz
