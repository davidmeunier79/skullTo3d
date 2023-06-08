#!/usr/bin/bash

########### Variables #############
subject=Ebdo
data_path="/envau/work/nit/users/sghari.a/Analysis/segmentation_petra_ebdo/27_03_23"
k_dil_ero_headmask=5
thr_head=125
uthr_skull=120
k_dil_ero_final=7
min_size=100

#1111111 IMAGE_CROP for Galileo ##############
xmin=108, xmax=328, xsize=220
ymin=78, ymax=318, ysize=240
zmin=240, zmax=408, zsize=168
#_______________________________________________________________________#
#_______________________________________________________________________#
#_______________________________________________________________________#
#_______________________________________________________________________#
fslroi ${data_path}/sub-${subject}_ses-01_rec-mean_petra.nii.gz ${data_path}/sub-${subject}_ses-01_rec-mean_petra_roi5.nii.gz ${xmin} ${xsize} ${ymin} ${ysize} ${zmin} ${zsize}

#TEST_TEST_TEST_TEST commandes pour tester des paramètres sans lanceer le script
fslroi sub-Galileo_ses-01_rec-mean_petra.nii.gz sub-Galileo_ses-01_rec-mean_petra_roi5.nii.gz 108 220 78 240 240 168

fast -o sub-Galileo_ses-01_rec-mean_petra_roi5_bias.nii.gz -l 3 -b -B sub-Galileo_ses-01_rec-mean_petra_roi5.nii.gz

fslmaths sub-Galileo_ses-01_rec-mean_petra_roi5_bias_restore.nii.gz -thr 280 -bin sub-Galileo_ses-01_restore_head_280.nii.gz

#-bin est une etape seule dans nipype

#nettoyer avec skull_filter2.0

fslmaths sub-Galileo_ses-01_restore_head_280.nii.gz -kernel boxv 5 -dilD sub-Galileo_ses-01_restore_head_280_dilD5.nii.gz

fslmaths sub-Galileo_ses-01_restore_head_280_dilD5.nii.gz -fillh sub-Galileo_ses-01_restore_head_280_dilD5_fillh.nii.gz

#nettoyer avec skull_filter2.0 (jai pas vraiment verifier si ca sert a quelque chose, il faut que je le fasse en mode bash pour decider de garder cette etape dans le pipeline ou pas)

fslmaths sub-Galileo_ses-01_restore_head_280_dilD5.nii.gz -kernel boxv 5 -ero sub-Galileo_ses-01_restore_head_280_dilD5_fillh_ero5.nii.gz

fslmaths sub-Galileo_ses-01_rec-mean_petra_roi5_bias_restore.nii.gz -mas sub-Galileo_ses-01_restore_head_280_dilD5_fillh_ero5.nii.gz sub-Galileo_ses-01_rec-mean_petra_roi5_bias_restore_masked.nii.gz

fslmaths sub-Galileo_ses-01_rec-mean_petra_roi5_bias_restore_masked.nii.gz -uthr 250 sub-Galileo_ses-01_rec-mean_petra_roi5_bias_restore_masked_uthr250.nii.gz

/home/sghari.a/.conda/envs/skull_extract/bin/python /envau/work/nit/users/sghari.a/CODE/script_python/skull_filter2.0.py /envau/work/nit/users/sghari.a/Analysis/segmentation_petra_galileo/17_03_23/ sub-Galileo_ses-01_rec-mean_petra_roi5_bias_restore_masked_uthr250.nii.gz 100

fslmaths new_GCC_sub-Galileo_ses-01_rec-mean_petra_roi5_bias_restore_masked_uthr250.nii.gz -kernel boxv 5 -dilD new_GCC_sub-Galileo_ses-01_rec-mean_petra_roi5_bias_restore_masked_uthr250_dilD5.nii.gz

#A voir s'il faut mettre un fillh entre la dil et l'ero (apparement pour Galileo non ; en fait si)(meme pour ebdo)AUSSI(pas besoin de nettoyer avec skull_filter2.0)

fslmaths new_GCC_sub-Galileo_ses-01_rec-mean_petra_roi5_bias_restore_masked_uthr250_dilD5.nii.gz -kernel boxv 5 -ero new_GCC_sub-Galileo_ses-01_rec-mean_petra_roi5_bias_restore_masked_uthr250_dilD5_ero5.nii.gz.nii.gz

#PARTIE MASKING WITH BRAINMASK_




#_______________________________________________________________________#
#_______________________________________________________________________#
#_______________________________________________________________________#
#_______________________________________________________________________#
#_______________________________________________________________________#




                        #2222222 RESTORE(BIAS)_of_ORIGINAL_IMAGE #######
#fast -o ${data_path}/sub-${subject}_ses-01_rec-mean_petra_roi5_bias.nii.gz -l 3 -b -B ${data_path}/sub-${subject}_ses-01_rec-mean_petra_roi5.nii.gz



                        #3333333 HEAD_MASK_GENERATION #######
#fslmaths ${data_path}/sub-${subject}_ses-01_rec-mean_petra_roi5_bias_restore.nii.gz -thr ${thr_head} -bin ${data_path}/sub-${subject}_ses-01_restore_head_${thr_head}.nii.gz

#fslmaths ${data_path}/sub-${subject}_ses-01_restore_head_${thr_head}.nii.gz -kernel boxv ${k_dil_ero_headmask} -dilD -ero ${data_path}/sub-${subject}_ses-01_restore_head_${thr_head}_dilD${k_dil_ero_headmask}_ero${k_dil_ero_headmask}.nii.gz





                        ######## RECIPROCAL & LOG ####### 
#fslmaths sub-${subject}_ses-01_rec-mean_petra_roi5_bias_restore.nii.gz -recip -log sub-${subject}_ses-01_rec-mean_petra_roi5_bias_restore_recip_log.nii.gz

#fslmaths sub-${subject}_ses-01_rec-mean_petra_roi5_bias_restore_recip_log.nii.gz -mas sub-${subject}_ses-01_restore_head_${thr_head}_dilD${k_dil_ero_headmask}_ero${k_dil_ero_headmask}.nii.gz sub-${subject}_ses-01_rec-mean_petra_roi5_bias_restore_recip_log_masked.nii.gz



                        #44444444 MASKING_THE_RESTORED_IMAGE ###############
#fslmaths ${data_path}/sub-${subject}_ses-01_rec-mean_petra_roi5_bias_restore.nii.gz -mas ${data_path}/sub-${subject}_ses-01_restore_head_${thr_head}_dilD${k_dil_ero_headmask}_ero${k_dil_ero_headmask}.nii.gz ${data_path}/sub-${subject}_ses-01_rec-mean_petra_roi5_bias_restore_masked.nii.gz



                        #55555555 THRESHOLDING_THE_MASKED_IMAGE ####### 
#fslmaths ${data_path}/sub-${subject}_ses-01_rec-mean_petra_roi5_bias_restore_masked.nii.gz -uthr ${uthr_skull} ${data_path}/sub-${subject}_ses-01_rec-mean_petra_roi5_bias_restore_masked_uthr${uthr_skull}.nii.gz



                        #66666666 NETTOYER AVANT
#skull_filter.py
#/home/sghari.a/.conda/envs/skull_extract/bin/python /envau/work/nit/users/sghari.a/CODE/script_python/skull_filter.py /envau/work/nit/users/sghari.a/Analysis/Segmentation_petra_galelio/16_03_23/ sub-${subject}_ses-01_rec-mean_petra_roi5_bias_restore_masked_uthr${uthr_skull}.nii.gz ${min_size}
#skull_filter2.0.py
#/home/sghari.a/.conda/envs/skull_extract/bin/python /envau/work/nit/users/sghari.a/CODE/script_python/skull_filter2.0.py /envau/work/nit/users/sghari.a/Analysis/Segmentation_petra_galelio/16_03_23/ sub-${subject}_ses-01_rec-mean_petra_roi5_bias_restore_masked_uthr${uthr_skull}.nii.gz ${min_size}



                        #77777777 CLOSING_HOLES ####### meilleurs résultats avec kernel 7 

#fslmaths ${data_path}/new_${min_size}_sub-${subject}_ses-01_rec-mean_petra_roi5_bias_restore_masked_uthr${uthr_skull}.nii.gz -kernel boxv ${k_dil_ero_final} -dilD -fillh -ero ${data_path}/new_${min_size}_sub-${subject}_ses-01_rec-mean_petra_roi5_bias_restore_masked_uthr${uthr_skull}_dilD${k_dil_ero_final}_fillh_ero${k_dil_ero_final}.nii.gz

#A voir s'il faut mettre un fillh entre la dil et l'ero (MEILLEUR RESULTAT avec fillh)

                        ##############  BrainMasking   ##########



                        ########   MESH_GENERATION   ########
                        
#module load nii2mesh et une fois que tu as fait ca, tu lances la commande avec nii2mesh mon_fichier.nii.gz mon_fichier.stl                        
