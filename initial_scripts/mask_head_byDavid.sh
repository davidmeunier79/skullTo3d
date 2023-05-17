#!/usr/bin/bash

res_path="/envau/work/nit/users/meunier.d/Data_BIDS/PrimeDE_ucdavisBIDS/derivatives/head_masks"

mkdir -p ${res_path}

sub=$1
ses=$2

T1_intens=30
k_dil_ero=5
min_islands=100

skull_thr=3.0
k_dil_ero_skull=3

data_path="/envau/work/nit/users/meunier.d/Data_BIDS/PrimeDE_ucdavisBIDS/sub-${sub}/ses-${ses}/anat"

echo "**** creating head mask ${sub} ${ses}****"

echo "* threshold ${T1_intens} and binarize"
fslmaths ${data_path}/sub-${sub}_ses-${ses}_run-1_T1w.nii.gz -thr ${T1_intens} -bin ${res_path}/sub-${sub}_ses-${ses}_run-1_thr_${T1_intens}.nii.gz

echo "* GCC headmask"
python skull_filter.py ${res_path} sub-${sub}_ses-${ses}_run-1_thr_${T1_intens}.nii.gz

echo "* erode/fill/dilate ${k_dil_ero} headmask"
fslmaths ${res_path}/new_GCC_sub-${sub}_ses-${ses}_run-1_thr_${T1_intens}.nii.gz -kernel boxv ${k_dil_ero} -dilD -fillh -ero ${res_path}/sub-${sub}_ses-${ses}_run-1_headmask.nii.gz
echo "* done headmask"

echo "**** creating skullmask ****"
# #on repart de l'image d'origin et on inverse (et *-1)
echo "* restart from orig T1w image and log inverse *-1"
fslmaths ${data_path}/sub-${sub}_ses-${ses}_run-1_T1w.nii.gz -recip -log -mul -1 -uthr ${skull_thr} ${res_path}/sub-${sub}_ses-${ses}_run-1_thr_${T1_intens}_uthr_${skull_thr}.nii.gz

# on masque l'image avec le masque de tete
echo "* threshold image with headmask ${sub} ${ses}"
fslmaths ${res_path}/sub-${sub}_ses-${ses}_run-1_thr_${T1_intens}_uthr_${skull_thr}.nii.gz -mas ${res_path}/sub-${sub}_ses-${ses}_run-1_headmask.nii.gz -bin ${res_path}/sub-${sub}_ses-${ses}_run-1_thr_${T1_intens}_uthr_${skull_thr}_masked.nii.gz

echo "* GCC skullmask"
python skull_filter.py ${res_path} sub-${sub}_ses-${ses}_run-1_thr_${T1_intens}_uthr_${skull_thr}_masked.nii.gz

echo "* erode/fill/dilate ${k_dil_ero_skull} skullmask"
fslmaths ${res_path}/new_GCC_sub-${sub}_ses-${ses}_run-1_thr_${T1_intens}_uthr_${skull_thr}_masked.nii.gz -kernel boxv ${k_dil_ero_skull} -dilD -fillh -ero  ${res_path}/sub-${sub}_ses-${ses}_run-1_skullmask.nii.gz

echo "* deleting intermediate files"
rm ${res_path}/*thr_${T1_intens}*